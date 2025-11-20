"""
Base Device Management Module

.. module:: base_device
    :synopsis: Core device management functionality for ThingsBoard integration
    :platform: Linux, Windows, macOS
    :author: Fleet Management System Team

This module provides the foundational base class for all ThingsBoard device types
within the fleet management system. It implements common device operations including
creation, MQTT client management, telemetry transmission, and device lifecycle management.

The BaseDevice class serves as the parent class for all specialized device types,
providing standardized methods for ThingsBoard integration, connection management,
and error handling across the entire device ecosystem.

.. note::
    Key Features:
    - Robust device creation with automatic retry mechanisms
    - Secure MQTT client management with TLS encryption
    - Real-time telemetry transmission to ThingsBoard
    - Automatic device cleanup and relationship management
    - Comprehensive error handling and logging integration
    - Connection state monitoring and recovery

.. versionadded:: 1.0.0
    Initial implementation of base device management

.. seealso::
    - :mod:`MQTT.ThingsBoard.rest_api` for ThingsBoard REST API operations
    - :mod:`paho.mqtt.client` for MQTT client functionality

Example:
    Basic usage as a parent class for device implementations::

        from MQTT.ThingsBoard.devices.base_device import BaseDevice
        
        class SensorDevice(BaseDevice):
            def __init__(self, tb_api, mqtt_logger, tb_host, port, telemetry_topic):
                super().__init__(tb_api, mqtt_logger, tb_host, port, telemetry_topic)
                
            def process_sensor_data(self, data):
                # Specialized sensor processing
                device_id, token = self.create_device("sensor_01", "temperature")
                client = self.create_client(token)
                self.send_telemetry(client, data)
"""

import json
import paho.mqtt.client as mqtt
import time
import logging
import ssl # No certificate


