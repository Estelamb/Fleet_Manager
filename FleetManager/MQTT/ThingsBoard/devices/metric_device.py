"""
Metric Device Management Module

.. module:: metric_device
    :synopsis: Specialized device handler for vehicle system metrics and performance monitoring
    :platform: Linux, Windows, macOS
    :author: Fleet Management System Team

This module implements the MetricDevice class, which manages system metric collection
devices for vehicle fleet monitoring. It handles the creation, management, and cleanup
of metric devices that track vehicle performance, system health, and operational
parameters during fleet operations.

The metric system provides comprehensive monitoring capabilities for vehicle-mounted
systems (typically Raspberry Pi 5 devices), including CPU usage, memory consumption,
network statistics, and custom operational metrics for fleet management.

.. note::
    Key Features:
    - Dynamic metric device creation per vehicle
    - Real-time system performance monitoring
    - Vehicle-specific metric collection and transmission
    - Comprehensive telemetry data handling for system health
    - Efficient resource management and cleanup
    - Support for Raspberry Pi 5 and similar embedded systems

.. versionadded:: 1.0.0
    Initial implementation of metric device management

.. seealso::
    - :mod:`MQTT.ThingsBoard.devices.base_device` for base device functionality
    - :mod:`MQTT.ThingsBoard.devices.vehicle_device` for vehicle coordination

Example:
    Basic usage of metric device management::

        from MQTT.ThingsBoard.devices.metric_device import MetricDevice
        from MQTT.ThingsBoard.rest_api import ThingsBoardAPI
        
        # Initialize ThingsBoard API
        tb_api = ThingsBoardAPI("https://thingsboard.company.com")
        tb_api.login("username", "password")
        
        # Create metric device handler
        metric_device = MetricDevice(
            tb_api=tb_api,
            mqtt_logger=logger,
            tb_host="thingsboard.company.com",
            port=8883,
            telemetry_topic="v1/devices/me/telemetry"
        )
        
        # Process vehicle system metrics
        metric_msg = {
            "vehicle_id": "V001",
            "telemetry": {
                "cpu_usage": 45.2,
                "memory_usage": 78.5,
                "temperature": 62.1,
                "disk_usage": 34.7,
                "network_rx": 1024768,
                "network_tx": 892345
            }
        }
        metric_device.handle_message(metric_msg)
"""

from MQTT.ThingsBoard.devices.base_device import BaseDevice


