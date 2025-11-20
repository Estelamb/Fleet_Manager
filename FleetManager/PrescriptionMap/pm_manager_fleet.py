"""
Prescription Map Manager Fleet Module
====================================

This module provides prescription map (PM) management functionality for the agricultural
fleet management system. It handles the generation, validation, and comparison of
prescription maps for different vehicle types and agricultural treatments.

The module manages the complete lifecycle of prescription maps including:
- Generation of prescription maps based on treatment requirements
- Reception and storage of prescription maps from vehicles
- Comparison and validation between generated and received prescription maps
- State management for vehicle-specific prescription map operations

Key Features:
    - Multi-process prescription map generation for performance
    - Vehicle-specific prescription map tracking and validation
    - File-based comparison between generated and received prescription maps
    - Support for multiple prescription map types (ISOBUS, Drone, etc.)
    - Automatic cleanup and state management per vehicle
    - Integration with external prescription map generation scripts

Usage Example:
    ::

        # Handle prescription map generation request
        handle_generate(vehicle_id, generation_message, logger)
        
        # Handle received prescription map from vehicle
        handle_received(vehicle_id, received_message, logger)
        
        # Handle mission completion signal
        handle_finish(vehicle_id, logger)

Author: Fleet Management System
Date: 2025
"""

from concurrent.futures import ProcessPoolExecutor, as_completed
import json
import os
import subprocess
import sys
import shutil
import datetime

# Global variable to control finish status per vehicle_id
finish_status = {}

def handle_comparison_result(gen_path, rec_path, finished_dir, logger, vehicle_id, match):
    """
    Handle the result of a prescription map comparison by moving files, 
    generating error reports, and cleaning up original files.
    
    Args:
        gen_path (str): Path to the generated prescription map file
        rec_path (str): Path to the received prescription map file
        finished_dir (str): Directory to store finished files
        logger: Logger instance for operation tracking
        vehicle_id (str): Vehicle identifier for logging
        match (bool): True if files match, False otherwise
    """
    try:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        gen_filename = os.path.basename(gen_path)
        
        if match:
            # Mover el archivo generado a Finished con timestamp
            new_filename = f"{timestamp}_{gen_filename}"
            new_path = os.path.join(finished_dir, new_filename)
            shutil.move(gen_path, new_path)
            logger.info(f"[PM Manager] - Moved generated file to Finished: {new_filename}")
            
            # Eliminar el archivo recibido
            os.remove(rec_path)
            logger.info(f"[PM Manager] - Removed received file: {os.path.basename(rec_path)}")
        else:
            # Crear archivo de error combinado
            error_filename = f"ERROR-{timestamp}-{gen_filename}"
            error_path = os.path.join(finished_dir, error_filename)
            
            # Leer ambos archivos
            with open(gen_path, 'r') as f1, open(rec_path, 'r') as f2:
                gen_content = json.load(f1)
                rec_content = json.load(f2)
            
            # Generar estructura combinada con diferencias
            combined = {"differences": []}
            
            # Función recursiva para encontrar diferencias
            def find_diff(d1, d2, path=""):
                if isinstance(d1, dict) and isinstance(d2, dict):
                    keys = set(d1.keys()) | set(d2.keys())
                    for key in keys:
                        new_path = f"{path}.{key}" if path else key
                        if key not in d1:
                            combined["differences"].append({
                                "field": new_path,
                                "generated": "MISSING",
                                "received": d2[key]
                            })
                        elif key not in d2:
                            combined["differences"].append({
                                "field": new_path,
                                "generated": d1[key],
                                "received": "MISSING"
                            })
                        else:
                            find_diff(d1[key], d2[key], new_path)
                elif isinstance(d1, list) and isinstance(d2, list):
                    len1, len2 = len(d1), len(d2)
                    max_len = max(len1, len2)
                    for i in range(max_len):
                        new_path = f"{path}[{i}]"
                        if i >= len1:
                            combined["differences"].append({
                                "field": new_path,
                                "generated": "MISSING",
                                "received": d2[i]
                            })
                        elif i >= len2:
                            combined["differences"].append({
                                "field": new_path,
                                "generated": d1[i],
                                "received": "MISSING"
                            })
                        else:
                            find_diff(d1[i], d2[i], new_path)
                else:
                    if d1 != d2:
                        combined["differences"].append({
                            "field": path,
                            "generated": d1,
                            "received": d2
                        })
            
            find_diff(gen_content, rec_content)
            
            # Añadir contenidos completos para referencia
            combined["generated_content"] = gen_content
            combined["received_content"] = rec_content
            
            # Guardar archivo de error
            with open(error_path, 'w') as ef:
                json.dump(combined, ef, indent=4)
            logger.info(f"[PM Manager] - Created error file: {error_filename}")
            
            # Eliminar ambos archivos originales
            os.remove(gen_path)
            os.remove(rec_path)
            logger.info(f"[PM Manager] - Removed original files due to mismatch: {gen_filename}, {os.path.basename(rec_path)}")
            
    except Exception as e:
        logger.error(f"[PM Manager] - Error handling comparison result: {str(e)}")


