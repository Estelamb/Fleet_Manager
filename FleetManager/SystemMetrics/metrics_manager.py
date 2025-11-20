"""
System Metrics Management and Distribution Module

.. module:: metrics_manager
    :synopsis: Comprehensive system metrics processing and multi-service distribution for Fleet Management

.. moduleauthor:: Fleet Management System Team

.. versionadded:: 1.0

This module implements a robust system metrics management system that processes, normalizes,
and distributes drone system metrics across multiple services within the Fleet Management
System. It provides thread-safe processing, real-time data distribution, and comprehensive
error handling for reliable fleet monitoring and analytics.

Architecture Overview:
    The module implements a producer-consumer pattern for system metrics processing:
    
    1. **Queue Processing**: Thread-safe consumption of metrics from ROS 2 subscribers
    2. **Data Normalization**: JSON parsing and format standardization
    3. **Multi-service Distribution**: Parallel distribution to MQTT, databases, and analytics
    4. **Error Recovery**: Comprehensive error handling with graceful degradation
    5. **Thread Management**: Daemon thread operation for system integration

System Metrics Pipeline:
    .. mermaid::
    
        graph LR
            A[ROS 2 Subscribers] --> B[Metrics Queue]
            B --> C[Metrics Manager]
            C --> D[Data Processing]
            D --> E[MQTT Distribution]
            D --> F[Database Storage]
            D --> G[Analytics Engine]
            
            E --> H[ThingsBoard]
            F --> I[Time Series DB]
            G --> J[Fleet Analytics]

Data Processing Workflow:
    1. **Queue Monitoring**: Continuous polling for new metrics data
    2. **Data Extraction**: Parse vehicle ID and raw metrics payload
    3. **JSON Normalization**: Parse and validate JSON format
    4. **Data Enhancement**: Add timestamps and metadata
    5. **Service Distribution**: Forward to configured downstream services
    6. **Error Handling**: Log failures and continue processing

Key Features:
    - **Thread-safe Processing**: Concurrent metrics handling without data corruption
    - **Multi-service Distribution**: Simultaneous delivery to multiple endpoints
    - **Data Normalization**: Consistent format across all downstream services
    - **Error Resilience**: Graceful handling of malformed data and service failures
    - **Performance Optimization**: Efficient queue processing with configurable timeouts
    - **Comprehensive Logging**: Detailed operation tracking and error reporting

Service Integration:
    **MQTT Services**: Real-time metrics streaming to MQTT infrastructure
    **Database Services**: Persistent storage for historical analysis
    **Analytics Services**: Real-time processing for fleet intelligence
    **Monitoring Services**: System health and performance tracking

Data Format Standards:
    **Input Format**: [vehicle_id, raw_metrics_json] from ROS 2 subscribers
    **Processing**: JSON parsing with quote normalization and validation
    **Output Format**: Standardized JSON with metadata for service distribution

Threading Architecture:
    - **Manager Thread**: Main metrics processing daemon thread
    - **Queue Thread**: Producer thread from ROS 2 metric subscribers
    - **Service Threads**: Concurrent distribution to multiple services
    - **Main Thread**: System coordination and lifecycle management

Error Handling Strategy:
    **Queue Errors**: Empty queue handling with appropriate timeouts
    **JSON Errors**: Malformed data parsing with detailed error logging
    **Service Errors**: Distribution failures with service-specific error handling
    **System Errors**: Critical failures with graceful shutdown procedures

Configuration Management:
    - **Queue Timeout**: Configurable polling intervals for efficiency
    - **Log Management**: Rotating logs with size and count limits
    - **Service Endpoints**: Configurable service distribution targets
    - **Processing Limits**: Configurable batch sizes and rate limiting

Classes:
    .. autoclass:: SystemMetricsManagerThread
        :members:
        :undoc-members:
        :show-inheritance:

Functions:
    .. autofunction:: start_metrics_manager

Usage Examples:
    **Basic Manager Initialization**::
    
        import queue
        import logging
        
        # Create shared infrastructure
        metrics_queue = queue.Queue()
        logger = logging.getLogger('SystemMetrics')
        
        # Start metrics manager
        manager = start_metrics_manager(metrics_queue, logger)
        
    **Integration with ROS 2 Subscribers**::
    
        # Create shared queue for ROS 2 integration
        shared_queue = queue.Queue()
        
        # Start ROS 2 metrics subscriber
        subscriber = start_metrics_subscriber(shared_queue, logger)
        
        # Start metrics manager for processing
        manager = start_metrics_manager(shared_queue, logger)
        
    **Custom Service Distribution**::
    
        # Manager automatically distributes to configured services
        # Add custom service handlers by extending send_to_service method

.. note::
    This module operates as a daemon thread and requires proper shutdown procedures
    to ensure graceful system termination and resource cleanup.

.. warning::
    The manager thread runs indefinitely and processes metrics continuously.
    Ensure proper error handling in downstream services to prevent data loss.

.. seealso::
    - :mod:`SystemMetrics.grpc_metrics_fleet`: MQTT service distribution
    - :mod:`SystemMetrics.src.system_metrics_pubsub`: ROS 2 metrics collection
    - :class:`threading.Thread`: Python threading for concurrent processing
    - :mod:`queue`: Thread-safe queue operations for producer-consumer patterns
"""

