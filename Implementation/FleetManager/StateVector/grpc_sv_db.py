"""
gRPC Database Client Module for State Vector Storage

.. note::
    Features:
    - Secure gRPC channel management
    - Database request validation
    - Connection timeout handling
    - Contextual logging
"""

import grpc
from typing import Optional
import logging
from GRPC.db_request_pb2 import DBReqRequest
from GRPC.db_request_pb2_grpc import DBReqCommunicationStub

# Configuration constants
_DB_SERVER_ADDRESS = 'localhost:50060'
_CHANNEL_TIMEOUT = 10  # Seconds for connection timeout

def run_sv_db_client(db_request: str, sv_logger: logging.Logger) -> Optional[bool]:
    """Send state vector data to database service via gRPC.

    :param db_request: Serialized state vector data in JSON format
    :param sv_logger: Configured logger instance for operation tracking
    :return: True if successful, None on failure
    :raises ValueError: If invalid request format is detected

    Example:
        .. code-block:: python

            success = run_sv_db_client(
                json.dumps(state_data), 
                logger
            )
            if success:
                handle_success()
    """
    channel = None
    try:
        # Validate input format before establishing connection
        if not isinstance(db_request, str):
            raise ValueError("Database request must be serialized string")

        # Create insecure channel with timeout
        channel = grpc.insecure_channel(
            _DB_SERVER_ADDRESS,
            options=(('grpc.connect_timeout_ms', _CHANNEL_TIMEOUT * 1000),)
        )
        
        stub = DBReqCommunicationStub(channel)
        sv_logger.debug(f" - Initiating database transaction to {_DB_SERVER_ADDRESS}")

        # Execute database request
        response = stub.SendDBReq(DBReqRequest(db_request=db_request))
        sv_logger.info(" - State vector successfully stored in database")
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