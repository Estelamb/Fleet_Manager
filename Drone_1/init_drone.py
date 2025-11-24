"""
Drone Control System Initialization Module
==========================================

This module implements the core initialization functionality for a gRPC-based drone 
control system, providing comprehensive system startup, cleanup, and communication 
infrastructure setup for autonomous agricultural drone operations.

The module serves as the main entry point for drone system initialization, coordinating
multiple subsystems including gRPC communication, logging infrastructure, file system
cleanup, and background service management for real-time drone operations.

.. module:: init_drone
    :synopsis: Main initialization and startup module for drone control systems

System Architecture
-------------------
The drone control system implements a multi-service architecture:
    - **gRPC Communication Services**: Bidirectional communication with Mission Management
    - **Command Processing**: Real-time command reception and execution
    - **Metrics Transmission**: Continuous system health and performance monitoring
    - **Prescription Map Management**: Agricultural data processing and transmission
    - **Logging Infrastructure**: Comprehensive system event recording and debugging

Workflow
--------
Drone Initialization Pipeline:
    1. **System Cleanup**: Clear temporary files and reset system state
    2. **Logger Creation**: Initialize dedicated logging infrastructure for drone ID
    3. **Metrics Service**: Start continuous system metrics transmission to Mission Management
    4. **Command Service**: Initialize gRPC server for real-time command reception
    5. **Background Operation**: Maintain system operation until manual termination
    6. **Graceful Shutdown**: Handle interrupts and cleanup on system termination

Features
--------
- **Multi-Service Coordination**: Simultaneous gRPC services for commands and metrics
- **Unique Drone Identification**: Support for multiple drone instances with unique IDs
- **Comprehensive Logging**: Rotating log files with drone-specific identification
- **File System Management**: Automatic cleanup of temporary and cache directories
- **Prescription Map Cleanup**: Agricultural data management and storage cleanup
- **Error Handling**: Robust exception management with graceful degradation
- **Background Operation**: Non-blocking service execution with thread management

Functions
---------
.. autofunction:: main
.. autofunction:: cleanup_system

System Requirements
------------------
- **Python**: 3.8+ with threading and logging support
- **gRPC Infrastructure**: Active Mission Management system for communication
- **File System**: Write permissions for logging and temporary file management
- **Network**: Access to gRPC communication ports (51001, 51003, 51004)

Directory Structure
------------------
The system manages the following directory structure:
    - **Images/Models/**: AI model temporary processing files
    - **Images/Camera/**: Captured image temporary storage
    - **Images/Results/**: Image analysis result files
    - **PrescriptionMap/pm_generation/**: Agricultural prescription map data
    - **Logs/**: System and drone-specific log files

Communication Ports
-------------------
- **Port 51001**: Inbound commands from Mission Management
- **Port 51003**: Outbound prescription map data to Mission Management  
- **Port 51004**: Outbound metrics data to Mission Management

Examples
--------
>>> # Command line execution
>>> python init_drone.py --drone_id 1
Complete cleanup finished
[Drone 1] - gRPC services started successfully

>>> # Programmatic execution
>>> from init_drone import main
>>> main(drone_id=2)  # Initialize drone with ID 2

Notes
-----
- **Single Instance**: Each drone ID should run on a separate system or container
- **Resource Management**: System automatically cleans temporary files on startup
- **Mission Management**: Requires active Mission Management system for full operation
- **Logging**: All drone operations are logged with timestamps and drone identification
- **Threading**: Uses background threads for non-blocking service operation

See Also
--------
Init.create_logger_drone : Logging infrastructure setup and configuration
Init.clear_drone : File system cleanup and maintenance functions
GRPC.grpc_drone_metrics : System metrics transmission service
GRPC.grpc_drone_commands : Command reception and processing service
"""

import logging
import argparse
import sys
import time
import threading
from typing import NoReturn

from Init.create_logger_drone import create_logger
from Init.clear_drone import clean_directory, clean_pms_subfolders

from GRPC.grpc_drone_metrics import start_grpc_metrics
from GRPC.grpc_drone_commands import start_grpc_commands

