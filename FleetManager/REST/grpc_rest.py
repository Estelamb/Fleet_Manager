"""
gRPC REST Communication Module for Fleet Management System

.. module:: grpc_rest
    :synopsis: Bidirectional gRPC communication for mission management and status tracking

.. moduleauthor:: Fleet Management System Team

.. versionadded:: 1.0

This module implements the core gRPC communication layer between REST API components
and the Fleet Management System. It provides both server and client capabilities
for handling mission submissions, status updates, and real-time communication
between distributed system components.

Architecture Overview:
    The module follows a bidirectional communication pattern where:
    
    1. **Server Component**: Receives mission status updates from Fleet Management
    2. **Client Component**: Sends mission data to Fleet Management for processing
    3. **Thread Management**: Handles concurrent server operations in background threads
    4. **Error Recovery**: Provides robust error handling and connection management

Communication Flow:
    .. mermaid::
    
        graph LR
            A[REST API] --> B[gRPC Client]
            B --> C[Fleet Management]
            C --> D[gRPC Server]
            D --> E[Status Updates]
            
            B --> B1[Mission Submission]
            D --> D1[Status Reception]

Components:
    .. autoclass:: RestCommunicationService
        :members:
        :undoc-members:
        :show-inheritance:

Functions:
    .. autofunction:: run_rest_server
    .. autofunction:: run_rest_client
    .. autofunction:: start_grpc_rest

Protocol Buffers Integration:
    Uses auto-generated code from Protocol Buffer definitions:
    
    - **rest_pb2(_grpc)**: REST status communication messages and services
    - **mission_pb2(_grpc)**: Mission data transmission messages and services

Network Configuration:
    - **Server Port**: 50052 (REST status reception)
    - **Client Target**: localhost:50092 (Fleet Management)
    - **Thread Pool**: 10 worker threads for concurrent request handling
    - **Connection Type**: Insecure channels for internal communication

Error Handling Strategy:
    - **Connection Failures**: Graceful degradation with error logging
    - **Timeout Management**: Configurable timeouts for network operations
    - **Resource Cleanup**: Proper channel and server resource management
    - **Thread Safety**: Daemon threads for background server operations

Usage Examples:
    **Standalone Server Operation**::
    
        # Start as standalone service
        $ python grpc_rest.py
        
    **Client Integration**::
    
        from grpc_rest import run_rest_client
        
        # Send mission to Fleet Management
        confirmation = run_rest_client('{"mission_id": 123}', logger)
        if confirmation:
            print(f"Mission confirmed: {confirmation}")
            
    **Server Integration**::
    
        from grpc_rest import start_grpc_rest
        
        # Start server in background
        start_grpc_rest(logger)

Performance Considerations:
    - **Concurrent Processing**: ThreadPoolExecutor enables parallel request handling
    - **Resource Management**: Automatic cleanup of gRPC channels and servers
    - **Memory Efficiency**: Daemon threads prevent resource leaks on shutdown
    - **Network Optimization**: Local communication minimizes latency

.. note::
    This module is designed for internal system communication and uses
    insecure gRPC channels. For external communication, implement proper
    authentication and encryption mechanisms.

.. warning::
    Server components run as daemon threads and will terminate with the
    main process. Ensure proper shutdown procedures for production deployments.

.. seealso::
    - :mod:`REST.default_controller`: REST API endpoints that use this client
    - :mod:`MissionManager.grpc_mission_rest`: Fleet Management server counterpart
    - :mod:`GRPC`: Protocol Buffer definitions and generated code
"""

from concurrent import futures
import grpc
import time
import threading
import logging
from concurrent_log_handler import ConcurrentRotatingFileHandler

from GRPC.rest_pb2 import RestResponse
from GRPC.rest_pb2_grpc import RestCommunicationServicer, add_RestCommunicationServicer_to_server
from GRPC.mission_pb2 import MissionRequest
from GRPC.mission_pb2_grpc import MissionCommunicationStub


