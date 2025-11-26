"""
This module defines the abstract base class and concrete implementations for
all drone command types, such as navigation, image capture, analysis, and spraying.

The module implements a command pattern where each drone operation is encapsulated
as a command object with standardized execution and result reporting interfaces.

Workflow
--------
1. Commands are instantiated with specific parameters for their operation type
2. The :meth:`execute` method performs the actual drone operation
3. The :meth:`result` method returns standardized feedback about the operation
4. All operations are logged through the provided logger instance

Classes
-------
.. autoclass:: Command
    :members:
.. autoclass:: Nav_TakeOff
    :members:
.. autoclass:: Nav_Land
    :members:
.. autoclass:: Nav_Waypoint
    :members:
.. autoclass:: Nav_Home
    :members:
.. autoclass:: Camera_Image
    :members:
.. autoclass:: Analyze_Image
    :members:
.. autoclass:: Spray
    :members:
"""

import json
import time
import random
import logging
import subprocess
from abc import ABC, abstractmethod
from Sensors.gps_simulator import save_coordinates, get_latest_coordinates 
from Sensors.take_photo import take_photo
from Images.analyze_image import analyze_image
from PrescriptionMap.pm_manager import generate_pm, send_all

class Command(ABC):
    """
    Abstract base class for all drone command types.

    This class defines the common interface and properties that all drone commands
    must implement. It follows the Command pattern to encapsulate drone operations
    as objects with standardized execution and feedback interfaces.

    Parameters
    ----------
    related_task : int
        ID of parent task that contains this command.
    id : int
        Unique command identifier within the system.
    command_type : str
        Command category (e.g., 'NAVIGATION', 'CAMERA', 'ANALYSIS', 'SPRAY').
    start_time : int
        Unix timestamp of command initiation.
    command_status : str
        Current execution state ('NotAssigned'|'NotStarted'|'Running'|'Finished'|'Stopped').
    logger : logging.Logger
        Logger instance for recording command execution events.

    Attributes
    ----------
    related_task : int
        Parent task identifier.
    id : int
        Command unique identifier.
    command_type : str
        Type category of the command.
    start_time : int
        Command initiation timestamp.
    command_status : str
        Current command execution status.
    logger : logging.Logger
        Logger for command events.

    Workflow
    --------
    1. Command is instantiated with required parameters
    2. :meth:`execute` is called to perform the drone operation
    3. :meth:`result` is called to retrieve operation outcome
    4. All steps are logged for monitoring and debugging

    Notes
    -----
    All concrete commands must implement :meth:`execute` and :meth:`result`.
    """
    
    def __init__(self, related_task: int, id: int, command_type: str, 
                 start_time: int, command_status: str, logger: logging.Logger):
        self.related_task = related_task
        self.id = id
        self.command_type = command_type
        self.start_time = start_time
        self.command_status = command_status
        self.logger = logger

    @abstractmethod
    def execute(self):
        """
        Execute the specific command logic.
        
        This method must be implemented by all concrete command subclasses
        to perform the actual drone operation (navigation, imaging, etc.).
        
        Raises
        ------
        NotImplementedError
            If not implemented by subclass.
            
        Notes
        -----
        Implementation should handle all necessary hardware interactions
        and update command status accordingly.
        """
        pass
    
    @abstractmethod
    def result(self):
        """
        Return command execution outcome and status information.
        
        This method must be implemented by all concrete command subclasses
        to provide standardized feedback about the operation results.

        Returns
        -------
        tuple
            Standardized tuple containing (command_id, result_data, latitude, longitude).
            The exact structure varies by command type but always includes:
            - command_id (int): The unique identifier of this command
            - result_data: Command-specific result information
            - latitude (float or None): Final latitude position
            - longitude (float or None): Final longitude position
            
        Raises
        ------
        NotImplementedError
            If not implemented by subclass.
        """
        pass


