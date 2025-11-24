"""
gRPC ROS2 Communication Module
==============================

This module provides bidirectional gRPC communication infrastructure for drone command 
execution and feedback processing between the drone system and ROS2 components.

The module implements a client-server architecture where the drone acts as both a gRPC 
server (receiving commands) and a gRPC client (sending feedback) to enable real-time 
communication with ROS2 mission control systems.

.. module:: grpc_drone_commands
    :synopsis: Provides bidirectional gRPC communication for ROS2 command execution

Workflow
--------
Command Processing Pipeline:
    1. **gRPC Server Initialization**: Start command reception server on port 51001
    2. **Command Reception**: Receive JSON command strings from ROS2 clients
    3. **Command Processing**: Parse and execute commands through commands_processor
    4. **Feedback Generation**: Generate execution results and status information
    5. **Feedback Transmission**: Send results back to ROS2 via gRPC client on port 51002

Communication Architecture:
    - **Inbound Channel**: Commands from ROS2 → Drone (Port 51001)
    - **Outbound Channel**: Feedback from Drone → ROS2 (Port 51002)
    - **Threading Model**: Multi-threaded server with configurable worker pool
    - **Error Handling**: Comprehensive exception management with logging

Features
--------
- **Bidirectional Communication**: Full duplex gRPC communication channels
- **Thread-Safe Operations**: Concurrent request handling with thread pool executor
- **Robust Error Handling**: Exception catching and logging for reliable operation
- **JSON Protocol**: Standardized JSON format for command and feedback data
- **Real-Time Processing**: Immediate command execution with instant feedback

Classes
-------
.. autoclass:: CommandCommunicationService
    :members:
    :show-inheritance:

Functions
---------
.. autofunction:: run_commands_server
.. autofunction:: run_feedback_client
.. autofunction:: start_grpc_commands

Protocol Buffer Definitions
---------------------------
- **command_pb2**: Command message structures for ROS2 communication
- **feedback_pb2**: Feedback message structures for result transmission

Port Configuration
------------------
- **Port 51001**: Inbound command reception from ROS2
- **Port 51002**: Outbound feedback transmission to ROS2

Notes
-----
This module requires active ROS2 nodes listening on the configured ports for 
successful bidirectional communication. The gRPC server runs continuously 
until manually stopped or interrupted.

See Also
--------
Commands.commands_processor : Command execution and processing logic
GRPC.definitions : Protocol buffer message definitions
"""

from concurrent import futures
import json
import grpc
import time
import queue
import threading
import logging
from typing import Any, Optional

from GRPC.definitions.command_pb2 import CommandResponse
from GRPC.definitions.command_pb2_grpc import CommandCommunicationServicer, add_CommandCommunicationServicer_to_server
from GRPC.definitions.feedback_pb2 import FeedbackRequest
from GRPC.definitions.feedback_pb2_grpc import FeedbackCommunicationStub

from Commands.commands_processor import process_command


