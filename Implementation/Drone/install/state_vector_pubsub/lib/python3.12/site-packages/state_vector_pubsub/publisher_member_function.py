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

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from src.state_vector_pubsub.state_vector_pubsub.state_vector import StateVector
from rclpy.executors import MultiThreadedExecutor
import threading
import queue  # Added import for queue.Empty exception

class StateVectorPublisher(Node):
    def __init__(self, drone_id, drone_logger, topic_queue):
        # Unique node name using drone_id
        super().__init__(f'state_vector_publisher_{drone_id}')
        self.drone_logger = drone_logger
        self.topic_queue = topic_queue
        self.msg = String()
        
        # Create a topic per drone using drone_id in the topic name
        self.publisher_ = self.create_publisher(String, f'state_vector/drone_{drone_id}', 10)
        
        self.timer_period = 2  # seconds
        self.timer = self.create_timer(self.timer_period, self.timer_callback)
        
        self.drone_logger.info(f" - State vector publisher started.")

    def timer_callback(self):
        state_vector = None

        # Retrieve all messages, keeping the last one
        while True:
            try:
                state_vector = self.topic_queue.get_nowait()
            except queue.Empty:  # Or the specific exception your queue uses
                break
            
        if state_vector:
            self.msg = String()
            self.msg.data = str(state_vector)

        # Publish the message (previous or new)
        self.publisher_.publish(self.msg)
        self.drone_logger.info(f'[State Vector] - {self.msg}')
    

def main(args=None, drone_id=0, drone_logger=None, topic_queue=None):
    rclpy.init(args=args)
    
    executor = MultiThreadedExecutor()

    publisher = StateVectorPublisher(drone_id, drone_logger, topic_queue)

    executor.add_node(publisher)

    # Start the executor in a separate thread
    executor_thread = threading.Thread(target=executor.spin, daemon=True)
    executor_thread.start()

    try:
        while rclpy.ok():
            # Keep the main thread alive
            executor_thread.join(0.1)
    except KeyboardInterrupt:
        drone_logger.info(f"[State Vector] - Ctrl+C received, shutting down...")
    finally:
        # Cleanup
        executor.shutdown()
        publisher.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()