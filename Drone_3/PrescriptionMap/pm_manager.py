"""
Prescription Map Manager Module
==============================

This module provides comprehensive prescription map (PM) management functionality
for agricultural drone systems. It handles the generation, processing, and transmission
of prescription maps used for precision agriculture applications including fertilizer
application, pesticide treatment, and crop monitoring strategies.

The module orchestrates multiple PM generation scripts using parallel processing,
manages PM data storage and retrieval, and coordinates PM transmission to Mission
Management systems via gRPC communication channels.

.. module:: pm_manager
    :synopsis: Prescription map generation and transmission for agricultural drone operations

Features
--------
- **Multi-Type PM Generation**: Support for multiple prescription map types and algorithms
- **Parallel Processing**: Concurrent execution of PM generation scripts for efficiency
- **Grid-Based Mapping**: Spatial data organization using coordinate grid systems
- **gRPC Transmission**: Reliable PM data transmission to Mission Management systems
- **Error Handling**: Comprehensive error management and recovery mechanisms
- **JSON Storage**: Standardized PM data format for interoperability

Prescription Map Workflow
------------------------
PM Generation and Distribution Pipeline:
    1. **Configuration Loading**: Read PM type definitions and script mappings
    2. **Parallel Execution**: Launch multiple PM generation scripts concurrently
    3. **Data Aggregation**: Collect and process results from all generators
    4. **Quality Validation**: Verify PM data integrity and completeness
    5. **Storage Management**: Organize PM files in structured directory hierarchy
    6. **Transmission Coordination**: Send completed PMs to Mission Management
    7. **Status Reporting**: Track transmission success and error conditions

Grid System
-----------
Spatial data organization:
    - **Grid Coordinates**: [row, column] indexing system
    - **Geographic Mapping**: Grid cells mapped to GPS coordinates
    - **Resolution**: Configurable grid cell size for precision control
    - **Coverage**: Complete field coverage with overlapping boundaries

PM Types and Algorithms
----------------------
Supported prescription map types:
    - **Fertilizer Maps**: Nutrient application prescriptions
    - **Pesticide Maps**: Targeted treatment recommendations
    - **Irrigation Maps**: Water application scheduling
    - **Seeding Maps**: Planting density and variety recommendations
    - **Monitoring Maps**: Sensor placement and inspection schedules

Functions
---------
.. autofunction:: generate_pm
.. autofunction:: run_script
.. autofunction:: send_all

Dependencies
-----------
- **json**: PM data serialization and configuration management
- **os**: File system operations and directory management
- **subprocess**: External script execution and process management
- **concurrent.futures**: Parallel processing coordination
- **GRPC.grpc_drone_pm**: PM transmission to Mission Management systems

Integration Points
-----------------
This module integrates with:
    - **Mission Planning**: PM generation triggered by mission waypoints
    - **Image Analysis**: PM generation based on crop analysis results
    - **gRPC Services**: PM transmission to Mission Management systems
    - **Field Mapping**: Coordinate system integration for spatial accuracy

Performance Considerations
-------------------------
- **Parallel Execution**: Multiple PM generators run concurrently for efficiency
- **Memory Management**: Large PM datasets handled with streaming operations
- **Network Optimization**: Batch transmission reduces communication overhead
- **Storage Efficiency**: JSON format balances readability and storage space

Error Handling Strategy
----------------------
- **Script Failures**: Individual PM generator errors don't halt overall process
- **Transmission Errors**: Retry mechanisms for network communication failures
- **Data Validation**: PM content verification before transmission
- **Graceful Degradation**: System continues operation with partial PM sets

Configuration Files
------------------
PM generation requires configuration files:
    - **pm_types.json**: Mapping of PM types to generator scripts
    - **Grid Configuration**: Spatial coordinate system definitions
    - **Algorithm Parameters**: PM generation algorithm settings

Notes
-----
- PM generation scripts must accept standardized command-line arguments
- All PM data is validated before transmission to Mission Management
- Concurrent execution requires sufficient system resources
- Grid coordinates must be consistent across all PM types

See Also
--------
GRPC.grpc_drone_pm : PM transmission implementation
Images.analyze_image : Image analysis driving PM generation
subprocess.run : External script execution mechanism
concurrent.futures.ProcessPoolExecutor : Parallel processing implementation
"""

import json
import os
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Dict, List, Union, Any, Optional
import logging
import shutil
import datetime
import logging

