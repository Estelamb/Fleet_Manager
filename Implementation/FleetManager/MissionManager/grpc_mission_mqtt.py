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
    channel = grpc.insecure_channel('localhost:50057')
    stub = MQTTCommunicationStub(channel)
    
    while True:
        try:
            mqtt_message = send_mqtt_queue.get(timeout=0.1)
            mission_logger.info("[gRPC MQTT] - Sending mission data to MQTT bridge")
            response = stub.SendMQTT(MQTTRequest(mqtt_message=mqtt_message))
            mission_logger.debug("[gRPC MQTT] - Acknowledgment received from MQTT bridge")
            
        except queue.Empty:
            time.sleep(0.1)
        except grpc.RpcError as e:
            mission_logger.error(
                f"[gRPC MQTT] - Connection error ({e.code().name}): {e.details()}"
            )
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
    client_thread = threading.Thread(
        target=run_client,
        args=(send_mqtt_queue, mission_logger),
        name="MQTTClientThread",
        daemon=True
    )
    
    client_thread.start()
    mission_logger.info("[gRPC MQTT] - Client communication thread started")


if __name__ == '__main__':
    # Example configuration
    import logging
    send_mqtt_queue = queue.Queue()
    
    # Configure basic logging
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] - [%(name)s][%(levelname)s] %(message)s'
    )
    mission_logger = logging.getLogger("MQTTComm")
    
    start_grpc_mission_mqtt(send_mqtt_queue, mission_logger)
    
    try:
        while True:
            time.sleep(3600)  # Keep main thread alive
    except KeyboardInterrupt:
        mission_logger.info("[gRPC MQTT] - Main process terminated")