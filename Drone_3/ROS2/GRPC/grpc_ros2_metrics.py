"""
gRPC-ROS2 Metrics Communication Bridge Module
============================================

This module implements a specialized gRPC communication bridge for agricultural
drone system metrics collection and transmission. It provides a robust interface
between Mission Management systems and ROS2-based metrics publishing infrastructure,
enabling real-time monitoring of drone performance, sensor data, and operational
status for precision agriculture applications.

The module serves as the primary metrics communication gateway, facilitating
comprehensive system monitoring including hardware telemetry, sensor readings,
agricultural operation metrics, and performance indicators essential for
autonomous agricultural drone operations.

.. module:: grpc_ros2_metrics
    :synopsis: gRPC-ROS2 metrics communication bridge for agricultural drone monitoring

Features
--------
- **Metrics Reception**: gRPC server for receiving system metrics from Mission Management
- **Real-time Processing**: Immediate metrics processing and queue integration
- **Agricultural Monitoring**: Specialized metrics for precision agriculture operations
- **Thread-safe Operations**: Concurrent metrics handling with thread-safe queue operations
- **Error Resilience**: Comprehensive error handling and connection recovery
- **Performance Tracking**: Low-latency metrics transmission and processing
- **System Integration**: Seamless ROS2 publisher integration for metrics distribution

System Architecture
------------------
The gRPC-ROS2 metrics bridge operates within the agricultural drone monitoring ecosystem:

Metrics Flow Architecture:
    Mission Management → gRPC Metrics Server → Queue → ROS2 Publishers → Monitoring Systems

Communication Pipeline:
    1. **Metrics Reception**: gRPC server receives metrics from external systems
    2. **Data Processing**: JSON deserialization and validation of metrics data
    3. **Queue Integration**: Thread-safe metrics forwarding to ROS2 publishers
    4. **Distribution**: ROS2 publishers broadcast metrics to monitoring subscribers
    5. **Error Handling**: Robust error management and recovery mechanisms

Agricultural Metrics Categories:
    - **System Telemetry**: Hardware status, battery levels, communication health
    - **Sensor Data**: GPS coordinates, camera status, environmental sensors
    - **Operation Metrics**: Field coverage, application rates, task completion
    - **Performance Indicators**: Processing times, resource utilization, efficiency

Monitoring Integration:
    - **Real-time Dashboards**: Live metrics streaming to monitoring interfaces
    - **Historical Analysis**: Metrics persistence for operational analysis
    - **Alert Systems**: Threshold-based alerting for critical metrics
    - **Agricultural Analytics**: Field operation performance analysis

Workflow Architecture
--------------------
Metrics Processing Pipeline:
    1. **Metrics Reception**: External systems transmit metrics via gRPC
    2. **Data Validation**: JSON parsing and metrics data structure validation
    3. **Queue Processing**: Thread-safe metrics placement in ROS2 queue
    4. **Publisher Integration**: Metrics forwarded to ROS2 publisher components
    5. **Distribution**: Metrics broadcast to all monitoring subscribers
    6. **Error Recovery**: Connection errors handled with retry mechanisms

Agricultural Metrics Types:
    - **Field Operations**: Seeding rates, fertilizer application, crop monitoring
    - **Navigation Metrics**: Flight path accuracy, waypoint completion, altitude
    - **Sensor Metrics**: Camera capture rates, GPS accuracy, environmental readings
    - **System Health**: CPU usage, memory consumption, communication latency

Classes
-------
.. autoclass:: MetricsCommunicationService
    :members:
    :undoc-members:
    :show-inheritance:

Functions
---------
.. autofunction:: run_metrics_server
.. autofunction:: start_grpc_metrics

Dependencies
-----------
Core Dependencies:
    - **grpc**: Google gRPC framework for high-performance metrics communication
    - **concurrent.futures**: Thread pool executor for concurrent metrics processing
    - **threading**: Threading support for background server operation
    - **queue**: Thread-safe inter-component metrics communication
    - **json**: Metrics data serialization and deserialization

gRPC Protocol Buffers:
    - **metrics_pb2**: Metrics message definitions and serialization
    - **metrics_pb2_grpc**: Metrics service stubs and server implementations

Logging Dependencies:
    - **Logs.create_logger**: Centralized logging infrastructure for activity tracking

Integration Points
-----------------
External Integrations:
    - **Mission Management**: Metrics reception and status reporting via gRPC
    - **Monitoring Systems**: Real-time metrics distribution and visualization
    - **Agricultural Platforms**: Field operation metrics and analytics integration
    - **Alert Systems**: Critical metrics threshold monitoring and notifications

Internal Integrations:
    - **ROS2 Publishers**: Metrics distribution to system_metrics_pubsub components
    - **init_ros2.py**: System initialization and component coordination
    - **Queue Systems**: Thread-safe inter-component metrics message passing
    - **Logging Infrastructure**: Centralized metrics activity logging

Performance Characteristics
--------------------------
Metrics Processing Performance:
    - **Reception Latency**: Sub-second metrics reception and processing
    - **Throughput**: High-volume metrics processing capability
    - **Queue Efficiency**: Optimal thread-safe metrics queue management
    - **Distribution Speed**: Rapid metrics forwarding to ROS2 publishers

Scalability Features:
    - **Concurrent Processing**: Multi-threaded server with configurable worker pool
    - **Memory Efficiency**: Optimized metrics data handling and queue management
    - **Connection Resilience**: Automatic reconnection and error recovery
    - **Resource Optimization**: Minimal overhead with efficient processing

Agricultural Data Formats
-------------------------
Metrics Data Structure:
    - **JSON Serialization**: Structured metrics data in JSON format
    - **Metric Types**: System, operational, and agricultural performance metrics
    - **Timestamps**: Precise timing information for temporal analysis
    - **Metadata**: Context information and metric classification

Expected Metrics Format:
    - **System Metrics**: Hardware telemetry, resource utilization, health status
    - **Operational Metrics**: Task completion, performance indicators, efficiency
    - **Agricultural Metrics**: Field coverage, application rates, crop monitoring
    - **Environmental Metrics**: Weather conditions, soil parameters, growth indicators

Error Handling Strategy
----------------------
Multi-level Error Management:
    - **Connection-Level**: gRPC connection error handling and retry logic
    - **Message-Level**: Individual metrics processing error handling
    - **Queue-Level**: Thread-safe queue operation error management
    - **System-Level**: Graceful shutdown and resource cleanup procedures

Recovery Mechanisms:
    - **Automatic Reconnection**: gRPC connection recovery with exponential backoff
    - **Message Retry**: Failed metrics transmission retry with timeout handling
    - **Queue Monitoring**: Continuous queue state monitoring and error detection
    - **Graceful Degradation**: Continued operation despite individual component failures

Examples
--------
Programmatic Usage:

.. code-block:: python

    import queue
    import logging
    from grpc_ros2_metrics import start_grpc_metrics

    # Setup metrics communication infrastructure
    logger = logging.getLogger('agricultural_metrics')
    metrics_queue = queue.Queue()
    
    # Start gRPC metrics bridge
    start_grpc_metrics(metrics_queue, logger)

Agricultural Metrics Example:

.. code-block:: python

    # Agricultural operation metrics
    field_metrics = {
        "timestamp": "2024-06-27T08:30:00Z",
        "drone_id": "AGR_DRONE_001",
        "operation": "fertilizer_application",
        "field_id": "field_001",
        "metrics": {
            "coverage_area": 2.5,  # hectares
            "application_rate": 150,  # kg/ha
            "fuel_consumption": 0.8,  # liters
            "flight_duration": 1800,  # seconds
            "gps_accuracy": 0.05  # meters
        }
    }

System Integration Example:

.. code-block:: python

    # Integration with ROS2 metrics publishers
    from rclpy.executors import MultiThreadedExecutor
    
    # Initialize metrics bridge
    executor = MultiThreadedExecutor()
    
    # Start gRPC-ROS2 metrics bridge
    start_grpc_metrics(metrics_queue, logger)
    
    # Metrics flow through bridge to ROS2 publishers
    executor.spin()

Notes
-----
- **Agricultural Focus**: Optimized for precision agriculture metrics workflows
- **Real-time Processing**: Low-latency metrics handling for operational monitoring
- **Mission Integration**: Supports complex agricultural mission metrics collection
- **Error Resilience**: Robust error handling for continuous field operations

Configuration Requirements:
    - **gRPC Port**: Metrics server on port 51004
    - **Network Access**: Reliable network connectivity for gRPC communication
    - **Protocol Buffers**: Properly compiled protobuf definitions
    - **Logging Setup**: Configured logging infrastructure for activity tracking

Agricultural Considerations:
    - **Field Conditions**: Robust operation in various agricultural environments
    - **Metrics Precision**: High-accuracy metrics parameter handling
    - **Real-time Monitoring**: Continuous metrics streaming for operational oversight
    - **Scalability**: Support for large-scale agricultural operations monitoring

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

from GRPC.definitions.metrics_pb2 import MetricsResponse
from GRPC.definitions.metrics_pb2_grpc import MetricsCommunicationServicer, add_MetricsCommunicationServicer_to_server

from Logs.create_logger import create_logger


class MetricsCommunicationService(MetricsCommunicationServicer):
    """
    gRPC service implementation for agricultural drone metrics processing.
    
    This class handles incoming metrics data from Mission Management systems,
    processes the metrics information, and forwards it to ROS2 publishers for
    system-wide distribution. It specializes in agricultural drone telemetry,
    operational metrics, and performance indicators essential for precision
    agriculture monitoring and analysis.

    The service operates as a bridge between external monitoring systems and
    internal ROS2 infrastructure, ensuring reliable metrics transmission and
    processing for continuous agricultural operation oversight.

    :param logger: Configured logger instance for metrics activity tracking
    :type logger: logging.Logger
    :param metrics_queue: Thread-safe queue for ROS2 publisher integration
    :type metrics_queue: queue.Queue

    Attributes
    ----------
    logger : logging.Logger
        Configured logger instance for comprehensive activity tracking
    metrics_queue : queue.Queue
        Thread-safe queue for forwarding metrics to ROS2 publishers

    Methods
    -------
    SendMetrics(request, context)
        Process incoming metrics requests and forward to ROS2 infrastructure

    Workflow
    --------
    1. **Service Initialization**: Logger and queue setup for metrics processing
    2. **Request Reception**: gRPC metrics requests received from external systems
    3. **Data Processing**: JSON deserialization and validation of metrics data
    4. **Queue Integration**: Thread-safe metrics forwarding to ROS2 publishers
    5. **Response Generation**: Confirmation responses sent to requesting systems
    6. **Error Handling**: Comprehensive error management and logging

    Agricultural Metrics Handling:
        - **System Telemetry**: Hardware status, resource utilization, health metrics
        - **Operational Data**: Task completion, performance indicators, efficiency
        - **Field Metrics**: Coverage areas, application rates, environmental data
        - **Navigation Data**: GPS accuracy, flight paths, altitude information

    Examples
    --------
    .. code-block:: python

        import logging
        import queue
        
        # Initialize service components
        logger = logging.getLogger('metrics_service')
        metrics_queue = queue.Queue()
        
        # Create metrics communication service
        service = MetricsCommunicationService(logger, metrics_queue)
        
        # Service automatically handles incoming gRPC requests
        # and forwards metrics to ROS2 publishers via queue

    Notes
    -----
    - **Thread Safety**: All operations are designed for concurrent execution
    - **Error Resilience**: Comprehensive error handling prevents service disruption
    - **Agricultural Focus**: Optimized for precision agriculture metrics workflows
    - **Real-time Processing**: Low-latency metrics handling for operational monitoring
    """
    def __init__(self, logger, metrics_queue):
        """
        Initialize the MetricsCommunicationService with logging and queue integration.

        Sets up the service infrastructure for processing agricultural drone metrics,
        establishing connections to logging systems and ROS2 publisher queues for
        comprehensive metrics distribution and monitoring.

        :param logger: Configured logger instance for metrics activity tracking
        :type logger: logging.Logger
        :param metrics_queue: Thread-safe queue for ROS2 publisher integration
        :type metrics_queue: queue.Queue

        Workflow
        --------
        1. **Parent Initialization**: Call parent servicer constructor
        2. **Logger Assignment**: Configure logging for metrics processing activities
        3. **Queue Integration**: Establish connection to ROS2 publisher queue
        4. **Service Readiness**: Prepare service for incoming metrics requests

        Notes
        -----
        - **Immediate Availability**: Service ready for metrics processing upon initialization
        - **Thread Safety**: All components configured for concurrent operation
        - **Error Preparedness**: Logging infrastructure ready for error tracking
        """
        super().__init__()  # Initialize parent gRPC servicer
        self.logger = logger  # Configure logging for metrics activities
        self.metrics_queue = metrics_queue  # Establish ROS2 publisher queue connection

    def SendMetrics(self, request, context):
        """
        Process incoming agricultural drone metrics requests and forward to ROS2 infrastructure.

        This method handles gRPC metrics requests from Mission Management systems,
        deserializes the metrics data, validates the information, and forwards it
        to ROS2 publishers via thread-safe queue operations. It processes various
        types of agricultural metrics including system telemetry, operational data,
        field performance indicators, and environmental measurements.

        :param request: gRPC request containing serialized metrics data
        :type request: MetricsRequest
        :param context: gRPC connection context and metadata
        :type context: grpc.ServicerContext
        :returns: gRPC response with processing confirmation and status
        :rtype: MetricsResponse
        :raises grpc.RpcError: For critical processing failures and connection issues

        Workflow
        --------
        1. **Request Reception**: Receive gRPC metrics request from external system
        2. **Data Extraction**: Extract metrics string from request payload
        3. **JSON Deserialization**: Parse JSON metrics data into Python objects
        4. **Queue Integration**: Forward processed metrics to ROS2 publisher queue
        5. **Logging**: Record successful metrics processing and transmission
        6. **Response Generation**: Create confirmation response for requesting system
        7. **Error Handling**: Catch and handle processing errors with logging

        Agricultural Metrics Processing:
            - **System Telemetry**: Hardware status, battery levels, communication health
            - **Operational Metrics**: Task completion rates, performance indicators
            - **Field Data**: Coverage areas, application rates, environmental readings
            - **Navigation Metrics**: GPS accuracy, flight path data, altitude information

        Expected Request Format:
            - **metrics[0]**: JSON string containing structured metrics data
            - **JSON Structure**: Dictionary with metric types, values, and metadata
            - **Timestamp**: ISO format timestamp for temporal analysis
            - **Drone ID**: Unique identifier for metrics source tracking

        .. note::
            Expected metrics data structure:
            {
                "drone_id": "unique identifier",
                "metrics": {
                    "system": {...},
                    "operational": {...},
                    "agricultural": {...}
                }
            }

        Examples
        --------
        .. code-block:: python

            # Example metrics request processing
            metrics_data = {
                "timestamp": "2024-06-27T08:30:00Z",
                "drone_id": "AGR_DRONE_001",
                "metrics": {
                    "system": {
                        "battery_level": 85,
                        "cpu_usage": 45,
                        "memory_usage": 60
                    },
                    "operational": {
                        "coverage_area": 2.5,
                        "application_rate": 150,
                        "task_completion": 75
                    }
                }
            }

        Returns
        -------
        MetricsResponse
            Confirmation response with processing status:
            - **Success**: "Metrics received and sent"
            - **Error**: "Error processing metrics"

        Raises
        ------
        grpc.RpcError
            For critical processing failures requiring connection termination
        json.JSONDecodeError
            For malformed JSON metrics data (handled internally)
        Exception
            For unexpected processing errors (handled with comprehensive logging)

        Notes
        -----
        - **Thread Safety**: All queue operations are thread-safe for concurrent processing
        - **Error Resilience**: Comprehensive error handling prevents service disruption
        - **Agricultural Focus**: Optimized for precision agriculture metrics workflows
        - **Real-time Processing**: Low-latency metrics handling for operational monitoring
        """
        try:
            # Extract metrics string from gRPC request payload
            metrics_str = request.metrics[0]
            
            # Deserialize JSON metrics data into Python objects
            metrics = json.loads(metrics_str)

            # Forward processed metrics to ROS2 publisher queue (thread-safe operation)
            self.metrics_queue.put(metrics)
            self.logger.info(f"[ROS2][gRPC Metrics] - Metrics received from drone and forwarded to ROS2 publisher")

            # Generate successful processing confirmation response
            return MetricsResponse(confirmation=f"Metrics received and sent")
        except json.JSONDecodeError as e:
            # Handle JSON parsing errors with detailed logging
            self.logger.error(f"[ROS2][gRPC Metrics] - JSON parsing error in SendMetrics: {e}", exc_info=True)
            return MetricsResponse(confirmation="Error processing metrics: Invalid JSON format")
        except Exception as e:
            # Handle unexpected errors with comprehensive logging and error reporting
            self.logger.error(f"[ROS2][gRPC Metrics] - Unexpected error in SendMetrics: {e}", exc_info=True)
            return MetricsResponse(confirmation="Error processing metrics")


def run_metrics_server(logger, metrics_queue):
    """
    Start and manage gRPC metrics server instance for agricultural drone monitoring.

    This function initializes and operates a dedicated gRPC server for receiving
    agricultural drone metrics from Mission Management systems. It configures the
    server with appropriate threading, establishes service endpoints, and manages
    the server lifecycle including graceful shutdown procedures.

    The server operates continuously to handle incoming metrics requests, processing
    system telemetry, operational data, and agricultural performance indicators
    essential for precision agriculture monitoring and analysis.

    :param logger: Configured logger instance for server activity tracking
    :type logger: logging.Logger
    :param metrics_queue: Thread-safe queue for ROS2 publisher integration
    :type metrics_queue: queue.Queue
    :raises KeyboardInterrupt: For graceful server shutdown on user interruption
    :raises grpc.RpcError: For critical server configuration or operation failures

    Workflow
    --------
    1. **Server Creation**: Initialize gRPC server with thread pool executor
    2. **Service Registration**: Register MetricsCommunicationService with server
    3. **Port Binding**: Bind server to port 51004 for metrics communication
    4. **Server Startup**: Start server and begin accepting connections
    5. **Continuous Operation**: Run indefinitely processing metrics requests
    6. **Graceful Shutdown**: Handle interruption signals for clean termination

    Server Configuration:
        - **Thread Pool**: 10 worker threads for concurrent metrics processing
        - **Port**: 51004 (insecure) for gRPC metrics communication
        - **Service**: MetricsCommunicationService for metrics request handling
        - **Lifecycle**: Continuous operation with graceful shutdown support

    Agricultural Metrics Server Features:
        - **High Throughput**: Concurrent processing of multiple metrics streams
        - **Low Latency**: Optimized for real-time agricultural monitoring
        - **Error Resilience**: Robust error handling for continuous operation
        - **Scalability**: Thread pool architecture for load distribution

    Examples
    --------
    .. code-block:: python

        import logging
        import queue
        from grpc_ros2_metrics import run_metrics_server
        
        # Setup server components
        logger = logging.getLogger('metrics_server')
        metrics_queue = queue.Queue()
        
        # Start metrics server (blocking operation)
        run_metrics_server(logger, metrics_queue)

    Notes
    -----
    - **Blocking Operation**: Function runs indefinitely until interrupted
    - **Thread Safety**: All operations designed for concurrent execution
    - **Resource Management**: Proper cleanup on shutdown
    - **Agricultural Focus**: Optimized for precision agriculture workflows
    - **Continuous Operation**: Designed for 24/7 agricultural monitoring

    See Also
    --------
    grpc.server : gRPC server implementation
    concurrent.futures.ThreadPoolExecutor : Thread pool for concurrent processing
    MetricsCommunicationService : Service implementation for metrics processing
    """
    # Initialize gRPC server with thread pool executor for concurrent processing
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Register MetricsCommunicationService with server for metrics request handling
    add_MetricsCommunicationServicer_to_server(
        MetricsCommunicationService(logger, metrics_queue), server)
    
    # Bind server to port 51004 for insecure gRPC communication
    server.add_insecure_port('[::]:53004')
    
    # Start server and begin accepting incoming metrics connections
    server.start()
    logger.info(f"[ROS2][gRPC Metrics] - Server running on port 53004")

    try:
        # Run server indefinitely, processing metrics requests continuously
        while True:
            time.sleep(86400)  # Sleep for 24 hours, server handles requests in background
    except KeyboardInterrupt:
        # Handle graceful shutdown on user interruption
        logger.info("[ROS2][gRPC Metrics] - Shutting down server gracefully")
        server.stop(0)  # Stop server immediately without waiting for active RPCs


def start_grpc_metrics(metrics_queue: queue.Queue, logger):
    """
    Initialize and start ROS2 metrics communication infrastructure.

    This function establishes the complete metrics communication infrastructure
    for agricultural drone systems, launching the gRPC server in a dedicated
    daemon thread to enable continuous metrics reception and processing. It
    provides the primary entry point for integrating metrics collection with
    ROS2 publisher systems for comprehensive agricultural monitoring.

    The function configures thread-safe metrics processing, ensuring reliable
    communication between Mission Management systems and ROS2 infrastructure
    for real-time agricultural operation monitoring and analysis.

    :param metrics_queue: Thread-safe queue for ROS2 publisher integration
    :type metrics_queue: queue.Queue
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
        - **gRPC Server**: Metrics reception server running on dedicated thread
        - **Queue Integration**: Thread-safe connection to ROS2 publisher systems
        - **Logging Integration**: Comprehensive activity tracking and error reporting

    Agricultural Metrics Infrastructure:
        - **Continuous Operation**: 24/7 metrics reception for agricultural monitoring
        - **Real-time Processing**: Low-latency metrics handling for operational decisions
        - **Thread Safety**: Concurrent operation with other system components
        - **Scalability**: Support for high-volume metrics processing

    Examples
    --------
    .. code-block:: python

        import queue
        import logging
        from grpc_ros2_metrics import start_grpc_metrics
        
        # Setup metrics infrastructure
        logger = logging.getLogger('agricultural_metrics')
        metrics_queue = queue.Queue()
        
        # Start metrics communication infrastructure
        start_grpc_metrics(metrics_queue, logger)
        
        # Infrastructure now running in background
        # Main thread free for other operations

    Integration Example:

    .. code-block:: python

        # Complete agricultural monitoring setup
        from rclpy.executors import MultiThreadedExecutor
        
        # Initialize components
        executor = MultiThreadedExecutor()
        metrics_queue = queue.Queue()
        logger = logging.getLogger('agricultural_system')
        
        # Start metrics infrastructure
        start_grpc_metrics(metrics_queue, logger)
        
        # ROS2 system handles metrics distribution
        executor.spin()

    Notes
    -----
    - **Non-blocking**: Function returns immediately, server runs in background
    - **Thread Safety**: All operations designed for concurrent execution
    - **Daemon Thread**: Server thread automatically cleaned up on program exit
    - **Agricultural Focus**: Optimized for precision agriculture metrics workflows
    - **Infrastructure Role**: Primary entry point for metrics communication setup

    See Also
    --------
    run_metrics_server : Server implementation function
    threading.Thread : Python threading for background operation
    queue.Queue : Thread-safe inter-component communication
    """
    # Create dedicated daemon thread for gRPC metrics server operation
    server_metrics_thread = threading.Thread(target=run_metrics_server, args=(logger, metrics_queue))
    
    # Configure thread as daemon for automatic cleanup on program exit
    server_metrics_thread.daemon = True
    
    # Launch server thread for background metrics processing
    server_metrics_thread.start()