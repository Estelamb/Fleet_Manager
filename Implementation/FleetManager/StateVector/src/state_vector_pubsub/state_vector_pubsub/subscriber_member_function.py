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
Dynamic Drone State Vector Subscriber Module

.. note::
    Features:
    - Automatic discovery of new drone topics
    - Thread-safe queue integration for state vector data
    - Regular expression-based topic matching
    - Multi-threaded ROS 2 executor
"""

import threading
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import re
import queue
import logging

class DynamicDroneSubscriber(Node):
    """Dynamic subscriber for drone state vector topics.

    :param receive_sv_queue: Thread-safe queue for state vector data
    :param sv_logger: Configured logger instance
    """
    
    def __init__(self, receive_sv_queue, sv_logger):
        """Initialize dynamic subscriber node."""
        super().__init__('dynamic_drone_subscriber')
        self.active_subscriptions = {}
        self.receive_sv_queue = receive_sv_queue
        self.sv_logger = sv_logger
        
        # Check for new drones every 2 seconds
        self.timer = self.create_timer(2.0, self.scan_for_drones)
        self.sv_logger.info("[SV Subscriber] - Started dynamic drone subscriber")

    def scan_for_drones(self):
        """Discover and subscribe to new drone topics.
        
        .. note::
            Scans all ROS 2 topics every SCAN_INTERVAL seconds
            Matches using predefined TOPIC_PATTERN
        """
        # Get all available topics
        topic_list = self.get_topic_names_and_types()
        
        # Find all drone state vector topics
        drone_topics = [t[0] for t in topic_list if re.match(r'/state_vector/drone_\d+', t[0])]
        
        # Create subscriptions for new drones
        for topic in drone_topics:
            if topic not in self.active_subscriptions:
                drone_id = self.extract_drone_id(topic)
                self.create_drone_subscription(topic, drone_id)

    def extract_drone_id(self, topic):
        """Extract numeric drone ID from topic name.
        
        :return: Drone ID if valid format, None otherwise
        """
        # Extract numeric ID from topic name
        match = re.search(r'drone_(\d+)', topic)
        return int(match.group(1)) if match else None

    def create_drone_subscription(self, topic, drone_id):
        """Create subscription for a new drone topic."""
        if drone_id is not None:
            self.sv_logger.info(f"[SV Subscriber] - Discovered new drone: ID {drone_id}")
            sub = self.create_subscription(
                String,
                topic,
                self.create_callback(drone_id),
                10
            )
            self.active_subscriptions[topic] = sub

    def create_callback(self, drone_id):
        """Generate state vector callback with drone context.
        
        :param drone_id: Numeric drone identifier
        :return: Configured callback function
        """
        
        def callback(msg):
            self.sv_logger.info(f'[SV Subscriber] - State vector received from Drone {drone_id}')
            self.receive_sv_queue.put([drone_id, msg.data])
            
        return callback

def main(args=None, receive_sv_queue=None, sv_logger:logging.Logger =None):
    """Initialize and run dynamic drone subscriber.
    
    :param args: ROS 2 command line arguments
    :param receive_sv_queue: Thread-safe queue for state vectors
    :param sv_logger: Configured logger instance
    :return: Initialized node instance or None on failure
    
    :raises ROSError: If ROS 2 initialization fails
    
    Example:
        .. code-block:: python

            from queue import Queue
            import logging
            
            sv_queue = Queue()
            logger = logging.getLogger('SVSubscriber')
            node = main(receive_sv_queue=sv_queue, sv_logger=logger)
    """
    
    try:
        if not rclpy.ok():
            rclpy.init(args=args)
            
        subscriber = DynamicDroneSubscriber(receive_sv_queue, sv_logger)
        
        # Create and configure executor
        executor = rclpy.executors.MultiThreadedExecutor()
        executor.add_node(subscriber)
        
        # Start spinning in a separate thread
        executor_thread = threading.Thread(target=executor.spin, daemon=True)
        executor_thread.start()
        
        return subscriber  # Return node reference for proper cleanup

    except Exception as e:
        print(f"[ERROR][SV Subscriber] - Critical error: {str(e)}", exc_info=True)
        raise


if __name__ == '__main__':
    main()