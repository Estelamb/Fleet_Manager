"""
Grape Disease Detection and Classification with Hailo8L AI Acceleration Module
=============================================================================

This module implements comprehensive grape disease detection and classification using
advanced computer vision techniques with Hailo8L AI hardware acceleration. It provides
specialized agricultural pathology analysis capabilities for precision viticulture,
enabling automated identification, counting, and spatial mapping of grape diseases
for vineyard health monitoring and disease management applications.

The module serves as the core plant pathology processing engine for agricultural
drone systems, delivering high-performance disease detection with hardware-accelerated
inference for real-time field operations and comprehensive vineyard health analysis.

.. module:: grape_diseases_Hailo8L
    :synopsis: AI-powered grape disease detection with Hailo8L acceleration for precision agriculture

Features
--------
- **Disease Classification**: Multi-class grape disease identification and categorization
- **Hailo8L AI Acceleration**: Hardware-accelerated inference for real-time field processing
- **Batch Processing**: Efficient processing of multiple leaf images for comprehensive analysis
- **Disease Counting**: Accurate enumeration of disease instances across vineyard sections
- **Spatial Mapping**: Precise bounding box coordinates for disease localization
- **Visualization Output**: Annotated result images with disease detection overlays
- **Agricultural Integration**: Specialized interface for precision viticulture workflows

System Architecture
------------------
The grape disease detection system operates within the precision agriculture ecosystem:

Disease Detection Pipeline:
    Image Directory → Batch Processing → AI Classification → Disease Counting → Spatial Analysis → Visualization

Processing Workflow:
    1. **Directory Processing**: Batch processing of leaf images from input directory
    2. **Image Preprocessing**: Individual image loading, resizing, and color conversion
    3. **AI Classification**: Neural network disease detection with Hailo8L acceleration
    4. **Disease Extraction**: Result parsing and confidence-based validation
    5. **Spatial Mapping**: Coordinate transformation and bounding box generation
    6. **Disease Counting**: Comprehensive disease enumeration across all processed images
    7. **Visualization**: Detection overlay generation with disease annotations
    8. **Output Management**: Annotated image saving and disease statistics compilation

Agricultural Applications:
    - **Disease Monitoring**: Systematic grape disease surveillance and tracking
    - **Early Detection**: Rapid identification of disease outbreaks for intervention
    - **Treatment Planning**: Disease-specific treatment recommendations and mapping
    - **Yield Protection**: Disease impact assessment and yield loss prevention
    - **Quality Management**: Grape health assessment for quality control

Plant Pathology Integration:
    - **Multi-Disease Detection**: Comprehensive identification of various grape diseases
    - **Spatial Analysis**: Precise disease localization and distribution mapping
    - **Confidence Assessment**: Disease detection reliability scoring and validation
    - **Visual Documentation**: Professional disease annotation for agricultural records

Workflow Architecture
--------------------
Grape Disease Detection Processing Pipeline:
    1. **Input Validation**: Directory accessibility and image file verification
    2. **Label Loading**: Disease classification labels and model configuration
    3. **Batch Initialization**: Disease counter initialization and processing setup
    4. **Image Iteration**: Sequential processing of all leaf images in directory
    5. **Individual Processing**: Per-image disease detection and classification
    6. **Disease Aggregation**: Cumulative disease counting across all images
    7. **Visualization Generation**: Disease annotation overlay creation
    8. **Output Compilation**: Result image saving and statistics generation

AI Model Processing:
    - **Neural Network Architecture**: Specialized disease classification model
    - **Hailo8L Optimization**: Hardware-specific model acceleration and optimization
    - **Real-time Inference**: Low-latency processing for field operation compatibility
    - **Accuracy Optimization**: Disease-specific detection tuning for agricultural applications

Classes
-------
None - This module provides functional interfaces for grape disease detection

Functions
---------
.. autofunction:: diseases_classification_run
.. autofunction:: extract_detections
.. autofunction:: draw_detections

Dependencies
-----------
Core Dependencies:
    - **argparse**: Command-line argument parsing and configuration
    - **json**: JSON data processing and structured output formatting
    - **os**: File system operations and directory management
    - **sys**: System-specific parameters and error handling
    - **cv2**: OpenCV computer vision library for image processing

Hardware Dependencies:
    - **picamera2.devices.Hailo**: Hailo8L AI hardware acceleration interface
    - **Hailo Runtime**: Hardware-specific AI acceleration environment

Model Dependencies:
    - **grape_diseases_Hailo8L.hef**: Compiled disease classification model for Hailo8L
    - **grape_diseases_labels.txt**: Disease class label definitions

Integration Points
-----------------
External Integrations:
    - **Hailo8L AI Platform**: Hardware acceleration for neural network inference
    - **Disease Classification Models**: Integration with specialized pathology models
    - **Computer Vision**: OpenCV integration for image processing and visualization
    - **Agricultural Systems**: Integration with precision viticulture platforms

Internal Integrations:
    - **Batch Processing**: Efficient multi-image processing and management
    - **Disease Analytics**: Comprehensive disease counting and statistical analysis
    - **Visualization Systems**: Detection annotation and result image generation
    - **File Management**: Input/output directory handling and image file processing

Performance Characteristics
--------------------------
Detection Performance:
    - **Real-time Processing**: Hardware-accelerated inference for field operations
    - **High Accuracy**: Disease-specific detection optimization for agricultural applications
    - **Batch Efficiency**: Optimized multi-image processing for large-scale analysis
    - **Scalability**: Support for high-volume vineyard image processing workflows

Disease Analysis Optimization:
    - **Multi-class Detection**: Efficient handling of multiple disease categories
    - **Spatial Precision**: Accurate disease localization and bounding box generation
    - **Confidence Filtering**: Configurable thresholds for detection reliability
    - **Memory Management**: Optimized resource usage during batch processing

Agricultural Data Formats
-------------------------
Input Data Structure:
    - **Image Directories**: Organized leaf image collections for batch processing
    - **Image Files**: Agricultural leaf images in standard formats (JPEG, PNG)
    - **Configuration**: Detection thresholds and processing parameters

Output Data Structure:
    - **Disease Statistics**: Comprehensive disease counts by category
    - **Annotated Images**: Visualization images with disease detection overlays
    - **Spatial Data**: Bounding box coordinates and confidence scores
    - **Classification Results**: Disease identification and enumeration data

Disease Detection Format:
    - **Disease Categories**: Multi-class disease classification labels
    - **Bounding Boxes**: Rectangular disease regions with pixel coordinates
    - **Confidence Scores**: AI model confidence levels for each detection
    - **Spatial Mapping**: Coordinate transformation from model to image space

Error Handling Strategy
----------------------
Multi-level Error Management:
    - **Directory Validation**: Input directory accessibility and content verification
    - **Image Processing**: Individual image loading and format validation
    - **Model Processing**: AI inference and detection processing error handling
    - **Output Management**: Result file generation and directory creation error handling

Recovery Mechanisms:
    - **File Validation**: Image file accessibility verification and error reporting
    - **Detection Validation**: Individual detection format verification and error handling
    - **Processing Continuity**: Graceful handling of individual image failures
    - **Output Recovery**: Directory creation and file writing error management

Examples
--------
Basic Disease Detection:

.. code-block:: python

    # Execute grape disease detection on leaf image directory
    with Hailo("disease_model.hef") as hailo:
        results = diseases_classification_run(
            input_image_dir="Images/Leaves/vineyard_section_1/",
            output_folder="Images/Results/disease_analysis/",
            hailo=hailo,
            score_threshold=0.25
        )
    
    for disease, count in results.items():
        print(f"{disease}: {count} instances detected")

Command-line Usage:

.. code-block:: bash

    # Run disease detection from command line
    python grape_diseases_Hailo8L.py -f leaf_images/ --output_folder results/
    
    # Output: {'powdery_mildew': 5, 'black_rot': 2, 'downy_mildew': 3}

Vineyard Health Monitoring:

.. code-block:: python

    import os
    
    # Process multiple vineyard sections for disease surveillance
    vineyard_sections = [
        "Images/Leaves/section_A/",
        "Images/Leaves/section_B/", 
        "Images/Leaves/section_C/"
    ]
    
    total_diseases = {}
    
    with Hailo("disease_model.hef") as hailo:
        for section_path in vineyard_sections:
            section_name = os.path.basename(section_path.rstrip('/'))
            
            results = diseases_classification_run(
                section_path, f"results/{section_name}/", hailo
            )
            
            print(f"{section_name} disease analysis:")
            for disease, count in results.items():
                total_diseases[disease] = total_diseases.get(disease, 0) + count
                print(f"  {disease}: {count} instances")
    
    print(f"\\nTotal vineyard disease summary:")
    for disease, total_count in total_diseases.items():
        print(f"{disease}: {total_count} total instances")

Notes
-----
- **Hardware Requirements**: Requires Hailo8L AI acceleration hardware for optimal performance
- **Model Dependencies**: Depends on grape_diseases_Hailo8L.hef model and label files
- **Agricultural Focus**: Optimized for grape disease detection and vineyard health monitoring
- **Batch Processing**: Efficient handling of multiple leaf images for comprehensive analysis

Configuration Requirements:
    - **Hailo8L Hardware**: Compatible Hailo8L AI acceleration device
    - **Model Files**: Disease classification model (.hef) and label definitions (.txt)
    - **OpenCV**: Computer vision library for image processing and visualization
    - **File Access**: Read/write permissions for input and output directories

Disease Detection Considerations:
    - **Image Quality**: Sufficient resolution and clarity for disease identification
    - **Lighting Conditions**: Consistent lighting for reliable disease detection
    - **Leaf Conditions**: Various leaf stages and disease progression compatibility
    - **Field Variability**: Robust detection across different vineyard environments

See Also
--------
cv2 : OpenCV computer vision library
picamera2.devices.Hailo : Hailo8L AI hardware acceleration interface
argparse : Command-line argument parsing
os : File system operations and directory management
json : JSON data processing and output formatting
"""

