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
        send_mqtt_queue: queue.Queue,
        send_rest_queue: queue.Queue,
        send_pm_queue: queue.Queue,
        mission_logger: logging.Logger
    ):
        # Initialize parent gRPC servicer class
        super().__init__()
        
        # Store communication queues for inter-service messaging
        # These queues enable asynchronous communication with other system components
        self.send_ros2_queue = send_ros2_queue          # Outbound ROS2 vehicle commands
        self.receive_ros2_queue = receive_ros2_queue    # Inbound ROS2 vehicle responses
        self.send_mqtt_queue = send_mqtt_queue          # Outbound MQTT telemetry data
        self.send_rest_queue = send_rest_queue          # Outbound REST API status updates
        self.send_pm_queue = send_pm_queue              # Outbound Prescription Map data
        self.mission_logger = mission_logger            # Centralized logging instance

    def SendMission(self, request: Any, context: grpc.ServicerContext) -> MissionResponse:
        """Process incoming mission requests.

        :param request: gRPC request containing mission data
        :param context: gRPC connection context
        :return: Mission response with confirmation ID
        :raises: grpc.RpcError for critical processing failures
        """
        try:
            # Extract mission data from gRPC request payload
            # Convert protobuf repeated field to Python list for processing
            mission_data = list(request.mission_json)
            self.mission_logger.info("[gRPC REST] - Mission request received")
            
            # Delegate mission processing to mission manager
            # Pass all communication queues for distributed system coordination
            mission_id = create_mission_manager(
                mission_data,
                self.send_ros2_queue,
                self.receive_ros2_queue,
                self.send_mqtt_queue,
                self.send_rest_queue,
                self.send_pm_queue,
                self.mission_logger
            )
            # Return successful response with generated mission ID
            return MissionResponse(confirmation=f"{mission_id}")
        
        except Exception as e:
            # Handle critical mission processing failures
            # Set appropriate gRPC error status and provide detailed error information
            self.mission_logger.error(f"Mission processing failed: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Processing error: {str(e)}")
            # Return failure confirmation with standardized error ID
            return MissionResponse(confirmation="-1")


def run_client(send_rest_queue: queue.Queue, mission_logger: logging.Logger) -> None:
    """Continuous client for sending REST status updates.

    :param send_rest_queue: Queue containing status updates
    :param mission_logger: Configured logger instance
    """
    # Establish insecure gRPC channel to REST API service
    # Port 50052 is the dedicated REST communication endpoint
    channel = grpc.insecure_channel('localhost:50052')
    stub = RestCommunicationStub(channel)

    # Infinite loop for continuous REST status update processing
    # Ensures persistent communication with external REST API systems
    while True:
        try:
            # Attempt to retrieve status update from queue with timeout
            # Short timeout prevents blocking while allowing responsive status handling
            status_data = send_rest_queue.get(timeout=0.1)
            mission_logger.debug("[gRPC REST] - Sending mission status update")
            
            # Send status update via gRPC call to REST API service
            response = stub.SendRest(RestRequest(mission_status=status_data))
            mission_logger.info("[gRPC REST] - Status update confirmed")
            
        except queue.Empty:
            # No status updates available in queue - brief sleep to prevent CPU spinning
            time.sleep(0.1)
        except grpc.RpcError as e:
            # Handle gRPC communication errors with automatic retry logic
            # Logs specific error details for debugging and monitoring
            mission_logger.error(
                f"[gRPC REST] - Connection error ({e.code().name}): {e.details()}"
            )
            # Wait before retry to prevent rapid failure loops
            time.sleep(1)


def run_server(
    send_vehicle_queue: queue.Queue,
    receive_vehicle_queue: queue.Queue,
    send_mqtt_queue: queue.Queue,
    send_rest_queue: queue.Queue,
    send_pm_queue: queue.Queue,
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
    # Create gRPC server with thread pool for concurrent request handling
    # ThreadPoolExecutor allows up to 10 simultaneous mission requests
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Instantiate mission communication service with all required queues
    # Service handles incoming mission requests and coordinates system responses
    service = MissionCommunicationService(
        send_vehicle_queue,
        receive_vehicle_queue,
        send_mqtt_queue,
        send_rest_queue,
        send_pm_queue,
        mission_logger
    )
    
    # Register service with gRPC server infrastructure
    add_MissionCommunicationServicer_to_server(service, server)
    
    # Bind server to port 50092 for incoming mission requests
    # Uses IPv6 wildcard address for maximum compatibility
    server.add_insecure_port('[::]:50092')
    server.start()
    mission_logger.info("[gRPC REST] - Server running on port 50092")

    try:
        # Keep server running indefinitely with daily wake-up cycles
        # Long sleep interval reduces CPU usage while maintaining availability
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        # Graceful shutdown sequence on user interruption
        mission_logger.info("[gRPC REST] - Initiating graceful shutdown...")
        # Allow 5 seconds for ongoing requests to complete before force shutdown
        server.stop(5)
        mission_logger.info("[gRPC REST] - Server shutdown complete")


def start_grpc_mission_rest(
    send_vehicle_queue: queue.Queue,
    receive_vehicle_queue: queue.Queue,
    send_mqtt_queue: queue.Queue,
    send_rest_queue: queue.Queue,
    send_pm_queue: queue.Queue,
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
    # Create result queue for mission completion notifications
    # This queue can be used by calling code to track mission outcomes
    result_queue = queue.Queue()

    # Create dedicated daemon thread for REST client operations
    # Handles outbound status updates to external REST API systems
    client_thread = threading.Thread(
        target=run_client,
        args=(send_rest_queue, mission_logger),
        name="RESTClientThread",
        daemon=True
    )
    
    # Create dedicated daemon thread for gRPC server operations
    # Handles inbound mission requests from external systems
    server_thread = threading.Thread(
        target=run_server,
        args=(
            send_vehicle_queue,
            receive_vehicle_queue,
            send_mqtt_queue,
            send_rest_queue,
            send_pm_queue,
            mission_logger
        ),
        name="RESTServerThread",
        daemon=True
    )

    # Start both communication threads for bidirectional REST communication
    # Daemon threads ensure automatic cleanup when main process terminates
    client_thread.start()
    mission_logger.info("[gRPC REST] - Client communication thread started")
    server_thread.start()
    
    return result_queue