class Nav_TakeOff(Command):
    """
    Take off from ground or hand launch command implementation.
    
    This command initiates the drone takeoff sequence from either ground level
    or hand launch position, establishing initial flight parameters and heading.

    Parameters
    ----------
    related_task : int
        ID of parent task that contains this command.
    id : int
        Unique command identifier.
    command_type : str
        Command category, typically 'NAVIGATION'.
    start_time : int
        Unix timestamp of command initiation.
    command_status : str
        Current execution state.
    params : list
        Flight parameters in order:
            [0] minimum_pitch (float): Minimum pitch angle during takeoff (degrees)
            [1] yaw_angle (float): Initial heading orientation (degrees true)
            [2] latitude (float): Takeoff location latitude (decimal degrees)
            [3] longitude (float): Takeoff location longitude (decimal degrees)
    logger : logging.Logger
        Logger instance for recording takeoff events.
        
    Attributes
    ----------
    minimun_pitch : float
        Minimum pitch angle constraint during takeoff.
    yaw_angle : float
        Target heading after takeoff completion.
    latitude : float
        Takeoff position latitude coordinate.
    longitude : float
        Takeoff position longitude coordinate.
        
    Workflow
    --------
    1. Initialize takeoff parameters from input list
    2. Execute takeoff sequence with safety checks
    3. Return confirmation and final position coordinates
    """
    
    def __init__(self, related_task, id, command_type, start_time, 
                 command_status, params, logger):
        super().__init__(related_task, id, command_type, start_time, command_status, logger)
        self.minimun_pitch = params[0]
        self.yaw_angle = params[1]
        self.latitude = params[2]
        self.longitude = params[3]
        
    def execute(self):
        """
        Execute the takeoff procedure.
        
        Simulates the drone takeoff sequence including motor startup,
        lift generation, and initial stabilization. The operation includes
        a 1-second delay to represent actual takeoff duration.
        
        Notes
        -----
        In a real implementation, this would interface with flight control
        systems to manage motor speeds, attitude control, and safety checks.
        """
        self.logger.info("[NAV_TAKEOFF] - Taking off...")
        time.sleep(2)
        
    def result(self):
        """
        Return takeoff operation confirmation with final position.

        Returns
        -------
        tuple
            Takeoff result containing:
            - command_id (int): This command's unique identifier
            - status (str): "Takeoff successful" confirmation message
            - latitude (float): Final takeoff position latitude
            - longitude (float): Final takeoff position longitude
        """
        self.logger.info("[NAV_TAKEOFF] - Takeoff successful")
        return self.id, "Takeoff successful", self.latitude, self.longitude


class Nav_Land(Command):
    """
    Precision landing at specified coordinates command implementation.
    
    This command executes a controlled landing sequence at a target location
    with configurable precision and approach parameters.

    Parameters
    ----------
    related_task : int
        ID of parent task that contains this command.
    id : int
        Unique command identifier.
    command_type : str
        Command category, typically 'NAVIGATION'.
    start_time : int
        Unix timestamp of command initiation.
    command_status : str
        Current execution state.
    params : list
        Landing parameters in order:
            [0] minimum_altitude (float): Minimum safe altitude above ground (meters)
            [1] precision_land_mode (int): Landing accuracy mode (0-3, higher = more precise)
            [2] yaw_angle (float): Approach heading orientation (degrees)
            [3] latitude (float): Target landing latitude (decimal degrees)
            [4] longitude (float): Target landing longitude (decimal degrees)
            [5] landing_altitude (float): Final touchdown altitude reference (meters)
    logger : logging.Logger
        Logger instance for recording landing events.
        
    Attributes
    ----------
    minimun_altitude : float
        Safety altitude threshold during approach.
    precision_land_mode : int
        Landing precision level configuration.
    yaw_angle : float
        Final approach heading angle.
    latitude : float
        Target landing position latitude.
    longitude : float
        Target landing position longitude.
    landing_altitude : float
        Reference altitude for touchdown.
        
    Workflow
    --------
    1. Initialize landing parameters and target coordinates
    2. Execute controlled descent with precision guidance
    3. Perform final touchdown sequence
    4. Return confirmation and actual landing position
    """
    
    def __init__(self, related_task, id, command_type, start_time, 
                 command_status, params, logger):
        super().__init__(related_task, id, command_type, start_time, command_status, logger)
        self.minimun_altitude = params[0]
        self.precision_land_mode = params[1]
        self.yaw_angle = params[2]
        self.latitude = params[3]
        self.longitude = params[4]
        self.landing_altitude = params[5]
        
    def execute(self):
        """
        Execute the precision landing procedure.
        
        Simulates the controlled landing sequence including descent planning,
        approach stabilization, and final touchdown. The operation includes
        a 1-second delay to represent actual landing duration.
        
        Notes
        -----
        In a real implementation, this would interface with GPS, altitude sensors,
        and flight control systems to ensure safe and accurate landing.
        """
        self.logger.info("[NAV_LAND] - Landing...")
        time.sleep(2)
        
    def result(self):
        """
        Return landing operation confirmation with final position.

        Returns
        -------
        tuple
            Landing result containing:
            - command_id (int): This command's unique identifier
            - status (str): "Landing successful" confirmation message
            - latitude (float): Actual landing position latitude
            - longitude (float): Actual landing position longitude
        """
        self.logger.info("[NAV_LAND] - Landing successful")
        return self.id, "Landing successful", self.latitude, self.longitude


