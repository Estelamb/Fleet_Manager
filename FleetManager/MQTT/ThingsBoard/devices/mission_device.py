"""
Mission Device Module
====================

This module provides the `MissionDevice` class for managing ThingsBoard devices
that represent agricultural missions in the fleet management system.

The `MissionDevice` class handles the creation, management, and cleanup of ThingsBoard
devices that monitor and track mission execution, including field operations,
vehicle assignments, and mission-specific telemetry data.

Key Features:
    - Mission device lifecycle management
    - Mission state tracking with field and vehicle assignments
    - Telemetry data collection and transmission
    - Automatic device cleanup upon mission completion
    - Integration with ThingsBoard REST API and MQTT protocols

Usage Example:
    ::

        mission_device = MissionDevice(tb_api, mqtt_logger, tb_host, port, telemetry_topic)
        mission_id, device_id = mission_device.handle_message(mission_message)
        # ... mission execution ...
        mission_device.cleanup(mission_id)

Author: Fleet Management System
Date: 2025
"""

from MQTT.ThingsBoard.devices.base_device import BaseDevice


class MissionDevice:
    """
    ThingsBoard device manager for agricultural mission monitoring.
    
    This class manages ThingsBoard devices that represent missions in the agricultural
    fleet management system. Each mission gets its own device for tracking mission
    progress, field assignments, vehicle coordination, and telemetry data collection.
    
    The class maintains a registry of active missions with their associated device
    information, field mappings, and vehicle assignments. It provides methods for
    creating mission devices, handling mission messages, and cleaning up resources
    when missions are completed.
    
    Attributes:
        base (BaseDevice): Base device manager for ThingsBoard operations
        missions (dict): Registry of active missions with device information
        mqtt_logger: Logger instance for MQTT operations
        
    Note:
        Mission devices are automatically created when new mission messages are
        received and cleaned up when missions are completed or canceled.
    
    Warning:
        Ensure proper cleanup of mission devices to prevent resource leaks
        in the ThingsBoard platform.
    
    See Also:
        :class:`BaseDevice`: Base class for ThingsBoard device operations
        :mod:`MQTT.ThingsBoard.tb_manager`: ThingsBoard connection manager
    """
    
    def __init__(self, tb_api, mqtt_logger, tb_host, port, telemetry_topic):
        """
        Initialize the mission device manager.
        
        Sets up the base device manager and initializes the mission registry
        for tracking active missions and their associated ThingsBoard devices.
        
        Args:
            tb_api: ThingsBoard REST API client instance
            mqtt_logger: Logger instance for MQTT operations and debugging
            tb_host (str): ThingsBoard server hostname or IP address
            port (int): ThingsBoard MQTT port (typically 1883)
            telemetry_topic (str): MQTT topic for telemetry data transmission
            
        Example:
            ::
            
                tb_api = RestClientCE(base_url="http://localhost:8080")
                mission_device = MissionDevice(
                    tb_api=tb_api,
                    mqtt_logger=logger,
                    tb_host="localhost", 
                    port=1883,
                    telemetry_topic="v1/devices/me/telemetry"
                )
        """
        self.base = BaseDevice(tb_api, mqtt_logger, tb_host, port, telemetry_topic)
        self.missions = {}  # Registry of active missions: {mission_id: mission_data}
        self.mqtt_logger = mqtt_logger
    
    def handle_message(self, message):
        """
        Process mission message and create/update corresponding ThingsBoard device.
        
        This method handles incoming mission messages by creating new mission entries
        in the registry or updating existing ones. Each mission gets a dedicated
        ThingsBoard device for monitoring mission progress and collecting telemetry data.
        
        The method performs the following operations:
        1. Creates or updates mission entry in the registry
        2. Creates a new ThingsBoard device for the mission
        3. Establishes MQTT client connection with the device token
        4. Sends initial telemetry data to the device
        
        Args:
            message (dict): Mission message containing mission details with keys:
                - mission_id (str): Unique identifier for the mission
                - fields (list): List of field configurations for the mission
                - vehicles (list, optional): List of assigned vehicles
                - telemetry (dict): Initial telemetry data to send
                
        Returns:
            tuple: A tuple containing:
                - mission_id (str): The mission identifier
                - mission_device_id (str): ThingsBoard device ID for the mission
                
        Example:
            ::
            
                message = {
                    'mission_id': 'MISSION_001',
                    'fields': [{'field_id': 'F001', 'area': 100}],
                    'vehicles': ['VEHICLE_001', 'VEHICLE_002'],
                    'telemetry': {
                        'status': 'active',
                        'start_time': '2025-01-15T10:00:00Z',
                        'estimated_duration': 3600
                    }
                }
                mission_id, device_id = mission_device.handle_message(message)
                
        Note:
            If the mission already exists in the registry, this method will update
            the mission's device information and vehicle assignments.
        """
        mission_id = message['mission_id']
        
        # Initialize mission entry if not exists
        if mission_id not in self.missions:
            self.missions[mission_id] = {
                'device_id': None,
                'access_token': None,
                'fields': [{} for _ in message['fields']],  # Initialize field placeholders
                'vehicles': message.get('vehicles', [])
            }

        # Create ThingsBoard device for the mission
        mission_device_id, access_token = self.base.create_device(f"Mission {mission_id}", "Mission")
        
        # Update mission registry with device information
        self.missions[mission_id]['device_id'] = mission_device_id
        self.missions[mission_id]['access_token'] = access_token
        self.missions[mission_id]['vehicles'] = message.get('vehicles', [])

        # Establish MQTT connection and send initial telemetry
        client = self.base.create_client(access_token)
        self.base.send_telemetry(client, message['telemetry'])
        
        return mission_id, mission_device_id
    
    def cleanup(self, mission_id):
        """
        Clean up mission device and remove from registry.
        
        This method performs cleanup operations for a completed or canceled mission
        by deleting the associated ThingsBoard device and removing the mission
        entry from the local registry.
        
        The cleanup process includes:
        1. Retrieving mission device information from the registry
        2. Deleting the ThingsBoard device with retry mechanism
        3. Removing the mission entry from the local registry
        
        Args:
            mission_id (str): Unique identifier of the mission to clean up
            
        Example:
            ::
            
                # Clean up completed mission
                mission_device.cleanup('MISSION_001')
                
        Note:
            This method uses the base device's delete_device_with_retry method
            to ensure robust device deletion even in case of temporary network issues.
            
        Warning:
            After cleanup, the mission device will no longer be accessible in
            ThingsBoard and all associated telemetry data collection will stop.
        """
        if mission_id in self.missions:
            mission_device_id = self.missions[mission_id].get('device_id')
            
            # Delete ThingsBoard device if it exists
            if mission_device_id:
                self.base.delete_device_with_retry(mission_device_id)
                
            # Remove mission from local registry
            del self.missions[mission_id]