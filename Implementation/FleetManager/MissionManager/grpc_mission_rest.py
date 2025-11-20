"""
gRPC Mission REST Communication Module

.. module:: grpc_mission_rest
    :synopsis: Provides gRPC services for mission management and REST communication

.. note::
    Features:
    - gRPC server for mission reception and processing
    - gRPC client for status updates
    - Queue-based inter-service communication
    - Comprehensive logging system
"""

from concurrent import futures
import grpc
import queue
import time
import threading
import logging
from typing import Optional, Any, Tuple, Dict, List
from concurrent_log_handler import ConcurrentRotatingFileHandler

from GRPC.mission_pb2 import MissionResponse
from GRPC.mission_pb2_grpc import MissionCommunicationServicer, add_MissionCommunicationServicer_to_server
from GRPC.rest_pb2 import RestRequest
from GRPC.rest_pb2_grpc import RestCommunicationStub
from MissionManager.mission_manager import create_mission_manager


class MissionCommunicationService(MissionCommunicationServicer):
    """gRPC service handler for mission operations.

    :param send_ros2_queue: Queue for ROS2-bound messages
    :param receive_ros2_queue: Queue for ROS2-originated messages
    :param send_db_queue: Queue for database operations
    :param receive_db_queue: Queue for database responses
    :param send_mqtt_queue: Queue for MQTT messages
    :param send_rest_queue: Queue for REST updates
    :param mission_logger: Configured logger instance
    """

    def __init__(
        self,
        send_ros2_queue: queue.Queue,
        receive_ros2_queue: queue.Queue,
        send_db_queue: queue.Queue,
        receive_db_queue: queue.Queue,
        send_mqtt_queue: queue.Queue,
        send_rest_queue: queue.Queue,
        mission_logger: logging.Logger
    ):
        super().__init__()
        self.send_ros2_queue = send_ros2_queue
        self.receive_ros2_queue = receive_ros2_queue
        self.send_db_queue = send_db_queue
        self.receive_db_queue = receive_db_queue
        self.send_mqtt_queue = send_mqtt_queue
        self.send_rest_queue = send_rest_queue
        self.mission_logger = mission_logger

    def SendMission(self, request: Any, context: grpc.ServicerContext) -> MissionResponse:
        """Process incoming mission requests.

        :param request: gRPC request containing mission data
        :param context: gRPC connection context
        :return: Mission response with confirmation ID
        :raises: grpc.RpcError for critical processing failures
        """
        try:
            mission_data = list(request.mission_json)
            self.mission_logger.info("[gRPC REST] - Mission request received")
            
            mission_id = create_mission_manager(
                mission_data,
                self.send_ros2_queue,
                self.receive_ros2_queue,
                self.send_db_queue,
                self.receive_db_queue,
                self.send_mqtt_queue,
                self.send_rest_queue,
                self.mission_logger
            )
            return MissionResponse(confirmation=f"{mission_id}")
        
        except Exception as e:
            self.mission_logger.error(f"Mission processing failed: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Processing error: {str(e)}")
            return MissionResponse(confirmation="-1")


def run_client(send_rest_queue: queue.Queue, mission_logger: logging.Logger) -> None:
    """Continuous client for sending REST status updates.

    :param send_rest_queue: Queue containing status updates
    :param mission_logger: Configured logger instance
    """
    channel = grpc.insecure_channel('localhost:50052')
    stub = RestCommunicationStub(channel)

    while True:
        try:
            status_data = send_rest_queue.get(timeout=0.1)
            mission_logger.debug("[gRPC REST] - Sending mission status update")
            response = stub.SendRest(RestRequest(mission_status=status_data))
            mission_logger.info("[gRPC REST] - Status update confirmed")
            
        except queue.Empty:
            time.sleep(0.1)
        except grpc.RpcError as e:
            mission_logger.error(
                f"[gRPC REST] - Connection error ({e.code().name}): {e.details()}"
            )
            time.sleep(1)


