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
    def __init__(self, tb_api, mqtt_logger, tb_host, port, telemetry_topic):
        self.base = BaseDevice(tb_api, mqtt_logger, tb_host, port, telemetry_topic)
        self.vehicles = {}
        self.clients = {}
        self.mqtt_logger = mqtt_logger
    
    def handle_message(self, message, missions):
        vehicle_id = message['vehicle_id']
        telemetry = message['telemetry']
        
        self.mqtt_logger.info(f"[VehicleDevice] Processing StateVector for vehicle {vehicle_id}")
        self.mqtt_logger.info(f"[VehicleDevice] Current vehicles: {list(self.vehicles.keys())}")
        
        # Crear dispositivo si no existe
        if vehicle_id not in self.vehicles:
            self.mqtt_logger.info(f"[VehicleDevice] Creating new device for vehicle {vehicle_id}")
            device_id, access_token = self.base.create_device(
                f"Vehicle {vehicle_id}", "Drone"
            )
            
            if not device_id or not access_token:
                self.mqtt_logger.error(f"[VehicleDevice] FAILED to create device for {vehicle_id}")
                return
            else:
                self.mqtt_logger.info(f"[VehicleDevice] Successfully created device {device_id} for {vehicle_id}")

            self.vehicles[vehicle_id] = {
                'device_id': device_id,
                'access_token': access_token
            }
            self.clients[vehicle_id] = self.base.create_client(access_token)
            
            # Verificar que el cliente se creó
            if self.clients[vehicle_id]:
                self.mqtt_logger.info(f"[VehicleDevice] MQTT client created for {vehicle_id}")
            else:
                self.mqtt_logger.error(f"[VehicleDevice] FAILED to create MQTT client for {vehicle_id}")
        else:
            self.mqtt_logger.info(f"[VehicleDevice] Vehicle {vehicle_id} already exists with device_id: {self.vehicles[vehicle_id]['device_id']}")

        vehicle_device_id = self.vehicles[vehicle_id]['device_id']
        client = self.clients[vehicle_id]
        
        self.mqtt_logger.info(f"[VehicleDevice] Sending telemetry for vehicle {vehicle_id} with device {vehicle_device_id}")

        # Enviar telemetría
        telemetry_data = {
            'Time': telemetry['time'],
            'Vehicle ID': telemetry['vehicle_id'],
            'Vehicle Status': telemetry['vehicle_status'],
            'Battery Capacity': telemetry['battery_capacity'],
            'Battery Percentage': telemetry['battery_percentage'],
            'Last Update': telemetry['last_update'],
            'longitude': telemetry['longitude'],
            'latitude': telemetry['latitude'],
            'Altitude': telemetry['altitude'],
            'Roll': telemetry['roll'],
            'Pitch': telemetry['pitch'],
            'Yaw': telemetry['yaw'],
            'Gimbal Pitch': telemetry['gimbal_pitch'],
            'Linear Speed': telemetry['linear_speed']
        }

        self.base.send_telemetry(client, telemetry_data)
        self.mqtt_logger.info(f"[VehicleDevice] Telemetry sent for vehicle {vehicle_id}")
        
        # Intentar crear relaciones con misiones
        self._create_mission_relations(vehicle_id, vehicle_device_id, missions)

    def _create_mission_relations(self, vehicle_id, vehicle_device_id, missions):
        """Crear relaciones con todas las misiones que incluyan este vehículo"""
        self.mqtt_logger.info(f"[VehicleDevice] Checking missions for vehicle {vehicle_id}")
        self.mqtt_logger.info(f"[VehicleDevice] Available missions: {list(missions.keys())}")
        
        for mission_id, mission_data in missions.items():
            mission_vehicles = mission_data.get('vehicles', [])
            self.mqtt_logger.info(f"[VehicleDevice] Mission {mission_id} has vehicles: {mission_vehicles}")
            
            if vehicle_id in mission_vehicles:
                mission_device_id = mission_data.get('device_id')
                self.mqtt_logger.info(f"[VehicleDevice] Vehicle {vehicle_id} belongs to mission {mission_id}")
                self.mqtt_logger.info(f"[VehicleDevice] Mission device ID: {mission_device_id}, Vehicle device ID: {vehicle_device_id}")
                
                if mission_device_id and vehicle_device_id:
                    self.mqtt_logger.info(f"[VehicleDevice] Attempting to create relation: {mission_device_id} -> {vehicle_device_id}")
                    
                    success = self.base.tb.create_relation(
                        mission_device_id,
                        vehicle_device_id,
                        "ASSIGNED_TO"
                    )
                    
                    if success:
                        self.mqtt_logger.info(f"[VehicleDevice] SUCCESS: Created relation mission {mission_id} -> vehicle {vehicle_id}")
                    else:
                        self.mqtt_logger.error(f"[VehicleDevice] FAILED: Could not create relation mission {mission_id} -> vehicle {vehicle_id}")
                else:
                    self.mqtt_logger.error(f"[VehicleDevice] Missing device IDs: mission_device_id={mission_device_id}, vehicle_device_id={vehicle_device_id}")