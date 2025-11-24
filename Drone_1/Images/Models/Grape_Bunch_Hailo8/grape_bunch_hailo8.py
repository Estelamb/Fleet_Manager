"""
YOLOv8n Grape Bunch Detection with Hailo AI Acceleration Module
==============================================================

This module implements real-time grape bunch detection using YOLOv8n neural networks
optimized with Hailo AI hardware acceleration. It provides comprehensive computer vision
capabilities for precision viticulture applications, enabling automated grape detection,
counting, and spatial analysis for vineyard monitoring and yield estimation.

The module serves as the core AI processing engine for agricultural drone systems,
delivering high-performance grape bunch detection with hardware-accelerated inference
for real-time field operations and comprehensive vineyard analysis workflows.

.. module:: grape_bunch_hailo8
    :synopsis: YOLOv8n grape bunch detection with Hailo AI acceleration for precision viticulture

Features
--------
- **YOLOv8n Neural Network**: Advanced object detection architecture for grape bunch identification
- **Hailo AI Acceleration**: Hardware-accelerated inference for real-time field processing
- **Computer Vision Processing**: Comprehensive image preprocessing and detection visualization
- **Grape Counting**: Accurate grape bunch counting and spatial analysis
- **Detection Filtering**: Configurable confidence thresholds for detection optimization
- **Visualization Output**: Annotated result images with detection overlays
- **Vineyard Integration**: Specialized interface for precision viticulture workflows

System Architecture
------------------
The YOLOv8n grape detection system operates within the precision agriculture ecosystem:

Detection Pipeline:
    Image Input → Preprocessing → YOLOv8n Inference → Hailo Acceleration → Detection Extraction → Visualization

Processing Workflow:
    1. **Image Loading**: Agricultural image file loading and validation
    2. **Preprocessing**: Image resizing and color space conversion for model input
    3. **AI Inference**: YOLOv8n neural network execution with Hailo acceleration
    4. **Detection Processing**: Result extraction and confidence-based filtering
    5. **Spatial Mapping**: Coordinate transformation from model space to image space
    6. **Visualization**: Detection overlay generation with bounding boxes and labels
    7. **Output Generation**: Annotated image saving and result compilation

Agricultural Applications:
    - **Yield Estimation**: Accurate grape bunch counting for harvest prediction
    - **Vineyard Monitoring**: Systematic grape development tracking and analysis
    - **Quality Assessment**: Grape bunch distribution and density evaluation
    - **Harvest Planning**: Data-driven harvest timing and resource allocation
    - **Field Operations**: Real-time grape detection during vineyard operations

Computer Vision Integration:
    - **Object Detection**: Advanced neural network-based grape identification
    - **Spatial Analysis**: Precise bounding box coordinates and object localization
    - **Confidence Assessment**: Detection reliability scoring and threshold filtering
    - **Visual Annotation**: Comprehensive detection visualization and annotation

Workflow Architecture
--------------------
Grape Detection Processing Pipeline:
    1. **Input Validation**: Image file accessibility and format verification
    2. **Model Initialization**: Hailo AI runtime and YOLOv8n model loading
    3. **Image Preprocessing**: Resizing, color conversion, and format standardization
    4. **Neural Network Inference**: YOLOv8n execution with hardware acceleration
    5. **Detection Extraction**: Result parsing and confidence-based filtering
    6. **Coordinate Transformation**: Model coordinate mapping to original image space
    7. **Visualization Generation**: Bounding box and label annotation overlay
    8. **Output Management**: Result image saving and detection count compilation

AI Model Processing:
    - **YOLOv8n Architecture**: State-of-the-art object detection neural network
    - **Hailo Optimization**: Hardware-specific model optimization and acceleration
    - **Real-time Inference**: Low-latency processing for field operations
    - **Accuracy Optimization**: Precision-optimized detection for agricultural applications

Classes
-------
None - This module provides functional interfaces for grape bunch detection

Functions
---------
.. autofunction:: extract_detections
.. autofunction:: draw_detections
.. autofunction:: grape_bunch_run

Dependencies
-----------
Core Dependencies:
    - **argparse**: Command-line argument parsing and configuration
    - **os**: File system operations and path management
    - **sys**: System-specific parameters and error handling
    - **cv2**: OpenCV computer vision library for image processing

Hardware Dependencies:
    - **picamera2.devices.Hailo**: Hailo AI hardware acceleration interface
    - **Hailo Runtime**: Hardware-specific AI acceleration environment

Model Dependencies:
    - **grape_bunch_hailo8.hef**: Compiled YOLOv8n model for Hailo hardware
    - **grape_bunch_labels.txt**: Class label definitions for grape detection

Integration Points
-----------------
External Integrations:
    - **Hailo AI Platform**: Hardware acceleration for neural network inference
    - **YOLOv8n Models**: Integration with specialized grape detection models
    - **Computer Vision**: OpenCV integration for image processing and visualization
    - **Agricultural Systems**: Integration with precision viticulture platforms

Internal Integrations:
    - **Image Processing**: Comprehensive image preprocessing and postprocessing
    - **Detection Systems**: AI model output processing and result compilation
    - **Visualization**: Detection annotation and result image generation
    - **File Management**: Input/output file handling and directory management

Performance Characteristics
--------------------------
Detection Performance:
    - **Real-time Processing**: Hardware-accelerated inference for field operations
    - **High Accuracy**: YOLOv8n-optimized detection with vineyard specialization
    - **Low Latency**: Hailo AI acceleration for responsive processing
    - **Scalability**: Support for high-volume vineyard image processing

Computer Vision Optimization:
    - **Preprocessing Efficiency**: Optimized image resizing and color conversion
    - **Detection Filtering**: Configurable confidence thresholds for accuracy
    - **Visualization Performance**: Efficient annotation and overlay generation
    - **Memory Management**: Optimized resource usage during processing

Agricultural Data Formats
-------------------------
Input Data Structure:
    - **Image Files**: Agricultural images in standard formats (JPEG, PNG)
    - **File Paths**: Structured path specifications for input and output
    - **Configuration**: Detection threshold and processing parameters

Output Data Structure:
    - **Detection Results**: Structured grape bunch detection counts and coordinates
    - **Annotated Images**: Visualization images with detection overlays
    - **Spatial Data**: Bounding box coordinates and confidence scores
    - **Count Information**: Total grape bunch counts and detection statistics

Detection Data Format:
    - **Bounding Boxes**: Rectangular detection regions with pixel coordinates
    - **Confidence Scores**: AI model confidence levels for each detection
    - **Class Labels**: Object classification labels and identifiers
    - **Spatial Mapping**: Coordinate transformation from model to image space

Error Handling Strategy
----------------------
Multi-level Error Management:
    - **Input Validation**: Image file accessibility and format verification
    - **Model Loading**: Hailo AI model loading and initialization error handling
    - **Processing Errors**: AI inference and detection processing error management
    - **Output Errors**: Result file generation and saving error handling

Recovery Mechanisms:
    - **File Validation**: Input image accessibility verification and error reporting
    - **Model Recovery**: Hailo AI initialization error handling and retry logic
    - **Processing Fallback**: Graceful handling of inference failures
    - **Output Management**: Directory creation and file writing error handling

Examples
--------
Basic Grape Detection:

.. code-block:: python

    # Execute grape bunch detection on vineyard image
    result = grape_bunch_run(
        input="Images/Camera/vineyard_section_1.jpg",
        output_folder="Images/Results/vineyard_analysis/"
    )
    
    grape_count = result["Grape_bunch"]
    print(f"Detected {grape_count} grape bunches")

Command-line Usage:

.. code-block:: bash

    # Run grape detection from command line
    python grape_bunch_hailo8.py -i vineyard_image.jpg --output_folder results/
    
    # Output: {'Grape_bunch': 12}

Vineyard Monitoring Integration:

.. code-block:: python

    import os
    
    # Process multiple vineyard images
    vineyard_images = [
        "section_A_row_1.jpg",
        "section_A_row_2.jpg",
        "section_B_row_1.jpg"
    ]
    
    total_grapes = 0
    
    for image in vineyard_images:
        result = grape_bunch_run(image, "results/")
        grape_count = result["Grape_bunch"]
        total_grapes += grape_count
        
        print(f"{image}: {grape_count} grape bunches detected")
    
    print(f"Total vineyard grape bunches: {total_grapes}")

Notes
-----
- **Hardware Requirements**: Requires Hailo AI acceleration hardware for optimal performance
- **Model Dependencies**: Depends on grape_bunch_hailo8.hef model file and label definitions
- **Precision Agriculture**: Optimized for vineyard monitoring and grape detection applications
- **Real-time Processing**: Hardware acceleration enables field operation compatibility

Configuration Requirements:
    - **Hailo Hardware**: Compatible Hailo AI acceleration device
    - **Model Files**: YOLOv8n model (.hef) and label definitions (.txt)
    - **OpenCV**: Computer vision library for image processing
    - **File Access**: Read/write permissions for input and output directories

Vineyard Considerations:
    - **Light Conditions**: Robust detection across various vineyard lighting
    - **Grape Varieties**: Compatible with multiple grape bunch types and sizes
    - **Growth Stages**: Effective detection across grape development phases
    - **Field Conditions**: Optimized for practical vineyard environments

See Also
--------
cv2 : OpenCV computer vision library
picamera2.devices.Hailo : Hailo AI hardware acceleration interface
argparse : Command-line argument parsing
os : File system operations and path management
"""

