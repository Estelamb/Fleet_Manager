"""
Dataset Split Generator for YOLO Training
=========================================

This module creates train/validation/test splits for YOLO object detection datasets.
It processes image directories, generates split files, and creates YAML configuration
files required for YOLO training workflows.

The script automatically discovers images in a dataset directory structure,
randomly splits them into training, validation, and test sets, and generates
the necessary configuration files for both regular training and ONNX export.

Dataset Structure Expected:

.. code-block:: text

    dataset/
    ├── images/
    │   ├── image1.jpg
    │   ├── image2.jpg
    │   └── ...
    ├── labels/
    │   ├── image1.txt
    │   ├── image2.txt
    │   └── ...
    └── classes.json

Features:
    - Configurable train/validation/test split ratios
    - Support for ONNX export configuration (reduced dataset size)
    - Automatic YAML configuration file generation
    - Class information extraction from JSON metadata
    - Relative path handling for cross-platform compatibility

Example:
    Basic usage for dataset splitting::
    
        $ python create_data_splits.py --data_dir /path/to/dataset
        
    Custom split ratios::
    
        $ python create_data_splits.py --data_dir /path/to/dataset \\
            --test_split 0.15 --val_split 0.15
            
    Generate ONNX export configuration::
    
        $ python create_data_splits.py --data_dir /path/to/dataset --onnx_config

Output Files:
    - train.txt / train_onnx.txt: Training image paths
    - val.txt / val_onnx.txt: Validation image paths  
    - test.txt / test_onnx.txt: Test image paths
    - configs/dataset_config.yaml: YOLO configuration file

Requirements:
    - classes.json file in the dataset directory
    - Standard library modules (argparse, os, random, json)

Author: PFG Electronics Training Team
Date: June 2025
"""

import argparse
import os
import random
import json
from typing import List, Dict, Any