class CommandCommunicationService(CommandCommunicationServicer):
    """
    gRPC service implementation for drone command reception and processing.
    
    This class implements the CommandCommunicationServicer interface to handle
    incoming command requests from ROS2 clients. It processes JSON-formatted
    commands and automatically sends feedback responses back to the ROS2 system.

    The service operates as part of a bidirectional communication system where
    commands flow from ROS2 to the drone, and feedback flows back to ROS2.

    Inherits
    --------
    CommandCommunicationServicer
        Base gRPC servicer class generated from protocol buffer definitions.

    Parameters
    ----------
    logger : logging.Logger
        Logger instance for recording gRPC communication events and errors.

    Attributes
    ----------
    logger : logging.Logger
        Logger for recording service operations and debugging information.

    Workflow
    --------
    1. **Command Reception**: Receive gRPC command request from ROS2 client
    2. **Data Extraction**: Convert protobuf command data to JSON string
    3. **Command Processing**: Execute command through commands_processor module
    4. **Feedback Generation**: Create JSON feedback with results and status
    5. **Feedback Transmission**: Send feedback to ROS2 via gRPC client
    6. **Response Confirmation**: Return acknowledgment to original command sender

    Methods
    -------
    SendCommand(request, context)
        Process incoming command requests and generate feedback responses.

    Examples
    --------
    >>> import logging
    >>> logger = logging.getLogger('command_service')
    >>> service = CommandCommunicationService(logger)
    >>> # Service is typically used within gRPC server context

    Notes
    -----
    This service handles all command types supported by the commands_processor
    module and automatically manages the feedback loop with ROS2 systems.
    """
    
    def __init__(self, logger: logging.Logger) -> None:
        super().__init__()
        self.logger = logger

    def SendCommand(self, request: Any, context: Any) -> CommandResponse:
        """
        Process incoming gRPC command requests and execute drone operations.

        This method serves as the main entry point for command processing in the gRPC
        service. It handles the complete workflow from command reception through
        execution and feedback transmission.

        Parameters
        ----------
        request : Any
            gRPC request object containing the command data in protobuf format.
            Expected to have a 'command' field with JSON command string.
        context : Any
            gRPC context object providing request metadata and communication context.

        Returns
        -------
        CommandResponse
            gRPC response object containing operation confirmation message.
            - "Command received" on successful processing
            - "Error processing command" on failure

        Workflow
        --------
        1. **Data Extraction**: Extract command list from protobuf request
        2. **JSON Reconstruction**: Convert command list back to JSON string
        3. **Command Parsing**: Parse JSON string to command dictionary
        4. **Command Execution**: Process command through commands_processor
        5. **Feedback Preparation**: Format execution results as JSON feedback
        6. **Feedback Transmission**: Send results to ROS2 via feedback client
        7. **Confirmation Response**: Return success/error confirmation

        Raises
        ------
        Exception
            Any processing errors are caught and logged, returning error response.

        Examples
        --------
        This method is typically called by the gRPC framework, not directly:
        
        >>> # Example command request (internal gRPC format)
        >>> # request.command = ["{'id': 1, 'command_type': 'NAV_TAKEOFF', ...}"]
        >>> response = service.SendCommand(request, context)
        >>> print(response.confirmation)  # "Command received"

        Notes
        -----
        - All exceptions are caught to ensure service stability
        - Failed commands return error responses rather than raising exceptions
        - Feedback is automatically sent to ROS2 regardless of processing outcome
        - The method logs all significant events for debugging and monitoring
        """
        try:
            # Extract command data from protobuf request format
            command_list = list(request.command)
            self.logger.info("[gRPC Commands] - Command received")
            
            # Reconstruct JSON string from command list
            command_str = ''.join(command_list)
            
            # Parse JSON string to command dictionary
            command = json.loads(command_str)

            # Execute command through the commands processor
            command_id, command_data, latitude, longitude = process_command(command, self.logger)

            # Prepare feedback data for ROS2 transmission
            feedback = json.dumps([command_id, command_data, latitude, longitude])

            # Send feedback back to ROS2 system
            run_feedback_client(feedback, self.logger)

            return CommandResponse(confirmation="Command received")
        except Exception as e:
            # Log error details and return error response
            self.logger.error(f"[gRPC Commands] - Error in SendCommand: {e}", exc_info=True)
            return CommandResponse(confirmation="Error processing command")


def run_commands_server(logger: logging.Logger) -> None:
    """
    Initialize and run the gRPC commands server for receiving ROS2 commands.

    This function sets up a multi-threaded gRPC server that listens for incoming
    command requests from ROS2 clients. The server runs continuously until
    manually interrupted, processing commands concurrently through a thread pool.

    Parameters
    ----------
    logger : logging.Logger
        Logger instance for recording server operations, startup events, and errors.

    Returns
    -------
    None
        This function runs indefinitely until interrupted.

    Workflow
    --------
    1. **Server Initialization**: Create gRPC server with thread pool executor
    2. **Service Registration**: Add CommandCommunicationService to server
    3. **Port Binding**: Bind server to port 51001 for command reception
    4. **Server Startup**: Start server and begin listening for requests
    5. **Continuous Operation**: Run indefinitely with daily sleep cycles
    6. **Graceful Shutdown**: Handle keyboard interrupt for clean termination

    Configuration
    -------------
    - **Port**: 51001 (insecure channel for command reception)
    - **Workers**: 10 concurrent thread pool workers
    - **Protocol**: gRPC with protobuf message serialization
    - **Binding**: All interfaces ([::]:51001)

    Examples
    --------
    >>> import logging
    >>> logger = logging.getLogger('grpc_server')
    >>> run_commands_server(logger)  # Runs until KeyboardInterrupt
    [gRPC Commands] - Server started

    Notes
    -----
    - Server runs in the calling thread (blocking operation)
    - Uses insecure channel for local/trusted network communication
    - Thread pool allows concurrent processing of multiple commands
    - KeyboardInterrupt (Ctrl+C) provides clean server shutdown
    - Server automatically logs startup and shutdown events

    Raises
    ------
    KeyboardInterrupt
        Handled gracefully to allow clean server shutdown.
    """
    # Create gRPC server with configurable thread pool for concurrent requests
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Register the command communication service with the server
    add_CommandCommunicationServicer_to_server(CommandCommunicationService(logger), server)
    
    # Bind server to port 51001 on all interfaces for command reception
    server.add_insecure_port('[::]:53001')
    
    # Start the server and begin listening for incoming requests
    server.start()
    logger.info("[gRPC Commands] - Server running on port 53001")
    
    try:
        # Keep server running with daily sleep cycles (24 hours = 86400 seconds)
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        # Handle graceful shutdown on Ctrl+C
        server.stop(0)


