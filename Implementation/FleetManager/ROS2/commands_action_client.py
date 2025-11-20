"""
This module implements a ROS 2 Action Client for drone command management, featuring:
- Multi-drone command handling
- Asynchronous goal management
- Feedback and result processing
- Thread-safe queue integration
- Concurrent logging

Classes
-------
CommandsActionClient
    ROS 2 Node managing action client communication with drones

Functions
---------
create_ros2_action_client
    Factory function for initializing ROS 2 components
main
    Main execution entry point
create_logger
    Configure concurrent-safe logging

Usage
------
Start action client::

    from ros2_action_client import create_ros2_action_client

    ros2_queue = queue.Queue()
    logger = create_logger('ROS2', 'ros2.log')
    client = create_ros2_action_client(ros2_queue, logger)
    client.send_goal(1, ["takeoff", "scan_area"])
"""

import json
import logging
from concurrent_log_handler import ConcurrentRotatingFileHandler
import rclpy
import queue
from rclpy.action import ActionClient
from rclpy.node import Node
from functools import partial
from rclpy.executors import MultiThreadedExecutor
import threading

from commands_action_interface.action import Commands


class CommandsActionClient(Node):
    """ROS 2 Action Client node for drone command management.

    Manages bidirectional communication with drone action servers including:
    - Goal submission tracking
    - Feedback processing
    - Result handling
    - Connection management

    :param ros2_action_queue: Thread-safe queue for action status updates
    :type ros2_action_queue: queue.Queue
    :param ros2_logger: Configured logger instance for ROS operations
    :type ros2_logger: logging.Logger

    :ivar _action_clients: Active drone action clients (drone_id → ActionClient)
    :vartype _action_clients: dict[int, ActionClient]
    """

    def __init__(self, ros2_action_queue, ros2_logger):
        """Initialize action client node with communication infrastructure."""
        super().__init__('commands_action_client')
        self._action_clients = {}  # Maps drone_id to ActionClient
        self.ros2_action_queue = ros2_action_queue
        self.ros2_logger = ros2_logger

    def send_goal(self, drone_id, commands_list):
        """Submit command sequence to target drone action server.

        :param drone_id: Unique drone identifier
        :type drone_id: int
        :param commands_list: Ordered command sequence for execution
        :type commands_list: list[str]
        :raises RuntimeError: If action server unavailable after timeout

        .. note::
            Creates new ActionClient for unrecognized drone IDs
            Maintains 2-second server connection timeout
        """
        if drone_id not in self._action_clients:
            action_client = ActionClient(
                self,
                Commands,
                f'drone{drone_id}/commands'  # Full topic: /droneX/commands
            )
            self._action_clients[drone_id] = action_client
        else:
            action_client = self._action_clients[drone_id]
        
        if not action_client.wait_for_server(timeout_sec=2.0):
            self.ros2_logger.error(f"[ROS2 Manager] - Drone {drone_id} server unavailable.")
            return
        
        goal_msg = Commands.Goal()
        goal_msg.commands_list = commands_list
        self.ros2_logger.info(f'[ROS2 Manager] - Sending commands to drone {drone_id}')

        send_goal_future = action_client.send_goal_async(
            goal_msg,
            feedback_callback=partial(self.feedback_callback, drone_id=drone_id)
        )
        send_goal_future.add_done_callback(
            partial(self.goal_response_callback, drone_id=drone_id)
        )

    def goal_response_callback(self, future, drone_id):
        """Handle action server goal acceptance/rejection.

        :param future: Pending goal submission future
        :type future: rclpy.task.Future
        :param drone_id: Target drone identifier
        :type drone_id: int
        """
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.ros2_logger.info(f"[ROS2 Manager] - Drone {drone_id}: Goal rejected.")
            self.ros2_action_queue.put(json.dumps([drone_id, 1]))
            return

        self.ros2_logger.info(f"[ROS2 Manager] - Drone {drone_id}: Goal accepted.")
        get_result_future = goal_handle.get_result_async()
        get_result_future.add_done_callback(
            partial(self.get_result_callback, drone_id=drone_id)
        )
        self.ros2_action_queue.put(json.dumps([drone_id, 0]))

    def get_result_callback(self, future, drone_id):
        """Process final command execution results.

        :param future: Completed result future
        :type future: rclpy.task.Future
        :param drone_id: Originating drone ID
        :type drone_id: int
        """
        result = future.result().result
        self.ros2_logger.info(f"[ROS2 Manager] - Drone {drone_id}: Result: {result.plan_result}")
        self.ros2_action_queue.put(json.dumps(result.plan_result))

    def feedback_callback(self, feedback_msg, drone_id):
        """Handle intermediate command execution updates.

        :param feedback_msg: ROS 2 feedback message
        :type feedback_msg: Commands.FeedbackMessage
        :param drone_id: Source drone identifier
        :type drone_id: int
        """
        feedback = feedback_msg.feedback
        self.ros2_logger.info(f"[ROS2 Manager] - Drone {drone_id}: Feedback: {feedback.command_status}")
        self.ros2_action_queue.put(json.dumps(feedback.command_status))


def create_ros2_action_client(ros2_action_queue, ros2_logger):
    """Initialize and configure ROS 2 action client infrastructure.

    :param ros2_action_queue: Shared queue for action status updates
    :type ros2_action_queue: queue.Queue
    :param ros2_logger: Configured logger instance
    :type ros2_logger: logging.Logger
    :return: Initialized action client node
    :rtype: CommandsActionClient

    .. note::
        Starts independent executor thread for ROS 2 node
        Sets up MultiThreadedExecutor for concurrent callbacks
    """
    
    rclpy.init()
    action_client = CommandsActionClient(ros2_action_queue, ros2_logger)

    executor = MultiThreadedExecutor()
    executor.add_node(action_client)

    thread = threading.Thread(target=executor.spin, daemon=True)
    thread.start()

    return action_client


def main(args=None):
    """Main execution entry point for standalone operation.

    :param args: ROS 2 initialization arguments
    :type args: list | None

    Example:
        Basic usage::
        
            $ python3 ros2_action_client.py
            [INFO][ROS2] - Sending commands to drone 1
            [INFO][ROS2] - Sending commands to drone 2
    """
    ros2_action_queue = queue.Queue()
    ros2_logger = create_logger('ROS2', 'Logs/ros2.log')
    rclpy.init(args=args)

    action_client = CommandsActionClient(ros2_action_queue, ros2_logger)

    # Example: Send goals to drones 1 and 2
    action_client.send_goal(1, ["command1", "command2"])
    action_client.send_goal(2, ["command3", "command4"])

    rclpy.spin(action_client)


def create_logger(logger_name, log_file):
    """Configure concurrent-safe logging with rotation.

    :param logger_name: Namespace for logger instance
    :type logger_name: str
    :param log_file: Path to primary log file
    :type log_file: str
    :return: Configured logger instance
    :rtype: logging.Logger

    Configuration:
    - 1MB log rotation with 5 backups
    - Concurrent write safety
    - Unified console/file formatting
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    file_handler = ConcurrentRotatingFileHandler(log_file, maxBytes=1000000, backupCount=5)
    console_handler = logging.StreamHandler()

    formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s]%(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


if __name__ == '__main__':
    main()