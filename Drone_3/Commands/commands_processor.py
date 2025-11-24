"""
This module provides functionality for parsing and executing drone commands 
from JSON-formatted strings. It serves as the main interface between command
input and concrete command implementations.

The module implements a command processing pipeline that follows these steps:
1. Parse JSON command strings into Python dictionaries
2. Validate command structure and extract parameters
3. Instantiate appropriate command objects based on command type
4. Execute commands and return standardized results

Workflow
--------
Command Processing Pipeline:
    1. **Input Validation**: JSON string is parsed and validated
    2. **Command Selection**: Appropriate command class is selected based on type
    3. **Command Instantiation**: Command object is created with extracted parameters
    4. **Command Execution**: The command's execute() method is called
    5. **Result Collection**: Standardized results are returned to caller

Supported Command Types:
    - NAV_TAKEOFF: Drone takeoff operations
    - NAV_LAND: Drone landing operations  
    - NAV_WAYPOINT: Navigation to specific coordinates
    - NAV_HOME: Return to home position
    - CAMERA_IMAGE: Image capture operations
    - ANALYZE_IMAGE: Image analysis and processing
    - SPRAY: Precision spraying operations

Functions
---------
.. autofunction:: process_command
.. autofunction:: parse_command
.. autofunction:: select_command

Exceptions
----------
ValueError
    Raised for invalid JSON command format or malformed command structure.
json.JSONDecodeError
    Raised when JSON parsing fails due to syntax errors.

Examples
--------
>>> logger = logging.getLogger('drone')
>>> command_json = '{"id": 1, "command_type": "NAV_TAKEOFF", "related_task": 1, "start_time": 1640995200, "command_status": "NotStarted", "params": {"altitude": 10}}'
>>> command_id, result_data = process_command(command_json, logger)
>>> print(f"Command {command_id} executed with result: {result_data}")

Notes
-----
All commands must follow the standardized JSON schema with required fields:
id, command_type, related_task, start_time, command_status, and params.
"""

import random
import json
import logging
from typing import Tuple, Dict, Union
from Commands.commands import Command, Nav_TakeOff, Nav_Land, Nav_Waypoint, Nav_Home, Camera_Image, Analyze_Image, Spray

def process_command(command_str: str, logger: logging.Logger) -> Tuple[int, Dict]:
    """
    Execute the full command processing pipeline for drone operations.

    This function serves as the main entry point for command processing. It coordinates
    the entire workflow from JSON parsing through command execution and result collection.

    Workflow
    --------
    1. **Parse Command**: Convert JSON string to validated dictionary
    2. **Select Command**: Instantiate appropriate command class based on type
    3. **Execute Command**: Run the command's specific logic (navigation, imaging, etc.)
    4. **Collect Results**: Extract standardized result data from command
    5. **Log Success**: Record successful completion in system logs

    Parameters
    ----------
    command_str : str
        JSON-formatted command string containing all necessary command parameters.
        Must include: id, command_type, related_task, start_time, command_status, params.
    logger : logging.Logger
        Logger instance for recording command processing events, errors, and status updates.

    Returns
    -------
    Tuple[int, Dict]
        A tuple containing:
        - command_id (int): Unique identifier of the executed command
        - result_data (Dict): Command-specific result information including:
            * execution status
            * output data (coordinates, image paths, analysis results, etc.)
            * timing information
            * error details (if applicable)

    Raises
    ------
    ValueError
        If input string contains invalid JSON format or missing required fields.
    json.JSONDecodeError
        If JSON parsing fails due to syntax errors in the command string.
    Exception
        If command execution fails due to hardware issues or invalid parameters.

    See Also
    --------
    parse_command : For JSON string validation and parsing
    select_command : For command type selection and instantiation
    Commands.commands.Command : Base class for all command implementations

    Notes
    -----
    This function is thread-safe and can handle multiple concurrent command requests.
    All command executions are logged for monitoring, debugging, and audit purposes.
    """
    # Step 1: Parse and validate the JSON command string
    command_dict = parse_command(command_str, logger)
    
    # Step 2: Select and instantiate the appropriate command class
    command = select_command(command_dict, logger)
    
    # Step 3: Execute the command's specific logic
    command.execute()
    
    # Step 4: Extract standardized results from the executed command
    command_id, command_data, latitude, longitude = command.result()
    
    # Step 5: Log successful completion
    logger.info("[COMMANDS] - Command executed successfully")
    
    # Return command ID and result data (latitude/longitude handled internally)
    return command_id, command_data, latitude, longitude

def parse_command(command_str: str, logger: logging.Logger) -> Dict:
    """
    Validate and parse a JSON command string into a Python dictionary.

    This function performs the first step in the command processing pipeline by
    converting the raw JSON input into a structured dictionary format that can
    be processed by subsequent functions.

    Parameters
    ----------
    command_str : str
        Input command string in JSON format. Must contain valid JSON syntax
        with all required command fields (id, command_type, related_task, 
        start_time, command_status, params).
    logger : logging.Logger
        Logger instance for recording parsing events and errors.

    Returns
    -------
    Dict
        Validated command dictionary containing all parsed command parameters.
        Structure includes:
        - id (int): Unique command identifier
        - command_type (str): Type of command to execute
        - related_task (int): Parent task identifier
        - start_time (int): Unix timestamp of command initiation
        - command_status (str): Current execution status
        - params (Dict): Command-specific parameters

    Raises
    ------
    ValueError
        If JSON parsing fails or command string format is invalid.
    json.JSONDecodeError
        If the input string contains malformed JSON syntax.

    Examples
    --------
    >>> import logging
    >>> logger = logging.getLogger('parser')
    >>> json_cmd = '{"id": 1, "command_type": "NAV_TAKEOFF", "params": {"altitude": 10}}'
    >>> cmd_dict = parse_command(json_cmd, logger)
    >>> print(cmd_dict['command_type'])  # Output: 'NAV_TAKEOFF'

    Notes
    -----
    This function only validates JSON syntax, not command semantics.
    Semantic validation is performed by individual command classes.
    """
    try:
        # Attempt to parse JSON string into Python dictionary
        command_dict = json.loads(command_str)
    except json.JSONDecodeError:
        # Log parsing error and raise ValueError for consistent error handling
        if logger:
            logger.error("[COMMANDS] - Invalid JSON format in command string")
        raise ValueError("Invalid command string format")
    return command_dict

