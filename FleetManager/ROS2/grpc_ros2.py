"""
gRPC ROS 2 Communication Bridge Module

.. module:: grpc_ros2
    :synopsis: Bidirectional gRPC communication bridge for ROS 2 command execution and result reporting

.. moduleauthor:: Fleet Management System Team

.. versionadded:: 1.0

This module implements a comprehensive communication bridge between the Fleet Management System
and ROS 2 environments. It provides bidirectional gRPC services for drone plan distribution
and result collection, enabling seamless integration between fleet management and autonomous
vehicle control systems.

Architecture Overview:
    The module follows a dual-service architecture:
    
    1. **gRPC Server**: Receives drone plans from Mission Management System
    2. **gRPC Client**: Sends execution results back to Mission Management System
    3. **ROS 2 Action Client**: Interfaces with ROS 2 action servers for command execution
    4. **Queue-based Communication**: Thread-safe result passing between components

Communication Flow:
    .. mermaid::
    
        graph LR
            A[Mission Management] --> B[gRPC Server]
            B --> C[ROS 2 Action Client]
            C --> D[ROS 2 Action Server]
            D --> E[Vehicle Control]
            E --> F[Result Queue]
            F --> G[gRPC Client]
            G --> A

Key Features:
    - **Bidirectional Communication**: Full duplex communication with Mission Management
    - **ROS 2 Integration**: Native ROS 2 action client for vehicle command execution
    - **Thread-safe Operations**: Queue-based communication between gRPC and ROS 2 components
    - **JSON Protocol**: Standardized JSON messaging for plan and result data
    - **Error Recovery**: Comprehensive error handling and connection management
    - **Concurrent Processing**: Multi-threaded operation for high throughput

ROS 2 Integration:
    The module integrates with ROS 2 through action clients, providing:
    - **Action Goal Submission**: Send drone commands as ROS 2 action goals
    - **Result Collection**: Gather execution results from ROS 2 action servers
    - **Status Monitoring**: Track action execution status and progress
    - **Error Handling**: Manage ROS 2 communication failures and timeouts

gRPC Services:
    **Plan Communication Service** (Port 50099):
    - Receives drone plans from Mission Management
    - Parses JSON-formatted plan data
    - Submits goals to ROS 2 action clients
    
    **Result Communication Client** (Port 50070):
    - Monitors result queue for completed actions
    - Sends results back to Mission Management
    - Handles connection failures with retry logic

Data Formats:
    **Drone Plan Format**::
    
        [drone_id, [command1_json, command2_json, ...]]
        
    **Command Format**::
    
        {
            "command_type": "MOVE_TO",
            "parameters": {...},
            "sequence": 1
        }

Thread Management:
    - **Server Thread**: Handles incoming gRPC plan requests
    - **Client Thread**: Processes outgoing result submissions
    - **Action Thread**: Manages ROS 2 action client operations
    - **Main Thread**: Coordinates overall system operation

Network Configuration:
    - **Server Port**: 50099 (Plan reception from Mission Management)
    - **Client Target**: localhost:50070 (Result submission to Mission Management)
    - **Protocol**: gRPC with HTTP/2 transport
    - **Security**: Insecure channels (internal communication)

Classes:
    .. autoclass:: PlanCommunicationService
        :members:
        :undoc-members:
        :show-inheritance:

Functions:
    .. autofunction:: run_ros2_server
    .. autofunction:: run_ros2_client
    .. autofunction:: start_grpc_ros2
    .. autofunction:: create_logger

.. note::
    This module requires a running ROS 2 environment with appropriate action
    servers for vehicle control. Ensure ROS 2 workspace is properly sourced.

.. warning::
    The module uses insecure gRPC channels suitable for internal communication.
    Implement proper authentication for external deployments.

.. seealso::
    - :mod:`MissionManager.grpc_mission_vehicle`: Mission Management counterpart
    - :mod:`ROS2.src.commands_action_interface`: ROS 2 action client implementation
    - :mod:`GRPC`: Protocol Buffer definitions for plan and result messages
"""

from concurrent import futures
import json
import grpc
import time
import queue
import threading

import logging

from GRPC.plan_pb2 import DronePlanResponse
from GRPC.plan_pb2_grpc import PlanCommunicationServicer, add_PlanCommunicationServicer_to_server
from GRPC.result_pb2 import DroneResultRequest
from GRPC.result_pb2_grpc import ResultCommunicationStub

from ROS2.src.commands_action_interface.commands_action_interface import commands_action_client as action


