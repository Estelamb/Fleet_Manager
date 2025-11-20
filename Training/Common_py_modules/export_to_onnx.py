"""
ONNX Model Export Utility
========================

This module provides functionality to export trained YOLO models to ONNX format.
ONNX (Open Neural Network Exchange) is an open format that allows models to be 
transferred between different machine learning frameworks and optimized for deployment.

Example:
    Basic usage of the export utility::
    
        $ python export_to_onnx.py
        
    The script will load a trained YOLO model and export it to ONNX format
    optimized for inference with batch size 1.

Note:
    Before running this script, ensure that:
    - The model file "your_best_model.pt" exists in the current directory
    - The ultralytics package is installed
    - Sufficient disk space is available for the exported model

"""

from ultralytics import YOLO

# Load the trained YOLO model from the PyTorch checkpoint file
model = YOLO("your_best_model.pt")  # Load your trained model

# Export the model to ONNX format with optimized settings for inference
# Parameters:
# - format: "onnx" - specifies the export format as ONNX
# - batch: 1 - sets the batch size to 1 for optimized single-image inference
model.export(format="onnx", batch=1)
