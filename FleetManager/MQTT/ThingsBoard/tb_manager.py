"""
ThingsBoard Manager Module

.. module:: tb_manager
    :synopsis: High-level ThingsBoard integration and device management for fleet operations
    :platform: Linux, Windows, macOS
    :author: Fleet Management System Team

This module provides a comprehensive ThingsBoard management system that handles device
lifecycle, telemetry processing, and MQTT message routing for the fleet management platform.
It implements a multi-threaded architecture for efficient real-time data processing.

The module integrates with the ThingsBoard IoT platform to manage various device types
including drones, missions, fields, and treatment systems. It provides automatic device
cleanup, message processing, and telemetry forwarding capabilities.

.. note::
    Key Features:
    - Multi-threaded message processing for high throughput
    - Automatic device type management and cleanup
    - Robust message parsing and error handling
    - Real-time telemetry forwarding to ThingsBoard
    - Support for multiple message formats (JSON, string, list)
    - Comprehensive logging and monitoring integration

.. versionadded:: 1.0.0
    Initial implementation of ThingsBoard management system

.. seealso::
    - :mod:`MQTT.ThingsBoard.rest_api` for ThingsBoard REST API operations
    - :mod:`MQTT.ThingsBoard.devices.devices_manager` for device-specific management

Example:
    Basic usage of the ThingsBoard manager::

        import queue
        import logging
        from MQTT.ThingsBoard.tb_manager import start_tb_manager

        # Initialize message queue and logger
        tb_queue = queue.Queue()
        mqtt_logger = logging.getLogger('MQTT')
        
        # Start ThingsBoard manager
        tb_thread = start_tb_manager(tb_queue, mqtt_logger)
        
        # Manager is now running and processing messages
        print("ThingsBoard manager started successfully")
"""

import json
import logging
import queue
import threading
from MQTT.ThingsBoard.rest_api import ThingsBoardAPI
from MQTT.ThingsBoard.devices.devices_manager import DevicesManager

# ========================================
# ThingsBoard Configuration Constants
# ========================================

#: str: ThingsBoard server host URL for REST API operations
TB_HOST = "https://srv-iot.diatel.upm.es"

#: str: Username for ThingsBoard authentication
USERNAME = "estela.mora.barba@alumnos.upm.es"

#: str: Password for ThingsBoard authentication (consider using environment variables in production)
PASSWORD = "fleet_manager"

#: str: ThingsBoard host for MQTT telemetry connections
THINGSBOARD_HOST = "srv-iot.diatel.upm.es"

#: int: MQTT port for secure telemetry transmission (8883 for TLS)
PORT = 8883

#: str: MQTT topic for device telemetry data transmission
TELEMETRY_TOPIC = "v1/devices/me/telemetry"