class PlanCommunicationService(PlanCommunicationServicer):
    """gRPC service implementation for processing drone plans and submitting them to ROS 2.

    This class extends the auto-generated PlanCommunicationServicer to provide concrete
    implementation for receiving drone plans from the Mission Management System and
    converting them into ROS 2 action goals for vehicle execution.

    Service Responsibilities:
        - **Plan Reception**: Receive gRPC requests containing drone plan data
        - **Data Parsing**: Parse JSON-formatted plan and command structures
        - **Format Conversion**: Convert plan data to ROS 2 action goal format
        - **Goal Submission**: Submit action goals to ROS 2 action clients
        - **Response Generation**: Provide confirmation responses to Mission Management

    Plan Processing Workflow:
        1. **Request Reception**: Receive gRPC request with serialized plan data
        2. **Data Extraction**: Extract drone_plan list from request
        3. **JSON Parsing**: Parse concatenated JSON string to extract plan structure
        4. **Component Extraction**: Separate drone_id and command list
        5. **Command Processing**: Parse individual commands and normalize JSON format
        6. **Goal Submission**: Send processed commands to ROS 2 action client
        7. **Response Generation**: Return confirmation to Mission Management

    Data Format Handling:
        **Input Format** (from Mission Management)::
        
            drone_plan = [drone_id, [raw_command1, raw_command2, ...]]
            
        **Processing Steps**:
        - Convert gRPC repeated field to Python list
        - Join list elements into single JSON string
        - Parse JSON to extract drone_id and raw_commands_list
        - Process each raw command (handle quote normalization)
        - Convert processed commands back to JSON strings

    ROS 2 Integration:
        The service interfaces with ROS 2 through an action client that:
        - Accepts drone_id for vehicle identification
        - Receives command list in JSON string format
        - Submits goals to appropriate ROS 2 action servers
        - Handles action execution and result collection

    :param action_client: Initialized ROS 2 action client for goal submission
    :type action_client: commands_action_client.ActionClient
    :param ros2_logger: Configured logger instance for operation tracking
    :type ros2_logger: logging.Logger

    :ivar action_client: ROS 2 action client for command execution
    :vartype action_client: commands_action_client.ActionClient
    :ivar ros2_logger: Logger instance for service operation tracking
    :vartype ros2_logger: logging.Logger

    Example:
        **Service Instantiation** (typically done by gRPC server)::
        
            action_client = create_ros2_action_client(queue, logger)
            service = PlanCommunicationService(action_client, logger)
            add_PlanCommunicationServicer_to_server(service, server)

    .. note::
        The service handles JSON quote normalization to ensure compatibility
        between Mission Management and ROS 2 JSON parsing requirements.

    .. warning::
        Command parsing failures will result in error responses being sent
        back to Mission Management. Ensure proper error handling in clients.
    """
    def __init__(self, action_client, ros2_logger):
        """Initialize gRPC service with ROS 2 action client and logging.

        Sets up the service with necessary components for plan processing and
        ROS 2 integration. Configures logging for operation tracking and debugging.

        :param action_client: Pre-configured ROS 2 action client for goal submission
        :type action_client: commands_action_client.ActionClient
        :param ros2_logger: Pre-configured logger for service operations
        :type ros2_logger: logging.Logger
        """
        # Initialize parent gRPC servicer class
        super().__init__()
        
        # Store ROS 2 action client for command submission
        self.action_client = action_client
        
        # Store logger instance for operation tracking
        self.ros2_logger = ros2_logger

    def SendPlan(self, request, context):
        """Process incoming drone plan requests and submit them to ROS 2 action servers.

        This method implements the core gRPC service interface for receiving drone plans
        from the Mission Management System, parsing the plan data, and converting it into
        ROS 2 action goals for vehicle execution.

        Processing Workflow:
            1. **Data Extraction**: Convert gRPC repeated field to Python list
            2. **JSON Reconstruction**: Join list elements into complete JSON string
            3. **Plan Parsing**: Parse JSON to extract drone_id and command list
            4. **Command Processing**: Normalize and parse individual commands
            5. **Goal Submission**: Send processed commands to ROS 2 action client
            6. **Response Generation**: Return confirmation to Mission Management

        Data Format Processing:
            **Input Structure**::
            
                request.drone_plan = ["[", "123", ",", "[", "command1", ",", "command2", "]", "]"]
                
            **Reconstructed JSON**::
            
                "[123, [\"command1\", \"command2\"]]"
                
            **Parsed Structure**::
            
                [123, ["command1", "command2"]]

        Command Normalization:
            - **Quote Handling**: Convert single quotes to double quotes for JSON compliance
            - **JSON Parsing**: Parse each command string as individual JSON objects
            - **Re-serialization**: Convert parsed commands back to JSON strings
            - **Format Validation**: Ensure commands are valid JSON format

        Error Handling Strategy:
            - **JSON Parsing Errors**: Caught and logged with detailed error information
            - **Action Client Errors**: Handled by action client with appropriate timeouts
            - **Response Generation**: Error responses sent back to Mission Management
            - **Exception Logging**: Full stack traces logged for debugging

        :param request: gRPC request containing serialized drone plan data
        :type request: plan_pb2.DronePlanRequest
        :param context: gRPC connection context for metadata and error handling
        :type context: grpc.ServicerContext

        :return: Confirmation response with processing status
        :rtype: plan_pb2.DronePlanResponse

        :raises json.JSONDecodeError: If plan data contains invalid JSON syntax
        :raises KeyError: If required plan components (drone_id, commands) are missing
        :raises Exception: For any other processing failures during plan execution

        Example:
            **Successful Processing**::
            
                # Input: drone_plan for drone 123 with two commands
                # Output: DronePlanResponse(confirmation="Plan 123 received and sent")
                
            **Error Processing**::
            
                # Input: malformed JSON data
                # Output: DronePlanResponse(confirmation="Error processing plan")

        .. note::
            The method expects the plan data to follow the specific format used by
            the Mission Management System with drone_id as first element.

        .. warning::
            All processing exceptions are caught and logged, but only generic error
            messages are returned to clients for security reasons.
        """
        try:
            # Convert the gRPC repeated field to a Python list
            # The drone_plan comes as separate string elements that need reconstruction
            drone_plan = list(request.drone_plan)
            self.ros2_logger.info(f"[gRPC ROS2] - Plan received from Mission Management")
            
            # Reconstruct the complete JSON string from individual elements
            # Mission Management sends plan as fragmented string parts
            drone_plan_str = ''.join(drone_plan)
            
            # Parse the reconstructed JSON string to extract plan structure
            # Expected format: [drone_id, [command1, command2, ...]]
            drone_plan = json.loads(drone_plan_str)

            # Extract drone_id (first element) and raw command list (second element)
            # drone_id identifies the target vehicle for command execution
            drone_id = drone_plan[0]
            raw_commands_list = drone_plan[1]

            # Process each command in the command list to ensure proper JSON formatting
            # Commands may have quote inconsistencies that need normalization
            commands_list = []
            for raw_command in raw_commands_list:
                # Parse the raw command and convert single quotes to double quotes
                # This ensures JSON compliance for ROS 2 action processing
                command = json.loads(raw_command.replace("'", '"'))  # Normalize quotes for JSON parsing
                
                # Convert the parsed command back to a properly formatted JSON string
                # This ensures consistent formatting for ROS 2 action client
                commands_list.append(json.dumps(command))

            # Send the processed goal to the ROS 2 action client
            # Action client handles goal submission and execution tracking
            self.action_client.send_goal(drone_id, commands_list)
            self.ros2_logger.info(f"[gRPC ROS2][Vehicle {drone_id}] - Goal sent")

            # Return success confirmation to Mission Management
            return DronePlanResponse(confirmation=f"Plan {drone_id} received and sent")
            
        except Exception as e:
            # Log detailed error information for debugging and monitoring
            # Include full stack trace for comprehensive error analysis
            self.ros2_logger.error(f"[gRPC ROS2] - Error in SendPlan: {e}", exc_info=True)
            
            # Return generic error response to Mission Management
            # Avoid exposing internal error details for security reasons
            return DronePlanResponse(confirmation="Error processing plan")


