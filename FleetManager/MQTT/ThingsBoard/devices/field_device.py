"""
Field Device Management Module

.. module:: field_device
    :synopsis: Specialized device handler for agricultural field monitoring and management
    :platform: Linux, Windows, macOS
    :author: Fleet Management System Team

This module implements the FieldDevice class, which manages field monitoring devices
within the fleet management system. It handles the creation, management, and cleanup
of field devices that monitor agricultural areas, collect environmental data, and
track field-specific operations during missions.

The field device system provides comprehensive monitoring capabilities for agricultural
fields, including soil conditions, crop status, environmental parameters, and
operational metrics during mission execution.

.. note::
    Key Features:
    - Dynamic field device creation per mission
    - Sequential field numbering and organization
    - Real-time field telemetry collection and transmission
    - Mission-field relationship management
    - Multi-field support per mission
    - Comprehensive cleanup and resource management

.. versionadded:: 1.0.0
    Initial implementation of field device management

.. seealso::
    - :mod:`MQTT.ThingsBoard.devices.base_device` for base device functionality
    - :mod:`MQTT.ThingsBoard.devices.mission_device` for mission coordination

Example:
    Basic usage of field device management::

        from MQTT.ThingsBoard.devices.field_device import FieldDevice
        from MQTT.ThingsBoard.rest_api import ThingsBoardAPI
        
        # Initialize ThingsBoard API
        tb_api = ThingsBoardAPI("https://thingsboard.company.com")
        tb_api.login("username", "password")
        
        # Create field device handler
        field_device = FieldDevice(
            tb_api=tb_api,
            mqtt_logger=logger,
            tb_host="thingsboard.company.com",
            port=8883,
            telemetry_topic="v1/devices/me/telemetry"
        )
        
        # Process mission with multiple fields
        mission_msg = {
            "fields": [
                {"area": 100, "crop_type": "wheat", "soil_ph": 6.5},
                {"area": 150, "crop_type": "corn", "soil_ph": 6.8}
            ]
        }
        field_device.handle_message(mission_msg, "M001", "mission_device_id")
"""

from MQTT.ThingsBoard.devices.base_device import BaseDevice


