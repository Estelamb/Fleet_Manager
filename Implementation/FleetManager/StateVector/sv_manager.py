"""
State Vector Management Module

.. note::
    Features:
    - Multi-service state vector distribution (Database, MQTT)
    - Thread-safe queue processing
    - Timestamp normalization
    - Comprehensive logging
"""

import threading
import time
import queue
import json
import logging
from typing import Optional, Dict, Any, Literal
from concurrent_log_handler import ConcurrentRotatingFileHandler

from StateVector.grpc_sv_db import run_sv_db_client
from StateVector.grpc_sv_mqtt import run_sv_mqtt_client

# Configuration constants
QUEUE_TIMEOUT = 0.1  # Seconds for queue polling
MAX_LOG_SIZE = 1_000_000  # 1MB per log file
LOG_BACKUP_COUNT = 5

class StateVectorManagerThread(threading.Thread):
    """Thread-based state vector processor and distributor.
    
    :param receive_sv_queue: Thread-safe queue for incoming state vectors
    :param sv_logger: Configured logger instance
    """
    
    def __init__(self, receive_sv_queue: queue.Queue, sv_logger: logging.Logger):
        super().__init__(daemon=True)
        self.receive_sv_queue = receive_sv_queue
        self.sv_logger = sv_logger
        
    def run(self) -> None:
        """Main processing loop for state vector management."""
        try:
            while True:
                self.process_queue()
        except Exception as e:
            self.sv_logger.critical(f" - Manager failure: {str(e)}", exc_info=True)
        finally:
            self.sv_logger.info(" - State vector manager shutdown")

    def process_queue(self) -> None:
        """Process messages from the state vector queue."""
        try:
            state_vector = self.receive_sv_queue.get(timeout=QUEUE_TIMEOUT)
            vehicle_id, raw_data = state_vector
            self.sv_logger.debug(f" - Processing state vector from vehicle {vehicle_id}")
            
            processed_data = self.process_data(raw_data)
            self.distribute_data(vehicle_id, processed_data)
            
        except queue.Empty:
            time.sleep(QUEUE_TIMEOUT)
        except json.JSONDecodeError as e:
            self.sv_logger.error(f" - Invalid JSON data: {str(e)}")
        except Exception as e:
            self.sv_logger.error(f" - Processing error: {str(e)}", exc_info=True)

    def process_data(self, raw_data: str) -> Dict[str, Any]:
        """Normalize and enhance incoming state vector data."""
        try:
            data = json.loads(raw_data.replace("'", '"'))
            data["time"] = time.strftime('%Y-%m-%d %H:%M:%S')
            return data
        except Exception as e:
            self.sv_logger.error(f" - Data processing failed: {str(e)}")
            raise

    def distribute_data(self, vehicle_id: int, data: Dict[str, Any]) -> None:
        """Distribute processed data to all downstream services."""
        self.send_to_service('DB', vehicle_id, data)
        self.send_to_service('MQTT', vehicle_id, data)

    def send_to_service(
        self,
        service: Literal['DB', 'MQTT'],
        vehicle_id: int,
        data: Dict[str, Any]
    ) -> None:
        """Format and send data to specified service."""
        try:
            if service == 'DB':
                message = json.dumps(['StateVector', data])
                run_sv_db_client(message, self.sv_logger)
            elif service == 'MQTT':
                message = json.dumps({
                    'type': 'StateVector',
                    'vehicle_id': vehicle_id,
                    'telemetry': data
                })
                run_sv_mqtt_client(message, self.sv_logger)
                
            self.sv_logger.info(f" - Sent to {service}: Vehicle {vehicle_id}")
        except Exception as e:
            self.sv_logger.error(f" - {service} send failed: {str(e)}", exc_info=True)


def start_sv_manager(
    receive_sv_queue: queue.Queue,
    sv_logger: logging.Logger
) -> StateVectorManagerThread:
    """Initialize and start state vector management thread.
    
    :param receive_sv_queue: Shared queue for state vector data
    :param sv_logger: Configured logger instance
    :return: Running manager thread instance
    """
    manager = StateVectorManagerThread(receive_sv_queue, sv_logger)
    manager.start()
    sv_logger.info(" - State vector manager started")
    return manager


def create_logger(logger_name: str, log_file: str) -> logging.Logger:
    """Configure concurrent-safe logging system.
    
    :param logger_name: Namespace for the logger
    :param log_file: Path to log file location
    :return: Configured logger instance
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    handlers = [
        ConcurrentRotatingFileHandler(
            log_file,
            maxBytes=MAX_LOG_SIZE,
            backupCount=LOG_BACKUP_COUNT,
            encoding='utf-8'
        ),
        logging.StreamHandler()
    ]

    formatter = logging.Formatter('[%(asctime)s] - [%(name)s][%(levelname)s]%(message)s')
    for handler in handlers:
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


if __name__ == "__main__":
    """Command-line entry point with test configuration."""
    try:
        sv_logger = create_logger('SV', 'Logs/state_vector.log')
        receive_sv_queue = queue.Queue()
        manager = start_sv_manager(receive_sv_queue, sv_logger)
        
        # Keep main thread alive
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        sv_logger.info(" - Main process terminated")
    except Exception as e:
        sv_logger.critical(f"Critical failure: {str(e)}", exc_info=True)