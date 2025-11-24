"""
Camera Simulator Module
=======================

This module provides camera simulation functionality for drone development and testing
environments. It implements a file-based camera interface that copies random test images 
from a predefined library to simulate camera capture, enabling development and testing
without requiring actual camera hardware.

The module serves as a drop-in replacement for hardware camera modules during
development and testing scenarios, providing identical interface compatibility while
using randomly selected test images from a predefined collection.

.. module:: camera_simulator
    :synopsis: File-based random image selection camera simulator

Features
--------
- **Random Image Selection**: Selects random images from test library
- **Hardware-Free Operation**: Camera simulation without hardware dependencies
- **Interface Compatibility**: Drop-in replacement for hardware camera modules
- **Flexible Image Selection**: Support for multiple image formats and sources
- **Test Image Library**: Access to comprehensive test image collection
- **Path Management**: Automatic workspace-relative path resolution
- **Development Support**: Consistent results for algorithm development and testing

Simulation Workflow
------------------
Camera Simulation Pipeline:
    1. **Command Line Processing**: Parse output filename parameter
    2. **Random Image Selection**: Select random image from test library
    3. **Path Resolution**: Calculate source and destination paths
    4. **File System Operation**: Copy selected image to camera output directory
    5. **Renaming**: Use specified output filename for destination file
    6. **Error Handling**: Report empty library or operation failures

Directory Structure
------------------
Image file organization:
    - **Source Directory**: Images/Test/ (test image library)
    - **Destination Directory**: Images/Camera/ (simulated camera output)
    - **Workspace Root**: Calculated relative to script location
    - **Recursive Search**: Test images can be in subdirectories

Supported Image Formats
----------------------
The simulator supports comprehensive image format compatibility:
    - **Common Formats**: .jpg, .jpeg, .png, .gif, .bmp
    - **Professional Formats**: .tiff, .tif, .webp, .heic
    - **Vector Graphics**: .svg
    - **RAW Formats**: .cr2 (Canon), .nef (Nikon), .arw (Sony), .dng (Adobe)

Use Cases
---------
- **Algorithm Development**: Random test images for computer vision development
- **System Integration**: End-to-end testing without hardware dependencies
- **Mission Simulation**: Random image sequences for mission testing
- **Continuous Integration**: Automated testing with varied image data
- **Performance Analysis**: Standardized tests with random image inputs

Global Configuration
-------------------
BASE_DIR : str
    Directory containing the camera simulator script (Sensors/Cameras/).
    Automatically calculated from script location for path resolution.

WORKSPACE_ROOT : str
    Root directory of the drone workspace, calculated relative to script location.
    Used as base path for all image directory calculations.

SOURCE_FOLDER : str
    Path to test image library directory (Images/Test/).
    Contains predefined images for simulation operations.

DESTINATION_FOLDER : str
    Path to simulated camera output directory (Images/Camera/).
    Target location for copied simulation images.

IMAGE_EXTENSIONS : set
    Set of supported image file extensions for format validation.
    Includes common, professional, and RAW image formats.

Functions
---------
.. autofunction:: copy_random_photo

Integration Points
-----------------
This module integrates with:
    - **Sensors.take_photo**: Primary camera interface for simulation mode
    - **Mission Planning**: Automated photography simulation during testing
    - **Image Analysis**: Varied test data for algorithm validation
    - **Development Workflow**: Hardware-independent development environment

Performance Characteristics
--------------------------
- **Operation Time**: File copy operations typically 10-100ms
- **Storage Impact**: Duplicate images in Camera directory
- **Memory Usage**: Minimal overhead for file operations
- **Search Performance**: O(n) scan across test image library

Configuration Requirements
-------------------------
- **Test Image Library**: Populate Images/Test/ with appropriate test images
- **Directory Permissions**: Write access to Images/Camera/ directory
- **Storage Space**: Sufficient disk space for image duplication

Examples
--------
Command line usage:

.. code-block:: bash

    # Simulate capture with random test image
    python3 camera_simulator.py -o "capture_001.jpg"
    # Copies random image to Images/Camera/capture_001.jpg

Integration usage:

.. code-block:: python

    # Called via take_photo module in simulation mode
    import subprocess
    subprocess.run([
        "python3", "Sensors/Cameras/camera_simulator.py", 
        "-o", "mission_simulation_001.jpg"
    ], check=True)

Error Handling
--------------
- **Empty Library**: Reports when no images found in test library
- **Path Issues**: Automatic directory creation for destination paths
- **Permission Errors**: File system permission validation and error reporting
- **Format Validation**: Implicit validation through extension checking

Notes
-----
- Simulator maintains identical interface to hardware camera modules
- Test image library should contain representative images for target use cases
- Recursive directory search allows organized test image libraries
- Copy operation preserves original file metadata and timestamps

See Also
--------
Sensors.take_photo : Primary camera interface using this simulator
Sensors.Cameras.pi_camera : Hardware camera module being simulated
Images.analyze_image : Image analysis using simulated camera output
shutil.copy2 : Underlying file copy operation with metadata preservation
"""

import argparse
import os
import shutil
import sys
import random
from typing import List

# Path Resolution Constants
# =========================

# This resolves to the directory Sensors/Cameras
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Current script directory location
# Go up two levels to get to workspace/
WORKSPACE_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))  # Navigate to workspace root

# Directory Configuration for Image Simulation
# ============================================

SOURCE_FOLDER = os.path.join(WORKSPACE_ROOT, "Images", "Test")  # Test image library directory
DESTINATION_FOLDER = os.path.join(WORKSPACE_ROOT, "Images", "Camera")  # Simulated camera output directory

