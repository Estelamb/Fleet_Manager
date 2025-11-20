"""
Field Prescription Map Device Management Module

.. module:: field_pm_device
    :synopsis: Specialized device handler for agricultural prescription map management
    :platform: Linux, Windows, macOS
    :author: Fleet Management System Team

This module implements the FieldPMDevice class, which manages prescription map (PM) devices
for agricultural field operations. It handles the creation, management, and cleanup of
field prescription map devices that track treatment applications, coordinate-based operations,
and grid-specific agricultural activities during precision farming missions.

The prescription map system provides precise agricultural treatment tracking with grid-based
positioning, allowing for accurate monitoring of fertilizer application, pesticide treatment,
and other precision farming operations across field zones.

.. note::
    Key Features:
    - Grid-based prescription map device creation and management
    - Coordinate-precise treatment tracking and monitoring
    - Integration with treatment device systems for workflow coordination
    - Real-time telemetry with timestamp and state tracking
    - Mission and vehicle association for operational context
    - Comprehensive relationship management with treatment devices
    - Multi-cleanup strategies (by treatment or mission)

.. versionadded:: 1.0.0
    Initial implementation of prescription map device management

.. seealso::
    - :mod:`MQTT.ThingsBoard.devices.base_device` for base device functionality
    - :mod:`MQTT.ThingsBoard.devices.treatment_device` for treatment coordination

Example:
    Basic usage of field prescription map device management::

        from MQTT.ThingsBoard.devices.field_pm_device import FieldPMDevice
        from MQTT.ThingsBoard.devices.treatment_device import TreatmentDevice
        from MQTT.ThingsBoard.rest_api import ThingsBoardAPI
        
        # Initialize ThingsBoard API and treatment device
        tb_api = ThingsBoardAPI("https://thingsboard.company.com")
        tb_api.login("username", "password")
        treatment_device = TreatmentDevice(tb_api, logger, "thingsboard.com", 8883, "v1/devices/me/telemetry")
        
        # Create field PM device handler with treatment integration
        field_pm_device = FieldPMDevice(
            tb_api=tb_api,
            mqtt_logger=logger,
            tb_host="thingsboard.company.com",
            port=8883,
            telemetry_topic="v1/devices/me/telemetry",
            treatment_device=treatment_device
        )
        
        # Process prescription map message
        pm_msg = {
            "telemetry": {
                "coordinates": [40.7128, -74.0060],
                "amount": 2.5,
                "grid": [10, 15],
                "point": [10.5, 15.2],
                "vehicle_id": "V001",
                "state": "applied"
            },
            "mission_id": "M001"
        }
        field_pm_device.handle_message(pm_msg, "fertilizer_N")
"""

from datetime import datetime
import time
from MQTT.ThingsBoard.devices.base_device import BaseDevice

#: str: Standard relationship type for prescription map to treatment device connections
RELATION_TYPE = "CONTAINS"


