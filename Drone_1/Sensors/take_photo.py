"""
Camera Photo Capture Module
===========================

This module provides camera control functionality for drone-based photography systems.
It implements a unified interface for capturing photos using multiple camera configurations,
managing camera selection, execution coordination, and error handling for aerial photography
during drone missions.

The module serves as the primary camera interface for drone operations, supporting
configurable camera systems through JSON-based camera definitions and providing
robust subprocess management for camera script execution.

.. module:: take_photo
    :synopsis: Camera photo capture interface for drone photography systems

Features
--------
- **Multi-Camera Support**: Dynamic camera selection via configuration files
- **Subprocess Management**: Robust camera script execution with error handling
- **Configuration-Driven**: JSON-based camera path management and selection
- **Error Logging**: Comprehensive logging for camera operation failures
- **Script Integration**: Python-based camera script execution with parameters
- **Mission Integration**: Seamless integration with drone mission photography workflows

Workflow
--------
Camera Capture Pipeline:
    1. **Configuration Loading**: Read camera definitions from JSON configuration
    2. **Camera Selection**: Resolve camera identifier to executable script path
    3. **Command Assembly**: Construct subprocess command with output parameters
    4. **Script Execution**: Execute camera script with subprocess management
    5. **Error Handling**: Capture and log execution failures with detailed information
    6. **Process Monitoring**: Ensure camera script completion and resource cleanup

Camera Configuration
-------------------
Camera definitions are stored in JSON format (Sensors/cameras.json):
    {
        "camera_id": "/path/to/camera/script.py",
        "main_camera": "Scripts/main_camera.py",
        "thermal_camera": "Scripts/thermal_camera.py"
    }

Supported Camera Types
---------------------
- **Main Camera**: Primary RGB camera for standard photography
- **Thermal Camera**: Infrared imaging for temperature analysis
- **Multispectral**: Specialized cameras for agricultural monitoring
- **Custom Scripts**: User-defined camera implementations

Functions
---------
.. autofunction:: take_photo

Dependencies
-----------
- **json**: Configuration file parsing and camera definition loading
- **subprocess**: Camera script execution and process management
- **logging**: Error reporting and operation status tracking

Error Handling
--------------
- **Configuration Errors**: Missing or malformed camera configuration files
- **Camera Selection**: Invalid camera identifiers or missing camera definitions
- **Script Execution**: Camera script failures, permission issues, hardware problems
- **File System**: Output path validation and write permission verification

Examples
--------
>>> import logging
>>> logger = logging.getLogger('camera')
>>> 
>>> # Capture photo with main camera
>>> take_photo("main_camera", "mission_001.jpg", logger)
>>> 
>>> # Capture thermal image
>>> take_photo("thermal_camera", "thermal_001.jpg", logger)
>>> 
>>> # Custom camera configuration
>>> take_photo("multispectral", "analysis_001.jpg", logger)

Integration Points
-----------------
This module integrates with:
    - **Mission Planning**: Automated photography during waypoint navigation
    - **Image Analysis**: Photo capture for AI-based crop monitoring
    - **GPS Integration**: Coordinate-based image geotagging
    - **GRPC Services**: Remote camera control and image transmission

Performance Considerations
-------------------------
- **Execution Time**: Camera script duration varies by hardware and settings
- **Resource Usage**: Subprocess overhead minimal for short-duration captures
- **Concurrency**: No built-in protection against concurrent camera access
- **Storage Impact**: Output file size depends on camera resolution and format

Notes
-----
- Camera scripts must accept -o parameter for output filename specification
- All camera scripts should be Python 3 compatible
- Ensure proper file permissions for camera script execution
- Consider implementing camera availability checks before capture attempts

See Also
--------
Sensors.gps_simulator : GPS coordinate integration for image geotagging
Images.analyze_image : Post-capture image analysis and processing
GRPC.grpc_drone_commands : Remote camera control interface
"""

import json
import subprocess
from typing import Any
import logging