def run_server(
    send_vehicle_queue: queue.Queue,
    receive_vehicle_queue: queue.Queue,
    send_db_queue: queue.Queue,
    receive_db_queue: queue.Queue,
    send_mqtt_queue: queue.Queue,
    send_rest_queue: queue.Queue,
    mission_logger: logging.Logger
) -> None:
    """gRPC server instance manager.

    :param send_vehicle_queue: Vehicle command queue
    :param receive_vehicle_queue: Vehicle status queue
    :param send_db_queue: Database operation queue
    :param receive_db_queue: Database response queue
    :param send_mqtt_queue: MQTT message queue
    :param send_rest_queue: REST update queue
    :param mission_logger: Configured logger instance
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service = MissionCommunicationService(
        send_vehicle_queue,
        receive_vehicle_queue,
        send_db_queue,
        receive_db_queue,
        send_mqtt_queue,
        send_rest_queue,
        mission_logger
    )
    add_MissionCommunicationServicer_to_server(service, server)
    server.add_insecure_port('[::]:50092')
    server.start()
    mission_logger.info("[gRPC REST] - Server listening on port 50092")

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        mission_logger.info("[gRPC REST] - Initiating graceful shutdown...")
        server.stop(5)
        mission_logger.info("[gRPC REST] - Server shutdown complete")


def start_grpc_mission_rest(
    send_vehicle_queue: queue.Queue,
    receive_vehicle_queue: queue.Queue,
    send_db_queue: queue.Queue,
    receive_db_queue: queue.Queue,
    send_mqtt_queue: queue.Queue,
    send_rest_queue: queue.Queue,
    mission_logger: logging.Logger
) -> queue.Queue:
    """Initialize and start gRPC communication components.

    :param send_vehicle_queue: Vehicle command queue
    :param receive_vehicle_queue: Vehicle status queue
    :param send_db_queue: Database operation queue
    :param receive_db_queue: Database response queue
    :param send_mqtt_queue: MQTT message queue
    :param send_rest_queue: REST update queue
    :param mission_logger: Configured logger instance
    :return: Mission result queue
    """
    result_queue = queue.Queue()

    client_thread = threading.Thread(
        target=run_client,
        args=(send_rest_queue, mission_logger),
        name="RESTClientThread",
        daemon=True
    )
    
    server_thread = threading.Thread(
        target=run_server,
        args=(
            send_vehicle_queue,
            receive_vehicle_queue,
            send_db_queue,
            receive_db_queue,
            send_mqtt_queue,
            send_rest_queue,
            mission_logger
        ),
        name="RESTServerThread",
        daemon=True
    )

    client_thread.start()
    server_thread.start()
    mission_logger.info("[gRPC REST] - Communication threads initialized")
    
    return result_queue


def create_logger(logger_name: str, log_file: str) -> logging.Logger:
    """Configure and return a concurrent-safe logger instance.

    :param logger_name: Name for the logger instance
    :param log_file: Path to log file
    :return: Configured logger instance
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    file_handler = ConcurrentRotatingFileHandler(
        log_file,
        maxBytes=1_000_000,
        backupCount=5,
        encoding='utf-8'
    )
    
    console_handler = logging.StreamHandler()
    
    formatter = logging.Formatter(
        '[%(asctime)s] - [%(name)s][%(levelname)s]%(message)s'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


if __name__ == '__main__':
    """Main entry point for standalone execution."""
    mission_logger = create_logger('MissionManager', 'Logs/mission_manager.log')
    
    # Initialize communication queues
    queues = (
        queue.Queue(),  # send_vehicle
        queue.Queue(),  # receive_vehicle
        queue.Queue(),  # send_db
        queue.Queue(),  # receive_db
        queue.Queue(),  # send_mqtt
        queue.Queue()   # send_rest
    )
    
    start_grpc_mission_rest(*queues, mission_logger)
    
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        mission_logger.info("Main process terminated")