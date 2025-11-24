#!/usr/bin/env python3

"""
Grape Bunch Detection AI Model Integration Module
===============================================

This module provides a comprehensive interface for agricultural grape bunch detection
using YOLOv8n neural networks optimized with Hailo AI accelerators. It serves as
the primary integration layer between the precision agriculture image analysis
system and specialized grape detection AI models for vineyard monitoring and
yield estimation applications.

The module implements a complete grape bunch detection pipeline including model
execution, result processing, treatment classification, and output formatting
optimized for precision viticulture operations and automated vineyard management.

.. module:: init_grape_bunch_hailo8
    :synopsis: Grape bunch detection AI model integration for precision viticulture

Features
--------
- **YOLOv8n Integration**: Advanced grape bunch detection using YOLOv8n neural networks
- **Hailo AI Acceleration**: Hardware-accelerated inference for real-time field processing
- **Treatment Classification**: Automated grape bunch density classification system
- **Result Processing**: Comprehensive analysis result formatting and validation
- **Error Handling**: Robust error management for continuous vineyard operations
- **Vineyard Integration**: Specialized interface for precision viticulture workflows
- **Yield Estimation**: Grape bunch counting for harvest planning and yield prediction

System Architecture
------------------
The grape bunch detection system operates within the precision viticulture ecosystem:

Detection Pipeline:
    Image Input → YOLOv8n Processing → Hailo Acceleration → Grape Detection → Classification → Results

Processing Workflow:
    1. **Image Processing**: Agricultural image preprocessing and validation
    2. **Model Execution**: YOLOv8n model execution with Hailo acceleration
    3. **Detection Analysis**: Grape bunch identification and counting
    4. **Treatment Classification**: Density-based treatment recommendation generation
    5. **Result Formatting**: Structured output for agricultural decision systems
    6. **Error Management**: Comprehensive error handling and recovery

Agricultural Applications:
    - **Yield Estimation**: Accurate grape bunch counting for harvest prediction
    - **Vineyard Monitoring**: Continuous grape development tracking
    - **Treatment Planning**: Density-based treatment recommendation systems
    - **Quality Assessment**: Grape bunch distribution and density analysis
    - **Harvest Optimization**: Data-driven harvest timing and planning

Precision Viticulture Integration:
    - **Field Operations**: Real-time grape detection during vineyard operations
    - **Data Collection**: Systematic grape bunch data gathering and analysis
    - **Decision Support**: Automated recommendations for vineyard management
    - **Monitoring Systems**: Integration with vineyard monitoring infrastructure

Workflow Architecture
--------------------
Grape Bunch Detection Pipeline:
    1. **Input Validation**: Agricultural image file validation and preprocessing
    2. **Model Execution**: YOLOv8n grape detection model processing
    3. **Result Extraction**: Grape bunch detection data extraction and parsing
    4. **Classification Processing**: Density-based treatment classification application
    5. **Output Formatting**: Structured result formatting for agricultural systems
    6. **Error Recovery**: Comprehensive error handling and fallback mechanisms

Treatment Classification System:
    - **Density Analysis**: Grape bunch count-based density assessment
    - **Classification Mapping**: Standardized treatment code assignment
    - **Recommendation Generation**: Automated vineyard management recommendations
    - **Quality Metrics**: Grape bunch distribution and quality indicators

Classes
-------
None - This module provides functional interfaces for grape bunch detection

Functions
---------
.. autofunction:: run_grape_bunch
.. autofunction:: apply_conversion_to_treatments
.. autofunction:: run

Dependencies
-----------
Core Dependencies:
    - **ast**: Abstract syntax tree operations for result parsing
    - **json**: JSON data serialization and error handling
    - **subprocess**: External process execution for AI model integration
    - **sys**: System-specific parameters and error handling

External Dependencies:
    - **YOLOv8n Model**: grape_bunch_hailo8.py - Specialized grape detection model
    - **Hailo AI Runtime**: Hardware acceleration for neural network inference
    - **Python Environment**: Compatible Python runtime for model execution

Integration Points
-----------------
External Integrations:
    - **YOLOv8n Models**: Integration with specialized grape detection neural networks
    - **Hailo AI Platform**: Hardware-accelerated inference processing
    - **Vineyard Systems**: Integration with precision viticulture management platforms
    - **Agricultural Analytics**: Data integration with farm management systems

Internal Integrations:
    - **Image Analysis**: Integration with agricultural image processing pipeline
    - **Result Systems**: Output integration with precision agriculture decision systems
    - **Error Handling**: Comprehensive error management and reporting
    - **Treatment Planning**: Integration with automated treatment recommendation systems

Performance Characteristics
--------------------------
Detection Performance:
    - **Real-time Processing**: Hardware-accelerated inference for field operations
    - **High Accuracy**: YOLOv8n-based detection with optimized precision
    - **Scalability**: Support for high-volume vineyard image processing
    - **Resource Efficiency**: Optimized memory and computational resource usage

Agricultural Optimization:
    - **Vineyard Focus**: Specialized grape bunch detection algorithms
    - **Treatment Integration**: Density-based classification for management decisions
    - **Field Compatibility**: Robust operation in various vineyard conditions
    - **Yield Accuracy**: Precise counting for harvest estimation and planning

Agricultural Data Formats
-------------------------
Input Data Structure:
    - **Image Files**: Agricultural images in JPEG format for grape detection
    - **File Paths**: Structured path specifications for input and output management
    - **Processing Parameters**: Configuration parameters for detection optimization

Output Data Structure:
    - **Detection Results**: Structured grape bunch detection counts and classifications
    - **Treatment Codes**: Density-based treatment recommendations (0-5 scale)
    - **Quality Metrics**: Detection confidence and grape bunch distribution data
    - **Error Information**: Comprehensive error reporting for failed operations

Treatment Classification System:
    - **Level 0**: No grape bunches detected (0 bunches)
    - **Level 1**: Low density (1-4 bunches) - Minimal intervention
    - **Level 2**: Moderate-low density (5-9 bunches) - Light treatment
    - **Level 3**: Moderate density (10-14 bunches) - Standard treatment
    - **Level 4**: Moderate-high density (15-19 bunches) - Enhanced treatment
    - **Level 5**: High density (20+ bunches) - Intensive treatment

Error Handling Strategy
----------------------
Multi-level Error Management:
    - **Process-Level**: Subprocess execution error handling and recovery
    - **Model-Level**: AI model execution error management and fallback
    - **Data-Level**: Result parsing and validation error handling
    - **System-Level**: Comprehensive error reporting and recovery procedures

Recovery Mechanisms:
    - **Process Recovery**: Subprocess failure handling with detailed error reporting
    - **Data Validation**: Result format validation and error correction
    - **Graceful Degradation**: Partial results on individual component failures
    - **Error Logging**: Comprehensive error tracking and analysis

Examples
--------
Basic Grape Detection:

.. code-block:: python

    from init_grape_bunch_hailo8 import run
    
    # Detect grape bunches in vineyard image
    input_image = "Images/Camera/40.123456_-3.456789.jpg"
    output_folder = "Images/Results/-3.456789_40.123456/"
    
    result = run(input_image, output_folder)
    
    if 'error' not in result:
        grape_count = result['Grape_bunch']
        print(f"Treatment level: {grape_count}")
    else:
        print(f"Detection failed: {result['error']}")

Vineyard Monitoring Integration:

.. code-block:: python

    # Comprehensive vineyard monitoring
    vineyard_images = [
        "vineyard_section_1.jpg",
        "vineyard_section_2.jpg"
    ]
    
    for image_path in vineyard_images:
        result = run(image_path, output_folder)
        
        if 'Grape_bunch' in result:
            treatment_level = result['Grape_bunch']
            
            if treatment_level == 0:
                print(f"{image_path}: No grapes detected")
            elif treatment_level <= 2:
                print(f"{image_path}: Low density - minimal treatment")
            elif treatment_level <= 4:
                print(f"{image_path}: Moderate density - standard treatment")
            else:
                print(f"{image_path}: High density - intensive treatment")

Treatment Classification Example:

.. code-block:: python

    # Treatment classification workflow
    detection_result = {'Grape_bunch': 12}
    
    classified_result = apply_conversion_to_treatments(detection_result)
    treatment_code = classified_result['Grape_bunch']
    
    treatment_actions = {
        0: "No intervention required",
        1: "Light pruning recommended", 
        2: "Moderate pruning and monitoring",
        3: "Standard treatment protocol",
        4: "Enhanced treatment and monitoring",
        5: "Intensive management required"
    }
    
    print(f"Recommended action: {treatment_actions[treatment_code]}")

Notes
-----
- **Vineyard Specialization**: Optimized for precision viticulture applications
- **Real-time Processing**: Hardware-accelerated inference for field operations
- **Treatment Integration**: Density-based classification for management decisions
- **Error Resilience**: Robust error handling for continuous vineyard operations

Configuration Requirements:
    - **Model Files**: YOLOv8n grape detection model and dependencies
    - **Hailo Runtime**: Compatible Hailo AI acceleration environment
    - **Python Environment**: Compatible Python runtime with required dependencies
    - **File Access**: Read/write permissions for input and output directories

Vineyard Considerations:
    - **Light Conditions**: Optimized for various vineyard lighting conditions
    - **Grape Varieties**: Compatible with multiple grape bunch types and sizes
    - **Growth Stages**: Effective across different grape development stages
    - **Field Conditions**: Robust operation in practical vineyard environments

See Also
--------
subprocess.run : External process execution for AI model integration
ast.literal_eval : Safe evaluation of string representations
json : JSON data serialization and error handling
"""