def comparation(vehicle_id, logger):
    """
    Compare generated and received prescription maps for a specific vehicle.
    
    This function performs a comprehensive comparison between prescription maps
    that were generated by the system and those that were actually received
    from the vehicle after execution. The comparison helps validate that the
    vehicle executed the correct prescription map.
    
    The comparison process includes:
    1. Checking if the finish signal has been activated for the vehicle
    2. Scanning for received prescription map files
    3. Finding matching generated prescription map files
    4. Performing content comparison between file pairs
    5. Logging results and updating vehicle finish status
    
    Args:
        vehicle_id (str): Unique identifier of the vehicle for which to compare
                         prescription maps
        logger: Logger instance for operation tracking and debugging
        
    Note:
        This function only executes if the finish status is activated for the
        specified vehicle. The finish status is automatically deactivated
        after comparison completion.
        
    Warning:
        The function performs file system operations and JSON parsing, which
        may raise exceptions for corrupted files or missing directories.
        
    Example:
        ::
        
            # Compare prescription maps for vehicle after mission completion
            comparation("VEHICLE_001", logger)
    """
    try:
        if not finish_status.get(vehicle_id, False):
            logger.info(f"[PM Manager] - Finish not activated for vehicle {vehicle_id}, skipping comparison")
            return
        
        logger.info(f"[PM Manager] - Starting comparison for vehicle {vehicle_id}")
        
        received_dir = os.path.join("PrescriptionMap", "pm_generation", "Received")
        generated_base_dir = os.path.join("PrescriptionMap", "pm_generation")
        finished_dir = os.path.join("PrescriptionMap", "pm_generation", "Finished")
        
        os.makedirs(finished_dir, exist_ok=True)
        
        received_files = [f for f in os.listdir(received_dir) 
                         if f.startswith(f"{vehicle_id}_") and f.endswith("_received.json")]
        received_basenames = {f.replace("_received.json", "") for f in received_files}
        logger.info(f"[PM Manager] - Received files base names: {sorted(received_basenames)}")
        
        matched_pairs = set()
        for root, dirs, files in os.walk(generated_base_dir):
            if "Received" in root.split(os.sep) or "Finished" in root.split(os.sep):
                continue
            
            for file in files:
                if (file.startswith(f"{vehicle_id}_") and 
                    file.endswith(".json") and 
                    not file.endswith("_received.json")):
                    
                    file_base = file.replace(".json", "")
                    if file_base in received_basenames:
                        rec_file = f"{file_base}_received.json"
                        pair = (file, rec_file)
                        if pair not in matched_pairs:
                            matched_pairs.add(pair)
                            logger.info(f"[PM Manager] - Found matching pair: {file} <-> {rec_file}")
        
        matched_pairs = list(matched_pairs)
        logger.info(f"[PM Manager] - Found {len(matched_pairs)} unique matched file pairs for vehicle {vehicle_id}")
        
        if not matched_pairs:
            logger.info(f"[PM Manager] - No matching file pairs found for vehicle {vehicle_id}")
            return
        
        all_match = True
        for gen_file, rec_file in matched_pairs:
            gen_path = None
            for root, dirs, files in os.walk(generated_base_dir):
                if "Received" in root.split(os.sep) or "Finished" in root.split(os.sep):
                    continue
                if gen_file in files:
                    gen_path = os.path.join(root, gen_file)
                    break
            
            rec_path = os.path.join(received_dir, rec_file)
            
            if not gen_path or not os.path.exists(gen_path):
                logger.warning(f"[PM Manager] - Generated file not found: {gen_file}")
                all_match = False
                continue
                
            if not os.path.exists(rec_path):
                logger.warning(f"[PM Manager] - Received file not found: {rec_file}")
                all_match = False
                continue
                
            try:
                with open(gen_path, 'r') as f1, open(rec_path, 'r') as f2:
                    gen_content = json.load(f1)
                    rec_content = json.load(f2)
                    
                    if gen_content == rec_content:
                        logger.info(f"[PM Manager] - Content matches for vehicle {vehicle_id}, file {gen_file[:-5]}")
                        # Llamar a la nueva función para manejar archivos coincidentes
                        handle_comparison_result(gen_path, rec_path, finished_dir, logger, vehicle_id, True)
                    else:
                        logger.warning(f"[PM Manager] - Content mismatch for vehicle {vehicle_id}, file {gen_file[:-5]}")
                        all_match = False
                        # Llamar a la nueva función para manejar diferencias
                        handle_comparison_result(gen_path, rec_path, finished_dir, logger, vehicle_id, False)
            except Exception as e:
                logger.error(f"[PM Manager] - Error comparing files {gen_path} and {rec_path}: {str(e)}")
                all_match = False
                # Intentar limpiar archivos incluso si falla la comparación
                try:
                    if gen_path and os.path.exists(gen_path):
                        os.remove(gen_path)
                    if os.path.exists(rec_path):
                        os.remove(rec_path)
                except:
                    pass
        
        if all_match:
            logger.info(f"[PM Manager] - ALL files match for vehicle {vehicle_id}")
        else:
            logger.warning(f"[PM Manager] - Some files DO NOT match for vehicle {vehicle_id}")
        
        finish_status[vehicle_id] = False
        logger.info(f"[PM Manager] - Finish status deactivated for vehicle {vehicle_id}")
        
    except Exception as e:
        logger.error(f"[PM Manager] - Error in comparation: {str(e)}", exc_info=True)