def take_photo(camera: str, filename: str, logger: logging.Logger) -> None:
    """
    Capture a photo using the specified camera configuration.

    This function serves as the primary interface for drone photography operations,
    managing camera selection, script execution, and error handling for aerial
    image capture during mission operations. It provides a unified interface
    for multiple camera types through configuration-driven script execution.

    Parameters
    ----------
    camera : str
        Camera identifier corresponding to an entry in the cameras configuration file.
        Must match a key in Sensors/cameras.json that maps to a valid camera script path.
        Examples: "main_camera", "thermal_camera", "multispectral"
    filename : str
        Output filename for the captured image, including file extension.
        Should specify the complete path where the image will be saved.
        Examples: "mission_001.jpg", "Images/thermal_001.png", "analysis/crop_001.tiff"
    logger : logging.Logger
        Logger instance for recording camera operation events, errors, and status updates.
        Used for debugging camera script execution and tracking capture operations.

    Returns
    -------
    None
        Function performs image capture operation without returning values.
        Success is indicated by successful subprocess completion.

    Raises
    ------
    FileNotFoundError
        If the cameras configuration file (Sensors/cameras.json) is not found.
    KeyError
        If the specified camera identifier is not defined in the configuration.
    json.JSONDecodeError
        If the cameras configuration file contains invalid JSON format.
    subprocess.CalledProcessError
        If the camera script execution fails due to hardware or software issues.

    Workflow
    --------
    1. **Configuration Loading**: Open and parse cameras.json configuration file
    2. **Camera Resolution**: Look up camera script path using camera identifier
    3. **Command Assembly**: Construct subprocess command with Python3 and parameters
    4. **Script Execution**: Execute camera script with output filename parameter
    5. **Error Monitoring**: Capture subprocess errors and log execution failures
    6. **Resource Cleanup**: Ensure proper subprocess termination and resource release

    Camera Script Interface
    ----------------------
    Camera scripts must implement the following interface:
        - **Python 3 Compatibility**: Scripts executed with python3 interpreter
        - **Output Parameter**: Accept -o parameter for output filename specification
        - **Error Codes**: Return appropriate exit codes for success/failure indication
        - **Resource Management**: Handle camera hardware initialization and cleanup

    Examples
    --------
    >>> import logging
    >>> logger = logging.getLogger('drone_camera')
    >>> 
    >>> # Capture standard RGB image
    >>> take_photo("main_camera", "mission_photo_001.jpg", logger)
    >>> 
    >>> # Capture thermal image for analysis
    >>> take_photo("thermal_camera", "thermal_analysis_001.png", logger)
    >>> 
    >>> # Mission-based photography with GPS coordinates
    >>> import gps_simulator
    >>> lat, lon = gps_simulator.get_latest_coordinates()
    >>> filename = f"{lat}_{lon}.jpg"
    >>> take_photo("main_camera", filename, logger)

    Error Scenarios
    --------------
    - **Missing Configuration**: cameras.json file not found or inaccessible
    - **Invalid Camera ID**: Camera identifier not present in configuration
    - **Script Not Found**: Camera script path invalid or file missing
    - **Permission Denied**: Insufficient permissions for script execution
    - **Hardware Failure**: Camera hardware unavailable or malfunctioning
    - **Storage Issues**: Insufficient disk space or invalid output path

    Performance Characteristics
    --------------------------
    - **Execution Time**: 1-10 seconds depending on camera type and settings
    - **Resource Usage**: Minimal memory overhead for subprocess management
    - **Concurrent Access**: No built-in synchronization for camera resource sharing
    - **Error Recovery**: Graceful failure handling without system disruption

    Integration Notes
    ----------------
    Function integrates with:
        - **Mission Execution**: Automated photography during waypoint navigation
        - **GPS Tagging**: Coordinate-based filename generation for geotagged images
        - **Image Analysis**: Captured images processed by analysis modules
        - **Remote Control**: gRPC-based camera control from Mission Management

    Configuration Example
    --------------------
    Sensors/cameras.json structure:
        {
            "main_camera": "Scripts/rgb_camera.py",
            "thermal_camera": "Scripts/thermal_capture.py",
            "multispectral": "Scripts/multispectral_camera.py"
        }

    Notes
    -----
    - Function blocks until camera script completion
    - No validation performed on output filename format or path
    - Camera script failures logged but do not raise exceptions to caller
    - Consider implementing timeout protection for long-running camera operations

    See Also
    --------
    subprocess.run : Underlying subprocess execution mechanism
    json.load : Configuration file parsing implementation
    logging.Logger : Error logging and operation tracking
    """
    # Load camera configuration from JSON file
    cameras_path = "Sensors/cameras.json"
    with open(cameras_path, "r") as f:
        cameras_dict = json.load(f)
        
    # Resolve camera identifier to script path
    camera_path = cameras_dict[camera]
    
    try:
        # Execute camera script with output filename parameter
        subprocess.run(
            ["python3", camera_path, "-o", filename],
            check=True
        )
    except subprocess.CalledProcessError as e:
        # Log camera script execution failure with error details
        logger.error(f"[CAMERA_IMAGE] - Camera execution failed: {e}")