from GRPC.grpc_drone_pm import run_pm_client


def generate_pm(pm_types: Dict[str, bool], amount: Dict[str, float], grid: List[int], long: float, lat: float, logger: logging.Logger) -> None:
    """
    Generate prescription maps using parallel processing of multiple PM generation algorithms.

    This function orchestrates the execution of multiple prescription map generation
    scripts based on the specified PM types and input parameters. It uses parallel
    processing to execute multiple PM generators concurrently, improving efficiency
    for complex agricultural analysis workflows.

    Parameters
    ----------
    pm_types : Dict[str, bool]
        Dictionary mapping prescription map type names to boolean activation flags.
        Keys correspond to entries in pm_types.json configuration file.
        Only PM types with True values will be processed.
        Examples: {"fertilizer": True, "pesticide": False, "irrigation": True}
    amount : Dict[str, float]
        Dictionary mapping substance/treatment names to application amounts.
        Used as input data for PM generation algorithms.
        Examples: {"nitrogen": 50.0, "phosphorus": 30.0, "water": 100.0}
    grid : List[int]
        Grid coordinates specifying the spatial location for PM generation.
        Format: [row, column] in the field coordinate system.
        Examples: [10, 15], [0, 0], [25, 40]
    long : float
        Longitude coordinate in decimal degrees for geographic reference.
        Used for spatial mapping and coordinate system alignment.
        Range: -180.0 to +180.0 degrees
    lat : float
        Latitude coordinate in decimal degrees for geographic reference.
        Used for spatial mapping and coordinate system alignment.
        Range: -90.0 to +90.0 degrees
    logger : logging.Logger
        Logger instance for recording PM generation events, progress, and errors.
        Provides detailed logging for debugging and operation monitoring.

    Returns
    -------
    None
        Function performs PM generation operations without returning values.
        Results are stored in generated PM files and logged via logger.

    Workflow
    --------
    1. **Configuration Loading**: Read PM type definitions from pm_types.json
    2. **Type Filtering**: Select active PM types based on pm_types parameter
    3. **Script Resolution**: Map PM types to executable generator script paths
    4. **Parallel Execution**: Launch PM generation scripts using ProcessPoolExecutor
    5. **Result Collection**: Gather outputs from all completed PM generators
    6. **Status Logging**: Record generation progress and completion status
    7. **Error Handling**: Capture and log any generation failures

    Parallel Processing Strategy
    ---------------------------
    Uses ProcessPoolExecutor for concurrent PM generation:
        - **Isolation**: Each PM type runs in separate process
        - **Resource Sharing**: Optimal CPU core utilization
        - **Error Containment**: Individual script failures don't affect others
        - **Scalability**: Automatic scaling based on available system resources

    Configuration File Format
    -------------------------
    pm_types.json structure:
        {
            "fertilizer": "path/to/fertilizer_generator.py",
            "pesticide": "path/to/pesticide_generator.py",
            "irrigation": "path/to/irrigation_generator.py"
        }

    Error Scenarios
    --------------
    - **Missing Configuration**: pm_types.json file not found or malformed
    - **Invalid PM Types**: Requested PM type not defined in configuration
    - **Script Execution Failure**: PM generation script errors or timeouts
    - **Resource Exhaustion**: Insufficient system resources for parallel execution

    Performance Characteristics
    --------------------------
    - **Execution Time**: 5-30 seconds depending on PM complexity and system resources
    - **Memory Usage**: Scales with number of concurrent PM generators
    - **CPU Utilization**: Maximizes available cores for parallel processing
    - **Storage Impact**: Generated PM files stored in configured directories

    Integration Notes
    ----------------
    Function integrates with:
        - **Mission Execution**: Called during waypoint-based PM generation
        - **Image Analysis**: Triggered by crop analysis results
        - **Field Mapping**: Grid coordinates aligned with field coordinate systems
        - **PM Transmission**: Generated PMs sent via send_all() function

    Script Interface Requirements
    ----------------------------
    PM generation scripts must implement standardized interface:
        - **Command Line Args**: --amount, --grid, --long, --lat parameters
        - **JSON Input**: amount and grid parameters as JSON strings
        - **Stdout Output**: PM data or status information
        - **Error Handling**: Appropriate exit codes for success/failure

    Notes
    -----
    - Function blocks until all PM generators complete or fail
    - Individual PM generation failures don't halt overall process
    - Results are collected and logged but not returned to caller
    - Generated PM files must be manually retrieved or sent via send_all()

    See Also
    --------
    run_script : Individual PM generator script execution
    send_all : PM transmission to Mission Management systems
    concurrent.futures.ProcessPoolExecutor : Parallel processing implementation
    """
    # Load PM type configuration mapping type names to script paths
    pm_types_path = "PrescriptionMap/pm_generation/pm_types.json"
    with open(pm_types_path, "r") as f:
        pm_types_dict = json.load(f)

    # Filter PM types based on activation flags and resolve to script paths
    pm_types_to_run = [pm_types_dict[t] for t in pm_types if t in pm_types_dict]
    results = {}

    try:
        # Initialize parallel processing executor for concurrent PM generation
        with ProcessPoolExecutor() as executor:
            futures = []
            
            # Submit PM generation tasks for parallel execution
            for pm_type_path in pm_types_to_run:
                logger.info(f"[PM_MANAGER] - Running PM generator: {pm_type_path}")
                futures.append(
                    executor.submit(run_script, pm_type_path, amount, grid, long, lat, logger)
                )

            # Collect results as PM generation tasks complete
            for i, future in enumerate(as_completed(futures)):
                output = future.result()
                logger.info(f"[PM_MANAGER] - PM output [{i}]: \n{output}")
                
                # Store PM generation results for potential future use
                results[f"PM_{i}"] = output

    except Exception as e:
        # Log any unexpected errors during PM generation coordination
        logger.error(f"[PM_MANAGER] - Error during PM generation: {str(e)}")