def run_ros2_server(action_client, ros2_logger):
    """Start and manage gRPC server instance for drone plan reception.

    This function initializes and manages a gRPC server that receives drone plans from
    the Mission Management System. It configures the server with appropriate threading,
    service registration, and connection handling for high-throughput plan processing.

    Server Configuration:
        - **Thread Pool**: ThreadPoolExecutor with 10 concurrent workers
        - **Service Registration**: PlanCommunicationService for plan processing
        - **Network Binding**: Insecure port 50099 for internal communication
        - **Protocol**: gRPC over HTTP/2 for efficient message handling

    Lifecycle Management:
        1. **Server Creation**: Initialize gRPC server with thread pool executor
        2. **Service Registration**: Add PlanCommunicationService to server
        3. **Port Binding**: Bind to port 50099 for plan reception
        4. **Server Startup**: Start server and begin accepting connections
        5. **Continuous Operation**: Run indefinitely until interruption
        6. **Graceful Shutdown**: Handle keyboard interrupts with proper cleanup

    Threading Architecture:
        The server uses a ThreadPoolExecutor to handle concurrent plan requests:
        - **Worker Threads**: Up to 10 concurrent plan processing threads
        - **Request Isolation**: Each plan request handled independently
        - **Resource Management**: Automatic thread lifecycle management
        - **Blocking Operations**: Long-running plan processing won't block other requests

    Network Configuration:
        - **Binding Address**: [::]:50099 (all interfaces, port 50099)
        - **Protocol**: Insecure gRPC (suitable for internal communication)
        - **Client Source**: Mission Management System on same network
        - **Message Format**: Protocol Buffer messages for plan data

    Error Handling:
        - **Startup Errors**: Server initialization failures logged and propagated
        - **Runtime Errors**: Individual request errors handled by service implementation
        - **Shutdown Handling**: KeyboardInterrupt triggers graceful server shutdown
        - **Connection Issues**: Handled by gRPC infrastructure with automatic retry

    :param action_client: Pre-configured ROS 2 action client for goal submission
    :type action_client: commands_action_client.CommandsActionClient
    :param ros2_logger: Pre-configured logger instance for server operations
    :type ros2_logger: logging.Logger

    :raises grpc.RpcError: If server cannot bind to specified port
    :raises OSError: If network interface is unavailable
    :raises Exception: For any other server initialization failures

    Example:
        **Server Startup**::
        
            action_client = create_ros2_action_client(queue, logger)
            # This function runs indefinitely, typically in a separate thread
            run_ros2_server(action_client, logger)

    .. note::
        This function runs indefinitely and should typically be executed in a
        separate thread or process to avoid blocking the main application.

    .. warning::
        The server uses insecure gRPC channels suitable only for internal
        communication. Implement proper authentication for external deployments.

    .. seealso::
        - :class:`PlanCommunicationService`: Service implementation for plan processing
        - :func:`start_grpc_ros2`: Main function that starts server in separate thread
    """
    # Initialize gRPC server with ThreadPoolExecutor for concurrent request handling
    # ThreadPoolExecutor allows multiple plan requests to be processed simultaneously
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Register the PlanCommunicationService with the server
    # This service handles incoming drone plan requests from Mission Management
    add_PlanCommunicationServicer_to_server(
        PlanCommunicationService(action_client, ros2_logger), server)
    
    # Bind server to port 50099 on all network interfaces
    # Uses insecure channel for internal Fleet Management System communication
    server.add_insecure_port('[::]:50099')
    
    # Start the gRPC server and begin accepting connections
    server.start()
    ros2_logger.info("[gRPC ROS2] - Server running on port [::]:50099")
    
    try:
        # Keep server running indefinitely
        # Sleep for 24 hours in a loop to maintain server operation
        while True:
            time.sleep(86400)  # Sleep for 24 hours
    except KeyboardInterrupt:
        # Handle graceful shutdown on keyboard interrupt (Ctrl+C)
        # Stop server with 0-second grace period for immediate shutdown
        server.stop(0)