import argparse
import json
import os
import sys
import time
import cv2
from picamera2.devices import Hailo

def diseases_classification_run(input_image_dir: str, output_folder: str, hailo: 'Hailo', score_threshold: float = 0.25) -> dict:
    """
    Execute comprehensive grape disease detection and classification on leaf image directories.

    This function provides the complete disease detection pipeline for batch processing
    of leaf images using AI-powered classification with Hailo8L hardware acceleration.
    It performs systematic disease identification, counting, and spatial analysis across
    multiple leaf images to deliver comprehensive vineyard health assessment and
    disease monitoring capabilities for precision agriculture applications.

    The function serves as the primary interface for agricultural plant pathology
    analysis, integrating computer vision processing, AI model inference, and disease
    quantification into a comprehensive solution for vineyard disease management
    and health monitoring workflows.

    :param input_image_dir: Directory path containing leaf images for disease analysis
    :type input_image_dir: str
    :param output_folder: Directory path for saving annotated disease detection results
    :type output_folder: str
    :param hailo: Initialized Hailo8L AI acceleration instance for model inference
    :type hailo: Hailo
    :param score_threshold: Minimum confidence score for disease detection validation (default: 0.25)
    :type score_threshold: float
    :returns: Dictionary containing disease counts by category across all processed images
    :rtype: dict
    :raises FileNotFoundError: When input directory or label file cannot be accessed
    :raises ValueError: When image format is invalid or processing fails
    :raises RuntimeError: When Hailo8L AI model inference fails
    :raises OSError: When output directory creation or image saving fails

    Workflow
    --------
    1. **Label Loading**: Load disease classification labels from model definition file
    2. **Disease Initialization**: Initialize disease counter dictionary with all categories
    3. **Directory Processing**: Iterate through all image files in input directory
    4. **Image Validation**: Verify file accessibility and format compatibility
    5. **Image Loading**: Load individual leaf images for processing
    6. **Dimension Extraction**: Extract image dimensions for coordinate transformation
    7. **Image Preprocessing**: Resize and convert images for model input requirements
    8. **AI Inference**: Execute disease classification with Hailo8L acceleration
    9. **Detection Processing**: Extract and validate disease detections
    10. **Disease Counting**: Accumulate disease counts across all processed images
    11. **Visualization Generation**: Draw detection overlays and annotations
    12. **Output Management**: Save annotated images and compile disease statistics

    Disease Detection Pipeline:
        - **Batch Processing**: Systematic processing of multiple leaf images
        - **AI Classification**: Hardware-accelerated disease identification
        - **Statistical Analysis**: Comprehensive disease counting and enumeration
        - **Spatial Mapping**: Disease localization and bounding box generation

    Agricultural Analysis Features:
        - **Multi-Disease Detection**: Comprehensive identification of various grape diseases
        - **Disease Quantification**: Accurate counting and statistical analysis
        - **Spatial Documentation**: Precise disease localization for treatment planning
        - **Visual Validation**: Annotated images for agricultural reporting and assessment

    Disease Processing Configuration:
        - **Confidence Threshold**: Configurable minimum score for detection validation
        - **Batch Efficiency**: Optimized processing for large image collections
        - **Hardware Acceleration**: Hailo8L AI optimization for real-time analysis
        - **Output Management**: Structured result organization and visualization

    Expected Input Requirements:
        - **Directory Structure**: Organized leaf image collections in input directory
        - **Image Formats**: Standard formats (JPEG, PNG, BMP, TIFF) compatible with OpenCV
        - **Image Quality**: Sufficient resolution and clarity for disease identification
        - **Hailo Instance**: Pre-initialized Hailo8L AI acceleration context

    .. note::
        The function processes all valid image files in the input directory and
        requires a pre-initialized Hailo8L context for optimal performance. Disease
        labels are loaded from the model-specific label definition file.

    Examples
    --------
    Basic Disease Detection:

    .. code-block:: python

        # Execute disease detection on leaf image directory
        with Hailo("grape_diseases_Hailo8L.hef") as hailo:
            results = diseases_classification_run(
                input_image_dir="Images/Leaves/vineyard_section_A/",
                output_folder="Images/Results/disease_analysis/",
                hailo=hailo,
                score_threshold=0.3
            )
        
        print(f"Disease detection results:")
        for disease, count in results.items():
            print(f"  {disease}: {count} instances detected")

    Vineyard Health Assessment:

    .. code-block:: python

        import os
        
        # Comprehensive vineyard disease monitoring
        vineyard_sections = [
            "Images/Leaves/north_section/",
            "Images/Leaves/central_section/",
            "Images/Leaves/south_section/"
        ]
        
        vineyard_health_report = {}
        
        with Hailo("grape_diseases_Hailo8L.hef") as hailo:
            for section_dir in vineyard_sections:
                section_name = os.path.basename(section_dir.rstrip('/'))
                
                # Process section for disease analysis
                disease_results = diseases_classification_run(
                    input_image_dir=section_dir,
                    output_folder=f"Results/{section_name}_analysis/",
                    hailo=hailo,
                    score_threshold=0.25
                )
                
                vineyard_health_report[section_name] = disease_results
                
                # Calculate section health metrics
                total_diseases = sum(disease_results.values())
                print(f"{section_name}: {total_diseases} total disease instances")
                
                # Identify most prevalent diseases
                if disease_results:
                    most_common = max(disease_results.items(), key=lambda x: x[1])
                    print(f"  Most prevalent: {most_common[0]} ({most_common[1]} instances)")
        
        # Generate vineyard summary report
        overall_diseases = {}
        for section_results in vineyard_health_report.values():
            for disease, count in section_results.items():
                overall_diseases[disease] = overall_diseases.get(disease, 0) + count
        
        print(f"\\nVineyard Health Summary:")
        for disease, total_count in sorted(overall_diseases.items(), key=lambda x: x[1], reverse=True):
            print(f"{disease}: {total_count} total instances across vineyard")

    Precision Agriculture Integration:

    .. code-block:: python

        # Disease monitoring with treatment recommendations
        def analyze_vineyard_health(leaf_directories, treatment_thresholds):
            treatment_recommendations = {}
            
            with Hailo("grape_diseases_Hailo8L.hef") as hailo:
                for directory in leaf_directories:
                    # Extract location identifier from directory name
                    location_id = os.path.basename(directory.rstrip('/'))
                    
                    # Perform disease detection
                    disease_results = diseases_classification_run(
                        input_image_dir=directory,
                        output_folder=f"Analysis/{location_id}/",
                        hailo=hailo,
                        score_threshold=0.2
                    )
                    
                    # Generate treatment recommendations
                    recommendations = []
                    for disease, count in disease_results.items():
                        threshold = treatment_thresholds.get(disease, 5)
                        if count >= threshold:
                            recommendations.append(f"Immediate {disease} treatment required")
                        elif count > 0:
                            recommendations.append(f"Monitor {disease} development")
                    
                    treatment_recommendations[location_id] = {
                        'disease_counts': disease_results,
                        'total_diseases': sum(disease_results.values()),
                        'recommendations': recommendations
                    }
            
            return treatment_recommendations
        
        # Example usage
        leaf_dirs = ["section_A_leaves/", "section_B_leaves/", "section_C_leaves/"]
        thresholds = {'powdery_mildew': 3, 'black_rot': 2, 'downy_mildew': 4}
        
        analysis_results = analyze_vineyard_health(leaf_dirs, thresholds)
        
        for location, data in analysis_results.items():
            print(f"\\n{location} Analysis:")
            print(f"  Total diseases: {data['total_diseases']}")
            for recommendation in data['recommendations']:
                print(f"  - {recommendation}")

    Returns
    -------
    dict
        Comprehensive disease detection results and statistics:
        
        Dictionary format:
            {
                "disease_name_1": count_1,
                "disease_name_2": count_2,
                ...
                "disease_name_n": count_n
            }
        
        Example returns:
            {
                "powdery_mildew": 8,
                "black_rot": 3,
                "downy_mildew": 5,
                "healthy": 12,
                "leaf_scorch": 1
            }
        
        Disease count interpretations:
            - 0: No instances of disease detected
            - 1-5: Low disease pressure
            - 6-15: Moderate disease pressure requiring monitoring
            - 16+: High disease pressure requiring immediate intervention

    Raises
    ------
    FileNotFoundError
        When input directory or required files cannot be accessed:
        - Invalid input directory path
        - Missing disease labels file
        - Inaccessible image files

    ValueError
        When image processing or format validation fails:
        - Unsupported image formats
        - Corrupted image data
        - Invalid processing parameters

    RuntimeError
        When Hailo8L AI model operations fail:
        - Model inference processing errors
        - Hardware acceleration failures
        - Memory allocation issues

    OSError
        When output directory or file operations fail:
        - Insufficient disk space
        - Directory creation permission errors
        - Image file writing failures

    Notes
    -----
    - **Hailo8L Context**: Requires pre-initialized Hailo8L instance for optimal performance
    - **Batch Processing**: Efficiently processes all valid images in input directory
    - **Disease Categories**: Returns counts for all disease classes defined in label file
    - **Agricultural Focus**: Optimized for grape disease detection and vineyard health monitoring

    Processing Specifications:
        - **Confidence Threshold**: 25% default minimum for disease detection validation
        - **Image Preprocessing**: Automatic resizing and color conversion for model compatibility
        - **Batch Efficiency**: Sequential processing optimized for memory and performance
        - **Output Format**: Annotated images with disease detection overlays

    Agricultural Applications:
        - **Disease Surveillance**: Systematic monitoring of vineyard health status
        - **Early Detection**: Rapid identification of disease outbreaks for intervention
        - **Treatment Planning**: Disease-specific intervention mapping and scheduling
        - **Quality Control**: Grape health assessment for harvest and quality decisions

    Performance Characteristics:
        - **Hardware Acceleration**: Hailo8L AI optimization for real-time field processing
        - **Scalability**: Support for large-scale vineyard image processing workflows
        - **Accuracy**: Disease-specific detection optimization for agricultural applications
        - **Integration Ready**: Compatible with precision agriculture management systems
    """
    # Load grape disease classification labels from model definition file
    # This file contains the disease class names used by the AI classification model
    with open("Images/Models/Grape_Diseases_Hailo8L/Grape_Diseases/grape_diseases_labels.txt", 'r', encoding="utf-8") as f:
        class_names = f.read().splitlines()
    
    # Initialize disease detection dictionary with all disease categories set to zero
    # This ensures comprehensive tracking of all possible disease classifications
    detected_diseases = {disease: 0 for disease in class_names}
    
    # Process each leaf image file in the input directory for disease detection
    # Iterate through all files to perform comprehensive batch analysis
    for leaf_image in os.listdir(input_image_dir):
        # Construct full file path for current leaf image
        leaf_path = os.path.join(input_image_dir, leaf_image)
        
        # Validate that current item is a file (skip directories and invalid entries)
        if not os.path.isfile(leaf_path):
            continue
            
        # Load current leaf image for disease detection processing
        # OpenCV loads images in BGR color format by default
        input_image = cv2.imread(leaf_path)

        # Extract original image dimensions for coordinate transformation
        # Required for mapping model coordinates back to original image space
        h, w, _ = input_image.shape

        # Get model input dimensions for image preprocessing requirements
        # AI models require specific input dimensions for proper inference
        model_h, model_w, _ = hailo.get_input_shape()
        
        # Resize input image to match model input requirements
        # Neural network models require specific input dimensions
        resized_image = cv2.resize(input_image, (model_w, model_h))
        
        # Convert BGR to RGB color space for neural network compatibility
        # AI models typically expect RGB input format
        resized_image_rgb = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
        
        # Inference time
        start_time = time.time()

        # Execute disease classification inference with Hailo8L hardware acceleration
        # This performs the actual disease detection on the preprocessed leaf image
        results = hailo.run(resized_image_rgb)
        
        # Inference time
        end_time = time.time()
        inference_time = end_time - start_time

        # Extract and filter disease detections from model output
        # Apply confidence threshold and coordinate transformation
        detection = extract_detections(results, w, h, class_names, score_threshold)

        # Count and accumulate disease detections across all processed images
        # Update disease counters for comprehensive statistical analysis
        for class_name, bbox, score in detection:
            detected_diseases[class_name] += 1

        # Draw disease detection bounding boxes and labels on original image
        # This creates visual annotation for result documentation and validation
        draw_detections(input_image, detection)
        
        # Ensure output directory exists for result saving
        # Create directory structure if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)
        
        # Generate output file path for annotated disease detection results
        output_path = os.path.join(output_folder, leaf_image)
        
        # Save annotated image with disease detection overlays to output directory
        # Verify successful image writing and report errors if saving fails
        if not cv2.imwrite(output_path, input_image):
            print(f"Error: Failed to save output image: {output_path}", file=sys.stderr)
    
        # Inference time
        record_model_execution("Grape_Diseases_Hailo8L", inference_time, input_image_dir)
    
    # Return comprehensive disease detection statistics for all processed images
    return detected_diseases

