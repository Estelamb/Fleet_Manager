"""
Treatment Device Module
======================

This module provides the `TreatmentDevice` class for managing ThingsBoard devices
that represent agricultural treatments in the fleet management system.

The `TreatmentDevice` class handles the creation, management, and cleanup of ThingsBoard
devices that track treatment applications, including pesticide/fertilizer applications,
field-treatment relationships, and treatment-specific telemetry data.

Key Features:
    - Treatment device lifecycle management
    - Treatment-field prescription map relationships
    - Vehicle-treatment association tracking
    - Telemetry data collection for treatment monitoring
    - Automatic device cleanup by treatment or mission
    - Integration with field prescription map devices

Usage Example:
    ::

        treatment_device = TreatmentDevice(tb_api, mqtt_logger, tb_host, port, telemetry_topic)
        treatment_device.handle_message(treatment_message)
        treatment_device.add_field_pm(treatment_id, field_pm_device_id, "CONTAINS")
        # ... treatment execution ...
        treatment_device.cleanup(treatment_id)

Author: Fleet Management System
Date: 2025
"""

from MQTT.ThingsBoard.devices.base_device import BaseDevice
import time

RELATION_TYPE = "CONTAINS"  # Consistent relation type for treatment-field associations


class TreatmentDevice:
    """
    ThingsBoard device manager for agricultural treatment monitoring.
    
    This class manages ThingsBoard devices that represent treatments in the agricultural
    fleet management system. Each treatment gets its own device for tracking treatment
    applications, field associations, vehicle assignments, and related telemetry data.
    
    The class maintains a registry of active treatments with their associated device
    information, field prescription map relationships, and mission context. It provides
    methods for creating treatment devices, handling treatment messages, managing
    field relationships, and cleaning up resources.
    
    Attributes:
        base (BaseDevice): Base device manager for ThingsBoard operations
        treatments (dict): Registry of active treatments with device and relationship info
        mqtt_logger: Logger instance for MQTT operations
        
    Note:
        Treatment devices are automatically linked to field prescription map devices
        when treatments are applied to specific field areas.
        
    Warning:
        Ensure proper cleanup of treatment devices and their relationships to prevent
        resource leaks in the ThingsBoard platform.
    
    See Also:
        :class:`BaseDevice`: Base class for ThingsBoard device operations
        :class:`field_pm_device.FieldPMDevice`: Field prescription map device manager
        :mod:`MQTT.ThingsBoard.tb_manager`: ThingsBoard connection manager
    """
    
    def __init__(self, tb_api, mqtt_logger, tb_host, port, telemetry_topic):
        """
        Initialize the treatment device manager.
        
        Sets up the base device manager and initializes the treatment registry
        for tracking active treatments and their associated ThingsBoard devices.
        
        Args:
            tb_api: ThingsBoard REST API client instance
            mqtt_logger: Logger instance for MQTT operations and debugging
            tb_host (str): ThingsBoard server hostname or IP address
            port (int): ThingsBoard MQTT port (typically 1883)
            telemetry_topic (str): MQTT topic for telemetry data transmission
            
        Example:
            ::
            
                tb_api = RestClientCE(base_url="http://localhost:8080")
                treatment_device = TreatmentDevice(
                    tb_api=tb_api,
                    mqtt_logger=logger,
                    tb_host="localhost", 
                    port=1883,
                    telemetry_topic="v1/devices/me/telemetry"
                )
        """
        self.base = BaseDevice(tb_api, mqtt_logger, tb_host, port, telemetry_topic)
        self.treatments = {}  # Registry of active treatments: {treatment_id: treatment_data}
        self.mqtt_logger = mqtt_logger
    
    def handle_message(self, message):
        """
        Process treatment message and create/update corresponding ThingsBoard device.
        
        This method handles incoming treatment messages by creating new treatment devices
        or updating existing ones. Each treatment gets a dedicated ThingsBoard device
        for monitoring treatment applications and collecting telemetry data.
        
        The method performs the following operations:
        1. Extracts treatment information from the message
        2. Creates a new ThingsBoard device for the treatment if it doesn't exist
        3. Establishes MQTT client connection with the device token
        4. Sets server attributes for searchability (treatment_id, mission_id, vehicle_id)
        5. Sends initial telemetry data to the device
        
        Args:
            message (dict): Treatment message containing treatment details with keys:
                - telemetry (dict): Treatment telemetry data including:
                    - treatment (str): Treatment identifier/name
                    - vehicle_id (str, optional): Assigned vehicle ID
                - mission_id (str, optional): Associated mission identifier
                
        Example:
            ::
            
                message = {
                    'mission_id': 'MISSION_001',
                    'telemetry': {
                        'treatment': 'PESTICIDE_APP_001',
                        'vehicle_id': 'VEHICLE_001',
                        'application_rate': 2.5,
                        'pressure': 3.2,
                        'timestamp': '2025-01-15T14:30:00Z'
                    }
                }
                treatment_device.handle_message(message)
                
        Note:
            Server attributes are set on the device to facilitate searches and
            relationship management in the ThingsBoard platform.
        """
        telemetry = message['telemetry']
        treatment = telemetry.get('treatment')
        mission_id = message.get('mission_id')
        vehicle_id = telemetry.get('vehicle_id')
        
        treatment = f"{mission_id}-{vehicle_id} {treatment}"
        
        # Create treatment device if it doesn't exist
        if treatment not in self.treatments:
            device_name = treatment
            device_id, access_token = self.base.create_device(device_name, "Treatment")
            
            if device_id and access_token:
                client = self.base.create_client(access_token)
                self.treatments[treatment] = {
                    'device_id': device_id,
                    'client': client,
                    'mission_id': mission_id,
                    'fields_pm': {}  # Dictionary to maintain associated Field_PMs
                }
                
                # Set server attributes for search and relationship management
                self.base.tb.set_server_attribute(device_id, 'treatment_id', treatment)
                if mission_id:
                    self.base.tb.set_server_attribute(device_id, 'mission_id', mission_id)
                if vehicle_id:
                    self.base.tb.set_server_attribute(device_id, 'vehicle_id', vehicle_id)
                
                # Send initial telemetry data
                self.base.send_telemetry(client, telemetry)
    
    def add_field_pm(self, treatment, field_pm_device_id, relation_type):
        """
        Associate a field prescription map device with a treatment device.
        
        This method creates a relationship between a treatment device and a field
        prescription map device, indicating that the treatment is applied to a
        specific field area defined by the prescription map.
        
        The relationship is created in ThingsBoard and tracked locally for cleanup
        purposes. This enables tracking which treatments are applied to which
        field areas and supports complex agricultural operation monitoring.
        
        Args:
            treatment (str): Treatment identifier/name
            field_pm_device_id (str): ThingsBoard device ID of the field prescription map
            relation_type (str): Type of relationship (typically "CONTAINS")
            
        Returns:
            bool: True if the relationship was successfully created, False otherwise
            
        Example:
            ::
            
                # Associate treatment with field prescription map
                success = treatment_device.add_field_pm(
                    "PESTICIDE_APP_001", 
                    "field_pm_device_123", 
                    "CONTAINS"
                )
                if success:
                    print("Treatment-field relationship created successfully")
                    
        Note:
            This method is typically called by FieldPMDevice to notify about
            new field prescription map associations with treatments.
            
        Warning:
            Duplicate relationships for the same treatment-field pair are prevented
            to avoid relationship conflicts in ThingsBoard.
        """
        if treatment in self.treatments:
            treatment_device_id = self.treatments[treatment]['device_id']
            
            # Check if relationship doesn't already exist
            if field_pm_device_id not in self.treatments[treatment]['fields_pm']:
                self.treatments[treatment]['fields_pm'][field_pm_device_id] = relation_type
                
                # Create relationship in ThingsBoard
                return self.base.create_relation(
                    treatment_device_id,
                    field_pm_device_id,
                    relation_type
                )
        return False

    def cleanup(self, treatment):
        """
        Clean up treatment device and all its relationships.
        
        This method performs comprehensive cleanup for a treatment by:
        1. Deleting all relationships with field prescription map devices
        2. Closing the MQTT client connection
        3. Deleting the ThingsBoard device
        4. Removing the treatment from the local registry
        
        Args:
            treatment (str): Treatment identifier/name to clean up
            
        Example:
            ::
            
                # Clean up completed treatment
                treatment_device.cleanup('PESTICIDE_APP_001')
                
        Note:
            This method ensures complete cleanup of all resources associated
            with the treatment, including ThingsBoard relationships and MQTT connections.
            
        Warning:
            After cleanup, the treatment device will no longer be accessible in
            ThingsBoard and all associated telemetry data collection will stop.
        """
        if treatment in self.treatments:
            # Delete all relationships with Field_PM devices
            for field_pm_id in self.treatments[treatment]['fields_pm']:
                self.base.tb.delete_relation(
                    self.treatments[treatment]['device_id'],
                    field_pm_id,
                    RELATION_TYPE
                )
            
            # Clean up MQTT client and ThingsBoard device
            self.base.delete_client(self.treatments[treatment]['client'])
            self.base.delete_device_with_retry(self.treatments[treatment]['device_id'])
            
            # Remove from local registry
            del self.treatments[treatment]

    def cleanup_by_mission(self, mission_id):
        """
        Clean up all treatments associated with a specific mission.
        
        This method identifies and cleans up all treatments that belong to a
        specific mission. It's typically called when a mission is completed
        or canceled to ensure all related treatment devices are properly cleaned up.
        
        The method performs the following operations:
        1. Identifies all treatments associated with the given mission ID
        2. Calls cleanup() for each identified treatment
        3. Ensures complete cleanup of all mission-related treatment resources
        
        Args:
            mission_id (str): Mission identifier for which to clean up treatments
            
        Example:
            ::
            
                # Clean up all treatments for completed mission
                treatment_device.cleanup_by_mission('MISSION_001')
                
        Note:
            This method is useful for bulk cleanup operations when missions
            are completed, ensuring no orphaned treatment devices remain.
        """
        # Identify treatments associated with the mission
        to_delete = [t for t, treatment in self.treatments.items()
                    if treatment.get('mission_id') == mission_id]
        
        # Clean up each identified treatment
        for treatment in to_delete:
            self.cleanup(treatment)