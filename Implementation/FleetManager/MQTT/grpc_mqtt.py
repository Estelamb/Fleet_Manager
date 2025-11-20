"""
gRPC MQTT Communication Server Module

.. module:: grpc_mqtt_server
    :synopsis: Provides gRPC services for MQTT data handling and ThingsBoard integration

.. note::
    Features:
    - gRPC server implementation for MQTT data reception
    - Thread-safe queue integration for data processing
    - Graceful shutdown handling
    - Comprehensive logging integration
"""

from concurrent import futures
import grpc
import time
import threading
import logging
from typing import Any, Optional, Union
from queue import Queue

from GRPC.mqtt_pb2 import MQTTResponse
from GRPC.mqtt_pb2_grpc import MQTTCommunicationServicer, add_MQTTCommunicationServicer_to_server

# Server configuration
_SERVER_ADDRESS = '[::]:50057'
_MAX_WORKERS = 10
_SERVER_GRACE_PERIOD = 5  # Seconds for graceful shutdown


class MQTTCommunicationService(MQTTCommunicationServicer):
    """gRPC service implementation for MQTT data handling.

    :param data_to_tb: Thread-safe queue for outgoing data to ThingsBoard
    :param mqtt_logger: Configured logger instance for MQTT operations
    """

    def __init__(self, data_to_tb: Queue, mqtt_logger: Optional[logging.Logger] = None):
        self.data_to_tb = data_to_tb
        self.mqtt_logger = mqtt_logger or logging.getLogger('MQTT')

    def SendMQTT(self, request: Any, context: grpc.ServicerContext) -> MQTTResponse:
        """Handle incoming MQTT data requests.

        :param request: gRPC request containing MQTT message data
        :param context: gRPC connection context
        :return: Response confirmation
        :raises grpc.RpcError: For critical processing errors

        .. note::
            Processes incoming messages by:
            1. Extracting message content
            2. Logging receipt
            3. Queueing for ThingsBoard transmission
        """
        try:
            mqtt_message = list(request.mqtt_message)
            self.mqtt_logger.info("[gRPC MQTT] - Received data payload")
            self.data_to_tb.put(mqtt_message)
            return MQTTResponse(confirmation="Data queued successfully")
        except Exception as e:
            self.mqtt_logger.error(f"Message processing failed: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Processing error: {str(e)}")
            return MQTTResponse(confirmation="Data processing failed")


def run_grpc_mqtt_server(data_to_tb: Queue, mqtt_logger: Optional[logging.Logger] = None) -> None:
    """Run the gRPC server for MQTT communication.

    :param data_to_tb: Shared queue for ThingsBoard-bound data
    :param mqtt_logger: Configured logger instance

    .. note::
        Server features:
        - Thread pool executor for concurrent requests
        - Graceful shutdown on keyboard interrupt
        - Port configuration from _SERVER_ADDRESS constant
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=_MAX_WORKERS))
    service = MQTTCommunicationService(data_to_tb, mqtt_logger)
    
    add_MQTTCommunicationServicer_to_server(service, server)
    server.add_insecure_port(_SERVER_ADDRESS)
    
    server.start()
    (mqtt_logger or logging.getLogger()).info(f"[gRPC MQTT] - Server started on {_SERVER_ADDRESS}")

    try:
        while True:
            time.sleep(86400)  # Maintain server thread alive
    except KeyboardInterrupt:
        (mqtt_logger or logging.getLogger()).info("[gRPC MQTT] - Initiating graceful shutdown...")
        server.stop(_SERVER_GRACE_PERIOD)
        (mqtt_logger or logging.getLogger()).info("[gRPC MQTT] - Server shutdown complete")


def start_grpc_mqtt(data_to_tb: Queue, mqtt_logger: Optional[logging.Logger] = None) -> None:
    """Initialize and start the gRPC server in a daemon thread.

    :param data_to_tb: Shared queue for outgoing data
    :param mqtt_logger: Configured logger instance
    """
    server_thread = threading.Thread(
        target=run_grpc_mqtt_server,
        args=(data_to_tb, mqtt_logger),
        name="MQTTgRPCServer",
        daemon=True
    )
    server_thread.start()
    (mqtt_logger or logging.getLogger()).info("[gRPC MQTT] - Server thread initialized")


if __name__ == '__main__':
    """Entry point for standalone execution with test queue."""
    import logging
    logging.basicConfig(level=logging.INFO)
    start_grpc_mqtt(Queue(), logging.getLogger('MQTT'))
    
    try:
        while True:
            time.sleep(3600)  # Keep main thread alive
    except KeyboardInterrupt:
        logging.info("Main process terminated")