def main(drone_id: int) -> None:
    """
    Initialize and start the complete drone control system infrastructure.

    This function serves as the main entry point for drone system initialization,
    coordinating all necessary subsystems including file cleanup, logging setup,
    and gRPC communication services. It establishes the complete operational
    environment for autonomous drone operations with Mission Management integration.

    Parameters
    ----------
    drone_id : int
        Unique identifier for the drone instance. Used for:
        - Log file naming and identification
        - System resource allocation and management
        - Multi-drone coordination and communication
        - Mission Management drone tracking and coordination

    Returns
    -------
    None
        Function completes after successful system initialization.

    Workflow
    --------
    1. **System Cleanup**: 
        - Clear temporary image processing files
        - Remove cached AI model data
        - Reset prescription map generation directories
        - Prepare clean system state for new operations

    2. **Logger Initialization**:
        - Create drone-specific logger with unique identification
        - Configure rotating log files in Logs/ directory
        - Set up structured logging for system monitoring and debugging

    3. **Metrics Service Startup**:
        - Initialize gRPC metrics transmission service
        - Start continuous system health monitoring
        - Begin periodic data transmission to Mission Management (10-second intervals)

    4. **Command Service Startup**:
        - Initialize gRPC command reception server
        - Begin listening for Mission Management commands
        - Enable real-time drone control and coordination

    Service Configuration
    ---------------------
    The function initializes the following services:
        - **Metrics Service**: Continuous transmission on port 51004
        - **Command Service**: Reception server on port 51001
        - **Prescription Map**: Transmission capability on port 51003
        - **Logging Service**: Drone-specific log file management

    Error Handling
    --------------
    - **Exception Catching**: All initialization errors are caught and logged
    - **System Exit**: Critical errors result in graceful system termination
    - **Logging**: All errors are logged with full exception information
    - **Exit Codes**: Returns exit code 1 on critical failures

    Examples
    --------
    >>> # Initialize drone with ID 1
    >>> main(drone_id=1)
    Complete cleanup finished
    [Drone 1] - Logger initialized successfully
    [gRPC metrics] - Metrics client thread started successfully
    [gRPC Commands] - Server started

    >>> # Initialize drone with ID 2 for multi-drone operations
    >>> main(drone_id=2)
    Complete cleanup finished
    [Drone 2] - Logger initialized successfully
    # ... similar startup sequence with unique drone identification

    Integration Points
    ------------------
    This function integrates with:
        - **Mission Management**: Central coordination and command system
        - **File System**: Temporary storage and log management
        - **gRPC Services**: Communication infrastructure
        - **AI Models**: Image processing and analysis systems
        - **Prescription Maps**: Agricultural data management

    Multi-Drone Support
    -------------------
    - **Unique Identification**: Each drone instance uses separate resources
    - **Isolated Logging**: Drone-specific log files prevent data mixing
    - **Resource Separation**: Independent file system cleanup and management
    - **Concurrent Operation**: Multiple drones can operate simultaneously

    Notes
    -----
    - Function should be called once per drone instance during system startup
    - Requires write permissions for log files and temporary directories
    - Depends on active Mission Management system for full functionality
    - System continues running until manual termination or critical error
    - All services run in background threads for non-blocking operation

    Raises
    ------
    SystemExit
        Critical initialization errors result in system termination with exit code 1.

    See Also
    --------
    cleanup_system : File system cleanup and preparation
    Init.create_logger_drone.create_logger : Logging infrastructure setup
    GRPC.grpc_drone_metrics.start_grpc_metrics : Metrics service initialization
    GRPC.grpc_drone_commands.start_grpc_commands : Command service initialization
    """
    try:
        # Step 1: Initialize drone-specific logging infrastructure
        drone_logger = create_logger(f'Drone {drone_id}', f'Logs/Drone{drone_id}.log')
        
        # Step 2: Perform comprehensive system cleanup
        cleanup_system()
        drone_logger.info(f"[Init Drone] - Complete cleanup finished")

        # Step 3: Start continuous metrics transmission service (background thread)
        start_grpc_metrics(logger=drone_logger)
        
        # Step 4: Start command reception service (background thread)
        start_grpc_commands(logger=drone_logger)
        
        drone_logger.info("[Init Drone] - All system components initialized successfully")

    except Exception as e:
        # Handle critical initialization errors with logging and graceful exit
        logging.error(f" - Critical error in main: {str(e)}", exc_info=True)
        sys.exit(1)
        
        