class Nav_Waypoint(Command):
    """
    Navigate to specific waypoint coordinates command implementation.
    
    This command directs the drone to fly to a specified geographic waypoint
    with configurable loiter behavior, acceptance criteria, and altitude.

    Parameters
    ----------
    related_task : int
        ID of parent task that contains this command.
    id : int
        Unique command identifier.
    command_type : str
        Command category, typically 'NAVIGATION'.
    start_time : int
        Unix timestamp of command initiation.
    command_status : str
        Current execution state.
    params : list
        Navigation parameters in order:
            [0] hold_time (int): Loiter duration at waypoint (seconds)
            [1] acceptancer_radius (float): Waypoint acceptance radius (meters)
            [2] pass_waypoint (bool): True to continue through, False to stop
            [3] yaw_angle (float): Target heading at waypoint (degrees)
            [4] latitude (float): Waypoint target latitude (decimal degrees)
            [5] longitude (float): Waypoint target longitude (decimal degrees)
            [6] relative_altitude (float): Altitude relative to takeoff point (meters)
    logger : logging.Logger
        Logger instance for recording navigation events.
        
    Attributes
    ----------
    hold_time : int
        Duration to maintain position at waypoint.
    acceptancer_radius : float
        Distance threshold for waypoint arrival detection.
    pass_waypoint : bool
        Whether to continue flight or hold at waypoint.
    yaw_angle : float
        Desired heading orientation at waypoint.
    latitude : float
        Target waypoint latitude coordinate.
    longitude : float
        Target waypoint longitude coordinate.
    relative_altitude : float
        Flight altitude above takeoff reference.
        
    Workflow
    --------
    1. Initialize waypoint parameters and target coordinates
    2. Execute navigation to waypoint using GPS guidance
    3. Hold position for specified duration if required
    4. Save coordinates to GPS simulator and return confirmation
    """
    
    def __init__(self, related_task, id, command_type, start_time, 
                 command_status, params, logger):
        super().__init__(related_task, id, command_type, start_time, command_status, logger)
        self.hold_time = params[0]
        self.acceptancer_radius = params[1]
        self.pass_waypoint = params[2]
        self.yaw_angle = params[3]
        self.latitude = params[4]
        self.longitude = params[5]
        self.relative_altitude = params[6]
        
    def execute(self):
        """
        Execute waypoint navigation procedure.
        
        Simulates the drone navigation to the specified waypoint including
        flight path calculation, GPS guidance, and arrival detection.
        The operation includes a 1-second delay to represent flight time.
        
        Notes
        -----
        In a real implementation, this would interface with autopilot systems,
        GPS modules, and flight control algorithms for precise navigation.
        """
        self.logger.info("[NAV_WAYPOINT] - Going to WP...")
        time.sleep(2)
        
    def result(self):
        """
        Return waypoint navigation confirmation with final position.
        
        Updates the GPS simulator with the new coordinates and provides
        confirmation of successful waypoint arrival.

        Returns
        -------
        tuple
            Waypoint result containing:
            - command_id (int): This command's unique identifier
            - status (str): "WP reached" confirmation message
            - latitude (float): Actual arrival position latitude
            - longitude (float): Actual arrival position longitude
        """
        save_coordinates(self.latitude, self.longitude)
        self.logger.info("[NAV_WAYPOINT] - Waypoint reached")
        return self.id, "WP reached", self.latitude, self.longitude


