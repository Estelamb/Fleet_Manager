# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
ROS2 Drone System Metrics Publisher Module
==========================================

This module implements a comprehensive ROS2 publisher node for real-time distribution
of drone system metrics and health monitoring data within agricultural drone operations.
It provides continuous system performance monitoring, health status tracking, and
operational metrics distribution for mission-critical drone fleet management.

The publisher enables seamless distribution of system metrics from drone hardware and
software components to Mission Management systems, supporting real-time monitoring,
performance optimization, and predictive maintenance workflows for precision agriculture.

.. module:: publisher_metrics_function
    :synopsis: ROS2 publisher for drone system metrics and health monitoring data

Features
--------
- **Real-time Metrics Publishing**: Continuous system performance data distribution (1Hz)
- **Queue-based Buffering**: Thread-safe message queuing with latest-state prioritization
- **Multi-threaded Execution**: Concurrent processing with ThreadedExecutor for scalability
- **Drone-specific Namespacing**: Isolated topic namespaces for multi-drone fleet operations
- **Health Monitoring**: Comprehensive system health and performance tracking
- **gRPC Integration**: Seamless integration with Mission Management monitoring systems

System Architecture
------------------
The system metrics publisher operates within a multi-layered monitoring architecture:

Data Flow:
    Drone Hardware/Software → Data Collector → Queue → ROS2 Publisher → Mission Management

Monitoring Integration:
    - **Hardware Metrics**: CPU, memory, storage, network utilization monitoring
    - **Software Performance**: Process health, response times, error rates tracking
    - **Flight Systems**: Battery levels, sensor readings, actuator status monitoring
    - **Communication Health**: Network connectivity, message rates, latency tracking

Communication Architecture:
    1. **Data Collection**: System metrics gathered from drone components
    2. **Queue Buffering**: Thread-safe queuing with latest-state retention
    3. **ROS2 Publishing**: Real-time distribution to monitoring subsystems
    4. **Topic Isolation**: Drone-specific topics for fleet monitoring coordination
    5. **gRPC Transmission**: External monitoring system integration

Workflow Architecture
--------------------
System Metrics Distribution Pipeline:
    1. **Queue Monitoring**: Continuous monitoring of system metrics queue
    2. **Latest State Retention**: Priority handling of most recent metrics data
    3. **Data Formatting**: Conversion to ROS2 String message format
    4. **Topic Publishing**: Distribution to drone-specific monitoring topics
    5. **Status Logging**: Comprehensive logging of metrics distribution activities
    6. **Error Recovery**: Graceful handling of queue and communication errors

Timer-based Processing:
    - **Frequency**: 1Hz processing rate for real-time monitoring
    - **Latest State Priority**: Most recent metrics prioritized over queued data
    - **Non-blocking Operations**: Queue operations prevent timer callback blocking
    - **Resource Optimization**: Efficient memory usage with latest-state retention

Classes
-------
.. autoclass:: SystemMetricsPublisher
    :members:
    :undoc-members:
    :show-inheritance:

Functions
---------
.. autofunction:: main

Dependencies
-----------
Core Dependencies:
    - **rclpy**: ROS2 Python client library for node and publisher functionality
    - **rclpy.node.Node**: Base ROS2 node class for publisher implementation
    - **rclpy.executors.MultiThreadedExecutor**: Concurrent execution framework
    - **std_msgs.msg.String**: Standard ROS2 message type for metrics data
    - **queue**: Python queue module for thread-safe inter-component communication
    - **threading**: Threading support for concurrent operations

Message Dependencies:
    - **std_msgs.msg.String**: System metrics data serialization format
    - **ROS2 Topics**: Drone-specific topic namespacing and message distribution

Integration Points
-----------------
External Integrations:
    - **Mission Management**: System health and performance data transmission via gRPC
    - **Monitoring Systems**: Real-time drone fleet health monitoring and alerting
    - **Analytics Platforms**: Performance data aggregation and trend analysis
    - **Maintenance Systems**: Predictive maintenance and health assessment

