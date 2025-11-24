#!/usr/bin/env python3

"""
Raspberry Pi Camera Capture Module
==================================

This module provides direct interface to Raspberry Pi camera hardware using PiCamera2
library for high-quality image capture during drone operations. It implements a
command-line camera script compatible with the drone's take_photo interface,
supporting configurable output paths and standardized image formats.

The module serves as a hardware-specific camera implementation for Raspberry Pi-based
drone systems, providing reliable image capture with optimal camera settings for
aerial photography and mission documentation.

.. module:: pi_camera
    :synopsis: Raspberry Pi camera hardware interface for drone photography

Features
--------
- **PiCamera2 Integration**: Native Raspberry Pi camera support with hardware optimization
- **Command-Line Interface**: Standard -o parameter support for output filename specification
- **Automatic Path Management**: Intelligent output directory creation and path resolution
- **Hardware Optimization**: Camera warm-up timing and configuration for optimal image quality
- **Standardized Output**: Consistent image format and resolution for mission compatibility
- **Error Prevention**: Robust path handling and directory creation for reliable operation

Hardware Requirements
--------------------
- **Raspberry Pi**: Models 3, 4, or newer with camera connector
- **Pi Camera Module**: v1, v2, v3, or HQ camera module support
- **System Libraries**: PiCamera2 library and OpenCV for image processing
- **Storage**: Sufficient disk space for image storage in Images/Camera directory

Image Specifications
-------------------
Camera capture settings:
    - **Resolution**: 1280x960 pixels (4:3 aspect ratio)
    - **Format**: XRGB8888 raw format for maximum quality
    - **Color Space**: RGB color representation
    - **File Format**: JPEG compression for storage efficiency
    - **Quality**: High-quality settings optimized for analysis

Workflow
--------
Camera Capture Pipeline:
    1. **Command Line Parsing**: Process -o parameter for output filename
    2. **Path Resolution**: Calculate absolute paths and create output directories
    3. **Camera Initialization**: Hardware warm-up and configuration setup
    4. **Capture Configuration**: Set resolution, format, and quality parameters
    5. **Image Acquisition**: Capture raw frame data from camera sensor
    6. **Image Processing**: Convert and save image using OpenCV
    7. **Resource Cleanup**: Automatic camera resource release

Command Line Interface
---------------------
Script accepts the following parameters:
    -o, --output FILENAME
        Output filename for captured image.
        Default: "captured.jpg"
        Image saved to: Images/Camera/{FILENAME}

Directory Structure
------------------
Output images are automatically saved to:
    WORKSPACE_ROOT/Images/Camera/{filename}
    
Where WORKSPACE_ROOT is calculated relative to script location:
    - Script location: Sensors/Cameras/pi_camera.py
    - Workspace root: ../../ (two levels up)
    - Output directory: Images/Camera/

Dependencies
-----------
- **argparse**: Command-line argument parsing and validation
- **time.sleep**: Camera hardware warm-up timing control
- **os**: File system path manipulation and directory operations
- **cv2 (OpenCV)**: Image processing and file format conversion
- **picamera2**: Raspberry Pi camera hardware interface library

Examples
--------
Command line usage:

.. code-block:: bash

    # Capture with default filename
    python3 pi_camera.py
    # Output: Images/Camera/captured.jpg
    
    # Capture with custom filename
    python3 pi_camera.py -o mission_001.jpg
    # Output: Images/Camera/mission_001.jpg
    
    # GPS-based filename (called by take_photo module)
    python3 pi_camera.py -o "40.123456_-74.987654.jpg"
    # Output: Images/Camera/40.123456_-74.987654.jpg

Integration Usage:

.. code-block:: python

    # Called via take_photo module
    import subprocess
    subprocess.run([
        "python3", "Sensors/Cameras/pi_camera.py", 
        "-o", "aerial_survey_001.jpg"
    ], check=True)

Performance Characteristics
--------------------------
- **Initialization Time**: ~1-2 seconds including warm-up period
- **Capture Time**: ~0.5-1 second for image acquisition and processing
- **Image Size**: ~200-500KB depending on scene complexity
- **Memory Usage**: Minimal footprint with efficient resource management
- **CPU Impact**: Low processing overhead with hardware acceleration

Error Handling
--------------
Common error scenarios:
    - **Hardware Unavailable**: Camera module not connected or recognized
    - **Permission Issues**: Insufficient privileges for camera access
    - **Storage Problems**: Disk full or write permission denied
    - **Library Missing**: PiCamera2 or OpenCV not properly installed

Troubleshooting
--------------
- **Camera Not Found**: Verify camera module connection and enable camera interface
- **Permission Denied**: Run with appropriate user privileges or add user to video group
- **Library Errors**: Install required dependencies: pip install picamera2 opencv-python
- **Path Issues**: Ensure script is run from correct directory context

Notes
-----
- Script designed for standalone execution and integration via take_photo module
- Camera warm-up period prevents blurred or improperly exposed images
- Output directory creation ensures reliable file storage
- XRGB8888 format provides maximum image quality for analysis applications
- Context manager ensures proper camera resource cleanup

See Also
--------
Sensors.take_photo : Primary interface for camera operations
Images.analyze_image : Post-capture image analysis and processing
picamera2.Picamera2 : Underlying camera hardware interface
cv2.imwrite : Image file format conversion and storage
"""

