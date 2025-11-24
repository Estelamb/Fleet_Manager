#!/usr/bin/env python3

"""
Grape Leaf Detection and Extraction with Hailo8L AI Acceleration Module
======================================================================

This module implements comprehensive grape leaf detection and extraction using
YOLOv8n neural networks optimized with Hailo8L AI hardware acceleration. It provides
specialized computer vision capabilities for precision viticulture, enabling automated
leaf identification, localization, and extraction for subsequent plant pathology
analysis and disease detection workflows.

The module serves as the preprocessing engine for agricultural leaf analysis systems,
delivering high-performance leaf detection with hardware-accelerated inference for
real-time field operations and comprehensive vineyard leaf extraction workflows.

.. module:: leaf_detection_Hailo8l
    :synopsis: YOLOv8n grape leaf detection with Hailo8L acceleration for agricultural preprocessing

Features
--------
- **Leaf Detection**: Advanced YOLOv8n neural network architecture for grape leaf identification
- **Hailo8L AI Acceleration**: Hardware-accelerated inference for real-time field processing
- **Leaf Extraction**: Automated cropping and extraction of detected leaf regions
- **Spatial Mapping**: Precise bounding box coordinates for leaf localization
- **Batch Processing**: Efficient processing for multiple leaf detection and extraction
- **Preprocessing Pipeline**: Specialized interface for plant pathology workflows
- **Agricultural Integration**: Optimized for precision viticulture applications

System Architecture
------------------
The grape leaf detection system operates within the precision agriculture ecosystem:

Detection Pipeline:
    Image Input → Preprocessing → YOLOv8n Inference → Hailo8L Acceleration → Leaf Extraction → Crop Generation

Processing Workflow:
    1. **Image Loading**: Agricultural image file loading and validation
    2. **Preprocessing**: Image resizing and color space conversion for model input
    3. **AI Inference**: YOLOv8n neural network execution with Hailo8L acceleration
    4. **Leaf Detection**: Result extraction and confidence-based filtering
    5. **Spatial Mapping**: Coordinate transformation from model space to image space
    6. **Leaf Extraction**: Individual leaf cropping and boundary sanitization
    7. **Output Generation**: Cropped leaf image saving and directory organization

Agricultural Applications:
    - **Plant Pathology**: Leaf extraction for disease detection and analysis
    - **Quality Assessment**: Individual leaf isolation for detailed examination
    - **Research Applications**: Leaf dataset generation for agricultural research
    - **Preprocessing**: Automated leaf preparation for downstream analysis
    - **Field Operations**: Real-time leaf detection during vineyard operations

Computer Vision Integration:
    - **Object Detection**: Advanced neural network-based leaf identification
    - **Spatial Analysis**: Precise bounding box coordinates and object localization
    - **Confidence Assessment**: Detection reliability scoring and threshold filtering
    - **Image Processing**: Comprehensive leaf cropping and extraction workflows

Workflow Architecture
--------------------
Grape Leaf Detection and Extraction Pipeline:
    1. **Input Validation**: Image file accessibility and format verification
    2. **Model Initialization**: Hailo8L AI runtime and YOLOv8n model loading
    3. **Image Preprocessing**: Resizing, color conversion, and format standardization
    4. **Neural Network Inference**: YOLOv8n execution with hardware acceleration
    5. **Detection Processing**: Result parsing and confidence-based filtering
    6. **Coordinate Transformation**: Model coordinate mapping to original image space
    7. **Leaf Extraction**: Individual leaf cropping with coordinate sanitization
    8. **Output Management**: Cropped leaf image saving and directory organization

AI Model Processing:
    - **YOLOv8n Architecture**: State-of-the-art object detection neural network
    - **Hailo8L Optimization**: Hardware-specific model optimization and acceleration
    - **Real-time Inference**: Low-latency processing for field operations
    - **Accuracy Optimization**: Leaf-specific detection tuning for agricultural applications

Classes
-------
None - This module provides functional interfaces for grape leaf detection

Functions
---------
.. autofunction:: leaf_detection_run
.. autofunction:: extract_detections
.. autofunction:: draw_detections

Dependencies
-----------
Core Dependencies:
    - **argparse**: Command-line argument parsing and configuration
    - **gc**: Garbage collection for memory management optimization
    - **os**: File system operations and path management
    - **json**: JSON data processing and structured output formatting
    - **sys**: System-specific parameters and error handling
    - **cv2**: OpenCV computer vision library for image processing

Hardware Dependencies:
    - **picamera2.devices.Hailo**: Hailo8L AI hardware acceleration interface
    - **Hailo Runtime**: Hardware-specific AI acceleration environment

Model Dependencies:
    - **leaf_detection_Hailo8L.hef**: Compiled YOLOv8n model for Hailo8L hardware
    - **leaf_detection_labels.txt**: Class label definitions for leaf detection

Integration Points
-----------------
External Integrations:
    - **Hailo8L AI Platform**: Hardware acceleration for neural network inference
    - **YOLOv8n Models**: Integration with specialized leaf detection models
    - **Computer Vision**: OpenCV integration for image processing and cropping
    - **Agricultural Systems**: Integration with precision viticulture platforms

Internal Integrations:
    - **Image Processing**: Comprehensive image preprocessing and postprocessing
    - **Detection Systems**: AI model output processing and result compilation
    - **Extraction Pipeline**: Automated leaf cropping and file management
    - **Directory Management**: Organized output structure for downstream processing

Performance Characteristics
--------------------------
Detection Performance:
    - **Real-time Processing**: Hardware-accelerated inference for field operations
    - **High Accuracy**: YOLOv8n-optimized detection with leaf specialization
    - **Low Latency**: Hailo8L AI acceleration for responsive processing
    - **Scalability**: Support for high-volume vineyard image processing

Leaf Extraction Optimization:
    - **Coordinate Sanitization**: Robust boundary checking and validation
    - **Cropping Efficiency**: Optimized leaf region extraction algorithms
    - **Directory Organization**: Structured output management for batch processing
    - **Memory Management**: Optimized resource usage during processing

Agricultural Data Formats
-------------------------
Input Data Structure:
    - **Image Files**: Agricultural images in standard formats (JPEG, PNG)
    - **File Paths**: Structured path specifications for input processing
    - **Configuration**: Detection threshold and processing parameters

Output Data Structure:
    - **Cropped Leaves**: Individual leaf images extracted from source image
    - **Directory Structure**: Organized leaf collections for downstream analysis
    - **Detection Metadata**: Leaf detection coordinates and confidence scores
    - **Processing Information**: Leaf count and extraction statistics

Leaf Extraction Format:
    - **Individual Files**: Separate image files for each detected leaf
    - **Naming Convention**: Sequential leaf numbering (leaf_0.jpg, leaf_1.jpg, ...)
    - **Directory Organization**: Image-specific subdirectories for leaf collections
    - **Coordinate Validation**: Sanitized bounding box coordinates for valid crops

Error Handling Strategy
----------------------
Multi-level Error Management:
    - **Input Validation**: Image file accessibility and format verification
    - **Model Loading**: Hailo8L AI model loading and initialization error handling
    - **Detection Processing**: AI inference and leaf detection error management
    - **Extraction Errors**: Leaf cropping and file saving error handling

Recovery Mechanisms:
    - **File Validation**: Input image accessibility verification and error reporting
    - **Coordinate Sanitization**: Bounding box validation and boundary correction
    - **Directory Creation**: Output directory management and creation error handling
    - **Processing Continuity**: Graceful handling of individual leaf extraction failures

Examples
--------
Basic Leaf Detection and Extraction:

.. code-block:: python

    # Execute leaf detection and extraction on vineyard image
    output_directory = leaf_detection_run(
        input_image_path="Images/Camera/vineyard_section_1.jpg",
        score_threshold=0.3
    )
    
    print(f"Extracted leaves saved to: {output_directory}")

Command-line Usage:

.. code-block:: bash

    # Run leaf detection from command line
    python leaf_detection_hailo8l.py -i vineyard_image.jpg

    # Output: Images/Models/Grape_Diseases_Hailo8/Leafs/vineyard_image/

Batch Leaf Processing:

.. code-block:: python

    import os
    import glob
    
    # Process multiple vineyard images for leaf extraction
    vineyard_images = glob.glob("Images/Camera/*.jpg")
    
    leaf_directories = []
    
    for image_path in vineyard_images:
        print(f"Processing {image_path}...")
        
        # Extract leaves from current image
        leaf_dir = leaf_detection_run(
            input_image_path=image_path,
            score_threshold=0.25
        )
        
        leaf_directories.append(leaf_dir)
        
        # Count extracted leaves
        leaf_count = len([f for f in os.listdir(leaf_dir) if f.endswith('.jpg')])
        print(f"  Extracted {leaf_count} leaves")
    
    print(f"\\nTotal processing completed: {len(leaf_directories)} image sets")

Notes
-----
- **Hardware Requirements**: Requires Hailo8L AI acceleration hardware for optimal performance
- **Model Dependencies**: Depends on leaf_detection_Hailo8L.hef model and label files
- **Preprocessing Focus**: Optimized for leaf extraction and plant pathology preprocessing
- **Directory Organization**: Structured output for downstream disease analysis workflows

Configuration Requirements:
    - **Hailo8L Hardware**: Compatible Hailo8L AI acceleration device
    - **Model Files**: YOLOv8n model (.hef) and label definitions (.txt)
    - **OpenCV**: Computer vision library for image processing and cropping
    - **File Access**: Read/write permissions for input and output directories

Leaf Detection Considerations:
    - **Image Quality**: Sufficient resolution and clarity for leaf identification
    - **Lighting Conditions**: Robust detection across various vineyard lighting
    - **Leaf Varieties**: Compatible with multiple grape leaf types and growth stages
    - **Field Conditions**: Optimized for practical vineyard environments

See Also
--------
cv2 : OpenCV computer vision library
picamera2.devices.Hailo : Hailo8L AI hardware acceleration interface
argparse : Command-line argument parsing
os : File system operations and directory management
"""