class Nav_Home(Command):
    """
    Return to home position command implementation.
    
    This command directs the drone to return to its predefined home location,
    typically the takeoff point, with optional automatic landing capability.

    Parameters
    ----------
    related_task : int
        ID of parent task that contains this command.
    id : int
        Unique command identifier.
    command_type : str
        Command category, typically 'NAVIGATION'.
    start_time : int
        Unix timestamp of command initiation.
    command_status : str
        Current execution state.
    params : list
        Return-to-home parameters:
            [0] landing_permission (bool): True to allow automatic landing at home
    logger : logging.Logger
        Logger instance for recording return-to-home events.
        
    Attributes
    ----------
    landing_permission : bool
        Whether automatic landing is authorized upon reaching home.
        
    Workflow
    --------
    1. Initialize return-to-home parameters
    2. Send all accumulated prescription map data
    3. Execute navigation back to home coordinates
    4. Optionally perform automatic landing if authorized
    """
    
    def __init__(self, related_task, id, command_type, start_time, 
                 command_status, params, logger):
        super().__init__(related_task, id, command_type, start_time, command_status, logger)
        self.landing_permission = params[0]
        
    def execute(self):
        """
        Execute return-to-home procedure.
        
        Initiates the return flight to the predefined home position and
        transmits all collected prescription map data before departure.
        The operation includes a 1-second delay to represent flight time.
        
        Notes
        -----
        This method calls send_all() to ensure all mission data is transmitted
        before the drone returns to base, preventing data loss.
        """
        self.logger.info("[NAV_HOME] - Returning home...")
        send_all(self.logger)
        time.sleep(2)
        
    def result(self):
        """
        Return home operation confirmation.
        
        Provides confirmation of successful return-to-home completion.
        Position coordinates are None as home position is predefined.

        Returns
        -------
        tuple
            Return-to-home result containing:
            - command_id (int): This command's unique identifier
            - status (str): "Returned home" confirmation message
            - latitude (None): No specific coordinates for home position
            - longitude (None): No specific coordinates for home position
        """
        self.logger.info("[NAV_HOME] - Return home successful")
        return self.id, "Returned home", None, None


