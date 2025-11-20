"""
gRPC ROS 2 Communication Module

.. module:: grpc_ros2
    :synopsis: Provides bidirectional gRPC communication for ROS 2 command execution

.. note::
    Features:
    - gRPC server for receiving drone plans from Mission Management
    - gRPC client for sending execution results back
    - Integrated ROS 2 action client
    - Thread-safe queue operations
    - Comprehensive logging and error handling
"""

from concurrent import futures
import json
import grpc
import time
import queue
import threading

import logging
from concurrent_log_handler import ConcurrentRotatingFileHandler

from GRPC.plan_pb2 import DronePlanResponse
from GRPC.plan_pb2_grpc import PlanCommunicationServicer, add_PlanCommunicationServicer_to_server
from GRPC.result_pb2 import DroneResultRequest
from GRPC.result_pb2_grpc import ResultCommunicationStub

from ROS2 import commands_action_client as action


class PlanCommunicationService(PlanCommunicationServicer):
    """gRPC service implementation for drone plan processing.

    :param action_client: Initialized ROS 2 action client
    :param ros2_logger: Configured logger instance
    """
    def __init__(self, action_client, ros2_logger):
        super().__init__()
        self.action_client = action_client
        self.ros2_logger = ros2_logger

    def SendPlan(self, request, context):
        """Process incoming drone plan requests.

        :param request: gRPC request containing serialized plan data
        :param context: gRPC connection context
        :return: gRPC response with processing confirmation
        :raises: grpc.RpcError for critical processing failures

        .. note::
            Expected request format:
            [drone_id: int, [command1: str, command2: str, ...]]
        """
        try:
            # Convert the gRPC request to a list
            drone_plan = list(request.drone_plan)
            self.ros2_logger.info(f"[gRPC ROS2] - Plan received from Mission Management")
            drone_plan_str = ''.join(drone_plan)
            drone_plan = json.loads(drone_plan_str)

            # Extract drone_id and raw_command_list
            drone_id = drone_plan[0]
            raw_commands_list = drone_plan[1]

            # Parse each command in the command_list and ensure it's a string[]
            commands_list = []
            for raw_command in raw_commands_list:
                # Parse the raw command and convert it to a string
                command = json.loads(raw_command.replace("'", '"'))  # Replace single quotes with double quotes
                commands_list.append(json.dumps(command))  # Convert the parsed command back to a JSON string

            # Send the goal to the action client
            self.action_client.send_goal(drone_id, commands_list)
            self.ros2_logger.info(f"[gRPC ROS2][Vehicle {drone_id}] - Goal sent")

            return DronePlanResponse(confirmation=f"Plan {drone_id} received and sent")
        except Exception as e:
            self.ros2_logger.error(f"[gRPC ROS2] - Error in SendPlan: {e}", exc_info=True)
            return DronePlanResponse(confirmation="Error processing plan")


def run_ros2_server(action_client, ros2_logger):
    """Start and manage gRPC server instance.
    
    :param action_client: Initialized ROS 2 action client
    :param ros2_logger: Configured logger instance
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_PlanCommunicationServicer_to_server(
        PlanCommunicationService(action_client, ros2_logger), server)
    server.add_insecure_port('[::]:50099')
    server.start()
    ros2_logger.info("[gRPC ROS2] - Server started")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


def run_ros2_client(ros2_action_queue, ros2_logger):
    """Handle drone result transmission to Mission Management.
    
    :param ros2_action_queue: Thread-safe result queue
    :param ros2_logger: Configured logger instance
    """
    channel = grpc.insecure_channel('localhost:50070')
    stub = ResultCommunicationStub(channel)

    while True:
        try:
            drone_result = ros2_action_queue.get()
            ros2_logger.info(f"[gRPC ROS2] - Sending drone result to Mission Management")
            response = stub.SendResult(DroneResultRequest(drone_result=drone_result))
            ros2_logger.info(f"[gRPC ROS2] - ACK received from Mission Management")
        except queue.Empty:
            time.sleep(0.1)
        except grpc.RpcError as e:
            ros2_logger.error(f"[gRPC ROS2] - Connection error: {e}")
            time.sleep(1)


def start_grpc_ros2(ros2_action_queue: queue.Queue, ros2_logger):
    """Initialize and start ROS 2 communication infrastructure.
    
    :param ros2_action_queue: Shared action/results queue
    :param ros2_logger: Configured logger instance
    """
    action_client = action.create_ros2_action_client(ros2_action_queue = ros2_action_queue, ros2_logger = ros2_logger)

    server_ros2_thread = threading.Thread(target=run_ros2_server, args=(action_client, ros2_logger,))
    client_ros2_thread = threading.Thread(target=run_ros2_client, args=(ros2_action_queue, ros2_logger,))

    server_ros2_thread.daemon = True
    client_ros2_thread.daemon = True

    server_ros2_thread.start()
    client_ros2_thread.start()


def create_logger(logger_name, log_file):
    """Configure concurrent-safe logging system.
    
    :param logger_name: Logger namespace identifier
    :param log_file: Path to log file location
    :return: Configured logger instance
    """
    logger = logging.getLogger(logger_name)

    # Set level
    logger.setLevel(logging.INFO)

    # Create a file handler
    file_handler = ConcurrentRotatingFileHandler(log_file, maxBytes=1000000, backupCount=5)

    # Create a console handler
    console_handler = logging.StreamHandler()

    # Set formatter
    formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s]%(message)s')

    # Attach formatter to handlers
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Attach handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


if __name__ == '__main__':
    """Command-line entry point with logging setup."""
    ros2_logger = create_logger('Mission Manager', 'Logs/Mission_manager.log')

    ros2_action_queue = queue.Queue()

    start_grpc_ros2(ros2_action_queue, ros2_logger)