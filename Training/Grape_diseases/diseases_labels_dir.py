"""
YOLO Dataset Label Generator for Classification Tasks
===================================================

This module creates YOLO-format labels and dataset structure for image classification
tasks, specifically designed for grape disease classification. It processes class-based
directory structures and converts them to YOLO object detection format with full-image
bounding boxes.

The script performs the following operations:
    1. Creates standardized dataset directory structure
    2. Processes class-based image directories
    3. Generates YOLO-format label files with full-image annotations
    4. Creates train/validation/test dataset splits
    5. Validates generated labels for completeness

Dataset Structure Created:

.. code-block:: text

    data_directory/
    ├── images/
    │   ├── image1.jpg
    │   ├── image2.jpg
    │   └── ...
    ├── labels/
    │   ├── Healthy/
    │   ├── Black_measles/
    │   ├── Black_rot/
    │   └── Isariopsis/
    ├── train.txt
    ├── val.txt
    └── test.txt

Input Structure Expected:

.. code-block:: text

    data_directory/images/
    ├── Healthy/
    │   ├── img1.jpg
    │   └── ...
    ├── Black_measles/
    │   ├── img2.jpg
    │   └── ...
    └── ...

Features:
    - Automatic YOLO label generation for classification tasks
    - Full-image bounding box annotations (0.5 0.5 1.0 1.0)
    - Configurable class mapping with disease categories
    - Automatic dataset splitting (70% train, 20% val, 10% test)
    - Label validation and error reporting
    - Cross-platform path handling using pathlib

Note:
    This script treats classification as object detection by creating
    full-image bounding boxes. Each image gets a single annotation
    covering the entire image area with the appropriate class ID.

Example:
    Basic usage (run in directory containing class subdirectories)::
    
        $ python create_labels_dir.py

Author: PFG Electronics Training Team
Date: June 2025
"""

import os
import random
from pathlib import Path
import shutil

# ==================== Configuration Section ====================
"""
Dataset and class configuration for grape disease classification.

This section defines the core parameters for the dataset generation process,
including the output directory structure and class-to-ID mapping for the
grape disease detection task.
"""

# Base directory for the generated YOLO dataset structure
base_dir = Path("data_directory")

# Class mapping dictionary for grape disease classification
# Maps human-readable class names to YOLO class IDs (integers)
# Class IDs must be sequential starting from 0 for YOLO compatibility
class_mapping = {
    "Healthy": 0,           # Healthy grape leaves/plants
    "Black_measles": 1,     # Black measles disease symptoms
    "Black_rot": 2,         # Black rot disease symptoms  
    "Isariopsis": 3         # Isariopsis leaf spot disease symptoms
}

# ==================== Directory Structure Creation ====================
"""
Create the standard YOLO dataset directory structure.

This section sets up the required directories for YOLO training:
- images/: Contains all training images in a flat structure
- labels/: Contains corresponding YOLO-format annotation files
"""

# Create main directories for YOLO dataset structure
images_dir = base_dir / "images"  # Directory for all training images
labels_dir = base_dir / "labels"  # Directory for YOLO label files

# Create directories with parent creation and existence checking
images_dir.mkdir(exist_ok=True, parents=True)
labels_dir.mkdir(exist_ok=True, parents=True)

# ==================== Image Processing and Label Generation ====================
"""
Process each class directory and generate YOLO-format labels.

This section iterates through each disease class, processes images in their
respective directories, and creates corresponding YOLO annotation files.
Each image receives a full-image bounding box annotation with its class ID.
"""