class FieldDevice:
    """
    Specialized device handler for managing agricultural field monitoring devices.
    
    This class manages the creation and lifecycle of field devices that monitor
    agricultural areas during mission execution. It provides sequential field
    numbering, relationship management with missions, and comprehensive telemetry
    collection for field-specific data.
    
    The field system supports multiple fields per mission, allowing for comprehensive
    monitoring of complex agricultural operations across various field zones.
    
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
        Field devices are automatically numbered sequentially within each mission
        (e.g., "Field M001.1", "Field M001.2") for easy identification and tracking
        of different field zones.
        
    .. warning::
        Field devices must be properly cleaned up when missions complete to
        prevent resource leaks and maintain optimal system performance.
        
    .. versionadded:: 1.0.0
        Initial implementation of field device management
        
    Attributes:
        base (BaseDevice): Base device functionality for ThingsBoard operations
        fields (dict): Dictionary mapping mission IDs to lists of field device data
        mqtt_logger (logging.Logger): Logger for operation tracking and debugging
        
    Example:
        Initialize and use field device handler::
        
            field_handler = FieldDevice(tb_api, logger, "thingsboard.com", 8883, "v1/devices/me/telemetry")
            
            # Process mission with field data
            mission_data = {
                "fields": [
                    {"area": 100, "crop": "wheat", "temperature": 22.5},
                    {"area": 75, "crop": "corn", "temperature": 24.1}
                ]
            }
            field_handler.handle_message(mission_data, "M001", "mission_device_id")
    """
    
    def __init__(self, tb_api, mqtt_logger, tb_host, port, telemetry_topic):
        """Initialize the field device handler with ThingsBoard integration.
        
        Sets up the field device management system with base device functionality
        and initializes the storage for mission-specific field devices.
        
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
        self.fields = {}  # Dictionary: mission_id -> list of field device data
        self.mqtt_logger = mqtt_logger
    
    def handle_message(self, message, mission_id, mission_device_id):
        """Process mission messages and create corresponding field monitoring devices.
        
        Creates field devices for each field specified in the mission message,
        establishes relationships with the mission device, and transmits initial
        field telemetry data. Each field is automatically numbered for tracking.
        
        The method handles multiple fields per mission, creating individual
        ThingsBoard devices for each field zone to enable independent monitoring
        and data collection.
        
        :param message: Mission message containing field data array
        :type message: dict
        :param mission_id: Unique identifier of the associated mission
        :type mission_id: str
        :param mission_device_id: ThingsBoard device ID of the mission
        :type mission_device_id: str
        :return: None
        :rtype: None
        
        .. note::
            Field Processing Steps:
            1. Initialize mission field list if first processing
            2. Iterate through each field in the message
            3. Expand field list if new fields detected
            4. Create sequential field devices with unique names
            5. Store device credentials and establish MQTT connections
            6. Transmit initial field telemetry data
            7. Create relationships with mission device
            
        .. warning::
            The message must contain a 'fields' array with field data objects.
            Each field object should contain relevant monitoring parameters.
            
        .. tip:
            Field devices are numbered sequentially (Field M001.1, Field M001.2)
            making it easy to identify and correlate field data with specific zones.
            
        Message Structure:
            Expected message format::
            
                {
                    "fields": [
                        {
                            "area": 100,
                            "crop_type": "wheat",
                            "soil_ph": 6.5,
                            "moisture": 45.2,
                            "temperature": 22.5
                        },
                        {
                            "area": 150,
                            "crop_type": "corn",
                            "soil_ph": 6.8,
                            "moisture": 42.1,
                            "temperature": 24.1
                        }
                    ]
                }
        
        Example:
            Process mission with multiple agricultural fields::
            
                mission_msg = {
                    "fields": [
                        {
                            "field_id": "F001",
                            "area": 100,
                            "crop_type": "wheat",
                            "soil_conditions": {
                                "ph": 6.5,
                                "moisture": 45.2,
                                "nitrogen": 120
                            },
                            "environmental": {
                                "temperature": 22.5,
                                "humidity": 65.0
                            }
                        },
                        {
                            "field_id": "F002",
                            "area": 75,
                            "crop_type": "corn",
                            "soil_conditions": {
                                "ph": 6.8,
                                "moisture": 42.1,
                                "nitrogen": 110
                            },
                            "environmental": {
                                "temperature": 24.1,
                                "humidity": 62.5
                            }
                        }
                    ]
                }
                
                field_device.handle_message(
                    message=mission_msg,
                    mission_id="M001",
                    mission_device_id="mission_device_uuid"
                )
        """
        # Initialize field list for mission if not exists
        if mission_id not in self.fields:
            self.fields[mission_id] = []
            
        # Process each field in the mission
        for i, field in enumerate(message['fields']):
            # Expand field list if processing new fields
            if i >= len(self.fields[mission_id]):
                self.fields[mission_id].append({})
                
            # Create field device with sequential naming
            field_device_id, field_access_token = self.base.create_device(
                f"Field {mission_id}.{i+1}", "Field"
            )
            
            # Store field device credentials
            self.fields[mission_id][i]['device_id'] = field_device_id
            self.fields[mission_id][i]['access_token'] = field_access_token

            # Create MQTT client and transmit initial field telemetry
            client = self.base.create_client(field_access_token)
            self.base.send_telemetry(client, field)
            
            # Create relationship between mission and field device
            if mission_device_id and field_device_id:
                self.base.tb.create_relation(
                    mission_device_id, 
                    field_device_id, 
                    "FIELD"
                )
    
    def cleanup(self, mission_id):
        """Clean up all field devices associated with a completed mission.
        
        Performs comprehensive cleanup of all field devices created for the
        specified mission, including device deletion from ThingsBoard and
        removal from local storage. This ensures proper resource management
        and prevents accumulation of unused devices.
        
        :param mission_id: Unique identifier of the mission to clean up
        :type mission_id: str
        :return: None
        :rtype: None
        
        .. note::
            Cleanup Operations:
            1. Iterate through all field devices for the mission
            2. Delete each field device from ThingsBoard using retry mechanism
            3. Remove mission field data from local storage
            
        .. warning::
            This operation is irreversible and will permanently delete all
            field devices and their associated telemetry data from ThingsBoard.
            
        .. tip:
            Always call this method when missions complete to maintain
            system performance and prevent resource accumulation across
            multiple mission cycles.
            
        Example:
            Clean up field devices after mission completion::
            
                # Mission completed successfully
                mission_id = "M001"
                
                # Clean up all associated field devices
                field_device.cleanup(mission_id)
                
                print(f"All field devices for mission {mission_id} cleaned up")
                
        Cleanup Process:
            The method uses the retry mechanism from base device functionality
            to ensure reliable device deletion even under network stress or
            ThingsBoard server load conditions.
        """
        # Check if mission has field devices to clean up
        if mission_id in self.fields:
            # Clean up each field device for this mission
            for field in self.fields[mission_id]:
                if 'device_id' in field:
                    # Delete field device from ThingsBoard with retry mechanism
                    self.base.delete_device_with_retry(field['device_id'])
                    
            # Remove mission field data from local storage
            del self.fields[mission_id]