def handle_finish(vehicle_id, logger):
    """
    Handle mission finish signal for a specific vehicle.
    
    This function processes the finish signal sent when a vehicle completes
    its mission. It activates the finish status for the vehicle and immediately
    triggers the prescription map comparison process.
    
    The finish signal indicates that:
    - The vehicle has completed executing its prescription map
    - All prescription map data should have been received from the vehicle
    - Comparison between generated and received maps can now be performed
    
    Args:
        vehicle_id (str): Unique identifier of the vehicle that finished its mission
        logger: Logger instance for operation tracking and debugging
        
    Example:
        ::
        
            # Handle mission completion signal
            handle_finish("VEHICLE_001", logger)
            
    Note:
        This function automatically triggers the comparation process to validate
        prescription map execution immediately after setting the finish status.
    """
    try:
        logger.info(f"[PM Manager] - Received finish signal for vehicle {vehicle_id}")
        # Activate finish status for this vehicle_id
        finish_status[vehicle_id] = True
        logger.info(f"[PM Manager] - Finish status activated for vehicle {vehicle_id}")
        
        # Trigger comparison immediately
        comparation(vehicle_id, logger)
    except Exception as e:
        logger.error(f"[PM Manager] - Error in handle_finish: {str(e)}", exc_info=True)


def handle_received(vehicle_id, message, logger):
    """
    Handle received prescription map data from a vehicle.
    
    This function processes prescription map data that has been received from
    a vehicle after executing its mission. The received data is stored in the
    Received directory for later comparison with the originally generated
    prescription map.
    
    The function performs the following operations:
    1. Extracts prescription map content from the message
    2. Validates message structure and filename
    3. Saves the received prescription map to the appropriate directory
    4. Triggers comparison if finish status is active for the vehicle
    
    Args:
        vehicle_id (str): Unique identifier of the vehicle sending the prescription map
        message (dict): Message containing prescription map data with keys:
            - content (dict): Nested content structure containing the actual PM data
                - content (list/dict): The actual prescription map content array
            - filename (str): Original filename of the prescription map
        logger: Logger instance for operation tracking and debugging
        
    Example:
        ::
        
            message = {
                'content': {
                    'content': [
                        {'x': 100, 'y': 200, 'treatment': 'pesticide', 'rate': 2.5},
                        {'x': 150, 'y': 250, 'treatment': 'pesticide', 'rate': 2.3}
                    ]
                },
                'filename': 'pesticide_application.json'
            }
            handle_received("VEHICLE_001", message, logger)
            
    Note:
        The function automatically triggers comparison at the end to check if
        the received prescription map matches the generated one, provided the
        finish status is active for the vehicle.
        
    Warning:
        Missing 'content' field or 'filename' in the message will cause the
        function to log warnings and return without processing the data.
    """
    try:                
        # Extract the actual content array from the message
        pm_data = message.get('content', {}).get('content')
            
        if pm_data is None:
            logger.warning("[PM Manager] - Missing 'content' field in message")
            return

        # Validate and extract filename from message
        filename = message.get('filename')
        if not filename:
            logger.warning("[PM Manager] - Missing filename in message")
            return

        # Remove .json extension if present for consistent naming
        if filename.endswith(".json"):
            filename = filename[:-5]

        logger.info(f"[PM Manager] - Received PM for vehicle {vehicle_id} with filename: {filename}")

        # Create standardized filename for received prescription map
        base_filename = f"{vehicle_id}_{filename}_received.json"

        # Ensure received directory exists
        received_dir = os.path.join("PrescriptionMap", "pm_generation", "Received")
        os.makedirs(received_dir, exist_ok=True)
        received_path = os.path.join(received_dir, base_filename)

        logger.info(f"[PM Manager] - Saving received PM to {received_path}")

        # Save only the content array directly to file
        with open(received_path, "w") as f:
            json.dump(pm_data, f, indent=2)
            
        logger.info(f"[PM Manager] - Received PM saved: {received_path}")
        
        # Trigger comparison at the end of handle_received
        comparation(vehicle_id, logger)
        
    except Exception as e:
        logger.error(f"[PM Manager] - Error in handle_received: {str(e)}", exc_info=True)