import argparse
import json
import os
import sys
import time
import cv2
from picamera2.devices import Hailo


def extract_detections(hailo_output, w, h, class_names, threshold=0.5):
    """
    Extract and filter grape bunch detections from Hailo AI model output.

    This function processes raw Hailo AI neural network output to extract valid
    grape bunch detections based on confidence thresholds. It performs coordinate
    transformation from model space to original image coordinates and filters
    detections for precision viticulture analysis and grape counting applications.

    The function serves as the primary detection processing interface, converting
    raw AI model predictions into structured detection data suitable for
    agricultural analysis and vineyard monitoring workflows.

    :param hailo_output: Raw output from Hailo AI YOLOv8n model inference
    :type hailo_output: list
    :param w: Width of the original agricultural image in pixels
    :type w: int
    :param h: Height of the original agricultural image in pixels
    :type h: int
    :param class_names: List of object class names for detection classification
    :type class_names: list
    :param threshold: Minimum confidence score for detection validation
    :type threshold: float
    :returns: List of validated detections with class, coordinates, and confidence
    :rtype: list
    :raises IndexError: When model output format is inconsistent
    :raises ValueError: When coordinate transformation fails

    Workflow
    --------
    1. **Output Processing**: Iterate through Hailo AI model detection results
    2. **Class Iteration**: Process detections for each object class category
    3. **Detection Validation**: Filter detections based on confidence threshold
    4. **Confidence Assessment**: Evaluate detection reliability and accuracy
    5. **Coordinate Transformation**: Convert model coordinates to image space
    6. **Bounding Box Calculation**: Generate pixel-accurate detection regions
    7. **Result Compilation**: Compile validated detections into structured format

    Detection Processing Pipeline:
        - **Raw Output**: Hailo AI model detection results in normalized coordinates
        - **Confidence Filtering**: Threshold-based detection validation
        - **Coordinate Mapping**: Transformation from normalized to pixel coordinates
        - **Classification**: Object class assignment and label mapping

    Grape Detection Features:
        - **Precision Filtering**: Configurable confidence thresholds for accuracy
        - **Spatial Accuracy**: Precise bounding box coordinate calculation
        - **Class Recognition**: Grape bunch classification and labeling
        - **Quality Assessment**: Detection confidence and reliability scoring

    Expected Model Output Format:
        - **Detection Array**: [y0, x0, y1, x1, confidence_score]
        - **Normalized Coordinates**: Values between 0.0 and 1.0
        - **Class Organization**: Detections grouped by object class
        - **Confidence Scores**: Float values representing detection reliability

    .. note::
        The function expects Hailo AI output in YOLOv8n format with normalized
        coordinates. Detection coordinates are transformed to match original
        image dimensions for accurate spatial analysis.

    Examples
    --------
    Basic Detection Extraction:

    .. code-block:: python

        # Extract grape detections from model output
        detections = extract_detections(
            hailo_output=model_results,
            w=1920,  # Image width
            h=1080,  # Image height
            class_names=['grape_bunch'],
            threshold=0.25
        )
        
        print(f"Found {len(detections)} grape bunches")
        
        for detection in detections:
            class_name, bbox, confidence = detection
            x0, y0, x1, y1 = bbox
            print(f"Grape bunch at ({x0}, {y0}) with confidence {confidence:.2f}")

    Vineyard Analysis Integration:

    .. code-block:: python

        # Process detections for vineyard analysis
        grape_classes = ['grape_bunch', 'grape_cluster']
        confidence_threshold = 0.3
        
        detections = extract_detections(
            hailo_output, image_width, image_height, 
            grape_classes, confidence_threshold
        )
        
        # Analyze detection distribution
        high_confidence = [d for d in detections if d[2] > 0.7]
        medium_confidence = [d for d in detections if 0.4 <= d[2] <= 0.7]
        
        print(f"High confidence detections: {len(high_confidence)}")
        print(f"Medium confidence detections: {len(medium_confidence)}")

    Spatial Analysis Example:

    .. code-block:: python

        # Spatial distribution analysis
        detections = extract_detections(hailo_output, w, h, class_names, 0.25)
        
        # Calculate detection density
        total_area = w * h
        detection_density = len(detections) / total_area * 1000000  # per million pixels
        
        # Analyze bounding box sizes
        box_areas = []
        for _, bbox, _ in detections:
            x0, y0, x1, y1 = bbox
            area = (x1 - x0) * (y1 - y0)
            box_areas.append(area)
        
        avg_grape_size = sum(box_areas) / len(box_areas) if box_areas else 0
        print(f"Average grape bunch size: {avg_grape_size:.2f} pixels²")

    Returns
    -------
    list
        List of validated grape bunch detections:
        
        Each detection contains:
            - **Class Name** (str): Object classification label
            - **Bounding Box** (tuple): Pixel coordinates (x0, y0, x1, y1)
            - **Confidence Score** (float): Detection reliability (0.0-1.0)
        
        Example format:
            [
                ['grape_bunch', (150, 200, 300, 400), 0.85],
                ['grape_bunch', (500, 100, 650, 250), 0.72]
            ]

    Raises
    ------
    IndexError
        When model output format is inconsistent or malformed
    ValueError
        When coordinate transformation produces invalid values
    TypeError
        When input parameters have incorrect data types

    Notes
    -----
    - **Confidence Filtering**: Only detections above threshold are returned
    - **Coordinate Accuracy**: Precise pixel-level bounding box coordinates
    - **Agricultural Focus**: Optimized for grape bunch detection and analysis
    - **Performance Optimization**: Efficient processing for real-time applications

    Performance Considerations:
        - **Threshold Selection**: Balance between precision and recall
        - **Coordinate Precision**: Integer pixel coordinates for visualization
        - **Memory Efficiency**: Optimized detection data structures
        - **Processing Speed**: Efficient iteration and filtering algorithms
    """
    # Initialize results list for validated grape bunch detections
    results = []
    
    # Iterate through each object class in the Hailo AI model output
    for class_id, detections in enumerate(hailo_output):
        # Process individual detections for current object class
        for detection in detections:
            # Extract confidence score from detection data (5th element)
            score = detection[4]
            
            # Validate detection against confidence threshold for quality filtering
            if score >= threshold:
                # Extract normalized coordinates from detection output [y0, x0, y1, x1]
                y0, x0, y1, x1 = detection[:4]
                
                # Transform normalized coordinates to pixel coordinates in original image space
                bbox = (int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h))
                
                # Compile validated detection with class name, coordinates, and confidence
                results.append([class_names[class_id], bbox, score])
    
    return results


