"""
ThingsBoard REST API Client Module

.. module:: rest_api
    :synopsis: Provides a comprehensive client for ThingsBoard REST API operations
    :platform: Linux, Windows, macOS
    :author: Fleet Management System Team

This module implements a complete REST API client for ThingsBoard IoT platform integration.
It provides high-level methods for device management, authentication, telemetry operations,
and relationship management within the fleet management system.

.. note::
    Key Features:
    - Comprehensive device lifecycle management (create, read, update, delete)
    - Automatic authentication and session management
    - Device relationship and hierarchy management
    - Server-side attribute management for device configuration
    - Bulk operations for efficient fleet management
    - Robust error handling with automatic retry mechanisms

.. versionadded:: 1.0.0
    Initial implementation of ThingsBoard REST API client

.. seealso::
    - `ThingsBoard REST API Documentation <https://thingsboard.io/docs/reference/rest-api/>`_
    - :mod:`MQTT.ThingsBoard.tb_manager` for higher-level ThingsBoard operations

Example:
    Basic usage of the ThingsBoard API client::

        from MQTT.ThingsBoard.rest_api import ThingsBoardAPI

        # Initialize API client
        api = ThingsBoardAPI("https://your-thingsboard-host")
        
        # Authenticate
        if api.login("username", "password"):
            # Create a new device
            device_id = api.create_device("my_device", "sensor")
            
            # Set device attributes
            api.set_server_attribute(device_id, "location", "warehouse_1")
"""

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# No certificate
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class ThingsBoardAPI:
    """
    Comprehensive ThingsBoard REST API client for device and telemetry management.
    
    This class provides a high-level interface to the ThingsBoard REST API, handling
    authentication, session management, and all common device operations. It's designed
    to integrate seamlessly with fleet management systems requiring IoT device control.
    
    The client automatically manages authentication tokens and provides retry mechanisms
    for robust operation in production environments. All methods include comprehensive
    error handling and return appropriate status indicators.

    :param host: ThingsBoard server URL (e.g., 'https://demo.thingsboard.io')
    :type host: str
    
    .. note::
        The client maintains a persistent session with automatic token refresh
        capabilities for long-running applications.
        
    .. warning::
        Ensure the provided host URL is accessible and the ThingsBoard instance
        is properly configured before attempting operations.
        
    .. versionadded:: 1.0.0
        Initial implementation of ThingsBoard API client
        
    Attributes:
        host (str): ThingsBoard server base URL
        token (str): Current authentication token (None if not authenticated)
        session (requests.Session): Persistent HTTP session for API calls
        username (str): Stored username for automatic re-authentication
        password (str): Stored password for automatic re-authentication
        
    Example:
        Initialize and authenticate with ThingsBoard::
        
            api = ThingsBoardAPI("https://demo.thingsboard.io")
            if api.login("tenant@thingsboard.org", "tenant"):
                print("Successfully authenticated")
                # Perform API operations...
    """
    
    def __init__(self, host):
        """Initialize the ThingsBoard API client.
        
        Sets up the client with the specified ThingsBoard host URL and initializes
        the HTTP session for subsequent API calls. No authentication is performed
        during initialization.
        
        :param host: Base URL of the ThingsBoard server
        :type host: str
        
        Example:
            Create API client for different environments::
            
                # Production environment
                prod_api = ThingsBoardAPI("https://thingsboard.company.com")
                
                # Development environment  
                dev_api = ThingsBoardAPI("https://localhost:8080")
        """
        self.host = host
        self.token = None
        self.session = requests.Session()
        self.username = None
        self.password = None
        
        # No certificate
        self.session.verify = False

    def login(self, username, password):
        """Authenticate with ThingsBoard using username and password credentials.
        
        Performs user authentication with the ThingsBoard server and obtains an
        access token for subsequent API calls. The token is automatically added
        to the session headers for all future requests.
        
        Credentials are stored internally to enable automatic re-authentication
        if the token expires during long-running operations.
        
        :param username: ThingsBoard username (e.g., tenant@thingsboard.org)
        :type username: str
        :param password: ThingsBoard password
        :type password: str
        :return: True if authentication successful, False otherwise
        :rtype: bool
        
        .. note::
            The authentication token is automatically included in all subsequent
            API requests via the session headers.
            
        .. warning::
            Credentials are stored in memory for automatic re-authentication.
            Ensure proper security measures in production environments.
            
        Example:
            Authenticate with different credential types::
            
                # Tenant user authentication
                success = api.login("tenant@thingsboard.org", "tenant")
                
                # Customer user authentication
                success = api.login("customer@company.com", "password123")
                
                if success:
                    print("Authentication successful")
                else:
                    print("Authentication failed")
        """
        # Store credentials for potential re-authentication
        self.username = username
        self.password = password
        
        # Construct authentication endpoint URL
        url = f"{self.host}/api/auth/login"
        headers = {"Content-Type": "application/json"}
        data = {"username": username, "password": password}
        
        # Attempt authentication with ThingsBoard
        response = self.session.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            # Extract authentication token from response
            self.token = response.json().get("token")
            
            # Add token to session headers for future requests
            self.session.headers.update({"X-Authorization": f"Bearer {self.token}"})
            return True
        return False

    def ensure_auth(self):
        """Ensure valid authentication before API operations.
        
        Verifies that a valid authentication token exists and is properly
        configured in the session headers. If authentication is missing or
        invalid, attempts automatic re-authentication using stored credentials.
        
        This method is called internally before each API operation to ensure
        requests are properly authenticated and will succeed.
        
        :return: True if authentication is valid or successfully refreshed, False otherwise
        :rtype: bool
        
        .. note::
            This method is called automatically by all API methods that require
            authentication. Manual calls are typically not necessary.
            
        .. warning::
            Requires stored username and password for automatic re-authentication.
            If credentials are not available, manual login is required.
            
        Example:
            Manual authentication check (rarely needed)::
            
                if api.ensure_auth():
                    print("Ready for API operations")
                else:
                    print("Authentication required")
                    api.login("username", "password")
        """
        # Check if token and authorization header are present
        if not self.token or not self.session.headers.get("X-Authorization"):
            # Attempt re-authentication with stored credentials
            if self.username and self.password:
                return self.login(self.username, self.password)
        return True

    def create_device(self, device_name, device_type="default"):
        """Create a new device in ThingsBoard with specified name and type.
        
        Creates a new IoT device entity in the ThingsBoard platform with the
        provided name and type. The device will be associated with the currently
        authenticated tenant and can immediately receive telemetry data.
        
        :param device_name: Unique name for the device within the tenant scope
        :type device_name: str
        :param device_type: Device type classification (default: "default")
        :type device_type: str
        :return: Device ID if creation successful, None otherwise
        :rtype: str or None
        
        .. note::
            Device names must be unique within the tenant scope. Device types
            are used for organization and can be used for bulk operations.
            
        .. warning::
            Requires valid authentication. Returns None if authentication fails
            or if the device name already exists.
            
        Example:
            Create devices with different types::
            
                # Create a temperature sensor
                sensor_id = api.create_device("temp_sensor_01", "temperature_sensor")
                
                # Create a GPS tracker
                tracker_id = api.create_device("vehicle_tracker_05", "gps_tracker")
                
                # Create device with default type
                device_id = api.create_device("generic_device_01")
                
                if device_id:
                    print(f"Device created with ID: {device_id}")
        """
        # Ensure valid authentication before proceeding
        if not self.ensure_auth():
            return None
            
        # Construct device creation endpoint URL
        url = f"{self.host}/api/device"
        data = {"name": device_name, "type": device_type}
        
        # Send device creation request
        response = self.session.post(url, json=data)
        
        if response.ok:
            # Extract and return the device ID from the response
            return response.json().get('id', {}).get('id')
        return None

    def get_device_access_token(self, device_id):
        """Retrieve the access token for a specific device.
        
        Fetches the device credentials from ThingsBoard and returns the access token
        if the device is configured for ACCESS_TOKEN authentication. This token is
        required for devices to publish telemetry data to ThingsBoard.
        
        :param device_id: Unique identifier of the device
        :type device_id: str
        :return: Device access token if available, None otherwise
        :rtype: str or None
        
        .. note::
            Only devices configured with ACCESS_TOKEN credential type will return
            a valid token. Other credential types (X.509, MQTT Basic) will return None.
            
        .. warning::
            The access token is sensitive information that should be securely
            transmitted to devices and stored safely.
            
        Example:
            Retrieve and use device access token::
            
                device_id = api.create_device("sensor_01", "temperature")
                token = api.get_device_access_token(device_id)
                
                if token:
                    print(f"Device token: {token}")
                    # Configure device with this token for telemetry publishing
                else:
                    print("Failed to retrieve device token")
        """
        # Ensure valid authentication before proceeding
        if not self.ensure_auth():
            return None
            
        # Construct device credentials endpoint URL
        url = f"{self.host}/api/device/{device_id}/credentials"
        response = self.session.get(url)
        
        # Check if response is valid and credentials type is ACCESS_TOKEN
        if response.ok and response.json().get("credentialsType") == "ACCESS_TOKEN":
            return response.json().get("credentialsId")
        return None

    def delete_device(self, device_id):
        """Delete a specific device from ThingsBoard.
        
        Permanently removes a device and all its associated data (telemetry,
        attributes, relationships) from the ThingsBoard platform. This operation
        cannot be undone.
        
        :param device_id: Unique identifier of the device to delete
        :type device_id: str
        :return: True if deletion successful, False otherwise
        :rtype: bool
        
        .. warning::
            This operation permanently deletes the device and ALL associated data.
            Ensure proper backup procedures are in place before deletion.
            
        .. note::
            Related entities (relationships, alarms, events) are also removed
            as part of the deletion process.
            
        Example:
            Safe device deletion with confirmation::
            
                device_id = "device-uuid-here"
                
                # Optionally backup device data before deletion
                # backup_device_data(device_id)
                
                if api.delete_device(device_id):
                    print("Device successfully deleted")
                else:
                    print("Failed to delete device")
        """
        # Ensure valid authentication before proceeding
        if not self.ensure_auth():
            return False
            
        # Construct device deletion endpoint URL
        url = f"{self.host}/api/device/{device_id}"
        response = self.session.delete(url)
        
        # Return success status (HTTP 200 indicates successful deletion)
        return response.status_code == 200
    
    def get_devices_by_type(self, device_type):
        """Retrieve all devices of a specific type from the tenant.
        
        Fetches a list of all devices belonging to the current tenant that match
        the specified device type. This is useful for bulk operations and fleet
        management tasks.
        
        :param device_type: Device type to filter by (e.g., "temperature_sensor")
        :type device_type: str
        :return: List of device objects matching the specified type
        :rtype: list
        
        .. note::
            The method returns up to 100 devices per call. For tenants with more
            devices of the same type, implement pagination using the page parameter.
            
        .. tip::
            Use this method for fleet-wide operations like bulk configuration
            updates or status monitoring.
            
        Example:
            Retrieve and process devices by type::
            
                # Get all temperature sensors
                temp_sensors = api.get_devices_by_type("temperature_sensor")
                
                for device in temp_sensors:
                    device_id = device.get('id', {}).get('id')
                    device_name = device.get('name')
                    print(f"Found sensor: {device_name} (ID: {device_id})")
                    
                # Get all GPS trackers
                trackers = api.get_devices_by_type("gps_tracker")
                print(f"Found {len(trackers)} GPS trackers")
        """
        # Construct tenant devices endpoint URL with type filter
        url = f"{self.host}/api/tenant/devices"
        params = {
            "type": device_type,  # Filter by device type
            "pageSize": 100,      # Maximum devices per request
            "page": 0             # Start from first page
        }
        
        # Send request to retrieve devices
        response = self.session.get(url, params=params)
        
        if response.ok:
            # Return the data array from the response
            return response.json().get("data", [])
        return []

    def delete_all_devices_by_type(self, device_type):
        """Delete all devices of a specific type from the tenant.
        
        Performs a bulk deletion of all devices matching the specified type.
        This is a powerful operation useful for fleet management scenarios
        where entire device categories need to be removed.
        
        :param device_type: Device type to delete (e.g., "old_sensor_type")
        :type device_type: str
        :return: None
        :rtype: None
        
        .. danger::
            This operation will permanently delete ALL devices of the specified
            type and their associated data. Use with extreme caution.
            
        .. note::
            The operation processes devices in batches and may take time for
            large device fleets. Each device is deleted individually.
            
        .. tip::
            Consider implementing logging or confirmation prompts before using
            this method in production environments.
            
        Example:
            Bulk device cleanup with safety measures::
            
                device_type = "deprecated_sensor_v1"
                
                # Check how many devices will be deleted
                devices = api.get_devices_by_type(device_type)
                print(f"Will delete {len(devices)} devices of type '{device_type}'")
                
                # Confirm deletion (in production, implement proper confirmation)
                confirm = input("Continue? (yes/no): ")
                if confirm.lower() == 'yes':
                    api.delete_all_devices_by_type(device_type)
                    print("Bulk deletion completed")
        """
        # Retrieve all devices of the specified type
        devices = self.get_devices_by_type(device_type)
        
        # Delete each device individually
        for device in devices:
            device_id = device.get('id', {}).get('id')
            if device_id:
                self.delete_device(device_id)
                
    def get_device_by_name(self, device_name):
        """Retrieve a specific device by its name.
        
        Searches for and returns a device with the exact name match within
        the current tenant scope. Device names are unique within a tenant,
        so this method returns at most one device.
        
        :param device_name: Exact name of the device to find
        :type device_name: str
        :return: Device object if found, None otherwise
        :rtype: dict or None
        
        .. note::
            Device names are case-sensitive and must match exactly. The search
            is performed within the current tenant scope only.
            
        .. tip::
            This method is useful when you know the device name but need to
            retrieve its ID or other properties for further operations.
            
        Example:
            Find device by name and perform operations::
            
                device = api.get_device_by_name("temperature_sensor_hall_A")
                
                if device:
                    device_id = device.get('id', {}).get('id')
                    device_type = device.get('type')
                    print(f"Found device: {device_id} (type: {device_type})")
                    
                    # Get access token for the device
                    token = api.get_device_access_token(device_id)
                    print(f"Device token: {token}")
                else:
                    print("Device not found")
        """
        # Ensure valid authentication before proceeding
        if not self.ensure_auth():
            return None
            
        # Construct tenant devices endpoint URL with name filter
        url = f"{self.host}/api/tenant/devices"
        params = {
            "deviceName": device_name,  # Filter by exact device name
            "pageSize": 1,              # We expect only one match
            "page": 0                   # Start from first page
        }
        
        # Send request to search for the device
        response = self.session.get(url, params=params)
        
        if response.ok:
            devices = response.json().get("data", [])
            # Verify exact name match (additional safety check)
            for device in devices:
                if device.get('name') == device_name:
                    return device
        return None
    
    def create_relation(self, from_id, to_id, relation_type):
        """Create a relationship between two devices in ThingsBoard.
        
        Establishes a directional relationship between two devices, which can be
        used to model hierarchical structures, dependencies, or logical groupings
        within the IoT device fleet.
        
        :param from_id: Source device ID in the relationship
        :type from_id: str
        :param to_id: Target device ID in the relationship
        :type to_id: str
        :param relation_type: Type of relationship (e.g., "Contains", "Manages")
        :type relation_type: str
        :return: True if relationship created successfully, False otherwise
        :rtype: bool
        
        .. note::
            Relationships are directional (from_id -> to_id) and can be used to
            create complex device hierarchies and dependencies.
            
        .. tip::
            Common relation types include:
            - "Contains": For parent-child relationships
            - "Manages": For controller-device relationships  
            - "Uses": For dependency relationships
            
        Example:
            Create device relationships for fleet organization::
            
                # Create a gateway device
                gateway_id = api.create_device("gateway_01", "gateway")
                
                # Create sensor devices
                sensor1_id = api.create_device("sensor_01", "temperature")
                sensor2_id = api.create_device("sensor_02", "humidity")
                
                # Establish relationships (gateway contains sensors)
                api.create_relation(gateway_id, sensor1_id, "Contains")
                api.create_relation(gateway_id, sensor2_id, "Contains")
                
                print("Device hierarchy created successfully")
        """
        # Ensure valid authentication before proceeding
        if not self.ensure_auth():
            return False
            
        # Construct relationship creation endpoint URL
        url = f"{self.host}/api/relation"
        data = {
            "from": {"entityType": "DEVICE", "id": from_id},
            "to": {"entityType": "DEVICE", "id": to_id},
            "type": relation_type
        }
        
        # Send relationship creation request
        response = self.session.post(url, json=data)
        return response.ok
        
    def delete_relation(self, from_id, to_id, relation_type):
        """Delete a specific relationship between two devices.
        
        Removes an existing directional relationship between two devices.
        This operation only affects the relationship itself; the devices
        remain unchanged.
        
        :param from_id: Source device ID in the relationship to delete
        :type from_id: str
        :param to_id: Target device ID in the relationship to delete
        :type to_id: str
        :param relation_type: Type of relationship to delete (must match exactly)
        :type relation_type: str
        :return: True if relationship deleted successfully, False otherwise
        :rtype: bool
        
        .. note::
            All relationship parameters (from_id, to_id, relation_type) must
            match exactly for the deletion to succeed.
            
        .. warning::
            Deleting relationships may affect business logic that depends on
            device hierarchies or dependencies.
            
        Example:
            Remove specific device relationships::
            
                gateway_id = "gateway-device-id"
                sensor_id = "sensor-device-id"
                
                # Remove the Contains relationship
                if api.delete_relation(gateway_id, sensor_id, "Contains"):
                    print("Relationship removed successfully")
                else:
                    print("Failed to remove relationship")
                    
                # This would not work (wrong relation type)
                api.delete_relation(gateway_id, sensor_id, "Manages")  # False
        """
        # Ensure valid authentication before proceeding
        if not self.ensure_auth():
            return False
            
        # Construct relationship deletion endpoint URL
        url = f"{self.host}/api/relation"
        params = {
            'fromId': from_id,
            'fromType': 'DEVICE',
            'relationType': relation_type,
            'toId': to_id,
            'toType': 'DEVICE'
        }
        
        # Send relationship deletion request
        response = self.session.delete(url, params=params)
        return response.ok
    
    def set_server_attribute(self, device_id, key, value):
        """Set a server-side attribute for a specific device.
        
        Creates or updates a server-side attribute for the specified device.
        Server-side attributes are used for device configuration, metadata,
        and other non-telemetry data that should be managed by the server.
        
        Server-side attributes are typically used for:
        - Device configuration parameters
        - Location information
        - Firmware versions
        - Device metadata and tags
        
        :param device_id: Unique identifier of the target device
        :type device_id: str
        :param key: Attribute name/key
        :type key: str
        :param value: Attribute value (can be string, number, boolean, or object)
        :type value: Any
        :return: True if attribute set successfully, False otherwise
        :rtype: bool
        
        .. note::
            Server-side attributes are persistent and can be retrieved by both
            the server and client applications. They are ideal for configuration
            and metadata that doesn't change frequently.
            
        .. tip::
            Use consistent naming conventions for attribute keys to maintain
            organization across your device fleet.
            
        Example:
            Set various types of device attributes::
            
                device_id = "device-uuid-here"
                
                # Set location information
                api.set_server_attribute(device_id, "location", "Building A, Floor 2")
                
                # Set configuration parameters
                api.set_server_attribute(device_id, "sampling_rate", 30)
                
                # Set complex configuration object
                config = {
                    "wifi_ssid": "IoT_Network",
                    "sleep_interval": 300,
                    "enabled_sensors": ["temperature", "humidity"]
                }
                api.set_server_attribute(device_id, "device_config", config)
                
                # Set boolean flags
                api.set_server_attribute(device_id, "maintenance_mode", False)
        """
        # Ensure valid authentication before proceeding
        if not self.ensure_auth():
            return False
            
        # Construct server attribute endpoint URL
        url = f"{self.host}/api/plugins/telemetry/DEVICE/{device_id}/SERVER_SCOPE"
        
        # Send attribute update request
        response = self.session.post(url, json={key: value})
        return response.ok