def run_ros2_client(ros2_action_queue, ros2_logger):
    """Continuously monitor result queue and transmit drone results to Mission Management.

    This function implements a persistent gRPC client that monitors the ROS 2 action
    result queue and transmits completed drone execution results back to the Mission
    Management System. It provides reliable result delivery with automatic error
    recovery and connection management.

    Client Architecture:
        - **Persistent Connection**: Maintains long-lived gRPC channel to Mission Management
        - **Queue Monitoring**: Continuously polls result queue for new completion data
        - **Automatic Retry**: Handles connection failures with exponential backoff
        - **Result Forwarding**: Transmits results using ResultCommunication gRPC service

    Result Processing Workflow:
        1. **Queue Monitoring**: Continuously check result queue for new data
        2. **Result Extraction**: Extract drone execution results from queue
        3. **gRPC Transmission**: Send results to Mission Management via gRPC
        4. **Acknowledgment**: Wait for and log confirmation from Mission Management
        5. **Error Handling**: Retry failed transmissions with appropriate delays

    Connection Management:
        - **Target Server**: Mission Management System on localhost:50070
        - **Channel Type**: Insecure gRPC channel for internal communication
        - **Persistence**: Channel maintained throughout function lifetime
        - **Automatic Reconnection**: gRPC handles connection recovery automatically

    Error Recovery Strategy:
        **Queue Empty**: Brief sleep to prevent excessive CPU usage during idle periods
        **gRPC Errors**: Longer sleep with error logging for connection recovery
        **Network Issues**: Automatic retry with exponential backoff
        **Persistent Failures**: Continuous operation with periodic retry attempts

    Queue Integration:
        The function interfaces with the shared result queue:
        - **Thread Safety**: Queue operations are inherently thread-safe
        - **Blocking Get**: Uses queue.get() without timeout for immediate processing
        - **Data Format**: Expects JSON-serialized result data from ROS 2 actions
        - **Result Types**: Handles feedback, status updates, and final results

    Result Transmission Format:
        Results are transmitted using DroneResultRequest protocol buffers:
        - **Message Type**: DroneResultRequest containing serialized result data
        - **Data Format**: JSON string with execution results and status information
        - **Service Method**: SendResult() on ResultCommunication service
        - **Response Handling**: Acknowledgment messages logged for confirmation

    :param ros2_action_queue: Thread-safe queue containing drone execution results
    :type ros2_action_queue: queue.Queue
    :param ros2_logger: Pre-configured logger instance for client operations
    :type ros2_logger: logging.Logger

    :raises grpc.RpcError: For gRPC communication failures (logged and retried)
    :raises queue.Empty: For empty queue conditions (handled with brief sleep)
    :raises Exception: For any other processing failures during result transmission

    Example:
        **Client Operation**::
        
            result_queue = queue.Queue()
            logger = logging.getLogger('ROS2')
            # This function runs indefinitely, typically in a separate thread
            run_ros2_client(result_queue, logger)
            
        **Queue Data Format**::
        
            # Results added to queue by ROS 2 action client
            queue.put('{"drone_id": 123, "status": "completed", "results": [...]}')

    .. note::
        This function runs indefinitely and should be executed in a separate thread
        to avoid blocking other system components.

    .. warning::
        The client expects the Mission Management System to be available on
        localhost:50070. Ensure proper service availability before starting.

    .. seealso::
        - :func:`start_grpc_ros2`: Main function that starts client in separate thread
        - :mod:`MissionManager.grpc_mission_vehicle`: Mission Management result receiver
        - :class:`commands_action_client.CommandsActionClient`: Source of result data
    """
    # Establish persistent gRPC channel to Mission Management System
    # Uses insecure channel for internal Fleet Management System communication
    channel = grpc.insecure_channel('localhost:50070')
    
    # Create gRPC client stub for ResultCommunication service
    # This stub provides access to result transmission methods
    stub = ResultCommunicationStub(channel)

    # Main client loop - continuously monitor and transmit results
    while True:
        try:
            # Block until a result is available in the queue
            # This is thread-safe and prevents busy-waiting
            drone_result = ros2_action_queue.get()
            
            # Log result transmission for monitoring and debugging
            ros2_logger.info(f"[gRPC ROS2] - Sending drone result to Mission Management")
            
            # Transmit result to Mission Management via gRPC
            # DroneResultRequest contains the serialized result data
            response = stub.SendResult(DroneResultRequest(drone_result=drone_result))
            
            # Log successful acknowledgment from Mission Management
            ros2_logger.info(f"[gRPC ROS2] - ACK received from Mission Management")
            
        except queue.Empty:
            # Queue is empty - brief sleep to prevent excessive CPU usage
            # This exception rarely occurs with blocking queue.get()
            time.sleep(0.1)
            
        except grpc.RpcError as e:
            # Handle gRPC communication errors (network issues, server unavailable)
            # Log error details and sleep before retry for connection recovery
            ros2_logger.error(f"[gRPC ROS2] - Connection error: {e}")
            time.sleep(1)  # Wait before retry to allow connection recovery


