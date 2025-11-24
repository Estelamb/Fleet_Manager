"""
Feedback Device Management Module

.. module:: feedback_device
    :synopsis: Specialized device handler for user feedback and response management
    :platform: Linux, Windows, macOS
    :author: Fleet Management System Team

This module implements the FeedbackDevice class, which manages feedback collection
devices within the fleet management system. It handles the creation, management,
and cleanup of feedback devices that collect user responses, system feedback,
and operational data during mission execution.

The feedback system allows for real-time collection of user inputs, system responses,
and operational feedback during missions, providing valuable data for system
improvement and mission analysis.

.. note::
    Key Features:
    - Dynamic feedback device creation per mission
    - Sequential feedback numbering and organization
    - Real-time telemetry collection and transmission
    - Mission-feedback relationship management
    - Comprehensive cleanup and resource management
    - Multi-feedback support per mission

.. versionadded:: 1.0.0
    Initial implementation of feedback device management

.. seealso::
    - :mod:`MQTT.ThingsBoard.devices.base_device` for base device functionality
    - :mod:`MQTT.ThingsBoard.devices.mission_device` for mission coordination

Example:
    Basic usage of feedback device management::

        from MQTT.ThingsBoard.devices.feedback_device import FeedbackDevice
        from MQTT.ThingsBoard.rest_api import ThingsBoardAPI
        
        # Initialize ThingsBoard API
        tb_api = ThingsBoardAPI("https://thingsboard.company.com")
        tb_api.login("username", "password")
        
        # Create feedback device handler
        feedback_device = FeedbackDevice(
            tb_api=tb_api,
            mqtt_logger=logger,
            tb_host="thingsboard.company.com",
            port=8883,
            telemetry_topic="v1/devices/me/telemetry"
        )
        
        # Process feedback message
        feedback_msg = {
            "telemetry": {
                "user_rating": 4.5,
                "comments": "Mission completed successfully"
            }
        }
        feedback_device.handle_message(feedback_msg, "M001", "mission_device_id")
"""

from MQTT.ThingsBoard.devices.base_device import BaseDevice