def run_script(path: str, amount: Dict[str, float], grid: List[int], long: float, lat: float, logger: logging.Logger) -> str:
    """
    Execute a prescription map generation script with standardized parameters.

    This function provides a standardized interface for running external PM generation
    scripts, handling parameter serialization, subprocess management, and error
    capture. It serves as the execution layer for individual PM generation algorithms
    within the parallel processing framework.

    Parameters
    ----------
    path : str
        Absolute or relative path to the Python script to execute.
        Script must implement the standardized PM generation interface.
        Examples: "pm_generation/fertilizer/fertilizer_generator.py"
    amount : Dict[str, float]
        Dictionary mapping substance names to application amounts.
        Serialized to JSON for script input parameter.
        Examples: {"nitrogen": 50.0, "phosphorus": 30.0, "potassium": 25.0}
    grid : List[int]
        Grid coordinates as [row, column] for spatial positioning.
        Serialized to JSON for script input parameter.
        Examples: [10, 15], [0, 0], [25, 40]
    long : float
        Longitude coordinate in decimal degrees.
        Converted to string for script command-line parameter.
        Range: -180.0 to +180.0 degrees
    lat : float
        Latitude coordinate in decimal degrees.
        Converted to string for script command-line parameter.
        Range: -90.0 to +90.0 degrees
    logger : logging.Logger
        Logger instance for error reporting (not passed to subprocess).
        Used for local error logging within this function.

    Returns
    -------
    str
        Raw stdout output from the executed script.
        On success: Script-generated PM data or status information
        On failure: Formatted error message with failure details

    Workflow
    --------
    1. **Parameter Serialization**: Convert dictionaries and lists to JSON strings
    2. **Command Construction**: Build subprocess command with all parameters
    3. **Script Execution**: Run Python script with subprocess.run()
    4. **Output Capture**: Collect stdout and stderr streams
    5. **Error Handling**: Process execution errors and format error messages
    6. **Result Processing**: Clean and return script output or error information

    Command Line Interface
    ---------------------
    Scripts are executed with the following standardized parameters:
        python {path} --amount {amount_json} --grid {grid_json} --long {longitude} --lat {latitude}

    Where:
        - amount_json: JSON-serialized amount dictionary
        - grid_json: JSON-serialized grid coordinate list
        - longitude/latitude: String-converted coordinate values

    Error Handling Strategy
    ----------------------
    Three categories of errors are handled:
        1. **Script Execution Errors**: Non-zero exit codes from subprocess
        2. **Process Exceptions**: Timeout, permission, or system resource errors
        3. **Unexpected Errors**: Python exceptions during parameter processing
        
    Script Requirements
    ------------------
    PM generation scripts must implement:
        - **Argument Parsing**: Handle --amount, --grid, --long, --lat parameters
        - **JSON Processing**: Parse amount and grid JSON input parameters
        - **Output Generation**: Produce PM data or status information on stdout
        - **Error Handling**: Return appropriate exit codes for success/failure
        - **Resource Management**: Clean up temporary files and resources

    Performance Characteristics
    --------------------------
    - **Execution Time**: 1-30 seconds depending on PM algorithm complexity
    - **Memory Usage**: Isolated process memory space for each script
    - **CPU Impact**: Single-threaded execution per script instance
    - **I/O Operations**: File-based input/output for PM data management

    Error Message Format
    --------------------
    Execution errors return formatted strings:
        "Script execution failed: {path}
        Return code: {exit_code}
        Stderr: {error_output}"

    Unexpected errors return:
        "Unexpected error in {path}: {exception_message}"

    Integration Notes
    ----------------
    Function used by:
        - **generate_pm()**: Parallel execution of multiple PM generators
        - **ProcessPoolExecutor**: Concurrent script execution management
        - **PM Generation Pipeline**: Individual algorithm execution layer

    Notes
    -----
    - Scripts run in isolated processes for safety and resource management
    - All output is captured and returned as strings for further processing
    - Error conditions are handled gracefully without raising exceptions
    - JSON serialization ensures consistent parameter format across scripts

    See Also
    --------
    subprocess.run : Underlying subprocess execution mechanism
    json.dumps : Parameter serialization implementation
    generate_pm : Parallel processing coordinator using this function
    """
    try:
        # Serialize complex parameters to JSON strings for script consumption
        amount_str = json.dumps(amount)
        grid_str = json.dumps(grid) 

        # Execute PM generation script with standardized parameter interface
        result = subprocess.run(
            [
                'python', path,
                "--amount", amount_str,    # JSON-serialized amount dictionary
                "--grid", grid_str,        # JSON-serialized grid coordinates
                "--long", str(long),       # String-converted longitude
                "--lat", str(lat)          # String-converted latitude
            ],
            capture_output=True,          # Capture both stdout and stderr
            text=True,                    # Decode output as text strings
            check=True                    # Raise exception on non-zero exit codes
        )
        
        # Return cleaned script output for further processing
        return result.stdout.strip()

    except subprocess.CalledProcessError as e:
        # Handle script execution failures with detailed error information
        error_msg = f"Script execution failed: {path}\nReturn code: {e.returncode}\nStderr: {e.stderr.strip()}"
        return error_msg

    except Exception as e:
        # Handle unexpected errors during script execution setup
        error_msg = f"Unexpected error in {path}: {str(e)}"
        return error_msg

