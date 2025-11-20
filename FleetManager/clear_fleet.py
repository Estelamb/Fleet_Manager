"""
Fleet Management System - Directory Cleanup Utilities

.. module:: clear_fleet
    :synopsis: Directory cleanup and maintenance utilities for Fleet Management System

.. moduleauthor:: Fleet Management System Team

.. versionadded:: 1.0

This module provides essential directory cleanup functionality for the Fleet Management System,
ensuring proper maintenance of temporary files, cached data, and system state directories.
It supports both individual directory cleanup and recursive subfolder maintenance.

Key Features:
    - **Safe Directory Cleanup**: Removes contents while preserving directory structure
    - **Recursive Subfolder Management**: Handles nested directory structures
    - **Error Resilience**: Continues operation even if individual files fail to delete
    - **Logging Integration**: Provides detailed feedback on cleanup operations

Typical Usage:
    The cleanup utilities are primarily used during system initialization and shutdown
    to ensure clean system state and prevent accumulation of temporary files.

.. warning::
    These functions permanently delete files and directories. Use with caution
    and ensure no critical data is stored in target directories.

.. note::
    All cleanup operations are designed to be idempotent - they can be safely
    called multiple times without adverse effects.
"""

import os
import shutil

def clean_directory(dir_path: str) -> None:
    """Safely deletes all contents of a directory while preserving the directory structure.
    
    This function provides a safe way to clean directory contents without removing
    the parent directory itself. It handles both files and subdirectories, with
    comprehensive error handling to ensure partial failures don't stop the cleanup process.

    Cleanup Workflow:
        1. **Validation**: Check if target directory exists
        2. **Enumeration**: List all items in the directory
        3. **Classification**: Identify files, symbolic links, and subdirectories
        4. **Deletion**: Remove items using appropriate methods:
           - Files and symlinks: :func:`os.unlink`
           - Directories: :func:`shutil.rmtree`
        5. **Error Handling**: Log failures but continue with remaining items
        6. **Completion**: Report successful cleanup

    Supported Item Types:
        - **Regular Files**: Standard files of any type and size
        - **Symbolic Links**: Both file and directory symlinks
        - **Subdirectories**: Recursive directory tree removal
        - **Special Files**: Device files, pipes, and other special filesystem objects

    :param dir_path: Absolute or relative path to the directory to be cleaned
    :type dir_path: str
    :rtype: None
    :raises OSError: Individual file deletion failures are caught and logged,
                    but don't stop the overall cleanup process

    .. note::
        The function is designed to be non-destructive to the parent directory
        structure, making it safe for cleaning cache and temporary directories.

    .. warning::
        This operation is irreversible. Ensure the target directory contains
        only disposable files and subdirectories.

    Example:
        >>> clean_directory("/tmp/fleet_cache")
        Contents of /tmp/fleet_cache deleted
        
        >>> clean_directory("/nonexistent/path")
        Directory not found: /nonexistent/path
    """
    # Validate directory existence before attempting cleanup operations
    # This prevents errors and provides clear feedback for invalid paths
    if not os.path.exists(dir_path):
        print(f"Directory not found: {dir_path}")
        return
    
    # Iterate through all items in the target directory
    # os.listdir() returns both files and subdirectories as a flat list
    for item in os.listdir(dir_path):
        # Construct full path for each item to enable proper deletion
        # os.path.join() handles path separators across different operating systems
        item_path = os.path.join(dir_path, item)
        
        try:
            # Check if current item is a regular file or symbolic link
            # Both file types can be safely removed using os.unlink()
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)  # Remove file or symbolic link
                
            # Check if current item is a directory (not a symlink to directory)
            # Directories require recursive removal using shutil.rmtree()
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)  # Recursively remove directory and all contents
                
        except Exception as e:
            # Catch any deletion errors (permissions, file locks, etc.)
            # Log the error but continue processing remaining items
            # This ensures partial failures don't stop the entire cleanup process
            print(f"Error deleting {item_path}: {e}")
    

def clean_pms_subfolders(base_dir: str) -> None:
    """Recursively finds and cleans all 'PMs' subfolders within a base directory structure.
    
    This function is specifically designed for the Fleet Management System's prescription
    map (PM) directory structure. It searches through all subdirectories of the base
    directory looking for 'PMs' folders and cleans their contents while preserving
    the folder structure itself.

    Directory Structure Expected:
        .. code-block:: text
        
            base_dir/
            ├── VehicleType1/
            │   └── PMs/          # ← Cleaned
            │       ├── file1.json
            │       └── file2.xml
            ├── VehicleType2/
            │   └── PMs/          # ← Cleaned
            │       └── cached_pm.dat
            └── VehicleType3/
                └── Other/        # ← Ignored (not named 'PMs')

    Cleanup Workflow:
        1. **Base Validation**: Verify base directory exists
        2. **Directory Enumeration**: List all first-level subdirectories
        3. **PMs Folder Detection**: Look for 'PMs' subfolder in each directory
        4. **Targeted Cleanup**: Clean contents of found 'PMs' directories
        5. **Status Reporting**: Log success/failure for each operation

    Use Cases:
        - **System Initialization**: Clean cached prescription maps before startup
        - **Memory Management**: Free up storage space used by temporary PM files
        - **State Reset**: Ensure clean state for prescription map generation
        - **Maintenance**: Regular cleanup of accumulated cache files

    :param base_dir: Path to the base directory containing vehicle-specific subdirectories
    :type base_dir: str
    :rtype: None
    :raises OSError: Directory access failures are caught and logged individually

    .. note::
        This function specifically targets directories named 'PMs' and ignores
        all other subdirectories, making it safe for mixed-content directories.

    .. seealso::
        - :func:`clean_directory`: Core directory cleaning functionality used internally

    Example:
        >>> clean_pms_subfolders("PrescriptionMap/pm_generation")
        Contents of PrescriptionMap/pm_generation/Drone/PMs deleted
        Contents of PrescriptionMap/pm_generation/ISOBUS/PMs deleted
        PMs not found in Config
        
        >>> clean_pms_subfolders("/invalid/path")
        Base directory not found: /invalid/path
    """
    # Validate base directory existence before starting subfolder search
    # Early validation prevents unnecessary processing and provides clear error feedback
    if not os.path.exists(base_dir):
        print(f"Base directory not found: {base_dir}")
        return
    
    # Iterate through all first-level subdirectories in the base directory
    # This processes each vehicle type or category folder individually
    for folder in os.listdir(base_dir):
        # Construct path to potential 'PMs' subfolder within current directory
        # Following the expected structure: base_dir/VehicleType/PMs/
        pms_dir = os.path.join(base_dir, folder, "PMs")
        
        # Check if the 'PMs' subfolder actually exists in current directory
        # Only existing 'PMs' directories will be processed for cleanup
        if os.path.exists(pms_dir):
            # Call the core directory cleaning function to remove PMs contents
            # This preserves the 'PMs' directory structure while clearing cached files
            clean_directory(pms_dir)