class ThingsboardThread(threading.Thread):
    """
    Dedicated thread for processing ThingsBoard messages and managing device operations.
    
    This class implements a worker thread that continuously processes MQTT messages
    from a queue and forwards them to the appropriate device managers in ThingsBoard.
    It handles various message formats and provides robust error handling for
    production environments.
    
    The thread operates independently and processes messages asynchronously, allowing
    the main application to continue operating while telemetry data is being processed
    and forwarded to ThingsBoard in real-time.
    
    :param tb: Authenticated ThingsBoard API client instance
    :type tb: ThingsBoardAPI
    :param tb_queue: Thread-safe queue containing messages to process
    :type tb_queue: queue.Queue
    :param mqtt_logger: Logger instance for operation tracking and debugging
    :type mqtt_logger: logging.Logger
    :param tb_host: ThingsBoard host for MQTT connections
    :type tb_host: str
    :param port: MQTT port for telemetry transmission
    :type port: int
    :param telemetry_topic: MQTT topic for device telemetry
    :type telemetry_topic: str
    
    .. note::
        This thread runs indefinitely until the parent process terminates.
        All exceptions are caught and logged to ensure continuous operation.
        
    .. versionadded:: 1.0.0
        Initial implementation of ThingsBoard message processing thread
        
    Attributes:
        tb_queue (queue.Queue): Message queue for processing
        devices_manager (DevicesManager): Manager for device-specific operations
        mqtt_logger (logging.Logger): Logger for operation tracking
        
    Example:
        Create and start a ThingsBoard processing thread::
        
            tb_api = ThingsBoardAPI("https://thingsboard.company.com")
            tb_api.login("username", "password")
            
            tb_thread = ThingsboardThread(
                tb=tb_api,
                tb_queue=message_queue,
                mqtt_logger=logger,
                tb_host="thingsboard.company.com",
                port=8883,
                telemetry_topic="v1/devices/me/telemetry"
            )
            tb_thread.start()
    """
    
    def __init__(self, tb, tb_queue, mqtt_logger, tb_host, port, telemetry_topic):
        """Initialize the ThingsBoard processing thread.
        
        Sets up the thread with all necessary components for message processing
        including the devices manager, queue, and logging infrastructure.
        
        :param tb: Authenticated ThingsBoard API client
        :type tb: ThingsBoardAPI
        :param tb_queue: Queue for incoming messages
        :type tb_queue: queue.Queue
        :param mqtt_logger: Logger for operations
        :type mqtt_logger: logging.Logger
        :param tb_host: ThingsBoard host address
        :type tb_host: str
        :param port: MQTT connection port
        :type port: int
        :param telemetry_topic: MQTT topic for telemetry
        :type telemetry_topic: str
        """
        super().__init__()
        self.tb_queue = tb_queue
        self.devices_manager = DevicesManager(
            tb, mqtt_logger, tb_host, port, telemetry_topic
        )
        self.mqtt_logger = mqtt_logger

    def run(self):
        """Main thread execution loop for processing ThingsBoard messages.
        
        Continuously processes messages from the queue, handling various message
        formats and routing them to the appropriate device managers. The method
        implements robust error handling to ensure the thread continues operating
        even when individual messages fail processing.
        
        The processing loop handles three message formats:
        1. Dictionary objects (direct JSON)
        2. String objects (JSON strings to parse)
        3. List objects (joined and parsed as JSON)
        
        :return: None (runs indefinitely until thread termination)
        :rtype: None
        
        .. note::
            This method runs in an infinite loop and only terminates when the
            thread is stopped externally or the parent process ends.
            
        .. warning::
            All exceptions are caught and logged to prevent thread termination.
            Monitor logs for processing errors that may indicate data issues.
            
        Message Processing Flow:
            1. Retrieve message from queue (blocking operation)
            2. Determine message format and parse accordingly
            3. Forward parsed message to devices manager
            4. Log any processing errors and continue
            
        Example:
            The run method is called automatically when the thread starts::
            
                tb_thread = ThingsboardThread(...)
                tb_thread.start()  # This calls run() in a separate thread
        """
        while True:
            # Retrieve next message from the queue (blocks until message available)
            mqtt_message = self.tb_queue.get()
            
            try:
                # Handle different message format types
                if isinstance(mqtt_message, dict):
                    # Message is already a dictionary (parsed JSON)
                    message = mqtt_message
                elif isinstance(mqtt_message, str):
                    # Message is a JSON string, parse it
                    message = json.loads(mqtt_message)
                elif isinstance(mqtt_message, list):
                    # Message is a list of strings, join and parse
                    message_str = ''.join(mqtt_message)
                    message = json.loads(message_str)
                else:
                    # Unsupported message type, log error and continue
                    self.mqtt_logger.error(f"[MQTT][ThingsBoard] - Unsupported message type: {type(mqtt_message)}")
                    continue
                    
                # Forward parsed message to devices manager for processing
                self.devices_manager.handle_message(message)
                
            except Exception as e:
                # Log processing errors but continue operation
                self.mqtt_logger.error(f"[MQTT][ThingsBoard] - Error processing message: {str(e)}")

