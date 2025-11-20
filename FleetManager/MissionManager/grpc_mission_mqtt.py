"""
gRPC MQTT Communication Module

.. module:: grpc_mqtt_client
    :synopsis: Provides gRPC client implementation for MQTT communication

.. note::
    Features:
    - Continuous message sending from queue
    - Automatic reconnection on errors
    - Thread-safe operation
"""

import grpc
import queue
import time
import threading
import logging
from typing import Optional

from GRPC.mqtt_pb2 import MQTTRequest
from GRPC.mqtt_pb2_grpc import MQTTCommunicationStub


def run_client(send_mqtt_queue: queue.Queue, mission_logger: logging.Logger) -> None:
    """Continuous client operation for sending MQTT messages via gRPC.

    Args:
        send_mqtt_queue: Queue containing outgoing MQTT messages
        mission_logger: Configured logger instance for mission operations

    Raises:
        grpc.RpcError: For communication failures with the MQTT service
    """
    # Establish insecure gRPC channel to MQTT service
    # Port 50057 is the dedicated MQTT communication endpoint
    channel = grpc.insecure_channel('localhost:50057')
    stub = MQTTCommunicationStub(channel)
    
    # Infinite loop for continuous message processing
    # Ensures persistent communication with MQTT bridge service
    while True:
        try:
            # Attempt to retrieve message from queue with timeout
            # Short timeout prevents blocking while allowing responsive message handling
            mqtt_message = send_mqtt_queue.get(timeout=0.1)
            mission_logger.info("[gRPC MQTT] - Sending mission data to MQTT bridge")
            
            # Send MQTT message via gRPC call to bridge service
            response = stub.SendMQTT(MQTTRequest(mqtt_message=mqtt_message))
            mission_logger.debug("[gRPC MQTT] - Acknowledgment received from MQTT bridge")
            
        except queue.Empty:
            # No messages available in queue - brief sleep to prevent CPU spinning
            time.sleep(0.1)
        except grpc.RpcError as e:
            # Handle gRPC communication errors with automatic retry logic
            # Logs specific error details for debugging and monitoring
            mission_logger.error(
                f"[gRPC MQTT] - Connection error ({e.code().name}): {e.details()}"
            )
            # Wait before retry to prevent rapid failure loops
            time.sleep(1)


def start_grpc_mission_mqtt(
    send_mqtt_queue: queue.Queue,
    mission_logger: logging.Logger
) -> None:
    """Initialize and start the MQTT gRPC client thread.

    Args:
        send_mqtt_queue: Thread-safe queue for outgoing messages
        mission_logger: Configured logger instance

    Example:
        >>> start_grpc_mission_mqtt(message_queue, logger)
    """
    # Create dedicated daemon thread for MQTT client operations
    # Daemon status ensures thread terminates when main process exits
    # Named thread aids in debugging and process monitoring
    client_thread = threading.Thread(
        target=run_client,
        args=(send_mqtt_queue, mission_logger),
        name="MQTTClientThread",
        daemon=True
    )
    
    # Start thread execution and log successful initialization
    client_thread.start()
    mission_logger.info("[gRPC MQTT] - Client communication thread started")


if __name__ == '__main__':
    # Standalone execution example and testing configuration
    # Demonstrates proper initialization and usage patterns
    import logging
    send_mqtt_queue = queue.Queue()
    
    # Configure basic logging with timestamp and level information
    # Format provides comprehensive debugging information for production use
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] - [%(name)s][%(levelname)s] %(message)s'
    )
    mission_logger = logging.getLogger("MQTTComm")
    
    # Initialize MQTT gRPC client with configured queue and logger
    start_grpc_mission_mqtt(send_mqtt_queue, mission_logger)
    
    try:
        # Keep main thread alive indefinitely for continuous operation
        # Long sleep interval reduces CPU usage while maintaining process
        while True:
            time.sleep(3600)  # Keep main thread alive
    except KeyboardInterrupt:
        # Graceful shutdown on user interruption (Ctrl+C)
        # Ensures proper cleanup and logging of termination
        mission_logger.info("[gRPC MQTT] - Main process terminated")