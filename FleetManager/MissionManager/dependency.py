"""
Mission Task Dependency Resolution System

.. note:: 
    Implements critical mission management functionality including:
    - Task dependency validation
    - Command-task association
    - Treatment task parameter updates
    - Dependency status tracking
"""
import time
import logging

def check_dependencies(mission_id: int, plans: dict, drone_command: int, mission_logger: logging.Logger) -> tuple:
    """Resolves task dependencies based on completed commands.

    Args:
        mission_id: Unique mission identifier
        plans: Nested mission structure {vehicle_id: {task_id: task_data}}
        drone_command: Completed command ID triggering dependency check
        mission_logger: Configured logging instance

    Returns:
        Tuple containing:
        - Updated plans structure
        - List of vehicle IDs with fully resolved dependencies

    Raises:
        ValueError: If no task contains the completed command
        RuntimeError: For critical dependency resolution failures

    Example:
        .. code-block:: python

            updated_plans, ready_vehicles = check_dependencies(
                123, 
                mission_plans, 
                456, 
                logger
            )
    """
    # Initialize performance timing and result containers for dependency resolution
    start = time.perf_counter()
    vehicle_ids = []  # List to store vehicle IDs with resolved dependencies
    task_result = None  # Container for the task containing the completed command

    mission_logger.info(f"[Mission {mission_id}][Dependency] - Starting dependency check process.")
    try:
        # Locate the specific task that contains the completed command
        # This is crucial for dependency resolution as we need the task context
        task_result = find_task_by_command(mission_id, plans, drone_command, mission_logger)
        if task_result is None:
            raise ValueError(f"[Mission {mission_id}][Dependency] - No task found for the completed command with ID {drone_command}")
        mission_logger.info(f"[Mission {mission_id}][Dependency] - Task associated with command ID {drone_command} found successfully.")

        # Iterate through all vehicles and tasks to resolve dependencies
        # This nested loop processes each task's dependency against the completed task
        for vehicle_id, plan in plans.items():
            for task_id, task in plan.items():
                try:
                    # Extract dependency configuration from current task
                    dependency = task.get('task_dependency')
                    
                    # Check if the dependency conditions are satisfied by the completed task
                    if is_dependency_satisfied(mission_id, dependency, task_result, mission_logger):
                        mission_logger.info(f"[Mission {mission_id}][Dependency] - Dependency satisfied for task ID {task_id} in vehicle ID {vehicle_id}.")
                        
                        # Apply task-specific dependency resolution logic
                        plans = apply_dependency(mission_id, plans, vehicle_id, task_id, task_result, mission_logger)
                        
                        # Mark dependency as modified to prevent reprocessing
                        plans[vehicle_id][task_id]['task_dependency']['dependency_status'] = "Modified"
                        mission_logger.info(f"[Mission {mission_id}][Dependency] - Task with dependency completed: {task_id}")
                except KeyError as e:
                    mission_logger.error(f"[Mission {mission_id}][Dependency] - KeyError while processing task {task_id} in vehicle ID {vehicle_id}: {e}")
                except Exception as e:
                    mission_logger.error(f"[Mission {mission_id}][Dependency] - Unexpected error while processing task {task_id} in vehicle ID {vehicle_id}: {e}")

        # Final verification: Check if all dependencies are resolved for each vehicle
        # Vehicles with all dependencies resolved are ready for mission execution
        for vehicle_id, plan in plans.items():
            try:
                if all_dependencies_resolved(mission_id, plan, mission_logger):
                    mission_logger.info(f"[Mission {mission_id}][Dependency] - All dependencies resolved for vehicle ID {vehicle_id}.")
                    vehicle_ids.append(vehicle_id)
                    
                    # Mark all dependency statuses as completed for this vehicle
                    for task_id, task in plan.items():
                        if task.get('task_dependency'):
                            plans[vehicle_id][task_id]['task_dependency']['dependency_status'] = "Completed"
            except Exception as e:
                mission_logger.error(f"[Mission {mission_id}][Dependency] - Error while checking dependencies for vehicle {vehicle_id}: {e}")

    except Exception as e:
        # Handle critical errors in the dependency resolution process
        mission_logger.error(f"[Mission {mission_id}][Dependency] - Error in check_dependencies: {e}")
        raise

    # Calculate and log performance metrics for dependency resolution
    end = time.perf_counter()
    duration = end - start
    
    mission_logger.info(f"[Mission {mission_id}][Dependency] - Dependency check process completed in {duration:.6f} seconds.")
    return plans, vehicle_ids