class BaseDevice:
    """
    Base class for all ThingsBoard device implementations in the fleet management system.
    
    This class provides the fundamental functionality required for managing IoT devices
    within the ThingsBoard platform. It handles device lifecycle operations, MQTT
    connectivity, telemetry transmission, and relationship management.
    
    The class is designed to be inherited by specialized device types that need
    ThingsBoard integration. It provides standardized methods for common operations
    while allowing specialized classes to implement device-specific logic.
    
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
        This class maintains a dictionary of active MQTT clients to support
        multiple concurrent device connections efficiently.
        
    .. warning::
        Always ensure proper cleanup of MQTT clients using delete_client()
        to prevent resource leaks in long-running applications.
        
    .. versionadded:: 1.0.0
        Initial implementation of base device management
        
    Attributes:
        tb (ThingsBoardAPI): ThingsBoard REST API client instance
        mqtt_logger (logging.Logger): Logger for operation tracking
        tb_host (str): ThingsBoard server hostname
        port (int): MQTT connection port
        telemetry_topic (str): MQTT topic for telemetry data
        clients (dict): Dictionary of active MQTT client connections
        
    Example:
        Inherit from BaseDevice for specialized implementations::
        
            class TemperatureSensor(BaseDevice):
                def __init__(self, tb_api, mqtt_logger, tb_host, port, telemetry_topic):
                    super().__init__(tb_api, mqtt_logger, tb_host, port, telemetry_topic)
                    
                def send_temperature(self, device_name, temperature):
                    device_id, token = self.create_device(device_name, "temperature_sensor")
                    if device_id and token:
                        client = self.create_client(token)
                        self.send_telemetry(client, {"temperature": temperature})
    """
    
    def __init__(self, tb_api, mqtt_logger, tb_host, port, telemetry_topic):
        """Initialize the base device with ThingsBoard connection parameters.
        
        Sets up the device with all necessary components for ThingsBoard integration
        including API client, logging, and connection configuration.
        
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
        self.tb = tb_api
        self.mqtt_logger = mqtt_logger
        self.tb_host = tb_host
        self.port = port
        self.telemetry_topic = telemetry_topic
        self.clients = {}
    
    def create_device(self, device_name, device_type):
        """Create or recreate a device in ThingsBoard with robust retry mechanism.
        
        Attempts to create a new device in ThingsBoard, handling existing devices
        by deleting and recreating them. This ensures a clean device state and
        prevents conflicts from previous device instances.
        
        The method implements a retry mechanism to handle temporary network issues
        or ThingsBoard server load, ensuring reliable device creation in production
        environments.
        
        :param device_name: Unique name for the device within the tenant
        :type device_name: str
        :param device_type: Device type classification for organization
        :type device_type: str
        :return: Tuple of (device_id, access_token) if successful, (None, None) if failed
        :rtype: tuple[str, str] or tuple[None, None]
        
        .. note::
            The method automatically handles existing devices by deleting them
            first, ensuring a clean slate for new device creation.
            
        .. warning::
            Deleting existing devices will remove all associated telemetry data.
            Consider backup procedures if historical data is important.
            
        .. tip::
            Use descriptive device names that include location or function
            information for easier fleet management.
            
        Example:
            Create various types of devices::
            
                # Create a temperature sensor
                device_id, token = self.create_device("temp_sensor_hall_A", "temperature_sensor")
                
                # Create a GPS tracker
                device_id, token = self.create_device("vehicle_tracker_01", "gps_tracker")
                
                if device_id and token:
                    print(f"Device created: {device_id} with token: {token}")
                else:
                    print("Failed to create device after all retries")
        """
        max_retries = 3  # Maximum number of creation attempts
        
        for _ in range(max_retries):
            # Check if device already exists
            existing_device = self.tb.get_device_by_name(device_name)
            if existing_device:
                # Extract device ID from existing device
                existing_device_id = existing_device.get('id', {}).get('id')
                if existing_device_id:
                    # Delete existing device to ensure clean state
                    if self.tb.delete_device(existing_device_id):
                        time.sleep(1)  # Wait for deletion to complete
                        
            # Attempt to create new device
            device_id = self.tb.create_device(device_name, device_type)
            if device_id:
                # Get access token for the new device
                access_token = self.tb.get_device_access_token(device_id)
                if access_token:
                    return device_id, access_token
                    
            # Brief delay before retry
            time.sleep(0.5)
            
        # All retries failed
        return None, None

    def create_client(self, access_token):
        """Create and configure a secure MQTT client for ThingsBoard communication.
        
        Establishes a secure MQTT connection to ThingsBoard using the provided
        access token for authentication. The client is configured with TLS encryption
        and automatic connection monitoring.
        
        The method handles connection establishment, authentication, and initial
        setup required for reliable telemetry transmission to ThingsBoard.
        
        :param access_token: Device access token from ThingsBoard for authentication
        :type access_token: str
        :return: Connected MQTT client if successful, None if connection failed
        :rtype: paho.mqtt.client.Client or None
        
        .. note::
            The client is configured with:
            - TLS encryption for secure communication
            - Username/password authentication using access token
            - Connection state monitoring with timeout
            - Automatic keep-alive mechanism
            
        .. warning::
            Failed connections return None. Always check the return value
            before attempting to use the client for telemetry transmission.
            
        .. tip::
            Store the returned client instance and reuse it for multiple
            telemetry transmissions to optimize connection overhead.
            
        Example:
            Create and use an MQTT client for telemetry::
            
                # Get device credentials
                device_id, token = self.create_device("sensor_01", "temperature")
                
                # Create MQTT client
                client = self.create_client(token)
                if client:
                    # Send telemetry data
                    self.send_telemetry(client, {"temperature": 25.5})
                    
                    # Clean up when done
                    self.delete_client(client)
                else:
                    print("Failed to establish MQTT connection")
        """
        # Validate access token
        if not access_token:
            return None

        # Create and configure MQTT client
        client = mqtt.Client()
        #client.tls_set()  # Enable TLS encryption for secure communication
        
        # No certificate
        client.tls_set(
            ca_certs=None,
            certfile=None,
            keyfile=None,
            cert_reqs=ssl.CERT_NONE,  # No requerir verificación de certificado
            tls_version=ssl.PROTOCOL_TLS
        )
        # No certificate
        client.tls_insecure_set(True)
        
        client.on_connect = self.on_connect  # Set connection callback
        client.username_pw_set(access_token)  # Set authentication credentials
        client.connected_flag = False  # Initialize connection state flag

        try:
            # Attempt connection to ThingsBoard
            client.connect(host=self.tb_host, port=self.port, keepalive=60)
            client.loop_start()  # Start network loop for message processing

            # Wait for connection establishment with timeout
            wait_time = 0
            while not client.connected_flag and wait_time < 10:
                time.sleep(0.5)
                wait_time += 0.5

            # Check if connection was successful
            if client.connected_flag:
                return client
                
            # Connection failed, clean up
            client.loop_stop()
            return None
            
        except Exception as e:
            # Log connection errors and return None
            self.mqtt_logger.error(f" - Connection error: {str(e)}")
            return None
        
    def delete_client(self, client):
        """Safely disconnect and clean up an MQTT client connection.
        
        Performs proper cleanup of an MQTT client by stopping the network loop,
        disconnecting from the server, and allowing time for graceful shutdown.
        This prevents resource leaks and ensures clean connection termination.
        
        :param client: MQTT client instance to disconnect and clean up
        :type client: paho.mqtt.client.Client or None
        :return: None
        :rtype: None
        
        .. note::
            The method handles None clients gracefully and includes exception
            handling to ensure cleanup always completes successfully.
            
        .. tip::
            Always call this method when finished with an MQTT client to
            prevent connection leaks and optimize resource usage.
            
        Example:
            Proper client lifecycle management::
            
                # Create client
                client = self.create_client(access_token)
                
                try:
                    # Use client for telemetry
                    self.send_telemetry(client, telemetry_data)
                finally:
                    # Always clean up, even if errors occur
                    self.delete_client(client)
        """
        if client is not None:
            try:
                # Stop the network processing loop
                client.loop_stop()
                
                # Disconnect from ThingsBoard server
                client.disconnect()
            except Exception:
                # Ignore cleanup exceptions to ensure method completes
                pass
                
            # Brief delay to allow connection cleanup to complete
            time.sleep(0.5)
        
    def send_telemetry(self, client, telemetry):
        """Send telemetry data to ThingsBoard via MQTT.
        
        Publishes telemetry data to ThingsBoard using the configured MQTT client
        and telemetry topic. The data is automatically serialized to JSON format
        for transmission.
        
        :param client: Connected MQTT client for data transmission
        :type client: paho.mqtt.client.Client or None
        :param telemetry: Telemetry data dictionary to send to ThingsBoard
        :type telemetry: dict
        :return: None
        :rtype: None
        
        .. note::
            Telemetry data should be a dictionary with key-value pairs representing
            sensor readings, status information, or other device metrics.
            
        .. warning::
            Ensure the client is connected before calling this method. No validation
            is performed on the client connection state.
            
        .. tip::
            Use descriptive telemetry keys that match your ThingsBoard device
            profile configuration for proper data visualization.
            
        Example:
            Send various types of telemetry data::
            
                # Temperature sensor data
                temp_data = {
                    "temperature": 23.5,
                    "humidity": 65.2,
                    "battery": 87
                }
                self.send_telemetry(client, temp_data)
                
                # GPS location data
                gps_data = {
                    "latitude": 40.7128,
                    "longitude": -74.0060,
                    "altitude": 10.5,
                    "speed": 15.2
                }
                self.send_telemetry(client, gps_data)
        """
        # Validate client availability
        if client is None:
            return
            
        try:
            # Serialize telemetry data to JSON and publish to ThingsBoard
            client.publish(self.telemetry_topic, json.dumps(telemetry))
        except Exception as e:
            # Log publish errors for debugging
            self.mqtt_logger.error(f"Publish error: {str(e)}")
    
    def delete_device_with_retry(self, device_id, max_retries=3):
        """Delete a device from ThingsBoard with automatic retry mechanism.
        
        Attempts to delete a device from ThingsBoard with configurable retry logic
        to handle temporary network issues or server load. This ensures reliable
        device cleanup in production environments.
        
        :param device_id: Unique identifier of the device to delete
        :type device_id: str or None
        :param max_retries: Maximum number of deletion attempts (default: 3)
        :type max_retries: int
        :return: True if deletion successful, False if all retries failed
        :rtype: bool
        
        .. note::
            The method includes automatic delays between retry attempts to
            avoid overwhelming the ThingsBoard server during high load periods.
            
        .. warning::
            Device deletion is permanent and removes all associated telemetry
            data, attributes, and relationships. Ensure proper backup procedures.
            
        .. tip::
            Use this method instead of direct deletion for improved reliability
            in production environments with network variability.
            
        Example:
            Reliable device cleanup with retry logic::
            
                device_id = "device-uuid-to-delete"
                
                # Attempt deletion with default retries
                if self.delete_device_with_retry(device_id):
                    print("Device deleted successfully")
                else:
                    print("Failed to delete device after all retries")
                    
                # Custom retry count for critical operations
                success = self.delete_device_with_retry(device_id, max_retries=5)
        """
        # Validate device ID
        if not device_id:
            return False
            
        # Attempt deletion with retry logic
        for _ in range(max_retries):
            if self.tb.delete_device(device_id):
                return True
                
            # Wait before retry to avoid overwhelming server
            time.sleep(1)
            
        # All retries failed
        return False
    
    def on_connect(self, client, userdata, flags, rc):
        """MQTT connection callback handler for monitoring connection status.
        
        This callback is automatically invoked by the MQTT client when a connection
        attempt completes. It updates the client's connection flag based on the
        result code to enable connection state monitoring.
        
        :param client: MQTT client instance that triggered the callback
        :type client: paho.mqtt.client.Client
        :param userdata: User data passed to the client (unused)
        :type userdata: Any
        :param flags: Connection flags from the broker (unused)
        :type flags: dict
        :param rc: Connection result code (0 = success, >0 = failure)
        :type rc: int
        :return: None
        :rtype: None
        
        .. note::
            Result Codes:
            - 0: Connection successful
            - 1: Incorrect protocol version
            - 2: Invalid client identifier
            - 3: Server unavailable
            - 4: Bad username or password
            - 5: Not authorized
            
        .. tip::
            This method is used internally by the MQTT client and typically
            doesn't need to be called directly by user code.
            
        Example:
            The callback is automatically triggered during connection::
            
                client = mqtt.Client()
                client.on_connect = self.on_connect  # Set callback
                client.connect(host, port)  # This triggers the callback
        """
        if rc == 0:
            # Connection successful
            client.connected_flag = True
        else:
            # Connection failed
            client.connected_flag = False
            
    def create_relation(self, from_id, to_id, relation_type):
        """Create a relationship between two devices in ThingsBoard.
        
        Establishes a directional relationship between two devices using the
        ThingsBoard REST API. Relationships are used to model device hierarchies,
        dependencies, and logical groupings within the IoT fleet.
        
        :param from_id: Source device ID for the relationship
        :type from_id: str
        :param to_id: Target device ID for the relationship
        :type to_id: str
        :param relation_type: Type of relationship (e.g., "Contains", "Manages")
        :type relation_type: str
        :return: True if relationship created successfully, False otherwise
        :rtype: bool
        
        .. note::
            Common relationship types include:
            - "Contains": For parent-child hierarchies
            - "Manages": For controller-device relationships
            - "Uses": For dependency relationships
            - "Located": For location-based relationships
            
        .. warning::
            Both devices must exist in ThingsBoard before creating relationships.
            Invalid device IDs will cause the operation to fail.
            
        .. tip:
            Use consistent relationship types across your fleet for better
            organization and easier querying of device hierarchies.
            
        Example:
            Create device relationships for fleet organization::
            
                # Create gateway-sensor relationship
                gateway_id = "gateway-device-uuid"
                sensor_id = "sensor-device-uuid"
                
                # Gateway contains sensor
                success = self.create_relation(gateway_id, sensor_id, "Contains")
                if success:
                    print("Relationship created successfully")
                else:
                    print("Failed to create relationship")
        """
        try:
            # Attempt to create the relationship using ThingsBoard API
            result = self.tb.create_relation(from_id, to_id, relation_type)
            return result
        except Exception as e:
            # Log exceptions and return failure status
            self.mqtt_logger.error(f"Excepción creando relación: {str(e)}")
            return False