def handle_generate(vehicle_id, message, logger):
    """
    Handle prescription map generation request for a vehicle.
    
    This function processes requests to generate prescription maps for a specific
    vehicle based on treatment requirements, field coordinates, and prescription
    map types. It validates the input data and delegates the actual generation
    to the generate_pm function.
    
    The function expects a specific message format containing all necessary
    parameters for prescription map generation including treatments, amounts,
    field grid, coordinates, and prescription map types.
    
    Args:
        vehicle_id (str): Unique identifier of the vehicle for which to generate
                         prescription maps
        message (dict): Generation request message containing:
            - data (list): List of 5 elements in specific order:
                [treatments, amount, grid, coords, pm_types]
                - treatments: Treatment specifications
                - amount (dict): Treatment amounts/rates
                - grid (list): Field grid definition
                - coords (list): [latitude, longitude] coordinates
                - pm_types (dict): Prescription map types to generate
        logger: Logger instance for operation tracking and debugging
        
    Example:
        ::
        
            message = {
                'data': [
                    {'pesticide': True, 'fertilizer': False},  # treatments
                    {'pesticide': 2.5, 'fertilizer': 0},       # amounts
                    [[0, 0], [100, 100]],                      # grid
                    [40.4168, -3.7038],                        # coords [lat, long]
                    {'ISOBUS': True, 'Drone': False}           # pm_types
                ]
            }
            handle_generate("VEHICLE_001", message, logger)
            
    Note:
        The function validates that exactly 5 elements are provided in the data
        array and that pm_types is iterable before proceeding with generation.
        
    Warning:
        Invalid data length or malformed pm_types will cause the function to
        log errors and return without generating prescription maps.
    """
    try:
        # Validate message data structure
        data = message.get('data', [])
        if len(data) != 5:
            logger.error(f"[PM Manager] - Invalid data length in 'Generate' message. Expected 5 elements, got {len(data)}")
            return

        # Unpack message data components
        try:
            treatments, amount, grid, coords, pm_types = data
            lat, long = coords
        except (ValueError, TypeError) as e:
            logger.error(f"[PM Manager] - Error unpacking message data: {str(e)}")
            return
            
        # Validate that pm_types is iterable
        if not pm_types or not hasattr(pm_types, '__iter__'):
            logger.error(f"[PM Manager] - Invalid pm_types format: {type(pm_types)}")
            return

        # Delegate prescription map generation
        generate_pm(vehicle_id, pm_types, amount, grid, long, lat, logger)

    except Exception as e:
        logger.error(f"[PM Manager] - Critical error in handle_generate: {str(e)}", exc_info=True)


