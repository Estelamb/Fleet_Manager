import time
import random
from abc import ABC, abstractmethod

class Command(ABC):
    """Abstract base class for all drone command types.

    :param related_task: ID of parent task
    :type related_task: int
    :param id: Unique command identifier
    :type id: int
    :param command_type: Command category (e.g., 'NAVIGATION', 'CAMERA')
    :type command_type: str
    :param start_time: Unix timestamp of command initiation
    :type start_time: int
    :param command_status: Current execution state ('Pending'|'Running'|'Completed')
    :type command_status: str

    .. note::
        All concrete commands must implement execute() and result() methods
    """
    
    def __init__(self, related_task: int, id: int, command_type: str, 
                 start_time: int, command_status: str):
        self.related_task = related_task
        self.id = id
        self.command_type = command_type
        self.start_time = start_time
        self.command_status = command_status
    
    @abstractmethod
    def execute(self):
        """Execute command logic. Must be implemented by subclasses."""
        pass
    
    @abstractmethod
    def result(self):
        """Return command outcome. Must be implemented by subclasses.
        
        :return: Tuple containing (command_id, status_message, lat, lon)
        :rtype: tuple
        """
        pass


class Nav_TakeOff(Command):
    """Take off from ground/hand command implementation.

    :param params: Flight parameters in order:
        [0] minimum_pitch (float): Minimum pitch angle during takeoff (degrees)
        [1] yaw_angle (float): Initial heading (degrees true)
        [2] latitude (float): Takeoff latitude (decimal degrees)
        [3] longitude (float): Takeoff longitude (decimal degrees)
    """
    
    def __init__(self, related_task, id, command_type, start_time, 
                 command_status, params):
        super().__init__(related_task, id, command_type, start_time, command_status)
        self.minimun_pitch = params[0]
        self.yaw_angle = params[1]
        self.latitude = params[2]
        self.longitude = params[3]
        
    def execute(self):
        """Simulate takeoff procedure with 10s delay."""
        print("Taking off...")
        time.sleep(20)
        
    def result(self):
        """Return takeoff confirmation with position.
        
        :return: (command_id, status, lat, lon)
        """
        return self.id, "Takeoff successful", self.latitude, self.longitude


class Nav_Land(Command):
    """Land at specified location command implementation.

    :param params: Landing parameters in order:
        [0] minimum_altitude (float): Minimum safe altitude (meters)
        [1] precision_land_mode (int): Landing accuracy mode (0-3)
        [2] yaw_angle (float): Approach heading (degrees)
        [3] latitude (float): Target latitude (decimal degrees)
        [4] longitude (float): Target longitude (decimal degrees)
        [5] landing_altitude (float): Touchdown altitude (meters)
    """
    
    def __init__(self, related_task, id, command_type, start_time, 
                 command_status, params):
        super().__init__(related_task, id, command_type, start_time, command_status)
        self.minimun_altitude = params[0]
        self.precision_land_mode = params[1]
        self.yaw_angle = params[2]
        self.latitude = params[3]
        self.longitude = params[4]
        self.landing_altitude = params[5]
        
    def execute(self):
        """Simulate landing procedure with 10s delay."""
        print("Landing...")
        time.sleep(20)
        
    def result(self):
        """Return landing confirmation with position.
        
        :return: (command_id, status, lat, lon)
        """
        return self.id, "Landing successful", self.latitude, self.longitude


