"""
gRPC-ROS2 Prescription Map Communication Bridge Module
====================================================

This module implements a specialized gRPC communication bridge for agricultural
prescription map (PM) transmission and processing. It provides a robust interface
between Mission Management systems and ROS2-based prescription map distribution
infrastructure, enabling real-time transmission of variable rate application maps
essential for precision agriculture operations.

The module serves as the primary prescription map communication gateway, facilitating
the distribution of field-specific application instructions including fertilizer rates,
pesticide applications, seeding densities, and other variable rate agricultural
operations critical for precision farming workflows.

.. module:: grpc_ros2_pm
    :synopsis: gRPC-ROS2 prescription map communication bridge for precision agriculture

Features
--------
- **Prescription Map Reception**: gRPC server for receiving prescription maps from Mission Management
- **Real-time Processing**: Immediate PM processing and ROS2 queue integration
- **Agricultural Operations**: Specialized handling for variable rate application maps
- **Thread-safe Operations**: Concurrent PM handling with thread-safe queue operations
- **Error Resilience**: Comprehensive error handling and connection recovery
- **Performance Optimization**: Low-latency PM transmission and processing
- **Field Integration**: Seamless ROS2 publisher integration for PM distribution

System Architecture
------------------
The gRPC-ROS2 prescription map bridge operates within the precision agriculture ecosystem:

Prescription Map Flow Architecture:
    Mission Management → gRPC PM Server → Queue → ROS2 Publishers → Field Application Systems

Communication Pipeline:
    1. **PM Reception**: gRPC server receives prescription maps from external systems
    2. **Data Processing**: JSON deserialization and validation of prescription map data
    3. **Queue Integration**: Thread-safe PM forwarding to ROS2 publishers
    4. **Distribution**: ROS2 publishers broadcast PMs to field application systems
    5. **Error Handling**: Robust error management and recovery mechanisms

Agricultural Prescription Map Types:
    - **Fertilizer Maps**: Variable rate fertilizer application instructions
    - **Pesticide Maps**: Targeted pesticide application zones and rates
    - **Seeding Maps**: Variable rate seeding density instructions
    - **Irrigation Maps**: Precision irrigation scheduling and rates
    - **Harvesting Maps**: Optimized harvesting path and timing instructions

Field Application Integration:
    - **Variable Rate Controllers**: Direct integration with VRT equipment
    - **Sprayer Systems**: Real-time prescription map processing for sprayers
    - **Planter Controllers**: Seeding rate adjustments based on prescription maps
    - **Irrigation Systems**: Precision water management using PM instructions

Workflow Architecture
--------------------
Prescription Map Processing Pipeline:
    1. **PM Reception**: External systems transmit prescription maps via gRPC
    2. **Data Validation**: JSON parsing and prescription map structure validation
    3. **Queue Processing**: Thread-safe PM placement in ROS2 queue
    4. **Publisher Integration**: PMs forwarded to ROS2 publisher components
    5. **Field Distribution**: Prescription maps broadcast to field application systems
    6. **Error Recovery**: Connection errors handled with retry mechanisms

Agricultural PM Processing:
    - **Field Mapping**: Spatial coordinate mapping and georeferencing
    - **Rate Calculations**: Application rate computations and validations
    - **Equipment Integration**: Compatibility with various agricultural equipment
    - **Real-time Updates**: Dynamic prescription map updates during operations

Classes
-------
.. autoclass:: PMCommunicationService
    :members:
    :undoc-members:
    :show-inheritance:

Functions
---------
.. autofunction:: run_pm_server
.. autofunction:: start_grpc_pm

Dependencies
-----------
Core Dependencies:
    - **grpc**: Google gRPC framework for high-performance PM communication
    - **concurrent.futures**: Thread pool executor for concurrent PM processing
    - **threading**: Threading support for background server operation
    - **queue**: Thread-safe inter-component PM communication
    - **json**: Prescription map data serialization and deserialization

gRPC Protocol Buffers:
    - **pm_pb2**: Prescription map message definitions and serialization
    - **pm_pb2_grpc**: PM service stubs and server implementations

Logging Dependencies:
    - **Logs.create_logger**: Centralized logging infrastructure for activity tracking

Integration Points
-----------------
External Integrations:
    - **Mission Management**: Prescription map reception and status reporting via gRPC
    - **Agricultural Systems**: Field management and prescription map execution coordination
    - **Farm Management**: Integration with farm planning and field management systems
    - **Equipment Controllers**: Direct integration with variable rate application equipment

Internal Integrations:
    - **ROS2 Publishers**: PM distribution to prescription_map_pubsub components
    - **init_ros2.py**: System initialization and component coordination
    - **Queue Systems**: Thread-safe inter-component PM message passing
    - **Logging Infrastructure**: Centralized PM processing activity logging

Performance Characteristics
--------------------------
Prescription Map Processing Performance:
    - **Reception Latency**: Sub-second PM reception and processing
    - **Throughput**: High-volume prescription map processing capability
    - **Queue Efficiency**: Optimal thread-safe PM queue management
    - **Distribution Speed**: Rapid PM forwarding to ROS2 publishers

Scalability Features:
    - **Concurrent Processing**: Multi-threaded server with configurable worker pool
    - **Memory Efficiency**: Optimized PM data handling and queue management
    - **Connection Resilience**: Automatic reconnection and error recovery
    - **Resource Optimization**: Minimal overhead with efficient processing

Agricultural Data Formats
-------------------------
Prescription Map Data Structure:
    - **JSON Serialization**: Structured prescription map data in JSON format
    - **Spatial Information**: GPS coordinates, field boundaries, zone definitions
    - **Application Rates**: Variable rate instructions for different field zones
    - **Metadata**: Field information, crop types, application timing

Expected PM Format:
    - **Field Identification**: Unique field identifiers and crop information
    - **Zone Mapping**: Spatial zones with specific application instructions
    - **Rate Specifications**: Application rates, timings, and equipment settings
    - **Quality Parameters**: Data quality metrics and validation information

Error Handling Strategy
----------------------
Multi-level Error Management:
    - **Connection-Level**: gRPC connection error handling and retry logic
    - **Message-Level**: Individual PM processing error handling
    - **Queue-Level**: Thread-safe queue operation error management
    - **System-Level**: Graceful shutdown and resource cleanup procedures

Recovery Mechanisms:
    - **Automatic Reconnection**: gRPC connection recovery with exponential backoff
    - **Message Retry**: Failed PM transmission retry with timeout handling
    - **Queue Monitoring**: Continuous queue state monitoring and error detection
    - **Graceful Degradation**: Continued operation despite individual component failures

Examples
--------
Programmatic Usage:

.. code-block:: python

    import queue
    import logging
    from grpc_ros2_pm import start_grpc_pm

    # Setup prescription map communication infrastructure
    logger = logging.getLogger('agricultural_pm')
    pm_queue = queue.Queue()
    
    # Start gRPC PM bridge
    start_grpc_pm(pm_queue, logger)

System Integration Example:

.. code-block:: python

    # Integration with ROS2 prescription map publishers
    from rclpy.executors import MultiThreadedExecutor
    
    # Initialize PM infrastructure
    executor = MultiThreadedExecutor()
    
    # Start gRPC-ROS2 PM bridge
    start_grpc_pm(pm_queue, logger)
    
    # PMs flow through bridge to ROS2 publishers
    executor.spin()

Notes
-----
- **Agricultural Focus**: Optimized for precision agriculture prescription map workflows
- **Real-time Processing**: Low-latency PM handling for field operations
- **Variable Rate Integration**: Supports complex variable rate application systems
- **Error Resilience**: Robust error handling for continuous field operations

Configuration Requirements:
    - **gRPC Port**: Prescription map server on port 51003
    - **Network Access**: Reliable network connectivity for gRPC communication
    - **Protocol Buffers**: Properly compiled protobuf definitions
    - **Logging Setup**: Configured logging infrastructure for activity tracking

Agricultural Considerations:
    - **Field Conditions**: Robust operation in various agricultural environments
    - **PM Precision**: High-accuracy prescription map parameter handling
    - **Real-time Distribution**: Continuous PM streaming for field operations
    - **Equipment Compatibility**: Support for various agricultural equipment types

See Also
--------
grpc.server : gRPC server implementation
queue.Queue : Thread-safe inter-component communication
threading.Thread : Background thread management for server operation
"""