class FeedbackDevice:
    """
    Specialized device handler for managing feedback collection within missions.
    
    This class manages the creation and lifecycle of feedback devices that collect
    user inputs, system responses, and operational data during mission execution.
    It provides sequential feedback numbering, relationship management with missions,
    and comprehensive cleanup capabilities.
    
    The feedback system supports multiple feedback instances per mission, allowing
    for comprehensive data collection throughout mission execution phases.
    
    :param tb_api: Authenticated ThingsBoard REST API client
    :type tb_api: ThingsBoardAPI
    :param mqtt_logger: Logger instance for MQTT operations and debugging
    :type mqtt_logger: logging.Logger
    :param tb_host: ThingsBoard server hostname for MQTT connections
    :type tb_host: str
    :param port: MQTT port for secure connections (typically 8883 for TLS)
    :type port: int
    :param telemetry_topic: MQTT topic for publishing device telemetry data
    :type telemetry_topic: str
    
    .. note::
        Feedback devices are automatically numbered sequentially within each mission
        (e.g., "Feedback M001.1", "Feedback M001.2") for easy identification and tracking.
        
    .. warning:
        Feedback devices must be properly cleaned up when missions complete to
        prevent resource leaks and maintain system performance.
        
    .. versionadded:: 1.0.0
        Initial implementation of feedback device management
        
    Attributes:
        base (BaseDevice): Base device functionality for ThingsBoard operations
        feedbacks (dict): Dictionary mapping mission IDs to lists of feedback devices
        mqtt_logger (logging.Logger): Logger for operation tracking and debugging
        
    Example:
        Initialize and use feedback device handler::
        
            feedback_handler = FeedbackDevice(tb_api, logger, "thingsboard.com", 8883, "v1/devices/me/telemetry")
            
            # Process user feedback
            feedback_data = {
                "telemetry": {
                    "user_satisfaction": 4.2,
                    "completion_time": 120,
                    "comments": "Task completed efficiently"
                }
            }
            feedback_handler.handle_message(feedback_data, "M001", "mission_device_id")
    """
    
    def __init__(self, tb_api, mqtt_logger, tb_host, port, telemetry_topic):
        """Initialize the feedback device handler with ThingsBoard integration.
        
        Sets up the feedback device management system with base device functionality
        and initializes the storage for mission-specific feedback devices.
        
        :param tb_api: Authenticated ThingsBoard API client
        :type tb_api: ThingsBoardAPI
        :param mqtt_logger: Logger for MQTT operations
        :type mqtt_logger: logging.Logger
        :param tb_host: ThingsBoard server hostname
        :type tb_host: str
        :param port: MQTT connection port
        :type port: int
        :param telemetry_topic: MQTT topic for telemetry
        :type telemetry_topic: str
        """
        self.base = BaseDevice(tb_api, mqtt_logger, tb_host, port, telemetry_topic)
        self.feedbacks = {}  # mission_id -> list of feedback devices
        self.mqtt_logger = mqtt_logger
    
    def handle_message(self, message, mission_id, mission_device_id):
        """Process feedback messages and create corresponding ThingsBoard devices.
        
        Creates a new feedback device for the specified mission, establishes
        relationships with the mission device, and transmits the feedback telemetry
        data. Each feedback instance is automatically numbered for easy tracking.
        
        The method handles the complete lifecycle of feedback processing including
        device creation, relationship establishment, and telemetry transmission.
        
        :param message: Feedback message containing telemetry data
        :type message: dict
        :param mission_id: Unique identifier of the associated mission
        :type mission_id: str
        :param mission_device_id: ThingsBoard device ID of the mission
        :type mission_device_id: str
        :return: None
        :rtype: None
        
        .. note::
            Feedback Processing Steps:
            1. Initialize mission feedback list if first feedback
            2. Generate sequential feedback device name
            3. Create ThingsBoard device with "Feedback" type
            4. Set device attributes and establish MQTT connection
            5. Create relationship with mission device
            6. Transmit feedback telemetry data
            
        .. warning::
            The message must contain a 'telemetry' field with feedback data.
            Missing telemetry will result in empty data transmission.
            
        .. tip::
            Feedback devices are automatically numbered sequentially, making
            it easy to track multiple feedback instances per mission.
            
        Message Structure:
            Expected message format::
            
                {
                    "telemetry": {
                        "user_rating": 4.5,
                        "completion_time": 120,
                        "comments": "Mission feedback text",
                        "satisfaction_score": 8.5
                    }
                }
        
        Example:
            Process user feedback for a mission::
            
                feedback_msg = {
                    "telemetry": {
                        "user_satisfaction": 4.2,
                        "task_difficulty": 3.1,
                        "completion_time": 95,
                        "suggestions": "Consider route optimization"
                    }
                }
                
                feedback_device.handle_message(
                    message=feedback_msg,
                    mission_id="M001",
                    mission_device_id="mission_device_uuid"
                )
        """
        if mission_id not in self.feedbacks:
            self.feedbacks[mission_id] = []

        # Número secuencial de feedback
        feedback_number = len(self.feedbacks[mission_id]) + 1
        feedback_name = f"Feedback {mission_id}.{feedback_number}"

        # Crear dispositivo Feedback
        device_id, access_token = self.base.create_device(feedback_name, "Feedback")
        if not device_id or not access_token:
            self.mqtt_logger.error(f"[FeedbackDevice] Failed to create feedback device {feedback_name}")
            return

        # Establecer atributo para identificar el feedback
        self.base.tb.set_server_attribute(device_id, 'feedback', 'feedback')

        # Crear cliente MQTT
        client = self.base.create_client(access_token)
        if not client:
            self.mqtt_logger.error(f"[FeedbackDevice] Failed to create MQTT client for {feedback_name}")
            return

        # Guardar feedback
        self.feedbacks[mission_id].append({
            'device_id': device_id,
            'client': client
        })

        # Crear relación Mission → Feedback
        if mission_device_id:
            if not self.base.tb.create_relation(mission_device_id, device_id, "FEEDBACK"):
                self.mqtt_logger.error(f"[FeedbackDevice] Failed to create relation for {feedback_name}")

        # Enviar telemetría
        self.base.send_telemetry(client, message.get('telemetry', {}))
        self.mqtt_logger.info(f"[FeedbackDevice] Sent telemetry for {feedback_name}")
    
    def cleanup(self, mission_id, mission_device_id):
        """Clean up all feedback devices associated with a completed mission.
        
        Performs comprehensive cleanup of all feedback devices created for the
        specified mission, including MQTT client disconnection, device deletion,
        and relationship removal. This ensures proper resource management and
        prevents memory leaks in long-running systems.
        
        :param mission_id: Unique identifier of the mission to clean up
        :type mission_id: str
        :param mission_device_id: ThingsBoard device ID of the mission
        :type mission_device_id: str
        :return: None
        :rtype: None
        
        .. note:
            Cleanup Operations:
            1. Disconnect all MQTT clients for the mission's feedback devices
            2. Delete all feedback devices from ThingsBoard
            3. Remove all mission-feedback relationships
            4. Clear mission feedback data from local storage
            
        .. warning::
            This operation is irreversible and will permanently delete all
            feedback devices and their associated telemetry data.
            
        .. tip:
            Always call this method when missions complete to maintain
            system performance and prevent resource accumulation.
            
        Example:
            Clean up feedback devices after mission completion::
            
                # Mission completed successfully
                mission_id = "M001"
                mission_device_id = "mission_device_uuid"
                
                # Clean up all associated feedback devices
                feedback_device.cleanup(mission_id, mission_device_id)
                
                print(f"All feedback devices for mission {mission_id} cleaned up")
                
        Cleanup Process:
            The method ensures graceful cleanup even if some operations fail,
            continuing with remaining cleanup tasks to maximize resource recovery.
        """
        if mission_id not in self.feedbacks:
            return

        for feedback in self.feedbacks[mission_id]:
            # Desconectar cliente MQTT
            self.base.delete_client(feedback['client'])
            # Eliminar dispositivo con reintentos
            self.base.delete_device_with_retry(feedback['device_id'])
            # Eliminar relación Mission → Feedback
            if mission_device_id:
                self.base.tb.delete_relation(mission_device_id, feedback['device_id'], "FEEDBACK")

        # Limpiar almacenamiento local
        del self.feedbacks[mission_id]
        self.mqtt_logger.info(f"[FeedbackDevice] Cleaned up all feedback devices for mission {mission_id}")