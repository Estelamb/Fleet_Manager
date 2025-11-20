"""
Devices Manager Module

.. module:: devices_manager
    :synopsis: Central orchestrator for all ThingsBoard device types in the fleet management system
    :platform: Linux, Windows, macOS
    :author: Fleet Management System Team

This module implements the central device management orchestrator that coordinates all specialized
device types within the fleet management system. It acts as a message router and coordinator,
handling different message types and delegating operations to appropriate device managers.

The DevicesManager class provides a unified interface for managing missions, vehicles, fields,
treatments, and telemetry data across the entire IoT fleet, ensuring proper coordination and
data flow between different device types.

.. note::
    Key Features:
    - Centralized message routing and coordination across device types
    - Mission lifecycle management with multi-device orchestration
    - Real-time telemetry processing and distribution
    - Vehicle state tracking and mission assignment
    - Treatment and prescription map coordination
    - Comprehensive cleanup and resource management
    - Inter-device relationship management

.. versionadded:: 1.0.0
    Initial implementation of centralized device management

.. seealso::
    - :mod:`MQTT.ThingsBoard.devices.mission_device` for mission management
    - :mod:`MQTT.ThingsBoard.devices.vehicle_device` for vehicle tracking
    - :mod:`MQTT.ThingsBoard.devices.field_device` for field monitoring

Example:
    Basic usage of the devices manager::

        from MQTT.ThingsBoard.devices.devices_manager import DevicesManager
        from MQTT.ThingsBoard.rest_api import ThingsBoardAPI
        
        # Initialize ThingsBoard API
        tb_api = ThingsBoardAPI("https://thingsboard.company.com")
        tb_api.login("username", "password")
        
        # Create devices manager
        manager = DevicesManager(
            tb_api=tb_api,
            mqtt_logger=logger,
            tb_host="thingsboard.company.com",
            port=8883,
            telemetry_topic="v1/devices/me/telemetry"
        )
        
        # Process different message types
        mission_msg = {"type": "Mission", "mission_id": "001", ...}
        manager.handle_message(mission_msg)
"""

import json
import logging
from MQTT.ThingsBoard.devices.mission_device import MissionDevice
from MQTT.ThingsBoard.devices.field_device import FieldDevice
from MQTT.ThingsBoard.devices.vehicle_device import VehicleDevice
from MQTT.ThingsBoard.devices.feedback_device import FeedbackDevice
from MQTT.ThingsBoard.devices.treatment_device import TreatmentDevice
from MQTT.ThingsBoard.devices.field_pm_device import FieldPMDevice
from MQTT.ThingsBoard.devices.metric_device import MetricDevice