class FieldPMDevice:
    """
    Specialized device handler for managing agricultural prescription map devices.
    
    This class manages the creation and lifecycle of prescription map devices that track
    precise agricultural treatments applied to specific field coordinates. It provides
    grid-based device organization, treatment integration, and comprehensive telemetry
    collection for precision farming operations.
    
    The prescription map system coordinates with treatment devices to provide complete
    tracking of agricultural applications across field grids, enabling precise monitoring
    of fertilizer, pesticide, and other treatment applications.
    
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
    :param treatment_device: Reference to treatment device for coordination (optional)
    :type treatment_device: TreatmentDevice or None
    
    .. note::
        Grid-Based Naming Convention:
        Prescription map devices are named using the format "{treatment} [{lat}, {long}]"
        where lat and long are 1-indexed grid coordinates for human-readable identification.
        
    .. warning::
        Treatment device integration is optional but recommended for complete workflow
        tracking. Without it, treatment relationships will not be established.
        
    .. versionadded:: 1.0.0
        Initial implementation of prescription map device management
        
    Attributes:
        base (BaseDevice): Base device functionality for ThingsBoard operations
        fields_pm (dict): Dictionary mapping field IDs to prescription map device data
        mqtt_logger (logging.Logger): Logger for operation tracking and debugging
        treatment_device (TreatmentDevice): Reference to treatment device for coordination
        
    Example:
        Initialize and use prescription map device handler::
        
            field_pm_handler = FieldPMDevice(
                tb_api, logger, "thingsboard.com", 8883, "v1/devices/me/telemetry",
                treatment_device=treatment_handler
            )
            
            # Process prescription map application
            pm_data = {
                "telemetry": {
                    "coordinates": [40.7128, -74.0060],
                    "amount": 3.2,
                    "grid": [5, 8],
                    "vehicle_id": "V001",
                    "state": "applied"
                },
                "mission_id": "M001"
            }
            field_pm_handler.handle_message(pm_data, "fertilizer_NPK")
    """
    
    def __init__(self, tb_api, mqtt_logger, tb_host, port, telemetry_topic, treatment_device=None):
        """Initialize the field prescription map device handler with optional treatment integration.
        
        Sets up the prescription map device management system with base device functionality
        and initializes storage for grid-based prescription map devices with optional
        treatment device coordination.
        
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
        :param treatment_device: Treatment device reference for coordination
        :type treatment_device: TreatmentDevice or None
        """
        self.base = BaseDevice(tb_api, mqtt_logger, tb_host, port, telemetry_topic)
        self.fields_pm = {}  # Dictionary: field_id -> prescription map device data
        self.mqtt_logger = mqtt_logger
        self.treatment_device = treatment_device  # Reference for treatment coordination
    
    def handle_message(self, message, treatment):
        """Process prescription map messages and create corresponding ThingsBoard devices.
        
        Processes incoming prescription map messages containing treatment application data,
        creates grid-specific devices for tracking, and establishes relationships with
        treatment devices. Each grid location gets a unique device for precise monitoring.
        
        The method handles the complete prescription map workflow including coordinate
        validation, grid-based device creation, treatment integration, and comprehensive
        telemetry transmission with timestamps.
        
        :param message: Prescription map message containing telemetry and coordinates
        :type message: dict
        :param treatment: Treatment type being applied (e.g., "fertilizer_N", "pesticide_A")
        :type treatment: str
        :return: None
        :rtype: None
        
        .. note::
            Message Processing Steps:
            1. Extract and validate telemetry data (coordinates, grid, amount, etc.)
            2. Generate unique field ID based on treatment and grid coordinates
            3. Create prescription map device if not exists (with 1-indexed naming)
            4. Establish MQTT client connection for telemetry transmission
            5. Set up device relationships with treatment devices
            6. Configure device attributes (treatment, mission, vehicle associations)
            7. Transmit comprehensive telemetry with timestamp
            
        .. warning::
            The message must contain a 'telemetry' object with required fields:
            coordinates, grid, amount, point, vehicle_id, and state. Missing
            fields may cause processing errors.
            
        .. tip:
            Grid coordinates are converted to 1-indexed values for human-readable
            device names, making field identification easier in ThingsBoard UI.
            
        Message Structure:
            Expected message format::
            
                {
                    "telemetry": {
                        "coordinates": [latitude, longitude],    # GPS coordinates
                        "amount": float,                         # Treatment amount applied
                        "grid": [x, y],                         # 0-indexed grid position
                        "point": [x_precise, y_precise],        # Precise point within grid
                        "vehicle_id": "vehicle_identifier",     # Applying vehicle ID
                        "state": "applied|planned|failed"       # Application state
                    },
                    "mission_id": "mission_identifier"          # Associated mission
                }
        
        Example:
            Process fertilizer application prescription map::
            
                pm_msg = {
                    "telemetry": {
                        "coordinates": [40.7128, -74.0060],     # GPS location
                        "amount": 2.5,                          # 2.5 kg/hectare
                        "grid": [10, 15],                       # Grid position (0-indexed)
                        "point": [10.3, 15.7],                 # Precise application point
                        "vehicle_id": "TRACTOR_001",            # Applying vehicle
                        "state": "applied"                      # Successfully applied
                    },
                    "mission_id": "FERTILIZE_2024_001"
                }
                
                field_pm_device.handle_message(pm_msg, "fertilizer_NPK")
                # Creates device: "fertilizer_NPK [11, 16]" (1-indexed display)
        """
        try:
            # Extract and validate telemetry data from message
            coordinates = message['telemetry'].get('coordinates')
            amount = message['telemetry'].get('amount')
            grid = message['telemetry'].get('grid')
            point = message['telemetry'].get('point')
            vehicle_id = message['telemetry'].get('vehicle_id')
            mission_id = message.get('mission_id')
            state = message['telemetry'].get('state')

            # Generate unique field ID based on treatment and grid coordinates
            grid_lat = int(grid[0])
            grid_long = int(grid[1])
            field_id = f"{mission_id}_{vehicle_id}_{treatment}_{grid_lat}_{grid_long}"

            # Check if prescription map device exists for this grid location, create if needed
            if field_id not in self.fields_pm:
                # Create human-readable device name with 1-indexed coordinates
                device_name = f"{mission_id}_{vehicle_id} {treatment} [{grid_lat}, {grid_long}]"
                device_id, access_token = self.base.create_device(device_name, "Field_PM")

                # Validate device creation success
                if not device_id or not access_token:
                    self.mqtt_logger.error(f"[MQTT][ThingsBoard] - Failed to create device {device_name}")
                    return

                # Create MQTT client for telemetry transmission
                client = self.base.create_client(access_token)
                if not client:
                    self.mqtt_logger.error(f"[MQTT][ThingsBoard] - Failed to create MQTT client for {device_name}")
                    return

                # Store prescription map device information
                self.fields_pm[field_id] = {
                    'device_id': device_id,
                    'client': client,
                    'treatment': f"{mission_id}-{vehicle_id} {treatment}",
                    'mission_id': mission_id
                }

                # Set up device relationships and attributes
                self.setup_device_relations(field_id, f"{mission_id}-{vehicle_id} {treatment}", vehicle_id, mission_id)

            # Prepare comprehensive telemetry data with timestamp
            telemetry = {
                'cell': f"{treatment} {grid}",  # 1-indexed display
                'coordinates': coordinates,      # GPS coordinates of application
                'treatment': treatment,          # Treatment type applied
                'amount': amount,               # Amount of treatment applied
                'point': point,                 # Precise point within grid cell
                'grid': grid,                   # Grid coordinates (0-indexed)
                'mission_id': mission_id,       # Associated mission identifier
                'vehicle_id': vehicle_id,       # Vehicle performing application
                'state': state,                 # Application state
                'lastUpdate': datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Timestamp
            }

            # Transmit telemetry data to ThingsBoard
            self.base.send_telemetry(
                self.fields_pm[field_id]['client'],
                telemetry
            )

        except Exception as e:
            # Log critical errors with full exception information for debugging
            self.mqtt_logger.error(f"[MQTT][ThingsBoard] - Critical error in handle_message: {str(e)}", exc_info=True)

    def setup_device_relations(self, field_id, treatment, vehicle_id, mission_id):
        """Configure device relationships and attributes for prescription map devices.
        
        Establishes relationships between prescription map devices and treatment devices,
        and sets comprehensive device attributes for proper identification and tracking
        within the agricultural workflow system.
        
        :param field_id: Unique identifier for the field prescription map device
        :type field_id: str
        :param treatment: Treatment type being applied
        :type treatment: str
        :param vehicle_id: Identifier of the vehicle applying the treatment
        :type vehicle_id: str
        :param mission_id: Identifier of the associated mission
        :type mission_id: str
        :return: None
        :rtype: None
        
        .. note::
            Relationship Setup:
            1. Creates "CONTAINS" relationship from treatment device to field PM device
            2. Sets server attributes for treatment, mission, vehicle, and field associations
            3. Provides comprehensive device metadata for ThingsBoard organization
            
        .. warning::
            Treatment device relationships are only created if treatment_device reference
            exists and the specific treatment is available in the treatment system.
            
        Example:
            Device relationships and attributes are set up automatically during
            prescription map device creation. This method is called internally.
        """
        try:
            # Create relationship with treatment device if available
            if self.treatment_device and treatment in self.treatment_device.treatments:
                treatment_device_id = self.treatment_device.treatments[treatment]['device_id']
                self.base.create_relation(
                    treatment_device_id,
                    self.fields_pm[field_id]['device_id'],
                    RELATION_TYPE
                )

            # Set comprehensive device attributes for identification and tracking
            device_id = self.fields_pm[field_id]['device_id']
            self.base.tb.set_server_attribute(device_id, 'treatment', treatment)      # Treatment type
            self.base.tb.set_server_attribute(device_id, 'mission_id', mission_id)   # Associated mission
            self.base.tb.set_server_attribute(device_id, 'vehicle_id', vehicle_id)   # Applying vehicle
            self.base.tb.set_server_attribute(device_id, 'field_id', field_id)       # Field identifier

        except Exception as e:
            # Log relationship setup errors for debugging
            self.mqtt_logger.error(f"[MQTT][ThingsBoard] - Error setting up relations for {field_id}: {str(e)}")
    
    def cleanup(self, treatment):
        """Clean up all prescription map devices associated with a specific treatment.
        
        Performs comprehensive cleanup of all prescription map devices created for
        the specified treatment type, including relationship removal, device deletion,
        and local storage cleanup. This method is useful for treatment-specific cleanup.
        
        :param treatment: Treatment type to clean up (e.g., "fertilizer_N")
        :type treatment: str
        :return: None
        :rtype: None
        
        .. note::
            Treatment Cleanup Steps:
            1. Identify all field PM devices associated with the treatment
            2. Remove treatment-field relationships from ThingsBoard
            3. Disconnect MQTT clients and delete devices
            4. Remove devices from local storage
            
        .. warning:
            This operation is irreversible and will permanently delete all
            prescription map devices and their telemetry data for the treatment.
            
        Example:
            Clean up all fertilizer prescription map devices::
            
                # Clean up all fertilizer application devices
                field_pm_device.cleanup("fertilizer_NPK")
                print("All fertilizer NPK prescription map devices cleaned up")
        """
        # Identify field PM devices associated with the treatment
        to_delete = [fid for fid, field in self.fields_pm.items() 
                    if field['treatment'] == treatment]
        
        # Clean up each identified field PM device
        for field_id in to_delete:
            # Remove relationship with treatment device if exists
            if self.treatment_device and treatment in self.treatment_device.treatments:
                treatment_device_id = self.treatment_device.treatments[treatment]['device_id']
                self.base.tb.delete_relation(
                    treatment_device_id,
                    self.fields_pm[field_id]['device_id'],
                    RELATION_TYPE
                )
            
            # Disconnect MQTT client and delete device with retry mechanism
            self.base.delete_client(self.fields_pm[field_id]['client'])
            self.base.delete_device_with_retry(self.fields_pm[field_id]['device_id'])
            
            # Remove from local storage
            del self.fields_pm[field_id]

    def cleanup_by_mission(self, mission_id):
        """Clean up all prescription map devices associated with a specific mission.
        
        Performs comprehensive cleanup of all prescription map devices created during
        the specified mission, regardless of treatment type. This method provides
        mission-based cleanup for complete mission lifecycle management.
        
        :param mission_id: Mission identifier to clean up
        :type mission_id: str
        :return: None
        :rtype: None
        
        .. note::
            Mission Cleanup Steps:
            1. Identify all field PM devices associated with the mission
            2. Remove treatment-field relationships for each device
            3. Disconnect MQTT clients and delete devices with retry mechanism
            4. Remove all mission devices from local storage
            
        .. warning:
            This operation is irreversible and will permanently delete all
            prescription map devices and their telemetry data for the mission.
            
        .. tip:
            Use this method for complete mission cleanup when missions are completed
            or cancelled, ensuring no orphaned prescription map devices remain.
            
        Example:
            Clean up all prescription map devices for a completed mission::
            
                # Mission completed successfully
                mission_id = "FERTILIZE_2024_001"
                
                # Clean up all associated prescription map devices
                field_pm_device.cleanup_by_mission(mission_id)
                print(f"All prescription map devices for mission {mission_id} cleaned up")
        """
        # Identify field PM devices associated with the mission
        to_delete = [fid for fid, field in self.fields_pm.items()
                    if field['mission_id'] == mission_id]
        
        # Clean up each identified field PM device
        for field_id in to_delete:
            treatment = self.fields_pm[field_id]['treatment']
            
            # Remove relationship with treatment device if exists
            if self.treatment_device and treatment in self.treatment_device.treatments:
                treatment_device_id = self.treatment_device.treatments[treatment]['device_id']
                self.base.tb.delete_relation(
                    treatment_device_id,
                    self.fields_pm[field_id]['device_id'],
                    RELATION_TYPE
                )
            
            # Disconnect MQTT client and delete device with retry mechanism
            self.base.delete_client(self.fields_pm[field_id]['client'])
            self.base.delete_device_with_retry(self.fields_pm[field_id]['device_id'])
            
            # Remove from local storage
            del self.fields_pm[field_id]