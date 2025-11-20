"""
Mission Data Parsing and Normalization Utilities

.. note::
    Core functionalities include:
    - Mission plan construction from raw input data
    - Command structure normalization and organization
    - Vehicle-specific data extraction and typing
    - Feedback data standardization 
"""

import ast
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
        # Initialize performance timing for mission parsing operation
        start = time.perf_counter()
        mission_logger.info(f"[Mission {mission_id}][Data parser] - Parsing mission data")

        # Sort commands by start_time to ensure proper chronological execution order
        # Commands must be executed in temporal sequence for mission consistency
        try:
            commands = sorted(mission_data['commands'], key=lambda x: x['start_time'])
        except KeyError as e:
            mission_logger.error(f"[Mission {mission_id}][Data parser] - Missing key in commands: {str(e)}", exc_info=True)
            return {}
        except Exception as e:
            mission_logger.error(f"[Mission {mission_id}][Data parser] - Error sorting commands: {str(e)}", exc_info=True)
            return {}

        # Build tasks dictionary with empty command containers
        # Each task gets initialized with an empty commands dictionary for later population
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

        # Assign commands to their respective tasks based on related_task relationship
        # This creates the hierarchical structure: task -> commands
        for command in commands:
            try:
                task_id = command['related_task']['id']
                if task_id in tasks:
                    tasks[task_id]['commands'][command['id']] = command
                else:
                    mission_logger.error(f"[Mission {mission_id}][Data parser] - Task {task_id} not found for command {command['id']}")
            except KeyError as e:
                mission_logger.error(f"[Mission {mission_id}][Data parser] - Missing key in command: {str(e)}", exc_info=True)

        # Build plans dictionary organizing tasks by assigned vehicle
        # Final structure: {vehicle_id: {task_id: task_with_commands}}
        # Only includes tasks assigned to each specific vehicle
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

        # Calculate and log performance metrics for mission parsing operation
        end = time.perf_counter()
        duration = end - start
        mission_logger.info(f"[Mission {mission_id}][Data parser] - Finished parsing mission data in {duration:.6f} seconds")
        return plans

    except Exception as e:
        # Handle any unexpected errors during mission parsing process
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
        # Initialize performance timing for command extraction operation
        start = time.perf_counter()
        mission_logger.info(f"[Mission {mission_id}][Data parser] - Obtaining commands for vehicle {vehicle_id}")

        # Flatten commands from all tasks into a single dictionary for the vehicle
        # This creates a unified command dictionary for easier access and processing
        # Uses nested dictionary comprehension to extract commands from task hierarchy
        commands = {
            command['id']: command
            for task in plan.values()
            for command in task['commands'].values()
        }

        # Calculate and log performance metrics for command extraction
        end = time.perf_counter()
        duration = end - start
        mission_logger.info(f"[Mission {mission_id}][Data parser] - Obtained {len(commands)} commands for vehicle {vehicle_id} in {duration:.6f} seconds")
        return commands

    except KeyError as e:
        # Handle missing keys in the plan structure
        mission_logger.error(f"[Mission {mission_id}][Data parser] - Missing key: {str(e)}", exc_info=True)
        return {}
    except Exception as e:
        # Handle any unexpected errors during command extraction
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
        # Initialize performance timing for command list conversion
        start = time.perf_counter()
        mission_logger.info(f"[Mission {mission_id}][Data parser] - Converting commands to list")

        # Convert each command dictionary to string representation
        # Maintains the order of commands as they appear in the dictionary
        # Useful for serialization and transmission to external systems
        commands_list = [str(command) for command in commands.values()]
        
        # Calculate and log performance metrics for conversion operation
        end = time.perf_counter()
        duration = end - start
        mission_logger.info(f"[Mission {mission_id}][Data parser] - Converted commands to list in {duration:.6f} seconds")

        return commands_list

    except Exception as e:
        # Handle any errors during command list conversion
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
        # Initialize performance timing for vehicle type lookup operation
        start = time.perf_counter()
        mission_logger.info(f"[Mission {mission_id}][Data parser] - Obtaining type of vehicle for vehicle {vehicle_id}")

        # Search for vehicle type using generator expression with next()
        # Returns the first matching vehicle type or None if not found
        # More efficient than filtering the entire list for single lookups
        vehicle_type = next(
            (vehicle['type'] for vehicle in mission_data['vehicles'] if vehicle['id'] == vehicle_id),
            None
        )

        # Calculate performance metrics and log results
        end = time.perf_counter()
        duration = end - start
        
        if vehicle_type:
            mission_logger.info(f"[Mission {mission_id}][Data parser] - Vehicle {vehicle_id} is of type {vehicle_type} ({duration:.6f} seconds)")
        else:
            mission_logger.error(f"[Mission {mission_id}][Data parser] - Vehicle {vehicle_id} not found")

        return vehicle_type

    except KeyError as e:
        # Handle missing required keys in mission data structure
        mission_logger.error(f"[Mission {mission_id}][Data parser] - Missing key: {str(e)}", exc_info=True)
        return None
    except Exception as e:
        # Handle any unexpected errors during vehicle type lookup
        mission_logger.error(f"[Mission {mission_id}][Data parser] - Error obtaining vehicle type: {str(e)}", exc_info=True)
        return None
    

def parse_feedback_data(mission_id: int, vehicle_id: int, drone_result, mission_logger: logging.Logger) -> list:
    """Standardizes feedback data from vehicles into consistent list format.

    Args:
        mission_id: Current mission identifier
        vehicle_id: Source vehicle identifier
        drone_result: Raw feedback data from vehicle (various types)
        mission_logger: Configured logging instance

    Returns:
        List containing parsed feedback elements

    Note:
        Handles multiple input formats:
        - Direct lists (returned as-is)
        - JSON strings (parsed to objects/lists)
        - Python literal strings (using ast.literal_eval)
        - Plain strings (wrapped in list)
        - Other types (wrapped in list)

    Example:
        .. code-block:: python

            feedback = parse_feedback_data(123, 456, '["WP reached"]', logger)
            # Returns: ["WP reached"]
    """
    # Initialize performance timing for feedback data parsing
    start = time.perf_counter()

    try:
        # Handle different input data types for robust feedback parsing
        
        # Case 1: Input is already a list - use directly
        if isinstance(drone_result, list):
            data = drone_result

        # Case 2: Input is a string - attempt JSON parsing first, then literal evaluation
        elif isinstance(drone_result, str):
            try:
                # Try to parse as JSON string (most common format)
                data = json.loads(drone_result)
                # Ensure result is a list for consistency
                if not isinstance(data, list):
                    data = [data] 
            except json.JSONDecodeError:
                try:
                    # Fallback to Python literal evaluation for string representations
                    parsed = ast.literal_eval(drone_result)
                    if isinstance(parsed, list):
                        data = parsed
                    else:
                        # Wrap non-list results in a list
                        data = [drone_result]
                except Exception:
                    # If all parsing fails, treat as plain string
                    data = [drone_result]
        
        # Case 3: Any other data type - wrap in list for uniformity
        else:
            data = [drone_result]

    except Exception as e:
        # Handle any unexpected errors during feedback parsing
        # Log as warning since this is not critical to mission execution
        mission_logger.warning(f"[Mission {mission_id}][Data parser] - Failed to parse feedback from vehicle {vehicle_id}: {e}")
        data = [drone_result]

    # Calculate and log performance metrics for feedback parsing
    end = time.perf_counter()
    mission_logger.info(f"[Mission {mission_id}][Data parser] - Feedback parsed for vehicle {vehicle_id} in {end - start:.6f}s")
    return data