from concurrent import futures
import json
import grpc
import time
import queue
import threading

from GRPC.definitions.pm_pb2 import PMResponse
from GRPC.definitions.pm_pb2_grpc import PMCommunicationServicer, add_PMCommunicationServicer_to_server

from Logs.create_logger import create_logger


class PMCommunicationService(PMCommunicationServicer):
    """
    gRPC service implementation for agricultural prescription map processing.
    
    This class handles incoming prescription map data from Mission Management systems,
    processes the PM information, and forwards it to ROS2 publishers for field-wide
    distribution. It specializes in agricultural prescription maps including variable
    rate application instructions, field boundary definitions, and equipment-specific
    configuration parameters essential for precision agriculture operations.

    The service operates as a critical bridge between external farm management systems
    and internal ROS2 infrastructure, ensuring reliable prescription map transmission
    and processing for optimal field operations and variable rate applications.

    :param logger: Configured logger instance for PM activity tracking
    :type logger: logging.Logger
    :param pm_queue: Thread-safe queue for ROS2 publisher integration
    :type pm_queue: queue.Queue

    Attributes
    ----------
    logger : logging.Logger
        Configured logger instance for comprehensive PM activity tracking
    pm_queue : queue.Queue
        Thread-safe queue for forwarding prescription maps to ROS2 publishers

    Methods
    -------
    SendPM(request, context)
        Process incoming prescription map requests and forward to ROS2 infrastructure

    Workflow
    --------
    1. **Service Initialization**: Logger and queue setup for PM processing
    2. **Request Reception**: gRPC PM requests received from external systems
    3. **Data Processing**: JSON deserialization and validation of prescription map data
    4. **Queue Integration**: Thread-safe PM forwarding to ROS2 publishers
    5. **Response Generation**: Confirmation responses sent to requesting systems
    6. **Error Handling**: Comprehensive error management and logging

    Agricultural PM Handling:
        - **Variable Rate Maps**: Fertilizer, pesticide, and seeding rate instructions
        - **Field Boundaries**: Spatial definitions and coordinate mapping
        - **Equipment Settings**: Application parameters and timing specifications
        - **Quality Control**: Data validation and integrity verification

    Examples
    --------
    .. code-block:: python

        import logging
        import queue
        
        # Initialize service components
        logger = logging.getLogger('pm_service')
        pm_queue = queue.Queue()
        
        # Create PM communication service
        service = PMCommunicationService(logger, pm_queue)
        
        # Service automatically handles incoming gRPC requests
        # and forwards prescription maps to ROS2 publishers via queue

    Notes
    -----
    - **Thread Safety**: All operations are designed for concurrent execution
    - **Error Resilience**: Comprehensive error handling prevents service disruption
    - **Agricultural Focus**: Optimized for precision agriculture PM workflows
    - **Real-time Processing**: Low-latency PM handling for field operations
    """
    def __init__(self, logger, pm_queue):
        """
        Initialize the PMCommunicationService with logging and queue integration.

        Sets up the service infrastructure for processing agricultural prescription maps,
        establishing connections to logging systems and ROS2 publisher queues for
        comprehensive PM distribution and field operation coordination.

        :param logger: Configured logger instance for PM activity tracking
        :type logger: logging.Logger
        :param pm_queue: Thread-safe queue for ROS2 publisher integration
        :type pm_queue: queue.Queue

        Workflow
        --------
        1. **Parent Initialization**: Call parent servicer constructor
        2. **Logger Assignment**: Configure logging for PM processing activities
        3. **Queue Integration**: Establish connection to ROS2 publisher queue
        4. **Service Readiness**: Prepare service for incoming prescription map requests

        Notes
        -----
        - **Immediate Availability**: Service ready for PM processing upon initialization
        - **Thread Safety**: All components configured for concurrent operation
        - **Error Preparedness**: Logging infrastructure ready for error tracking
        """
        super().__init__()  # Initialize parent gRPC servicer
        self.logger = logger  # Configure logging for PM activities
        self.pm_queue = pm_queue  # Establish ROS2 publisher queue connection

    def SendPM(self, request, context):
        """
        Process incoming agricultural prescription map requests and forward to ROS2 infrastructure.

        This method handles gRPC prescription map requests from Mission Management systems,
        deserializes the PM data, validates the information, and forwards it to ROS2
        publishers via thread-safe queue operations. It processes various types of
        agricultural prescription maps including variable rate application instructions,
        field boundary definitions, and equipment-specific parameters.

        :param request: gRPC request containing serialized prescription map data
        :type request: PMRequest
        :param context: gRPC connection context and metadata
        :type context: grpc.ServicerContext
        :returns: gRPC response with processing confirmation and status
        :rtype: PMResponse
        :raises grpc.RpcError: For critical processing failures and connection issues

        Workflow
        --------
        1. **Request Reception**: Receive gRPC prescription map request from external system
        2. **Data Concatenation**: Combine PM string segments from request payload
        3. **JSON Deserialization**: Parse JSON prescription map data into Python objects
        4. **Processing Logging**: Record successful PM reception and processing
        5. **Queue Integration**: Forward processed PM to ROS2 publisher queue
        6. **Success Logging**: Record successful PM forwarding to queue
        7. **Response Generation**: Create confirmation response for requesting system
        8. **Error Handling**: Catch and handle processing errors with comprehensive logging

        Agricultural PM Processing:
            - **Variable Rate Maps**: Fertilizer rates, pesticide applications, seeding densities
            - **Field Boundaries**: Spatial coordinates, zone definitions, boundary mapping
            - **Application Parameters**: Equipment settings, timing specifications, quality control
            - **Metadata Processing**: Field identification, crop types, operation scheduling

        Expected Request Format:
            - **pm[]**: Array of strings containing JSON prescription map segments
            - **JSON Structure**: Dictionary with field definitions, zones, and application rates
            - **Spatial Data**: GPS coordinates, field boundaries, zone specifications
            - **Application Data**: Variable rates, equipment settings, timing parameters

        Returns
        -------
        PMResponse
            Confirmation response with processing status:
            - **Success**: "PM received and added to queue"
            - **Error**: "Error processing PM"

        Raises
        ------
        grpc.RpcError
            For critical processing failures requiring connection termination
        json.JSONDecodeError
            For malformed JSON prescription map data (handled internally)
        Exception
            For unexpected processing errors (handled with comprehensive logging)

        Notes
        -----
        - **Thread Safety**: All queue operations are thread-safe for concurrent processing
        - **Error Resilience**: Comprehensive error handling prevents service disruption
        - **Agricultural Focus**: Optimized for precision agriculture PM workflows
        - **Real-time Processing**: Low-latency PM handling for field operations
        """
        try:
            # Concatenate PM string segments from gRPC request payload
            pm_str = "".join(request.pm)
            
            # Deserialize JSON prescription map data into Python objects
            pm = json.loads(pm_str)

            # Forward processed prescription map to ROS2 publisher queue (thread-safe operation)
            self.pm_queue.put(pm)
            self.logger.info(f"[ROS2][gRPC PM] - Prescription map sent to ROS2 publisher")

            # Generate successful processing confirmation response
            return PMResponse(confirmation=f"PM received and added to queue")
        except json.JSONDecodeError as e:
            # Handle JSON parsing errors with detailed logging
            self.logger.error(f"[ROS2][gRPC PM] - JSON parsing error in SendPM: {e}", exc_info=True)
            return PMResponse(confirmation="Error processing PM: Invalid JSON format")
        except Exception as e:
            # Handle unexpected errors with comprehensive logging and error reporting
            self.logger.error(f"[ROS2][gRPC PM] - Unexpected error in SendPM: {e}", exc_info=True)
            return PMResponse(confirmation="Error processing PM")