class Camera_Image(Command):
    """
    Digital image capture command implementation.
    
    This command controls the drone's camera system to capture high-resolution
    images at the current location with configurable camera settings.

    Parameters
    ----------
    related_task : int
        ID of parent task that contains this command.
    id : int
        Unique command identifier.
    command_type : str
        Command category, typically 'CAMERA'.
    start_time : int
        Unix timestamp of command initiation.
    command_status : str
        Current execution state.
    params : list
        Camera parameters in order:
            [0] yaw_angle (float): Camera heading orientation (degrees)
            [1] pitch_angle (float): Camera tilt angle (degrees, negative = down)
            [2] photo_count (int): Number of sequential images to capture
            [3] time_interval (float): Time delay between captures (seconds)
            [4] camera (str): Camera identifier/configuration to use
    logger : logging.Logger
        Logger instance for recording imaging events.
        
    Attributes
    ----------
    yaw_angle : float
        Camera horizontal orientation angle.
    pitch_angle : float
        Camera vertical tilt angle.
    photo_count : int
        Total number of images to capture.
    time_interval : float
        Interval between sequential captures.
    camera : str
        Camera system identifier or configuration.
        
    Workflow
    --------
    1. Initialize camera parameters and positioning
    2. Retrieve current GPS coordinates for image geotagging
    3. Execute photo capture using configured camera system
    4. Generate filename based on coordinate location
    5. Return confirmation of successful image capture
    """
    
    def __init__(self, related_task, id, command_type, start_time, 
                 command_status, params, logger):
        super().__init__(related_task, id, command_type, start_time, command_status, logger)
        self.yaw_angle = params[0]
        self.pitch_angle = params[1]
        self.photo_count = params[2]
        self.time_interval = params[3]
        self.camera = params[4]
        
    def execute(self):
        """
        Execute image capture procedure.
        
        Retrieves current GPS coordinates, generates a location-based filename,
        and triggers the camera module to capture an image. The operation
        includes a 1-second delay to represent capture and processing time.
        
        Notes
        -----
        The filename format is "{latitude}_{longitude}.jpg" for easy
        geographic identification of captured images.
        """
        self.logger.info("[CAMERA_IMAGE] - Taking picture...")
        lat, lon = get_latest_coordinates()
        filename = f"{lat}_{lon}.jpg"

        take_photo(self.camera, filename, self.logger)

        time.sleep(1)
        
        self.logger.info(f"[CAMERA_IMAGE] - Picture taken successfully as {lat}_{lon}.jpg")

    def result(self):
        """
        Return image capture confirmation.
        
        Provides confirmation of successful image capture completion.
        No specific coordinates are returned as the image is geotagged.

        Returns
        -------
        tuple
            Image capture result containing:
            - command_id (int): This command's unique identifier
            - status (str): "Picture taken" confirmation message
            - latitude (None): No position update needed
            - longitude (None): No position update needed
        """
        
        return self.id, "Picture taken", None, None


class Analyze_Image(Command):
    """
    AI-powered image analysis command implementation.
    
    This command processes captured images using machine learning models to
    detect agricultural conditions and generate prescription map data for
    targeted treatment applications.

    Parameters
    ----------
    related_task : int
        ID of parent task that contains this command.
    id : int
        Unique command identifier.
    command_type : str
        Command category, typically 'ANALYSIS'.
    start_time : int
        Unix timestamp of command initiation.
    command_status : str
        Current execution state.
    params : list
        Analysis parameters in order:
            [0] treatment (str): Target detection treatment type
            [1] latitude (float): Image location latitude (decimal degrees)
            [2] longitude (float): Image location longitude (decimal degrees)
            [3] grid (any): Grid cell identifier for prescription mapping
            [4] pm_types (list): Prescription map type configurations
    logger : logging.Logger
        Logger instance for recording analysis events.
        
    Attributes
    ----------
    treatment : str
        Type of treatment to analyze for (e.g., 'fungicide', 'herbicide').
    latitude : float
        Geographic latitude of analyzed image.
    longitude : float
        Geographic longitude of analyzed image.
    grid : any
        Grid cell identifier for spatial mapping.
    pm_types : list
        Prescription map type configurations.
    amount : dict
        Analysis results containing treatment amounts by type.
        
    Workflow
    --------
    1. Initialize analysis parameters and target conditions
    2. Retrieve current GPS coordinates for accurate positioning
    3. Execute AI image analysis to detect agricultural conditions
    4. Generate prescription map data based on analysis results
    5. Return comprehensive analysis results with location data
    """
    
    def __init__(self, related_task, id, command_type, start_time, 
                 command_status, params, logger):
        super().__init__(related_task, id, command_type, start_time, command_status, logger)
        self.treatment = params[0]
        self.latitude = params[1]
        self.longitude = params[2]
        self.grid = params[3]
        self.pm_types = params[4]
        self.amount = dict()
        
    def execute(self):
        """
        Execute AI-powered image analysis procedure.
        
        Retrieves current GPS coordinates and processes the captured image
        using machine learning models to detect agricultural conditions
        and determine appropriate treatment requirements. The operation
        includes a 1-second delay to represent analysis processing time.
        
        Notes
        -----
        The analyze_image function performs computer vision analysis
        to detect diseases, pests, or other conditions requiring treatment.
        """
        self.logger.info("[ANALYZE_IMAGE] - Analyzing image...")
        self.latitude, self.longitude = get_latest_coordinates()
        self.amount = analyze_image(self.latitude, self.longitude, self.treatment, self.logger)        
        time.sleep(1)
        
    def result(self):
        """
        Return comprehensive image analysis results with prescription data.
        
        Generates prescription map entries based on analysis results and
        returns detailed information about detected conditions and
        recommended treatments.

        Returns
        -------
        tuple
            Analysis result containing:
            - command_id (int): This command's unique identifier
            - result_data (list): Complex result data including:
                [0] treatment (str): Treatment type analyzed
                [1] amount (dict): Detected condition amounts by type
                [2] grid (any): Grid cell identifier
                [3] coordinates (list): [latitude, longitude] of analysis
                [4] pm_types (list): Prescription map configurations
            - latitude (float): Analysis location latitude
            - longitude (float): Analysis location longitude
        """
        self.logger.info("[ANALYZE_IMAGE] - Analysis completed")
        generate_pm(self.pm_types, self.amount, self.grid, self.longitude, self.latitude, self.logger)
        return self.id, [self.treatment, self.amount, self.grid, [self.latitude, self.longitude], self.pm_types], self.latitude, self.longitude


