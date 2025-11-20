"""
gRPC MQTT Communication Server Module

.. module:: grpc_mqtt_server
    :synopsis: Provides gRPC services for MQTT data handling and ThingsBoard integration
    :platform: Linux, Windows, macOS
    :author: Fleet Management System Team

This module implements a gRPC server for handling MQTT communication within the fleet management
system. It provides a bridge between MQTT messages and ThingsBoard for telemetry data processing.

.. note::
    Key Features:
    - High-performance gRPC server implementation for MQTT data reception
    - Thread-safe queue integration for reliable data processing
    - Graceful shutdown handling with configurable grace period
    - Comprehensive logging integration with configurable log levels
    - Concurrent request handling via thread pool executor
    - Daemon thread support for background operation

.. versionadded:: 1.0.0
    Initial implementation of MQTT gRPC communication service

.. seealso::
    - :mod:`GRPC.mqtt_pb2` for protocol buffer definitions
    - :mod:`MQTT.ThingsBoard` for ThingsBoard integration components

Example:
    Basic usage of the MQTT gRPC server::

        from queue import Queue
        import logging
        from MQTT.grpc_mqtt import start_grpc_mqtt

        # Initialize queue and logger
        tb_queue = Queue()
        mqtt_logger = logging.getLogger('MQTT')
        
        # Start the gRPC server
        start_grpc_mqtt(tb_queue, mqtt_logger)
"""

from concurrent import futures
import grpc
import time
import threading
import logging
from typing import Any, Optional, Union
from queue import Queue

# Import gRPC generated protocol buffer classes for MQTT communication
from GRPC.mqtt_pb2 import MQTTResponse
from GRPC.mqtt_pb2_grpc import MQTTCommunicationServicer, add_MQTTCommunicationServicer_to_server

# ========================================
# Server Configuration Constants
# ========================================

#: str: Server bind address supporting both IPv4 and IPv6 connections
_SERVER_ADDRESS = '[::]:50057'

#: int: Maximum number of worker threads for concurrent request handling
_MAX_WORKERS = 10

#: int: Grace period in seconds for server shutdown (allows pending requests to complete)
_SERVER_GRACE_PERIOD = 5  # Seconds for graceful shutdown


class MQTTCommunicationService(MQTTCommunicationServicer):
    """gRPC service implementation for MQTT data handling and ThingsBoard integration.
    
    This class implements the MQTTCommunicationServicer interface to provide
    a gRPC service for receiving and processing MQTT messages within the fleet
    management system. It acts as a bridge between incoming MQTT data and the
    ThingsBoard telemetry system.
    
    The service handles incoming requests asynchronously and queues data for
    further processing by ThingsBoard components. All operations are thread-safe
    and include comprehensive error handling.

    :param tb_queue: Thread-safe queue for outgoing data to ThingsBoard
    :type tb_queue: Queue
    :param mqtt_logger: Configured logger instance for MQTT operations
    :type mqtt_logger: Optional[logging.Logger]
    
    .. note::
        The service uses a fail-safe approach where processing errors are logged
        but don't crash the server, ensuring high availability.
        
    .. versionadded:: 1.0.0
        Initial implementation of MQTT communication service
        
    Attributes:
        tb_queue (Queue): Thread-safe queue for ThingsBoard data transmission
        mqtt_logger (logging.Logger): Logger instance for operation tracking
    """

    def __init__(self, tb_queue: Queue, mqtt_logger: Optional[logging.Logger] = None):
        """Initialize the MQTT communication service.
        
        :param tb_queue: Queue for storing messages destined for ThingsBoard
        :type tb_queue: Queue
        :param mqtt_logger: Logger for MQTT operations (creates default if None)
        :type mqtt_logger: Optional[logging.Logger]
        """
        self.tb_queue = tb_queue
        self.mqtt_logger = mqtt_logger or logging.getLogger('MQTT')

    def SendMQTT(self, request: Any, context: grpc.ServicerContext) -> MQTTResponse:
        """Handle incoming MQTT data requests via gRPC.

        This method processes incoming MQTT messages received through the gRPC interface.
        It extracts the message content, logs the operation, and queues the data for
        transmission to ThingsBoard. The method implements robust error handling to
        ensure service availability even when individual messages fail processing.

        :param request: gRPC request containing MQTT message data and metadata
        :type request: Any (protocol buffer message type)
        :param context: gRPC connection context for client communication management
        :type context: grpc.ServicerContext
        :return: Response confirmation with operation status
        :rtype: MQTTResponse
        :raises grpc.RpcError: For critical processing errors that prevent message handling

        .. note::
            Processing Pipeline:
            1. Extract MQTT message content from the gRPC request
            2. Log successful message receipt for audit purposes
            3. Add message to ThingsBoard processing queue
            4. Return success confirmation to client
            
        .. warning::
            If an exception occurs during processing, the error is logged and
            a gRPC error status is set, but the service continues operating.
            
        .. versionadded:: 1.0.0
            Initial implementation of MQTT message handling
            
        Example:
            The method is called automatically by the gRPC framework when
            clients send MQTT data::
            
                # Client-side call (handled automatically)
                response = stub.SendMQTT(mqtt_request)
                print(response.confirmation)  # "Data queued successfully"
        """
        try:
            # Extract MQTT message content from the gRPC request
            mqtt_message = list(request.mqtt_message)
            
            # Log successful message receipt for monitoring and debugging
            self.mqtt_logger.info("[gRPC MQTT] - Received data to send to ThingsBoard")
            
            # Queue the message for ThingsBoard processing
            self.tb_queue.put(mqtt_message)
            
            # Return success confirmation to the client
            return MQTTResponse(confirmation="Data queued successfully")
            
        except Exception as e:
            # Log the error for debugging and monitoring purposes
            self.mqtt_logger.error(f"Message processing failed: {str(e)}")
            
            # Set gRPC error status for client notification
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Processing error: {str(e)}")
            
            # Return failure confirmation
            return MQTTResponse(confirmation="Data processing failed")


