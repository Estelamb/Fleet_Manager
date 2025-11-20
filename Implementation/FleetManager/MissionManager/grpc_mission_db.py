"""
gRPC Database Communication Module

.. module:: grpc_db_communication
    :synopsis: Provides bidirectional gRPC communication for database operations

.. note::
    Implements both client and server components for:
    - Sending database requests via client
    - Receiving database responses via server
    - Queue-based message buffering
    - Thread-managed communication channels
"""

from concurrent import futures
import grpc
import queue
import time
import threading
import logging
from typing import Optional

from GRPC.db_request_pb2 import DBReqRequest
from GRPC.db_request_pb2_grpc import DBReqCommunicationStub
from GRPC.db_response_pb2 import DBRespResponse
from GRPC.db_response_pb2_grpc import DBRespCommunicationServicer, add_DBRespCommunicationServicer_to_server


class DBRespCommunicationService(DBRespCommunicationServicer):
    """gRPC servicer for handling database responses from the Database subsystem.

    Attributes:
        receive_db_queue (queue.Queue): Queue for incoming database responses
        mission_logger (logging.Logger): Configured logger instance
    """

    def __init__(self, receive_db_queue: queue.Queue, mission_logger: logging.Logger) -> None:
        """Initialize the response servicer.

        Args:
            receive_db_queue: Queue for storing incoming database responses
            mission_logger: Configured logger for mission operations
        """
        super().__init__()
        self.receive_db_queue = receive_db_queue
        self.mission_logger = mission_logger
        
    def SendDBResp(self, request: DBReqRequest, context: grpc.ServicerContext) -> DBRespResponse:
        """Handle incoming database response messages.

        Args:
            request: Incoming gRPC request message
            context: gRPC connection context

        Returns:
            DBRespResponse: Response confirmation message

        Example:
            >>> service.SendDBResp(DBReqRequest(db_response=["test"]), None)
            DBRespResponse(confirmation="Feedback received")
        """
        db_response = list(request.db_response)
        self.mission_logger.info("[gRPC DB] - DB feedback received")
        self.receive_db_queue.put(db_response)
        return DBRespResponse(confirmation="Feedback received")


def run_client(send_db_queue: queue.Queue, mission_logger: logging.Logger) -> None:
    """Continuous client operation for sending database requests.

    Args:
        send_db_queue: Queue containing outgoing database requests
        mission_logger: Configured logger instance

    Raises:
        grpc.RpcError: For communication failures with the database service
    """
    channel = grpc.insecure_channel('localhost:50061')
    stub = DBReqCommunicationStub(channel)
    
    while True:
        try:
            db_request = send_db_queue.get(timeout=0.1)
            mission_logger.info("[gRPC DB] - Sending Mission data to Database")
            response = stub.SendDBReq(DBReqRequest(db_request=db_request))
            mission_logger.info("[gRPC DB] - ACK received from Database")
        except queue.Empty:
            time.sleep(0.1)
        except grpc.RpcError as e:
            mission_logger.error(f"[gRPC DB] - Connection error: {e.code().name}")
            time.sleep(1)


def run_server(receive_db_queue: queue.Queue, mission_logger: logging.Logger) -> None:
    """Start and maintain the gRPC response server.

    Args:
        receive_db_queue: Queue for storing incoming responses
        mission_logger: Configured logger instance

    Raises:
        KeyboardInterrupt: Propagates keyboard interrupts for clean shutdown
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_DBRespCommunicationServicer_to_server(
        DBRespCommunicationService(receive_db_queue, mission_logger), server)
    server.add_insecure_port('[::]:50056')
    server.start()
    mission_logger.info("[gRPC DB] - Response server started on port 50056")

    try:
        while True:
            time.sleep(86400)  # Maintain server thread alive
    except KeyboardInterrupt:
        mission_logger.info("[gRPC DB] - Initiating server shutdown")
        server.stop(5)  # 5-second grace period
        mission_logger.info("[gRPC DB] - Server shutdown complete")


def start_grpc_mission_db(
    send_db_queue: queue.Queue,
    receive_db_queue: queue.Queue,
    mission_logger: logging.Logger
) -> None:
    """Initialize and start gRPC communication components.

    Args:
        send_db_queue: Queue for outgoing database requests
        receive_db_queue: Queue for incoming database responses
        mission_logger: Configured logger instance

    Example:
        >>> start_grpc_mission_db(send_q, receive_q, logger)
    """
    client_thread = threading.Thread(
        target=run_client,
        args=(send_db_queue, mission_logger),
        name="DBClientThread"
    )
    server_thread = threading.Thread(
        target=run_server,
        args=(receive_db_queue, mission_logger),
        name="DBServerThread"
    )

    client_thread.daemon = True
    server_thread.daemon = True
    
    client_thread.start()
    server_thread.start()
    mission_logger.info("[gRPC DB] - Communication threads started")


if __name__ == '__main__':
    # Example standalone configuration
    send_db_queue = queue.Queue()
    receive_db_queue = queue.Queue()
    mission_logger = logging.getLogger("DBComm")
    
    start_grpc_mission_db(send_db_queue, receive_db_queue, mission_logger)
    
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        mission_logger.info("[gRPC DB] - Main process terminated")