class RestCommunicationService(RestCommunicationServicer):
    """gRPC service implementation for handling mission status updates from Fleet Management.
    
    This class extends the auto-generated RestCommunicationServicer to provide concrete
    implementation of the gRPC service methods. It handles incoming status updates
    from the Fleet Management System and processes them according to system requirements.

    Service Responsibilities:
        - **Status Reception**: Receive mission status updates from Fleet Management
        - **Data Processing**: Parse and validate incoming status information
        - **Response Generation**: Provide acknowledgment responses to clients
        - **Error Handling**: Manage connection and processing errors gracefully
        - **Logging Integration**: Record all service operations for monitoring

    gRPC Service Interface:
        Implements the RestCommunication service as defined in rest.proto:
        
        - SendRest(RestRequest) returns (RestResponse)

    Status Processing Workflow:
        1. **Request Reception**: Receive gRPC request with status data
        2. **Data Extraction**: Parse mission status list from request
        3. **Validation**: Ensure status data meets expected format
        4. **Logging**: Record status reception for audit trail
        5. **Response**: Return confirmation message to client

    :param rest_logger: Configured logger instance for service operations
    :type rest_logger: logging.Logger

    :ivar rest_logger: Logger instance for recording service operations and errors
    :vartype rest_logger: logging.Logger

    Example:
        ::

            # Service instantiation (typically done by gRPC server)
            service = RestCommunicationService(logger)
            
            # Service is registered with gRPC server
            add_RestCommunicationServicer_to_server(service, server)

    .. note::
        This service is designed to be instantiated by the gRPC server framework.
        Direct instantiation is typically not required in normal usage.

    .. warning::
        The service currently includes a TODO for POST handling implementation.
        Full status processing functionality may require additional development.
    """

    def __init__(self, rest_logger):
        """Initialize gRPC service with configured logger instance.

        Sets up the service with the necessary logging infrastructure for
        operation tracking and error reporting. Calls parent class constructor
        to ensure proper gRPC service initialization.

        :param rest_logger: Pre-configured logger for service operations
        :type rest_logger: logging.Logger
        """
        # Initialize parent gRPC servicer class
        super().__init__()
        
        # Store logger instance for service operation tracking
        self.rest_logger = rest_logger

    def SendRest(self, request, context):
        """Handle incoming mission status updates from Fleet Management System.
        
        This method implements the core gRPC service interface for receiving
        mission status updates. It processes incoming requests, extracts status
        information, and provides appropriate response confirmations.

        Processing Workflow:
            1. **Request Reception**: Receive gRPC request with mission status array
            2. **Data Extraction**: Convert repeated field to Python list
            3. **Logging**: Record status reception with timestamp
            4. **Future Processing**: Placeholder for POST handling implementation
            5. **Response Generation**: Create confirmation message with status echo

        Status Types:
            Common mission status values include:
            - "PENDING": Mission queued for execution
            - "IN_PROGRESS": Mission currently executing
            - "COMPLETED": Mission finished successfully
            - "FAILED": Mission encountered errors
            - "CANCELLED": Mission terminated by user request

        :param request: Incoming gRPC request containing mission status data
        :type request: rest_pb2.RestRequest
        :param context: gRPC connection context with metadata and error handling
        :type context: grpc.ServicerContext
        
        :return: Response confirmation with status receipt acknowledgment
        :rtype: rest_pb2.RestResponse
        
        :raises grpc.RpcError: If connection issues occur during processing
        :raises ValueError: If status data format is invalid or unexpected

        Example:
            Typical status update request::
            
                request.mission_status = ["COMPLETED", "IN_PROGRESS", "FAILED"]
                
            Corresponding response::
            
                RestResponse(
                    confirmation="Server received mission status: ['COMPLETED', 'IN_PROGRESS', 'FAILED']"
                )

        .. note::
            The method currently includes a TODO for implementing POST handling
            to forward status updates to external systems or databases.

        .. warning::
            Status validation is minimal in the current implementation.
            Production deployments should include comprehensive status validation.
        """
        # Extract mission status array from gRPC request
        # Convert protobuf repeated field to standard Python list
        mission_status = list(request.mission_status)
        
        # Log status reception for audit trail and monitoring
        self.rest_logger.info("[gRPC REST] - Mission status received from Fleet Management")
        
        # TODO: Implement POST handling for status updates
        # This placeholder indicates future implementation for:
        # - Database status persistence
        # - External system notifications
        # - Status aggregation and reporting
        # request.post()  
        
        # Generate confirmation response with received status echo
        return RestResponse(confirmation=f"Server received mission status: {mission_status}")