def run_grpc_mqtt_server(tb_queue: Queue, mqtt_logger: Optional[logging.Logger] = None) -> None:
    """Run the gRPC server for MQTT communication with blocking execution.

    This function creates and starts a gRPC server that listens for MQTT communication
    requests. The server runs with a thread pool executor for handling concurrent
    requests and includes graceful shutdown capabilities.
    
    The server binds to the configured address and runs indefinitely until interrupted
    by a keyboard signal (Ctrl+C). Upon interruption, it performs a graceful shutdown
    allowing pending requests to complete within the configured grace period.

    :param tb_queue: Shared thread-safe queue for ThingsBoard-bound data
    :type tb_queue: Queue
    :param mqtt_logger: Configured logger instance for operation tracking
    :type mqtt_logger: Optional[logging.Logger]
    :return: None (function runs until interrupted)
    :rtype: None

    .. note::
        Server Configuration:
        - Uses ThreadPoolExecutor with configurable maximum workers
        - Binds to IPv6 address (with IPv4 compatibility)
        - Implements graceful shutdown with configurable timeout
        - Provides comprehensive logging for monitoring
        
    .. warning::
        This function blocks the calling thread. Use :func:`start_grpc_mqtt`
        for non-blocking daemon thread execution.
        
    .. versionadded:: 1.0.0
        Initial implementation of MQTT gRPC server
        
    Raises:
        KeyboardInterrupt: Caught and handled gracefully for server shutdown
        
    Example:
        Direct server execution (blocking)::
        
            from queue import Queue
            import logging
            
            queue = Queue()
            logger = logging.getLogger('MQTT')
            run_grpc_mqtt_server(queue, logger)  # Blocks until Ctrl+C
    """
    # Create gRPC server with thread pool executor for concurrent request handling
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=_MAX_WORKERS))
    
    # Initialize the MQTT communication service with provided queue and logger
    service = MQTTCommunicationService(tb_queue, mqtt_logger)
    
    # Register the service implementation with the gRPC server
    add_MQTTCommunicationServicer_to_server(service, server)
    
    # Bind server to the configured address (supports both IPv4 and IPv6)
    server.add_insecure_port(_SERVER_ADDRESS)
    
    # Start the server and begin accepting connections
    server.start()
    (mqtt_logger or logging.getLogger()).info(f"[gRPC MQTT] - Server running on port {_SERVER_ADDRESS}")

    try:
        # Keep the main thread alive while server handles requests
        while True:
            time.sleep(86400)  # Maintain server thread alive (24 hours sleep cycles)
    except KeyboardInterrupt:
        # Handle graceful shutdown on user interruption
        (mqtt_logger or logging.getLogger()).info("[gRPC MQTT] - Initiating graceful shutdown...")
        
        # Stop server with grace period to allow pending requests to complete
        server.stop(_SERVER_GRACE_PERIOD)
        
        # Log successful shutdown completion
        (mqtt_logger or logging.getLogger()).info("[gRPC MQTT] - Server shutdown complete")


def start_grpc_mqtt(tb_queue: Queue, mqtt_logger: Optional[logging.Logger] = None) -> None:
    """Initialize and start the gRPC MQTT server in a daemon background thread.

    This function provides a convenient way to start the MQTT gRPC server without
    blocking the main application thread. The server runs as a daemon thread,
    meaning it will automatically terminate when the main program exits.
    
    This is the preferred method for integrating the MQTT gRPC server into larger
    applications where other components need to run concurrently.

    :param tb_queue: Shared thread-safe queue for outgoing ThingsBoard data
    :type tb_queue: Queue
    :param mqtt_logger: Configured logger instance for operation tracking
    :type mqtt_logger: Optional[logging.Logger]
    :return: None (server starts in background thread)
    :rtype: None
    
    .. note::
        Thread Configuration:
        - Runs as daemon thread (terminates with main process)
        - Named thread for easier debugging and monitoring
        - Non-blocking operation allows concurrent application components
        
    .. tip::
        Use this function when integrating the MQTT server into a larger
        fleet management application that needs to run multiple services
        simultaneously.
        
    .. versionadded:: 1.0.0
        Initial implementation of background MQTT server startup
        
    Example:
        Non-blocking server startup for integration::
        
            from queue import Queue
            import logging
            from MQTT.grpc_mqtt import start_grpc_mqtt
            
            # Setup
            tb_queue = Queue()
            mqtt_logger = logging.getLogger('MQTT')
            
            # Start server in background
            start_grpc_mqtt(tb_queue, mqtt_logger)
            
            # Continue with other application components
            # ... rest of application code ...
    """
    # Create daemon thread for non-blocking server execution
    server_thread = threading.Thread(
        target=run_grpc_mqtt_server,  # Target function to execute in thread
        args=(tb_queue, mqtt_logger),  # Arguments for the target function
        name="MQTTgRPCServer",  # Descriptive thread name for debugging
        daemon=True  # Daemon thread terminates with main process
    )
    
    # Start the server thread (non-blocking)
    server_thread.start()