class MetricDevice:
    """
    Specialized device handler for managing vehicle system metrics and performance monitoring.
    
    This class manages the creation and lifecycle of metric devices that monitor
    system performance and operational parameters of vehicle-mounted computing systems.
    It provides real-time telemetry collection for fleet health monitoring and
    performance optimization.
    
    The metric system is designed to work with embedded systems like Raspberry Pi 5
    devices mounted on vehicles, collecting system health data, performance metrics,
    and operational statistics for comprehensive fleet monitoring.
    
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
        Device Type Classification:
        Metric devices are created with type "RPI5" to indicate Raspberry Pi 5
        systems, but can be adapted for other embedded computing platforms.
        
    .. warning::
        Metric devices must be properly cleaned up when vehicles are decommissioned
        to prevent resource accumulation and maintain system performance.
        
    .. versionadded:: 1.0.0
        Initial implementation of metric device management
        
    Attributes:
        base (BaseDevice): Base device functionality for ThingsBoard operations
        metrics (dict): Dictionary mapping vehicle IDs to metric device data
        mqtt_logger (logging.Logger): Logger for operation tracking and debugging
        
    Example:
        Initialize and use metric device handler::
        
            metric_handler = MetricDevice(tb_api, logger, "thingsboard.com", 8883, "v1/devices/me/telemetry")
            
            # Process vehicle system metrics
            system_metrics = {
                "vehicle_id": "TRUCK_001",
                "telemetry": {
                    "cpu_usage": 42.5,
                    "memory_usage": 67.8,
                    "disk_usage": 28.3,
                    "temperature": 58.9,
                    "uptime": 86400,
                    "load_average": 0.75
                }
            }
            metric_handler.handle_message(system_metrics)
    """
    
    def __init__(self, tb_api, mqtt_logger, tb_host, port, telemetry_topic):
        """Initialize the metric device handler with ThingsBoard integration.
        
        Sets up the metric device management system with base device functionality
        and initializes storage for vehicle-specific metric devices.
        
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
        self.metrics = {}  # Dictionary: vehicle_id -> metric device data
        self.mqtt_logger = mqtt_logger
    
    def handle_message(self, message):
        """Process metric messages and create corresponding vehicle system monitoring devices.
        
        Creates metric devices for vehicle system monitoring, establishes MQTT connections,
        and transmits system performance telemetry data. Each vehicle gets a dedicated
        metric device for comprehensive system health tracking.
        
        The method handles the complete metric collection workflow including device
        creation for new vehicles and real-time telemetry transmission for system
        performance monitoring.
        
        :param message: Metric message containing vehicle ID and telemetry data
        :type message: dict
        :return: None
        :rtype: None
        
        .. note::
            Message Processing Steps:
            1. Extract vehicle ID from the message
            2. Create metric device if not exists for the vehicle
            3. Establish MQTT client connection for telemetry transmission
            4. Store device information for future metric transmissions
            5. Transmit system metric telemetry data to ThingsBoard
            
        .. warning::
            The message must contain a 'vehicle_id' field for device identification
            and a 'telemetry' object with metric data. Missing fields will prevent
            proper metric collection.
            
        .. tip:
            Metric devices are automatically named "Vehicle {vehicle_id}" for easy
            identification in ThingsBoard dashboards and device management.
            
        Message Structure:
            Expected message format::
            
                {
                    "vehicle_id": "vehicle_identifier",
                    "telemetry": {
                        "cpu_usage": float,          # CPU utilization percentage
                        "memory_usage": float,       # Memory utilization percentage
                        "disk_usage": float,         # Disk utilization percentage
                        "temperature": float,        # System temperature in Celsius
                        "uptime": int,              # System uptime in seconds
                        "load_average": float,       # System load average
                        "network_rx": int,          # Network bytes received
                        "network_tx": int,          # Network bytes transmitted
                        "battery_level": float,      # Battery level percentage (if applicable)
                        "gps_quality": int,         # GPS signal quality (if applicable)
                        "custom_metrics": {}        # Additional vehicle-specific metrics
                    }
                }
        
        Example:
            Process various types of vehicle system metrics::
            
                # Standard system metrics
                system_msg = {
                    "vehicle_id": "TRACTOR_001",
                    "telemetry": {
                        "cpu_usage": 35.7,
                        "memory_usage": 62.3,
                        "disk_usage": 18.9,
                        "temperature": 55.4,
                        "uptime": 172800,           # 48 hours
                        "load_average": 0.65
                    }
                }
                metric_device.handle_message(system_msg)
                
                # Extended metrics with networking and GPS
                extended_msg = {
                    "vehicle_id": "DRONE_005",
                    "telemetry": {
                        "cpu_usage": 78.2,
                        "memory_usage": 84.1,
                        "temperature": 71.5,
                        "battery_level": 67.8,
                        "gps_quality": 8,           # GPS satellites
                        "network_rx": 2048576,
                        "network_tx": 1536789,
                        "flight_time": 1847,        # Custom metric
                        "altitude": 120.5           # Custom metric
                    }
                }
                metric_device.handle_message(extended_msg)
        """
        # Extract vehicle identifier from message
        vehicle_id = message['vehicle_id']
        
        # Create metric device if not exists for this vehicle
        if vehicle_id not in self.metrics:
            # Generate descriptive device name for vehicle metrics
            device_name = f"RPI5 - Vehicle {vehicle_id}"
            
            # Create ThingsBoard device with RPI5 type for embedded systems
            device_id, access_token = self.base.create_device(device_name, "RPI5")
            
            if device_id and access_token:
                # Create MQTT client for metric telemetry transmission
                client = self.base.create_client(access_token)
                
                # Store metric device information for future transmissions
                self.metrics[vehicle_id] = {
                    'device_id': device_id,
                    'client': client
                }
        
        # Transmit vehicle system metrics telemetry if device exists and telemetry data available
        if vehicle_id in self.metrics and 'telemetry' in message:
            self.base.send_telemetry(self.metrics[vehicle_id]['client'], message['telemetry'])
    
    def cleanup(self, vehicle_id):
        """Clean up metric device associated with a specific vehicle.
        
        Performs comprehensive cleanup of the metric device created for the
        specified vehicle, including MQTT client disconnection, device deletion
        from ThingsBoard, and removal from local storage. This ensures proper
        resource management when vehicles are decommissioned or removed from service.
        
        :param vehicle_id: Unique identifier of the vehicle to clean up
        :type vehicle_id: str
        :return: None
        :rtype: None
        
        .. note::
            Cleanup Operations:
            1. Disconnect MQTT client for the vehicle's metric device
            2. Delete metric device from ThingsBoard using retry mechanism
            3. Remove vehicle metric data from local storage
            
        .. warning:
            This operation is irreversible and will permanently delete the
            metric device and all its associated telemetry data from ThingsBoard.
            
        .. tip:
            Call this method when vehicles are permanently removed from the fleet
            or when metric collection is no longer needed for specific vehicles.
            
        Example:
            Clean up metric device for decommissioned vehicle::
            
                # Vehicle being removed from fleet
                vehicle_id = "TRACTOR_001"
                
                # Clean up associated metric device
                metric_device.cleanup(vehicle_id)
                
                print(f"Metric device for vehicle {vehicle_id} cleaned up")
                
        Cleanup Process:
            The method uses the retry mechanism from base device functionality
            to ensure reliable device deletion even under network stress or
            ThingsBoard server load conditions, maintaining system reliability.
        """
        # Check if vehicle has metric device to clean up
        if vehicle_id in self.metrics:
            # Disconnect and clean up MQTT client
            self.base.delete_client(self.metrics[vehicle_id]['client'])
            
            # Delete metric device from ThingsBoard with retry mechanism
            self.base.delete_device_with_retry(self.metrics[vehicle_id]['device_id'])
            
            # Remove vehicle metric data from local storage
            del self.metrics[vehicle_id]