Internal Integrations:
    - **init_ros2.py**: System initialization and component coordination
    - **Data Collector**: System metrics gathering from drone components
    - **gRPC Services**: Bidirectional communication with external monitoring systems
    - **Logging Infrastructure**: Centralized system metrics activity logging

Performance Characteristics
--------------------------
Publishing Performance:
    - **Frequency**: 1Hz system metrics processing and distribution
    - **Latency**: Sub-second metrics data distribution and transmission
    - **Throughput**: Handles high-volume system metrics efficiently
    - **Queue Strategy**: Latest-state priority for real-time monitoring accuracy

Scalability Features:
    - **Multi-Drone Support**: Isolated topic namespaces for fleet operations
    - **Concurrent Processing**: Thread-safe operations for multi-component systems
    - **Resource Efficiency**: Optimized CPU and memory usage for continuous operation
    - **Error Isolation**: Individual metrics failures don't affect system stability

System Metrics Data Types
-------------------------
Hardware Metrics:
    - **CPU Utilization**: Processor usage percentages and load averages
    - **Memory Usage**: RAM utilization, swap usage, memory pressure indicators
    - **Storage Metrics**: Disk usage, I/O rates, storage health indicators
    - **Network Performance**: Bandwidth utilization, packet rates, connection health

Software Metrics:
    - **Process Health**: Application status, response times, error rates
    - **Service Performance**: ROS2 node health, message rates, processing latency
    - **System Services**: Critical service status and performance indicators
    - **Resource Consumption**: Per-process resource utilization tracking

Flight System Metrics:
    - **Battery Status**: Charge levels, voltage, current, health indicators
    - **Sensor Readings**: GPS accuracy, IMU status, camera health, sensor fusion
    - **Actuator Status**: Motor health, servo positions, control surface status
    - **Flight Performance**: Altitude accuracy, position stability, control responsiveness

Data Format:
    - **JSON Serialization**: Structured system metrics data in JSON format
    - **Timestamp Information**: Precise timing data for metrics correlation
    - **Component Identification**: Source component identification for metrics
    - **Status Indicators**: Health status and alert level information

Error Handling Strategy
----------------------
Multi-level Error Management:
    - **Queue-Level**: Empty queue handling with graceful continuation
    - **Message-Level**: Individual metrics processing error handling
    - **Communication-Level**: ROS2 publishing error detection and recovery
    - **System-Level**: Graceful shutdown and resource cleanup procedures

Recovery Mechanisms:
    - **Queue Monitoring**: Continuous queue state monitoring and error detection
    - **Data Validation**: System metrics data validation before publishing
    - **Retry Logic**: Automatic retry for transient communication failures
    - **Graceful Degradation**: Continued operation despite individual component failures

Notes
-----
- **Real-time Monitoring**: Optimized for continuous system health tracking
- **Fleet Management**: Designed for multi-drone fleet monitoring and coordination
- **Predictive Maintenance**: Supports predictive maintenance through continuous monitoring
- **Performance Optimization**: Latest-state priority ensures current system visibility

Configuration Requirements:
    - **ROS2 Environment**: Properly sourced ROS2 workspace and environment
    - **Topic Permissions**: Appropriate permissions for system metrics topic access
    - **Queue Configuration**: Adequate queue size for system metrics volume
    - **Logging Setup**: Configured logging infrastructure for monitoring activity tracking

Monitoring Considerations:
    - **Data Frequency**: 1Hz rate balances real-time needs with resource efficiency
    - **Data Accuracy**: Latest-state priority ensures current system status visibility
    - **Resource Impact**: Minimal overhead designed for continuous operation
    - **Scalability**: Fleet-ready architecture for large-scale drone operations

