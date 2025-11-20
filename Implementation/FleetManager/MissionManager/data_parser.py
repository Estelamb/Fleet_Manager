"""
Mission Data Parsing and Normalization Utilities

.. note::
    Core functionalities include:
    - Mission plan construction from raw input data
    - Command structure normalization and organization
    - Vehicle-specific data extraction and typing
    - Feedback data standardization 
"""

import time
import json
import logging

def parse_mission(mission_id: int, mission_data: dict, mission_logger: logging.Logger) -> dict:
    """Constructs structured vehicle mission plans from raw mission data.

    Args:
        mission_id: Unique identifier for the current mission
        mission_data: Raw mission structure containing tasks, commands and vehicles
        mission_logger: Configured logger instance for mission operations

    Returns:
        Nested dictionary structure:
        {vehicle_id: {
            task_id: {**task_data, 'commands': {command_id: command_data}}}
        }

    Raises:
        KeyError: If required data fields are missing in input structures
        ValueError: If invalid data formats are detected

    Example:
        .. code-block:: python

            mission_data = {
                'tasks': [...],
                'commands': [...],
                'vehicles': [...]
            }
            plans = parse_mission(123, mission_data, logger)
    """
    try:
        start = time.perf_counter()
        mission_logger.info(f"[Mission {mission_id}][Data parser] - Parsing mission data")

        # Sort commands by start_time
        try:
            commands = sorted(mission_data['commands'], key=lambda x: x['start_time'])
        except KeyError as e:
            mission_logger.error(f"[Mission {mission_id}][Data parser] - Missing key in commands: {str(e)}", exc_info=True)
            return {}
        except Exception as e:
            mission_logger.error(f"[Mission {mission_id}][Data parser] - Error sorting commands: {str(e)}", exc_info=True)
            return {}

        # Build tasks dictionary
        try:
            tasks = {
                task['id']: {**task, 'commands': {}}
                for task in mission_data['tasks']
            }
        except KeyError as e:
            mission_logger.error(f"[Mission {mission_id}][Data parser] - Missing key in tasks: {str(e)}", exc_info=True)
            return {}
        except Exception as e:
            mission_logger.error(f"[Mission {mission_id}][Data parser] - Error building tasks dictionary: {str(e)}", exc_info=True)
            return {}

        # Assign commands to tasks
        for command in commands:
            try:
                task_id = command['related_task']['id']
                if task_id in tasks:
                    tasks[task_id]['commands'][command['id']] = command
                else:
                    mission_logger.error(f"[Mission {mission_id}][Data parser] - Task {task_id} not found for command {command['id']}")
            except KeyError as e:
                mission_logger.error(f"[Mission {mission_id}][Data parser] - Missing key in command: {str(e)}", exc_info=True)

        # Build plans dictionary
        try:
            plans = {
                vehicle['id']: {
                    task_id: task
                    for task_id, task in tasks.items()
                    if task['assigned_vehicle_id'] == vehicle['id']
                }
                for vehicle in mission_data['vehicles']
            }
        except KeyError as e:
            mission_logger.error(f"[Mission {mission_id}][Data parser] - Missing key in vehicles: {str(e)}", exc_info=True)
            return {}
        except Exception as e:
            mission_logger.error(f"[Mission {mission_id}][Data parser] - Error building plans dictionary: {str(e)}", exc_info=True)
            return {}

        end = time.perf_counter()
        duration = end - start
        mission_logger.info(f"[Mission {mission_id}][Data parser] - Finished parsing mission data in {duration:.6f} seconds")
        return plans

    except Exception as e:
        mission_logger.error(f"[Mission {mission_id}][Data parser] - Critical error parsing mission: {str(e)}", exc_info=True)
        return {}


def obtain_commands_per_vehicle(mission_id: int, vehicle_id: int, plan: dict, mission_logger: logging.Logger) -> dict:
    """Flattens command hierarchy into vehicle-specific command dictionary.

    Args:
        mission_id: Current mission identifier
        vehicle_id: Target vehicle identifier
        plan: Vehicle's mission plan structure from parse_mission()
        mission_logger: Configured logging instance

    Returns:
        Dictionary mapping command IDs to full command specifications:
        {command_id: {command_data}}

    Raises:
        KeyError: If command structure violates expected format
    """
    try:
        start = time.perf_counter()
        mission_logger.info(f"[Mission {mission_id}][Data parser] - Obtaining commands for vehicle {vehicle_id}")

        # Flatten commands from all tasks into a single dictionary
        commands = {
            command['id']: command
            for task in plan.values()
            for command in task['commands'].values()
        }

        end = time.perf_counter()
        duration = end - start
        mission_logger.info(f"[Mission {mission_id}][Data parser] - Obtained {len(commands)} commands for vehicle {vehicle_id} in {duration:.6f} seconds")
        return commands

    except KeyError as e:
        mission_logger.error(f"[Mission {mission_id}][Data parser] - Missing key: {str(e)}", exc_info=True)
        return {}
    except Exception as e:
        mission_logger.error(f"[Mission {mission_id}][Data parser] - Error obtaining commands: {str(e)}", exc_info=True)
        return {}