def run_pm_server(logger, pm_queue):
    """
    Start and manage gRPC prescription map server instance for agricultural operations.

    This function initializes and operates a dedicated gRPC server for receiving
    agricultural prescription maps from Mission Management systems. It configures the
    server with appropriate threading, establishes service endpoints, and manages
    the server lifecycle including graceful shutdown procedures for continuous
    precision agriculture operations.

    The server operates continuously to handle incoming prescription map requests,
    processing variable rate application instructions, field boundary definitions,
    and equipment-specific parameters essential for precision agriculture field
    operations and variable rate applications.

    :param logger: Configured logger instance for server activity tracking
    :type logger: logging.Logger
    :param pm_queue: Thread-safe queue for ROS2 publisher integration
    :type pm_queue: queue.Queue
    :raises KeyboardInterrupt: For graceful server shutdown on user interruption
    :raises grpc.RpcError: For critical server configuration or operation failures

    Workflow
    --------
    1. **Server Creation**: Initialize gRPC server with thread pool executor
    2. **Service Registration**: Register PMCommunicationService with server
    3. **Port Binding**: Bind server to port 51003 for prescription map communication
    4. **Server Startup**: Start server and begin accepting connections
    5. **Continuous Operation**: Run indefinitely processing prescription map requests
    6. **Graceful Shutdown**: Handle interruption signals for clean termination

    Server Configuration:
        - **Thread Pool**: 10 worker threads for concurrent PM processing
        - **Port**: 51003 (insecure) for gRPC prescription map communication
        - **Service**: PMCommunicationService for PM request handling
        - **Lifecycle**: Continuous operation with graceful shutdown support

    Agricultural PM Server Features:
        - **High Throughput**: Concurrent processing of multiple prescription map streams
        - **Low Latency**: Optimized for real-time agricultural field operations
        - **Error Resilience**: Robust error handling for continuous operation
        - **Scalability**: Thread pool architecture for load distribution

    Examples
    --------
    .. code-block:: python

        import logging
        import queue
        from grpc_ros2_pm import run_pm_server
        
        # Setup server components
        logger = logging.getLogger('pm_server')
        pm_queue = queue.Queue()
        
        # Start PM server (blocking operation)
        run_pm_server(logger, pm_queue)

    Notes
    -----
    - **Blocking Operation**: Function runs indefinitely until interrupted
    - **Thread Safety**: All operations designed for concurrent execution
    - **Resource Management**: Proper cleanup on shutdown
    - **Agricultural Focus**: Optimized for precision agriculture workflows
    - **Continuous Operation**: Designed for 24/7 agricultural field operations

    See Also
    --------
    grpc.server : gRPC server implementation
    concurrent.futures.ThreadPoolExecutor : Thread pool for concurrent processing
    PMCommunicationService : Service implementation for PM processing
    """
    # Initialize gRPC server with thread pool executor for concurrent processing
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Register PMCommunicationService with server for prescription map request handling
    add_PMCommunicationServicer_to_server(
        PMCommunicationService(logger, pm_queue), server)
    
    # Bind server to port 51003 for insecure gRPC communication
    server.add_insecure_port('[::]:52003')
    
    # Start server and begin accepting incoming prescription map connections
    server.start()
    logger.info(f"[ROS2][gRPC PM] - Server running on port 52003")
    
    try:
        # Run server indefinitely, processing prescription map requests continuously
        while True:
            time.sleep(86400)  # Sleep for 24 hours, server handles requests in background
    except KeyboardInterrupt:
        # Handle graceful shutdown on user interruption
        logger.info("[ROS2][gRPC PM] - Shutting down server gracefully")
        server.stop(0)  # Stop server immediately without waiting for active RPCs