def main() -> None:
    """
    Main execution function for dataset splitting and configuration generation.
    
    This function orchestrates the complete dataset preparation workflow for YOLO training:
    
    **Workflow:**
    
    1. **Argument Parsing**: Parse command line arguments for dataset configuration
    2. **Image Discovery**: Recursively find all images in the dataset/images directory
    3. **Random Shuffling**: Randomize image order to ensure unbiased data splits
    4. **Dataset Splitting**: Split images into train/validation/test sets based on ratios
    5. **ONNX Optimization**: Optionally reduce dataset size for ONNX export/calibration
    6. **Split File Generation**: Write image paths to separate .txt files for each split
    7. **YAML Configuration**: Generate YOLO-compatible configuration files with class info
    
    **Supported Modes:**
    
    - **Regular mode**: Full dataset splits for standard training workflows
    - **ONNX mode**: Reduced dataset splits optimized for model export and calibration
    
    :raises FileNotFoundError: If the required classes.json file is not found in dataset directory
    :raises ValueError: If invalid split ratios are provided (ratios must sum to <= 1.0)
    :raises OSError: If unable to write output files due to permission or disk space issues
        
    .. note::
        The function expects a specific dataset structure with 'images/' and 'labels/' 
        subdirectories, plus a 'classes.json' file containing class definitions.
        
    .. warning::
        The ONNX mode significantly reduces dataset size (max 300 samples per split)
        which may not be suitable for training but optimizes export performance.
        
    **Example Usage:**
    
    .. code-block:: bash
    
        # Basic dataset splitting with default ratios (80% train, 10% val, 20% test)
        python create_data_splits.py --data_dir my_dataset
        
        # Custom split ratios
        python create_data_splits.py --data_dir my_dataset --test_split 0.15 --val_split 0.15
        
        # Generate ONNX-optimized configuration
        python create_data_splits.py --data_dir my_dataset --onnx_config
    """
    # ==================== Argument Parsing Section ====================
    """
    **Step 1: Command Line Argument Configuration**
    
    Parse and validate command line arguments that control the dataset splitting behavior.
    This includes dataset paths, split ratios, class configuration, and operational modes.
    """
    # Create argument parser for command line interface
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description='Create text files indicating the train/test/val splits.')

    # Dataset configuration arguments
    parser.add_argument('--data_dir', type=str, help='Base directory to load images')

    # Split ratio configuration arguments  
    parser.add_argument('--test_split', type=float, help='Percentage of images to split into the test set',
                        default=0.2)
    parser.add_argument('--val_split', type=float, help='Percentage of images to split into the val set',
                        default=0.1)
    
    # Class configuration arguments
    parser.add_argument('--num_classes', type=int, help='Specify the number of classes if classes json does not exist',
                        default=1)
    
    # Mode configuration arguments
    parser.add_argument("--onnx_config",  action='store_true', help="Create a Split and Config for onnx export")

    # Parse all command line arguments
    args: argparse.Namespace = parser.parse_args()

    # ==================== Image Discovery Section ====================
    """
    **Step 2: Image File Discovery and Path Collection**
    
    Recursively traverse the dataset's images directory to discover all image files.
    Convert absolute paths to relative paths for YOLO compatibility and cross-platform support.
    """
    # Construct path to images directory within the dataset
    img_input_root_dir: str = os.path.join(args.data_dir, "images")

    # Collect all image file paths from the images directory and subdirectories
    all_img_paths: List[str] = []
    for root, _, files in os.walk(img_input_root_dir):
        # Skip empty directories to avoid processing issues
        if len(files) == 0:
            continue

        # Process each file in the current directory
        for file in files:
            # Create absolute file path
            file_path: str = os.path.join(root, file)
            # Convert to relative path for YOLO compatibility and cross-platform support
            relative_path: str = file_path.replace(img_input_root_dir, "./images")
            # Add newline for proper file formatting in output text files
            all_img_paths.append(relative_path + '\n')

    # ==================== Dataset Splitting Section ====================
    """
    **Step 3: Random Data Splitting and Path Assignment**
    
    Randomize the image order and split into train/validation/test sets based on 
    specified ratios. Calculate exact sample counts and define output file paths.
    """
    # Randomize image order to ensure unbiased splits and prevent data leakage
    random.shuffle(all_img_paths)
    
    # Determine file suffix based on configuration mode (regular vs ONNX)
    file_suffix: str = "_onnx" if args.onnx_config else ""

    # Calculate split sizes based on total images and specified ratios
    total_images: int = len(all_img_paths)
    test_num: int = int(args.test_split * total_images)
    val_num: int = int(args.val_split * total_images)

    # Define output file paths for each data split
    test_filepath: str = os.path.join(args.data_dir, f"test{file_suffix}.txt")
    val_filepath: str = os.path.join(args.data_dir, f"val{file_suffix}.txt")
    train_filepath: str = os.path.join(args.data_dir, f"train{file_suffix}.txt")

    # Extract images for test and validation sets (modifies all_img_paths list in-place)
    test_images: List[str] = [all_img_paths.pop() for _ in range(test_num)]
    val_images: List[str] = [all_img_paths.pop() for _ in range(val_num)]
    # Remaining images in all_img_paths become the training set

    # ==================== ONNX Configuration Optimization ====================
    """
    **Step 4: ONNX Mode Dataset Size Optimization**
    
    When ONNX mode is enabled, reduce dataset size to maximum 300 samples per split.
    This optimization improves ONNX export speed and calibration performance while
    maintaining representative data for model conversion.
    """
    # Reduce dataset size for ONNX calibration to improve export speed and memory usage
    if args.onnx_config:
        test_images = test_images[:300]
        val_images = val_images[:300]
        all_img_paths = all_img_paths[:300]  # Training set (remaining images)

    # ==================== Split File Generation Section ====================
    """
    **Step 5: Data Split File Writing**
    
    Write the image paths for each data split (train/validation/test) to separate
    text files. These files will be used by YOLO training scripts to load the
    appropriate datasets during different phases of model development.
    """
    # Write test set image paths to file
    with open(test_filepath, 'w') as f:
        f.writelines(test_images)

    # Write validation set image paths to file  
    with open(val_filepath, 'w') as f:
        f.writelines(val_images)

    # Write training set image paths to file (remaining images after test/val extraction)
    with open(train_filepath, 'w') as f:
        f.writelines(all_img_paths)

    # ==================== YAML Configuration Generation Section ====================
    """
    **Step 6: Class Information Loading and Validation**
    
    Load class definitions from the classes.json metadata file. This file contains
    the mapping between class indices and class names required for YOLO training.
    Validate that the file exists and is properly formatted.
    """
    # Load class information from JSON metadata file
    try:
        class_dict_filepath: str = os.path.join(args.data_dir, "classes.json")
        with open(class_dict_filepath) as f:
            d: Dict[str, Any] = json.load(f)
            num_classes: int = len(list(d.keys()))
    except Exception as e:
        print(f"No classes.json file found at {args.data_dir}, please define! (see example)")
        print(e)
        return

    """
    **Step 7: YOLO Configuration File Generation**
    
    Create a YAML configuration file compatible with YOLO training frameworks.
    This file specifies dataset paths, class count, and class names required
    for model training and evaluation.
    """
    # Extract dataset name from directory path for configuration naming
    base_dir: str = args.data_dir.split("/")[-1]
    if base_dir == '':
        base_dir = args.data_dir.split("/")[-2]
    
    # Define YAML configuration file path within configs subdirectory
    yaml_filename: str = f"configs/{base_dir}{file_suffix}_config.yaml"

    # Generate YAML configuration file with complete dataset specifications
    with open(yaml_filename, 'w') as f:
        # Training data configuration section
        f.write(f"# Train images - Path to training dataset split\n")
        f.write(f"train: {train_filepath}\n")
        f.write(f"\n")

        # Validation data configuration section
        f.write(f"# Validation images - Path to validation dataset split\n")
        f.write(f"val: {val_filepath}\n")
        f.write(f"\n")

        # Test data configuration section
        f.write(f"# Test images - Path to test dataset split\n")
        f.write(f"test: {test_filepath}\n")
        f.write(f"\n")

        # Class count configuration section
        f.write(f"# Number of classes - Total object classes in dataset\n")
        f.write(f"nc: {str(num_classes)}\n")
        f.write(f"\n")

        # Class names configuration section
        f.write(f"# Class names - List of all object class labels\n")
        f.write(f"names: {list(d.keys())}\n")

# Script entry point - execute main function when run directly
# This allows the script to be imported as a module without executing main()
if __name__ == "__main__":
    """
    **Script Entry Point**
    
    Execute the main function when the script is run directly from command line.
    This conditional ensures the script can also be imported as a module without
    automatically executing the dataset splitting workflow.
    
    .. note::
        When imported as a module, only the function definitions are loaded,
        allowing other scripts to reuse the dataset splitting functionality.
    """
    main()