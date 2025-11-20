"""
This module provides functionality for parsing and executing drone commands 
from JSON-formatted strings. It serves as the main interface between command
input and concrete command implementations.

Functions
---------
process_command
    Main command processing pipeline
parse_command
    JSON command validation and parsing
select_command
    Command object instantiation based on type

Exceptions
----------
ValueError
    Raised for invalid JSON command format
"""

import random, json
from src.commands_action_interface.src.commands import Command, Nav_TakeOff, Nav_Land, Nav_Waypoint, Nav_Home, Camera_Image, Analyze_Image, Spray

def process_command(command_str : str):
    """Execute full command processing pipeline.
    
    1. Parse input string to command dictionary
    2. Instantiate appropriate command object
    3. Execute command logic
    4. Return formatted results
    
    :param command_str: JSON-formatted command string
    :type command_str: str
    :return: Tuple containing (command_id, result_data, latitude, longitude)
    :rtype: tuple
    :raises ValueError: If input string contains invalid JSON
    
    Example:
        Process a takeoff command::
            
            result = process_command('{"command_type": "NAV_TAKEOFF, ...}')
    """
    
    command_dict = parse_command(command_str)
    
    command = select_command(command_dict)
    
    command.execute()
    
    command_id, command_data, latitude, longitude = command.result()
    
    return command_id, command_data, latitude, longitude


def parse_command(command_str : str):
    """Validate and parse JSON command string to dictionary.
    
    :param command_str: Input command string in JSON format
    :type command_str: str
    :return: Validated command dictionary
    :rtype: dict
    :raises ValueError: If JSON parsing fails
    """
    
    try:
        command_dict = json.loads(command_str)
    except json.JSONDecodeError:
        raise ValueError("Invalid command string format")
    
    return command_dict

def select_command(command_dict : dict):
    """Instantiate appropriate command subclass based on command type.
    
    Supported command types:
    - NAV_TAKEOFF: Nav_TakeOff
    - NAV_LAND: Nav_Land
    - NAV_WAYPOINT: Nav_Waypoint
    - NAV_HOME: Nav_Home
    - CAMERA_IMAGE: Camera_Image
    - ANALYZE_IMAGE: Analyze_Image
    - SPRAY: Spray
    
    :param command_dict: Validated command dictionary
    :type command_dict: dict
    :return: Concrete command instance
    :rtype: Command
    """
    
    related_task = command_dict['related_task']
    id = command_dict['id']
    command_type = command_dict['command_type']
    start_time = command_dict['start_time']
    command_status = command_dict['command_status']
    params = command_dict['params']
    
    if command_dict['command_type'] == 'NAV_TAKEOFF':
        command = Nav_TakeOff(related_task, id, command_type, start_time, command_status, params)
    elif command_dict['command_type'] == 'NAV_LAND':
        command = Nav_Land(related_task, id, command_type, start_time, command_status, params)
    elif command_dict['command_type'] == 'NAV_WAYPOINT':
        command = Nav_Waypoint(related_task, id, command_type, start_time, command_status, params)
    elif command_dict['command_type'] == 'NAV_HOME':
        command = Nav_Home(related_task, id, command_type, start_time, command_status, params)
    elif command_dict['command_type'] == 'CAMERA_IMAGE':
        command = Camera_Image(related_task, id, command_type, start_time, command_status, params)
    elif command_dict['command_type'] == 'ANALYZE_IMAGE':
        command = Analyze_Image(related_task, id, command_type, start_time, command_status, params)
    elif command_dict['command_type'] == 'SPRAY':
        command = Spray(related_task, id, command_type, start_time, command_status, params)
    else:
        command = Command(related_task, id, command_type, start_time, command_status, params)
        
    return command