def generate_pm(vehicle_id, pm_types: dict, amount: dict, grid: list, long: float, lat: float, logger) -> list:
    """
    Generate prescription maps for a vehicle using external generation scripts.
    
    This function coordinates the generation of prescription maps by executing
    external scripts for each specified prescription map type. It uses a process
    pool for parallel execution to improve performance when generating multiple
    prescription map types.
    
    The function performs the following operations:
    1. Loads the prescription map types configuration
    2. Validates the existence of generation scripts
    3. Executes scripts in parallel using ProcessPoolExecutor
    4. Monitors execution with timeouts to prevent hanging
    5. Logs outputs and handles errors for each generation process
    
    Args:
        vehicle_id (str): Unique identifier of the vehicle
        pm_types (dict): Dictionary specifying which PM types to generate
        amount (dict): Treatment amounts and application rates
        grid (list): Field grid definition for spatial mapping
        long (float): Longitude coordinate of the field
        lat (float): Latitude coordinate of the field  
        logger: Logger instance for operation tracking and debugging
        
    Returns:
        list: Empty list (return value maintained for compatibility)
        
    Example:
        ::
        
            pm_types = {'ISOBUS': True, 'Drone': False}
            amount = {'pesticide': 2.5, 'fertilizer': 1.8}
            grid = [[0, 0], [100, 50], [100, 100], [0, 50]]
            generate_pm("VEHICLE_001", pm_types, amount, grid, -3.7038, 40.4168, logger)
            
    Note:
        The function uses timeouts (30s global, 15s per process) to prevent
        hanging on unresponsive generation scripts. All outputs are logged
        for debugging and monitoring purposes.
        
    Warning:
        Missing pm_types.json configuration file or invalid script paths will
        cause the function to return early without generating prescription maps.
    """
    # Define path to prescription map types configuration
    pm_types_path = "PrescriptionMap/pm_generation/pm_types.json"
    
    # Verify that the pm_types.json configuration file exists
    if not os.path.exists(pm_types_path):
        logger.error(f"[PM Manager] - PM types file not found: {pm_types_path}")
        return []
    
    # Load prescription map types configuration
    try:
        with open(pm_types_path, "r") as f:
            pm_types_dict = json.load(f)
    except Exception as e:
        logger.error(f"[PM Manager] - Error loading PM types: {str(e)}", exc_info=True)
        return []

    # Filter and map requested PM types to their script paths
    pm_types_to_run = [pm_types_dict[t] for t in pm_types if t in pm_types_dict]
    
    if not pm_types_to_run:
        logger.warning(f"[PM Manager] - No valid PM types found to run for vehicle {vehicle_id}")
        return []
        
    # Validate that all generation scripts exist before execution
    valid_scripts = []
    for script_path in pm_types_to_run:
        if os.path.exists(script_path):
            valid_scripts.append(script_path)
        else:
            logger.warning(f"[PM Manager] - Script not found: {script_path}")
    
    if not valid_scripts:
        logger.error(f"[PM Manager] - No valid PM scripts found for vehicle {vehicle_id}")
        return []

    # Execute prescription map generation scripts in parallel
    try:
        with ProcessPoolExecutor() as executor:
            futures = []
            
            # Submit each valid script for execution
            for pm_type_path in valid_scripts:
                logger.info(f"[PM Manager] - Running PM generator: {pm_type_path}")
                futures.append(
                    executor.submit(run_script, pm_type_path, vehicle_id, amount, grid, long, lat)
                )
                
            # Process completed futures with timeout handling
            for future in as_completed(futures, timeout=30):  # Global timeout for all processes
                try:
                    output = future.result(timeout=15)  # Individual timeout per process
                    logger.info(f"[PM Manager] - PM output: \n{output}")
                except Exception as e:
                    logger.error(f"[PM Manager] - Future failed or timed out: {str(e)}", exc_info=True)
                

    except Exception as e:
        logger.error(f"[PM Manager] - Error during PM generation: {str(e)}", exc_info=True)
        return []