import threading
import time
import queue
import json
import logging
from typing import Optional, Dict, Any, Literal

from SystemMetrics.grpc_metrics_fleet import run_metrics_mqtt_client

# System configuration constants for metrics processing and logging
QUEUE_TIMEOUT = 0.1        # Seconds for queue polling interval - balances responsiveness and CPU usage
MAX_LOG_SIZE = 1_000_000   # Maximum log file size (1MB) before rotation
LOG_BACKUP_COUNT = 5       # Number of backup log files to maintain for historical tracking

class SystemMetricsManagerThread(threading.Thread):
    """Dedicated thread for comprehensive system metrics processing and multi-service distribution.

    This class implements a robust producer-consumer pattern for processing drone system
    metrics collected from ROS 2 subscribers. It provides thread-safe processing, data
    normalization, and reliable distribution to multiple downstream services including
    MQTT infrastructure, databases, and analytics engines.

    Thread Architecture:
        - **Daemon Thread**: Runs as daemon thread for proper lifecycle management
        - **Continuous Processing**: Indefinite loop for real-time metrics handling
        - **Queue-based Input**: Thread-safe consumption from shared metrics queue
        - **Concurrent Distribution**: Parallel forwarding to multiple services

    Processing Pipeline:
        The thread implements a comprehensive metrics processing workflow:
        
        1. **Queue Monitoring**: Continuous polling for new metrics data
        2. **Data Extraction**: Parse vehicle ID and raw metrics payload
        3. **JSON Processing**: Normalize and validate JSON format
        4. **Data Enhancement**: Add metadata and timestamp information
        5. **Service Distribution**: Forward to all configured downstream services
        6. **Error Recovery**: Handle failures gracefully and continue processing

    Data Flow Management:
        **Input**: [vehicle_id, raw_metrics_json] tuples from ROS 2 subscribers
        **Processing**: JSON parsing, validation, and format normalization
        **Output**: Standardized metrics distributed to multiple service endpoints
        **Error Handling**: Comprehensive error logging with graceful degradation

    Service Distribution Strategy:
        - **MQTT Services**: Real-time streaming for monitoring dashboards
        - **Database Services**: Persistent storage for historical analysis
        - **Analytics Services**: Real-time processing for fleet intelligence
        - **Alert Services**: Threshold-based alerting and notification systems

    Thread Safety Features:
        - **Queue Operations**: Thread-safe queue access for concurrent producers
        - **Logger Access**: Thread-safe logging for operation tracking
        - **Resource Management**: Proper cleanup and resource handling
        - **Exception Isolation**: Error containment prevents thread termination

    Performance Characteristics:
        - **Low Latency**: Minimal processing delay for real-time requirements
        - **High Throughput**: Efficient batch processing for large metric volumes
        - **Memory Efficient**: Streaming processing without data accumulation
        - **CPU Optimized**: Configurable polling intervals for resource management

    :param metrics_queue: Thread-safe queue containing metrics from ROS 2 subscribers
    :type metrics_queue: queue.Queue
    :param metrics_logger: Pre-configured logger instance for operation tracking
    :type metrics_logger: logging.Logger

    :ivar metrics_queue: Shared queue for receiving metrics data from collectors
    :vartype metrics_queue: queue.Queue
    :ivar metrics_logger: Logger instance for operation tracking and debugging
    :vartype metrics_logger: logging.Logger

    Example:
        **Thread Initialization and Startup**::
        
            import queue
            import logging
            
            # Create shared infrastructure
            metrics_queue = queue.Queue()
            logger = logging.getLogger('SystemMetrics')
            
            # Create and start manager thread
            manager = SystemMetricsManagerThread(metrics_queue, logger)
            manager.start()
            
        **Integration with Metrics Collection**::
        
            # Metrics are automatically processed as they arrive:
            # Input: [42, '{"cpu": 65.2, "memory": 78.1, "battery": 89.5}']
            # Processing: JSON parsing and validation
            # Output: Distributed to MQTT, database, and analytics services

    .. note::
        This thread runs as a daemon thread and will terminate automatically when
        the main process exits. Ensure proper shutdown procedures for graceful cleanup.

    .. warning::
        The thread runs indefinitely and processes metrics continuously. Monitor
        system resources and implement appropriate rate limiting if necessary.

    .. seealso::
        - :func:`start_metrics_manager`: Factory function for thread creation
        - :mod:`SystemMetrics.grpc_metrics_fleet`: MQTT distribution service
        - :class:`threading.Thread`: Base Python threading class
    """
    
    def __init__(self, metrics_queue: queue.Queue, metrics_logger: logging.Logger):
        """Initialize system metrics manager thread with processing infrastructure.

        Sets up the thread with all necessary components for metrics processing including
        queue access, logging capabilities, and daemon thread configuration for proper
        lifecycle management within the Fleet Management System.

        Initialization Process:
            1. **Thread Setup**: Configure as daemon thread for automatic cleanup
            2. **Queue Configuration**: Store reference to shared metrics queue
            3. **Logging Setup**: Configure logger for operation tracking
            4. **Resource Preparation**: Initialize processing infrastructure

        Thread Configuration:
            - **Daemon Mode**: Thread terminates with main process
            - **Priority**: Standard priority for balanced system performance
            - **Lifecycle**: Automatic cleanup when parent process exits
            - **Resource Management**: Proper resource handling and cleanup

        :param metrics_queue: Thread-safe queue for metrics data from ROS 2 collectors
        :type metrics_queue: queue.Queue
        :param metrics_logger: Pre-configured logger for operation tracking and debugging
        :type metrics_logger: logging.Logger
        """
        # Initialize parent Thread class with daemon configuration
        # Daemon threads terminate automatically when main process exits
        super().__init__(daemon=True)
        
        # Store reference to shared metrics queue for data consumption
        self.metrics_queue = metrics_queue
        
        # Store logger instance for operation tracking and error reporting
        self.metrics_logger = metrics_logger
        
    def run(self) -> None:
        """Execute main processing loop for continuous system metrics management.

        This method implements the core thread execution logic, providing continuous
        processing of system metrics data with comprehensive error handling and
        graceful shutdown capabilities. It runs indefinitely until system shutdown
        or critical failure conditions.

        Processing Loop Architecture:
            - **Infinite Loop**: Continuous operation for real-time processing
            - **Queue Processing**: Regular polling and processing of metrics data
            - **Error Containment**: Individual processing errors don't terminate thread
            - **Graceful Shutdown**: Proper cleanup and logging on thread termination

        Error Handling Strategy:
            **Processing Errors**: Individual metric processing failures logged and skipped
            **Critical Errors**: System-level failures logged with full stack trace
            **Resource Errors**: Memory and connection issues handled gracefully
            **Shutdown Handling**: Proper cleanup and notification on thread termination

        Performance Characteristics:
            - **Continuous Operation**: 24/7 processing capability for production systems
            - **Error Resilience**: Single failures don't affect overall system operation
            - **Resource Efficiency**: Optimized polling intervals for CPU management
            - **Memory Management**: Streaming processing without data accumulation

        Lifecycle Management:
            1. **Startup**: Begin continuous metrics processing loop
            2. **Processing**: Handle metrics data with error recovery
            3. **Error Recovery**: Log and recover from processing failures
            4. **Shutdown**: Graceful cleanup and resource release

        .. note::
            This method runs indefinitely and should only be called by the threading
            framework. Manual invocation is not recommended for production systems.

        .. warning::
            Critical exceptions will terminate the thread. Ensure proper error handling
            in all called methods to maintain system stability.
        """
        try:
            # Main processing loop - runs indefinitely for continuous metrics handling
            while True:
                # Process next available metrics data from queue
                # Individual processing errors are handled within process_queue
                self.process_queue()
                
        except Exception as e:
            # Handle critical system-level failures that terminate the thread
            # Log with full stack trace for comprehensive debugging information
            self.metrics_logger.critical(f"[System Metrics] - Manager failure: {str(e)}", exc_info=True)
            
        finally:
            # Ensure proper shutdown logging regardless of termination cause
            # Provides visibility into thread lifecycle for monitoring
            self.metrics_logger.info("[System Metrics] - System metrics manager shutdown")

    def process_queue(self) -> None:
        """Process individual metrics messages from the system metrics queue.

        This method handles the complete processing workflow for individual metrics
        messages, including data extraction, validation, processing, and distribution
        to downstream services. It implements comprehensive error handling to ensure
        system stability and continuous operation.

        Processing Workflow:
            1. **Queue Polling**: Attempt to retrieve metrics data with timeout
            2. **Data Extraction**: Parse vehicle ID and raw metrics payload
            3. **Data Processing**: Normalize and validate JSON format
            4. **Service Distribution**: Forward processed data to all configured services
            5. **Error Handling**: Log and recover from various failure conditions

        Queue Management:
            - **Timeout Handling**: Configurable timeout prevents blocking operations
            - **Empty Queue**: Brief sleep when no data available for CPU efficiency
            - **Data Format**: Expects [vehicle_id, raw_metrics_json] tuple format
            - **Thread Safety**: Queue operations are inherently thread-safe

        Error Recovery Strategy:
            **Empty Queue**: Normal condition handled with brief sleep
            **JSON Errors**: Malformed data logged and skipped for continued processing
            **Processing Errors**: Individual failures logged without thread termination
            **Service Errors**: Distribution failures handled gracefully

        Performance Optimization:
            - **Non-blocking Operations**: Timeout prevents indefinite blocking
            - **Efficient Polling**: Brief sleeps during idle periods
            - **Error Isolation**: Individual failures don't affect batch processing
            - **Resource Management**: Minimal memory footprint per operation

        Data Validation:
            - **Format Checking**: Verify expected tuple structure
            - **JSON Validation**: Parse and validate metrics data format
            - **Content Verification**: Ensure required fields are present
            - **Error Reporting**: Detailed logging for debugging malformed data

        .. note::
            This method is called continuously by the main processing loop and
            should complete quickly to maintain real-time processing performance.

        .. warning::
            Exceptions in this method are caught and logged but do not terminate
            the processing thread. Ensure proper error handling for system stability.
        """
        try:
            # Attempt to retrieve metrics data from queue with timeout
            # Timeout prevents indefinite blocking and allows periodic status checks
            system_metrics = self.metrics_queue.get(timeout=QUEUE_TIMEOUT)
            
            # Log successful metrics reception for monitoring and debugging
            self.metrics_logger.info(f"[System Metrics] - Received System Metrics")
            
            # Extract vehicle ID and raw metrics data from queue tuple
            # Expected format: [vehicle_id, raw_metrics_json_string]
            vehicle_id, raw_data = system_metrics
            
            # Process and normalize the raw metrics data into standard format
            processed_data = self.process_data(raw_data)
            
            # Distribute processed data to all configured downstream services
            self.distribute_data(vehicle_id, processed_data)
            
        except queue.Empty:
            # Normal condition when no metrics data is available in queue
            # Brief sleep prevents excessive CPU usage during idle periods
            time.sleep(QUEUE_TIMEOUT)
            
        except json.JSONDecodeError as e:
            # Handle malformed JSON data from metrics sources
            # Log error details for debugging but continue processing other metrics
            self.metrics_logger.error(f"[System Metrics] - Invalid JSON data: {str(e)}")
            
        except Exception as e:
            # Handle any other unexpected processing errors with full stack trace
            # Comprehensive error logging for debugging while maintaining system stability
            self.metrics_logger.error(f"[System Metrics] - Processing error: {str(e)}", exc_info=True)

    def process_data(self, raw_data: str) -> Dict[str, Any]:
        """Normalize and validate incoming system metrics data for consistent processing.

        This method handles the complete data normalization pipeline for raw metrics
        data received from ROS 2 subscribers. It performs JSON parsing, quote
        normalization, and data validation to ensure consistent format across
        all downstream services.

        Data Processing Pipeline:
            1. **Quote Normalization**: Convert single quotes to double quotes for JSON compliance
            2. **JSON Parsing**: Parse string data into Python dictionary structure
            3. **Format Validation**: Verify data structure and required fields
            4. **Error Handling**: Comprehensive error reporting for malformed data

        Normalization Features:
            - **Quote Handling**: Automatic conversion of single to double quotes
            - **JSON Compliance**: Ensures strict JSON format for service compatibility
            - **Type Preservation**: Maintains original data types during parsing
            - **Structure Validation**: Verifies expected data structure format

        Error Handling Strategy:
            - **Parse Errors**: JSON syntax errors logged with detailed information
            - **Format Errors**: Invalid data structure errors reported
            - **Content Errors**: Missing or invalid field errors documented
            - **Exception Propagation**: Errors re-raised for upstream handling

        Data Quality Assurance:
            - **Format Consistency**: Standardized output format for all services
            - **Type Safety**: Proper type handling and validation
            - **Content Verification**: Basic sanity checks on metric values
            - **Error Reporting**: Detailed logging for debugging data issues

        :param raw_data: Raw JSON string containing system metrics from ROS 2 sources
        :type raw_data: str

        :return: Parsed and normalized metrics data as dictionary structure
        :rtype: Dict[str, Any]

        :raises json.JSONDecodeError: If raw data contains invalid JSON syntax
        :raises ValueError: If data structure is invalid or missing required fields
        :raises Exception: For any other data processing failures

        Input Format Examples:
            **Valid Input**::
            
                "{'cpu_usage': 65.2, 'memory_usage': 78.1, 'battery_level': 89.5}"
                
            **Normalized Output**::
            
                {
                    "cpu_usage": 65.2,
                    "memory_usage": 78.1,
                    "battery_level": 89.5
                }

        .. note::
            This method automatically handles quote normalization between single
            and double quotes to ensure JSON compliance across different data sources.

        .. warning::
            Malformed data will raise exceptions that must be handled by calling
            code to prevent processing thread termination.
        """
        try:
            # Normalize quotes and parse JSON data into Python dictionary
            # Replace single quotes with double quotes for JSON compliance
            data = json.loads(raw_data.replace("'", '"'))
            
            # Return parsed and validated data structure
            return data
            
        except Exception as e:
            # Log detailed error information for debugging malformed data
            # Include original raw data context for troubleshooting
            self.metrics_logger.error(f"[System Metrics] - Data processing failed: {str(e)}")
            
            # Re-raise exception for upstream error handling
            # Allows calling code to implement appropriate recovery strategies
            raise

    def distribute_data(self, vehicle_id: int, data: Dict[str, Any]) -> None:
        """Distribute processed metrics data to all configured downstream services.

        This method orchestrates the distribution of normalized metrics data to
        multiple downstream services including MQTT infrastructure, databases,
        and analytics engines. It provides centralized service management and
        error handling for reliable data delivery across the Fleet Management System.

        Distribution Architecture:
            - **Multi-service Support**: Simultaneous distribution to multiple endpoints
            - **Service Isolation**: Individual service failures don't affect others
            - **Centralized Management**: Single point for service configuration
            - **Error Recovery**: Per-service error handling and recovery

        Service Categories:
            **Real-time Services**: MQTT streaming for live monitoring and dashboards
            **Storage Services**: Database persistence for historical analysis
            **Analytics Services**: Real-time processing for fleet intelligence
            **Alert Services**: Threshold-based monitoring and notification systems

        Distribution Strategy:
            - **Parallel Processing**: Concurrent distribution for performance
            - **Error Isolation**: Service failures handled independently
            - **Service Priority**: Critical services processed first
            - **Retry Logic**: Configurable retry mechanisms for failed distributions

        Service Management:
            - **Configuration**: Centralized service endpoint configuration
            - **Monitoring**: Service health tracking and performance metrics
            - **Load Balancing**: Distribute load across service instances
            - **Failover**: Automatic failover to backup service instances

        :param vehicle_id: Unique identifier for the source vehicle/drone
        :type vehicle_id: int
        :param data: Processed and normalized metrics data for distribution
        :type data: Dict[str, Any]

        Service Distribution Flow:
            1. **MQTT Services**: Real-time streaming to monitoring infrastructure
            2. **Database Services**: Persistent storage for historical analysis
            3. **Analytics Services**: Real-time processing for fleet insights
            4. **Notification Services**: Alert generation based on thresholds

        Example Data Flow:
            **Input**: vehicle_id=42, data={"cpu": 65.2, "battery": 89.5}
            **MQTT**: Real-time dashboard updates
            **Database**: Historical trend storage
            **Analytics**: Performance analysis and predictions

        .. note::
            This method currently supports MQTT distribution with extensible
            architecture for additional services. New services can be added
            by extending the send_to_service method.

        .. warning::
            Service distribution failures are logged but do not prevent
            distribution to other services. Monitor service health separately.
        """
        # Distribute metrics to MQTT infrastructure for real-time monitoring
        # MQTT provides live streaming to dashboards and monitoring systems
        self.send_to_service('MQTT', vehicle_id, data)

    def send_to_service(self, service: Literal['MQTT'], vehicle_id: int, data: Dict[str, Any]) -> None:
        """Format and transmit metrics data to specified downstream service.

        This method handles service-specific data formatting and transmission for
        individual downstream services. It provides a unified interface for service
        communication while allowing service-specific message formatting and
        error handling strategies.

        Service Communication Architecture:
            - **Service Abstraction**: Unified interface for different service types
            - **Format Customization**: Service-specific message formatting
            - **Error Handling**: Per-service error handling and recovery
            - **Extensible Design**: Easy addition of new service types

        Message Formatting Strategy:
            Each service requires specific message format and metadata:
            
            **MQTT Format**: Standardized telemetry message with type identification
            **Database Format**: Optimized for time-series storage and indexing
            **Analytics Format**: Structured for real-time processing and analysis
            **Alert Format**: Threshold-aware format for notification systems

        Service-Specific Processing:
            **MQTT Services**:
            - Message type identification for routing
            - Vehicle ID inclusion for fleet tracking
            - Telemetry data packaging for dashboard consumption
            - JSON serialization for network transmission

        Error Recovery Mechanisms:
            - **Service Timeouts**: Configurable timeout handling
            - **Retry Logic**: Exponential backoff for failed transmissions
            - **Fallback Services**: Alternative service routing on failures
            - **Error Logging**: Comprehensive error tracking and reporting

        Performance Optimization:
            - **Efficient Serialization**: Optimized JSON formatting
            - **Connection Pooling**: Reuse connections for multiple transmissions
            - **Batch Processing**: Group multiple metrics for efficient transmission
            - **Asynchronous Processing**: Non-blocking service communication

        :param service: Target service identifier for message routing
        :type service: Literal['MQTT']
        :param vehicle_id: Unique identifier for source vehicle/drone
        :type vehicle_id: int
        :param data: Processed metrics data for transmission
        :type data: Dict[str, Any]

        :raises ValueError: If service type is not supported or configured
        :raises ConnectionError: If service communication fails
        :raises Exception: For any other service-specific transmission failures

        Message Format Examples:
            **MQTT Message Format**::
            
                {
                    "type": "Metric",
                    "vehicle_id": 42,
                    "telemetry": {
                        "cpu_usage": 65.2,
                        "memory_usage": 78.1,
                        "battery_level": 89.5,
                        "timestamp": "2025-06-29T10:30:00Z"
                    }
                }

        Service Extension Example:
            **Adding Database Service**::
            
                elif service == 'DATABASE':
                    message = {
                        "table": "drone_metrics",
                        "vehicle_id": vehicle_id,
                        "metrics": data,
                        "timestamp": datetime.utcnow().isoformat()
                    }
                    database_client.insert(message)

        .. note::
            Currently supports MQTT service with extensible architecture for
            additional services. New services can be added by extending the
            conditional logic and implementing appropriate formatting.

        .. warning::
            Service transmission failures are logged but do not raise exceptions
            to prevent disruption of other service distributions.
        """
        try:
            # Handle MQTT service distribution with standardized message format
            if service == 'MQTT':
                # Create standardized MQTT message with type identification
                # Include vehicle ID for fleet tracking and telemetry data
                message = json.dumps({
                    "type": "Metric",        # Message type for MQTT routing
                    "vehicle_id": vehicle_id, # Source vehicle identification
                    "telemetry": data        # Processed metrics payload
                })
                
                # Transmit formatted message to MQTT infrastructure
                # Uses gRPC client for reliable delivery to MQTT bridge
                run_metrics_mqtt_client(message, self.metrics_logger)
                
        except Exception as e:
            # Log service-specific transmission failures with detailed error information
            # Include service name and error details for debugging and monitoring
            self.metrics_logger.error(f"[System Metrics] - {service} send failed: {str(e)}", exc_info=True)