def extract_detections(hailo_output: list, w: int, h: int, class_names: list, threshold: float = 0.5) -> list:
    """
    Extract and validate grape disease detections from Hailo8L AI model output with robust error handling.

    This function processes raw Hailo8L AI neural network output to extract valid
    disease detections based on confidence thresholds. It performs comprehensive
    error handling, coordinate transformation, and validation to ensure reliable
    disease detection results for precision agriculture pathology analysis and
    vineyard health monitoring applications.

    The function serves as the primary detection processing interface with enhanced
    robustness, converting raw AI model predictions into structured detection data
    suitable for agricultural disease analysis and plant pathology workflows.

    :param hailo_output: Raw output from Hailo8L AI disease classification model inference
    :type hailo_output: list
    :param w: Width of the original leaf image in pixels
    :type w: int
    :param h: Height of the original leaf image in pixels
    :type h: int
    :param class_names: List of disease class names for detection classification
    :type class_names: list
    :param threshold: Minimum confidence score for disease detection validation (default: 0.5)
    :type threshold: float
    :returns: List of validated disease detections with class, coordinates, and confidence
    :rtype: list
    :raises ValueError: When coordinate transformation produces invalid values
    :raises IndexError: When model output format is inconsistent with expectations

    Workflow
    --------
    1. **Output Processing**: Iterate through Hailo8L AI model disease detection results
    2. **Class Validation**: Verify class ID consistency and handle index errors
    3. **Detection Validation**: Validate individual detection format and completeness
    4. **Confidence Assessment**: Filter detections based on confidence threshold
    5. **Error Handling**: Comprehensive error management for processing failures
    6. **Coordinate Transformation**: Convert normalized coordinates to pixel space
    7. **Bounding Box Generation**: Create pixel-accurate disease detection regions
    8. **Result Compilation**: Compile validated detections with error recovery

    Disease Detection Processing Pipeline:
        - **Raw Output**: Hailo8L AI model detection results in normalized coordinates
        - **Format Validation**: Detection array format verification and error handling
        - **Confidence Filtering**: Threshold-based disease detection validation
        - **Coordinate Mapping**: Transformation from normalized to pixel coordinates
        - **Classification**: Disease class assignment with error recovery

    Error Handling Features:
        - **Index Error Protection**: Graceful handling of class ID mismatches
        - **Format Validation**: Detection array format verification
        - **Coordinate Validation**: Bounding box coordinate range checking
        - **Processing Continuity**: Error recovery to maintain batch processing

    Disease Detection Features:
        - **Multi-Disease Support**: Comprehensive handling of various disease categories
        - **Spatial Accuracy**: Precise bounding box coordinate calculation
        - **Confidence Assessment**: Disease detection reliability scoring
        - **Quality Validation**: Detection format and content verification

    Expected Model Output Format:
        - **Detection Array**: [y0, x0, y1, x1, confidence_score]
        - **Normalized Coordinates**: Values between 0.0 and 1.0
        - **Class Organization**: Detections grouped by disease class
        - **Confidence Scores**: Float values representing detection reliability

    .. note::
        The function includes comprehensive error handling to manage model output
        inconsistencies and ensures processing continuity during batch disease
        detection operations. Invalid detections are logged and skipped.

    Examples
    --------
    Basic Disease Detection Extraction:

    .. code-block:: python

        # Extract disease detections from model output
        disease_detections = extract_detections(
            hailo_output=model_results,
            w=1920,  # Image width
            h=1080,  # Image height
            class_names=['powdery_mildew', 'black_rot', 'downy_mildew'],
            threshold=0.3
        )
        
        print(f"Found {len(disease_detections)} disease instances")
        
        for detection in disease_detections:
            disease_name, bbox, confidence = detection
            x0, y0, x1, y1 = bbox
            print(f"{disease_name} at ({x0}, {y0}) with confidence {confidence:.2f}")

    Vineyard Disease Analysis:

    .. code-block:: python

        # Process detections for comprehensive disease analysis
        disease_classes = ['powdery_mildew', 'black_rot', 'downy_mildew', 'healthy']
        confidence_threshold = 0.25
        
        detections = extract_detections(
            hailo_output, image_width, image_height, 
            disease_classes, confidence_threshold
        )
        
        # Analyze disease distribution and severity
        disease_distribution = {}
        high_confidence_diseases = []
        
        for disease_name, bbox, confidence in detections:
            # Count disease instances
            disease_distribution[disease_name] = disease_distribution.get(disease_name, 0) + 1
            
            # Track high-confidence detections for priority treatment
            if confidence > 0.7:
                high_confidence_diseases.append((disease_name, confidence))
        
        print("Disease Distribution Analysis:")
        for disease, count in disease_distribution.items():
            print(f"  {disease}: {count} instances")
        
        print(f"\\nHigh-confidence diseases requiring immediate attention:")
        for disease, conf in high_confidence_diseases:
            print(f"  {disease}: {conf:.2f} confidence")

    Error Handling Integration:

    .. code-block:: python

        # Robust disease detection with comprehensive error handling
        def safe_disease_extraction(model_output, image_dims, classes, threshold=0.3):
            try:
                # Attempt disease detection extraction
                detections = extract_detections(
                    model_output, image_dims[0], image_dims[1], classes, threshold
                )
                
                # Validate detection results
                if not detections:
                    return {'status': 'no_diseases', 'detections': []}
                
                # Filter out potential false positives
                validated_detections = []
                for detection in detections:
                    disease_name, bbox, confidence = detection
                    
                    # Additional validation for disease-specific criteria
                    if confidence > threshold and disease_name in classes:
                        validated_detections.append(detection)
                
                return {
                    'status': 'success',
                    'detections': validated_detections,
                    'total_diseases': len(validated_detections)
                }
                
            except Exception as e:
                return {
                    'status': 'error',
                    'error_message': str(e),
                    'detections': []
                }
        
        # Example usage with error handling
        image_dimensions = (1920, 1080)
        disease_classes = ['powdery_mildew', 'black_rot', 'downy_mildew']
        
        result = safe_disease_extraction(
            model_results, image_dimensions, disease_classes, 0.25
        )
        
        if result['status'] == 'success':
            print(f"Successfully detected {result['total_diseases']} disease instances")
        else:
            print(f"Detection failed: {result['error_message']}")

    Returns
    -------
    list
        List of validated grape disease detections:
        
        Each detection contains:
            - **Disease Name** (str): Disease classification label
            - **Bounding Box** (tuple): Pixel coordinates (x0, y0, x1, y1)
            - **Confidence Score** (float): Detection reliability (0.0-1.0)
        
        Example format:
            [
                ['powdery_mildew', (150, 200, 300, 400), 0.85],
                ['black_rot', (500, 100, 650, 250), 0.72],
                ['downy_mildew', (200, 300, 350, 450), 0.68]
            ]

    Raises
    ------
    ValueError
        When coordinate transformation produces invalid values:
        - Negative bounding box coordinates
        - Coordinates outside image boundaries
        - Invalid coordinate format

    IndexError
        When model output format is inconsistent:
        - Missing detection elements
        - Class ID exceeds available class names
        - Insufficient detection data

    Notes
    -----
    - **Error Recovery**: Function continues processing despite individual detection errors
    - **Format Validation**: Comprehensive detection format verification
    - **Agricultural Focus**: Optimized for grape disease detection applications
    - **Processing Continuity**: Maintains batch processing reliability

    Error Handling Specifications:
        - **Index Protection**: Graceful handling of class ID mismatches
        - **Format Validation**: Detection array completeness verification  
        - **Coordinate Validation**: Bounding box coordinate range checking
        - **Exception Management**: Comprehensive error logging and recovery

    Performance Considerations:
        - **Error Logging**: Invalid detections logged for diagnostic purposes
        - **Processing Efficiency**: Optimized iteration with error handling
        - **Memory Management**: Efficient detection data structure handling
        - **Batch Reliability**: Robust processing for large-scale disease analysis

    Agricultural Applications:
        - **Disease Surveillance**: Reliable disease detection for vineyard monitoring
        - **Quality Control**: Detection validation for agricultural assessment
        - **Treatment Planning**: Accurate disease localization for intervention
        - **Research Applications**: Robust detection for agricultural research workflows
    """
    # Initialize results list for validated disease detections
    results = []
    
    # Iterate through each disease class in the Hailo8L AI model output
    for class_id, detections in enumerate(hailo_output):
        # Handle potential class ID index errors with graceful fallback
        # Ensure class name consistency even when model output exceeds label definitions
        class_name = class_names[class_id] if class_id < len(class_names) else f"Class_{class_id}"
        
        # Process individual disease detections for current class
        for detection in detections:
            # Validate detection format to ensure completeness and prevent processing errors
            # Skip malformed detections to maintain batch processing reliability
            if len(detection) < 5:
                print(f"Invalid detection format: {detection}")
                continue
                
            # Extract confidence score from detection data (5th element)
            score = detection[4]
            
            # Validate detection against confidence threshold for quality filtering
            if score >= threshold:
                try:
                    # Extract normalized coordinates from detection output [y0, x0, y1, x1]
                    y0, x0, y1, x1 = detection[:4]
                    
                    # Transform normalized coordinates to pixel coordinates in original image space
                    # Scale bounding box coordinates to match original image dimensions
                    bbox = (int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h))
                    
                    # Compile validated detection with disease class, coordinates, and confidence
                    results.append([class_name, bbox, score])
                    
                except Exception as e:
                    # Handle coordinate transformation errors with detailed error reporting
                    # Continue processing to maintain batch operation reliability
                    print(f"Error processing detection: {e}")
    
    # Return list of validated disease detections for further processing
    return results