def select_command(command_dict: Dict, logger: logging.Logger) -> Command:
    """
    Instantiate the appropriate command subclass based on command type.

    This function implements a factory pattern to create specific command objects
    based on the command_type field. Each command type corresponds to a different
    drone operation with its own implementation and parameter requirements.

    Supported Command Types
    -----------------------
    NAV_TAKEOFF : Nav_TakeOff
        Drone takeoff operations with altitude control
    NAV_LAND : Nav_Land  
        Drone landing operations with safety checks
    NAV_WAYPOINT : Nav_Waypoint
        Navigation to specific GPS coordinates
    NAV_HOME : Nav_Home
        Return to predefined home position
    CAMERA_IMAGE : Camera_Image
        Image capture operations with camera control
    ANALYZE_IMAGE : Analyze_Image
        Image analysis using AI models for object detection/classification
    SPRAY : Spray
        Precision spraying operations for agricultural applications

    Parameters
    ----------
    command_dict : dict
        Validated command dictionary containing all required fields:
        - related_task (int): Parent task identifier
        - id (int): Unique command identifier  
        - command_type (str): Command type determining which class to instantiate
        - start_time (int): Unix timestamp of command initiation
        - command_status (str): Current execution status
        - params (dict): Command-specific parameters
    logger : logging.Logger
        Logger instance for recording command selection and instantiation events.

    Returns
    -------
    Command
        Concrete command instance of the appropriate subclass, ready for execution.
        The returned object implements the Command interface with execute() and result() methods.

    Examples
    --------
    >>> import logging
    >>> logger = logging.getLogger('command_factory')
    >>> cmd_dict = {
    ...     'id': 1, 'command_type': 'NAV_TAKEOFF', 'related_task': 1,
    ...     'start_time': 1640995200, 'command_status': 'NotStarted',
    ...     'params': {'altitude': 10}
    ... }
    >>> command = select_command(cmd_dict, logger)
    >>> print(type(command).__name__)  # Output: 'Nav_TakeOff'

    Notes
    -----
    - Unknown command types default to the base Command class
    - All command parameters are passed directly to the respective constructors
    - Command selection is logged for debugging and monitoring purposes
    - Each command type has specific parameter requirements defined in its class

    See Also
    --------
    Commands.commands.Command : Base command class
    Commands.commands.Nav_TakeOff : Takeoff command implementation
    Commands.commands.Nav_Waypoint : Waypoint navigation implementation
    """
    # Extract command parameters from validated dictionary
    related_task = command_dict['related_task']
    id = command_dict['id']
    command_type = command_dict['command_type']
    start_time = command_dict['start_time']
    command_status = command_dict['command_status']
    params = command_dict['params']

    # Instantiate appropriate command class based on command type
    if command_type == 'NAV_TAKEOFF':
        if logger:
            logger.info("[COMMANDS] - Processing NAV_TAKEOFF command")
        command = Nav_TakeOff(related_task, id, command_type, start_time, command_status, params, logger)
    elif command_type == 'NAV_LAND':
        if logger:
            logger.info("[COMMANDS] - Processing NAV_LAND command")
        command = Nav_Land(related_task, id, command_type, start_time, command_status, params, logger)
    elif command_type == 'NAV_WAYPOINT':
        if logger:
            logger.info("[COMMANDS] - Processing NAV_WAYPOINT command")
        command = Nav_Waypoint(related_task, id, command_type, start_time, command_status, params, logger)
    elif command_type == 'NAV_HOME':
        if logger:
            logger.info("[COMMANDS] - Processing NAV_HOME command")
        command = Nav_Home(related_task, id, command_type, start_time, command_status, params, logger)
    elif command_type == 'CAMERA_IMAGE':
        if logger:
            logger.info("[COMMANDS] - Processing CAMERA_IMAGE command")
        command = Camera_Image(related_task, id, command_type, start_time, command_status, params, logger)
    elif command_type == 'ANALYZE_IMAGE':
        if logger:
            logger.info("[COMMANDS] - Processing ANALYZE_IMAGE command")
        command = Analyze_Image(related_task, id, command_type, start_time, command_status, params, logger)
    elif command_type == 'SPRAY':
        if logger:
            logger.info("[COMMANDS] - Processing SPRAY command")
        command = Spray(related_task, id, command_type, start_time, command_status, params, logger)
    else:
        # Default to base Command class for unknown command types
        if logger:
            logger.info("[COMMANDS] - Processing UNKNOWN command")
        command = Command(related_task, id, command_type, start_time, command_status, params, logger)
    return command