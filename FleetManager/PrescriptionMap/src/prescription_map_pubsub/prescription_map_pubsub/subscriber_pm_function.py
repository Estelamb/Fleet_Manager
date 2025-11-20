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
Dynamic Drone Prescription Map Subscriber Module
================================================

This module provides a dynamic ROS2 subscriber for receiving prescription map (PM) 
data from multiple drone vehicles in the agricultural fleet management system. It
automatically discovers new drone topics and creates dedicated subscriptions for
real-time prescription map data collection.

The module implements a scalable subscription system that can handle an arbitrary
number of drones joining and leaving the fleet dynamically, without requiring
manual configuration or restart of the subscription service.

Key Features:
    - Dynamic discovery of new drone prescription map topics
    - Automatic subscription creation for newly detected drones
    - Thread-safe integration with prescription map processing pipeline
    - Regular expression-based topic pattern matching
    - Multi-threaded ROS2 executor for concurrent message processing
    - Robust message parsing with fallback mechanisms
    - Integration with fleet-wide prescription map management

Architecture:
    The module follows a dynamic subscription pattern where:
    - A timer-based scanner discovers new drone topics periodically
    - Individual subscriptions are created for each detected drone
    - Message callbacks process and forward PM data to the fleet manager
    - Thread-safe execution ensures concurrent processing capability

Topic Pattern:
    Drone topics follow the pattern: ``/prescription_map/drone_{ID}``
    where {ID} is a numeric identifier for each drone in the fleet.

Usage Example:
    ::

        import logging
        from Logs.create_logger_fleet import create_logger
        
        # Create configured logger
        pm_logger = create_logger('pm_subscriber', logging.INFO)
        
        # Start dynamic PM subscriber (non-blocking)
        subscriber = main(pm_logger=pm_logger)

Author: Fleet Management System
Date: 2025

.. note::
    This module requires:
    - ROS2 (Robot Operating System 2) environment
    - rclpy for Python ROS2 integration
    - std_msgs for ROS2 message types
    - PrescriptionMap.pm_manager_fleet for data processing
    
.. warning::
    The subscriber runs in daemon threads. Ensure proper application
    lifecycle management for graceful shutdowns in production deployments.
