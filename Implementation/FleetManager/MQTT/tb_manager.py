import json
import logging
import queue
import threading
import time
import requests
import paho.mqtt.client as mqtt

# Configuration
TB_HOST = "https://srv-iot.diatel.upm.es"
USERNAME = "estela.mora.barba@alumnos.upm.es"
PASSWORD = "fleet_manager"

# ThingsBoard MQTT broker details
THINGSBOARD_HOST = "srv-iot.diatel.upm.es"

# MQTT connection settings
PORT = 8883
TELEMETRY_TOPIC = "v1/devices/me/telemetry"

# Callback when connecting to the server
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to ThingsBoard!")
        client.connected_flag = True
    else:
        print(f"Connection failed with code {rc}")
        client.connected_flag = False

class ThingsboardThread(threading.Thread):
    """
    A thread to handle ThingsBoard-related operations, including managing devices,
    telemetry, and relations between devices.
    """
    
    def __init__(self, tb, data_to_tb, mqtt_logger):
        """
        Initialize the ThingsboardThread.

        :param tb: An instance of the ThingsBoardAPI class.
        :type tb: ThingsBoardAPI
        :param data_to_tb: A queue for receiving data to send to ThingsBoard.
        :type data_to_tb: queue.Queue
        :param mqtt_logger: Logger for MQTT-related operations.
        :type mqtt_logger: logging.Logger
        """
        super().__init__()
        self.tb = tb
        self.data_to_tb = data_to_tb
        self.mqtt_logger = mqtt_logger
        self.clients = {'Mission': {}, 'Fields': {}, 'Feedback': {}, 'Vehicle': {}}
        self.missions = {}
        self.vehicles = {}
        self.feedbacks = {}
    
    def run(self):
        """
        Main loop for processing messages from the data queue.
        """
        while True:
            mqtt_message = self.data_to_tb.get()
            mqtt_message_str = ''.join(mqtt_message)
            message = json.loads(mqtt_message_str)
            
            match message['type']:
                case 'Mission':
                    self.mission_message(message)
                    
                case 'Telemetry':
                    self.telemetry_message(message)
                    
                case 'StateVector':
                    self.sv_message(message)
                    
                case 'Finish':
                    self.finish_message(message)

    def mission_message(self, message):
        """
        Handle mission-related messages.

        :param message: The mission message to process.
        :type message: dict
        """
        mission_id = message['mission_id']
        if mission_id not in self.missions:
            self.missions[mission_id] = {
                'device_id': None,
                'access_token': None,
                'fields': [{} for _ in message['fields']],
                'vehicles': message.get('vehicles', [])  # Store vehicle IDs
            }
        else:
            # Ensure existing mission has enough fields (in case of dynamic updates)
            current_fields = len(self.missions[mission_id]['fields'])
            needed_fields = len(message['fields'])
            if needed_fields > current_fields:
                # Extend the fields list with new entries
                for _ in range(needed_fields - current_fields):
                    self.missions[mission_id]['fields'].append({})

        # Create or update mission device
        mission_device_id, access_token = self.create_device(f"Mission {mission_id}", "Mission")
        self.missions[mission_id]['device_id'] = mission_device_id
        self.missions[mission_id]['access_token'] = access_token
        self.missions[mission_id]['vehicles'] = message.get('vehicles', [])

        # Initialize clients for 'Mission' type if not exists
        if 'Mission' not in self.clients:
            self.clients['Mission'] = {}
        self.clients['Mission'][mission_id] = self.create_client(access_token)
                    
        self.send_telemetry(self.clients['Mission'][mission_id], message['telemetry'])

        # Handle fields
        if 'Fields' not in self.clients:
            self.clients['Fields'] = {}
        if mission_id not in self.clients['Fields']:
            self.clients['Fields'][mission_id] = []

        # Update each field's device and client
        for i, field in enumerate(message['fields']):
            # Create field device
            field_device_id, field_access_token = self.create_device(
                f"Field {mission_id}.{i+1}", "Field"
            )
            # Update field entry in mission
            self.missions[mission_id]['fields'][i]['device_id'] = field_device_id
            self.missions[mission_id]['fields'][i]['access_token'] = field_access_token

            # Create client for the field and add to the list
            while i >= len(self.clients['Fields'][mission_id]):
                # Append new client if the list is too short
                self.clients['Fields'][mission_id].append(None)
                
            field_client = self.create_client(field_access_token)
            
            if mission_device_id and field_device_id:
                # Call create_relation for each field
                success = self.tb.create_relation(
                    mission_device_id, 
                    field_device_id, 
                    "FIELD"
                )
                        
            if field_client:
                self.clients['Fields'][mission_id][i] = field_client
                self.send_telemetry(field_client, message['fields'][i])
            else:
                self.mqtt_logger.error(f"[Thingsboard] - Failed to create client for field {i}")

        self.mqtt_logger.info(f"[Thingsboard] - Sent mission {mission_id} data to ThingsBoard")        

    def telemetry_message(self, message):
        """
        Handle telemetry-related messages.

        :param message: The telemetry message to process.
        :type message: dict
        """
        mission_id = message['mission_id']
                    
        # Get next feedback number for this mission
        feedback_count = len(self.feedbacks.get(mission_id, []))
        feedback_number = feedback_count + 1
                    
        # Create feedback device
        feedback_name = f"Feedback {mission_id}.{feedback_number}"
        device_id, access_token = self.create_device(feedback_name, "Feedback")
                    
        if device_id and access_token:
            # Create client and send telemetry once
            self.tb.set_server_attribute(device_id, 'feedback', 'feedback')
            client = self.create_client(access_token)
            if client:
                # Store feedback device
                if mission_id not in self.feedbacks:
                    self.feedbacks[mission_id] = []
                self.feedbacks[mission_id].append({
                    'device_id': device_id,
                    'client': client
                })
                            
                # Create relation to mission
                mission_device_id = self.missions[mission_id].get('device_id')
                if mission_device_id:
                    if self.tb.create_relation(
                        mission_device_id,
                        device_id,
                        "FEEDBACK"
                    ):
                        self.mqtt_logger.info(f"[Thingsboard] - Created Mission→Feedback relation for {mission_id}")
                    else:
                        self.mqtt_logger.error(f"[Thingsboard] - Failed to create Mission→Feedback relation for {mission_id}")
                
                # Send single telemetry
                self.send_telemetry(client, message['telemetry'])
                self.mqtt_logger.info(f"[Thingsboard] - Created feedback device {feedback_name}")
            else:
                self.mqtt_logger.error("[Thingsboard] - Failed to create feedback client")
        else:
            self.mqtt_logger.error("[Thingsboard] - Failed to create feedback device")
        
        for i, field_data in enumerate(message.get('fields', [])):
            if i < len(self.clients['Fields'].get(mission_id, [])):
                self.send_telemetry(self.clients['Fields'][mission_id][i], field_data)
            else:
                self.mqtt_logger.error(f"[Thingsboard] - Field index {i} out of range for mission {mission_id}")
                                       
        self.mqtt_logger.info(f"[Thingsboard] -  Sent mission {mission_id} feedback to ThingsBoard")

    def sv_message(self, message):
        """
        Handle state vector messages.

        :param message: The state vector message to process.
        :type message: dict
        """
        # Handle vehicle data
        vehicle_id = message['vehicle_id']
        self.mqtt_logger.info(f"[Thingsboard] - Received State vector from {vehicle_id}")
                    
        if vehicle_id not in self.vehicles:
            # Create device and access token
            device_id, access_token = self.create_device(f"Vehicle {vehicle_id}", "Drone")
            # Initialize the vehicle entry in the dictionary
            self.vehicles[vehicle_id] = {
                'device_id': device_id,
                'access_token': access_token
            }
            # Create and store the client
            self.clients['Vehicle'][vehicle_id] = self.create_client(access_token)
                        
        vehicle_device_id = self.vehicles[vehicle_id]['device_id']

        # Create relations with associated missions
        for mid, mission in self.missions.items():
            if vehicle_id in mission['vehicles']:
                mission_device_id = mission['device_id']
                if mission_device_id and vehicle_device_id:
                    # Create mission→vehicle relation
                    if self.tb.create_relation(mission_device_id, vehicle_device_id, "ASSIGNED_TO"):
                        self.mqtt_logger.info(f"[Thingsboard] - Created Mission→Vehicle relation for {mid} → {vehicle_id}")
                    else:
                        self.mqtt_logger.error(f"[Thingsboard] - Failed Mission→Vehicle relation for {mid} → {vehicle_id}")

        # Proceed to send telemetry
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

        self.send_telemetry(self.clients['Vehicle'][vehicle_id], telemetry_data)

    def finish_message(self, message):
        """
        Handle finish messages to clean up mission-related data.

        :param message: The finish message to process.
        :type message: dict
        """
        mission_id = message['mission_id']
        mission_data = self.missions.get(mission_id)

        if mission_data:
            # Delete vehicle relations
            mission_device_id = mission_data['device_id']
            if mission_device_id:
                for vehicle_id in mission_data['vehicles']:
                    if vehicle_id in self.vehicles:
                        vehicle_device_id = self.vehicles[vehicle_id]['device_id']
                        if self.tb.delete_relation(mission_device_id, vehicle_device_id, "ASSIGNED_TO"):
                            self.mqtt_logger.info(f"[Thingsboard] - Deleted relation to vehicle {vehicle_id}")
                        else:
                            self.mqtt_logger.error(f"[Thingsboard] - Failed deleting relation to vehicle {vehicle_id}")
                    
        for feedback in self.feedbacks[mission_id]:
            self.delete_client(feedback['client'])
            self.delete_device_with_retry(feedback['device_id'])
            # Delete feedback relation
            mission_device_id = self.missions.get(mission_id, {}).get('device_id')
            if mission_device_id:
                self.tb.delete_relation(
                    mission_device_id,
                    feedback['device_id'],
                    "FEEDBACK"
                )
        del self.feedbacks[mission_id]
                    
        # Existing cleanup code remains...
        self.cleanup_mission(mission_id)
        self.cleanup_mission_fields(mission_id)
        self.remove_mission_data(mission_id)
        self.mqtt_logger.info(f"[Thingsboard] - Completely cleaned up mission {mission_id}")

    def create_device(self, device_name, device_type):
        """
        Create a device in ThingsBoard.

        :param device_name: The name of the device.
        :type device_name: str
        :param device_type: The type of the device.
        :type device_type: str
        :return: A tuple containing the device ID and access token.
        :rtype: tuple
        """
        max_retries = 3  # Increased retries
        for _ in range(max_retries):
            existing_device = self.tb.get_device_by_name(device_name)
            if existing_device:
                existing_device_id = existing_device.get('id', {}).get('id')
                if existing_device_id:
                    self.mqtt_logger.info(f"[Thingsboard] - Deleting existing device {device_name} (ID: {existing_device_id})")
                    if self.tb.delete_device(existing_device_id):
                        time.sleep(1)  # Wait for deletion to propagate
                        self.mqtt_logger.info(f"[Thingsboard] - Deleted existing device {device_name}")
                    else:
                        self.mqtt_logger.error(f"[Thingsboard] - Failed to delete existing device {device_name}")

            # Attempt to create the new device
            device_id = self.tb.create_device(device_name, device_type)
            if device_id:
                access_token = self.tb.get_device_access_token(device_id)
                if access_token:
                    return device_id, access_token
                else:
                    self.mqtt_logger.error(f"[Thingsboard] - Failed to get access token for device {device_name}")
            else:
                self.mqtt_logger.error(f"[Thingsboard] - Failed to create device {device_name}, retrying...")
            
            time.sleep(0.5)  # Add delay between retries
        
        self.mqtt_logger.error(f"[Thingsboard] - Exceeded retry attempts for device {device_name}")
        return None, None

    def create_client(self, access_token):
        """
        Create an MQTT client for a device.

        :param access_token: The access token for the device.
        :type access_token: str
        :return: The created MQTT client.
        :rtype: mqtt.Client
        """
        if not access_token:  # Add validation check
            self.mqtt_logger.error("[Thingsboard] - Invalid access token")
            return None

        client = mqtt.Client()
        client.tls_set()
        client.on_connect = on_connect
        client.username_pw_set(access_token)
        client.connected_flag = False

        try:
            client.connect(host=THINGSBOARD_HOST, port=PORT, keepalive=60)
            client.loop_start()

            # Increase connection wait time
            wait_time = 0
            while not client.connected_flag and wait_time < 10:  # Increased to 10 seconds
                time.sleep(0.5)
                wait_time += 0.5

            if client.connected_flag:
                return client
            client.loop_stop()
            return None
        except Exception as e:
            self.mqtt_logger.error(f"[Thingsboard] - Connection error: {str(e)}")
            return None
        
    def delete_client(self, client):
        """
        Safely disconnect and clean up an MQTT client.

        :param client: The MQTT client to delete.
        :type client: mqtt.Client
        """
        if client is not None:
            try:
                client.loop_stop()
                client.disconnect()
                self.mqtt_logger.debug(f"[Thingsboard] - Disconnected client {client}")
            except Exception as e:
                self.mqtt_logger.error(f"[Thingsboard] - Error disconnecting client: {str(e)}")
            time.sleep(0.5)  # Allow time for cleanup
        
    def send_telemetry(self, client, telemetry):
        """
        Send telemetry data to ThingsBoard.

        :param client: The MQTT client to use for sending telemetry.
        :type client: mqtt.Client
        :param telemetry: The telemetry data to send.
        :type telemetry: dict
        """
        if client is None:
            self.mqtt_logger.error("[Thingsboard] - Cannot send telemetry - client is None")
            return
        try:
            client.publish(TELEMETRY_TOPIC, json.dumps(telemetry))
        except Exception as e:
            self.mqtt_logger.error(f"[Thingsboard] - Publish error: {str(e)}")
    
    def cleanup_mission(self, mission_id):
        """
        Clean up mission-related clients and devices.

        :param mission_id: The ID of the mission to clean up.
        :type mission_id: str
        """
        if mission_id in self.clients['Mission']:
            client = self.clients['Mission'][mission_id]
            if client:
                self.delete_client(client)
            del self.clients['Mission'][mission_id]

        if mission_id in self.missions:
            # Delete mission device
            mission_device_id = self.missions[mission_id].get('device_id')
            if mission_device_id:
                self.delete_device_with_retry(mission_device_id)  # Changed call

    def cleanup_mission_fields(self, mission_id):
        """
        Clean up all field-related clients and devices for a mission.

        :param mission_id: The ID of the mission to clean up.
        :type mission_id: str
        """
        if mission_id in self.clients['Fields']:
            for i, field_client in enumerate(self.clients['Fields'][mission_id]):
                if field_client:
                    self.delete_client(field_client)
                # Delete field device
                if mission_id in self.missions:
                    field_device_id = self.missions[mission_id]['fields'][i].get('device_id')
                    if field_device_id:
                        self.delete_device_with_retry(field_device_id)  # Changed call
            del self.clients['Fields'][mission_id]

    def remove_mission_data(self, mission_id):
        """
        Remove mission data from internal tracking.

        :param mission_id: The ID of the mission to remove.
        :type mission_id: str
        """
        if mission_id in self.missions:
            del self.missions[mission_id]

    def delete_device_with_retry(self, device_id, max_retries=3):
        """
        Delete a device with retries.

        :param device_id: The ID of the device to delete.
        :type device_id: str
        :param max_retries: The maximum number of retries.
        :type max_retries: int
        :return: True if the device was successfully deleted, False otherwise.
        :rtype: bool
        """
        if not device_id:
            return False
    
        for attempt in range(max_retries):
            if self.tb.delete_device(device_id):  # Call the API's delete method
                return True
            time.sleep(1)  # Wait between retries
        self.mqtt_logger.error(f"[Thingsboard] - Failed to delete device {device_id} after {max_retries} attempts")
        return False


