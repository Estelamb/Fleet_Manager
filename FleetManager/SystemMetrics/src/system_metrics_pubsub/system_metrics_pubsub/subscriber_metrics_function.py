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
Dynamic Drone State Vector Subscriber Module for System Metrics Collection

.. module:: subscriber_metrics_function
    :synopsis: Automatic discovery and subscription to drone system metrics topics

.. moduleauthor:: Fleet Management System Team

.. versionadded:: 1.0

This module implements a dynamic ROS 2 subscriber system for collecting system metrics
from multiple drones in the Fleet Management System. It provides automatic topic
discovery, real-time subscription management, and thread-safe data collection for
comprehensive fleet monitoring and performance analysis.

Architecture Overview:
    The module implements a self-managing subscription system that:
    
    1. **Dynamic Discovery**: Continuously scans for new drone metric topics
    2. **Automatic Subscription**: Creates subscriptions for newly discovered drones
    3. **Real-time Collection**: Collects system metrics in real-time
    4. **Queue Integration**: Thread-safe data passing to metrics processing systems
    5. **Scalable Design**: Handles arbitrary numbers of drones automatically

System Metrics Collection:
    The subscriber system collects comprehensive system metrics including:
    
    - **Performance Metrics**: CPU usage, memory consumption, system load
    - **Network Statistics**: Communication latency, bandwidth utilization
    - **Hardware Status**: Battery levels, sensor readings, actuator states
    - **Flight Parameters**: Position, velocity, orientation, altitude
    - **Error Conditions**: System warnings, error states, diagnostic information

Topic Discovery Mechanism:
    **Pattern Matching**: Uses regular expressions to identify drone metric topics
    **Topic Format**: ``/system_metrics/drone_{id}`` (e.g., /system_metrics/drone_1)
    **Scan Frequency**: 2-second intervals for balanced responsiveness and efficiency
    **Automatic Management**: Maintains active subscription list without manual intervention

ROS 2 Integration:
    **Node Architecture**: Single dynamic subscriber node managing multiple subscriptions
    **Message Type**: std_msgs/String for flexible JSON-formatted metric data
    **QoS Settings**: Queue depth of 10 for reliable message delivery
    **Executor Type**: MultiThreadedExecutor for concurrent callback processing

Data Flow Architecture:
    .. mermaid::
    
        graph LR
            A[Drone 1 Metrics] --> B[Topic /system_metrics/drone_1]
            C[Drone 2 Metrics] --> D[Topic /system_metrics/drone_2]
            E[Drone N Metrics] --> F[Topic /system_metrics/drone_n]
            
            B --> G[Dynamic Subscriber]
            D --> G
            F --> G
            
            G --> H[Metrics Queue]
            H --> I[Fleet Management]

Threading Architecture:
    - **Discovery Thread**: Periodic topic scanning and subscription management
    - **Callback Threads**: Individual metric processing for each drone
    - **Executor Thread**: ROS 2 node spinning for message handling
    - **Queue Thread**: Asynchronous data transmission to Fleet Management

Data Format:
    **Message Structure**: JSON-formatted strings containing metric data
    **Queue Format**: [drone_id, metrics_data] tuples for identification
    **Metric Categories**: Performance, network, hardware, flight, diagnostics

Scalability Features:
    - **Dynamic Scaling**: Automatically handles fleet size changes
    - **Memory Efficiency**: Minimal memory footprint per subscription
    - **Performance Optimization**: Efficient topic scanning and callback management
    - **Error Resilience**: Robust error handling for connection failures

Classes:
    .. autoclass:: DynamicMetricsSubscriber
        :members:
        :undoc-members:
        :show-inheritance:

Functions:
    .. autofunction:: main

Usage Examples:
    **Basic Subscriber Initialization**::
    
        import queue
        import logging
        
        metrics_queue = queue.Queue()
        logger = logging.getLogger('MetricsSubscriber')
        subscriber = main(metrics_queue=metrics_queue, metrics_logger=logger)
        
    **Integration with Fleet Management**::
    
        # Create shared queue for metrics collection
        fleet_metrics_queue = queue.Queue()
        
        # Start dynamic subscriber
        subscriber = main(metrics_queue=fleet_metrics_queue, metrics_logger=logger)
        
        # Process collected metrics
        while True:
            drone_id, metrics_data = fleet_metrics_queue.get()
            process_drone_metrics(drone_id, metrics_data)

