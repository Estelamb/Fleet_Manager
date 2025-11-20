"""
gRPC Mission Vehicle Communication Module

.. module:: grpc_mission_vehicle
    :synopsis: Provides gRPC services for vehicle plan distribution and result collection

.. note::
    Features:
    - Bidirectional communication with ROS2 systems
    - Thread-safe queue-based message handling
    - Graceful connection management
    - Comprehensive logging system
"""

import logging
import queue
import threading
import time
from concurrent import futures
import grpc
from concurrent_log_handler import ConcurrentRotatingFileHandler

from GRPC.plan_pb2 import DronePlanRequest
from GRPC.plan_pb2_grpc import PlanCommunicationStub
from GRPC.result_pb2 import DroneResultResponse
from GRPC.result_pb2_grpc import ResultCommunicationServicer, add_ResultCommunicationServicer_to_server

class ResultCommunicationService(ResultCommunicationServicer):
    """gRPC service handler for vehicle result collection from ROS2.

    :param receive_vehicle_queue: Queue for storing incoming vehicle results
    :param mission_logger: Configured logger instance
    """
    def __init__(self, receive_vehicle_queue, mission_logger):
        # Initialize parent gRPC servicer class
        super().__init__()
        
        # Store communication components for result processing
        # Queue enables asynchronous result collection from vehicle systems
        self.receive_vehicle_queue = receive_vehicle_queue  # Inbound vehicle result storage
        self.mission_logger = mission_logger                # Centralized logging instance
        
    def SendResult(self, request, context):
        """Process incoming vehicle results from ROS2.

        :param request: gRPC request containing drone result data
        :param context: gRPC connection context
        :return: Confirmation response
        """
        # Extract vehicle result data from gRPC request payload
        # Convert protobuf repeated field to Python list for processing
        drone_result = list(request.drone_result)
        self.mission_logger.info(f"[gRPC Vehicle] - Plan feedback received from ROS2")
        
        # Queue result data for processing by mission management system
        # Asynchronous queuing prevents blocking the gRPC response
        self.receive_vehicle_queue.put(drone_result)
        
        # Return acknowledgment to ROS2 system confirming receipt
        return DroneResultResponse(confirmation=f"Feedback received")

def run_client(send_vehicle_queue, mission_logger):
    """Continuous client for sending vehicle plans to ROS2.

    :param send_vehicle_queue: Queue containing outgoing vehicle plans
    :param mission_logger: Configured logger instance
    """
    channel = grpc.insecure_channel('localhost:50099')
    stub = PlanCommunicationStub(channel)
    
    while True:
        try:
            drone_plan = send_vehicle_queue.get()
            if drone_plan[0] == 'AUAV':
                drone_plan = drone_plan[1]
                mission_logger.info(f"[gRPC Vehicle] - Sending plan to ROS2")
                response = stub.SendPlan(DronePlanRequest(drone_plan=drone_plan))
                mission_logger.info(f"[gRPC Vehicle] - ACK received from ROS2")
        except queue.Empty:
            time.sleep(0.1)
        except grpc.RpcError as e:
            mission_logger.error(f"[gRPC Vehicle] - Connection error: {e}")
            time.sleep(1)

def run_server(receive_vehicle_queue, mission_logger):
    """gRPC server instance for result collection.

    :param receive_vehicle_queue: Queue for incoming vehicle results
    :param mission_logger: Configured logger instance
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_ResultCommunicationServicer_to_server(
        ResultCommunicationService(receive_vehicle_queue, mission_logger), server)
    server.add_insecure_port('[::]:50070')
    server.start()
    mission_logger.info("[gRPC Vehicle] - Server running on port [::]:50070")
    
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

def start_grpc_mission_vehicle(send_vehicle_queue, receive_vehicle_queue, mission_logger):
    """Initialize and start gRPC communication components.

    :param send_vehicle_queue: Outgoing vehicle plan queue
    :param receive_vehicle_queue: Incoming result queue
    :param mission_logger: Configured logger instance
    """
    client_thread = threading.Thread(target=run_client, args=(send_vehicle_queue, mission_logger,))
    server_thread = threading.Thread(target=run_server, args=(receive_vehicle_queue, mission_logger,))

    client_thread.daemon = True
    server_thread.daemon = True
    
    client_thread.start()
    mission_logger.info("[gRPC Vehicle] - Client communication thread started")
    server_thread.start()

def create_logger(logger_name, log_file):
    """Configure and return a concurrent-safe logger instance.

    :param logger_name: Name for the logger instance
    :param log_file: Path to log file
    :return: Configured logger instance
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
    """Main entry point for standalone execution."""
    mission_logger = create_logger('mission Manager', 'Logs/mission_manager.log')
    
    send_vehicle_queue = queue.Queue()
    receive_vehicle_queue = queue.Queue()
    
    start_grpc_mission_vehicle(send_vehicle_queue, receive_vehicle_queue, mission_logger)