# Supported Image Format Extensions
# =================================

IMAGE_EXTENSIONS = {
    '.jpg', '.jpeg', '.png', '.gif', '.bmp',      # Common web and photo formats
    '.tiff', '.tif', '.webp', '.heic', '.svg',    # Advanced and vector formats
    '.cr2', '.nef', '.arw', '.dng'                # Professional RAW camera formats
}

def get_all_image_files() -> List[str]:
    """
    Recursively scan the source folder and collect all supported image files.
    
    Returns:
        List of full paths to all image files found in the source directory tree
    """
    image_files = []
    for root, _, files in os.walk(SOURCE_FOLDER):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in IMAGE_EXTENSIONS:
                image_files.append(os.path.join(root, file))
    return image_files

def copy_random_photo(output_filename: str) -> None:
    """
    Copy a random test image from the test library to simulate camera capture.

    This function implements the core camera simulation logic by randomly selecting
    an image from the test library and copying it to the camera output directory
    using the specified output filename. It provides identical functionality to
    hardware camera capture while using random test images for varied results.

    Parameters
    ----------
    output_filename : str
        Filename to use for the copied image in the destination directory.

    Returns
    -------
    None
        Function performs file copy operation without returning values.
        Success is indicated by completion without exceptions.

    Workflow
    --------
    1. **Library Scan**: Collect all image files in the test library
    2. **Random Selection**: Choose a random image from available files
    3. **Path Construction**: Build source and destination file paths
    4. **Directory Creation**: Ensure destination directory exists
    5. **File Copy Operation**: Copy image with metadata preservation
    6. **Error Reporting**: Log empty library or operation failures

    Error Conditions
    ---------------
    - **Empty Library**: No images found in test library
    - **Permission Denied**: Insufficient read access to source file
    - **Disk Full**: Insufficient storage space for copy operation
    - **Path Issues**: Invalid characters in filename or path corruption

    Examples
    --------
    >>> # Copy random image to specific filename
    >>> copy_random_photo("mission_capture_001.jpg")
    >>> # Copies random image to Images/Camera/mission_capture_001.jpg

    Performance Characteristics
    --------------------------
    - **Scan Time**: O(n) where n is total number of files in test library
    - **Copy Time**: Depends on file size, typically 10-100ms for images
    - **Memory Usage**: Stores list of all image paths during operation
    - **Disk Impact**: Creates duplicate image file in destination directory

    Integration Notes
    ----------------
    Function called by:
        - **Main Script**: Direct execution via command-line interface
        - **take_photo Module**: Subprocess execution for camera simulation
        - **Test Suites**: Automated testing with random image sets
        - **Development Tools**: Varied image provision for algorithm testing

    Notes
    -----
    - Function assumes test image library is properly populated
    - No validation performed on image format or file integrity
    - Destination filename extension doesn't need to match source
    - Directory creation handled automatically for destination paths

    See Also
    --------
    os.walk : Recursive directory traversal implementation
    shutil.copy2 : File copy operation with metadata preservation
    os.makedirs : Destination directory creation
    """
    # Collect all image files in the source directory
    image_files = get_all_image_files()
    
    # Check if any images were found
    if not image_files:
        print(f"No images found in '{SOURCE_FOLDER}' with supported extensions.")
        return
    
    # Select a random image from the collected files
    selected_image = random.choice(image_files)
    
    # Construct destination path with specified filename
    dest_path = os.path.join(DESTINATION_FOLDER, output_filename)
    
    # Ensure destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    # Copy selected image to destination with new name
    shutil.copy2(selected_image, dest_path)

if __name__ == "__main__":
    """
    Main execution block for camera simulation script.
    
    This block implements the complete camera simulation workflow from command-line
    argument parsing through random image selection and copying. It provides identical
    interface compatibility with hardware camera modules while using random test images.
    
    Workflow Steps:
    1. Command-line argument parsing for output filename
    2. Random image selection from test library
    3. File copy operation to simulate camera capture
    4. Renaming of copied file to specified output filename
    5. Status reporting and error handling
    
    Command Line Interface:
    ----------------------
    The script accepts the same parameters as hardware camera modules:
    
    -o, --output : str, optional
        Output filename for the simulated camera capture.
        Default: "captured.jpg"
    
    Simulation Process:
    ------------------
    Instead of capturing from hardware, the script:
    1. Scans Images/Test/ for all supported images
    2. Randomly selects one image from the collection
    3. Copies it to Images/Camera/ with specified filename
    
    Error Handling:
    --------------
    - Empty test library results in console error message
    - File system errors are handled by underlying Python libraries
    - Invalid arguments handled by argparse with help messages
    
    Integration Compatibility:
    -------------------------
    This script serves as a drop-in replacement for hardware camera modules:
    - Identical command-line interface (-o parameter)
    - Same output directory structure (Images/Camera/)
    - Compatible with take_photo module subprocess execution
    - Maintains interface contracts for downstream processing
    
    Development Benefits:
    --------------------
    - Hardware-independent development and testing
    - Varied image data for robust testing
    - Faster iteration cycles without camera setup
    - Randomized test scenarios with diverse image content
    """
    # Parse command-line arguments with identical interface to hardware cameras
    parser = argparse.ArgumentParser(description="Simulate camera capture with random test image.")
    parser.add_argument("-o", "--output", default="captured.jpg",
                        help="Filename to use for the captured image (will be placed in Images/Camera/).")
    args = parser.parse_args()
    
    # Execute camera simulation by copying random test image
    copy_random_photo(args.output)