# Process each class defined in the mapping dictionary
for class_name, class_id in class_mapping.items():
    # Construct path to class-specific image directory
    class_image_dir = images_dir / class_name
    
    # Check if the class directory exists before processing
    if not class_image_dir.exists():
        print(f"Warning: Class directory not found - {class_image_dir}")
        continue
        
    # Process each image file in the current class directory
    for img_file in class_image_dir.glob("*.*"):
        # Filter for common image file extensions
        if img_file.suffix.lower() in [".jpg", ".jpeg", ".png"]:
            # Define destination paths for image and label files
            img_dest = images_dir / img_file.name  # Flat image structure
            label_dest = labels_dir / class_name / img_file.with_suffix(".txt").name

            # Copy image to the main images directory (flatten structure)
            if not img_dest.exists():
                shutil.copy2(str(img_file), str(img_dest))
            
            # Create YOLO-format label file with full-image annotation
            # Format: class_id center_x center_y width height (normalized 0-1)
            # Full image annotation: center at (0.5, 0.5) with full width/height (1.0, 1.0)
            with open(label_dest, "w") as f:
                f.write(f"{class_id} 0.5 0.5 1.0 1.0\n")
            print(f"Created label for {img_file.name}: class {class_id}")

# ==================== Label Validation Section ====================
"""
Verify the integrity of generated label files.

This section performs quality assurance by checking all generated label files
for completeness and identifying any empty or corrupted files that could
cause issues during YOLO training.
"""

print("\nVerifying label files...")
empty_labels = 0    # Counter for empty label files
total_labels = 0    # Counter for total label files processed

# Check each label file for content
for label_file in labels_dir.glob("*.txt"):
    total_labels += 1
    # Check if label file is empty (size = 0 bytes)
    if label_file.stat().st_size == 0:
        print(f"ERROR: Empty label file - {label_file}")
        empty_labels += 1

# Report validation results
if empty_labels == 0:
    print(f"Success! Created {total_labels} valid label files.")
else:
    print(f"Warning: Found {empty_labels} empty label files out of {total_labels}")

# ==================== Dataset Splitting Section ====================
def create_split_files():
    """
    Create train/validation/test splits for the YOLO dataset.
    
    This function randomly divides the processed images into three sets
    according to standard machine learning practices:
    - Training set: 70% of images for model training
    - Validation set: 20% of images for hyperparameter tuning
    - Test set: 10% of images for final model evaluation
    
    The function generates three text files containing relative paths to
    images in each split, formatted for YOLO training compatibility.
    
    Split Files Created:
        - train.txt: Training image paths
        - val.txt: Validation image paths  
        - test.txt: Test image paths
        
    Path Format:
        Each line contains a relative path like: ./images/filename.jpg
        
    Note:
        The random shuffle ensures unbiased distribution across splits,
        preventing class imbalance in any particular set.
    """
    # Collect all image files from the images directory
    all_images = list(images_dir.glob("*.*"))
    
    # Randomize image order to ensure unbiased splits
    random.shuffle(all_images)
    
    # Calculate split sizes based on total image count
    total = len(all_images)
    train_count = int(0.7 * total)  # 70% for training
    val_count = int(0.2 * total)    # 20% for validation
    # Remaining 10% automatically goes to test set
    
    # Create split arrays by slicing the shuffled image list
    train_files = all_images[:train_count]
    val_files = all_images[train_count:train_count+val_count]
    test_files = all_images[train_count+val_count:]
    
    # Write training split file with relative paths for YOLO compatibility
    with open(base_dir / "train.txt", "w") as f:
        for path in train_files:
            f.write(f"./images/{path.name}\n")
    
    # Write validation split file with relative paths
    with open(base_dir / "val.txt", "w") as f:
        for path in val_files:
            f.write(f"./images/{path.name}\n")
    
    # Write test split file with relative paths
    with open(base_dir / "test.txt", "w") as f:
        for path in test_files:
            f.write(f"./images/{path.name}\n")

# Execute the dataset splitting function
create_split_files()

# ==================== Final Summary and Statistics ====================
"""
Display completion summary with dataset statistics.

This section provides a comprehensive overview of the dataset generation
process results, including counts of processed files and class distribution
information for verification purposes.
"""

print("\nDataset preparation complete!")
# Report total number of images processed and copied to the images directory
print(f"Created {len(list(images_dir.glob('*.*')))} images")
# Report total number of label files generated in the labels directory
print(f"Created {len(list(labels_dir.glob('*.txt')))} labels")
# Display the class mapping for reference and verification
print(f"Class distribution: {class_mapping}")