def find_task_by_command(mission_id: int, plans: dict, drone_command: int, mission_logger: logging.Logger) -> dict:
    """Locates task containing specified command.

    Args:
        mission_id: Current mission identifier
        plans: Mission structure {vehicle_id: {task_id: task_data}}
        command_id: Command ID to locate
        mission_logger: Configured logging instance

    Returns:
        Task dictionary if found, None otherwise
    """
    try:
        # Perform exhaustive search through all vehicles, tasks, and commands
        # This nested iteration ensures we find the command regardless of hierarchy level
        for vehicle_id, plan in plans.items():
            for task_id, task in plan.items():
                for command_id, command in task['commands'].items():
                    # Direct command ID comparison to locate the completed command
                    if command['id'] == drone_command:
                        return task
    except KeyError as e:
        # Handle missing keys in the plan structure during search
        mission_logger.error(f"[Mission {mission_id}][Dependency] - KeyError in find_task_by_command: {e}")
    except Exception as e:
        # Handle any unexpected errors during command search
        mission_logger.error(f"[Mission {mission_id}][Dependency] - Unexpected error in find_task_by_command: {e}")
        
    mission_logger.info(f"[Mission {mission_id}][Dependency] - No task found for command ID {drone_command}.")
    return None


def is_dependency_satisfied(mission_id: int, dependency: dict, task_result: dict, mission_logger: logging.Logger) -> bool:
    """Validates dependency requirements against completed task.

    Args:
        dependency: Dependency configuration from task
        completed_task: Finished task data

    Returns:
        True if dependency conditions are met
    """
    try:
        # Comprehensive dependency validation using multiple criteria
        # All conditions must be true for dependency to be considered satisfied
        satisfied = (
            dependency and  # Dependency configuration must exist
            dependency['dependency_status'] == "NotModified" and  # Must be unprocessed
            dependency['dependency_task_id'] == task_result['id'] and  # Task ID must match
            dependency['dependency_task_status'] == task_result['task_status']  # Status must match
        )
        return satisfied
    except KeyError as e:
        # Handle missing dependency configuration keys
        mission_logger.error(f"[Mission {mission_id}][Dependency] - KeyError in is_dependency_satisfied: {e}")
        return False
    except Exception as e:
        # Handle any unexpected errors during dependency validation
        mission_logger.error(f"[Mission {mission_id}][Dependency] - Unexpected error in is_dependency_satisfied: {e}")
        return False


def all_dependencies_resolved(mission_id: int, plan: dict, mission_logger: logging.Logger) -> bool:
    """Verifies complete dependency resolution for vehicle plan.

    Args:
        plan: Vehicle-specific task structure {task_id: task_data}

    Returns:
        True if all dependencies marked resolved
    """
    try:
        # Complex dependency resolution verification with two main conditions:
        # 1. All tasks either have no dependencies OR have modified dependencies
        # 2. At least one task in the plan has a dependency (to ensure relevance)
        resolved = (
            all(
                task.get('task_dependency') is None or task['task_dependency']['dependency_status'] == "Modified"
                for task in plan.values()
            ) and any(task.get('task_dependency') is not None for task in plan.values())
        )
        return resolved
    except Exception as e:
        # Handle errors during dependency resolution verification
        mission_logger.error(f"[Mission {mission_id}][Dependency] - Error in all_dependencies_resolved: {e}")
        return False