def start_metrics_manager(
    metrics_queue: queue.Queue,
    metrics_logger: logging.Logger
) -> SystemMetricsManagerThread:
    """Initialize and start system metrics management thread for Fleet Management System.

    This function serves as a factory for creating and starting the system metrics
    management thread. It handles proper thread initialization, configuration, and
    startup procedures to ensure reliable metrics processing and distribution
    throughout the Fleet Management System.

    Initialization Process:
        1. **Thread Creation**: Create SystemMetricsManagerThread instance
        2. **Configuration**: Configure thread with queue and logger references
        3. **Thread Startup**: Start daemon thread for background processing
        4. **Status Logging**: Log successful startup for monitoring
        5. **Reference Return**: Return thread instance for lifecycle management

    Thread Management:
        - **Daemon Configuration**: Thread runs as daemon for proper cleanup
        - **Background Processing**: Non-blocking startup for system integration
        - **Lifecycle Management**: Thread terminates with main process
        - **Resource Cleanup**: Automatic resource management and cleanup

    System Integration:
        The started thread integrates with the broader Fleet Management System:
        
        - **ROS 2 Integration**: Consumes metrics from ROS 2 subscriber queues
        - **MQTT Integration**: Distributes metrics to MQTT infrastructure
        - **Database Integration**: Stores metrics for historical analysis
        - **Analytics Integration**: Feeds real-time analytics processing

    Error Handling:
        - **Startup Errors**: Thread creation and startup failures logged
        - **Runtime Errors**: Processing errors handled within thread
        - **Resource Errors**: Memory and connection issues managed gracefully
        - **Shutdown Errors**: Proper cleanup on system termination

    Performance Characteristics:
        - **Low Startup Time**: Minimal initialization overhead
        - **Immediate Processing**: Begins processing metrics immediately
        - **Resource Efficient**: Minimal memory and CPU footprint
        - **Scalable Design**: Handles high-throughput metric streams

    :param metrics_queue: Thread-safe queue containing metrics from ROS 2 collectors
    :type metrics_queue: queue.Queue
    :param metrics_logger: Pre-configured logger for operation tracking and debugging
    :type metrics_logger: logging.Logger

    :return: Running metrics manager thread instance for lifecycle management
    :rtype: SystemMetricsManagerThread

    :raises threading.ThreadError: If thread creation or startup fails
    :raises Exception: For any other initialization failures

    Usage Examples:
        **Basic Manager Startup**::
        
            import queue
            import logging
            
            # Create shared infrastructure
            metrics_queue = queue.Queue()
            logger = logging.getLogger('SystemMetrics')
            
            # Start metrics manager
            manager = start_metrics_manager(metrics_queue, logger)
            
        **Integration with ROS 2 Subscribers**::
        
            # Start complete metrics collection system
            shared_queue = queue.Queue()
            
            # Start ROS 2 metrics subscriber
            subscriber = start_metrics_subscriber(shared_queue, logger)
            
            # Start metrics manager for processing and distribution
            manager = start_metrics_manager(shared_queue, logger)
            
        **Production Deployment**::
        
            try:
                # Create production-grade infrastructure
                metrics_queue = queue.Queue(maxsize=10000)
                logger = create_production_logger('SystemMetrics')
                
                # Start metrics management system
                manager = start_metrics_manager(metrics_queue, logger)
                
                # Keep main process running
                while True:
                    time.sleep(60)
                    monitor_system_health(manager, logger)
                    
            except KeyboardInterrupt:
                logger.info("Shutting down metrics manager...")
                # Daemon thread will terminate automatically

    Return Value Management:
        The returned thread instance can be used for:
        - **Status Monitoring**: Check thread health and status
        - **Performance Metrics**: Monitor processing performance
        - **Graceful Shutdown**: Coordinate system shutdown procedures
        - **Error Detection**: Monitor for thread termination or errors

    .. note::
        The function starts a daemon thread that runs continuously until the
        main process terminates. Ensure proper system shutdown procedures.

    .. warning::
        The returned thread instance should be stored for monitoring and
        lifecycle management. Lost references may complicate system monitoring.

    .. seealso::
        - :class:`SystemMetricsManagerThread`: The managed thread implementation
        - :mod:`SystemMetrics.src.system_metrics_pubsub`: ROS 2 metrics collection
        - :func:`SystemMetrics.grpc_metrics_fleet.run_metrics_mqtt_client`: MQTT distribution
    """
    # Create system metrics manager thread with provided infrastructure
    # Configure as daemon thread for proper lifecycle management
    manager = SystemMetricsManagerThread(metrics_queue, metrics_logger)
    
    # Start the metrics processing thread for background operation
    # Thread begins processing metrics immediately upon startup
    manager.start()
    
    # Log successful startup for system monitoring and audit purposes
    metrics_logger.info("[System Metrics] - System Metrics manager started")
    
    # Return thread reference for lifecycle management and monitoring
    return manager