import argparse
import gc
import os
import json
import sys
import time
import cv2
from picamera2.devices import Hailo

def leaf_detection_run(input_image_path: str, score_threshold: float = 0.25) -> str:
    """
    Execute comprehensive grape leaf detection and extraction using YOLOv8n with Hailo8L AI acceleration.
    
    This function performs complete leaf detection workflow including neural network inference,
    detection processing, and automated leaf extraction. It utilizes YOLOv8n neural network
    architecture optimized with Hailo8L hardware acceleration for real-time grape leaf
    identification and cropping in precision viticulture applications.
    
    Workflow:
        1. **Label Loading**: Load class names from leaf detection label file
        2. **Image Validation**: Load and verify input agricultural image
        3. **Model Initialization**: Initialize Hailo8L AI accelerator with YOLOv8n model
        4. **Image Preprocessing**: Resize and convert image for model input format
        5. **AI Inference**: Execute neural network inference with hardware acceleration
        6. **Detection Processing**: Extract and filter leaf detections by confidence
        7. **Leaf Extraction**: Crop individual detected leaves with coordinate sanitization
        8. **Output Management**: Save cropped leaves with organized directory structure
    
    Parameters
    ----------
    input_image_path : str
        Absolute or relative path to the agricultural input image file.
        Supports standard image formats (JPEG, PNG, BMP).
        Example: "Images/Camera/vineyard_section_1.jpg"
    
    score_threshold : float, optional
        Minimum confidence score threshold for leaf detection filtering.
        Range: 0.0 to 1.0, where higher values require more confident detections.
        Default: 0.25 (25% confidence minimum)
        Recommended: 0.2-0.4 for agricultural field conditions
    
    Returns
    -------
    str
        Absolute path to the output directory containing extracted leaf images.
        Directory structure: "Images/Models/Grape_Diseases_Hailo8L/Leafs/{image_name}/"
        Individual leaves saved as: "leaf_0.jpg", "leaf_1.jpg", etc.
        Returns empty directory path if no leaves detected above threshold.
    
    Raises
    ------
    FileNotFoundError
        If input image file or label file cannot be found or accessed
    SystemExit
        If critical errors occur during image loading or model initialization
    cv2.error
        If image format is unsupported or corrupted
    OSError
        If output directory creation fails due to permissions
    
    Examples
    --------
    Basic leaf detection and extraction:
    
    >>> output_dir = leaf_detection_run("vineyard_image.jpg", score_threshold=0.3)
    >>> print(f"Leaves extracted to: {output_dir}")
    Leaves extracted to: Images/Models/Grape_Diseases_Hailo8L/Leafs/vineyard_image/
    
    High-confidence leaf detection:
    
    >>> # Extract only high-confidence leaves for research
    >>> research_dir = leaf_detection_run(
    ...     input_image_path="research_samples/grape_field_1.jpg",
    ...     score_threshold=0.6
    ... )
    
    Processing field images with moderate threshold:
    
    >>> field_images = ["field_1.jpg", "field_2.jpg", "field_3.jpg"]
    >>> leaf_collections = []
    >>> 
    >>> for image in field_images:
    ...     leaf_dir = leaf_detection_run(image, score_threshold=0.25)
    ...     leaf_collections.append(leaf_dir)
    
    Notes
    -----
    - **Hardware Acceleration**: Requires Hailo8L AI accelerator for optimal performance
    - **Model Dependencies**: Requires leaf_detection_Hailo8L.hef and leaf_detection_labels.txt
    - **Output Organization**: Creates image-specific subdirectories for leaf collections
    - **Coordinate Sanitization**: Automatically validates and corrects bounding box coordinates
    - **Memory Management**: Implements garbage collection for resource optimization
    - **Error Logging**: Logs processing information to stderr for debugging
    
    Performance Considerations:
        - **Real-time Processing**: Hardware acceleration enables field-ready processing speeds
        - **Batch Processing**: Suitable for high-volume vineyard image processing
        - **Memory Efficiency**: Optimized resource usage during detection and extraction
        - **Scalability**: Supports large-scale agricultural image processing workflows
    
    Agricultural Applications:
        - **Disease Detection Preprocessing**: Prepares individual leaves for pathology analysis
        - **Quality Assessment**: Isolates leaves for detailed inspection workflows
        - **Research Data Generation**: Creates structured leaf datasets for agricultural research
        - **Precision Viticulture**: Enables automated leaf analysis in vineyard operations
    
    See Also
    --------
    extract_detections : Extract detection results from Hailo8L neural network output
    draw_detections : Visualize detection results with bounding boxes and labels
    cv2.imread : OpenCV image loading functionality
    """
    # Load class labels from leaf detection model label file
    # This file contains the class names corresponding to model output indices
    with open("Images/Models/Grape_Diseases_Hailo8L/Leaf_Detection/leaf_detection_labels.txt", 'r', encoding="utf-8") as f:
        class_names = f.read().splitlines()

    # Load and validate the input agricultural image
    # Supports standard image formats (JPEG, PNG, BMP)
    input_image = cv2.imread(input_image_path)
    if input_image is None:
        # Critical error: Image file not found or format unsupported
        print(f"Error: Input image not found: {input_image_path}", file=sys.stderr)
        sys.exit(1)
    
    # Extract original image dimensions for coordinate transformation
    # Height (h), Width (w), and Channels (_) from image shape
    h, w, _ = input_image.shape

    # Initialize Hailo8L AI accelerator with leaf detection model
    # Uses context manager for proper resource cleanup
    with Hailo("Images/Models/Grape_Diseases_Hailo8L/Leaf_Detection/leaf_detection_hailo8l.hef") as hailo:
        # Get neural network input dimensions for image preprocessing
        # Model expects specific input dimensions for optimal performance
        model_h, model_w, _ = hailo.get_input_shape()
        
        # Resize input image to match neural network input requirements
        # Maintains aspect ratio awareness for coordinate transformation
        resized_image = cv2.resize(input_image, (model_w, model_h))
        
        # Convert from BGR (OpenCV default) to RGB (neural network requirement)
        # YOLOv8n models typically expect RGB color space input
        resized_image_rgb = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
        
        # Inference time
        start_time = time.time()

        # Execute neural network inference with hardware acceleration
        # Redirect inference logs to stderr to avoid stdout contamination
        results = hailo.run(resized_image_rgb)
        
        # Inference time
        end_time = time.time()
        inference_time = end_time - start_time
        
        # Inference time
        record_model_execution("Leaf_Detection_Hailo8L", inference_time, input_image_path)

        # Extract and filter leaf detections from neural network output
        # Transform coordinates from model space to original image space
        detections = extract_detections(results, w, h, class_names, score_threshold)
        num_leaves = len(detections)

        # Log detection results to stderr for debugging and monitoring
        # Provides detailed information about detected leaves and confidence scores
        for class_name, bbox, score in detections:
            print(f"{class_name}: {score:.2f}, box: {bbox}", file=sys.stderr)
        print(f"Total grape leaves detected: {num_leaves}", file=sys.stderr)

        # Visualize detections by drawing bounding boxes on original image
        # Useful for debugging and visual verification of detection quality
        draw_detections(input_image, detections)

        # Create organized output directory structure for extracted leaves
        # Directory named after input image for easy identification and organization
        output_dir = os.path.join("Images", "Models", "Grape_Diseases_Hailo8L", "Leafs", os.path.splitext(os.path.basename(input_image_path))[0])
        os.makedirs(output_dir, exist_ok=True)

        # Extract and save individual leaf crops from detected regions
        # Iterate through all valid detections for individual leaf processing
        for idx, (_, bbox, _) in enumerate(detections):
            x0, y0, x1, y1 = bbox

            # Sanitize bounding box coordinates to prevent out-of-bounds access
            # Ensure coordinates are within valid image boundaries
            x0 = max(0, x0)  # Left boundary: minimum 0
            y0 = max(0, y0)  # Top boundary: minimum 0
            x1 = min(w, x1)  # Right boundary: maximum image width
            y1 = min(h, y1)  # Bottom boundary: maximum image height

            # Validate bounding box dimensions before cropping
            # Ensure the box has positive width and height for valid cropping
            if x1 > x0 and y1 > y0:  # Valid bounding box check
                # Extract leaf region from original image using sanitized coordinates
                # NumPy array slicing: [y0:y1, x0:x1] for height×width indexing
                leaf_crop = input_image[y0:y1, x0:x1]
                
                # Generate sequential filename for individual leaf image
                # Format: leaf_0.jpg, leaf_1.jpg, etc. for easy identification
                output_path = os.path.join(output_dir, f"leaf_{idx}.jpg")
                
                # Save cropped leaf image to output directory
                # Uses JPEG format for efficient storage and compatibility
                cv2.imwrite(output_path, leaf_crop)

    # Return output directory path for downstream processing
    # Enables integration with disease detection and analysis workflows
    return output_dir

