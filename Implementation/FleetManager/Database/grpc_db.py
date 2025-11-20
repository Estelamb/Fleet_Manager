"""
This module implements a gRPC-based communication system for database operations.

It provides:
- gRPC server for receiving mission status updates
- gRPC client for sending database responses
- Threaded server implementation for concurrent operations
- Comprehensive logging and error handling

Classes:
    DBReqCommunicationService: Implementation of gRPC servicer for handling database requests

Functions:
    run_db_server: Starts and manages the gRPC server instance
    run_db_client: Handles client-side communication with Mission Management system
    start_grpc_db: Initializes and starts the gRPC server thread
"""

from concurrent import futures
import grpc
import time
import threading
import logging
from typing import Any, Optional, List
from concurrent_log_handler import ConcurrentRotatingFileHandler

from GRPC.db_response_pb2 import DBRespRequest
from GRPC.db_response_pb2_grpc import DBRespCommunicationStub
from GRPC.db_request_pb2 import DBReqResponse
from GRPC.db_request_pb2_grpc import DBReqCommunicationServicer, add_DBReqCommunicationServicer_to_server

from Database.db_manager import run_db_manager


class DBReqCommunicationService(DBReqCommunicationServicer):
    """gRPC servicer class handling database request operations.

    Attributes:
        db_logger (logging.Logger): Configured logger instance for database operations
    """

    def __init__(self, db_logger: logging.Logger) -> None:
        """Initialize the servicer with a logger instance.

        Args:
            db_logger (logging.Logger): Configured logger for database operations
        """
        super().__init__()
        self.db_logger = db_logger

    def SendDBReq(self, request: Any, context: grpc.ServicerContext) -> DBReqResponse:
        """Handle incoming database request messages.

        Args:
            request (Any): Incoming gRPC request message
            context (grpc.ServicerContext): gRPC connection context

        Returns:
            DBReqResponse: Response confirmation message

        Raises:
            grpc.RpcError: If critical communication errors occur
        """
        db_request = list(request.db_request)
        self.db_logger.info("[gRPC DB] - Data received")
        try:
            run_db_manager(db_request, self.db_logger)
            return DBReqResponse(confirmation="Data processed successfully")
        except Exception as e:
            self.db_logger.error(f"[gRPC DB] - Processing error: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Server error: {str(e)}")
            return DBReqResponse(confirmation="Data processing failed")


def run_db_server(db_logger: logging.Logger) -> None:
    """Start and manage the gRPC server instance.

    Args:
        db_logger (logging.Logger): Configured logger for server operations

    Raises:
        grpc.RpcError: If server startup or communication errors occur
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_DBReqCommunicationServicer_to_server(
        DBReqCommunicationService(db_logger), server
    )
    server.add_insecure_port('[::]:50060')
    server.start()
    db_logger.info("[gRPC DB] - Server started on port 50060")
    
    try:
        while True:
            time.sleep(86400)  # Maintain server thread alive
    except KeyboardInterrupt:
        db_logger.info("[gRPC DB] - Initiating graceful shutdown...")
        server.stop(5)  # 5-second grace period for existing connections
        db_logger.info("[gRPC DB] - Server shutdown complete")


def run_db_client(db_response: List[Any], db_logger: logging.Logger) -> Optional[str]:
    """Send database response to Mission Management system.

    Args:
        db_response (List[Any]): List of response items to send
        db_logger (logging.Logger): Configured logger for client operations

    Returns:
        Optional[str]: Confirmation message if successful, None otherwise
    """
    channel = grpc.insecure_channel('localhost:50061')
    try:
        stub = DBRespCommunicationStub(channel)
        db_logger.info("[gRPC DB] - Sending data to Mission Management")
        response = stub.SendDBResp(DBRespRequest(db_response=db_response))
        db_logger.info("[gRPC DB] - ACK received from Mission Management")
        return response.confirmation
    except grpc.RpcError as e:
        db_logger.error(f"[gRPC DB] - Connection error: {e.code()}: {e.details()}")
        return None
    finally:
        channel.close()


def start_grpc_db(db_logger: logging.Logger) -> None:
    """Initialize and start the gRPC server in a daemon thread.

    Args:
        db_logger (logging.Logger): Configured logger for database operations
    """
    server_db_thread = threading.Thread(
        target=run_db_server,
        args=(db_logger,),
        name="gRPC-DB-Server"
    )
    server_db_thread.daemon = True
    server_db_thread.start()
    db_logger.info("[gRPC DB] - Server thread started")


if __name__ == '__main__':
    """Main entry point for standalone execution of the DB gRPC server."""
    
    # Configure logging system
    db_logger = logging.getLogger('DB')
    db_logger.setLevel(logging.INFO)
    
    # Configure file handler with concurrent rotation
    file_handler = ConcurrentRotatingFileHandler(
        "Logs/DB.log",
        maxBytes=1_000_000,
        backupCount=5,
        encoding='utf-8'
    )
    
    # Configure console output
    console_handler = logging.StreamHandler()
    
    # Unified formatter for all handlers
    formatter = logging.Formatter(
        '[%(asctime)s] - [%(name)s][%(levelname)s] %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Attach handlers to logger
    db_logger.addHandler(file_handler)
    db_logger.addHandler(console_handler)

    # Start gRPC services
    start_grpc_db(db_logger)
    
    # Keep main thread alive
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        db_logger.info("[gRPC DB] - Main process terminated")