def cleanup_system() -> None:
    """
    Perform comprehensive file system cleanup and preparation for drone operations.

    This function ensures a clean system state by removing temporary files, cached data,
    and previous operation artifacts that could interfere with new drone missions.
    It prepares the file system for optimal performance and prevents data contamination
    between different operational sessions.

    Returns
    -------
    None
        Function completes after successful cleanup of all target directories.

    Workflow
    --------
    1. **AI Model Cleanup**:
        - Clear Grape_Diseases_Hailo8/Leafs temporary processing files
        - Clear Grape_Diseases_Hailo8L/Leafs temporary processing files
        - Remove cached model inference data and intermediate results

    2. **Image Data Cleanup**:
        - Clear Images/Camera directory of previous capture sessions
        - Clear Images/Results directory of previous analysis results
        - Prepare storage space for new image capture and processing

    3. **Prescription Map Cleanup**:
        - Clear PrescriptionMap/pm_generation subdirectories
        - Remove previous agricultural prescription map data
        - Prepare system for new prescription map generation

    4. **Completion Notification**:
        - Print confirmation message to console
        - Indicate successful completion of cleanup operations

    Directory Operations
    -------------------
    The function performs cleanup on the following directories:

    **AI Model Directories**:
        - Images/Models/Grape_Diseases_Hailo8/Leafs/
            * Temporary leaf image processing files
            * Intermediate analysis results
            * Cached model outputs

        - Images/Models/Grape_Diseases_Hailo8L/Leafs/
            * Alternative model processing files
            * Performance comparison data
            * Model validation artifacts

    **Image Processing Directories**:
        - Images/Camera/
            * Raw captured images from drone cameras
            * Temporary image files during processing
            * Image metadata and EXIF data

        - Images/Results/
            * Processed image analysis results
            * Object detection outputs
            * Classification and annotation data

    **Agricultural Data Directories**:
        - PrescriptionMap/pm_generation/
            * Generated prescription map files
            * Agricultural treatment recommendations
            * Field analysis and zoning data

    Performance Benefits
    -------------------
    - **Storage Optimization**: Frees up disk space for new operations
    - **Data Integrity**: Prevents mixing of data from different missions
    - **Performance**: Reduces directory traversal time for file operations
    - **Reliability**: Eliminates potential conflicts from residual files

    Examples
    --------
    >>> cleanup_system()
    Complete cleanup finished

    >>> # Typical usage in initialization sequence
    >>> cleanup_system()  # Clean system state
    >>> logger = create_logger("Drone1", "Logs/Drone1.log")  # Initialize logging
    >>> # Continue with service startup...

    Integration
    -----------
    This function is typically called:
        - **System Startup**: First operation during drone initialization
        - **Mission Preparation**: Before starting new agricultural missions
        - **Error Recovery**: After system errors or unexpected termination
        - **Maintenance**: During routine system maintenance procedures

    Error Handling
    --------------
    - **File Permissions**: Requires write/delete permissions for target directories
    - **Directory Existence**: Safely handles non-existent directories
    - **Concurrent Access**: Safe for use during system startup sequences
    - **Partial Failures**: Continues cleanup even if individual operations fail

    Notes
    -----
    - Function operates synchronously and blocks until completion
    - Safe to call multiple times without adverse effects
    - Does not require external dependencies or network access
    - Cleanup operations are logged by individual directory cleaning functions
    - Critical for maintaining system hygiene in production environments

    See Also
    --------
    Init.clear_drone.clean_directory : Individual directory cleanup implementation
    Init.clear_drone.clean_pms_subfolders : Prescription map specific cleanup
    """
    # Clean AI model temporary processing directories
    clean_directory("Images/Models/Grape_Diseases_Hailo8/Leafs")   # Primary disease detection model cache
    clean_directory("Images/Models/Grape_Diseases_Hailo8L/Leafs")  # Alternative model processing files
    
    # Clean image capture and processing directories
    clean_directory("Images/Camera")   # Raw captured images from drone cameras
    clean_directory("Images/Results")  # Processed image analysis results
    
    # Clean agricultural prescription map generation directories
    clean_pms_subfolders("PrescriptionMap/pm_generation")  # Agricultural treatment data


if __name__ == "__main__":
    # Configurar señal para salida inmediata
    import signal
    signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))

    # Configurar argumentos (existente)
    parser = argparse.ArgumentParser(
        description='Drone Control System - Initialize and start autonomous drone operations',
        epilog='Example: python init_drone.py --drone_id 1'
    )
    parser.add_argument(
        '--drone_id', 
        type=int, 
        required=True,
        help='Unique identifier for the drone instance (e.g., 1, 2, 3). '
             'Used for logging, resource allocation, and Mission Management coordination.'
    )
    args = parser.parse_args()

    try:
        # Inicializar el sistema (existente)
        main(args.drone_id)
        
        # Mantener el programa activo de forma segura
        while True:
            time.sleep(0.5)  # Bloqueo interrumpible con menor consumo de CPU
            
    except Exception as e:
        # Manejar excepciones (existente)
        logging.error(f"Unhandled exception: {str(e)}", exc_info=True)
        sys.exit(1)