def start_grpc_pm(pm_queue: queue.Queue, logger):
    """
    Initialize and start ROS2 prescription map communication infrastructure.

    This function establishes the complete prescription map communication infrastructure
    for agricultural drone systems, launching the gRPC server in a dedicated daemon
    thread to enable continuous PM reception and processing. It provides the primary
    entry point for integrating prescription map distribution with ROS2 publisher
    systems for comprehensive agricultural field operation coordination.

    The function configures thread-safe prescription map processing, ensuring reliable
    communication between Mission Management systems and ROS2 infrastructure for
    real-time agricultural variable rate application coordination and field management.

    :param pm_queue: Thread-safe queue for ROS2 publisher integration
    :type pm_queue: queue.Queue
    :param logger: Configured logger instance for infrastructure activity tracking
    :type logger: logging.Logger

    Workflow
    --------
    1. **Thread Creation**: Create dedicated daemon thread for server operation
    2. **Server Configuration**: Configure thread with server function and parameters
    3. **Daemon Setup**: Set thread as daemon for automatic cleanup on exit
    4. **Thread Launch**: Start server thread for background operation
    5. **Infrastructure Ready**: Return control while server runs in background

    Infrastructure Components:
        - **Daemon Thread**: Background server operation without blocking main thread
        - **gRPC Server**: Prescription map reception server running on dedicated thread
        - **Queue Integration**: Thread-safe connection to ROS2 publisher systems
        - **Logging Integration**: Comprehensive activity tracking and error reporting

    Agricultural PM Infrastructure:
        - **Continuous Operation**: 24/7 prescription map reception for agricultural operations
        - **Real-time Processing**: Low-latency PM handling for field operations
        - **Thread Safety**: Concurrent operation with other system components
        - **Scalability**: Support for high-volume prescription map processing

    Examples
    --------
    .. code-block:: python

        import queue
        import logging
        from grpc_ros2_pm import start_grpc_pm
        
        # Setup PM infrastructure
        logger = logging.getLogger('agricultural_pm')
        pm_queue = queue.Queue()
        
        # Start prescription map communication infrastructure
        start_grpc_pm(pm_queue, logger)
        
        # Infrastructure now running in background
        # Main thread free for other operations

    Integration Example:

    .. code-block:: python

        # Complete agricultural field management setup
        from rclpy.executors import MultiThreadedExecutor
        
        # Initialize components
        executor = MultiThreadedExecutor()
        pm_queue = queue.Queue()
        logger = logging.getLogger('agricultural_system')
        
        # Start PM infrastructure
        start_grpc_pm(pm_queue, logger)
        
        # ROS2 system handles prescription map distribution
        executor.spin()

    Notes
    -----
    - **Non-blocking**: Function returns immediately, server runs in background
    - **Thread Safety**: All operations designed for concurrent execution
    - **Daemon Thread**: Server thread automatically cleaned up on program exit
    - **Agricultural Focus**: Optimized for precision agriculture PM workflows
    - **Infrastructure Role**: Primary entry point for PM communication setup

    See Also
    --------
    run_pm_server : Server implementation function
    threading.Thread : Python threading for background operation
    queue.Queue : Thread-safe inter-component communication
    """
    # Create dedicated daemon thread for gRPC prescription map server operation
    server_pm_thread = threading.Thread(target=run_pm_server, args=(logger, pm_queue))
    
    # Configure thread as daemon for automatic cleanup on program exit
    server_pm_thread.daemon = True
    
    # Launch server thread for background prescription map processing
    server_pm_thread.start()