"""

import ast
import json
import queue
import threading
import time
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import re
import logging

from PrescriptionMap.pm_manager_fleet import handle_received


class DynamicPMSubscriber(Node):
    """
    Dynamic ROS2 subscriber for drone prescription map topics.
    
    This class implements a dynamic subscription system that automatically discovers
    and subscribes to prescription map topics from drone vehicles. It maintains
    active subscriptions for all detected drones and processes incoming prescription
    map data in real-time.
    
    The subscriber uses a timer-based discovery mechanism to periodically scan for
    new drone topics, ensuring that newly deployed drones are automatically
    integrated into the subscription system without manual intervention.
    
    Key Capabilities:
    - Automatic topic discovery using regex pattern matching
    - Dynamic subscription management for scalable drone fleets
    - Message parsing with robust error handling and fallback mechanisms
    - Integration with prescription map validation and processing pipeline
    - Thread-safe operation for concurrent message processing
    
    Attributes:
        active_subscriptions (dict): Registry of active topic subscriptions
                                   mapped by topic name to subscription objects
        pm_logger: Configured logger instance for operation tracking and debugging
        timer: ROS2 timer for periodic drone topic discovery
        
    Example:
        ::
        
            # Subscriber is typically created by the main() function
            subscriber = DynamicPMSubscriber(pm_logger)
            # Discovery and subscription happen automatically
            
    Note:
        The discovery timer runs every 2 seconds to balance responsiveness
        with system resource usage. This interval can be adjusted based on
        deployment requirements.
        
    See Also:
        :mod:`PrescriptionMap.pm_manager_fleet`: PM data processing backend
        :class:`rclpy.node.Node`: Base ROS2 node class
    """
    
    def __init__(self, pm_logger):
        """
        Initialize the dynamic prescription map subscriber node.
        
        Sets up the ROS2 node with automatic topic discovery capabilities and
        initializes the subscription management system for drone prescription
        map topics.
        
        Args:
            pm_logger: Configured logger instance for tracking subscription
                      operations, drone discovery, and message processing.
                      Should be properly configured with appropriate log levels
                      and output handlers.
                      
        Example:
            ::
            
                import logging
                pm_logger = logging.getLogger('pm_subscriber')
                pm_logger.setLevel(logging.INFO)
                subscriber = DynamicPMSubscriber(pm_logger)
        """
        super().__init__('dynamic_pm_subscriber')
        self.active_subscriptions = {}  # Registry of active topic subscriptions
        self.pm_logger = pm_logger
        
        # Set up periodic discovery timer (every 2 seconds)
        self.timer = self.create_timer(2.0, self.scan_for_drones)
        self.pm_logger.info("[PM Subscriber] - Started dynamic PM subscriber")

    def scan_for_drones(self):
        """
        Discover and subscribe to new drone prescription map topics.
        
        This method performs periodic scanning of available ROS2 topics to discover
        new drone prescription map publishers. It uses regex pattern matching to
        identify topics that follow the expected drone PM topic naming convention
        and creates subscriptions for newly detected drones.
        
        Discovery Process:
        1. Retrieve all available topics from the ROS2 topic list
        2. Filter topics using regex pattern for drone PM topics
        3. Check against existing subscriptions to identify new drones
        4. Create subscriptions for newly discovered drone topics
        
        Topic Pattern Matching:
            Matches topics with pattern: ``/prescription_map/drone_{numeric_id}``
            
        Example Topics:
            - ``/prescription_map/drone_1``
            - ``/prescription_map/drone_42``
            - ``/prescription_map/drone_101``
            
        Note:
            This method is called automatically by the ROS2 timer every 2 seconds.
            The scanning frequency balances discovery responsiveness with system
            resource usage.
            
        Warning:
            Topic discovery depends on ROS2 topic publication. Drones must be
            actively publishing or have published at least once to be discovered.
        """
        # Get all available topics from ROS2 system
        topic_list = self.get_topic_names_and_types()
        
        # Filter for drone PM topics using regex pattern matching
        drone_topics = [t[0] for t in topic_list if re.match(r'/prescription_map/drone_\d+', t[0])]
        
        # Create subscriptions for newly discovered drones
        for topic in drone_topics:
            if topic not in self.active_subscriptions:
                drone_id = self.extract_drone_id(topic)
                self.create_drone_subscription(topic, drone_id)

    def extract_drone_id(self, topic):
        """
        Extract numeric drone identifier from topic name.
        
        This method parses the drone topic name using regex to extract the
        numeric drone identifier. The identifier is used for message routing
        and subscription management throughout the system.
        
        Args:
            topic (str): Full topic name in format '/prescription_map/drone_{id}'
            
        Returns:
            int or None: Numeric drone identifier if successfully extracted,
                        None if the topic name doesn't match the expected pattern
                        
        Example:
            ::
            
                # Extract ID from valid topic
                drone_id = self.extract_drone_id('/prescription_map/drone_42')
                print(drone_id)  # Output: 42
                
                # Handle invalid topic
                drone_id = self.extract_drone_id('/invalid/topic')
                print(drone_id)  # Output: None
                
        Note:
            The method uses regex group matching to reliably extract the
            numeric portion from the topic name, ensuring robust parsing
            even with varied topic naming patterns.
        """
        # Use regex to extract drone ID from topic path
        match = re.search(r'drone_(\d+)', topic)
        return int(match.group(1)) if match else None

    def create_drone_subscription(self, topic, drone_id):
        """
        Create ROS2 subscription for a newly discovered drone topic.
        
        This method establishes a new ROS2 subscription for a specific drone's
        prescription map topic. It creates a dedicated callback function for
        the drone and registers the subscription in the active subscriptions
        registry for management and cleanup.
        
        Subscription Configuration:
        - Message type: std_msgs/String (JSON-encoded prescription map data)
        - Queue size: 10 messages (balanced for reliability and memory usage)
        - Callback: Dynamically created with drone context
        
        Args:
            topic (str): Full ROS2 topic name for the drone PM data
            drone_id (int): Numeric identifier for the drone
            
        Example:
            ::
            
                # Create subscription for newly discovered drone
                self.create_drone_subscription('/prescription_map/drone_5', 5)
                
        Note:
            The method only creates subscriptions for valid drone IDs (not None).
            Each subscription gets a unique callback function that includes the
            drone ID context for proper message routing.
            
        Warning:
            Duplicate subscriptions for the same topic are prevented by checking
            the active_subscriptions registry before creation.
        """
        # Create subscription only for valid drone IDs
        if drone_id is not None:
            self.pm_logger.info(f"[PM Subscriber] - Discovered new drone: ID {drone_id}")
            
            # Create ROS2 subscription with drone-specific callback
            sub = self.create_subscription(
                String,                          # Message type
                topic,                          # Topic name
                self.create_callback(drone_id), # Drone-specific callback
                10                              # Queue size
            )
            
            # Register subscription in active subscriptions registry
            self.active_subscriptions[topic] = sub

    def create_callback(self, drone_id):
        """
        Generate prescription map callback function with drone context.
        
        This method creates a closure that captures the drone ID context and
        returns a callback function for processing prescription map messages
        from that specific drone. The callback handles message parsing,
        validation, and forwarding to the prescription map processing pipeline.
        
        Message Processing Pipeline:
        1. Parse incoming JSON/Python data structures
        2. Validate message format and content structure
        3. Format message for prescription map manager
        4. Forward to handle_received for processing
        5. Log processing status and errors
        
        Args:
            drone_id (int): Numeric identifier for the drone that will use this callback
            
        Returns:
            function: Callback function configured for the specific drone that
                     accepts ROS2 String messages and processes PM data
                     
        Example:
            ::
            
                # Create callback for drone 5
                callback_func = self.create_callback(5)
                
                # Callback is used internally by ROS2 subscription
                # and handles messages automatically
                
        Note:
            The callback uses a fallback parsing mechanism, attempting JSON
            parsing first, then falling back to ast.literal_eval for Python
            literal structures.
            
        Warning:
            Message parsing failures are logged but do not crash the callback.
            Invalid message formats are rejected with appropriate error logging.
        """
        
        def callback(msg):
            """
            Process prescription map message from a specific drone.
            
            This inner function processes incoming prescription map messages,
            handling data parsing, validation, and forwarding to the fleet
            management system. It implements robust error handling to ensure
            system stability even with malformed messages.
            """
            try:
                self.pm_logger.info(f'[PM Subscriber] - PM received from Drone {drone_id}')
                
                # Attempt to parse message content with fallback mechanisms
                try:
                    # Primary parsing: JSON format
                    content = json.loads(msg.data)
                except json.JSONDecodeError:
                    try:
                        # Fallback parsing: Python literal evaluation
                        content = ast.literal_eval(msg.data)
                    except Exception as e:
                        self.pm_logger.error(f"[PM Subscriber] - Error parsing message: {str(e)}")
                        return

                # Validate that parsed content is a dictionary structure
                if not isinstance(content, dict):
                    self.pm_logger.error(f"[PM Subscriber] - Parsed message is not a dict: {content}")
                    return

                # Format message for prescription map manager processing
                parsed_msg = {
                    'type': 'Received',
                    'vehicle_id': drone_id,
                    'content': content,
                    'filename': content.get('filename', f"drone_{drone_id}_pm")
                }

                # Forward processed message to prescription map handler
                handle_received(parsed_msg.get('vehicle_id'), parsed_msg, self.pm_logger)
                self.pm_logger.info(f"[PM Subscriber] - PM data added to queue for Drone {drone_id}")
                
            except Exception as e:
                self.pm_logger.error(f"[PM Subscriber] - Error processing message: {str(e)}")
            
        return callback


def main(args=None, pm_logger:logging.Logger =None):
    """
    Initialize and run the dynamic drone prescription map subscriber.
    
    This function sets up and starts the complete ROS2 subscription system for
    receiving prescription map data from multiple drones. It initializes the
    ROS2 context, creates the dynamic subscriber node, and configures a
    multi-threaded executor for concurrent message processing.
    
    System Configuration:
    - ROS2 context initialization (if not already initialized)
    - Dynamic PM subscriber node creation
    - Multi-threaded executor setup for concurrent processing
    - Daemon thread execution for non-blocking operation
    
    Threading Model:
    - Main thread: Returns immediately after setup
    - Daemon thread: Runs ROS2 executor until main process exits
    - Multi-threaded executor: Handles concurrent message callbacks
    
    Args:
        args (list, optional): Command-line arguments for ROS2 initialization.
                              Defaults to None for standard initialization.
        pm_logger (logging.Logger, optional): Configured logger instance for
                                            tracking subscription operations.
                                            Must be provided for proper logging.
                                            
    Returns:
        DynamicPMSubscriber: The initialized subscriber node instance for
                           external reference and management
                           
    Example:
        ::
        
            import logging
            from Logs.create_logger_fleet import create_logger
            
            # Create configured logger
            pm_logger = create_logger('pm_subscriber', logging.INFO)
            
            # Start subscriber (non-blocking)
            subscriber = main(pm_logger=pm_logger)
            
            # Main application continues...
            print("PM subscriber started in background")
            
    Note:
        The function returns immediately after starting the daemon thread.
        The ROS2 subscriber will continue running in the background until
        the main process exits.
        
    Warning:
        ROS2 context initialization is handled automatically, but proper
        ROS2 environment setup is required. The executor runs in a daemon
        thread and will be terminated when the main process exits.
        
    Raises:
        Exception: Critical errors during initialization are logged and re-raised
                  to ensure proper error handling by the calling code
        SystemExit: May be raised if ROS2 initialization fails
        
    See Also:
        :class:`DynamicPMSubscriber`: The main subscriber node implementation
        :func:`rclpy.init`: ROS2 context initialization
        :class:`rclpy.executors.MultiThreadedExecutor`: Concurrent message processing
    """
    
    try:
        # Initialize ROS2 context if not already initialized
        if not rclpy.ok():
            rclpy.init(args=args)
            
        # Create dynamic PM subscriber node
        subscriber = DynamicPMSubscriber(pm_logger)
        
        # Create and configure multi-threaded executor for concurrent processing
        executor = rclpy.executors.MultiThreadedExecutor()
        executor.add_node(subscriber)
        
        # Start ROS2 executor in a separate daemon thread
        executor_thread = threading.Thread(target=executor.spin, daemon=True)
        executor_thread.start()
        
        return subscriber

    except Exception as e:
        pm_logger.critical(f"[PM Subscriber] - Critical error: {str(e)}", exc_info=True)
        raise


if __name__ == '__main__':
    main()