def apply_dependency(mission_id: int, plans: dict, vehicle_id: int, task_id: int, task_result: dict, mission_logger: logging.Logger) -> dict:
    """
    Applies task-specific dependency resolution logic.
    
    Args:
        mission_id: Current mission identifier
        plans: Mission plans dictionary
        vehicle_id: Target vehicle ID
        task_id: Task ID to modify
        task_result: Completed task data for reference
        mission_logger: Mission event logger

    Returns:
        Updated plans dictionary with modified task parameters
    """
    try:
        # Task-type specific dependency resolution using pattern matching
        # Currently supports TREATMENT tasks with potential for future expansion
        match plans[vehicle_id][task_id]['task_type']:
            case 'TREATMENT':
                # Apply treatment-specific dependency resolution logic
                plans = treatment(mission_id, plans, vehicle_id, task_id, task_result, mission_logger)
    except KeyError as e:
        # Handle missing task type or structure keys
        mission_logger.error(f"[Mission {mission_id}][Dependency] - KeyError in apply_dependency: {e}")
    except Exception as e:
        # Handle any unexpected errors during dependency application
        mission_logger.error(f"[Mission {mission_id}][Dependency] - Unexpected error in apply_dependency: {e}")
    return plans


def treatment(mission_id: int, plans: dict, vehicle_id: int, task_id: int, task_result: dict, mission_logger: logging.Logger) -> dict:
    """
    Processes TREATMENT-type task dependencies by updating spray commands.

    Args:
        mission_id: Current mission identifier
        plans: Mission plans dictionary
        vehicle_id: Target vehicle ID
        task_id: Task ID to modify
        task_result: Completed task data for reference
        mission_logger: Mission event logger
        
    Returns:
        Updated plans dictionary with modified task parameters
    """
    try:
        mission_logger.info(f"[Mission {mission_id}][Dependency] - Processing 'TREATMENT' task ID {task_id} in vehicle ID {vehicle_id}.")
        
        # Extract ANALYZE_IMAGE command results from the completed task
        # These results contain analysis data needed for spray parameter updates
        results = [
            command for command in task_result['commands'].values()
            if command['command_type'] == 'ANALYZE_IMAGE'
        ]

        # Process each SPRAY command in the current treatment task
        for command_id, command in plans[vehicle_id][task_id]['commands'].items():
            if command['command_type'] == 'SPRAY':
                # Match spray commands with analysis results based on coordinate parameters
                for command_result in results:
                    # Parameter matching logic:
                    # - params[2] and params[3] represent coordinates (x, y)
                    # - params[0] represents the target/area identifier
                    # - result[0] and result[1] contain analysis outcomes
                    if (
                        command['params'][2] == command_result['params'][1] and
                        command['params'][3] == command_result['params'][2]
                    ):
                    
                        # --- Convertir diccionario a arrays ---
                        dic = command_result['result'][1]     # {'Grape_bunch': 5.95, 'Grape_quality': 6.8}
                        params_array_0 = list(dic.keys())     # ['Grape_bunch', 'Grape_quality']
                        params_array_1 = list(dic.values())   # [5.95, 6.8]
                    
                        # Actualizar SPRAY con nuevos parámetros
                        plans[vehicle_id][task_id]['commands'][command_id]['params'][0] = params_array_0
                        plans[vehicle_id][task_id]['commands'][command_id]['params'][1] = params_array_1
                        mission_logger.info(f"[Mission {mission_id}][Dependency] - Updated 'SPRAY' command ID {command_id} with new parameters.")
    except KeyError as e:
        # Handle missing keys in command or result structures
        mission_logger.error(f"[Mission {mission_id}][Dependency] - KeyError in treatment: {e}")
    except Exception as e:
        # Handle any unexpected errors during treatment processing
        mission_logger.error(f"[Mission {mission_id}][Dependency] - Unexpected error in treatment: {e}")

    return plans