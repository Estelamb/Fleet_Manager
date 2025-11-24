"""
This module implements a threaded vehicle state management system with:
- Continuous state vector updates
- Position/orientation simulation
- Battery consumption modeling
- Thread-safe queue communication

Classes
-------
StateVector
    Threaded vehicle state manager
Position
    Geographic position tracker
Orientation
    Vehicle attitude simulator
Battery
    Battery consumption model

Functions
---------
start_state_vector
    Initialize and start state vector thread
"""

import random
import threading
import queue
import time

class StateVector(threading.Thread):
    """Threaded vehicle state manager with queue-based communication.

    :param vehicle_id: Unique vehicle identifier
    :type vehicle_id: int
    :param latitude: Initial latitude in decimal degrees
    :type latitude: float
    :param longitude: Initial longitude in decimal degrees
    :type longitude: float
    :param action_queue: Input queue for command updates (consumer)
    :type action_queue: queue.Queue
    :param topic_queue: Output queue for state publications (producer)
    :type topic_queue: queue.Queue

    :ivar vehicle_status: Current operational status ('Available'|'Busy'|'Charging')
    :vartype vehicle_status: str
    :ivar battery: Battery state model
    :vartype battery: Battery
    :ivar position: Geographic position tracker
    :vartype position: Position
    :ivar orientation: Vehicle attitude simulation
    :vartype orientation: Orientation
    """
    
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
        """Main state update loop with queue processing.
        
        1. Publishes initial state
        2. Processes incoming commands from action_queue
        3. Updates simulation values
        4. Publishes updated state to topic_queue
        
        .. note:: Runs continuously until thread termination
        """
        
        self.topic_queue.put(self.get_values())
        
        while True:
            update_values = self.action_queue.get()
            if update_values:
                self.update(update_values['vehicle_status'], update_values['latitude'], update_values['longitude'])
            self.topic_queue.put(self.get_values())
        
    def update(self, vehicle_status : str, longitude, latitude):
        """Update vehicle state with new command parameters.
        
        :param vehicle_status: New operational status
        :type vehicle_status: str
        :param longitude: Target longitude in decimal degrees
        :type longitude: float
        :param latitude: Target latitude in decimal degrees
        :type latitude: float
        """
        self.vehicle_status = vehicle_status
        self.battery.update_battery()
        self.last_update = time.strftime('%Y-%m-%d %H:%M:%S')
        self.position.update_position(longitude, latitude)
        self.orientation.update_orientation()
        self.gimbal_pitch = random.randint(-90, 90)
        self.linear_speed = random.randint(0, 100)
        
    def get_values(self):
        """Package current state into dictionary format.
        
        :return: Complete vehicle state snapshot
        :rtype: dict
        """
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
    """Geographic position tracker with altitude simulation.
    
    :param latitude: Initial latitude in decimal degrees
    :type latitude: float
    :param longitude: Initial longitude in decimal degrees
    :type longitude: float
    """
    def __init__(self, latitude, longitude):
        self.longitude = longitude
        self.latitude = latitude
        self.altitude = random.uniform(0, 100)

    def update_position(self, latitude, longitude):
        self.longitude = longitude
        self.latitude = latitude
        self.altitude = self.altitude + 1
        
class Orientation:
    """Vehicle attitude simulator with random walk model."""
    def __init__(self):
        self.roll = random.uniform(-180, 180)
        self.pitch = random.uniform(-90, 90)
        self.yaw = random.uniform(-180, 180)
    
    def update_orientation(self):
        self.roll = random.uniform(-180, 180)
        self.pitch = random.uniform(-90, 90)
        self.yaw = random.uniform(-180, 180)
    

class Battery:
    """Battery consumption model with linear discharge.
    
    :param battery_capacity: Total capacity in watt-hours
    :type battery_capacity: float
    :param battery_percentage: Initial charge percentage
    :type battery_percentage: float
    """
    def __init__(self, battery_capacity : float, battery_percentage : float):
        self.battery_capacity = battery_capacity
        self.battery_percentage = battery_percentage
        
    def update_battery(self):
        self.battery_percentage = self.battery_percentage - 0.5
    

def start_state_vector(vehicle_id : int, longitude, latitude, action_queue, topic_queue):
    """Initialize and start state vector management thread.
    
    :param vehicle_id: Unique vehicle identifier
    :type vehicle_id: int
    :param longitude: Initial longitude in decimal degrees
    :type longitude: float
    :param latitude: Initial latitude in decimal degrees
    :type latitude: float
    :param action_queue: Command input queue
    :type action_queue: queue.Queue
    :param topic_queue: State output queue
    :type topic_queue: queue.Queue
    
    Example:
        Start state tracking for drone 5::
            
            action_q = queue.Queue()
            topic_q = queue.Queue()
            start_state_vector(5, 40.7128, -74.0060, action_q, topic_q)
    """
    sv_thread = StateVector(vehicle_id, longitude, latitude, action_queue, topic_queue)
    sv_thread.daemon = True
    sv_thread.start()