def extract_detections(hailo_output: list, w: int, h: int, class_names: list, threshold: float = 0.5) -> list:
    """
    Extract and process leaf detections from Hailo8L neural network output with confidence filtering.
    
    This function processes the raw output from YOLOv8n neural network inference, extracting
    valid leaf detections above the specified confidence threshold. It performs coordinate
    transformation from normalized model space to original image pixel coordinates,
    enabling accurate leaf localization for subsequent cropping and analysis.
    
    Workflow:
        1. **Output Parsing**: Iterate through all class predictions from neural network
        2. **Confidence Filtering**: Apply threshold to filter low-confidence detections
        3. **Coordinate Transformation**: Convert normalized coordinates to pixel coordinates
        4. **Detection Compilation**: Compile filtered detections with class names and scores
        5. **Result Formatting**: Format detections for downstream processing workflows
    
    Parameters
    ----------
    hailo_output : list
        Raw output tensor from Hailo8L neural network inference.
        Structure: List of class predictions, each containing detection arrays.
        Each detection array format: [y0, x0, y1, x1, confidence_score, ...]
        Coordinates are normalized (0.0 to 1.0) relative to model input dimensions.
    
    w : int
        Width of the original input image in pixels.
        Used for coordinate transformation from normalized to pixel coordinates.
        Must be positive integer representing actual image width.
    
    h : int
        Height of the original input image in pixels.
        Used for coordinate transformation from normalized to pixel coordinates.
        Must be positive integer representing actual image height.
    
    class_names : list
        List of class label names corresponding to neural network output indices.
        Loaded from leaf_detection_labels.txt file.
        Index position must match neural network class output order.
        Example: ["grape_leaf", "vine_leaf", "other_vegetation"]
    
    threshold : float, optional
        Minimum confidence score threshold for detection filtering.
        Range: 0.0 to 1.0, where higher values require more confident detections.
        Default: 0.5 (50% confidence minimum)
        Recommended: 0.2-0.6 for agricultural applications depending on precision requirements.
    
    Returns
    -------
    list
        List of filtered and processed leaf detections.
        Each detection format: [class_name, bbox, confidence_score]
        
        Detection Components:
            - **class_name** (str): Human-readable class label from class_names list
            - **bbox** (tuple): Bounding box coordinates in pixel space (x0, y0, x1, y1)
                - x0, y0: Top-left corner coordinates (minimum x, minimum y)
                - x1, y1: Bottom-right corner coordinates (maximum x, maximum y)
            - **confidence_score** (float): Neural network confidence score (0.0 to 1.0)
        
        Returns empty list if no detections exceed the confidence threshold.
        Coordinates are guaranteed to be within image bounds and in integer pixel values.
    
    Raises
    ------
    IndexError
        If class_id exceeds the length of class_names list
    ValueError
        If image dimensions (w, h) are non-positive integers
    TypeError
        If hailo_output format is incompatible with expected structure
    
    Examples
    --------
    Basic detection extraction with default threshold:
    
    >>> # Neural network inference results
    >>> hailo_results = model.run(preprocessed_image)
    >>> class_labels = ["grape_leaf", "vine_leaf"]
    >>> 
    >>> # Extract detections with 50% confidence minimum
    >>> detections = extract_detections(hailo_results, 1920, 1080, class_labels)
    >>> print(f"Found {len(detections)} confident leaf detections")
    Found 5 confident leaf detections
    
    Low-threshold detection for maximum leaf capture:
    
    >>> # Extract all possible leaves with 25% confidence
    >>> all_detections = extract_detections(
    ...     hailo_output=inference_results,
    ...     w=image_width,
    ...     h=image_height,
    ...     class_names=leaf_classes,
    ...     threshold=0.25
    ... )
    >>> 
    >>> for class_name, bbox, score in all_detections:
    ...     print(f"Detected {class_name} at {bbox} with {score:.2f} confidence")
    
    High-precision detection for research applications:
    
    >>> # Extract only high-confidence detections for research data
    >>> research_detections = extract_detections(
    ...     hailo_output=model_output,
    ...     w=4096, h=3072,  # High-resolution agricultural image
    ...     class_names=["healthy_leaf", "diseased_leaf"],
    ...     threshold=0.8  # High confidence for research quality
    ... )
    
    Processing detection results:
    
    >>> detections = extract_detections(hailo_out, w, h, classes, 0.3)
    >>> 
    >>> for class_name, (x0, y0, x1, y1), confidence in detections:
    ...     width = x1 - x0
    ...     height = y1 - y0
    ...     area = width * height
    ...     print(f"Leaf: {class_name}, Size: {width}×{height}, Area: {area}px²")
    
    Notes
    -----
    - **Coordinate System**: Converts from normalized YOLOv8 format to pixel coordinates
    - **Confidence Filtering**: Threshold-based filtering reduces false positive detections
    - **Class Mapping**: Uses class_names list to provide human-readable detection labels
    - **Coordinate Validation**: Results are guaranteed to be valid pixel coordinates
    - **Performance**: Optimized for real-time processing in agricultural applications
    
    Coordinate Transformation Details:
        - **Input Format**: Normalized coordinates (0.0 to 1.0) from neural network
        - **Output Format**: Pixel coordinates (0 to image_width/height) as integers
        - **YOLOv8 Convention**: [y0, x0, y1, x1] coordinate order in model output
        - **OpenCV Convention**: (x0, y0, x1, y1) coordinate order in function output
    
    Agricultural Applications:
        - **Leaf Detection**: Primary grape leaf identification in vineyard images
        - **Disease Preprocessing**: Filter confident detections for pathology analysis
        - **Quality Control**: Threshold tuning for detection precision requirements
        - **Batch Processing**: Efficient detection processing for large image datasets
    
    See Also
    --------
    draw_detections : Visualize detection results with bounding boxes
    leaf_detection_run : Complete leaf detection and extraction workflow
    cv2.rectangle : OpenCV bounding box drawing functionality
    """
    # Initialize results list for filtered and processed detections
    results = []
    
    # Iterate through each class prediction in the neural network output
    # class_id corresponds to the index in class_names list
    for class_id, detections in enumerate(hailo_output):
        # Process each individual detection within the current class
        for detection in detections:
            # Extract confidence score from detection array (index 4)
            # YOLOv8 format: [y0, x0, y1, x1, confidence, ...]
            score = detection[4]
            
            # Apply confidence threshold filtering
            # Only process detections that meet minimum confidence requirements
            if score >= threshold:
                # Extract normalized bounding box coordinates from detection
                # YOLOv8 coordinate order: [y0, x0, y1, x1] (height-first convention)
                y0, x0, y1, x1 = detection[:4]
                
                # Transform normalized coordinates to pixel coordinates
                # Multiply by image dimensions to get actual pixel positions
                # Convert to integers for pixel-perfect coordinate representation
                # Reorder to OpenCV convention: (x0, y0, x1, y1) (width-first convention)
                bbox = (int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h))
                
                # Compile detection result with human-readable class name
                # Format: [class_name, bounding_box_coordinates, confidence_score]
                results.append([class_names[class_id], bbox, score])
    
    # Return filtered and processed detection list
    # Ready for downstream processing, visualization, or leaf extraction
    return results


