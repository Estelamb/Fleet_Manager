"""
gRPC Prescription Map (PM) Communication Module

.. module:: grpc_pm_client
    :synopsis: Provides gRPC client implementation for Prescription Map communication

.. note::
    Features:
    - Continuous message sending from queue to PM service
    - Automatic reconnection on communication errors
    - Thread-safe operation for concurrent access
    - Prescription Map data transmission and acknowledgment
"""

import grpc
import queue
import time
import threading
import logging
from typing import Optional

from GRPC.pm_pb2 import PMRequest
from GRPC.pm_pb2_grpc import PMCommunicationStub


def run_client(pm_queue: queue.Queue, mission_logger: logging.Logger) -> None:
    """Continuous client operation for sending PM messages via gRPC.

    Args:
        pm_queue: Queue containing outgoing PM messages
        mission_logger: Configured logger instance for mission operations

    Raises:
        grpc.RpcError: For communication failures with the PM service
    """
    # Establish insecure gRPC channel to Prescription Map service
    # Port 50087 is the dedicated PM communication endpoint
    channel = grpc.insecure_channel('localhost:50087')
    stub = PMCommunicationStub(channel)
    
    # Infinite loop for continuous PM message processing
    # Ensures persistent communication with Prescription Map service
    while True:
        try:
            # Attempt to retrieve PM message from queue with timeout
            # Short timeout prevents blocking while allowing responsive message handling
            pm_message = pm_queue.get(timeout=0.1)
            mission_logger.info("[gRPC PM] - Sending mission data to PM")
            
            # Send Prescription Map message via gRPC call to PM service
            response = stub.SendPM(PMRequest(pm_message=pm_message))
            mission_logger.debug("[gRPC PM] - Acknowledgment received from PM")

        except queue.Empty:
            # No messages available in queue - brief sleep to prevent CPU spinning
            time.sleep(0.1)
        except grpc.RpcError as e:
            # Handle gRPC communication errors with automatic retry logic
            # Logs specific error details for debugging and monitoring
            mission_logger.error(
                f"[gRPC PM] - Connection error ({e.code().name}): {e.details()}"
            )
            # Wait before retry to prevent rapid failure loops
            time.sleep(1)


def start_grpc_mission_pm(
    pm_queue: queue.Queue,
    mission_logger: logging.Logger
) -> None:
    """Initialize and start the PM gRPC client thread.

    Args:
        pm_queue: Thread-safe queue for outgoing messages
        mission_logger: Configured logger instance

    Example:
        >>> start_grpc_mission_pm(message_queue, logger)
    """
    # Create dedicated daemon thread for PM client operations
    # Daemon status ensures thread terminates when main process exits
    # Named thread aids in debugging and process monitoring
    client_thread = threading.Thread(
        target=run_client,
        args=(pm_queue, mission_logger),
        name="PMClientThread",
        daemon=True
    )
    
    # Start thread execution and log successful initialization
    client_thread.start()
    mission_logger.info("[gRPC PM] - Client communication thread started")


if __name__ == '__main__':
    # Standalone execution example and testing configuration
    # Demonstrates proper initialization and usage patterns for PM communication
    import logging
    pm_queue = queue.Queue()
    
    # Configure basic logging with timestamp and level information
    # Format provides comprehensive debugging information for production use
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] - [%(name)s][%(levelname)s] %(message)s'
    )
    mission_logger = logging.getLogger("PM")
    
    # Initialize PM gRPC client with configured queue and logger
    start_grpc_mission_pm(pm_queue, mission_logger)
    
    try:
        # Keep main thread alive indefinitely for continuous operation
        # Long sleep interval reduces CPU usage while maintaining process
        while True:
            time.sleep(3600)  # Keep main thread alive
    except KeyboardInterrupt:
        # Graceful shutdown on user interruption (Ctrl+C)
        # Ensures proper cleanup and logging of termination
        mission_logger.info("[gRPC PM] - Main process terminated")