def commands_to_list(mission_id: int, commands: dict, mission_logger: logging.Logger) -> list:
    """Serializes command dictionary to string list representation.

    Args:
        mission_id: Current mission identifier
        commands: Command dictionary from obtain_commands_per_vehicle()
        mission_logger: Configured logging instance

    Returns:
        List of string representations for each command

    Note:
        Maintains command insertion order based on dictionary ordering
    """
    try:
        start = time.perf_counter()
        mission_logger.info(f"[Mission {mission_id}][Data parser] - Converting commands to list")

        commands_list = [str(command) for command in commands.values()]
        
        end = time.perf_counter()
        duration = end - start
        mission_logger.info(f"[Mission {mission_id}][Data parser] - Converted commands to list in {duration:.6f} seconds")

        return commands_list

    except Exception as e:
        mission_logger.error(f"[Mission {mission_id}][Data parser] - Error converting commands to list: {str(e)}", exc_info=True)
        return []


def obtain_type_of_vehicle(mission_id: int, vehicle_id: int, mission_data: dict, mission_logger: logging.Logger) -> str:
    """Identifies vehicle type from mission configuration data.

    Args:
        mission_id: Current mission identifier
        vehicle_id: Target vehicle identifier
        mission_data: Original mission data structure
        mission_logger: Configured logging instance

    Returns:
        Vehicle type string if found, None otherwise

    Example:
        .. code-block:: python

            vehicle_type = obtain_type_of_vehicle(123, 456, mission_data, logger)
    """
    try:
        start = time.perf_counter()
        mission_logger.info(f"[Mission {mission_id}][Data parser] - Obtaining type of vehicle for vehicle {vehicle_id}")

        vehicle_type = next(
            (vehicle['type'] for vehicle in mission_data['vehicles'] if vehicle['id'] == vehicle_id),
            None
        )

        end = time.perf_counter()
        duration = end - start
        
        if vehicle_type:
            mission_logger.info(f"[Mission {mission_id}][Data parser] - Vehicle {vehicle_id} is of type {vehicle_type} ({duration:.6f} seconds)")
        else:
            mission_logger.error(f"[Mission {mission_id}][Data parser] - Vehicle {vehicle_id} not found")

        return vehicle_type

    except KeyError as e:
        mission_logger.error(f"[Mission {mission_id}][Data parser] - Missing key: {str(e)}", exc_info=True)
        return None
    except Exception as e:
        mission_logger.error(f"[Mission {mission_id}][Data parser] - Error obtaining vehicle type: {str(e)}", exc_info=True)
        return None
    
def parse_feedback_data(mission_id: int, vehicle_id: int, drone_result, mission_logger: logging.Logger) -> list:
    """Normalizes diverse feedback formats into standardized list structure.

    Args:
        mission_id: Current mission identifier
        vehicle_id: Source vehicle identifier
        raw_data: Input data from vehicle (JSON string or raw format)
        mission_logger: Configured logging instance

    Returns:
        List containing normalized feedback items:
        - JSON objects are parsed and wrapped in list
        - Strings are preserved in list
        - Invalid JSON treated as raw strings

    Raises:
        json.JSONDecodeError: For malformed JSON with detailed logging

    Example:
        .. code-block:: python

            >>> parse_feedback_data(123, 456, '{"status": "ok"}', logger)
            [{'status': 'ok'}]
            >>> parse_feedback_data(123, 456, "plain text", logger)
            ['plain text']
    """
    start = time.perf_counter()
    
    try:
        # Attempt to parse drone_result[3] as JSON
        data = json.loads(drone_result)
        
        # If the parsed data is not a list, wrap it in a list
        if not isinstance(data, list):
            data = [data]
    except json.JSONDecodeError:
        # If parsing fails, treat it as a plain string and wrap it in a list
        data = [drone_result]
        
    end = time.perf_counter()
    duration = end - start
    mission_logger.info(f"[Mission {mission_id}][Data parser] - Feedback data parsed for vehicle {vehicle_id} in {duration:.6f} seconds")
    
    return data