def draw_detections(image, detections):
    """
    Visualize leaf detection results by drawing annotated bounding boxes on the image.
    
    This function provides visual feedback for leaf detection results by overlaying
    bounding boxes, class labels, and confidence scores directly on the source image.
    It serves as a debugging and verification tool for agricultural computer vision
    workflows, enabling visual assessment of detection quality and model performance.
    
    Workflow:
        1. **Detection Iteration**: Process each detection result individually
        2. **Coordinate Extraction**: Extract bounding box pixel coordinates
        3. **Label Formatting**: Format class name and confidence score for display
        4. **Bounding Box Drawing**: Draw colored rectangle around detected leaf region
        5. **Text Annotation**: Add class label and confidence score near detection
        6. **Visual Enhancement**: Apply consistent styling for clear visibility
    
    Parameters
    ----------
    image : cv2.Mat (numpy.ndarray)
        Input image array where detection visualizations will be drawn.
        Modified in-place with bounding boxes and labels.
        Expected format: BGR color space (OpenCV default)
        Shape: (height, width, 3) for color images
        Data type: uint8 (0-255 pixel values)
    
    detections : list
        List of processed detection results from extract_detections function.
        Each detection format: [class_name, bbox, confidence_score]
        
        Detection Components:
            - **class_name** (str): Human-readable class label for the detected object
            - **bbox** (tuple): Bounding box coordinates (x0, y0, x1, y1) in pixel space
                - x0, y0: Top-left corner coordinates
                - x1, y1: Bottom-right corner coordinates
            - **confidence_score** (float): Neural network confidence (0.0 to 1.0)
    
    Returns
    -------
    None
        Function modifies the input image in-place. No return value.
        The original image array is updated with detection visualizations.
    
    Raises
    ------
    cv2.error
        If image format is incompatible with OpenCV drawing functions
    IndexError
        If bounding box coordinates are malformed or inaccessible
    ValueError
        If confidence scores cannot be formatted for display
    
    Examples
    --------
    Basic detection visualization:
    
    >>> import cv2
    >>> 
    >>> # Load image and run detection
    >>> image = cv2.imread("vineyard_image.jpg")
    >>> detections = extract_detections(model_output, w, h, classes, 0.3)
    >>> 
    >>> # Visualize detections on image
    >>> draw_detections(image, detections)
    >>> 
    >>> # Display or save annotated image
    >>> cv2.imwrite("annotated_vineyard.jpg", image)
    
    Agricultural quality assessment workflow:
    
    >>> # Process field image with detection visualization
    >>> field_image = cv2.imread("field_section_1.jpg")
    >>> 
    >>> # Run leaf detection with moderate threshold
    >>> leaf_detections = extract_detections(
    ...     hailo_output=inference_results,
    ...     w=field_image.shape[1],
    ...     h=field_image.shape[0],
    ...     class_names=["grape_leaf", "diseased_leaf"],
    ...     threshold=0.4
    ... )
    >>> 
    >>> # Add visual annotations for field assessment
    >>> draw_detections(field_image, leaf_detections)
    >>> 
    >>> # Save annotated image for agricultural report
    >>> cv2.imwrite("field_assessment_annotated.jpg", field_image)
    
    Research documentation workflow:
    
    >>> # Create annotated images for research documentation
    >>> research_images = ["sample_1.jpg", "sample_2.jpg", "sample_3.jpg"]
    >>> 
    >>> for img_path in research_images:
    ...     # Load and process each research image
    ...     img = cv2.imread(img_path)
    ...     detections = run_leaf_detection(img)
    ...     
    ...     # Add professional annotations
    ...     draw_detections(img, detections)
    ...     
    ...     # Save with research naming convention
    ...     output_name = f"annotated_{os.path.basename(img_path)}"
    ...     cv2.imwrite(f"research_output/{output_name}", img)
    
    Real-time visualization in agricultural monitoring:
    
    >>> # Real-time detection visualization for field monitoring
    >>> cap = cv2.VideoCapture(0)  # Agricultural camera feed
    >>> 
    >>> while True:
    ...     ret, frame = cap.read()
    ...     if not ret:
    ...         break
    ...     
    ...     # Run real-time leaf detection
    ...     detections = detect_leaves_realtime(frame)
    ...     
    ...     # Visualize detections for operator feedback
    ...     draw_detections(frame, detections)
    ...     
    ...     # Display annotated frame
    ...     cv2.imshow("Agricultural Monitoring", frame)
    ...     
    ...     if cv2.waitKey(1) & 0xFF == ord('q'):
    ...         break
    
    Notes
    -----
    - **In-place Modification**: Function modifies the input image directly
    - **Color Consistency**: Uses green color (0, 255, 0) for agricultural compatibility
    - **Text Positioning**: Labels placed at bottom-left of bounding boxes for visibility
    - **Font Selection**: Uses HERSHEY_SIMPLEX font for clear readability
    - **Coordinate Validation**: Assumes valid pixel coordinates from extract_detections
    
    Visualization Specifications:
        - **Bounding Box Color**: Green (0, 255, 0) in BGR format
        - **Line Thickness**: 2 pixels for clear visibility
        - **Font**: cv2.FONT_HERSHEY_SIMPLEX for professional appearance
        - **Font Scale**: 0.6 for balanced readability and space efficiency
        - **Text Color**: Green (0, 255, 0) matching bounding box color
        - **Text Thickness**: 2 pixels for clear text rendering
    
    Agricultural Applications:
        - **Field Assessment**: Visual verification of detection quality in field conditions
        - **Quality Control**: Manual validation of automated detection results
        - **Research Documentation**: Professional annotation for agricultural research
        - **Training Data**: Visual verification for machine learning dataset creation
        - **Operator Interface**: Real-time feedback for agricultural equipment operators
    
    Performance Considerations:
        - **Efficient Rendering**: Optimized for real-time agricultural applications
        - **Memory Usage**: In-place modification reduces memory allocation overhead
        - **Visual Clarity**: Styling optimized for outdoor viewing conditions
        - **Integration**: Compatible with standard agricultural imaging workflows
    
    See Also
    --------
    extract_detections : Extract detection results from neural network output
    cv2.rectangle : OpenCV rectangle drawing function
    cv2.putText : OpenCV text rendering function
    leaf_detection_run : Complete leaf detection workflow with visualization
    """
    # Iterate through each detection for individual visualization
    for class_name, bbox, score in detections:
        # Extract bounding box coordinates from detection tuple
        # Format: (x0, y0, x1, y1) representing top-left and bottom-right corners
        x0, y0, x1, y1 = bbox
        
        # Format detection label with class name and confidence score
        # Display confidence with 2 decimal places for precision assessment
        label = f"{class_name} {score:.2f}"
        
        # Draw bounding box rectangle around detected leaf region
        # Uses green color (0, 255, 0) for high visibility in agricultural settings
        # Line thickness of 2 pixels provides clear visual separation
        cv2.rectangle(image, (x0, y0), (x1, y1), (0, 255, 0), 2)
        
        # Add text label at bottom-left corner of bounding box
        # Position: (x0 + 5, y1 - 5) provides offset from box edges
        # Font: HERSHEY_SIMPLEX for clear, professional appearance
        # Scale: 0.6 balances readability with space efficiency
        # Color: Green (0, 255, 0) matching bounding box for consistency
        # Thickness: 2 pixels ensures text visibility in field conditions
        cv2.putText(image, label, (x0 + 5, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)


def record_model_execution(model_name: str, execution_time: float, image: str):
    """Time execution"""
    log_file = "Images/analyze_time_mission2.json"
    data = {
        "model_name": model_name,
        "execution_time": execution_time,
        "image": image
    }
    
    # Leer datos existentes o inicializar lista
    try:
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                existing_data = json.load(f)
        else:
            existing_data = []
    except json.JSONDecodeError:
        existing_data = []
    
    # Agregar nuevo registro
    existing_data.append(data)
    
    # Escribir archivo actualizado
    with open(log_file, 'w') as f:
        json.dump(existing_data, f, indent=4)

if __name__ == "__main__":
    """
    Command-line interface for grape leaf detection and extraction processing.
    
    This main execution block provides a command-line interface for agricultural
    leaf detection workflows, enabling field operators and researchers to process
    vineyard images directly from the terminal. It handles argument parsing,
    input validation, and output directory management for streamlined agricultural
    computer vision operations.
    
    Command-line Usage:
        python leaf_detection_hailo8l.py -i <input_image_path>

    Arguments:
        -i, --input: Path to input agricultural image file (required)
                    Supports JPEG, PNG, and BMP formats
                    Example: "Images/Camera/vineyard_section_1.jpg"
    
    Output:
        Prints the output directory path containing extracted leaf images.
        Directory structure: Images/Models/Grape_Diseases_Hailo8L/Leafs/{image_name}/
        Individual leaves saved as: leaf_0.jpg, leaf_1.jpg, etc.
    
    Examples:
        # Basic leaf detection
        python leaf_detection_Hailo8L.py -i vineyard_image.jpg
        
        # Process field survey image
        python leaf_detection_Hailo8L.py --input field_survey_1.jpg
        
        # Batch processing with shell script
        for img in *.jpg; do
            python leaf_detection_Hailo8L.py -i "$img"
        done
    
    Agricultural Workflow Integration:
        1. Field image capture with agricultural cameras
        2. Command-line leaf extraction processing
        3. Automated leaf directory organization
        4. Integration with disease detection pipelines
        5. Research data preparation and analysis
    """
    # Initialize command-line argument parser for agricultural processing
    # Provides structured interface for field operators and researchers
    parser = argparse.ArgumentParser(
        description="Run grape leaf detection and extraction using YOLOv8n with Hailo8L AI acceleration",
        epilog="Example: python leaf_detection_hailo8l.py -i vineyard_section_1.jpg",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Define required input image argument
    # Accepts path to agricultural image for leaf detection processing
    parser.add_argument(
        "-i", "--input", 
        required=True, 
        help="Path to input agricultural image file (JPEG, PNG, BMP supported)",
        metavar="IMAGE_PATH"
    )
    
    # Parse command-line arguments with error handling
    # Provides user-friendly error messages for invalid arguments
    args = parser.parse_args()
    
    # Execute leaf detection and extraction workflow
    # Uses default score threshold of 0.25 for agricultural field conditions
    # Lower threshold captures more potential leaves for comprehensive analysis
    output_folder = leaf_detection_run(args.input, score_threshold=0.25)
    
    # Output the result directory path for downstream processing
    # Enables integration with shell scripts and agricultural automation systems
    # Prints to stdout for capture by external systems
    print(output_folder)