import argparse
from time import sleep
import os
import cv2
from picamera2 import Picamera2

if __name__ == "__main__":
    """
    Main execution block for Raspberry Pi camera capture script.
    
    This block implements the complete camera capture workflow from command-line
    argument parsing through image acquisition and storage. It serves as the
    primary entry point for drone camera operations when called via the
    take_photo module interface.
    
    Workflow Steps:
    1. Command-line argument parsing and validation
    2. Output path calculation and directory creation
    3. Camera hardware initialization and warm-up
    4. Image capture configuration and execution
    5. Image processing and file storage
    6. Resource cleanup and status reporting
    
    Command Line Arguments:
    ----------------------
    -o, --output : str, optional
        Output filename for the captured image.
        Default: "captured.jpg"
        The image will be saved to Images/Camera/{filename}
    
    Path Resolution:
    ---------------
    The script automatically calculates the workspace root directory
    relative to its own location and creates the appropriate output
    directory structure for consistent image storage.
    
    Error Handling:
    --------------
    The script relies on Python's exception handling for error management:
    - Camera initialization errors halt execution
    - Path creation errors are handled by os.makedirs
    - Image capture errors terminate the process
    
    Integration Notes:
    -----------------
    This script is designed to be called by the take_photo module
    using subprocess.run() with the -o parameter for filename specification.
    The standardized interface ensures compatibility with the broader
    drone camera management system.
    """
    # Parse command-line arguments for output filename specification
    parser = argparse.ArgumentParser(description="Capture and save an image with PiCamera2.")
    parser.add_argument("-o", "--output", default="captured.jpg",
                        help="Filename to save the captured image (will be placed in Images/Camera/).")
    args = parser.parse_args()

    # Calculate absolute paths for reliable file storage
    # Always save to Images/Camera/{filename} relative to workspace root
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # Current script directory
    WORKSPACE_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))  # Navigate to workspace root
    output_dir = os.path.join(WORKSPACE_ROOT, "Images", "Camera")  # Construct output directory path
    os.makedirs(output_dir, exist_ok=True)  # Create directory structure if it doesn't exist
    output_path = os.path.join(output_dir, args.output)  # Complete output file path

    # Camera hardware warm-up period for optimal image quality
    sleep(1)  # Let camera warm up

    # Initialize camera hardware and capture image using context manager
    with Picamera2() as picam2:
        # Configure camera for high-quality still image capture
        config = picam2.create_still_configuration(main={'size': (1280, 960), 'format': 'XRGB8888'})
        picam2.configure(config)  # Apply configuration to camera hardware
        picam2.start()  # Start camera preview and prepare for capture

        # Capture and save image with status reporting
        print("Capturing image...")
        frame = picam2.capture_array()  # Capture raw image data as numpy array
        cv2.imwrite(output_path, frame)  # Convert and save image to specified path
        print(f"Image saved to {output_path}")  # Confirm successful image storage