def start_tb_manager(tb_queue: queue.Queue, mqtt_logger: logging.Logger):
    """Initialize and start the ThingsBoard management system.
    
    This function sets up the complete ThingsBoard integration system, including
    authentication, device cleanup, and message processing thread initialization.
    It performs a fresh start by cleaning up existing devices and then starts
    continuous processing of telemetry messages.
    
    The function performs the following initialization steps:
    1. Creates and authenticates ThingsBoard API client
    2. Performs cleanup of existing device types for fresh start
    3. Initializes and starts the message processing thread
    4. Returns the running thread for monitoring purposes
    
    :param tb_queue: Thread-safe queue for incoming MQTT messages
    :type tb_queue: queue.Queue
    :param mqtt_logger: Logger instance for operation tracking and debugging
    :type mqtt_logger: logging.Logger
    :return: Running ThingsBoard processing thread instance
    :rtype: ThingsboardThread
    
    .. note::
        Device Cleanup Types:
        The function automatically removes all existing devices of these types:
        - Drone: Unmanned aerial vehicle devices
        - Mission: Mission management and tracking devices
        - Field: Agricultural field monitoring devices
        - Feedback: User feedback and response devices
        - Treatment: Agricultural treatment application devices
        - Field_PM: Field prescription map devices
        - RPI5: Raspberry Pi 5 controller devices
        
    .. warning::
        This function performs bulk device deletion on startup. Ensure this
        behavior is appropriate for your production environment.
        
    .. tip::
        Consider implementing selective cleanup or backup procedures before
        using this function in production environments with valuable device data.
        
    .. versionadded:: 1.0.0
        Initial implementation of ThingsBoard manager startup
        
    Example:
        Start ThingsBoard manager in a fleet management application::
        
            import queue
            import logging
            from MQTT.ThingsBoard.tb_manager import start_tb_manager
            
            # Setup logging
            logging.basicConfig(level=logging.INFO)
            mqtt_logger = logging.getLogger('MQTT')
            
            # Create message queue
            tb_queue = queue.Queue()
            
            # Start ThingsBoard manager
            tb_thread = start_tb_manager(tb_queue, mqtt_logger)
            
            # Manager is now running and ready to process messages
            print("ThingsBoard manager started successfully")
            
            # Add messages to queue for processing
            tb_queue.put({"device_id": "sensor_01", "temperature": 25.5})
            
    Raises:
        Exception: If ThingsBoard authentication fails or thread startup encounters errors
    """
    # Initialize ThingsBoard API client with configured host
    tb = ThingsBoardAPI(TB_HOST)
    
    # Authenticate with ThingsBoard using configured credentials
    if tb.login(USERNAME, PASSWORD):
        # Perform device cleanup for fresh start - remove all existing device types
        tb.delete_all_devices_by_type("Drone")        # Unmanned aerial vehicles
        tb.delete_all_devices_by_type("Mission")      # Mission management devices
        tb.delete_all_devices_by_type("Field")        # Field monitoring devices
        tb.delete_all_devices_by_type("Feedback")     # Feedback collection devices
        tb.delete_all_devices_by_type("Treatment")    # Treatment application devices
        tb.delete_all_devices_by_type("Field_PM")     # Prescription map devices
        tb.delete_all_devices_by_type("RPI5")         # Raspberry Pi controllers
    
    # Create and configure the ThingsBoard processing thread
    tb_thread = ThingsboardThread(
        tb=tb,                              # Authenticated API client
        tb_queue=tb_queue,                  # Message processing queue
        mqtt_logger=mqtt_logger,            # Logger for operations
        tb_host=THINGSBOARD_HOST,           # MQTT host for telemetry
        port=PORT,                          # MQTT port for connections
        telemetry_topic=TELEMETRY_TOPIC     # Topic for telemetry data
    )
    
    # Start the processing thread (non-blocking)
    tb_thread.start()
    
    # Return the running thread for monitoring and management
    return tb_thread