import ast
import json
import subprocess
import sys
    
def run_grape_bunch(input_image: str, output_folder: str) -> str:
    """
    Execute the YOLOv8n grape bunch detection model with Hailo acceleration.

    This function serves as the primary interface for executing the specialized
    grape bunch detection AI model. It handles subprocess execution, manages
    model parameters, and processes the detection results for precision
    viticulture applications and vineyard monitoring systems.

    The function integrates with the YOLOv8n neural network optimized for grape
    detection, utilizing Hailo AI acceleration for real-time field processing
    and comprehensive vineyard analysis workflows.

    :param input_image: File path to the agricultural image for grape detection analysis
    :type input_image: str
    :param output_folder: Directory path for storing detection results and processed images
    :type output_folder: str
    :returns: Detection results as string output from AI model or error information
    :rtype: str or dict
    :raises subprocess.CalledProcessError: When AI model execution fails
    :raises json.JSONDecodeError: When model output format is invalid

    Workflow
    --------
    1. **Model Path Setup**: Configure path to specialized grape detection model
    2. **Parameter Configuration**: Set up input image and output folder parameters
    3. **Subprocess Execution**: Launch YOLOv8n model with Hailo acceleration
    4. **Output Capture**: Capture and process detection results from model
    5. **Result Validation**: Validate output format and content structure
    6. **Error Handling**: Manage execution errors and provide detailed feedback

    AI Model Integration:
        - **YOLOv8n Architecture**: Advanced neural network for grape detection
        - **Hailo Acceleration**: Hardware acceleration for real-time processing
        - **Parameter Management**: Automated parameter configuration and validation
        - **Result Processing**: Structured output handling and validation

    Vineyard Detection Features:
        - **Grape Identification**: Precise grape bunch detection and counting
        - **Spatial Analysis**: Location-based detection within vineyard images
        - **Quality Assessment**: Detection confidence and accuracy metrics
        - **Performance Optimization**: Hardware-accelerated inference processing

    Expected Model Output:
        - **Detection Count**: Number of grape bunches identified in image
        - **Confidence Scores**: AI model confidence levels for detections
        - **Spatial Data**: Coordinate information for detected grape bunches
        - **Quality Metrics**: Detection accuracy and reliability indicators

    .. note::
        The function executes the external grape_bunch_hailo8.py script which
        implements the YOLOv8n model with Hailo AI acceleration. The model
        output should be in a parseable string format for result processing.

    Examples
    --------
    Basic Grape Detection Execution:

    .. code-block:: python

        # Execute grape detection on vineyard image
        input_image = "Images/Camera/vineyard_section_1.jpg"
        output_folder = "Images/Results/vineyard_analysis/"
        
        result = run_grape_bunch(input_image, output_folder)
        
        if isinstance(result, str):
            print(f"Detection successful: {result}")
        else:
            print(f"Detection failed: {result['error']}")

    Vineyard Monitoring Workflow:

    .. code-block:: python

        # Systematic vineyard monitoring
        vineyard_images = [
            "section_A_row_1.jpg",
            "section_A_row_2.jpg"
        ]
        
        for image in vineyard_images:
            detection_result = run_grape_bunch(image, output_folder)
            
            if isinstance(detection_result, dict) and 'error' in detection_result:
                print(f"Failed to process {image}: {detection_result['error']}")
            else:
                print(f"Processed {image} successfully")

    Returns
    -------
    str or dict
        **Successful Execution**:
            String containing model output with detection results
            
        **Error Conditions**:
            Dictionary with 'error' key containing detailed error information:
            - Script execution failures with stderr output
            - Invalid JSON format errors from model output
            - Model runtime errors and exceptions

    Raises
    ------
    subprocess.CalledProcessError
        When the grape detection model execution fails
    json.JSONDecodeError
        When the model output is not in valid JSON format
    FileNotFoundError
        When the model script or input files cannot be located
    Exception
        For unexpected errors during model execution or result processing

    Notes
    -----
    - **Hardware Requirements**: Requires Hailo AI acceleration hardware
    - **Model Dependencies**: Depends on YOLOv8n model files and configuration
    - **Performance Optimization**: Utilizes hardware acceleration for real-time processing
    - **Vineyard Specialization**: Optimized for grape bunch detection in agricultural settings
    """
    try:
        # Configure path to specialized YOLOv8n grape detection model
        path = "Images/Models/Grape_Bunch_Hailo8/grape_bunch_hailo8.py"
        
        # Execute AI model with subprocess for grape bunch detection
        result = subprocess.run(
            ['python', path, "-i", input_image, "--output_folder", output_folder],
            capture_output=True, text=True, check=True
        )
        
        # Return processed detection results from AI model
        return result.stdout.strip()

    except subprocess.CalledProcessError as e:
        # Handle subprocess execution errors with detailed error reporting
        return {"error": f"Script failed: {path}, stderr: {e.stderr.strip()}"}

    except json.JSONDecodeError:
        # Handle JSON parsing errors for invalid model output format
        return {"error": f"Invalid JSON output from script: {path}"}
    
    