class DevicesManager:
    """
    Central coordinator for all ThingsBoard device types in the fleet management system.
    
    This class orchestrates the entire fleet of IoT devices by managing specialized device
    handlers for different entity types (missions, vehicles, fields, treatments, etc.).
    It acts as the primary message router, processing incoming messages and delegating
    operations to the appropriate device managers.
    
    The manager handles complex inter-device relationships and ensures proper coordination
    between different device types during mission execution, telemetry processing, and
    system cleanup operations.
    
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
        Device Initialization Order:
        The constructor initializes devices in a specific order to handle dependencies:
        1. TreatmentDevice - Independent treatment management
        2. FieldPMDevice - Depends on TreatmentDevice for prescription maps
        3. Other devices - Mission, Field, Vehicle, Feedback, Metric
        
    .. warning::
        The initialization order is critical for proper inter-device communication.
        Changing the order may break treatment and prescription map functionality.
        
    .. versionadded:: 1.0.0
        Initial implementation of centralized device management
        
    Attributes:
        treatment_device (TreatmentDevice): Handles agricultural treatment operations
        field_pm_device (FieldPMDevice): Manages prescription maps with treatment integration
        mission_device (MissionDevice): Coordinates mission lifecycle and tracking
        field_device (FieldDevice): Manages field monitoring and data collection
        vehicle_device (VehicleDevice): Tracks vehicle states and assignments
        feedback_device (FeedbackDevice): Handles user feedback and responses
        metric_device (MetricDevice): Processes system metrics and performance data
        mqtt_logger (logging.Logger): Logger for operation tracking
        
    Example:
        Initialize and use the devices manager::
        
            manager = DevicesManager(tb_api, logger, "thingsboard.com", 8883, "v1/devices/me/telemetry")
            
            # Process a mission message
            mission_msg = {
                "type": "Mission",
                "mission_id": "M001",
                "name": "Field Survey Alpha",
                "fields": [...]
            }
            manager.handle_message(mission_msg)
    """
    
    def __init__(self, tb_api, mqtt_logger, tb_host, port, telemetry_topic):
        """Initialize the devices manager with all specialized device handlers.
        
        Sets up the complete device management ecosystem with proper initialization
        order to handle inter-device dependencies, particularly between treatment
        and prescription map devices.
        
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
        # Initialize TreatmentDevice first (no dependencies)
        self.treatment_device = TreatmentDevice(tb_api, mqtt_logger, tb_host, port, telemetry_topic)
        
        # Initialize FieldPMDevice with TreatmentDevice reference (dependency injection)
        self.field_pm_device = FieldPMDevice(tb_api, mqtt_logger, tb_host, port, telemetry_topic, treatment_device=self.treatment_device)
        
        # Initialize remaining devices (no specific order requirements)
        self.mission_device = MissionDevice(tb_api, mqtt_logger, tb_host, port, telemetry_topic)
        self.field_device = FieldDevice(tb_api, mqtt_logger, tb_host, port, telemetry_topic)
        self.vehicle_device = VehicleDevice(tb_api, mqtt_logger, tb_host, port, telemetry_topic)
        self.feedback_device = FeedbackDevice(tb_api, mqtt_logger, tb_host, port, telemetry_topic)
        self.metric_device = MetricDevice(tb_api, mqtt_logger, tb_host, port, telemetry_topic)
        
        # Store logger reference for local operations
        self.mqtt_logger = mqtt_logger

    def handle_message(self, message):
        """Process and route messages to appropriate device handlers based on message type.
        
        This is the central message processing hub that analyzes incoming messages and
        delegates them to the appropriate specialized device handlers. It implements
        the main business logic for coordinating multi-device operations and managing
        complex workflows across the fleet management system.
        
        :param message: Message dictionary containing type and payload data
        :type message: dict
        :return: None
        :rtype: None
        
        .. note::
            Supported Message Types:
            - **Mission**: Mission creation and management with field coordination
            - **Telemetry**: Real-time sensor data processing and distribution
            - **StateVector**: Vehicle position and state updates
            - **Finish**: Mission completion and comprehensive cleanup
            - **Treatment**: Agricultural treatment operation management
            - **Field_PM**: Prescription map processing with treatment integration
            - **Metric**: System performance and operational metrics
            
        .. warning::
            Message processing order is critical for mission operations. Telemetry
            and StateVector messages depend on existing Mission context.
            
        .. tip::
            All message types must include a 'type' field for proper routing.
            Invalid or missing types will cause processing errors.
            
        Message Processing Flow:
            1. Extract message type from 'type' field
            2. Route to appropriate device handler(s)
            3. Coordinate multi-device operations when needed
            4. Handle cleanup and relationship management
            
        Example:
            Process different message types::
            
                # Mission creation
                mission_msg = {
                    "type": "Mission",
                    "mission_id": "M001",
                    "name": "Field Survey Alpha",
                    "fields": [{"id": "F001", "area": 100}]
                }
                manager.handle_message(mission_msg)
                
                # Vehicle telemetry
                telemetry_msg = {
                    "type": "Telemetry",
                    "mission_id": "M001",
                    "fields": [{"temperature": 25.5, "humidity": 60}]
                }
                manager.handle_message(telemetry_msg)
                
                # Mission completion
                finish_msg = {
                    "type": "Finish",
                    "mission_id": "M001"
                }
                manager.handle_message(finish_msg)
        """
        # Extract message type for routing
        msg_type = message['type']
        
        if msg_type == 'Mission':
            # Handle mission creation and coordination
            # Process mission through mission device and coordinate with field device
            mission_id, mission_device_id = self.mission_device.handle_message(message)
            self.field_device.handle_message(message, mission_id, mission_device_id)
            
        elif msg_type == 'Telemetry':
            # Handle real-time telemetry data processing and distribution
            mission_id = message['mission_id']
            
            # Retrieve mission context for telemetry processing
            mission = self.mission_device.missions.get(mission_id, {})
            mission_device_id = mission.get('device_id')
            
            # Process feedback telemetry through feedback device
            self.feedback_device.handle_message(message, mission_id, mission_device_id)
            
            # Distribute field telemetry data to corresponding field devices
            for i, field_data in enumerate(message.get('fields', [])):
                if i < len(self.field_device.fields.get(mission_id, [])):
                    # Get field device client and send telemetry
                    client = self.field_device.fields[mission_id][i].get('client')
                    self.mission_device.base.send_telemetry(client, field_data)
        
        elif msg_type == 'StateVector':
            # Handle vehicle state and position updates
            # Pass mission context to vehicle handler for proper coordination
            self.vehicle_device.handle_message(
                message, 
                self.mission_device.missions
            )
        
        elif msg_type == 'Finish':
            # Handle mission completion and comprehensive cleanup
            mission_id = message['mission_id']
            mission = self.mission_device.missions.get(mission_id, {})
            mission_device_id = mission.get('device_id')
            
            # Cleanup all mission-related devices in proper order
            self.feedback_device.cleanup(mission_id, mission_device_id)
            self.field_device.cleanup(mission_id)
            self.mission_device.cleanup(mission_id)
            
            # Clean up vehicle-mission relationships
            if mission_device_id:
                for vehicle_id in mission.get('vehicles', []):
                    vehicle = self.vehicle_device.vehicles.get(vehicle_id, {})
                    vehicle_device_id = vehicle.get('device_id')
                    if vehicle_device_id:
                        # Remove vehicle assignment relationship
                        self.mission_device.base.tb.delete_relation(
                            mission_device_id, 
                            vehicle_device_id, 
                            "ASSIGNED_TO"
                        )

            # Clean up vehicle metrics for completed mission
            if 'vehicles' in mission:
                for vehicle_id in mission['vehicles']:
                    self.metric_device.cleanup(vehicle_id)

        elif msg_type == 'Treatment':
            # Handle agricultural treatment operations
            self.treatment_device.handle_message(message)

        elif msg_type == 'Field_PM':
            # Handle prescription map processing with treatment coordination
            treatment = message['telemetry'].get('treatment')
            self.field_pm_device.handle_message(message, treatment)
        
        elif msg_type == 'Metric':
            # Handle system metrics and performance data
            self.metric_device.handle_message(message)