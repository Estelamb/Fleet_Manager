"""
This module implements a ROS 2 action server for drone command execution with:
- Multi-threaded command processing
- Real-time feedback publication
- Graceful shutdown handling
- Command queue integration

Classes
-------
CommandsActionServer
    ROS 2 node managing command execution lifecycle

Functions
---------
main
    Action server initialization and lifecycle management
"""

import sys
import time
import argparse

import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
import threading

from commands_action_interface.action import Commands
from src.commands_action_interface.src.commands_processor import process_command

class CommandsActionServer(Node):
    """ROS 2 action server for drone command execution management.

    :param drone_id: Unique drone identifier for namespacing
    :type drone_id: int
    :param drone_logger: Configured logger instance
    :type drone_logger: logging.Logger
    :param action_queue: Command execution status queue
    :type action_queue: queue.Queue

    :ivar _action_server: ROS 2 action server instance
    :vartype _action_server: rclpy.action.ActionServer
    """

    def __init__(self, drone_id, drone_logger, action_queue):
        """Initialize action server node with drone-specific configuration."""
        super().__init__(
            'commands_action_server', 
            namespace=f'drone{drone_id}',
            allow_undeclared_parameters=True
        )
        self.vehicle_id = drone_id
        self.drone_logger = drone_logger
        self.action_queue = action_queue
        self.latitude = 40.073670
        self.longitude = -4.612044
        
        self._action_server = ActionServer(
            self,
            Commands,
            'commands',
            self.execute_callback
        )
        self.drone_logger.info(f" - Action server started.")

    def execute_callback(self, goal_handle):
        """Process incoming command goals and manage execution lifecycle.
        
        :param goal_handle: Incoming goal request handle
        :type goal_handle: rclpy.action.ServerGoalHandle
        :return: Final command execution result
        :rtype: Commands.Result
        :raises Exception: On critical execution errors
        
        Lifecycle:
        1. Process each command in the goal request
        2. Publish real-time feedback
        3. Update vehicle position state
        4. Handle graceful shutdown requests
        """
        self.drone_logger.info(f" - Executing goal...")
        feedback_msg = Commands.Feedback()

        try:
            for command in goal_handle.request.commands_list:
                if not rclpy.ok():  # Check if shutdown was triggered
                    raise Exception(f" - Shutdown requested")
                
                command_id, command_data, latitude, longitude = process_command(command)
                
                if latitude != None and longitude != None:
                    self.latitude = latitude
                    self.longitude = longitude
                
                self.action_queue.put({'vehicle_status':'Running', 'latitude': self.latitude, 'longitude': self.longitude})
                command_status = [str(self.vehicle_id), str(1), str(command_id), str(command_data)]
                feedback_msg.command_status = command_status
                self.drone_logger.info(f' - Feedback: {feedback_msg.command_status}')
                goal_handle.publish_feedback(feedback_msg)
                time.sleep(1)
            
            goal_handle.succeed()
            self.action_queue.put({'vehicle_status':'Available', 'latitude': self.latitude, 'longitude': self.longitude})
            result = Commands.Result()
            result.plan_result = [str(self.vehicle_id), str(2)]
            return result
            
        except Exception as e:
            self.drone_logger.error(f' - Error during execution: {str(e)}')
            goal_handle.abort()
            raise

def main(args=None, drone_id=0, drone_logger=None):
    """Main execution flow for action server lifecycle management.
    
    :param args: ROS 2 initialization arguments
    :type args: list | None
    :param drone_id: Drone identifier for node configuration
    :type drone_id: int
    :param drone_logger: Configured logger instance
    :type drone_logger: logging.Logger
    
    Execution Flow:
    1. Initialize ROS context
    2. Configure multi-threaded executor
    3. Start executor in background thread
    4. Handle shutdown signals
    """
    rclpy.init(args=args)
    
    try:
        commands_action_server = CommandsActionServer(drone_id, drone_logger)
        executor = MultiThreadedExecutor()
        executor.add_node(commands_action_server)

        executor_thread = threading.Thread(target=executor.spin, daemon=True)
        executor_thread.start()

        # Keep main thread alive to handle signals
        try:
            while rclpy.ok():
                time.sleep(0.1)
        except KeyboardInterrupt:
            drone_logger.info(f" - Ctrl+C received, shutting down...")
        finally:
            executor.shutdown()
            commands_action_server.destroy_node()
            
    finally:
        rclpy.shutdown()

if __name__ == '__main__':
    """Command-line interface for action server execution."""
    parser = argparse.ArgumentParser(description='Drone Action Server')
    parser.add_argument('--drone_id', type=int, required=True,
                       help='ID of the drone (e.g., 1, 2)')
    args = parser.parse_args()
    
    try:
        main(drone_id=args.drone_id)
    except Exception as e:
        print(f"Error in main: {e}")
        sys.exit(1)