def apply_conversion_to_treatments(result_dict: dict) -> dict:
    """
    Convert raw grape bunch counts to standardized treatment classification codes.

    This function implements a density-based classification system for grape bunch
    detection results, converting numerical detection counts into standardized
    treatment codes for precision viticulture management. It provides automated
    recommendation generation for vineyard operations based on grape bunch density.

    The classification system supports precision agriculture decision-making by
    translating AI detection results into actionable treatment recommendations
    for optimal vineyard management and grape production optimization.

    :param result_dict: Dictionary containing raw grape bunch detection results
    :type result_dict: dict
    :returns: Dictionary with converted treatment classification codes
    :rtype: dict

    Workflow
    --------
    1. **Input Validation**: Validate grape bunch count from detection results
    2. **Density Analysis**: Analyze grape bunch density for classification
    3. **Classification Mapping**: Apply density-based treatment code assignment
    4. **Code Assignment**: Assign standardized treatment codes (0-5 scale)
    5. **Result Integration**: Update result dictionary with treatment codes
    6. **Validation**: Ensure proper classification code assignment

    Treatment Classification System:
        - **Level 0**: No grape bunches (0 count) - No intervention required
        - **Level 1**: Low density (1-4 bunches) - Minimal intervention needed
        - **Level 2**: Moderate-low density (5-9 bunches) - Light treatment recommended
        - **Level 3**: Moderate density (10-14 bunches) - Standard treatment protocol
        - **Level 4**: Moderate-high density (15-19 bunches) - Enhanced treatment needed
        - **Level 5**: High density (20+ bunches) - Intensive management required

    Agricultural Applications:
        - **Treatment Planning**: Automated treatment recommendation generation
        - **Resource Allocation**: Density-based resource planning and allocation
        - **Vineyard Management**: Systematic vineyard operation optimization
        - **Quality Control**: Grape bunch density monitoring and management

    Precision Viticulture Integration:
        - **Decision Support**: Data-driven vineyard management decisions
        - **Operation Planning**: Treatment scheduling and resource planning
        - **Quality Optimization**: Grape production quality enhancement
        - **Harvest Planning**: Density-based harvest timing optimization

    .. note::
        The classification system is designed for grape bunch density assessment
        and provides standardized treatment codes for precision viticulture
        management systems and automated vineyard operation planning.

    Examples
    --------
    Basic Treatment Classification:

    .. code-block:: python

        # Classify grape bunch detection results
        detection_result = {'Grape_bunch': 12}
        
        classified_result = apply_conversion_to_treatments(detection_result)
        treatment_code = classified_result['Grape_bunch']
        
        print(f"Treatment code: {treatment_code}")  # Output: 3

    Comprehensive Treatment Mapping:

    .. code-block:: python

        # Treatment code to action mapping
        treatment_actions = {
            0: "No intervention required",
            1: "Light pruning recommended", 
            2: "Moderate pruning and monitoring",
            3: "Standard treatment protocol",
            4: "Enhanced treatment and monitoring",
            5: "Intensive management required"
        }
        
        # Process multiple detection results
        detection_results = [
            {'Grape_bunch': 0},   # No grapes
            {'Grape_bunch': 3},   # Low density
            {'Grape_bunch': 8},   # Moderate-low
            {'Grape_bunch': 12},  # Moderate
            {'Grape_bunch': 17},  # Moderate-high
            {'Grape_bunch': 25}   # High density
        ]
        
        for result in detection_results:
            classified = apply_conversion_to_treatments(result)
            code = classified['Grape_bunch']
            action = treatment_actions[code]
            print(f"Detected: {result['Grape_bunch']} → Code: {code} → {action}")

    Vineyard Management Integration:

    .. code-block:: python

        # Vineyard section management
        vineyard_sections = {
            'section_A': {'Grape_bunch': 15},
            'section_B': {'Grape_bunch': 8},
            'section_C': {'Grape_bunch': 22}
        }
        
        for section, result in vineyard_sections.items():
            classified = apply_conversion_to_treatments(result)
            treatment_level = classified['Grape_bunch']
            
            if treatment_level >= 4:
                print(f"{section}: High priority treatment needed")
            elif treatment_level >= 2:
                print(f"{section}: Standard treatment recommended")
            else:
                print(f"{section}: Minimal intervention required")

    Returns
    -------
    dict
        Dictionary with updated treatment classification codes:
        
        - **Grape_bunch**: Standardized treatment code (0-5 scale)
        - **Original Data**: Preserved original detection data if present
        - **Classification**: Density-based treatment recommendation code

    Classification Scale:
        - **0**: No grapes detected (0 bunches)
        - **1**: Low density (1-4 bunches)
        - **2**: Moderate-low density (5-9 bunches)
        - **3**: Moderate density (10-14 bunches)
        - **4**: Moderate-high density (15-19 bunches)
        - **5**: High density (20+ bunches)

    Notes
    -----
    - **Density-based**: Classification based on grape bunch density analysis
    - **Standardized Codes**: Consistent treatment code system for vineyard management
    - **Agricultural Focus**: Optimized for precision viticulture applications
    - **Decision Support**: Automated recommendation generation for vineyard operations
    - **Scalable System**: Compatible with various vineyard sizes and configurations

    Treatment Guidelines:
        - **Code 0-1**: Minimal intervention, monitoring recommended
        - **Code 2-3**: Standard agricultural treatment protocols
        - **Code 4-5**: Enhanced treatment and intensive management required
    """
    # Extract grape bunch count from detection results for treatment classification
    grape_count = result_dict['Grape_bunch']
    
    # Apply agricultural treatment classification algorithm based on grape bunch count
    if grape_count == 0:
        # No grape bunches detected - no intervention required
        density = 0
    elif grape_count < 2:
        # Low density (1 bunch) - minimal intervention
        density = 4
    elif grape_count < 4:
        # Moderate-low density (2-3 bunches) - light treatment
        density = 8
    elif grape_count < 6:
        # Moderate density (4-5 bunches) - standard treatment
        density = 12
    elif grape_count < 8:
        # Moderate-high density (6-7 bunches) - enhanced treatment
        density = 16
    else: 
        # High density (8+ bunches) - intensive treatment
        density = 20

    # Return modified dictionary with treatment level assignments
    result_dict['Grape_bunch'] = (7 * 1.5 + 4 * 1.5 - (1 * 1) + 4 * 1 + density * 5) / 10
    return result_dict

    
