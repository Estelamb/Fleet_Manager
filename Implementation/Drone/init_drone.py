"""
This module implements the core functionality for a ROS 2-based drone control system, featuring:
- Multi-threaded ROS 2 node execution
- Concurrent command action server
- State vector publication
- Rotating log management
- Graceful shutdown handling

.. note::
    Requires ROS 2 Humble or newer with rclpy installation
    Uses custom interface definitions from commands_action_interface
"""

import logging
import argparse
import queue
import sys
import os

from concurrent_log_handler import ConcurrentRotatingFileHandler

from src.commands_action_interface.src.commands_action_server import CommandsActionServer
from src.state_vector_pubsub.state_vector_pubsub.state_vector import start_state_vector
from src.state_vector_pubsub.state_vector_pubsub.publisher_member_function import StateVectorPublisher

import rclpy
from rclpy.executors import MultiThreadedExecutor

def main(drone_id):
    """Main drone control system initialization and execution flow.

    Orchestrates:
    1. Logger configuration
    2. Queue initialization
    3. State vector subsystem startup
    4. ROS 2 node creation and lifecycle management
    5. Multi-threaded executor operation

    :param drone_id: Unique numeric identifier for the drone
    :type drone_id: int
    :raises SystemExit: On critical initialization failure
    :raises KeyboardInterrupt: On user-initiated shutdown

    Example:
        Start drone 5::
        
            $ python drone_control.py --drone_id 5
    """
    try:       
        # Create logger
        drone_logger = create_logger(f'Drone {drone_id}', f'Logs/drone{drone_id}.log')
        
        # Create queues
        action_queue = queue.Queue()
        topic_queue = queue.Queue()
        
        # Start State Vector
        start_state_vector(vehicle_id=drone_id, longitude=40.073670, latitude=-4.612044,
                           action_queue=action_queue, topic_queue=topic_queue)

        # Initialize ROS2 context
        rclpy.init()

        # Create nodes
        action_server = CommandsActionServer(drone_id=drone_id, drone_logger=drone_logger,
                           action_queue=action_queue)
        state_publisher = StateVectorPublisher(drone_id=drone_id, drone_logger=drone_logger,
                           topic_queue=topic_queue)

        # Create and configure executor
        executor = MultiThreadedExecutor()
        executor.add_node(action_server)
        executor.add_node(state_publisher)

        try:
            drone_logger.info(" - Spinning executor to run both nodes...")
            executor.spin()  # This will handle both nodes' callbacks
        except KeyboardInterrupt:
            drone_logger.info(" - Ctrl+C received, shutting down.")
        finally:
            # Cleanup
            executor.shutdown()
            action_server.destroy_node()
            state_publisher.destroy_node()
            rclpy.try_shutdown()

    except Exception as e:
        logging.error(f" - Critical error in main: {str(e)}", exc_info=True)
        sys.exit(1)
        


def create_logger(logger_name: str, log_file: str) -> logging.Logger:
    """Configure concurrent-safe logger with rotating file handler.

    :param logger_name: Namespace for logger instance
    :type logger_name: str
    :param log_file: Path for log file storage
    :type log_file: str
    :return: Configured logger instance
    :rtype: logging.Logger
    :raises IOError: If log file initialization fails

    Configuration Details:
    - 1MB log rotation with 5 backups
    - Concurrent write safety
    - Unified console/file formatting
    - UTC timestamp formatting
    """
    try:
        # Create a custom logger
        logger = logging.getLogger(logger_name)

        # Set level
        logger.setLevel(logging.INFO)

        # Create a file handler
        file_handler = ConcurrentRotatingFileHandler(log_file, maxBytes=1000000, backupCount=5)

        # Create a console handler
        console_handler = logging.StreamHandler()

        # Set formatter
        formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s]%(message)s')

        # Attach formatter to handlers
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Attach handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger
    except Exception as e:
        print(f"Error creating logger {logger_name}: {str(e)}")
        raise


if __name__ == "__main__":
    """Command-line interface entry point.
    
    Usage Examples:
        Basic operation:
            python drone_control.py --drone_id 1
        
        Multiple drones:
            parallel --linebuffer python drone_control.py --drone_id ::: {1..10}
    """
    parser = argparse.ArgumentParser(description='Drone Control System')
    parser.add_argument('--drone_id', type=int, required=True,
                       help='ID of the drone (e.g., 1, 2)')
    args = parser.parse_args()
    
    try:
        main(args.drone_id)
    except Exception as e:
        logging.error(f"Unhandled exception: {str(e)}", exc_info=True)
        sys.exit(1)