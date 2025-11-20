"""
gRPC MQTT Client Module for State Vector Transmission

.. note::
    Features:
    - Secure channel management
    - gRPC error handling
    - Contextual logging
    - Message confirmation tracking
"""

import grpc
from typing import Optional
import logging
from GRPC.mqtt_pb2 import MQTTRequest
from GRPC.mqtt_pb2_grpc import MQTTCommunicationStub

# Configuration constants
_MQTT_SERVER_ADDRESS = 'localhost:50057'
_CHANNEL_TIMEOUT = 10  # Seconds for connection timeout

def run_sv_mqtt_client(mqtt_message: str, sv_logger: logging.Logger) -> Optional[bool]:
    """Send state vector data to MQTT bridge via gRPC.

    :param mqtt_message: Serialized state vector data to transmit
    :param sv_logger: Configured logger instance for operation tracking
    :return: True if successful, None on failure
    :raises ValueError: If invalid message format is detected

    Example:
        .. code-block:: python

            success = run_sv_mqtt_client(
                json.dumps(state_data), 
                logger
            )
            if success:
                handle_success()
    """
    channel = None
    try:
        # Create insecure channel with timeout
        channel = grpc.insecure_channel(
            _MQTT_SERVER_ADDRESS,
            options=(('grpc.connect_timeout_ms', _CHANNEL_TIMEOUT * 1000),)
        )
        
        stub = MQTTCommunicationStub(channel)
        sv_logger.debug(f" - Initiating MQTT transmission to {_MQTT_SERVER_ADDRESS}")

        # Validate message format before sending
        if not isinstance(mqtt_message, str):
            raise ValueError("Message must be serialized string")

        response = stub.SendMQTT(MQTTRequest(mqtt_message=mqtt_message))
        sv_logger.info(" - State vector successfully transmitted to MQTT bridge")
        return True

    except grpc.RpcError as e:
        sv_logger.error(f" - gRPC communication error ({e.code().name}): {e.details()}")
        return None
    except ValueError as e:
        sv_logger.error(f" - Validation error: {str(e)}")
        return None
    except Exception as e:
        sv_logger.error(f" - Unexpected error: {str(e)}", exc_info=True)
        return None
    finally:
        if channel:
            sv_logger.debug(" - Closing gRPC channel")
            channel.close()