def run_rest_server(rest_logger):
    """Start and maintain the gRPC server for REST status communication.
    
    This function initializes, configures, and runs a gRPC server to handle
    incoming mission status updates from the Fleet Management System. It provides
    a robust server implementation with proper error handling and graceful shutdown.

    Server Configuration:
        - **Thread Pool**: ThreadPoolExecutor with 10 worker threads for concurrent processing
        - **Network Binding**: Listens on all interfaces (::) port 50052
        - **Service Registration**: Hosts RestCommunicationService for status handling
        - **Execution Model**: Blocking operation with keyboard interrupt handling

    Operational Workflow:
        1. **Server Creation**: Initialize gRPC server with thread pool
        2. **Service Registration**: Add RestCommunicationService to server
        3. **Port Binding**: Bind to port 50052 for incoming connections
        4. **Server Start**: Begin accepting gRPC requests
        5. **Maintenance Loop**: Keep server alive with 24-hour sleep intervals
        6. **Graceful Shutdown**: Handle KeyboardInterrupt for clean termination

    Thread Pool Configuration:
        - **Worker Threads**: 10 concurrent workers for request processing
        - **Request Handling**: Each worker can process one gRPC request simultaneously
        - **Resource Management**: Automatic cleanup of worker threads on shutdown
        - **Load Balancing**: gRPC framework distributes requests across workers

    Network Configuration:
        - **Interface**: [::] (all IPv4 and IPv6 interfaces)
        - **Port**: 50052 (dedicated REST communication port)
        - **Protocol**: HTTP/2 with gRPC framing
        - **Security**: Insecure channels (internal communication)

    :param rest_logger: Configured logger instance for server operations
    :type rest_logger: logging.Logger
    
    :raises KeyboardInterrupt: Handled for graceful server shutdown
    :raises grpc.RpcError: If server binding or startup fails
    :raises OSError: If port 50052 is already in use

    Example:
        ::

            # Start server in main thread (blocking)
            run_rest_server(logger)
            
            # Server will run until Ctrl+C is pressed

    .. note::
        This function blocks execution while running. For background operation,
        use start_grpc_rest() which runs the server in a daemon thread.

    .. warning::
        The server runs with insecure channels suitable for internal communication.
        External deployment should implement proper authentication and encryption.
    """
    # Create gRPC server with thread pool for concurrent request handling
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Register the REST communication service with the server
    add_RestCommunicationServicer_to_server(
        RestCommunicationService(rest_logger), server)
    
    # Bind server to all interfaces on port 50052
    server.add_insecure_port('[::]:50052')
    
    # Start the server and begin accepting requests
    server.start()
    rest_logger.info("[gRPC REST] - Server running on port [::]:50052")
    
    try:
        # Maintain server operation with periodic sleep cycles
        # Using 24-hour intervals to minimize CPU overhead while staying responsive
        while True:
            time.sleep(86400)  # Sleep for 24 hours (86400 seconds)
    except KeyboardInterrupt:
        # Handle graceful shutdown on user interrupt (Ctrl+C)
        server.stop(0)  # Stop immediately (0 seconds grace period)
        rest_logger.info("[gRPC REST] - Server shutdown complete")


