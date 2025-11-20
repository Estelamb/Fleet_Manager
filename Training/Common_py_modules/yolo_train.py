"""
YOLO Training and Export Pipeline
================================

This module provides a comprehensive training and export pipeline for YOLO (You Only Look Once)
object detection models using the Ultralytics framework. It supports training from scratch,
resuming training, model validation, and exporting to various formats including ONNX.

The script offers flexible configuration options for training parameters, device selection,
model initialization, and export settings. It's designed to handle the complete workflow
from training to deployment-ready model export.

Features:
    - Train YOLO models with custom datasets
    - Resume interrupted training sessions
    - Validate trained models
    - Export models to multiple formats (ONNX, IMX, etc.)
    - Support for quantized exports (INT8)
    - Flexible image size configuration
    - GPU memory management

Example:
    Basic training workflow::
    
        $ python yolo_train.py --config dataset.yaml --epochs 100 --name my_model
        
    Resume training::
    
        $ python yolo_train.py --config dataset.yaml --resume_training --name my_model
        
    Export only::
    
        $ python yolo_train.py --export_only --init_model best.pt --export_format onnx
        
    Validation only::
    
        $ python yolo_train.py --val_model --init_model best.pt

Requirements:
    - ultralytics: YOLO implementation and training framework
    - PyTorch: Deep learning framework
    - CUDA (optional): For GPU acceleration

Author: PFG Electronics Training Team
Date: June 2025
"""

from ultralytics import YOLO
import argparse

def parse_arguments():
    """
    Parse command line arguments for the YOLO training and export pipeline.
    
    This function configures the argument parser with all available options for
    training, validation, and export operations. It provides sensible defaults
    while allowing full customization of the training process.
    
    Returns:
        argparse.Namespace: Parsed command line arguments containing:
            - config (str): Path to dataset configuration YAML file
            - init_model (str): Path to pre-trained model weights file
            - name (str): Name for the training run (used for save directory)
            - epochs (int): Number of training epochs
            - device (int): GPU device index for training
            - gpu_percent (float): Fraction of GPU memory to use
            - export_format (str): Format for model export (onnx, imx, etc.)
            - export_config (str): Dataset config file for export operations
            - resume_training (bool): Whether to resume previous training
            - export_only (bool): Skip training and only export the model
            - int8_weights (bool): Export model with INT8 quantization
            - image_size (str): Input image dimensions as "WIDTHxHEIGHT"
            - val_model (bool): Perform validation only
            
    Example:
        >>> args = parse_arguments()
        >>> print(f"Training for {args.epochs} epochs")
        Training for 20 epochs
        
    Note:
        The image_size parameter uses the format "640x640" where the first
        number is height and the second is width, following YOLO conventions.
    """
    parser = argparse.ArgumentParser(description="YOLO trainer")
    
    # Dataset and model configuration
    parser.add_argument("--config", type=str, default="config.yaml", help="The dataset config file")
    parser.add_argument("--init_model", type=str, default="yolo11n.pt", help="The pre-trained model weights")

    # Training parameters
    parser.add_argument("--name", type=str, default="yolo", help="Save dir")
    parser.add_argument("--epochs", type=int, default=20, help="Number of training epochs")
    parser.add_argument("--device", type=int, default=0, help="Device training index")
    parser.add_argument("--gpu_percent", type=float, default=0.9, help="How much of the GPU RAM to use")

    # Export configuration
    parser.add_argument("--export_format", type=str, default="onnx", help="format to export the model as, eg onnx, imx")
    parser.add_argument("--export_config", type=str, default=None, help="The dataset config file for export")
    
    # Operation mode flags
    parser.add_argument("--resume_training",  action='store_true', help="Resume training of a model")
    parser.add_argument("--export_only",  action='store_true', help="Just export the weights as onnx")
    parser.add_argument("--int8_weights",  action='store_true', help="Export the weights as int8")
    parser.add_argument("--val_model",  action='store_true', help="Validate the model only")
    
    # Model configuration
    parser.add_argument("--image_size", type=str, default="640x640",
                        help="Image size as width height (default: 640x640)")

    return parser.parse_args()


def main():
    """
    Main execution function for the YOLO training and export pipeline.
    
    This function orchestrates the complete workflow based on command line arguments:
    1. Parses command line arguments
    2. Loads the specified YOLO model
    3. Configures image dimensions
    4. Executes the requested operation (train/validate/export)
    5. Exports the model if specified
    
    The function supports three main operation modes:
    - Training: Train a new model or resume training
    - Validation: Validate an existing model's performance
    - Export: Convert trained models to deployment formats
    
    The workflow is designed to be flexible, allowing combinations of operations
    such as training followed by automatic export, or standalone operations.
    
    Note:
        The function handles project directory creation automatically and
        manages GPU memory allocation based on the specified percentage.
        
    Raises:
        SystemExit: If model loading fails or invalid arguments are provided
        
    Example:
        The main function is executed when the script runs directly::
        
            $ python yolo_train.py --config my_dataset.yaml --epochs 50
    """
    # Parse all command line arguments for configuration
    args = parse_arguments()

    # Load the specified YOLO model (pre-trained or custom)
    # This supports various YOLO versions (YOLOv8, YOLOv11, etc.)
    model = YOLO(args.init_model)

    # Parse image dimensions from string format (e.g., "640x640" -> [640, 640])
    # Note: First value is height, second is width in YOLO convention
    image_h, image_w = map(int, args.image_size.split('x'))
    image_size = [image_h, image_w]
    print(image_size)  # Display parsed image dimensions for verification

    # Training workflow - execute unless export-only or validation-only mode
    if not args.export_only and not args.val_model:
        # Configure project directory based on training mode
        if args.resume_training:
            # Use existing project directory when resuming training
            project = args.name
        else:
            # Create new project directory for fresh training
            project = None

        # Execute training with comprehensive parameter configuration
        # Key parameters:
        # - data: dataset configuration file
        # - epochs: number of training iterations
        # - imgsz: input image size for training
        # - device: GPU device index
        # - batch: GPU memory utilization factor
        # - cache: disable image caching to save memory
        _ = model.train(data=args.config, epochs=args.epochs, imgsz=image_size, save=True,
                              device=args.device, name=args.name, batch=args.gpu_percent, resume=args.resume_training,
                              cache=False, project=project)
                              
    # Validation workflow - evaluate model performance on validation set
    elif args.val_model:
        # Perform validation using previously configured dataset and settings
        # The model remembers dataset configuration from training or loading
        _ = model.val(name=args.name, project=args.name)

    # Model export workflow - convert trained model to deployment format
    if args.export_format:
        # Export model with optimized settings for deployment
        # Parameters:
        # - format: target export format (onnx, imx, etc.)
        # - int8: enable INT8 quantization for smaller model size
        # - imgsz: input image size for exported model
        # - device: GPU device for export process
        # - batch: batch size for export optimization
        # - nms: include Non-Maximum Suppression in exported model
        # - data: dataset config for calibration during quantization
        # - opset: ONNX opset version for compatibility
        model.export(format=args.export_format, int8=args.int8_weights, imgsz=image_size, device=0, batch=16, nms=True,
                     data=args.export_config, opset=11, name=args.name, project=args.name)  # exports with PTQ quantization by default

# Script entry point - execute main function when run directly
# This allows the script to be imported as a module without executing main()
if __name__ == "__main__":
    main()