def run_feedback_client(feedback: str, logger: logging.Logger) -> None:
    """
    Send command execution feedback to ROS2 system via gRPC client.

    This function establishes a gRPC client connection to transmit command
    execution results and status information back to the ROS2 mission control
    system, completing the bidirectional communication loop.

    Parameters
    ----------
    feedback : str
        JSON-formatted feedback string containing command execution results.
        Typically includes command ID, execution status, and result data.
    logger : logging.Logger
        Logger instance for recording feedback transmission events and errors.

    Returns
    -------
    None
        Function completes after feedback transmission attempt.

    Workflow
    --------
    1. **Channel Creation**: Establish insecure gRPC channel to ROS2 (port 51002)
    2. **Stub Initialization**: Create FeedbackCommunicationStub for RPC calls
    3. **Feedback Transmission**: Send feedback via SendFeedback RPC method
    4. **Acknowledgment**: Log successful feedback transmission and ROS2 response
    5. **Error Handling**: Catch and log connection errors with retry delay

    Configuration
    -------------
    - **Target**: [::]:51002 (ROS2 feedback reception port)
    - **Protocol**: gRPC with protobuf FeedbackRequest messages
    - **Channel Type**: Insecure (for local/trusted network communication)
    - **Retry Strategy**: Simple delay on connection errors

    Parameters Format
    -----------------
    feedback (JSON string structure):
        [command_id, command_data]
        - command_id (int): Unique identifier of executed command
        - command_data: Command-specific execution results

    Error Handling
    --------------
    - **queue.Empty**: Handled with brief sleep (legacy exception handling)
    - **grpc.RpcError**: Connection errors logged with 1-second retry delay
    - **General Exceptions**: Not explicitly caught (will propagate)

    Notes
    -----
    - Function assumes ROS2 feedback service is running on port 51002
    - Connection errors result in logged warnings but don't raise exceptions
    - Each feedback transmission is independent (no persistent connection)
    - Function returns immediately after single transmission attempt

    See Also
    --------
    GRPC.definitions.feedback_pb2 : Feedback message structure definitions
    """
    # Establish insecure gRPC channel to ROS2 feedback service
    channel = grpc.insecure_channel('[::]:53002') 
    
    # Create stub for feedback communication RPC calls
    stub = FeedbackCommunicationStub(channel)

    try:
        # Send feedback data to ROS2 via gRPC call
        response = stub.SendFeedback(FeedbackRequest(feedback=feedback))
        
        logger.info("[gRPC Commands] - Feedback sent to ROS2")
    except queue.Empty:
        # Handle queue empty exception (legacy error handling)
        time.sleep(0.1)
    except grpc.RpcError as e:
        # Handle gRPC connection and communication errors
        logger.error(f"[gRPC Commands] - Connection error: {e}")
        time.sleep(1)


def start_grpc_commands(logger: logging.Logger) -> None:
    """
    Initialize and start the gRPC commands communication system in a separate thread.

    This function serves as the main entry point for starting the drone's gRPC
    command reception system. It creates a dedicated thread for the gRPC server
    to ensure non-blocking operation within the main application workflow.

    Parameters
    ----------
    logger : logging.Logger
        Logger instance for recording gRPC system startup events and operations.

    Returns
    -------
    None
        Function returns immediately after starting the background thread.

    Workflow
    --------
    1. **Thread Creation**: Create dedicated thread for gRPC commands server
    2. **Thread Configuration**: Configure thread with server function and logger
    3. **Thread Startup**: Start thread to begin gRPC server operations
    4. **Non-Blocking Return**: Return control to caller while server runs

    Threading Architecture
    ----------------------
    - **Main Thread**: Application continues normal execution
    - **gRPC Thread**: Dedicated thread runs commands server indefinitely
    - **Thread Safety**: Server operations isolated from main application flow
    - **Resource Management**: Thread handles its own lifecycle and cleanup

    Notes
    -----
    - Thread runs the gRPC server indefinitely until system shutdown
    - Non-blocking design allows integration with other drone subsystems
    - Server thread inherits logger configuration for consistent logging
    - Thread is not joined, allowing daemon-like background operation
    - System shutdown or KeyboardInterrupt will terminate the server thread

    See Also
    --------
    run_commands_server : The actual gRPC server implementation
    CommandCommunicationService : gRPC service for command processing
    """
    # Create dedicated thread for gRPC commands server
    server_commands_thread = threading.Thread(
        target=run_commands_server,  # Server function to run in background
        args=(logger,)              # Pass logger to server thread
    )
    
    # Start the gRPC server thread (non-blocking operation)
    server_commands_thread.start()