import random
import threading
import queue
import time

class StateVector(threading.Thread):
    
    def __init__(self, vehicle_id : int, latitude, longitude, action_queue, topic_queue):
        super().__init__()
        self.vehicle_id = vehicle_id
        self.vehicle_status = 'Available'
        self.battery = Battery(100, random.randint(80, 100))
        self.last_update = time.strftime('%Y-%m-%d %H:%M:%S')
        self.position = Position(latitude, longitude)
        self.orientation = Orientation()
        self.gimbal_pitch = random.randint(-90, 90)
        self.linear_speed = random.randint(0, 100)
        self.action_queue = action_queue
        self.topic_queue = topic_queue
        
    def run(self):
        self.topic_queue.put(self.get_values())
        
        while True:
            update_values = self.action_queue.get()
            if update_values:
                self.update(update_values['vehicle_status'], update_values['latitude'], update_values['longitude'])
            self.topic_queue.put(self.get_values())
        
    def update(self, vehicle_status : str, longitude, latitude):
        self.vehicle_status = vehicle_status
        self.battery.update_battery()
        self.last_update = time.strftime('%Y-%m-%d %H:%M:%S')
        self.position.update_position(longitude, latitude)
        self.orientation.update_orientation()
        self.gimbal_pitch = random.randint(-90, 90)
        self.linear_speed = random.randint(0, 100)
        
    def get_values(self):
        return {
            'vehicle_id': self.vehicle_id,
            'vehicle_status': self.vehicle_status,
            'battery_capacity': self.battery.battery_capacity,
            'battery_percentage': self.battery.battery_percentage,
            'last_update': self.last_update,
            'longitude': self.position.longitude,
            'latitude': self.position.latitude,
            'altitude': self.position.altitude,
            'roll': self.orientation.roll,
            'pitch': self.orientation.pitch,
            'yaw': self.orientation.yaw,
            'gimbal_pitch': self.gimbal_pitch,
            'linear_speed': self.linear_speed
        }

class Position:
    
    def __init__(self, latitude, longitude):
        self.longitude = longitude
        self.latitude = latitude
        self.altitude = random.uniform(0, 100)

    def update_position(self, latitude, longitude):
        self.longitude = longitude
        self.latitude = latitude
        self.altitude = self.altitude + 1
        
class Orientation:
    
    def __init__(self):
        self.roll = random.uniform(-180, 180)
        self.pitch = random.uniform(-90, 90)
        self.yaw = random.uniform(-180, 180)
    
    def update_orientation(self):
        self.roll = random.uniform(-180, 180)
        self.pitch = random.uniform(-90, 90)
        self.yaw = random.uniform(-180, 180)
    

class Battery:
    
    def __init__(self, battery_capacity : float, battery_percentage : float):
        self.battery_capacity = battery_capacity
        self.battery_percentage = battery_percentage
        
    def update_battery(self):
        self.battery_percentage = self.battery_percentage - 0.5
    

def start_state_vector(vehicle_id : int, longitude, latitude, action_queue, topic_queue):
    
    sv_thread = StateVector(vehicle_id, longitude, latitude, action_queue, topic_queue)
    sv_thread.daemon = True
    sv_thread.start()