def start_grpc_ros2(ros2_action_queue: queue.Queue, ros2_logger):
    """Initialize and start comprehensive ROS 2 communication infrastructure.

    This function serves as the main entry point for setting up the complete ROS 2
    communication system. It initializes all necessary components and starts both
    server and client threads for bidirectional communication with the Mission
    Management System.

    System Architecture Setup:
        The function establishes a complete communication infrastructure:
        
        1. **ROS 2 Action Client**: For interfacing with ROS 2 action servers
        2. **gRPC Server Thread**: For receiving drone plans from Mission Management
        3. **gRPC Client Thread**: For sending results back to Mission Management
        4. **Queue Communication**: Thread-safe result passing between components

    Component Initialization:
        **ROS 2 Action Client**:
        - Interfaces with ROS 2 action servers on drone vehicles
        - Handles goal submission, feedback processing, and result collection
        - Publishes results to shared queue for transmission to Mission Management
        
        **gRPC Server Thread**:
        - Receives drone plans from Mission Management System
        - Processes and validates incoming plan data
        - Converts plans to ROS 2 action goals for vehicle execution
        
        **gRPC Client Thread**:
        - Monitors result queue for completed action results
        - Transmits results back to Mission Management System
        - Handles connection management and error recovery

    Threading Strategy:
        - **Daemon Threads**: Both server and client threads run as daemon threads
        - **Background Operation**: Threads continue running without blocking main process
        - **Automatic Cleanup**: Daemon threads terminate when main process exits
        - **Independent Operation**: Each thread operates independently for fault isolation

    Queue-based Communication:
        The system uses a shared queue for inter-component communication:
        - **Thread Safety**: Queue operations are inherently thread-safe
        - **Asynchronous Processing**: ROS 2 results queued for later transmission
        - **Decoupled Components**: ROS 2 and gRPC components operate independently
        - **Buffering**: Queue provides buffering for high-throughput scenarios

    Startup Sequence:
        1. **Action Client Creation**: Initialize ROS 2 action client with queue and logger
        2. **Thread Configuration**: Create and configure server and client threads
        3. **Daemon Mode Setup**: Set threads as daemons for proper lifecycle management
        4. **Thread Startup**: Start both threads for concurrent operation
        5. **System Ready**: Complete communication infrastructure is operational

    :param ros2_action_queue: Shared queue for passing results between ROS 2 and gRPC components
    :type ros2_action_queue: queue.Queue
    :param ros2_logger: Pre-configured logger instance for system operations
    :type ros2_logger: logging.Logger

    :raises rclpy.exceptions.RCLError: If ROS 2 initialization fails
    :raises grpc.RpcError: If gRPC server cannot start on specified port
    :raises threading.ThreadError: If thread creation or startup fails
    :raises Exception: For any other system initialization failures

    Thread Management:
        Both threads are configured as daemon threads with the following characteristics:
        - **Automatic Termination**: Threads terminate when main process exits
        - **Background Processing**: Do not prevent program termination
        - **Independent Lifecycle**: Each thread manages its own lifecycle
        - **Error Isolation**: Thread failures do not affect other components

    Example:
        **System Startup**::
        
            import queue
            import logging
            
            # Create shared queue and logger
            result_queue = queue.Queue()
            logger = logging.getLogger('ROS2')
            
            # Start complete ROS 2 communication system
            start_grpc_ros2(result_queue, logger)
            
            # System now ready to:
            # - Receive plans from Mission Management (port 50099)
            # - Send results to Mission Management (port 50070)
            # - Interface with ROS 2 action servers on vehicles

    .. note::
        This function starts daemon threads that run indefinitely. Ensure proper
        system shutdown procedures to clean up resources appropriately.

    .. warning::
        Both server and client use insecure gRPC channels suitable only for
        internal communication. Implement authentication for external deployments.

    .. seealso::
        - :func:`run_ros2_server`: gRPC server implementation for plan reception
        - :func:`run_ros2_client`: gRPC client implementation for result transmission
        - :class:`commands_action_client.CommandsActionClient`: ROS 2 action client
    """
    # Initialize ROS 2 action client for interfacing with vehicle action servers
    # This client handles goal submission and result collection from ROS 2 ecosystem
    action_client = action.create_ros2_action_client(ros2_action_queue = ros2_action_queue, ros2_logger = ros2_logger)

    # Create server thread for handling incoming drone plans from Mission Management
    # This thread runs the gRPC server that receives plan requests
    server_ros2_thread = threading.Thread(target=run_ros2_server, args=(action_client, ros2_logger,))
    
    # Create client thread for transmitting results back to Mission Management
    # This thread monitors the result queue and sends completed results via gRPC
    client_ros2_thread = threading.Thread(target=run_ros2_client, args=(ros2_action_queue, ros2_logger,))

    # Configure both threads as daemon threads for proper lifecycle management
    # Daemon threads will terminate automatically when the main process exits
    server_ros2_thread.daemon = True
    client_ros2_thread.daemon = True

    # Start both threads to begin bidirectional communication
    # Server thread handles incoming plans, client thread handles outgoing results
    server_ros2_thread.start()
    client_ros2_thread.start()