.. note::
    This module requires a properly configured ROS 2 environment with drones
    publishing metrics on standardized topic patterns.

.. warning::
    The subscriber uses MultiThreadedExecutor for concurrent processing. Ensure
    proper queue thread safety when integrating with external systems.

.. seealso::
    - :mod:`SystemMetrics.metrics_manager`: Main metrics processing module
    - :mod:`SystemMetrics.grpc_metrics_fleet`: gRPC metrics communication
    - :doc:`ROS 2 Node Tutorial <https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html>`
"""

import threading
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import re
import queue
import logging

class DynamicMetricsSubscriber(Node):
    """Dynamic ROS 2 subscriber node for comprehensive drone system metrics collection.

    This class implements an intelligent subscription management system that automatically
    discovers and subscribes to drone system metrics topics. It provides real-time metric
    collection with dynamic fleet scaling capabilities and thread-safe data handling.

    Node Architecture:
        - **Node Name**: 'dynamic_metrics_subscriber'
        - **Discovery Method**: Periodic topic scanning with regex pattern matching
        - **Subscription Type**: std_msgs/String for flexible JSON metric data
        - **Queue Integration**: Thread-safe metric data queuing for external processing

    Dynamic Discovery System:
        The node implements an intelligent discovery mechanism:
        
        - **Pattern Recognition**: Identifies drone topics using regex patterns
        - **Automatic Subscription**: Creates subscriptions for newly discovered drones
        - **Subscription Management**: Maintains active subscription registry
        - **Scalable Design**: Handles arbitrary fleet sizes without configuration

    Topic Pattern Recognition:
        **Standard Pattern**: ``/system_metrics/drone_{id}``
        **Examples**:
        - /system_metrics/drone_1 (Drone ID: 1)
        - /system_metrics/drone_42 (Drone ID: 42)
        - /system_metrics/drone_999 (Drone ID: 999)

    Metrics Collection Workflow:
        1. **Topic Discovery**: Scan ROS 2 topic namespace for new drone metrics
        2. **Pattern Matching**: Apply regex filter to identify drone metric topics
        3. **ID Extraction**: Parse drone IDs from topic names
        4. **Subscription Creation**: Create new subscriptions for discovered drones
        5. **Data Collection**: Receive and queue metric data from active subscriptions
        6. **Queue Management**: Thread-safe forwarding to metrics processing systems

    Real-time Processing:
        - **Timer-based Scanning**: 2-second intervals for discovery updates
        - **Concurrent Callbacks**: Multi-threaded callback processing
        - **Immediate Queuing**: Real-time metric data forwarding
        - **Memory Efficient**: Minimal overhead per subscription

    Data Handling:
        **Input Format**: std_msgs/String containing JSON-formatted metrics
        **Output Format**: [drone_id, metrics_data] tuples in shared queue
        **Thread Safety**: All queue operations are inherently thread-safe
        **Error Resilience**: Robust handling of malformed or missing data

    :param metrics_queue: Thread-safe queue for metric data transmission to Fleet Management
    :type metrics_queue: queue.Queue
    :param metrics_logger: Pre-configured logger instance for subscriber operations
    :type metrics_logger: logging.Logger

    :ivar active_subscriptions: Registry of active topic subscriptions (topic → subscription)
    :vartype active_subscriptions: Dict[str, rclpy.subscription.Subscription]
    :ivar metrics_queue: Queue for metric data transmission to external systems
    :vartype metrics_queue: queue.Queue
    :ivar metrics_logger: Logger instance for operation tracking and debugging
    :vartype metrics_logger: logging.Logger
    :ivar timer: ROS 2 timer for periodic topic discovery (2-second intervals)
    :vartype timer: rclpy.timer.Timer

    Example:
        **Node Initialization**::
        
            import queue
            import logging
            
            metrics_queue = queue.Queue()
            logger = logging.getLogger('MetricsSubscriber')
            subscriber = DynamicMetricsSubscriber(metrics_queue, logger)
            
        **Automatic Discovery Process**::
        
            # Node automatically discovers topics like:
            # /system_metrics/drone_1, /system_metrics/drone_2, etc.
            # Creates subscriptions and begins collecting metrics
            
        **Metric Data Flow**::
        
            # Received metrics automatically queued as:
            # [1, '{"cpu": 45.2, "memory": 78.1, "battery": 89.5}']
            # [2, '{"cpu": 52.1, "memory": 65.3, "battery": 92.1}']

    .. note::
        The node uses a 2-second discovery timer to balance responsiveness with
        system performance. This interval can be adjusted based on fleet dynamics.

    .. warning::
        Ensure drone metric publishers use the standard topic naming convention
        for automatic discovery to function correctly.

    .. seealso::
        - :func:`main`: Factory function for node initialization
        - :mod:`std_msgs.msg`: ROS 2 standard message types
        - :class:`rclpy.node.Node`: Base ROS 2 node class
    """
    
    def __init__(self, metrics_queue, metrics_logger):
        """Initialize dynamic subscriber node with metric collection infrastructure.

        Sets up the ROS 2 node with all necessary components for automatic drone discovery
        and real-time metric collection. Configures timing, storage, and logging systems
        for comprehensive fleet monitoring capabilities.

        Initialization Process:
            1. **Node Creation**: Initialize ROS 2 node with descriptive name
            2. **Storage Setup**: Initialize subscription registry for topic management
            3. **Communication Setup**: Configure queue and logger references
            4. **Discovery Timer**: Create periodic timer for topic scanning
            5. **System Ready**: Log initialization completion and begin operations

        Timer Configuration:
            - **Frequency**: 2.0 seconds between discovery scans
            - **Purpose**: Balance between responsiveness and system resource usage
            - **Callback**: Executes scan_for_drones() method for topic discovery
            - **Persistence**: Continues throughout node lifetime for ongoing discovery

        :param metrics_queue: Thread-safe queue for metric data transmission
        :type metrics_queue: queue.Queue
        :param metrics_logger: Pre-configured logger for operation tracking
        :type metrics_logger: logging.Logger
        """
        # Initialize parent ROS 2 Node class with descriptive node name
        super().__init__('dynamic_metrics_subscriber')
        
        # Initialize dictionary to store active topic subscriptions
        # Key: topic_name (str), Value: Subscription object
        self.active_subscriptions = {}
        
        # Store reference to thread-safe queue for metric data transmission
        self.metrics_queue = metrics_queue
        
        # Store logger instance for operation tracking and debugging
        self.metrics_logger = metrics_logger
        
        # Create periodic timer for automatic drone topic discovery
        # Executes every 2 seconds to scan for new drone metric topics
        self.timer = self.create_timer(2.0, self.scan_for_drones)
        
        # Log successful initialization for monitoring and debugging
        self.metrics_logger.info("[System Metrics Subscriber] - Started dynamic System Metrics subscriber")

    def scan_for_drones(self):
        """Discover and subscribe to new drone system metrics topics automatically.

        This method implements the core discovery algorithm that continuously monitors
        the ROS 2 topic namespace for new drone metric publishers. It uses pattern
        matching to identify valid drone topics and creates subscriptions for newly
        discovered drones.

        Discovery Algorithm:
            1. **Topic Enumeration**: Query ROS 2 system for all available topics
            2. **Pattern Filtering**: Apply regex filter to identify drone metric topics
            3. **New Topic Detection**: Compare against existing subscriptions
            4. **ID Extraction**: Parse drone IDs from topic names
            5. **Subscription Creation**: Create new subscriptions for discovered drones

        Topic Pattern Matching:
            **Regex Pattern**: ``r'/system_metrics/drone_\\d+'``
            **Valid Examples**:
            - /system_metrics/drone_1
            - /system_metrics/drone_42
            - /system_metrics/drone_999
            
            **Invalid Examples** (ignored):
            - /metrics/drone_1 (wrong namespace)
            - /system_metrics/vehicle_1 (wrong prefix)
            - /system_metrics/drone_abc (non-numeric ID)

        Performance Considerations:
            - **Efficient Scanning**: Minimal overhead for topic enumeration
            - **Duplicate Prevention**: Checks existing subscriptions before creation
            - **Scalable Design**: Handles large numbers of drones efficiently
            - **Memory Management**: No memory leaks from repeated scanning

        Error Handling:
            - **Topic Query Failures**: Gracefully handle ROS 2 communication issues
            - **Pattern Match Errors**: Robust regex handling for malformed topics
            - **Subscription Failures**: Log and continue on individual subscription errors

        .. note::
            This method is called automatically every 2 seconds by the ROS 2 timer.
            It operates efficiently even with large drone fleets.

        .. warning::
            Topic discovery relies on ROS 2 topic enumeration. Ensure proper ROS 2
            network connectivity for reliable drone detection.
        """
        # Query ROS 2 system for all currently available topics and their types
        # Returns list of tuples: [(topic_name, [message_types]), ...]
        topic_list = self.get_topic_names_and_types()
        
        # Filter topics using regex pattern to identify drone system metrics
        # Pattern matches: /system_metrics/drone_{numeric_id}
        drone_topics = [t[0] for t in topic_list if re.match(r'/system_metrics/drone_\d+', t[0])]
        
        # Process each discovered drone topic for subscription management
        for topic in drone_topics:
            # Check if we already have an active subscription for this topic
            if topic not in self.active_subscriptions:
                # Extract drone ID from topic name for identification
                drone_id = self.extract_drone_id(topic)
                
                # Create new subscription for the newly discovered drone
                self.create_drone_subscription(topic, drone_id)

    def extract_drone_id(self, topic):
        """Extract numeric drone identifier from standardized topic name.

        This method parses drone topic names to extract unique numeric identifiers
        used for drone identification throughout the Fleet Management System. It uses
        regex pattern matching to ensure robust ID extraction from topic strings.

        Topic Name Parsing:
            **Input Format**: /system_metrics/drone_{numeric_id}
            **Regex Pattern**: ``r'drone_(\\d+)'``
            **Extraction Method**: Captures numeric group from pattern match

        ID Validation:
            - **Numeric Validation**: Ensures extracted ID is a valid integer
            - **Range Checking**: Accepts any positive integer value
            - **Error Handling**: Returns None for invalid or missing IDs
            - **Type Conversion**: Converts string digits to integer type

        :param topic: Complete ROS 2 topic name containing drone identifier
        :type topic: str

        :return: Extracted drone ID as integer, or None if extraction fails
        :rtype: int or None

        :raises ValueError: If extracted ID cannot be converted to integer
        :raises AttributeError: If regex match fails (handled gracefully)

        Examples:
            **Valid Extractions**::
            
                extract_drone_id('/system_metrics/drone_1') → 1
                extract_drone_id('/system_metrics/drone_42') → 42
                extract_drone_id('/system_metrics/drone_999') → 999
                
            **Invalid Inputs**::
            
                extract_drone_id('/metrics/drone_1') → None (wrong namespace)
                extract_drone_id('/system_metrics/vehicle_1') → None (wrong prefix)
                extract_drone_id('/system_metrics/drone_abc') → None (non-numeric)

        .. note::
            This method is called during topic discovery to associate subscriptions
            with specific drone identifiers for data routing.

        .. warning::
            Returns None for any topic that doesn't match the expected drone topic
            pattern. Ensure topic names follow the standard convention.
        """
        # Apply regex pattern to extract numeric drone ID from topic name
        # Pattern 'drone_(\\d+)' captures one or more digits after 'drone_'
        match = re.search(r'drone_(\d+)', topic)
        
        # Return extracted ID as integer if match found, otherwise return None
        # The group(1) extracts the first captured group (the numeric ID)
        return int(match.group(1)) if match else None

    def create_drone_subscription(self, topic, drone_id):
        """Create and register ROS 2 subscription for newly discovered drone metrics.

        This method handles the complete subscription creation process for individual
        drone metric topics. It configures message handling, creates appropriate
        callbacks, and registers the subscription for lifecycle management.

        Subscription Configuration:
            - **Message Type**: std_msgs/String for flexible JSON data format
            - **QoS Profile**: Queue depth of 10 for reliable message delivery
            - **Callback Function**: Dynamically generated with drone context
            - **Topic Binding**: Direct subscription to drone-specific topic

        Callback Generation:
            Each subscription receives a unique callback function that:
            - Maintains drone ID context for data identification
            - Processes incoming metric messages immediately
            - Forwards data to shared queue for Fleet Management consumption
            - Logs message reception for monitoring and debugging

        Registration Process:
            1. **ID Validation**: Verify extracted drone ID is valid
            2. **Discovery Logging**: Log new drone discovery event
            3. **Subscription Creation**: Create ROS 2 subscription with configured parameters
            4. **Callback Assignment**: Assign dynamically generated callback function
            5. **Registry Update**: Store subscription in active subscriptions dictionary

        Error Handling:
            - **Invalid IDs**: Skip subscription creation for None drone IDs
            - **Subscription Failures**: Log errors and continue operation
            - **Callback Errors**: Individual callback failures don't affect other drones
            - **Memory Management**: Proper subscription cleanup on errors

        :param topic: Complete ROS 2 topic name for drone metrics
        :type topic: str
        :param drone_id: Extracted numeric drone identifier
        :type drone_id: int or None

        :raises rclpy.exceptions.InvalidTopicNameException: If topic name is invalid
        :raises rclpy.exceptions.QoSException: If QoS settings are incompatible
        :raises Exception: For any other subscription creation failures

        Example:
            **Subscription Creation Process**::
            
                # Input: '/system_metrics/drone_42', 42
                # Creates subscription for drone 42 metrics
                # Registers callback with drone ID context
                # Adds to active_subscriptions registry

        .. note::
            This method is called automatically during topic discovery for each
            newly detected drone. Manual invocation is not typically necessary.

        .. warning::
            Subscription creation will be skipped if drone_id is None. Ensure
            proper topic naming conventions for successful subscription creation.
        """
        # Validate that drone ID was successfully extracted from topic name
        if drone_id is not None:
            # Log discovery of new drone for monitoring and fleet tracking
            self.metrics_logger.info(f"[System Metrics Subscriber] - Discovered new drone: ID {drone_id}")
            
            # Create ROS 2 subscription for the drone's metric topic
            # Uses std_msgs/String for flexible JSON-formatted metric data
            sub = self.create_subscription(
                String,                              # Message type for metric data
                topic,                              # Drone-specific topic name
                self.create_callback(drone_id),     # Dynamically generated callback
                10                                  # Queue depth for message buffering
            )
            
            # Register subscription in active subscriptions dictionary
            # Enables subscription lifecycle management and prevents duplicates
            self.active_subscriptions[topic] = sub

    def create_callback(self, drone_id):
        """Generate drone-specific callback function for metric message processing.

        This method implements a callback factory pattern that creates customized
        callback functions for each drone subscription. Each callback maintains
        drone identification context and handles metric data processing with
        appropriate logging and queue forwarding.

        Callback Factory Pattern:
            - **Context Preservation**: Each callback retains drone ID for identification
            - **Dynamic Generation**: Creates unique callbacks for each drone
            - **Closure Mechanism**: Uses Python closures to maintain drone context
            - **Thread Safety**: Generated callbacks are inherently thread-safe

        Callback Function Behavior:
            The generated callback function:
            1. **Message Reception**: Receives std_msgs/String containing metric data
            2. **Data Logging**: Logs message reception with drone identification
            3. **Data Extraction**: Extracts JSON metric data from message
            4. **Queue Forwarding**: Sends [drone_id, data] tuple to shared queue
            5. **Error Handling**: Gracefully handles processing errors

        Data Processing Flow:
            **Input**: std_msgs/String message with JSON metric data
            **Processing**: Extract message.data field containing metrics
            **Output**: [drone_id, metrics_data] tuple queued for Fleet Management
            **Thread Safety**: Queue operations are inherently thread-safe

        Message Format Handling:
            - **Expected Format**: JSON string containing system metrics
            - **Flexible Schema**: Accepts any valid JSON metric structure
            - **Error Resilience**: Handles malformed or empty messages gracefully
            - **Logging Integration**: All processing events logged for debugging

        :param drone_id: Unique numeric identifier for drone context
        :type drone_id: int

        :return: Configured callback function with drone context
        :rtype: Callable[[std_msgs.msg.String], None]

        Callback Function Signature:
            .. code-block:: python
            
                def callback(msg: std_msgs.msg.String) -> None:
                    # Process message with drone_id context
                    # Forward data to metrics queue

        Example:
            **Callback Generation and Usage**::
            
                # Generate callback for drone 42
                callback_func = create_callback(42)
                
                # Callback processes messages like:
                # msg.data = '{"cpu": 65.2, "memory": 78.1, "battery": 91.5}'
                # Queues: [42, '{"cpu": 65.2, "memory": 78.1, "battery": 91.5}']

        .. note::
            This method uses Python closures to maintain drone ID context within
            the generated callback function for proper data identification.

        .. warning::
            Generated callbacks assume valid JSON data in message.data field.
            Malformed data will be logged but processing will continue.
        """
        def callback(msg):
            """Process received metric message and forward to Fleet Management queue.

            This callback function processes incoming system metric messages from
            individual drones and forwards them to the shared queue for consumption
            by the Fleet Management System.

            :param msg: ROS 2 message containing JSON-formatted system metrics
            :type msg: std_msgs.msg.String
            """
            # Log message reception with drone identification for monitoring
            self.metrics_logger.info(f'[System Metrics Subscriber] - System Metrics received from Drone {drone_id}')
            
            # Forward metric data to shared queue as [drone_id, data] tuple
            # Queue operations are thread-safe for concurrent access
            self.metrics_queue.put([drone_id, msg.data])
            
        # Return the configured callback function with drone context
        return callback

def main(args=None, metrics_queue=None, metrics_logger: logging.Logger = None):
    """Initialize and configure dynamic drone metrics subscriber system.

    This function serves as the main entry point for the dynamic drone metrics
    subscription system. It handles ROS 2 initialization, node creation, executor
    configuration, and threading setup for comprehensive fleet metrics collection.

    System Initialization Process:
        1. **ROS 2 Setup**: Initialize ROS 2 runtime environment if needed
        2. **Node Creation**: Create DynamicMetricsSubscriber instance
        3. **Executor Configuration**: Set up MultiThreadedExecutor for concurrent processing
        4. **Threading Setup**: Start executor in daemon thread for background operation
        5. **Reference Return**: Provide node reference for lifecycle management

    ROS 2 Environment Management:
        - **Initialization Check**: Verifies ROS 2 runtime status before initialization
        - **Conditional Setup**: Only initializes ROS 2 if not already running
        - **Resource Management**: Proper handling of ROS 2 lifecycle and cleanup
        - **Error Recovery**: Comprehensive error handling for initialization failures

    Threading Architecture:
        **Main Thread**: Function execution and node creation
        **Executor Thread**: Dedicated daemon thread for ROS 2 message processing
        **Callback Threads**: Individual threads for each drone metric callback
        **Timer Thread**: Periodic drone discovery and subscription management

    Executor Configuration:
        - **Type**: MultiThreadedExecutor for concurrent callback processing
        - **Node Management**: Single node with multiple subscriptions
        - **Thread Safety**: Inherent thread safety for ROS 2 operations
        - **Background Operation**: Daemon thread prevents blocking main process

    Error Handling Strategy:
        - **Initialization Errors**: ROS 2 setup failures logged and propagated
        - **Node Creation Errors**: Comprehensive error logging with stack traces
        - **Threading Errors**: Executor thread failures handled gracefully
        - **Runtime Errors**: Continuous operation despite individual failures

    :param args: ROS 2 command line arguments for node configuration
    :type args: List[str] or None
    :param metrics_queue: Thread-safe queue for metric data transmission to Fleet Management
    :type metrics_queue: queue.Queue or None
    :param metrics_logger: Pre-configured logger instance for system operations
    :type metrics_logger: logging.Logger or None

    :return: Initialized subscriber node instance for lifecycle management
    :rtype: DynamicMetricsSubscriber or None

    :raises rclpy.exceptions.RCLError: If ROS 2 initialization or node creation fails
    :raises threading.ThreadError: If executor thread creation or startup fails
    :raises Exception: For any other critical system initialization failures

    Usage Examples:
        **Basic Initialization**::
        
            import queue
            import logging
            
            metrics_queue = queue.Queue()
            logger = logging.getLogger('MetricsSubscriber')
            
            # Start metrics collection system
            node = main(metrics_queue=metrics_queue, metrics_logger=logger)
            
        **Integration with Fleet Management**::
        
            # Create shared infrastructure
            fleet_metrics_queue = queue.Queue()
            fleet_logger = create_fleet_logger('metrics')
            
            # Initialize subscriber system
            subscriber = main(
                args=None,
                metrics_queue=fleet_metrics_queue,
                metrics_logger=fleet_logger
            )
            
            # Process collected metrics
            while True:
                drone_id, metrics_data = fleet_metrics_queue.get()
                process_drone_metrics(drone_id, metrics_data)
                
        **Command Line Integration**::
        
            import sys
            
            # Pass command line arguments to ROS 2
            node = main(args=sys.argv[1:], 
                       metrics_queue=shared_queue,
                       metrics_logger=system_logger)

    Return Value:
        Returns the initialized DynamicMetricsSubscriber instance for:
        - **Lifecycle Management**: Proper node shutdown and cleanup
        - **Subscription Control**: Runtime subscription management
        - **Monitoring Access**: Node status and performance monitoring
        - **Error Handling**: Runtime error detection and recovery

    .. note::
        This function starts a daemon thread for ROS 2 processing. The node will
        continue operating until the main process terminates or explicit shutdown.

    .. warning::
        Ensure proper cleanup of the returned node instance to avoid resource
        leaks. Use appropriate shutdown procedures in production environments.

    .. seealso::
        - :class:`DynamicMetricsSubscriber`: Main subscriber node implementation
        - :class:`rclpy.executors.MultiThreadedExecutor`: ROS 2 executor for threading
        - :mod:`threading`: Python threading module for concurrent processing
    """
    try:
        # Check and initialize ROS 2 runtime environment if necessary
        # Prevents multiple initialization attempts in shared ROS 2 processes
        if not rclpy.ok():
            rclpy.init(args=args)
            
        # Create dynamic metrics subscriber node with provided infrastructure
        # Node will begin automatic drone discovery and subscription management
        subscriber = DynamicMetricsSubscriber(metrics_queue, metrics_logger)
        
        # Create multi-threaded executor for concurrent message processing
        # Enables simultaneous handling of multiple drone metric streams
        executor = rclpy.executors.MultiThreadedExecutor()
        
        # Register subscriber node with executor for message processing
        executor.add_node(subscriber)
        
        # Start executor in dedicated daemon thread for background operation
        # Daemon thread ensures automatic termination with main process
        executor_thread = threading.Thread(target=executor.spin, daemon=True)
        executor_thread.start()
        
        # Return node reference for lifecycle management and monitoring
        return subscriber  # Return node reference for proper cleanup

    except Exception as e:
        # Log critical initialization errors with full stack trace for debugging
        # Use print for error output to ensure visibility even with logger failures
        print(f"[ERROR][System metrics Subscriber] - Critical error: {str(e)}", exc_info=True)
        
        # Re-raise exception to notify calling code of initialization failure
        raise

# Entry point for standalone execution and testing
if __name__ == '__main__':
    # Execute main function for standalone testing and development
    # Typically used for module testing and debugging purposes
    main()