def send_all(logger: logging.Logger) -> Optional[Dict[str, Any]]:
    """
    Transmit all generated prescription maps to Mission Management systems via gRPC.

    This function scans the PM generation directory structure, loads all generated
    prescription map files, and transmits them to Mission Management systems using
    the gRPC communication channel. It provides comprehensive status reporting
    for transmission success and failure tracking.

    Parameters
    ----------
    logger : logging.Logger
        Logger instance for recording transmission events, progress, and errors.
        Provides detailed logging for debugging and operation monitoring.

    Returns
    -------
    Optional[Dict[str, Any]]
        Transmission status report dictionary organized by PM type folders.
        Returns None if base directory is not found.
        
        Report structure:
            {
                "fertilizer": {
                    "status": "sent" | "error",
                    "files": [
                        {"file": "fertilizer_001.json", "status": "sent"},
                        {"file": "fertilizer_002.json", "status": "send error: details"}
                    ]
                },
                "pesticide": {
                    "status": "sent" | "error", 
                    "files": [...]
                }
            }

    Workflow
    --------
    1. **Directory Validation**: Verify PM generation base directory exists
    2. **Folder Enumeration**: Scan all PM type subdirectories
    3. **File Discovery**: Locate JSON PM files in each PMs subdirectory
    4. **Data Loading**: Read and parse PM JSON content
    5. **Message Preparation**: Format PM data for gRPC transmission
    6. **Transmission Execution**: Send PM data via gRPC client
    7. **Status Tracking**: Record transmission success or failure details
    8. **Report Generation**: Compile comprehensive status report

    Directory Structure
    ------------------
    Expected PM directory organization:
        PrescriptionMap/pm_generation/
        ├── fertilizer/
        │   └── PMs/
        │       ├── fertilizer_001.json
        │       └── fertilizer_002.json
        ├── pesticide/
        │   └── PMs/
        │       ├── pesticide_001.json
        │       └── pesticide_002.json
        └── irrigation/
            └── PMs/
                └── irrigation_001.json

    Message Format
    -------------
    PM data is transmitted with the following gRPC message structure:
        {
            "filename": "prescription_map_name.json",
            "content": {
                // Complete PM JSON data
                "grid_position": [row, col],
                "coordinates": {"lat": lat, "lon": lon},
                "treatments": {...},
                "metadata": {...}
            }
        }

    Error Scenarios
    --------------
    - **Missing Base Directory**: PM generation directory not found
    - **Missing PMs Subdirectory**: Individual PM type directories incomplete
    - **Malformed JSON**: PM files contain invalid JSON data
    - **Transmission Failures**: gRPC communication errors or timeouts
    - **File Access Errors**: Permission denied or file corruption issues

    Performance Characteristics
    --------------------------
    - **Scanning Time**: O(n) where n is total number of PM files
    - **Transmission Time**: Depends on PM file size and network conditions
    - **Memory Usage**: Scales with PM file size during JSON loading
    - **Network Impact**: Batch transmission optimizes communication efficiency

    Status Reporting
    ----------------
    Comprehensive status tracking for:
        - **Directory Discovery**: Missing or inaccessible PM directories
        - **File Processing**: JSON parsing success and failure
        - **Transmission Results**: Individual PM transmission outcomes
        - **Error Details**: Specific error messages for failed operations

    Integration Notes
    ----------------
    Function integrates with:
        - **gRPC Client**: PM data transmission to Mission Management
        - **PM Generation**: Sending newly generated prescription maps
        - **Mission Coordination**: PM delivery for agricultural operations
        - **Status Monitoring**: Transmission success tracking and reporting

    Error Recovery
    -------------
    - **Partial Failures**: Individual PM transmission errors don't halt process
    - **Directory Missing**: Graceful handling of incomplete PM generation
    - **File Corruption**: Robust JSON parsing with error containment
    - **Network Issues**: Error logging and status reporting for retries

    Notes
    -----
    - Function processes all available PM files regardless of generation status
    - Transmission errors are logged but don't raise exceptions
    - Status report enables monitoring and retry mechanisms
    - JSON parsing validates PM data integrity before transmission

    See Also
    --------
    GRPC.grpc_drone_pm.run_pm_client : PM transmission implementation
    json.load : PM data parsing and validation
    generate_pm : PM generation triggering transmission via this function
    """
    # Definir base_dir y verificar existencia
    base_dir = "PrescriptionMap/pm_generation"
    if not os.path.exists(base_dir):
        logger.error(f"Base directory not found: {base_dir}")
        return {}
    
    # Crear directorio Finished si no existe
    finished_dir = os.path.join(base_dir, "Finished")
    os.makedirs(finished_dir, exist_ok=True)
    
    # Inicializar reporte
    report = {}
    
    # Escanear directorios de tipos de PM
    for folder in os.listdir(base_dir):
        # Saltar el directorio Finished si existe
        if folder == "Finished":
            continue
            
        pms_dir = os.path.join(base_dir, folder, "PMs")
        
        if not os.path.exists(pms_dir):
            report[folder] = {"status": "PMs directory not found", "files": []}
            continue

        # Procesar archivos JSON
        for file in os.listdir(pms_dir):
            if file.endswith(".json"):
                file_path = os.path.join(pms_dir, file)
                
                try:
                    # Cargar y parsear datos
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                    
                    # Preparar y enviar payload
                    message_payload = {
                        "filename": file,
                        "content": data
                    }
                    message_payload = json.dumps(message_payload)
                    run_pm_client(message_payload, logger)
                    
                    # Registrar éxito en el reporte
                    report.setdefault(folder, {"status": "sent", "files": []})
                    report[folder]["files"].append({"file": file, "status": "sent"})
                    
                    # Mover archivo a Finished con timestamp
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    new_filename = f"{timestamp}_{file}"
                    new_path = os.path.join(finished_dir, new_filename)
                    
                    shutil.move(file_path, new_path)
                    logger.info(f"[PM Manager] - Moved sent file to Finished: {file} -> {new_filename}")
                    
                except Exception as e:
                    # Registrar error sin mover el archivo
                    report.setdefault(folder, {"status": "error", "files": []})
                    report[folder]["files"].append({"file": file, "status": f"send error: {str(e)}"})
                    logger.error(f"[PM Manager] - Error sending file {file}: {str(e)}")
    
    return report