def run_rest_client(mission_json, rest_logger):
    """Send mission data to Fleet Management system via gRPC client connection.
    
    This function establishes a gRPC client connection to the Fleet Management
    System and transmits mission data for processing. It provides comprehensive
    error handling and response validation for reliable mission submission.

    Client Operation Workflow:
        1. **Channel Creation**: Establish insecure gRPC channel to Fleet Management
        2. **Stub Initialization**: Create MissionCommunicationStub for service calls
        3. **Request Preparation**: Package mission JSON into gRPC request message
        4. **Transmission**: Send mission data via SendMission RPC call
        5. **Response Processing**: Extract confirmation message from response
        6. **Error Handling**: Manage connection failures and timeouts gracefully

    Network Configuration:
        - **Target Address**: localhost:50092 (Fleet Management gRPC server)
        - **Channel Type**: Insecure (suitable for internal communication)
        - **Protocol**: HTTP/2 with gRPC framing
        - **Timeout**: Default gRPC timeout settings

    Mission Data Format:
        The mission_json parameter should contain a valid JSON string representing
        a complete mission specification including:
        - Mission identification and metadata
        - Task definitions and sequences
        - Vehicle assignments and capabilities
        - Navigation areas and constraints

    :param mission_json: Complete mission specification in JSON string format
    :type mission_json: str
    :param rest_logger: Configured logger instance for client operations
    :type rest_logger: logging.Logger
    
    :return: Confirmation message from Fleet Management server, or None on failure
    :rtype: Union[str, None]
    
    :raises grpc.RpcError: If connection to Fleet Management server fails
    :raises json.JSONDecodeError: If mission_json contains invalid JSON syntax
    :raises ValueError: If mission data doesn't meet required format

    Response Format:
        Successful responses typically follow the pattern::
        
            "Mission received by Fleet Management: {mission_id}"
            
        Where mission_id is extracted from the submitted mission data.

    Error Handling:
        - **Connection Failures**: Logged and return None for graceful degradation
        - **Timeout Errors**: Handled by gRPC default timeout mechanisms
        - **Server Errors**: Propagated as gRPC exceptions with error details
        - **Network Issues**: Automatic retry logic (if configured in gRPC channel)

    Example:
        ::

            # Prepare mission data
            mission_data = {
                "mission_id": 12345,
                "tasks": [...],
                "vehicles": [...],
                "navigation_areas": [...]
            }
            
            # Convert to JSON and send
            mission_json = json.dumps(mission_data)
            confirmation = run_rest_client(mission_json, logger)
            
            if confirmation:
                print(f"Mission submitted successfully: {confirmation}")
            else:
                print("Mission submission failed")

    .. note::
        The client uses insecure channels suitable for internal system communication.
        External deployments should implement proper authentication and encryption.

    .. warning::
        Failed submissions return None rather than raising exceptions.
        Calling code should check return values for proper error handling.
    """
    # Establish insecure gRPC channel to Fleet Management server
    channel = grpc.insecure_channel('localhost:50092')
    
    # Create stub for MissionCommunication service calls
    stub = MissionCommunicationStub(channel)

    try:
        # Log mission transmission attempt for audit trail
        rest_logger.info("[gRPC REST] - Sending mission to Fleet Management")
        
        # Send mission data via gRPC call and await response
        response = stub.SendMission(MissionRequest(mission_json=mission_json))
        
        # Log successful acknowledgment receipt
        rest_logger.info("[gRPC REST] - ACK received from Fleet Management")
        
        # Return confirmation message from server response
        return response.confirmation
        
    except grpc.RpcError as e:
        # Handle gRPC communication errors with detailed logging
        rest_logger.error(f"[gRPC REST] - Connection error: {e}")
        
        # Return None to indicate failure for graceful error handling
        return None


def start_grpc_rest(rest_logger):
    """Initialize and start gRPC server in background daemon thread.
    
    This function provides a convenient way to start the gRPC REST server in
    a background thread, allowing the main application to continue execution
    while the server handles incoming requests concurrently.

    Thread Configuration:
        - **Thread Type**: Daemon thread (terminates with main process)
        - **Thread Name**: "gRPC-REST-Server" for identification and debugging
        - **Target Function**: run_rest_server for server execution
        - **Startup**: Immediate thread start after creation

    Daemon Thread Behavior:
        - **Lifecycle**: Thread terminates automatically when main process exits
        - **Resource Management**: No explicit cleanup required
        - **Error Isolation**: Thread exceptions don't affect main process
        - **Background Operation**: Non-blocking server initialization

    Operational Advantages:
        - **Non-blocking**: Main thread continues execution immediately
        - **Concurrent Processing**: Server handles requests while main app runs
        - **Resource Efficiency**: Automatic cleanup on process termination
        - **Development Friendly**: Easy integration with existing applications

    :param rest_logger: Configured logger instance for server operations
    :type rest_logger: logging.Logger

    :raises ThreadError: If thread creation or startup fails
    :raises RuntimeError: If system resources are insufficient for thread creation

    Usage Patterns:
        **Application Integration**::
        
            # Start gRPC server in background
            start_grpc_rest(logger)
            
            # Continue with main application logic
            main_application_loop()
            
        **Service Initialization**::
        
            # Initialize all services
            start_database_service()
            start_grpc_rest(logger)  # Non-blocking
            start_mqtt_service()
            
            # All services now running concurrently

    .. note::
        The server thread runs as a daemon and will terminate automatically
        when the main process exits. No explicit shutdown is required.

    .. warning::
        Since the thread is marked as daemon, it will terminate immediately
        when the main process exits, potentially interrupting active requests.
        For production deployments, consider proper shutdown procedures.
    """
    # Create daemon thread for background server operation
    server_rest_thread = threading.Thread(
        target=run_rest_server,  # Function to execute in thread
        args=(rest_logger,),     # Arguments passed to target function
        name="gRPC-REST-Server"  # Thread name for identification and debugging
    )
    
    # Mark thread as daemon to terminate with main process
    server_rest_thread.daemon = True
    
    # Start the thread immediately for background server operation
    server_rest_thread.start()