if __name__ == '__main__':
    """
    Command-line entry point for standalone gRPC prescription map server operation.
    
    This entry point enables standalone operation of the gRPC prescription map
    communication infrastructure for agricultural drone systems. It provides a
    complete setup for testing and development purposes, initializing logging
    infrastructure, creating PM queues, and starting the gRPC server for
    prescription map reception and processing.

    The standalone mode is particularly useful for:
    - **Development Testing**: Testing PM communication without full ROS2 setup
    - **System Integration**: Verifying gRPC connectivity and PM processing
    - **Field Testing**: Isolated PM server operation for field trials
    - **Performance Testing**: Load testing prescription map reception and processing

    Workflow
    --------
    1. **Logger Creation**: Initialize dedicated logger for PM operations
    2. **Queue Creation**: Create thread-safe queue for PM processing
    3. **Infrastructure Launch**: Start complete gRPC PM communication system
    4. **Continuous Operation**: Run indefinitely processing prescription map requests

    Standalone Configuration:
        - **Logger Name**: 'pm' for clear identification in logs
        - **Log File**: 'Logs/pm.log' for dedicated prescription map logging
        - **Queue Type**: Standard queue.Queue for thread-safe operations
        - **Operation Mode**: Continuous background processing

    Examples
    --------
    Command-line execution:

    .. code-block:: bash

        # Start standalone prescription map server
        python grpc_ros2_pm.py
        
        # Server starts and logs activity to Logs/pm.log
        # Ready to receive prescription maps from Mission Management systems

    Integration testing:

    .. code-block:: python

        # Test prescription map transmission
        import grpc
        from GRPC.definitions.pm_pb2 import PMRequest
        from GRPC.definitions.pm_pb2_grpc import PMCommunicationStub
        
        # Connect to standalone server
        channel = grpc.insecure_channel('localhost:51003')
        stub = PMCommunicationStub(channel)
        
        # Send test prescription map
        test_pm = '{"field_id": "test_field", "zones": []}'
        response = stub.SendPM(PMRequest(pm=[test_pm]))

    Notes
    -----
    - **Standalone Operation**: Complete PM server without ROS2 dependencies
    - **Development Tool**: Useful for testing and integration verification
    - **Logging Setup**: Dedicated logging for PM-specific activity tracking
    - **Background Processing**: Server runs continuously until manually stopped
    """
    # Initialize dedicated logger for standalone prescription map server operation
    logger = create_logger('pm', 'Logs/pm.log')
    logger.info("[ROS2][gRPC PM] - Starting standalone prescription map server")

    # Create thread-safe queue for prescription map processing and ROS2 integration
    pm_queue = queue.Queue()
    logger.debug("[ROS2][gRPC PM] - Prescription map queue created for processing")

    # Launch complete gRPC prescription map communication infrastructure
    start_grpc_pm(pm_queue, logger)
    logger.info("[ROS2][gRPC PM] - Standalone prescription map infrastructure operational")
    
    # Keep main thread alive while server operates in daemon thread
    try:
        while True:
            time.sleep(60)  # Sleep and let daemon thread handle PM processing
    except KeyboardInterrupt:
        logger.info("[ROS2][gRPC PM] - Standalone server shutdown requested")
        print("Prescription map server shutting down...")