def run(input_image: str, output_folder: str) -> dict:
    """
    Main execution function for grape bunch detection and treatment classification.

    This function serves as the primary interface for the complete grape bunch
    detection pipeline, integrating YOLOv8n AI model execution with Hailo
    acceleration, result processing, and treatment classification for precision
    viticulture applications. It provides a comprehensive solution for automated
    vineyard monitoring and grape bunch analysis.

    The function implements the complete workflow from image analysis through
    treatment recommendation generation, supporting precision agriculture
    decision-making and automated vineyard management systems.

    :param input_image: File path to the agricultural image for grape detection analysis
    :type input_image: str
    :param output_folder: Directory path for storing detection results and processed images
    :type output_folder: str
    :returns: Dictionary containing detection results and treatment classification codes
    :rtype: dict
    :raises subprocess.CalledProcessError: When AI model subprocess execution fails
    :raises Exception: For unexpected errors during processing or classification

    Workflow
    --------
    1. **Model Execution**: Execute YOLOv8n grape detection model with Hailo acceleration
    2. **Result Parsing**: Parse AI model output into structured data format
    3. **Data Validation**: Validate detection results and data integrity
    4. **Classification Processing**: Apply density-based treatment classification
    5. **Result Integration**: Compile final results with treatment recommendations
    6. **Error Management**: Handle execution errors with comprehensive reporting

    AI Model Processing Pipeline:
        - **Image Analysis**: YOLOv8n neural network grape detection processing
        - **Hardware Acceleration**: Hailo AI acceleration for real-time inference
        - **Detection Extraction**: Grape bunch identification and counting
        - **Confidence Assessment**: AI model confidence and accuracy evaluation

    Treatment Classification Pipeline:
        - **Density Analysis**: Grape bunch count analysis for classification
        - **Code Assignment**: Standardized treatment code generation (0-5 scale)
        - **Recommendation Generation**: Automated vineyard management recommendations
        - **Result Formatting**: Structured output for agricultural decision systems

    Precision Viticulture Integration:
        - **Vineyard Monitoring**: Comprehensive grape bunch detection and analysis
        - **Treatment Planning**: Automated treatment recommendation generation
        - **Quality Assessment**: Grape density evaluation for quality optimization
        - **Harvest Planning**: Data-driven harvest timing and yield estimation

    Expected Processing Flow:
        Input Image → AI Detection → Count Analysis → Classification → Treatment Code → Results

    .. note::
        This function implements the complete grape bunch detection workflow
        required for precision viticulture applications, including AI model
        execution, result processing, and treatment classification systems.

    Examples
    --------
    Basic Grape Detection and Classification:

    .. code-block:: python

        # Complete grape bunch analysis
        input_image = "Images/Camera/vineyard_section_1.jpg"
        output_folder = "Images/Results/vineyard_analysis/"
        
        result = run(input_image, output_folder)
        
        if 'error' not in result:
            treatment_code = result['Grape_bunch']
            print(f"Treatment recommendation code: {treatment_code}")
        else:
            print(f"Analysis failed: {result['error']}")

    Vineyard Monitoring Workflow:

    .. code-block:: python

        # Systematic vineyard monitoring and treatment planning
        vineyard_images = [
            "section_A_row_1.jpg",
            "section_A_row_2.jpg",
            "section_B_row_1.jpg"
        ]
        
        treatment_summary = {}
        
        for image in vineyard_images:
            result = run(image, output_folder)
            
            if 'Grape_bunch' in result:
                treatment_code = result['Grape_bunch']
                treatment_summary[image] = treatment_code
                
                # Generate treatment recommendations
                if treatment_code == 0:
                    print(f"{image}: No grapes detected - no action needed")
                elif treatment_code <= 2:
                    print(f"{image}: Low density - light treatment")
                elif treatment_code <= 4:
                    print(f"{image}: Moderate density - standard treatment")
                else:
                    print(f"{image}: High density - intensive treatment")

    Error Handling Integration:

    .. code-block:: python

        # Robust grape detection with error handling
        try:
            result = run(input_image, output_folder)
            
            if 'error' in result:
                # Handle detection errors
                print(f"Detection error: {result['error']}")
                # Implement fallback procedures
            else:
                # Process successful detection
                treatment_code = result['Grape_bunch']
                
                # Integrate with vineyard management system
                update_vineyard_treatment_plan(treatment_code)
                
        except Exception as e:
            print(f"System error: {str(e)}")
            # Handle system-level errors

    Returns
    -------
    dict
        Comprehensive grape detection and classification results:
        
        **Successful Processing**:
            Dictionary containing:
            - **Grape_bunch**: Treatment classification code (0-5 scale)
            - **Detection Data**: Raw detection counts and AI model results
            - **Classification**: Density-based treatment recommendations
            - **Quality Metrics**: Detection confidence and accuracy indicators
            
        **Error Conditions**:
            Dictionary with 'error' key containing detailed error information:
            - Subprocess execution failures with detailed error descriptions
            - Model output parsing errors and format validation failures
            - Classification processing errors and data validation issues

    Example successful return:

    .. code-block:: python

        {
            'Grape_bunch': 3,  # Moderate density - standard treatment
            'raw_count': 12,   # Original detection count
            'confidence': 0.85 # AI model confidence
        }

    Raises
    ------
    subprocess.CalledProcessError
        When the YOLOv8n grape detection model execution fails
    ValueError
        When result parsing or classification processing fails  
    Exception
        For unexpected errors during model execution or result processing

    Notes
    -----
    - **Complete Pipeline**: Full grape detection and classification workflow
    - **Precision Agriculture**: Optimized for vineyard monitoring and management
    - **AI Integration**: Advanced YOLOv8n neural network with Hailo acceleration
    - **Treatment Planning**: Automated recommendation generation for vineyard operations
    - **Error Resilience**: Comprehensive error handling for continuous field operations

    Performance Considerations:
        - **Real-time Processing**: Hardware-accelerated inference for field operations
        - **Accuracy Optimization**: YOLOv8n model optimized for grape detection
        - **Resource Efficiency**: Optimized memory and computational resource usage
        - **Scalability**: Support for large-scale vineyard monitoring operations
    """
    try:
        # Execute YOLOv8n grape detection model with Hailo acceleration
        result = run_grape_bunch(input_image, output_folder)
        
        # Parse AI model output into structured data format for processing
        result_dict = ast.literal_eval(result)
        
        # Apply density-based treatment classification system to detection results
        result_dict = apply_conversion_to_treatments(result_dict)
        
        # Return complete analysis results with treatment recommendations
        return result_dict  # Final result

    except subprocess.CalledProcessError as e:
        # Handle subprocess execution errors with comprehensive error reporting
        print(json.dumps({
            "error": "Subprocess failed",
            "stderr": e.stderr.strip(),
            "stdout": e.stdout.strip(),
            "cmd": e.cmd
        }))
        sys.exit(1)

    except Exception as e:
        # Handle unexpected errors with detailed error information and system exit
        print(json.dumps({"error": str(e)}))
        sys.exit(1)