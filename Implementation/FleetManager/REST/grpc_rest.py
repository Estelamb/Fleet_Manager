"""
This module implements bidirectional gRPC communication for mission management systems. 
Contains both server and client components for handling mission data and status updates.

Components
----------
- RestCommunicationService : gRPC service implementation for receiving mission statuses
- run_rest_server : gRPC server startup and management
- run_rest_client : gRPC client for mission submission
- start_grpc_rest : Server thread management

Protocol Buffers
----------------
Uses generated code from:
- rest_pb2(_grpc): For REST status communication
- mission_pb2(_grpc): For mission data transmission

Example
-------
Start server:
    $ python grpc_rest.py

Send mission from client:
    >>> from grpc_rest import run_rest_client
    >>> run_rest_client('{"mission": "data"}', logger)
"""

from concurrent import futures
import grpc
import time
import threading
import logging
from concurrent_log_handler import ConcurrentRotatingFileHandler

from GRPC.rest_pb2 import RestResponse
from GRPC.rest_pb2_grpc import RestCommunicationServicer, add_RestCommunicationServicer_to_server
from GRPC.mission_pb2 import MissionRequest
from GRPC.mission_pb2_grpc import MissionCommunicationStub


class RestCommunicationService(RestCommunicationServicer):
    """gRPC service implementation for handling mission status updates.
    
    Inherits from generated RestCommunicationServicer and implements the 
    gRPC service methods.

    :param rest_logger: Configured logger instance for service operations
    :type rest_logger: logging.Logger

    :ivar rest_logger: Logger instance for service operations
    :vartype rest_logger: logging.Logger
    """

    def __init__(self, rest_logger):
        """Initialize service with configured logger."""
        super().__init__()
        self.rest_logger = rest_logger

    def SendRest(self, request, context):
        """Handle incoming mission status updates from Fleet Management.
        
        :param request: Incoming gRPC request containing mission status data
        :type request: rest_pb2.RestRequest
        :param context: gRPC connection context
        :type context: grpc.ServicerContext
        
        :return: Response confirmation with status receipt acknowledgment
        :rtype: rest_pb2.RestResponse
        
        :raises grpc.RpcError: If connection issues occur during processing
        
        Example:
            Typical status format::
            
                mission_status = ["COMPLETED", "IN_PROGRESS", "FAILED"]
        """
        mission_status = list(request.mission_status)
        self.rest_logger.info("[gRPC REST] - Mission status received from Fleet Management")
        # TODO: Implement POST handling for status updates
        # request.post()  
        return RestResponse(confirmation=f"Server received mission status: {mission_status}")


def run_rest_server(rest_logger):
    """Start and maintain the gRPC server for REST communication.
    
    :param rest_logger: Configured logger instance for server operations
    :type rest_logger: logging.Logger
    
    Server Configuration:
    - Uses ThreadPoolExecutor with 10 worker threads
    - Listens on port 50052
    - Runs indefinitely until keyboard interrupt
    
    :note: Blocks execution while running - typically started in separate thread
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_RestCommunicationServicer_to_server(
        RestCommunicationService(rest_logger), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    rest_logger.info("[gRPC REST] - Server started")
    try:
        while True:
            time.sleep(86400)  # Maintain server for 24h intervals
    except KeyboardInterrupt:
        server.stop(0)
        rest_logger.info("[gRPC REST] - Server shutdown complete")


def run_rest_client(mission_json, rest_logger):
    """Send mission data to Fleet Management system via gRPC.
    
    :param mission_json: Mission data in JSON string format
    :type mission_json: str
    :param rest_logger: Configured logger instance for client operations
    :type rest_logger: logging.Logger
    
    :return: Confirmation message from server or None on failure
    :rtype: str | None
    
    :raises grpc.RpcError: If connection to server fails
    
    Example:
        Successful response::
        
            "Mission received by Fleet Management: 12345"
    """
    channel = grpc.insecure_channel('localhost:50092')
    stub = MissionCommunicationStub(channel)

    try:
        rest_logger.info("[gRPC REST] - Sending mission to Fleet Management")
        response = stub.SendMission(MissionRequest(mission_json=mission_json))
        rest_logger.info("[gRPC REST] - ACK received from Fleet Management")
        return response.confirmation
    except grpc.RpcError as e:
        rest_logger.error(f"[gRPC REST] - Connection error: {e}")
        return None


def start_grpc_rest(rest_logger):
    """Initialize and start gRPC server in background thread.
    
    :param rest_logger: Configured logger instance for server operations
    :type rest_logger: logging.Logger
    
    :note: Server thread runs as daemon and will terminate with main process
    """
    server_rest_thread = threading.Thread(
        target=run_rest_server, 
        args=(rest_logger,),
        name="gRPC-REST-Server"
    )
    server_rest_thread.daemon = True
    server_rest_thread.start()


if __name__ == '__main__':
    """Main execution block for standalone server operation.
    
    Configures logging with:
    - Concurrent log rotation (1MB files, 5 backups)
    - Console output
    - Standardized log format
    
    Starts gRPC server and maintains process until termination.
    """
    rest_logger = logging.getLogger('REST')
    rest_logger.setLevel(logging.INFO)
    
    # Configure rotating file handler
    file_rest = ConcurrentRotatingFileHandler(
        "rest.log",
        maxBytes=1000000,
        backupCount=5
    )
    
    # Configure console output
    console_rest = logging.StreamHandler()
    
    # Create unified formatter
    formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s]%(message)s')
    
    # Apply formatting
    file_rest.setFormatter(formatter)
    console_rest.setFormatter(formatter)
    
    # Register handlers
    rest_logger.addHandler(file_rest)
    rest_logger.addHandler(console_rest)

    # Start server components
    start_grpc_rest(rest_logger)
    
    # Maintain main thread
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        rest_logger.info("[gRPC REST] - Main process terminated")