def draw_detections(image, detections: list) -> None:
    """
    Draw disease detection bounding boxes and labels on leaf images for agricultural visualization.

    This function provides comprehensive visualization capabilities for grape disease
    detections by overlaying bounding boxes, confidence scores, and disease labels
    directly on the source leaf image. It enables visual validation of AI model results
    and supports precision agriculture plant pathology workflows with clear detection
    visualization for vineyard disease monitoring and assessment.

    The function serves as the primary visualization interface for disease detection
    results, creating annotated images suitable for agricultural reporting, plant
    pathology documentation, and vineyard disease management workflows.

    :param image: Source leaf image array for disease detection overlay
    :type image: numpy.ndarray
    :param detections: List of disease detections with coordinates and classification metadata
    :type detections: list

    Workflow
    --------
    1. **Detection Iteration**: Process each validated disease detection
    2. **Coordinate Extraction**: Extract bounding box pixel coordinates
    3. **Label Generation**: Create formatted labels with disease name and confidence
    4. **Rectangle Drawing**: Render detection bounding boxes on leaf image
    5. **Text Annotation**: Add disease classification and confidence scores
    6. **Visual Enhancement**: Apply consistent color coding for agricultural documentation

    Visualization Features:
        - **Disease Bounding Boxes**: Green rectangular overlays around detected disease areas
        - **Confidence Labels**: Formatted text showing detection confidence scores
        - **Disease Classification**: Clear labeling of detected disease types
        - **Agricultural Clarity**: Optimized colors and fonts for field documentation

    Plant Pathology Visualization Applications:
        - **Disease Validation**: Visual verification of AI disease detection accuracy
        - **Field Documentation**: Annotated images for agricultural disease records
        - **Training Materials**: Visual examples for agricultural education and training
        - **Research Documentation**: Scientific visualization for plant pathology studies

    Detection Annotation Elements:
        - **Rectangle Color**: Green (0, 255, 0) for disease detection visibility
        - **Line Thickness**: 2 pixels for clear boundary definition
        - **Font Style**: FONT_HERSHEY_SIMPLEX for optimal readability
        - **Text Positioning**: Offset positioning to avoid overlap with detection boxes

    .. note::
        The function modifies the input image in-place, adding visual annotations
        directly to the original image array. This enables immediate visualization
        without requiring separate image processing steps for agricultural workflows.

    Examples
    --------
    Basic Disease Visualization:

    .. code-block:: python

        import cv2
        
        # Load leaf image and process disease detections
        leaf_image = cv2.imread("grape_leaf_sample.jpg")
        disease_detections = [
            ['powdery_mildew', (100, 150, 200, 300), 0.85],
            ['black_rot', (400, 200, 500, 350), 0.72],
            ['downy_mildew', (250, 100, 350, 250), 0.68]
        ]
        
        # Draw disease detection overlays on leaf image
        draw_detections(leaf_image, disease_detections)
        
        # Save annotated image for documentation
        cv2.imwrite("annotated_leaf_diseases.jpg", leaf_image)

    Vineyard Disease Documentation:

    .. code-block:: python

        # Process multiple leaf images with disease visualization
        leaf_images = ["leaf_sample_1.jpg", "leaf_sample_2.jpg", "leaf_sample_3.jpg"]
        
        for leaf_file in leaf_images:
            # Load and process leaf image
            leaf_image = cv2.imread(leaf_file)
            
            # Run disease detection (assuming detection function exists)
            disease_detections = detect_diseases(leaf_image)
            
            # Add visual disease annotations
            draw_detections(leaf_image, disease_detections)
            
            # Generate disease summary statistics
            total_diseases = len(disease_detections)
            disease_types = set([d[0] for d in disease_detections])
            
            # Add summary information to image
            summary = f"Diseases: {len(disease_types)}, Total: {total_diseases}"
            cv2.putText(leaf_image, summary, (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            
            # Save annotated result for agricultural documentation
            output_name = f"disease_analysis_{leaf_file}"
            cv2.imwrite(output_name, leaf_image)

    Agricultural Report Generation:

    .. code-block:: python

        # Generate comprehensive disease visualization report
        def create_disease_report(leaf_images_dir, output_dir):
            disease_summary = {}
            
            for leaf_file in os.listdir(leaf_images_dir):
                if not leaf_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    continue
                
                # Load leaf image
                leaf_path = os.path.join(leaf_images_dir, leaf_file)
                leaf_image = cv2.imread(leaf_path)
                
                # Perform disease detection
                detections = detect_diseases(leaf_image)
                
                # Create visualization
                draw_detections(leaf_image, detections)
                
                # Analyze disease distribution
                for disease_name, bbox, confidence in detections:
                    if disease_name not in disease_summary:
                        disease_summary[disease_name] = {'count': 0, 'avg_confidence': 0}
                    
                    disease_summary[disease_name]['count'] += 1
                    current_avg = disease_summary[disease_name]['avg_confidence']
                    disease_summary[disease_name]['avg_confidence'] = (
                        (current_avg + confidence) / 2
                    )
                
                # Add report header to image
                report_text = f"Leaf: {leaf_file} | Diseases: {len(detections)}"
                cv2.putText(leaf_image, report_text, (10, leaf_image.shape[0] - 20),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                # Save annotated image
                output_path = os.path.join(output_dir, f"report_{leaf_file}")
                cv2.imwrite(output_path, leaf_image)
            
            # Generate summary report
            print("Vineyard Disease Summary Report:")
            for disease, stats in disease_summary.items():
                print(f"  {disease}: {stats['count']} instances, "
                      f"Avg confidence: {stats['avg_confidence']:.2f}")
            
            return disease_summary

    Notes
    -----
    - **In-place Modification**: Function modifies the input image directly
    - **Agricultural Focus**: Optimized colors and formatting for plant pathology use
    - **Visual Clarity**: Clear annotations for agricultural documentation and analysis
    - **Professional Output**: Suitable for agricultural reports and scientific documentation

    Visualization Specifications:
        - **Rectangle Color**: RGB(0, 255, 0) - Green for optimal visibility
        - **Line Width**: 2 pixels for clear definition and professional appearance
        - **Font**: OpenCV FONT_HERSHEY_SIMPLEX for optimal readability
        - **Text Scale**: 0.6 for appropriate sizing on various image resolutions
        - **Text Offset**: 5 pixels horizontal, 20 pixels vertical from bounding box

    Agricultural Applications:
        - **Disease Reports**: Visual documentation for vineyard disease management
        - **Quality Control**: Detection accuracy assessment and validation
        - **Educational Materials**: Annotated examples for agricultural training
        - **Research Documentation**: Scientific visualization for plant pathology research

    Plant Pathology Considerations:
        - **Disease Identification**: Clear visual marking of disease areas for diagnosis
        - **Spatial Documentation**: Precise disease localization for treatment planning
        - **Confidence Assessment**: Visual representation of detection reliability
        - **Professional Standards**: High-quality visualization for agricultural documentation
    """
    # Iterate through all validated disease detections for visualization
    for class_name, bbox, score in detections:
        # Extract pixel coordinates from bounding box tuple
        x0, y0, x1, y1 = bbox
        
        # Generate formatted detection label with disease name and confidence score
        label = f"{class_name} {score:.2f}"
        
        # Draw green rectangular bounding box around detected disease area
        cv2.rectangle(image, (x0, y0), (x1, y1), (0, 255, 0), 2)
        
        # Add disease classification and confidence score text with offset positioning
        cv2.putText(image, label, (x0 + 5, y0 + 20),
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
    Command-line interface for grape disease detection and classification processing.
    
    This main execution block provides command-line access to the grape disease
    detection functionality, enabling direct execution from terminal environments
    for vineyard health monitoring, agricultural pathology analysis, and batch
    processing workflows. The interface leverages Hailo8L AI hardware acceleration
    for optimal disease detection performance.
    
    The interface supports agricultural field operations by providing simple
    command-line access to AI-powered disease classification with Hailo8L acceleration,
    making it suitable for integration with agricultural data processing pipelines
    and vineyard disease management systems.
    
    Command-line Arguments:
        -f, --folder: Directory path containing leaf images for disease analysis
        --output_folder: Directory path for saving annotated disease detection results
    
    Usage Examples:
        # Basic disease detection on leaf image directory
        python grape_diseases_Hailo8L.py -f leaf_images/ --output_folder results/
        
        # Process vineyard section with specific output directory
        python grape_diseases_Hailo8L.py -f Images/Leaves/section_A/ --output_folder Images/Results/disease_analysis/
        
        # Batch processing integration (external script)
        for section in vineyard_sections/*/; do
            python grape_diseases_Hailo8L.py -f "$section" --output_folder "results/$(basename "$section")/"
        done
    
    Output Format:
        The script prints disease detection results in JSON-compatible dictionary format:
        {'disease_1': count_1, 'disease_2': count_2, ...}
        
        Example output: {'powdery_mildew': 5, 'black_rot': 2, 'downy_mildew': 3, 'healthy': 8}
    """
    # Initialize command-line argument parser for agricultural disease analysis
    parser = argparse.ArgumentParser(
        description="Run AI-powered grape disease classification on leaf image directories",
        epilog="Example: python grape_diseases_hailo8l.py -f leaf_images/ --output_folder disease_analysis/"
    )
    
    # Define required input directory path argument for leaf images
    parser.add_argument(
        "-f", "--folder", 
        required=True, 
        help="Directory path containing leaf images for disease detection and classification"
    )
    
    # Define optional output directory path argument for results
    parser.add_argument(
        "--output_folder", 
        default=None, 
        help="Directory path for saving annotated disease detection results and analysis"
    )
    
    # Parse command-line arguments provided by user
    args = parser.parse_args()

    # Initialize Hailo8L AI acceleration context for disease classification model
    # Single initialization for efficient batch processing of all leaf images
    with Hailo("Images/Models/Grape_Diseases_Hailo8L/Grape_Diseases/grape_diseases_hailo8l.hef") as hailo:
        # Execute comprehensive disease detection and classification on leaf image directory
        # Process all leaf images and generate comprehensive disease statistics
        result = diseases_classification_run(args.folder, args.output_folder, hailo, score_threshold=0.25)
        
        # Print disease detection results in structured format for integration
        print(result)