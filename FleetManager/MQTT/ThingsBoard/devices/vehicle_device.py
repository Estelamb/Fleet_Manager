"""
Vehicle Device Module
====================

This module provides the `VehicleDevice` class for managing ThingsBoard devices
that represent agricultural vehicles in the fleet management system.

The `VehicleDevice` class handles the creation, management, and monitoring of ThingsBoard
devices that track vehicle status, location, battery levels, and mission assignments.
It supports various vehicle types including drones, tractors, and other agricultural equipment.

Key Features:
    - Vehicle device lifecycle management
    - Real-time telemetry data collection (GPS, battery, orientation)
    - Mission-vehicle relationship management
    - Vehicle status and health monitoring
    - Integration with mission assignment system
    - Comprehensive telemetry data tracking

Usage Example:
    ::

        vehicle_device = VehicleDevice(tb_api, mqtt_logger, tb_host, port, telemetry_topic)
        vehicle_device.handle_message(vehicle_message, active_missions)

Author: Fleet Management System
Date: 2025
"""

from MQTT.ThingsBoard.devices.base_device import BaseDevice


class VehicleDevice:
    """
    ThingsBoard device manager for agricultural vehicle monitoring.
    
    This class manages ThingsBoard devices that represent vehicles in the agricultural
    fleet management system. Each vehicle gets its own device for tracking real-time
    status, location, battery levels, and mission assignments.
    
    The class maintains a registry of active vehicles with their associated device
    information and MQTT connections. It automatically creates relationships between
    vehicles and their assigned missions, enabling comprehensive fleet monitoring.
    
    Attributes:
        base (BaseDevice): Base device manager for ThingsBoard operations
        vehicles (dict): Registry of active vehicles with device information
        mqtt_logger: Logger instance for MQTT operations
        
    Note:
        Vehicle devices automatically establish relationships with missions when
        vehicles are assigned to specific agricultural operations.
        
    Warning:
        Vehicle telemetry data includes sensitive location information that should
        be handled according to privacy and security requirements.
    
    See Also:
        :class:`BaseDevice`: Base class for ThingsBoard device operations
        :class:`mission_device.MissionDevice`: Mission device manager
        :mod:`MQTT.ThingsBoard.tb_manager`: ThingsBoard connection manager
    """
    
    def __init__(self, tb_api, mqtt_logger, tb_host, port, telemetry_topic):
        """
        Initialize the vehicle device manager.
        
        Sets up the base device manager and initializes the vehicle registry
        for tracking active vehicles and their associated ThingsBoard devices.
        
        Args:
            tb_api: ThingsBoard REST API client instance
            mqtt_logger: Logger instance for MQTT operations and debugging
            tb_host (str): ThingsBoard server hostname or IP address
            port (int): ThingsBoard MQTT port (typically 1883)
            telemetry_topic (str): MQTT topic for telemetry data transmission
            
        Example:
            ::
            
                tb_api = RestClientCE(base_url="http://localhost:8080")
                vehicle_device = VehicleDevice(
                    tb_api=tb_api,
                    mqtt_logger=logger,
                    tb_host="localhost", 
                    port=1883,
                    telemetry_topic="v1/devices/me/telemetry"
                )
        """
        self.base = BaseDevice(tb_api, mqtt_logger, tb_host, port, telemetry_topic)
        self.vehicles = {}  # Registry of active vehicles: {vehicle_id: vehicle_data}
        self.mqtt_logger = mqtt_logger
    
    def handle_message(self, message, missions):
        """
        Process vehicle message and create/update corresponding ThingsBoard device.
        
        This method handles incoming vehicle messages by creating new vehicle devices
        or updating existing ones. It also establishes relationships between vehicles
        and their assigned missions, and sends comprehensive telemetry data including
        location, battery status, orientation, and operational parameters.
        
        The method performs the following operations:
        1. Creates a new ThingsBoard device for the vehicle if it doesn't exist
        2. Establishes MQTT client connection with the device token
        3. Creates relationships with assigned missions
        4. Sends comprehensive telemetry data to the device
        
        Args:
            message (dict): Vehicle message containing vehicle telemetry with keys:
                - vehicle_id (str): Unique identifier for the vehicle
                - telemetry (dict): Vehicle telemetry data including:
                    - time (str): Timestamp of the telemetry
                    - vehicle_id (str): Vehicle identifier
                    - vehicle_status (str): Current operational status
                    - battery_capacity (float): Total battery capacity
                    - battery_percentage (float): Current battery level percentage
                    - last_update (str): Last update timestamp
                    - longitude (float): GPS longitude coordinate
                    - latitude (float): GPS latitude coordinate
                    - altitude (float): Vehicle altitude in meters
                    - roll (float): Roll angle in degrees
                    - pitch (float): Pitch angle in degrees
                    - yaw (float): Yaw angle in degrees
                    - gimbal_pitch (float): Gimbal pitch angle (for drones)
                    - linear_speed (float): Current linear speed
            missions (dict): Active missions registry for relationship creation
                
        Example:
            ::
            
                message = {
                    'vehicle_id': 'DRONE_001',
                    'telemetry': {
                        'time': '2025-01-15T14:30:00Z',
                        'vehicle_id': 'DRONE_001',
                        'vehicle_status': 'ACTIVE',
                        'battery_capacity': 5000,
                        'battery_percentage': 85.5,
                        'last_update': '2025-01-15T14:30:00Z',
                        'longitude': -3.7038,
                        'latitude': 40.4168,
                        'altitude': 50.0,
                        'roll': 0.2,
                        'pitch': -0.1,
                        'yaw': 45.0,
                        'gimbal_pitch': -15.0,
                        'linear_speed': 5.2
                    }
                }
                vehicle_device.handle_message(message, active_missions)
                
        Note:
            The vehicle device is created with device type "Drone" but can represent
            any type of agricultural vehicle. Mission relationships are automatically
            created based on vehicle assignments in the missions registry.
            
        Warning:
            Telemetry data includes GPS coordinates and should be handled securely
            according to privacy and operational security requirements.
        """
        vehicle_id = message['vehicle_id']
                    
        # Create vehicle device if it doesn't exist
        if vehicle_id not in self.vehicles:
            device_id, access_token = self.base.create_device(f"Vehicle {vehicle_id}", "Drone")
            self.vehicles[vehicle_id] = {
                'device_id': device_id,
                'access_token': access_token,
                'client': self.base.create_client(access_token)
            }

        vehicle_device_id = self.vehicles[vehicle_id]['device_id']

        # Create relationships with assigned missions
        for mid, mission in missions.items():
            if vehicle_id in mission['vehicles']:
                mission_device_id = mission['device_id']
                if mission_device_id and vehicle_device_id:
                    self.base.tb.create_relation(
                        mission_device_id, 
                        vehicle_device_id, 
                        "ASSIGNED_TO"
                    )

        # Prepare comprehensive telemetry data
        telemetry_data = {
            'Time': message['telemetry']['time'],
            'Vehicle ID': message['telemetry']['vehicle_id'],
            'Vehicle Status': message['telemetry']['vehicle_status'],
            'Battery Capacity': message['telemetry']['battery_capacity'],
            'Battery Percentage': message['telemetry']['battery_percentage'],
            'Last Update': message['telemetry']['last_update'],
            'longitude': message['telemetry']['longitude'],
            'latitude': message['telemetry']['latitude'],
            'Altitude': message['telemetry']['altitude'],
            'Roll': message['telemetry']['roll'],
            'Pitch': message['telemetry']['pitch'],
            'Yaw': message['telemetry']['yaw'],
            'Gimbal Pitch': message['telemetry']['gimbal_pitch'],
            'Linear Speed': message['telemetry']['linear_speed']
        }

        # Send telemetry data to ThingsBoard

        self.base.send_telemetry(
            self.vehicles[vehicle_id]['client'], 
            telemetry_data
        )