class ThingsBoardAPI:
    """
    A class to interact with the ThingsBoard REST API.
    """
    
    def __init__(self, host):
        """
        Initialize the ThingsBoardAPI.

        :param host: The host URL of the ThingsBoard server.
        :type host: str
        """
        self.host = host
        self.token = None
        self.session = requests.Session()
        self.username = None
        self.password = None

    def login(self, username, password):
        """
        Log in to ThingsBoard.

        :param username: The username for authentication.
        :type username: str
        :param password: The password for authentication.
        :type password: str
        :return: True if login was successful, False otherwise.
        :rtype: bool
        """
        self.username = username
        self.password = password
        url = f"{self.host}/api/auth/login"
        headers = {"Content-Type": "application/json"}
        data = {"username": username, "password": password}
        response = self.session.post(url, headers=headers, json=data)
        if response.status_code == 200:
            self.token = response.json().get("token")
            self.session.headers.update({"X-Authorization": f"Bearer {self.token}"})
            return True
        print(f"Login failed: {response.text}")
        return False

    def ensure_auth(self):
        """
        Ensure the API is authenticated.

        :return: True if authentication is valid, False otherwise.
        :rtype: bool
        """
        if not self.token or not self.session.headers.get("X-Authorization"):
            if self.username and self.password:
                return self.login(self.username, self.password)
        return True

    def create_device(self, device_name, device_type="default"):
        """
        Create a device in ThingsBoard.

        :param device_name: The name of the device.
        :type device_name: str
        :param device_type: The type of the device.
        :type device_type: str
        :return: The ID of the created device.
        :rtype: str
        """
        if not self.ensure_auth():
            return None
        url = f"{self.host}/api/device"
        data = {"name": device_name, "type": device_type}
        response = self.session.post(url, json=data)
        if response.ok:
            return response.json().get('id', {}).get('id')
        print(f"Device creation failed: {response.text}")
        return None

    def get_device_access_token(self, device_id):
        """
        Get the access token for a device.

        :param device_id: The ID of the device.
        :type device_id: str
        :return: The access token for the device.
        :rtype: str
        """
        if not self.ensure_auth():
            return None
        url = f"{self.host}/api/device/{device_id}/credentials"
        response = self.session.get(url)
        if response.ok and response.json().get("credentialsType") == "ACCESS_TOKEN":
            return response.json().get("credentialsId")
        print(f"Failed to get access token: {response.text}")
        return None

    def delete_device(self, device_id):
        """
        Delete a device in ThingsBoard.

        :param device_id: The ID of the device to delete.
        :type device_id: str
        :return: True if the device was successfully deleted, False otherwise.
        :rtype: bool
        """
        if not self.ensure_auth():
            return False
        url = f"{self.host}/api/device/{device_id}"
        response = self.session.delete(url)
        if response.status_code == 200:
            print(f"Device {device_id} deleted successfully")
            return True
        else:
            print(f"Device deletion failed: {response.text}")
            return False

    def logout(self):
        """
        Log out from ThingsBoard.

        :return: True if logout was successful, False otherwise.
        :rtype: bool
        """
        url = f"{self.host}/api/auth/logout"
        response = self.session.post(url)
        self.session.close()
        return response.ok
    
    def get_devices_by_type(self, device_type):
        """
        Get all devices of a specific type.

        :param device_type: The type of devices to retrieve.
        :type device_type: str
        :return: A list of devices of the specified type.
        :rtype: list
        """
        url = f"{self.host}/api/tenant/devices"
        params = {
            "type": device_type,
            "pageSize": 100,
            "page": 0
        }
        response = self.session.get(url, params=params)
        if response.ok:
            return response.json().get("data", [])
        else:
            print(f"Failed to fetch devices: {response.text}")
            return []

    def delete_all_devices_by_type(self, device_type):
        """
        Delete all devices of a specific type.

        :param device_type: The type of devices to delete.
        :type device_type: str
        """
        devices = self.get_devices_by_type(device_type)
        for device in devices:
            device_id = device.get('id', {}).get('id')
            if device_id:
                self.delete_device(device_id)
                print(f"Deleted device {device_id}")
                
    def get_device_by_name(self, device_name):
        """
        Get a device by its name.

        :param device_name: The name of the device to retrieve.
        :type device_name: str
        :return: The device details if found, None otherwise.
        :rtype: dict
        """
        if not self.ensure_auth():
            return None
        url = f"{self.host}/api/tenant/devices"
        params = {
            "deviceName": device_name,
            "pageSize": 1,
            "page": 0
        }
        response = self.session.get(url, params=params)
        if response.ok:
            devices = response.json().get("data", [])
            for device in devices:
                if device.get('name') == device_name:
                    return device
        return None
    
    def create_relation(self, from_id, to_id, relation_type):
        """
        Create a relation between two devices.

        :param from_id: The ID of the source device.
        :type from_id: str
        :param to_id: The ID of the target device.
        :type to_id: str
        :param relation_type: The type of relation to create.
        :type relation_type: str
        :return: True if the relation was successfully created, False otherwise.
        :rtype: bool
        """
        if not self.ensure_auth():
            return False
        url = f"{self.host}/api/relation"
        data = {
            "from": {"entityType": "DEVICE", "id": from_id},
            "to": {"entityType": "DEVICE", "id": to_id},
            "type": relation_type
        }
        response = self.session.post(url, json=data)
        if response.ok:
            return True
        else:
            print(f"Failed to create relation: {response.text}")
            return False
        
    def delete_relation(self, from_id, to_id, relation_type):
        """
        Delete a relation between two devices.

        :param from_id: The ID of the source device.
        :type from_id: str
        :param to_id: The ID of the target device.
        :type to_id: str
        :param relation_type: The type of relation to delete.
        :type relation_type: str
        :return: True if the relation was successfully deleted, False otherwise.
        :rtype: bool
        """
        if not self.ensure_auth():
            return False
        url = f"{self.host}/api/relation"
        params = {
            'fromId': from_id,
            'fromType': 'DEVICE',
            'relationType': relation_type,
            'toId': to_id,
            'toType': 'DEVICE'
        }
        response = self.session.delete(url, params=params)
        if response.ok:
            return True
        print(f"Relation deletion failed: {response.text}")
        return False
    
    def set_server_attribute(self, device_id, key, value):
        """
        Set a server attribute for a device.

        :param device_id: The ID of the device.
        :type device_id: str
        :param key: The key of the attribute to set.
        :type key: str
        :param value: The value of the attribute to set.
        :type value: str
        :return: True if the attribute was successfully set, False otherwise.
        :rtype: bool
        """
        if not self.ensure_auth():
            return False
        url = f"{self.host}/api/plugins/telemetry/DEVICE/{device_id}/SERVER_SCOPE"
        response = self.session.post(url, json={key: value})
        if response.ok:
            return True
        print(f"Failed to set server attribute: {response.text}")
        return False
    
def start_tb_manager(data_to_tb: queue.Queue, mqtt_logger: logging.Logger):
    tb = ThingsBoardAPI(TB_HOST)
    if tb.login(USERNAME, PASSWORD):
        tb.delete_all_devices_by_type("Drone")
        tb.delete_all_devices_by_type("Mission")
        tb.delete_all_devices_by_type("Field")
        tb.delete_all_devices_by_type("Feedback")
        # Removed logout to keep session alive
    tb_thread = ThingsboardThread(tb, data_to_tb, mqtt_logger)
    tb_thread.start()