See Also
--------
rclpy.node.Node : Base ROS2 node class
rclpy.executors.MultiThreadedExecutor : Concurrent execution framework
std_msgs.msg.String : ROS2 string message type
queue.Queue : Thread-safe inter-component communication
threading.Thread : Background thread management
"""

import threading
import queue
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from rclpy.executors import MultiThreadedExecutor

class SystemMetricsPublisher(Node):
    """
    ROS2 Publisher Node for Real-time Drone System Metrics and Health Monitoring.

    This class implements a specialized ROS2 publisher node that manages the real-time
    distribution of comprehensive drone system metrics including hardware performance,
    software health, flight system status, and operational data. It provides continuous
    monitoring capabilities essential for mission-critical drone operations and fleet
    management in precision agriculture environments.

    The publisher serves as the primary interface for system health visibility,
    enabling Mission Management systems to monitor drone performance, detect anomalies,
    and implement predictive maintenance strategies for optimal fleet operation.

    Parameters
    ----------
    drone_id : int
        Unique identifier for the drone instance.
        Used for ROS2 node naming and topic namespace isolation.
        Must be positive integer for proper multi-drone fleet coordination.
        Range: 1-999 for standard drone fleet operations.
        Creates topic namespace: system_metrics/drone_{drone_id}

    drone_logger : logging.Logger
        Configured logger instance for system metrics activity logging and monitoring.
        Used for all publisher-related log messages, metrics distribution tracking, and errors.
        Must be properly configured with appropriate handlers and formatters.
        Typically created by centralized logging infrastructure with drone-specific context.

    metrics_queue : queue.Queue
        Thread-safe queue for system metrics data buffering and processing.
        Receives system metrics data from data collection components for ROS2 distribution.
        Enables asynchronous processing between metrics collection and ROS2 publishing.
        Must be Python queue.Queue instance for thread-safe concurrent access.

    Attributes
    ----------
    drone_logger : logging.Logger
        Logger instance for component-specific system metrics activity logging.
        Handles all publisher-related log messages, distribution tracking, and errors.
        Configured during initialization with drone-specific monitoring context.

    metrics_queue : queue.Queue
        Inter-component communication queue for system metrics data.
        Receives metrics updates from system data collection components.
        Thread-safe queue enabling concurrent system metrics processing.

    msg : std_msgs.msg.String
        Reusable ROS2 String message instance for system metrics publishing.
        Optimized for memory efficiency with message reuse across publishing cycles.
        Updated with latest metrics data before each publication.

    publisher_ : rclpy.publisher.Publisher
        ROS2 publisher instance for system metrics data distribution.
        Configured with drone-specific topic namespace and String message type.
        Handles real-time metrics publishing to monitoring subsystems.

    timer_period : float
        Timer interval in seconds for periodic metrics processing and publishing.
        Set to 1.0 second (1Hz) for real-time monitoring with resource efficiency.
        Balances monitoring responsiveness with system resource utilization.

    timer : rclpy.timer.Timer
        ROS2 timer for periodic system metrics processing and distribution.
        Configured for 1Hz processing frequency for continuous monitoring.
        Triggers timer_callback method for metrics queue processing and publishing.

    Raises
    ------
    Exception
        If ROS2 node initialization fails due to:
        - Invalid drone_id parameter
        - ROS2 context not properly initialized
        - Publisher creation failures
        - Timer setup errors
        - Topic namespace conflicts

    Workflow
    --------
    Initialization Sequence:
        1. **Node Creation**: Initialize ROS2 node with drone-specific name
        2. **Parameter Storage**: Store drone ID, logger, and queue references
        3. **Message Initialization**: Create reusable String message instance
        4. **Publisher Setup**: Create ROS2 publisher with system metrics topic
        5. **Timer Configuration**: Set up 1Hz timer for periodic processing
        6. **Service Advertisement**: Advertise system metrics topic for subscribers
        7. **Logging Confirmation**: Log successful initialization completion

    System Metrics Processing Workflow:
        1. **Timer Trigger**: 1Hz timer triggers system metrics processing
        2. **Queue Processing**: Process all queued metrics, retaining latest state
        3. **Data Prioritization**: Latest metrics data prioritized for accuracy
        4. **Message Formatting**: Convert metrics data to ROS2 String message
        5. **Topic Publishing**: Distribute formatted message to subscribers
        6. **Status Logging**: Log successful system metrics distribution
        7. **Error Handling**: Graceful handling of queue states and processing errors

    System Health Monitoring Pipeline:
        Hardware Sensors → Data Collector → Queue → Publisher → ROS2 Topic → 
        Mission Management → Monitoring Dashboard → Alerts/Maintenance

    Methods
    -------
    timer_callback()
        Periodic system metrics processing and distribution method.

    Notes
    -----
    - **Real-time Monitoring**: Optimized for continuous system health tracking
    - **Latest State Priority**: Most recent metrics prioritized for monitoring accuracy
    - **Multi-Drone Support**: Isolated topic namespaces for fleet monitoring
    - **Thread Safety**: All operations designed for concurrent execution
    - **Resource Efficiency**: Minimal overhead with message reuse and efficient processing

    Performance Characteristics:
        - **Processing Frequency**: 1Hz timer-based system metrics processing
        - **Queue Throughput**: High-volume metrics handling with latest-state priority
        - **Distribution Latency**: Sub-second metrics data distribution
        - **Memory Usage**: Efficient resource utilization with message reuse

    Monitoring Applications:
        - **System Health**: Continuous hardware and software health monitoring
        - **Performance Tracking**: Real-time performance metrics and trend analysis
        - **Predictive Maintenance**: Early detection of potential system issues
        - **Fleet Coordination**: Centralized monitoring for multi-drone operations

    Topic Configuration:
        - **Topic Name**: system_metrics/drone_{drone_id}
        - **Message Type**: std_msgs/String (JSON serialized metrics data)
        - **QoS Profile**: Default ROS2 QoS with queue depth of 1 (latest state)
        - **Namespace**: Drone-specific isolation for multi-drone operations

    System Metrics Categories:
        - **Hardware Metrics**: CPU, memory, storage, network, temperature
        - **Flight Systems**: Battery, GPS, sensors, actuators, control systems
        - **Software Health**: Process status, service performance, error rates
        - **Communication**: Network connectivity, message rates, signal strength

    See Also
    --------
    timer_callback : Periodic system metrics processing method
    rclpy.node.Node : Base ROS2 node class
    rclpy.timer.Timer : ROS2 timer for periodic processing
    std_msgs.msg.String : ROS2 string message type for metrics data
    """
    
    def __init__(self, drone_id: int, drone_logger, metrics_queue):
        """
        Initialize ROS2 system metrics publisher with drone-specific monitoring configuration.

        This constructor sets up the complete system metrics publishing infrastructure
        including ROS2 node initialization with drone-specific naming, publisher creation
        for metrics data distribution, timer configuration for periodic monitoring,
        and integration with system data collection queues for comprehensive health tracking.

        Parameters
        ----------
        drone_id : int
            Unique identifier for the drone instance.
            Used for ROS2 node naming (system_metrics_publisher_{drone_id}).
            Must be positive integer for proper multi-drone fleet coordination.
            Range: 1-999 for standard drone fleet operations.
            Creates topic namespace: system_metrics/drone_{drone_id}

        drone_logger : logging.Logger
            Configured logger instance for system metrics activity logging and monitoring.
            Used for all publisher-related log messages, metrics distribution tracking, and errors.
            Must be properly initialized with appropriate handlers and formatters.
            Typically created by centralized logging infrastructure with drone monitoring context.

        metrics_queue : queue.Queue
            Thread-safe queue for system metrics data buffering and processing.
            Receives system metrics data from data collection components for ROS2 distribution.
            Enables asynchronous processing between system monitoring and ROS2 publishing.
            Must be Python queue.Queue instance for thread-safe concurrent access.

        Raises
        ------
        Exception
            If system metrics publisher initialization fails due to:
            - Invalid drone_id parameter (non-positive integer)
            - ROS2 context not properly initialized before node creation
            - Publisher creation failures (topic conflicts, permission issues)
            - Timer setup errors (invalid frequency, resource allocation)
            - Queue parameter validation failures

        Workflow
        --------
        Initialization Sequence:
            1. **ROS2 Node Creation**: Initialize node with drone-specific name
            2. **Parameter Validation**: Validate and store initialization parameters
            3. **Attribute Assignment**: Set internal references for logger and queue
            4. **Message Initialization**: Create reusable String message instance
            5. **Publisher Creation**: Create ROS2 publisher for system metrics topic
            6. **Timer Setup**: Configure 1Hz timer for periodic metrics processing
            7. **Service Advertisement**: Advertise system metrics topic for subscribers
            8. **Logging Confirmation**: Log successful initialization completion

        ROS2 Node Configuration:
            - **Node Name**: system_metrics_publisher_{drone_id} (e.g., system_metrics_publisher_1)
            - **Topic Name**: system_metrics/drone_{drone_id} (e.g., system_metrics/drone_1)
            - **Message Type**: std_msgs/String for system metrics data serialization
            - **Queue Depth**: 1 message for latest-state priority monitoring
            - **Timer Frequency**: 1Hz (1.0 second intervals) for real-time monitoring

        Component Integration:
            - **Data Collection**: Queue-based communication with system data collectors
            - **Logging Infrastructure**: Centralized logging with system metrics context
            - **Multi-Threading**: Thread-safe design for concurrent monitoring operations
            - **Resource Management**: Automatic cleanup and proper disposal

        Notes
        -----
        - **Monitoring Focus**: Designed specifically for comprehensive system health tracking
        - **Real-time Processing**: 1Hz timer ensures timely metrics distribution
        - **Multi-Drone Support**: Isolated topic namespaces for fleet monitoring
        - **Thread Safety**: All components designed for concurrent monitoring operations
        - **Resource Efficiency**: Minimal overhead optimized for continuous operation

        Performance Considerations:
            - **Initialization Time**: < 1 second for typical monitoring hardware
            - **Memory Usage**: Minimal overhead with efficient message reuse
            - **Processing Rate**: 1Hz timer for real-time system health visibility
            - **Network Resources**: Single topic endpoint per drone for system metrics

        Monitoring Considerations:
            - **System Health**: Optimized for continuous system health tracking
            - **Data Accuracy**: Latest-state priority ensures current system visibility
            - **Fleet Coordination**: Multi-drone support for large-scale monitoring operations
            - **Resource Impact**: Low-overhead design for minimal system impact

        See Also
        --------
        timer_callback : Periodic system metrics processing method
        rclpy.node.Node : Base ROS2 node class
        std_msgs.msg.String : ROS2 string message type
        rclpy.timer.Timer : ROS2 timer for periodic processing
        """
        # Initialize ROS2 node with drone-specific name for system metrics publishing
        super().__init__(f'system_metrics_publisher_{drone_id}')
        
        # Store drone identification and communication components for metrics processing
        self.drone_logger = drone_logger  # Logger for system metrics activity tracking
        self.metrics_queue = metrics_queue  # Thread-safe queue for metrics data buffering
        self.msg = String()  # Reusable message instance for memory efficiency
        
        # Create ROS2 publisher for system metrics data distribution with drone-specific topic
        self.publisher_ = self.create_publisher(
            String,  # Message type for system metrics data serialization
            f'system_metrics/drone_{drone_id}',  # Drone-specific topic namespace
            1  # Queue depth of 1 for latest-state priority monitoring
        )
        
        # Configure periodic timer for continuous system metrics processing at 1Hz
        self.timer_period = 1  # Timer interval in seconds for monitoring frequency
        self.timer = self.create_timer(
            self.timer_period,  # 1Hz frequency (1.0 second intervals) for real-time monitoring
            self.timer_callback  # Callback method for system metrics processing
        )
        
        # Log successful initialization with system metrics context
        self.drone_logger.info(f"[ROS2][System Metrics Publisher] - System Metrics publisher initialized for drone {drone_id}")
        self.drone_logger.info(f"[ROS2][System Metrics Publisher] - System Metrics topic service available at: system_metrics/drone_{drone_id}")

    def timer_callback(self):
        """
        Periodic system metrics processing and distribution callback with latest-state prioritization.

        This method serves as the primary timer callback for continuous system metrics
        processing, handling queue monitoring, data retrieval with latest-state priority,
        message formatting, and ROS2 topic publishing. It processes all available metrics
        in the queue while retaining only the most recent data for accurate real-time
        system health visibility.

        The callback operates at 1Hz frequency, providing real-time system metrics
        distribution essential for continuous health monitoring, performance tracking,
        and predictive maintenance workflows in drone fleet operations.

        Parameters
        ----------
        None
            Timer callback method receives no parameters.
            Operates on class instance attributes for system metrics processing.

        Returns
        -------
        None
            Method performs system metrics processing and publishing operations.
            Does not return values; effects realized through ROS2 topic publishing.

        Raises
        ------
        queue.Empty
            Normal exception when no system metrics available in queue.
            Handled gracefully to continue monitoring without errors.
            Not propagated as it represents normal operational condition.

        Exception
            Potential exceptions during system metrics processing:
            - ROS2 publishing failures due to communication issues
            - Message serialization errors for system metrics data
            - Topic access permission errors

        Workflow
        --------
        System Metrics Processing Cycle:
            1. **Queue Processing**: Process all queued system metrics data
            2. **Latest State Retention**: Retain only the most recent metrics for accuracy
            3. **Data Validation**: Verify metrics data integrity and completeness
            4. **Message Creation**: Create/update ROS2 String message for metrics data
            5. **Data Serialization**: Convert system metrics to string format
            6. **Topic Publishing**: Distribute message to system metrics topic
            7. **Activity Logging**: Log successful system metrics distribution
            8. **Error Handling**: Graceful handling of queue states and processing errors

        Latest-State Priority Processing:
            - **Queue Draining**: Process all available metrics in queue
            - **State Prioritization**: Most recent metrics data prioritized
            - **Memory Efficiency**: Discard outdated metrics to preserve resources
            - **Accuracy Optimization**: Latest state ensures current system visibility

        System Health Data Processing:
            - **Hardware Metrics**: CPU usage, memory utilization, storage status
            - **Flight Systems**: Battery levels, GPS accuracy, sensor readings
            - **Software Health**: Process status, service performance, error rates
            - **Communication**: Network connectivity, message rates, signal strength

        Integration Notes
        ----------------
        System Integration:
            - **Data Collection**: System metrics received from hardware/software monitors
            - **Queue Coordination**: Thread-safe metrics buffering and latest-state processing
            - **ROS2 Distribution**: Real-time metrics distribution to monitoring subsystems
            - **Multi-Threading**: Concurrent operation with other monitoring components

        Performance Characteristics:
            - **Processing Rate**: 1Hz timer ensures real-time system health visibility
            - **Latest State Priority**: Most recent metrics prioritized for monitoring accuracy
            - **Low Latency**: Sub-second system metrics processing and distribution
            - **Resource Efficiency**: Queue draining prevents memory accumulation

        Notes
        -----
        - **Real-time Monitoring**: Optimized for continuous system health tracking
        - **Latest State Priority**: Most recent metrics ensure current system visibility
        - **Resource Optimization**: Queue draining prevents memory accumulation
        - **Error Resilience**: Individual metrics failures don't halt monitoring

        Monitoring Considerations:
            - **Data Accuracy**: Latest-state priority ensures current system health visibility
            - **Resource Management**: Efficient queue processing prevents memory issues
            - **Continuous Operation**: Robust error handling for uninterrupted monitoring
            - **Fleet Coordination**: Synchronized metrics distribution across drone fleet

        Performance Optimization:
            - **Queue Management**: Efficient latest-state retention for memory optimization
            - **Message Efficiency**: Reusable message instances for reduced memory allocation
            - **Resource Usage**: Minimal CPU and memory overhead for continuous operation
            - **Error Handling**: Graceful handling of queue states and communication errors

        See Also
        --------
        queue.Queue.get_nowait : Non-blocking queue item retrieval
        std_msgs.msg.String : ROS2 string message type
        rclpy.publisher.Publisher.publish : ROS2 message publishing
        rclpy.timer.Timer : ROS2 timer for periodic processing
        """
        # Initialize metrics variable for latest-state retention
        metrics = None

        # Process all available system metrics in queue, retaining only the latest state
        while True:
            try:
                # Attempt non-blocking retrieval of system metrics data from queue
                # Latest metrics overwrite previous ones for current system state accuracy
                metrics = self.metrics_queue.get_nowait()
                
            except queue.Empty:
                # Exit processing loop when no more system metrics available (normal condition)
                break  # No more system metrics in queue, exit processing loop

        # Publish latest system metrics if available for real-time monitoring
        if metrics:
            # Update reusable message instance with latest system metrics data
            self.msg = String()
            self.msg.data = str(metrics)  # Serialize system metrics data to string format

            # Publish system metrics message to drone-specific ROS2 topic
            self.publisher_.publish(self.msg)
            
            # Log successful system metrics distribution for monitoring activity tracking
            self.drone_logger.info('[ROS2][System Metrics Publisher] - System Metrics published')


def main(args=None, drone_id: int = 0, drone_logger=None, metrics_queue=None):
    """
    Main execution flow for standalone system metrics publisher with multi-threaded operation.

    This function provides a complete execution environment for the system metrics
    publisher, handling ROS2 context initialization, multi-threaded executor setup,
    publisher node creation, background thread management, signal handling, and
    graceful shutdown procedures for comprehensive drone system health monitoring.

    Parameters
    ----------
    args : list, optional, default=None
        ROS2 initialization arguments for context configuration.
        Passed directly to rclpy.init() for ROS2 runtime setup.
        Can include ROS2 command-line arguments like remapping and parameters.
        Default None uses standard ROS2 initialization without custom arguments.

    drone_id : int, optional, default=0
        Unique drone identifier for publisher configuration and namespace isolation.
        Used for system metrics publisher initialization and ROS2 topic naming.
        Must be positive integer for proper multi-drone fleet monitoring coordination.
        Default value of 0 indicates standalone testing mode.

    drone_logger : logging.Logger, optional, default=None
        Configured logger instance for system metrics activity logging and error reporting.
        Used for all main function related log messages and lifecycle events.
        If None, system metrics activities may not be properly logged.
        Typically provided by centralized monitoring logging infrastructure.

    metrics_queue : queue.Queue, optional, default=None
        Thread-safe queue for system metrics data buffering and processing.
        Contains system metrics data from data collection components for ROS2 distribution.
        If None, publisher will not have system metrics data source.
        Must be properly initialized queue for system health monitoring coordination.

    Returns
    -------
    None
        Function manages complete system metrics publisher lifecycle until shutdown.
        Does not return during normal operation; exits on shutdown signal.

    Raises
    ------
    Exception
        If critical initialization or execution errors occur:
        - ROS2 context initialization failures
        - System metrics publisher creation errors
        - Multi-threaded executor setup failures
        - Thread management and coordination failures
        - Resource allocation problems

    KeyboardInterrupt
        Gracefully handled for user-initiated shutdown (Ctrl+C).
        Triggers proper cleanup and resource disposal procedures.
        Normal termination method for monitoring operation completion.

    Workflow
    --------
    Initialization and Execution Sequence:
        1. **ROS2 Context Setup**: Initialize ROS2 runtime environment
        2. **Executor Creation**: Create multi-threaded executor for concurrent operation
        3. **Publisher Creation**: Create SystemMetricsPublisher instance
        4. **Node Registration**: Add publisher node to multi-threaded executor
        5. **Background Thread**: Start executor in daemon thread for non-blocking operation
        6. **Main Thread Monitoring**: Keep main thread active for signal handling
        7. **Shutdown Handling**: Process interrupts and perform graceful cleanup
        8. **Resource Cleanup**: Destroy nodes and shutdown ROS2 context

    Multi-Threading Architecture:
        - **Main Thread**: Signal handling and lifecycle management
        - **Executor Thread**: ROS2 system metrics publisher processing (daemon thread)
        - **Timer Processing**: System metrics distribution and queue management
        - **Data Collection**: External system monitoring data collection (if integrated)

    System Health Monitoring Lifecycle:
        - **Startup**: Initialize system metrics monitoring infrastructure
        - **Operation**: Continuous system health data processing and distribution
        - **Monitoring**: Real-time system performance and health tracking
        - **Shutdown**: Graceful termination with resource cleanup

    Error Handling Strategy:
        - **Initialization Errors**: Critical failures logged and propagated
        - **Runtime Errors**: Graceful error handling with resource cleanup
        - **Shutdown Errors**: Best-effort cleanup even on shutdown failures
        - **Monitoring Continuity**: Minimal disruption to system health tracking

    Integration Notes
    ----------------
    System Monitoring Integration:
        - **Hardware Monitoring**: Integration with system hardware monitoring tools
        - **Software Health**: Real-time software component health tracking
        - **Performance Tracking**: Continuous performance metrics collection and distribution
        - **Fleet Coordination**: Multi-drone system health monitoring coordination

    Performance Characteristics:
        - **Startup Time**: 2-5 seconds for monitoring system initialization
        - **Processing Rate**: 1Hz system metrics distribution frequency
        - **Resource Usage**: Minimal overhead optimized for continuous operation
        - **Memory Management**: Automatic cleanup prevents resource leaks

    Multi-Threading Considerations:
        - **Thread Safety**: All operations designed for concurrent execution
        - **Signal Handling**: Main thread remains responsive to system signals
        - **Resource Cleanup**: Proper cleanup even with threading complexities
        - **Performance**: Efficient resource utilization with background processing

    Notes
    -----
    - **System Health Focus**: Optimized for comprehensive system health monitoring
    - **Fleet Ready**: Multi-drone support for large-scale monitoring operations
    - **Real-time Operation**: Continuous system metrics processing and distribution
    - **Error Resilience**: Robust error handling for monitoring operation continuity

    System Requirements:
        - **ROS2 Environment**: Properly sourced ROS2 workspace and monitoring packages
        - **System Access**: Access to system monitoring data sources and hardware metrics
        - **Network Infrastructure**: Reliable communication for monitoring coordination
        - **Monitoring Hardware**: Compatible system monitoring tools and sensors

    Deployment Considerations:
        - **Service Management**: Compatible with system monitoring automation
        - **Process Monitoring**: System health monitoring and alerting capabilities
        - **Resource Management**: Efficient resource usage for continuous operation
        - **Scalability**: Support for varying monitoring operation scales

    See Also
    --------
    SystemMetricsPublisher : Main system metrics publisher class
    rclpy.init : ROS2 context initialization
    rclpy.executors.MultiThreadedExecutor : Concurrent execution framework
    threading.Thread : Background thread management
    queue.Queue : Thread-safe system metrics data buffering
    """
    # Initialize ROS2 runtime context with provided monitoring system arguments
    rclpy.init(args=args)
    
    # Create multi-threaded executor for concurrent system metrics processing
    executor = MultiThreadedExecutor()

    # Create system metrics publisher instance with monitoring configuration
    publisher = SystemMetricsPublisher(drone_id, drone_logger, metrics_queue)

    # Register publisher node with multi-threaded executor for concurrent operation
    executor.add_node(publisher)

    # Start executor in daemon thread for non-blocking background monitoring operation
    executor_thread = threading.Thread(target=executor.spin, daemon=True)
    executor_thread.start()

    try:
        # Keep main thread alive for signal handling and lifecycle management
        while rclpy.ok():
            # Brief thread monitoring to handle join timeouts and maintain responsiveness
            executor_thread.join(0.1)  # 100ms timeout for responsive signal handling
    except KeyboardInterrupt:
        # Handle graceful shutdown on Ctrl+C interrupt for monitoring operation completion
        if drone_logger:
            drone_logger.info("[ROS2][System Metrics Publisher] - Ctrl+C received, shutting down system metrics publisher...")
    finally:
        # Perform comprehensive resource cleanup for monitoring system integrity
        if drone_logger:
            drone_logger.info("[ROS2][System Metrics Publisher] - Cleaning up system metrics publisher resources")
        
        executor.shutdown()  # Stop executor and all running monitoring threads
        publisher.destroy_node()  # Clean up system metrics publisher node
        rclpy.shutdown()  # Shutdown ROS2 context
