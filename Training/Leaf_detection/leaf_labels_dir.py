"""
CSV to YOLO Label Converter for Leaf Detection
==============================================

This module converts bounding box annotations from CSV format to YOLO format
for leaf detection tasks. It processes a CSV file containing image IDs and
bounding box coordinates, then generates corresponding YOLO-format label files
for object detection training.

The script handles the conversion from absolute pixel coordinates to normalized
YOLO format coordinates and creates the proper directory structure for YOLO
training workflows.

CSV Format Expected:
    The CSV file should contain the following columns:
    - image_id: Filename of the image (e.g., "image001.jpg")
    - bbox: Bounding box coordinates as string "[x, y, w, h]"
    
    Where:
    - x, y: Top-left corner coordinates in pixels
    - w, h: Width and height in pixels

YOLO Format Generated:
    Each label file contains one line per object:
    class_id x_center y_center width height
    
    Where all coordinates are normalized (0.0 to 1.0):
    - x_center, y_center: Center of bounding box relative to image size
    - width, height: Bounding box dimensions relative to image size

Directory Structure:

.. code-block:: text

    base_directory/
    ├── train.csv             # Input CSV with annotations
    ├── images/Leaf/          # Source images directory
    └── labels/Leaf/          # Generated YOLO labels (created)

Features:
    - Automatic YOLO format conversion from CSV annotations
    - Normalized coordinate calculation for scale independence
    - Image dimension extraction for accurate normalization
    - Missing annotation detection and warning system
    - Automatic directory creation for output labels

Example:
    CSV Input:
        image_id,bbox
        leaf001.jpg,"[100, 50, 200, 150]"
        
    YOLO Output (leaf001.txt):
        0 0.312500 0.250000 0.312500 0.375000

Note:
    All detected objects are assigned class_id = 0 (single class detection).
    Modify the class assignment logic for multi-class scenarios.

Requirements:
    - pandas: CSV file processing
    - PIL (Pillow): Image dimension extraction
    - ast: Safe evaluation of bbox string literals

Author: PFG Electronics Training Team
Date: June 2025
"""

import os
import pandas as pd
import ast
from PIL import Image

# ==================== Path Configuration Section ====================
"""
Define file paths and directory structure for the CSV to YOLO conversion process.

This section configures all necessary paths for input data, source images,
and output label files. The paths are structured to match standard YOLO
dataset organization requirements.
"""

# Base directory containing the leaf detection dataset
base_dir = "C:/PFG_Electronica/Training/Leaf_detection/data_directory"
if not os.path.exists(base_dir):
    base_dir = "."
# Path to the CSV file containing image IDs and bounding box annotations
csv_path = os.path.join(base_dir, "train.csv")
if not os.path.exists(csv_path):
    csv_path = "."

# Source directory containing the original leaf images
images_dir = os.path.join(base_dir, "images", "Leaf")
if not os.path.exists(images_dir):
    images_dir = "."
    
# Output directory for generated YOLO-format label files
labels_dir = os.path.join(base_dir, "labels", "Leaf")
if not os.path.exists(labels_dir):
    labels_dir = "."

# Create the output labels directory if it doesn't exist
# This ensures the directory structure is ready for label file generation
os.makedirs(labels_dir, exist_ok=True)

# ==================== CSV Data Loading and Processing Section ====================
"""
Load and preprocess the CSV annotation data.

This section handles the loading of bounding box annotations from the CSV file
and organizes them by image ID for efficient processing during label generation.
"""

# Load the CSV file containing image annotations
# Expected columns: 'image_id' and 'bbox'
df = pd.read_csv(csv_path)

# Clean column names by removing any leading/trailing whitespace
# This prevents issues with column access due to formatting inconsistencies
df.columns = df.columns.str.strip()

# Group bounding boxes by image ID for efficient lookup
# Creates a dictionary where keys are image filenames and values are lists of bbox strings
# Format: {'image001.jpg': ['[x1,y1,w1,h1]', '[x2,y2,w2,h2]'], ...}
grouped = df.groupby('image_id')['bbox'].apply(list).to_dict()

# ==================== YOLO Label Generation Section ====================
"""
Convert CSV bounding box data to YOLO format label files.

This section processes each image in the dataset, extracts its dimensions,
converts bounding box coordinates from absolute pixels to normalized YOLO format,
and generates corresponding label files for YOLO training.

YOLO Format Conversion:
    CSV format: [x, y, w, h] (absolute pixels, top-left corner)
    YOLO format: class_id x_center y_center width height (normalized 0-1)
"""

# Process each image file in the images directory
for image_file in os.listdir(images_dir):
    # Filter for JPEG image files (modify extensions as needed)
    if image_file.endswith(".jpg"):
        # Construct full paths for image and corresponding label file
        image_path = os.path.join(images_dir, image_file)
        label_path = os.path.join(labels_dir, os.path.splitext(image_file)[0] + ".txt")

        # Check if bounding box annotations exist for this image
        if image_file in grouped:
            # Extract image dimensions for coordinate normalization
            # This is crucial for converting absolute pixel coordinates to normalized values
            with Image.open(image_path) as img:
                width, height = img.size

            # Create YOLO label file with converted annotations
            with open(label_path, "w") as f:
                # Process each bounding box annotation for the current image
                for bbox_str in grouped[image_file]:
                    # Parse bounding box coordinates from string format
                    # Expected format: "[x, y, w, h]" where x,y is top-left corner
                    x, y, w, h = ast.literal_eval(bbox_str)

                    # Convert from top-left corner format to center-based YOLO format
                    # Calculate center coordinates from top-left corner and dimensions
                    x_center = (x + w / 2) / width    # Normalized center X coordinate
                    y_center = (y + h / 2) / height   # Normalized center Y coordinate
                    w_norm = w / width                # Normalized width
                    h_norm = h / height               # Normalized height

                    # Write YOLO format annotation to label file
                    # Format: class_id x_center y_center width height
                    # Note: Assuming class_id = 0 for single-class leaf detection
                    f.write(f"0 {x_center:.6f} {y_center:.6f} {w_norm:.6f} {h_norm:.6f}\n")
        else:
            # Warn about images without corresponding annotations
            # This helps identify potential data inconsistencies
            print(f"[Warning] No label found for {image_file}")
