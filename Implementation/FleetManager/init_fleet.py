"""
System Initialization and Coordination Module

.. module:: main
    :synopsis: Core system initialization and component coordination

.. note::
    Manages:
    - Distributed system component initialization
    - Cross-service communication setup
    - Centralized logging configuration
    - Graceful error handling

Components:
    - Mission Management System
    - ROS2 Interface
    - Database Service
    - MQTT Communication
    - State Vector Management
    - REST API Interface
"""

import queue
import logging
import os
from typing import Optional
from concurrent_log_handler import ConcurrentRotatingFileHandler

# Component initializers
from MissionManager.grpc_mission_rest import start_grpc_mission_rest
from MissionManager.grpc_mission_vehicle import start_grpc_mission_vehicle
from MissionManager.grpc_mission_db import start_grpc_mission_db
from MissionManager.grpc_mission_mqtt import start_grpc_mission_mqtt
from REST.grpc_rest import start_grpc_rest
from ROS2.grpc_ros2 import start_grpc_ros2
from Database.grpc_db import start_grpc_db
from MQTT.grpc_mqtt import start_grpc_mqtt
from MQTT.tb_manager import start_tb_manager
from Database.create_db import create_db
from StateVector.sv_manager import start_sv_manager
from StateVector.src.state_vector_pubsub.state_vector_pubsub.subscriber_member_function import main as start_sv_subs
from REST import rest_server


def main() -> None:
    """Orchestrates system initialization and component startup.

    Initialization Sequence:
    1. Configure component-specific loggers
    2. Initialize inter-service communication queues
    3. Start mission management subsystems
    4. Launch ROS2 interface
    5. Initialize database services
    6. Configure MQTT communication
    7. Start state vector management
    8. Launch REST API interface

    :raises SystemError: If critical initialization failure occurs
    """
    try:
        # Configure logging subsystems
        loggers = initialize_loggers()
        if not loggers:
            raise RuntimeError("Logger initialization failed")

        # Initialize core components
        initialize_mission_system(loggers['mission'])
        initialize_ros2_system(loggers['ros2'])
        initialize_database_system(loggers['db'])
        initialize_mqtt_system(loggers['mqtt'])
        initialize_state_vector_system(loggers['sv'])
        initialize_rest_system(loggers['rest'])

    except Exception as e:
        logging.critical(f"System initialization failed: {str(e)}", exc_info=True)
        raise SystemError("Critical startup failure") from e


def initialize_loggers() -> Optional[dict]:
    """Configures component-specific logging systems.

    :return: Dictionary of configured loggers or None if failed
    """
    try:
        return {
            'rest': create_logger('REST', 'Logs/rest.log'),
            'mission': create_logger('MISSION', 'Logs/mission_manager.log'),
            'ros2': create_logger('ROS2', 'Logs/ros2.log'),
            'db': create_logger('DB', 'Logs/database.log'),
            'mqtt': create_logger('MQTT', 'Logs/mqtt.log'),
            'sv': create_logger('SV', 'Logs/state_vector.log')
        }
    except Exception as e:
        logging.error(f"Logger configuration failed: {str(e)}", exc_info=True)
        return None


def initialize_mission_system(mission_logger: logging.Logger) -> None:
    """Initializes mission management subsystem.

    :param mission_logger: Configured mission logger instance
    """
    try:
        queues = {
            'send_rest': queue.Queue(),
            'send_vehicle': queue.Queue(),
            'receive_vehicle': queue.Queue(),
            'send_db': queue.Queue(),
            'receive_db': queue.Queue(),
            'send_mqtt': queue.Queue()
        }

        start_grpc_mission_rest(
            queues['send_vehicle'],
            queues['receive_vehicle'],
            queues['send_db'],
            queues['receive_db'],
            queues['send_mqtt'],
            queues['send_rest'],
            mission_logger
        )
        start_grpc_mission_vehicle(queues['send_vehicle'], queues['receive_vehicle'], mission_logger)
        start_grpc_mission_db(queues['send_db'], queues['receive_db'], mission_logger)
        start_grpc_mission_mqtt(queues['send_mqtt'], mission_logger)
        
    except Exception as e:
        mission_logger.critical(f"Mission system initialization failed: {str(e)}", exc_info=True)
        raise


def initialize_ros2_system(ros2_logger: logging.Logger) -> None:
    """Initializes ROS2 communication interface.
    
    :param ros2_logger: Configured ROS2 logger instance
    """
    try:
        ros2_action_queue = queue.Queue()
        start_grpc_ros2(ros2_action_queue, ros2_logger)
    except Exception as e:
        ros2_logger.critical(f"ROS2 initialization failed: {str(e)}", exc_info=True)
        raise


def initialize_database_system(db_logger: logging.Logger) -> None:
    """Initializes database subsystem.
    
    :param db_logger: Configured database logger instance
    """
    try:
        create_db(db_logger)
        start_grpc_db(db_logger)
    except Exception as e:
        db_logger.critical(f"Database initialization failed: {str(e)}", exc_info=True)
        raise


def initialize_mqtt_system(mqtt_logger: logging.Logger) -> None:
    """Configures MQTT communication layer.
    
    :param mqtt_logger: Configured MQTT logger instance
    """
    try:
        data_to_tb = queue.Queue()
        start_grpc_mqtt(data_to_tb, mqtt_logger)
        start_tb_manager(data_to_tb, mqtt_logger)
    except Exception as e:
        mqtt_logger.critical(f"MQTT initialization failed: {str(e)}", exc_info=True)
        raise


def initialize_state_vector_system(sv_logger: logging.Logger) -> None:
    """Initializes state vector management.
    
    :param sv_logger: Configured state vector logger instance
    """
    try:
        receive_sv_queue = queue.Queue()
        start_sv_manager(receive_sv_queue, sv_logger)
        start_sv_subs(receive_sv_queue=receive_sv_queue, sv_logger=sv_logger)
    except Exception as e:
        sv_logger.critical(f"State Vector initialization failed: {str(e)}", exc_info=True)
        raise


def initialize_rest_system(rest_logger: logging.Logger) -> None:
    """Launches REST API interface.
    
    :param rest_logger: Configured REST logger instance
    """
    try:
        start_grpc_rest(rest_logger)
        rest_server.main()
    except Exception as e:
        rest_logger.critical(f"REST initialization failed: {str(e)}", exc_info=True)
        raise


def create_logger(logger_name: str, log_file: str) -> logging.Logger:
    """Configures a component-specific logger instance.

    :param logger_name: Identifier for the logger
    :param log_file: Path to log file
    :return: Configured logger instance
    :raises IOError: If log file cannot be created
    """
    try:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)

        handlers = [
            ConcurrentRotatingFileHandler(
                log_file,
                maxBytes=1_000_000,
                backupCount=5,
                encoding='utf-8'
            ),
            logging.StreamHandler()
        ]

        formatter = logging.Formatter('[%(asctime)s] - [%(name)s][%(levelname)s]%(message)s')
        for handler in handlers:
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger
    except IOError as e:
        logging.error(f"Failed to create log file {log_file}: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"Logger {logger_name} configuration failed: {str(e)}")
        raise


if __name__ == "__main__":
    """Main entry point with top-level exception handling."""
    try:
        main()
    except KeyboardInterrupt:
        print("\nSystem shutdown initiated by user")
    except Exception as e:
        logging.critical(f"Unhandled exception in main process: {str(e)}", exc_info=True)
        raise SystemExit(1) from e