def run_script(path: str, vehicle_id: int, amount: dict, grid: list, long: float, lat: float) -> str:
    """
    Execute a prescription map generation script with specified parameters.
    
    This function runs an external Python script for generating prescription maps,
    passing all necessary parameters as command-line arguments. It handles script
    execution, output capture, error handling, and timeout management.
    
    The script is executed as a subprocess with JSON-serialized parameters for
    complex data structures like amounts and grid definitions. Both stdout and
    stderr are captured for comprehensive logging.
    
    Args:
        path (str): File path to the prescription map generation script
        vehicle_id (int): Unique identifier of the vehicle
        amount (dict): Treatment amounts and application rates (JSON-serialized)
        grid (list): Field grid definition (JSON-serialized)
        long (float): Longitude coordinate of the field
        lat (float): Latitude coordinate of the field
        
    Returns:
        str: Script output on success, or error description on failure
        
    Example:
        ::
        
            output = run_script(
                "PrescriptionMap/pm_generation/ISOBUS/pm_isobus_fleet.py",
                "VEHICLE_001",
                {'pesticide': 2.5},
                [[0, 0], [100, 100]],
                -3.7038,
                40.4168
            )
            
    Note:
        The function uses a 20-second timeout to prevent hanging on unresponsive
        scripts. Complex parameters are JSON-serialized for reliable transmission.
        
    Warning:
        Script failures, timeouts, or unexpected errors are captured and returned
        as descriptive error messages rather than raising exceptions.
    """
    try:
        # Serialize complex parameters to JSON strings
        amount_str = json.dumps(amount)
        grid_str = json.dumps(grid) 

        # Execute the script with combined stdout/stderr capture
        result = subprocess.run(
            [
                sys.executable,  # Use current Python interpreter
                path,            # Script path
                "--vehicle_id", str(vehicle_id),
                "--amount", amount_str,
                "--grid", grid_str,
                "--long", str(long),
                "--lat", str(lat)
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # Combine stderr with stdout
            timeout=20,                # 20-second timeout
            text=True,                 # Return string output
            check=True                 # Raise exception on non-zero exit
        )
        return result.stdout.strip()
        
    except subprocess.CalledProcessError as e:
        # Handle script execution failures
        error_output = e.stdout.strip() if e.stdout else str(e.stderr)
        return f"Script failed: {path}\nCode: {e.returncode}\nOutput: {error_output}"
    except Exception as e:
        # Handle unexpected errors (timeouts, etc.)
        return f"Unexpected error in {path}: {str(e)}"