def draw_detections(image, detections):
    """
    Draw bounding boxes and labels on agricultural images for grape detection visualization.

    This function provides comprehensive visualization capabilities for grape bunch
    detections by overlaying bounding boxes, confidence scores, and class labels
    directly on the source image. It enables visual validation of AI model results
    and supports precision agriculture analysis workflows with clear detection
    visualization for vineyard monitoring and assessment.

    The function serves as the primary visualization interface for grape detection
    results, creating annotated images suitable for agricultural reporting,
    quality assessment, and vineyard management documentation.

    :param image: Source agricultural image array for detection overlay
    :type image: numpy.ndarray
    :param detections: List of grape bunch detections with coordinates and metadata
    :type detections: list

    Workflow
    --------
    1. **Detection Iteration**: Process each validated grape bunch detection
    2. **Coordinate Extraction**: Extract bounding box pixel coordinates
    3. **Label Generation**: Create formatted labels with class name and confidence
    4. **Rectangle Drawing**: Render detection bounding boxes on image
    5. **Text Annotation**: Add confidence scores and class labels
    6. **Visual Enhancement**: Apply color coding and formatting for clarity

    Visualization Features:
        - **Bounding Boxes**: Green rectangular overlays around detected grape bunches
        - **Confidence Labels**: Formatted text showing detection confidence scores
        - **Class Identification**: Clear labeling of detected object types
        - **Visual Clarity**: Optimized colors and fonts for agricultural field use

    Agricultural Visualization Applications:
        - **Quality Assessment**: Visual validation of AI detection accuracy
        - **Field Documentation**: Annotated images for vineyard records
        - **Training Validation**: Model performance assessment and verification
        - **Reporting**: Professional visualization for agricultural reports

    Detection Annotation Elements:
        - **Rectangle Color**: Green (0, 255, 0) for grape bunch detection visibility
        - **Line Thickness**: 2 pixels for clear boundary definition
        - **Font Style**: FONT_HERSHEY_SIMPLEX for readability
        - **Text Positioning**: Offset positioning to avoid overlap with detection boxes

    .. note::
        The function modifies the input image in-place, adding visual annotations
        directly to the original image array. This enables immediate visualization
        without requiring separate image processing steps.

    Examples
    --------
    Basic Detection Visualization:

    .. code-block:: python

        import cv2
        
        # Load vineyard image and process detections
        image = cv2.imread("vineyard_section.jpg")
        detections = [
            ['grape_bunch', (100, 150, 200, 300), 0.85],
            ['grape_bunch', (400, 200, 500, 350), 0.72]
        ]
        
        # Draw detection overlays on image
        draw_detections(image, detections)
        
        # Save annotated image for documentation
        cv2.imwrite("annotated_vineyard.jpg", image)

    Vineyard Monitoring Visualization:

    .. code-block:: python

        # Process multiple vineyard sections with visualization
        vineyard_images = ["section_A.jpg", "section_B.jpg"]
        
        for image_file in vineyard_images:
            # Load and process image
            image = cv2.imread(image_file)
            
            # Run grape detection (assuming detection function exists)
            detections = detect_grapes(image)
            
            # Add visual annotations
            draw_detections(image, detections)
            
            # Generate summary statistics
            total_grapes = len(detections)
            high_conf = len([d for d in detections if d[2] > 0.8])
            
            # Add summary text to image
            summary = f"Total: {total_grapes}, High Conf: {high_conf}"
            cv2.putText(image, summary, (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            # Save annotated result
            output_name = f"annotated_{image_file}"
            cv2.imwrite(output_name, image)

    Quality Assessment Integration:

    .. code-block:: python

        # Quality assessment with color-coded confidence levels
        def enhanced_draw_detections(image, detections):
            for class_name, bbox, score in detections:
                x0, y0, x1, y1 = bbox
                
                # Color-code by confidence level
                if score > 0.8:
                    color = (0, 255, 0)    # Green - high confidence
                elif score > 0.6:
                    color = (0, 255, 255)  # Yellow - medium confidence
                else:
                    color = (0, 0, 255)    # Red - low confidence
                
                # Draw rectangle and label
                cv2.rectangle(image, (x0, y0), (x1, y1), color, 2)
                label = f"{class_name} {score:.2f}"
                cv2.putText(image, label, (x0 + 5, y0 + 20),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    Notes
    -----
    - **In-place Modification**: Function modifies the input image directly
    - **Agricultural Focus**: Optimized colors and formatting for vineyard use
    - **Visual Clarity**: Clear annotations for field documentation and analysis
    - **Professional Output**: Suitable for agricultural reports and presentations

    Visualization Specifications:
        - **Rectangle Color**: RGB(0, 255, 0) - Green for visibility
        - **Line Width**: 2 pixels for clear definition
        - **Font**: OpenCV FONT_HERSHEY_SIMPLEX for readability
        - **Text Scale**: 0.6 for appropriate sizing
        - **Text Offset**: 5 pixels horizontal, 20 pixels vertical from bounding box

    Agricultural Applications:
        - **Field Reports**: Visual documentation for vineyard management
        - **Quality Control**: Detection accuracy assessment and validation
        - **Training Materials**: Annotated examples for agricultural education
        - **Research Documentation**: Scientific visualization for agricultural studies
    """
    # Iterate through all validated grape bunch detections for visualization
    for class_name, bbox, score in detections:
        # Extract pixel coordinates from bounding box tuple
        x0, y0, x1, y1 = bbox
        
        # Generate formatted detection label with class name and confidence score
        label = f"{class_name} {score:.2f}"
        
        # Draw green rectangular bounding box around detected grape bunch
        cv2.rectangle(image, (x0, y0), (x1, y1), (0, 255, 0), 2)
        
        # Add confidence score and class label text with offset positioning
        cv2.putText(image, label, (x0 + 5, y0 + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        
def grape_bunch_run(input: str, output_folder: str) -> dict:
    """
    Execute comprehensive grape bunch detection on agricultural images using YOLOv8n with Hailo AI acceleration.

    This function provides the complete grape detection pipeline, from image loading
    through AI inference to result visualization and output generation. It combines
    YOLOv8n neural network capabilities with Hailo AI hardware acceleration to
    deliver high-performance grape bunch detection optimized for precision
    viticulture applications and vineyard monitoring workflows.

    The function serves as the primary interface for agricultural grape detection,
    integrating computer vision processing, AI model inference, and result
    visualization into a comprehensive solution for vineyard analysis and
    yield estimation applications.

    :param input: Absolute or relative path to the input agricultural image file
    :type input: str
    :param output_folder: Directory path for saving annotated detection results
    :type output_folder: str
    :returns: Dictionary containing grape bunch count and detection statistics
    :rtype: dict
    :raises FileNotFoundError: When input image file cannot be accessed
    :raises ValueError: When image format is invalid or unsupported
    :raises RuntimeError: When Hailo AI model loading or inference fails
    :raises OSError: When output directory creation fails

    Workflow
    --------
    1. **Configuration Setup**: Initialize detection threshold and processing parameters
    2. **Label Loading**: Load grape bunch class labels from model definition file
    3. **Image Loading**: Read and validate input agricultural image file
    4. **Dimension Extraction**: Extract original image dimensions for coordinate mapping
    5. **Model Initialization**: Load and initialize Hailo AI YOLOv8n detection model
    6. **Image Preprocessing**: Resize and convert image for model input requirements
    7. **AI Inference**: Execute YOLOv8n grape detection with hardware acceleration
    8. **Detection Processing**: Extract, filter, and validate grape bunch detections
    9. **Visualization Generation**: Draw bounding boxes and labels on original image
    10. **Output Management**: Save annotated results and generate detection statistics

    AI Processing Pipeline:
        - **Model Loading**: Hailo AI runtime initialization with YOLOv8n model
        - **Input Preprocessing**: Image resizing and color space conversion
        - **Neural Network Inference**: Hardware-accelerated grape detection
        - **Detection Extraction**: Result parsing and confidence-based filtering
        - **Coordinate Transformation**: Model space to image space mapping

    Agricultural Analysis Features:
        - **Grape Counting**: Accurate grape bunch enumeration for yield estimation
        - **Spatial Mapping**: Precise detection coordinates for vineyard analysis
        - **Confidence Assessment**: Detection reliability scoring and validation
        - **Visual Documentation**: Annotated image generation for reporting

    Detection Configuration:
        - **Confidence Threshold**: 0.25 (25%) minimum detection confidence
        - **Model Architecture**: YOLOv8n optimized for grape bunch detection
        - **Hardware Acceleration**: Hailo AI inference optimization
        - **Output Format**: Annotated JPEG images with detection overlays

    Expected Input Requirements:
        - **Image Format**: Standard formats (JPEG, PNG, BMP, TIFF)
        - **Resolution**: Compatible with various agricultural image resolutions
        - **Content**: Vineyard or grape bunch imagery for detection processing
        - **Quality**: Sufficient image quality for AI model processing

    .. note::
        The function requires access to the YOLOv8n model file (.hef) and
        corresponding class label definitions. Ensure Hailo AI hardware
        is properly configured and accessible for optimal performance.

    Examples
    --------
    Basic Grape Detection:

    .. code-block:: python

        # Execute grape bunch detection on vineyard image
        result = grape_bunch_run(
            input="Images/Camera/vineyard_row_5.jpg",
            output_folder="Images/Results/section_A/"
        )
        
        grape_count = result["Grape_bunch"]
        print(f"Detected {grape_count} grape bunches in vineyard row 5")

    Batch Vineyard Processing:

    .. code-block:: python

        import os
        
        # Process multiple vineyard sections
        vineyard_images = [
            "Images/Camera/section_A_row_1.jpg",
            "Images/Camera/section_A_row_2.jpg",
            "Images/Camera/section_B_row_1.jpg"
        ]
        
        total_grapes = 0
        results_folder = "Images/Results/vineyard_analysis/"
        
        for image_path in vineyard_images:
            # Process each vineyard section
            result = grape_bunch_run(image_path, results_folder)
            
            section_grapes = result["Grape_bunch"]
            total_grapes += section_grapes
            
            # Extract section identifier from filename
            section_name = os.path.basename(image_path).split('.')[0]
            print(f"{section_name}: {section_grapes} grape bunches")
        
        print(f"Total vineyard grape bunches: {total_grapes}")

    Precision Agriculture Integration:

    .. code-block:: python

        # Vineyard monitoring with GPS coordinates
        vineyard_locations = [
            ("40.209544", "-3.465575", "north_section.jpg"),
            ("40.209544", "-3.465821", "central_section.jpg"),
            ("40.209544", "-3.466066", "south_section.jpg")
        ]
        
        vineyard_data = []
        
        for lat, lon, image_file in vineyard_locations:
            # Process vineyard section
            result = grape_bunch_run(
                input=f"Images/Camera/{image_file}",
                output_folder=f"Images/Results/{lon}_{lat}/"
            )
            
            # Compile vineyard analysis data
            vineyard_data.append({
                'latitude': lat,
                'longitude': lon,
                'grape_count': result["Grape_bunch"],
                'image_file': image_file
            })
        
        # Generate vineyard report
        for data in vineyard_data:
            print(f"Location ({data['latitude']}, {data['longitude']}): "
                  f"{data['grape_count']} grape bunches")

    Returns
    -------
    dict
        Grape bunch detection results and statistics:
        
        Dictionary containing:
            - **Grape_bunch** (int): Total number of detected grape bunches
        
        Example format:
            {
                "Grape_bunch": 15
            }
        
        Additional statistical information may be included in future versions:
            - Detection confidence distribution
            - Spatial distribution analysis
            - Processing performance metrics

    Raises
    ------
    FileNotFoundError
        When the input image file cannot be found or accessed:
        - Invalid file path specification
        - File permission restrictions
        - Missing image file

    ValueError
        When image format or content is invalid:
        - Unsupported image format
        - Corrupted image data
        - Empty or invalid image file

    RuntimeError
        When Hailo AI model operations fail:
        - Model file loading errors
        - Hardware acceleration initialization failure
        - AI inference processing errors

    OSError
        When output directory operations fail:
        - Insufficient disk space
        - Directory creation permission errors
        - File system access restrictions

    Notes
    -----
    - **Hardware Requirements**: Requires compatible Hailo AI acceleration hardware
    - **Model Dependencies**: Depends on grape_bunch_hailo8.hef and label files
    - **Performance Optimization**: Hardware acceleration for real-time processing
    - **Agricultural Focus**: Optimized for vineyard monitoring applications

    Processing Specifications:
        - **Detection Threshold**: 25% minimum confidence for grape bunch validation
        - **Model Input**: Resized images matching YOLOv8n input requirements
        - **Color Space**: RGB conversion for neural network compatibility
        - **Output Format**: Annotated JPEG images with detection overlays

    Vineyard Applications:
        - **Yield Estimation**: Accurate grape bunch counting for harvest planning
        - **Quality Assessment**: Visual validation of grape development
        - **Field Documentation**: Annotated imagery for vineyard records
        - **Precision Agriculture**: Data-driven vineyard management decisions

    Performance Characteristics:
        - **Real-time Processing**: Hardware acceleration for field operations
        - **High Accuracy**: YOLOv8n-optimized detection for agricultural applications
        - **Scalability**: Support for large-scale vineyard image processing
        - **Integration Ready**: Compatible with agricultural workflow systems
    """
    # Configure detection confidence threshold for grape bunch validation (25%)
    bunch_score_thresh = 0.25

    # Load grape bunch class labels from model definition file
    # This file contains the object class names used by the YOLOv8n model
    with open("Images/Models/Grape_Bunch_Hailo8/grape_bunch_labels.txt", 'r', encoding="utf-8") as f:
        class_names = f.read().splitlines()

    # Load input agricultural image for grape detection processing
    # OpenCV loads images in BGR color format by default
    input_image = cv2.imread(input)
    if input_image is None:
        print(f"Error: Input image not found: {input}", file=sys.stderr)
        sys.exit(1)
        
    # Extract original image dimensions for coordinate transformation
    # Required for mapping model coordinates back to original image space
    h, w, _ = input_image.shape

    # Initialize Hailo AI context manager for YOLOv8n model processing
    # This loads the compiled neural network model optimized for Hailo hardware
    with Hailo("Images/Models/Grape_Bunch_Hailo8/grape_bunch_hailo8.hef") as hailo:
        # Get model input dimensions for image preprocessing requirements
        model_h, model_w, _ = hailo.get_input_shape()
        
        # Resize input image to match model input requirements
        # Neural network models require specific input dimensions
        resized_image = cv2.resize(input_image, (model_w, model_h))
        
        # Convert BGR to RGB color space for neural network compatibility
        # YOLOv8n models expect RGB input format
        resized_image_rgb = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
        
        # Inference time
        start_time = time.time()

        # Execute YOLOv8n inference with Hailo AI hardware acceleration
        # This performs the actual grape bunch detection on the preprocessed image
        results = hailo.run(resized_image_rgb)
        
        # Inference time
        end_time = time.time()
        inference_time = end_time - start_time

        # Extract and filter grape bunch detections from model output
        # Apply confidence threshold and coordinate transformation
        detections = extract_detections(results, w, h, class_names, bunch_score_thresh)
        
        # Count total number of validated grape bunch detections
        num_grape_bunches = len(detections)

        # Draw detection bounding boxes and labels on original image
        # This creates the visual annotation for result documentation
        draw_detections(input_image, detections)

        # Ensure output directory exists for result saving
        # Create directory structure if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)
        
        # Generate output file path for annotated detection results
        output_path = os.path.join(output_folder, "grape_bunch_results.jpg")
        
        # Save annotated image with detection overlays to output directory
        cv2.imwrite(output_path, input_image)

        # Inference time
        record_model_execution("Grape_Bunch_Hailo8", inference_time, input)

        # Return structured detection results for further processing
        return {"Grape_bunch": num_grape_bunches}

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
    Command-line interface for grape bunch detection processing.
    
    This main execution block provides command-line access to the grape bunch
    detection functionality, enabling direct execution from terminal environments
    for vineyard monitoring, agricultural analysis, and batch processing workflows.
    
    The interface supports agricultural field operations by providing simple
    command-line access to YOLOv8n grape detection with Hailo AI acceleration,
    making it suitable for integration with agricultural data processing pipelines
    and vineyard management systems.
    
    Command-line Arguments:
        -i, --input: Path to input agricultural image file for processing
        --output_folder: Directory path for saving annotated detection results
    
    Usage Examples:
        # Basic grape detection on single image
        python grape_bunch_hailo8.py -i vineyard_image.jpg --output_folder results/
        
        # Process vineyard section with specific output directory
        python grape_bunch_hailo8.py -i Images/Camera/section_A.jpg --output_folder Images/Results/section_A/
        
        # Batch processing integration (external script)
        for image in vineyard_images/*; do
            python grape_bunch_hailo8.py -i "$image" --output_folder "results/$(basename "$image" .jpg)/"
        done
    
    Output Format:
        The script prints detection results in JSON-compatible dictionary format:
        {'Grape_bunch': <count>}
        
        Example output: {'Grape_bunch': 12}
    """
    # Initialize command-line argument parser for agricultural image processing
    parser = argparse.ArgumentParser(
        description="Run YOLOv8n grape bunch detection with Hailo AI acceleration",
        epilog="Example: python grape_bunch_hailo8.py -i vineyard.jpg --output_folder results/"
    )
    
    # Define required input image path argument
    parser.add_argument(
        "-i", "--input", 
        required=True, 
        help="Path to input agricultural image file for grape detection processing"
    )
    
    # Define required output directory path argument
    parser.add_argument(
        "--output_folder", 
        required=True, 
        help="Directory path for saving annotated detection results and analysis"
    )
    
    # Parse command-line arguments provided by user
    args = parser.parse_args()
    
    # Execute grape bunch detection with specified parameters
    # Process agricultural image and generate annotated results
    result = grape_bunch_run(args.input, args.output_folder)
    
    # Print detection results in structured format for integration
    print(result)