class Spray(Command):
    """
    Precision agricultural spray treatment command implementation.
    
    This command controls the drone's spraying system to apply treatments
    (pesticides, fertilizers, etc.) at specific locations with precise
    dosage control based on prescription map data.

    Parameters
    ----------
    related_task : int
        ID of parent task that contains this command.
    id : int
        Unique command identifier.
    command_type : str
        Command category, typically 'SPRAY'.
    start_time : int
        Unix timestamp of command initiation.
    command_status : str
        Current execution state.
    params : list
        Spray parameters in order:
            [0] treatment (str): Treatment type name (e.g., 'fungicide', 'herbicide')
            [1] treatment_amount (float): Precise quantity to dispense (liters)
            [2] latitude (float): Target application latitude (decimal degrees)
            [3] longitude (float): Target application longitude (decimal degrees)
    logger : logging.Logger
        Logger instance for recording spray events.
        
    Attributes
    ----------
    treatment : str
        Type of treatment being applied.
    treatment_amount : float
        Exact volume of treatment to dispense.
    latitude : float
        Target application latitude coordinate.
    longitude : float
        Target application longitude coordinate.
        
    Workflow
    --------
    1. Initialize spray parameters and target coordinates
    2. Execute precision spraying operation with dosage control
    3. Monitor application progress during 10-second spray cycle
    4. Return confirmation with treatment details and location
    """
    
    def __init__(self, related_task, id, command_type, start_time, 
                 command_status, params, logger):
        super().__init__(related_task, id, command_type, start_time, command_status, logger)
        self.treatment = params[0]
        self.treatment_amount = params[1]
        self.latitude = params[2]
        self.longitude = params[3]
        
    def execute(self):
        """
        Execute precision spray treatment operation.
        
        Activates the drone's spraying system to apply the specified treatment
        at the target location. The operation includes a 10-second duration
        to represent the actual spraying process, which is longer than other
        operations due to the physical application requirements.
        
        Notes
        -----
        In a real implementation, this would control pump systems, nozzles,
        flow rates, and spray pattern optimization for precise application.
        """
        self.logger.info("[SPRAY] - Spraying...")
        time.sleep(2)
        
    def result(self):
        """
        Return spray operation confirmation with treatment details.
        
        Provides confirmation of successful treatment application including
        the specific treatment type, amount applied, and precise location.

        Returns
        -------
        tuple
            Spray result containing:
            - command_id (int): This command's unique identifier
            - treatment_data (list): Treatment details including:
                [0] treatment (str): Type of treatment applied
                [1] treatment_amount (float): Volume successfully dispensed
            - latitude (float): Actual application latitude
            - longitude (float): Actual application longitude
        """
        self.logger.info("[SPRAY] - Spray operation successful")
        return self.id, [self.treatment, self.treatment_amount], self.latitude, self.longitude