class Nav_Waypoint(Command):
    """Navigate to waypoint command implementation.

    :param params: Navigation parameters in order:
        [0] hold_time (int): Loiter time at waypoint (seconds)
        [1] acceptancer_radius (float): Waypoint acceptance radius (meters)
        [2] pass_waypoint (bool): Continue through waypoint
        [3] yaw_angle (float): Target heading (degrees)
        [4] latitude (float): Waypoint latitude (decimal degrees)
        [5] longitude (float): Waypoint longitude (decimal degrees)
        [6] relative_altitude (float): Altitude relative to takeoff (meters)
    """
    
    def __init__(self, related_task, id, command_type, start_time, 
                 command_status, params):
        super().__init__(related_task, id, command_type, start_time, command_status)
        self.hold_time = params[0]
        self.acceptancer_radius = params[1]
        self.pass_waypoint = params[2]
        self.yaw_angle = params[3]
        self.latitude = params[4]
        self.longitude = params[5]
        self.relative_altitude = params[6]
        
    def execute(self):
        """Simulate waypoint navigation with 10s delay."""
        print("Going to WP...")
        time.sleep(20)
        
    def result(self):
        """Return waypoint confirmation with position.
        
        :return: (command_id, status, lat, lon)
        """
        return self.id, "WP reached", self.latitude, self.longitude


class Nav_Home(Command):
    """Return to home position command implementation.

    :param params: Return parameters:
        [0] landing_permission (bool): Allow automatic landing
    """
    
    def __init__(self, related_task, id, command_type, start_time, 
                 command_status, params):
        super().__init__(related_task, id, command_type, start_time, command_status)
        self.landing_permission = params[0]
        
    def execute(self):
        """Simulate return home with 10s delay."""
        print("Returning home...")
        time.sleep(20)
        
    def result(self):
        """Return home position confirmation.
        
        :return: (command_id, status, None, None)
        """
        return self.id, "Returned home", None, None


class Camera_Image(Command):
    """Image capture command implementation.

    :param params: Camera parameters in order:
        [0] yaw_angle (float): Camera heading (degrees)
        [1] pitch_angle (float): Camera tilt angle (degrees)
        [2] photo_count (int): Number of images to capture
        [3] time_interval (float): Time between captures (seconds)
    """
    
    def __init__(self, related_task, id, command_type, start_time, 
                 command_status, params):
        super().__init__(related_task, id, command_type, start_time, command_status)
        self.yaw_angle = params[0]
        self.pitch_angle = params[1]
        self.photo_count = params[2]
        self.time_interval = params[3]
        
    def execute(self):
        """Simulate photo capture with 1s delay."""
        print("Taking picture...")
        time.sleep(10)
        
    def result(self):
        """Return image capture confirmation.
        
        :return: (command_id, status, None, None)
        """
        return self.id, "Picture taken", None, None


class Analyze_Image(Command):
    """Image analysis command implementation.

    :param params: Analysis parameters in order:
        [0] product (str): Target detection product
        [1] latitude (float): Image location latitude
        [2] longitude (float): Image location longitude
    """
    
    def __init__(self, related_task, id, command_type, start_time, 
                 command_status, params):
        super().__init__(related_task, id, command_type, start_time, command_status)
        self.product = params[0]
        self.latitude = params[1]
        self.longitude = params[2]
        
    def execute(self):
        """Simulate analysis with random result and 10s delay."""
        print("Analyzing image...")
        self.product_amount = random.randint(0, 3)
        time.sleep(10)
        
    def result(self):
        """Return analysis results with location.
        
        :return: (command_id, [product, amount], lat, lon)
        """
        return self.id, [self.product, self.product_amount], self.latitude, self.longitude


class Spray(Command):
    """Spray treatment command implementation.

    :param params: Spray parameters in order:
        [0] product (str): Treatment product name
        [1] product_amount (float): Quantity to dispense (liters)
        [2] latitude (float): Application latitude
        [3] longitude (float): Application longitude
    """
    
    def __init__(self, related_task, id, command_type, start_time, 
                 command_status, params):
        super().__init__(related_task, id, command_type, start_time, command_status)
        self.product = params[0]
        self.product_amount = params[1]
        self.latitude = params[2]
        self.longitude = params[3]
        
    def execute(self):
        """Simulate spraying operation with 5s delay."""
        print("Spraying...")
        time.sleep(10)
        
    def result(self):
        """Return spray operation confirmation.
        
        :return: (command_id, [product, amount], lat, lon)
        """
        return self.id, [self.product, self.product_amount], self.latitude, self.longitude