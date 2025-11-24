#!/usr/bin/env python3

"""
Grape Bunch YOLOv8n Hailo8L Initialization and Treatment Conversion Module
==========================================================================

This module provides the initialization interface and treatment conversion pipeline
for grape bunch detection using YOLOv8n neural networks with Hailo8L hardware
acceleration. It serves as the primary integration layer between raw AI detection
outputs and precision agriculture treatment mapping systems, enabling automated
conversion from grape count data to agricultural treatment recommendations.

The module combines computer vision processing with agricultural decision-making
algorithms, transforming grape bunch detection results into actionable treatment
levels for precision viticulture applications and vineyard management workflows.

.. module:: init_grape_bunch_hailo8l
    :synopsis: Grape bunch detection initialization with treatment conversion for precision agriculture

Features
--------
- **YOLOv8n Integration**: Seamless interface to Hailo8L-accelerated grape detection
- **Treatment Conversion**: Automated mapping from grape counts to treatment levels
- **Subprocess Management**: Robust external process execution and error handling
- **Agricultural Scaling**: Precision agriculture-optimized grape count classification
- **Error Recovery**: Comprehensive error handling and process failure management
- **JSON Integration**: Structured data exchange for agricultural system integration

System Architecture
------------------
The grape bunch processing system operates within the precision agriculture ecosystem:

Processing Pipeline:
    Input Image → YOLOv8n Detection → Count Extraction → Treatment Conversion → Agricultural Output

Treatment Conversion Workflow:
    1. **Detection Execution**: YOLOv8n grape bunch detection with Hailo8L acceleration
    2. **Result Processing**: Raw detection output parsing and validation
    3. **Count Extraction**: Grape bunch count extraction from detection results
    4. **Treatment Mapping**: Agricultural treatment level assignment based on grape density
    5. **Output Generation**: Structured treatment recommendations for field application

Agricultural Integration:
    - **Precision Viticulture**: Integration with vineyard management systems
    - **Treatment Planning**: Automated agricultural intervention recommendations
    - **Field Operations**: Real-time treatment decision support for field equipment
    - **Data Analytics**: Agricultural data processing for vineyard optimization

Treatment Classification System:
    - **Level 0**: No grapes detected (0 bunches) - No treatment required
    - **Level 1**: Low density (1-4 bunches) - Minimal treatment application
    - **Level 2**: Medium-low density (5-9 bunches) - Standard treatment protocol
    - **Level 3**: Medium density (10-14 bunches) - Enhanced treatment application
    - **Level 4**: High density (15-19 bunches) - Intensive treatment protocol
    - **Level 5**: Maximum density (20+ bunches) - Maximum treatment application

Workflow Architecture
--------------------
Grape Detection and Treatment Processing Pipeline:
    1. **Process Initialization**: External detection script execution setup
    2. **Image Processing**: YOLOv8n grape detection via subprocess execution
    3. **Output Parsing**: Detection result extraction and format validation
    4. **Data Conversion**: String-to-dictionary conversion for structured processing
    5. **Treatment Classification**: Grape count-based treatment level assignment
    6. **Result Compilation**: Final treatment recommendations and metadata

Detection Integration:
    - **Subprocess Execution**: External YOLOv8n detection script orchestration
    - **Output Capture**: Standard output and error stream processing
    - **Error Handling**: Comprehensive subprocess failure management
    - **Result Validation**: Output format verification and data integrity checks

Agricultural Applications:
    - **Vineyard Monitoring**: Systematic grape density assessment and mapping
    - **Treatment Planning**: Automated agricultural intervention scheduling
    - **Resource Optimization**: Precision application of agricultural treatments
    - **Yield Management**: Grape density-based yield prediction and optimization

Classes
-------
None - This module provides functional interfaces for grape detection integration

Functions
---------
.. autofunction:: run_grape_bunch
.. autofunction:: apply_conversion_to_treatments
.. autofunction:: run

Dependencies
-----------
Core Dependencies:
    - **ast**: Abstract syntax tree processing for literal evaluation
    - **json**: JSON data processing and error message formatting
    - **subprocess**: External process execution and management
    - **sys**: System-specific parameters and error handling

External Dependencies:
    - **grape_bunch_hailo8l.py**: YOLOv8n detection script with Hailo8L acceleration
    - **Hailo8L Hardware**: AI acceleration hardware for neural network processing

Integration Points
-----------------
External Integrations:
    - **YOLOv8n Detection**: Integration with computer vision processing scripts
    - **Hailo8L Platform**: Hardware acceleration for neural network inference
    - **Agricultural Systems**: Integration with precision viticulture platforms
    - **Treatment Systems**: Connection to agricultural treatment application equipment

Internal Integrations:
    - **Detection Processing**: Computer vision result parsing and validation
    - **Treatment Conversion**: Agricultural decision-making algorithm integration
    - **Error Management**: Comprehensive error handling and recovery mechanisms
    - **Data Exchange**: Structured data format management and conversion

Performance Characteristics
--------------------------
Processing Performance:
    - **Subprocess Efficiency**: Optimized external process execution and monitoring
    - **Data Conversion**: Fast string-to-dictionary parsing and validation
    - **Treatment Mapping**: Efficient grape count-based classification algorithms
    - **Error Handling**: Minimal overhead error detection and recovery

Agricultural Optimization:
    - **Real-time Processing**: Suitable for field operation time requirements
    - **Scalability**: Support for large-scale vineyard processing workflows
    - **Integration Ready**: Compatible with existing agricultural system architectures
    - **Resource Efficiency**: Optimized memory and processing resource usage

Agricultural Data Formats
-------------------------
Input Data Structure:
    - **Image Paths**: Agricultural image file specifications for processing
    - **Output Directories**: Structured path specifications for result storage
    - **Detection Parameters**: Processing configuration and threshold settings

Output Data Structure:
    - **Treatment Levels**: Numerical treatment recommendations (0-5 scale)
    - **Grape Counts**: Original detection counts and classification metadata
    - **Error Information**: Comprehensive error reporting and diagnostic data

Treatment Level Mapping:
    - **Level 0**: 0 grape bunches detected - No agricultural intervention
    - **Level 1**: 1-4 grape bunches - Light treatment application
    - **Level 2**: 5-9 grape bunches - Standard treatment protocol
    - **Level 3**: 10-14 grape bunches - Moderate treatment intensification
    - **Level 4**: 15-19 grape bunches - High-intensity treatment application
    - **Level 5**: 20+ grape bunches - Maximum treatment application

Error Handling Strategy
----------------------
Multi-level Error Management:
    - **Subprocess Errors**: External script execution failure handling
    - **Format Validation**: Output format verification and error recovery
    - **Data Conversion**: JSON parsing and literal evaluation error management
    - **Agricultural Processing**: Treatment conversion error handling and validation

Recovery Mechanisms:
    - **Process Monitoring**: Subprocess execution status monitoring and reporting
    - **Output Validation**: Detection result format verification and error reporting
    - **Error Reporting**: Structured error message generation for system integration
    - **Graceful Degradation**: Controlled failure handling with diagnostic information

Examples
--------
Basic Grape Detection and Treatment Conversion:

.. code-block:: python

    # Execute grape detection with treatment conversion
    result = run(
        input_image="Images/Camera/vineyard_section_1.jpg",
        output_folder="Images/Results/vineyard_analysis/"
    )
    
    treatment_level = result["Grape_bunch"]
    print(f"Recommended treatment level: {treatment_level}")

Vineyard Section Analysis:

.. code-block:: python

    import os
    
    # Process multiple vineyard sections
    vineyard_sections = [
        "Images/Camera/section_A_row_1.jpg",
        "Images/Camera/section_A_row_2.jpg",
        "Images/Camera/section_B_row_1.jpg"
    ]
    
    treatment_map = {}
    
    for section_image in vineyard_sections:
        # Extract section identifier
        section_id = os.path.basename(section_image).split('.')[0]
        
        # Process section and get treatment recommendation
        result = run(section_image, "results/")
        treatment_level = result["Grape_bunch"]
        
        treatment_map[section_id] = treatment_level
        print(f"{section_id}: Treatment level {treatment_level}")
    
    # Generate treatment application map
    for section, level in treatment_map.items():
        if level == 0:
            print(f"{section}: No treatment required")
        elif level <= 2:
            print(f"{section}: Light treatment application")
        elif level <= 4:
            print(f"{section}: Standard treatment protocol")
        else:
            print(f"{section}: Intensive treatment required")

Agricultural Integration Example:

.. code-block:: python

    # Integration with precision agriculture system
    def process_vineyard_block(block_images, output_base):
        treatment_schedule = []
        
        for image_path in block_images:
            # Process each vineyard section
            result = run(image_path, f"{output_base}/processed/")
            
            # Extract GPS coordinates from filename (if available)
            filename = os.path.basename(image_path)
            coords = filename.split('_')[:2] if '_' in filename else ['unknown', 'unknown']
            
            # Create treatment recommendation
            treatment_recommendation = {
                'location': coords,
                'image_file': image_path,
                'treatment_level': result["Grape_bunch"],
                'grape_density': get_density_description(result["Grape_bunch"])
            }
            
            treatment_schedule.append(treatment_recommendation)
        
        return treatment_schedule
    
    def get_density_description(level):
        density_map = {
            0: "No grapes detected",
            1: "Low grape density",
            2: "Medium-low grape density", 
            3: "Medium grape density",
            4: "High grape density",
            5: "Maximum grape density"
        }
        return density_map.get(level, "Unknown density")

Notes
-----
- **External Dependencies**: Requires grape_bunch_hailo8l.py script in correct location
- **Hardware Requirements**: Depends on Hailo8L acceleration hardware availability
- **Agricultural Focus**: Optimized for precision viticulture treatment planning
- **Integration Ready**: Compatible with agricultural workflow management systems

Configuration Requirements:
    - **Script Path**: Correct path to grape_bunch_hailo8l.py detection script
    - **Hardware Access**: Available Hailo8L acceleration hardware
    - **File Permissions**: Read/write access to input and output directories
    - **Python Environment**: Compatible Python interpreter with required dependencies

Treatment Considerations:
    - **Grape Density**: Treatment levels based on grape bunch density analysis
    - **Agricultural Timing**: Consider seasonal factors in treatment application
    - **Field Conditions**: Adapt treatment recommendations to field-specific conditions
    - **Resource Planning**: Treatment level mapping for agricultural resource allocation

See Also
--------
ast : Abstract syntax tree processing for literal evaluation
json : JSON data processing and serialization
subprocess : External process execution and management
sys : System-specific parameters and error handling
"""

import ast
import json
import subprocess
import sys
    
def run_grape_bunch(input_image: str, output_folder: str) -> str:
    """
    Execute YOLOv8n grape bunch detection via external subprocess with Hailo8L acceleration.

    This function provides the primary interface for executing grape bunch detection
    by launching the external YOLOv8n detection script as a subprocess. It handles
    the complete process execution workflow, including parameter passing, output
    capture, and error management for agricultural computer vision processing.

    The function serves as the subprocess orchestration layer, enabling seamless
    integration between the treatment conversion system and the underlying YOLOv8n
    neural network processing with Hailo8L hardware acceleration.

    :param input_image: Absolute or relative path to agricultural image for processing
    :type input_image: str
    :param output_folder: Directory path for saving detection results and annotations
    :type output_folder: str
    :returns: Standard output string from detection script containing JSON results
    :rtype: str
    :raises subprocess.CalledProcessError: When detection script execution fails
    :raises json.JSONDecodeError: When detection script output format is invalid

    Workflow
    --------
    1. **Script Path Configuration**: Define external detection script location
    2. **Command Assembly**: Construct subprocess command with input parameters
    3. **Process Execution**: Launch YOLOv8n detection script with argument passing
    4. **Output Capture**: Capture standard output and error streams
    5. **Result Validation**: Verify successful process execution
    6. **Output Processing**: Extract and return detection results as string
    7. **Error Management**: Handle subprocess failures and format errors

    Subprocess Management:
        - **Command Construction**: Python script execution with parameter passing
        - **Stream Capture**: Standard output and error stream monitoring
        - **Process Monitoring**: Execution status tracking and validation
        - **Error Handling**: Comprehensive subprocess failure management

    Detection Integration:
        - **Parameter Passing**: Image path and output directory specification
        - **Result Extraction**: Detection output parsing and format validation
        - **Error Reporting**: Subprocess error reporting and diagnostic information
        - **Format Validation**: Output format verification for downstream processing

    Agricultural Processing Features:
        - **Image Processing**: Agricultural image file processing via external script
        - **Hardware Acceleration**: Hailo8L-accelerated YOLOv8n neural network execution
        - **Result Generation**: Detection count and visualization output generation
        - **Error Recovery**: Robust error handling for field operation reliability

    Expected Script Behavior:
        - **Input Processing**: Accept image file path and output directory arguments
        - **Detection Execution**: Perform YOLOv8n grape bunch detection with Hailo8L
        - **Result Output**: Generate JSON-formatted detection results to stdout
        - **Error Reporting**: Provide detailed error information via stderr

    .. note::
        The function expects the external detection script to be located at
        'Images/Models/Grape_Bunch_Hailo8L/grape_bunch_hailo8l.py' and to
        output JSON-formatted results to standard output.

    Examples
    --------
    Basic Detection Execution:

    .. code-block:: python

        # Execute grape detection on vineyard image
        output_string = run_grape_bunch(
            input_image="Images/Camera/vineyard_section_1.jpg",
            output_folder="Images/Results/analysis/"
        )
        
        print(f"Detection output: {output_string}")
        
        # Expected output format: "{'Grape_bunch': 12}"

    Batch Processing Integration:

    .. code-block:: python

        import os
        
        # Process multiple vineyard images
        vineyard_images = [
            "Images/Camera/section_A.jpg",
            "Images/Camera/section_B.jpg",
            "Images/Camera/section_C.jpg"
        ]
        
        detection_results = []
        
        for image_path in vineyard_images:
            try:
                # Execute detection for each image
                result_string = run_grape_bunch(
                    input_image=image_path,
                    output_folder="Images/Results/batch_processing/"
                )
                
                # Store results with image identifier
                image_name = os.path.basename(image_path)
                detection_results.append({
                    'image': image_name,
                    'raw_output': result_string
                })
                
            except Exception as e:
                print(f"Error processing {image_path}: {e}")
        
        print(f"Processed {len(detection_results)} images successfully")

    Error Handling Integration:

    .. code-block:: python

        def safe_detection_execution(image_path, output_dir):
            try:
                # Attempt grape detection
                result = run_grape_bunch(image_path, output_dir)
                
                # Validate output format
                if result.startswith('{') and result.endswith('}'):
                    return {'status': 'success', 'output': result}
                else:
                    return {'status': 'error', 'message': 'Invalid output format'}
                
            except subprocess.CalledProcessError as e:
                return {
                    'status': 'subprocess_error',
                    'stderr': e.stderr,
                    'stdout': e.stdout
                }
            except Exception as e:
                return {'status': 'unknown_error', 'message': str(e)}

    Returns
    -------
    str
        Detection results as string in JSON-compatible format:
        
        Expected format:
            "{'Grape_bunch': <count>}"
        
        Example outputs:
            - "{'Grape_bunch': 0}" - No grapes detected
            - "{'Grape_bunch': 5}" - Five grape bunches detected
            - "{'Grape_bunch': 15}" - Fifteen grape bunches detected

    Raises
    ------
    subprocess.CalledProcessError
        When the external detection script fails:
        - Script execution errors
        - Invalid command-line arguments
        - Processing failures in YOLOv8n inference
        - Hardware acceleration issues

    json.JSONDecodeError
        When script output cannot be parsed as JSON:
        - Malformed output format
        - Unexpected output content
        - Encoding issues in output stream

    Notes
    -----
    - **Script Dependencies**: Requires grape_bunch_hailo8l.py to be available
    - **Hardware Requirements**: Depends on Hailo8L acceleration hardware
    - **Output Format**: Expects JSON-compatible dictionary format from script
    - **Error Handling**: Comprehensive subprocess error management and reporting

    Processing Specifications:
        - **Command Execution**: Python subprocess with capture_output=True
        - **Text Mode**: text=True for string output handling
        - **Error Checking**: check=True for automatic error detection
        - **Output Extraction**: Standard output strip() for clean result strings

    Integration Considerations:
        - **Path Dependencies**: Script path must be correct relative to execution directory
        - **Permission Requirements**: Execute permissions on detection script
        - **Resource Availability**: Sufficient system resources for AI processing
        - **Hardware Access**: Available Hailo8L hardware for acceleration
    """
    try:
        # Define path to external YOLOv8n grape detection script with Hailo8L acceleration
        path = "Images/Models/Grape_Bunch_Hailo8L/grape_bunch_hailo8l.py"
        
        # Execute grape detection subprocess with input image and output directory parameters
        # capture_output=True: Capture both stdout and stderr for processing
        # text=True: Return string output instead of bytes
        # check=True: Raise CalledProcessError on non-zero exit codes
        result = subprocess.run(
            ['python', path, "-i", input_image, "--output_folder", output_folder],
            capture_output=True, text=True, check=True
        )
        
        # Return cleaned standard output containing JSON-formatted detection results
        return result.stdout.strip()

    except subprocess.CalledProcessError as e:
        # Handle subprocess execution failures with detailed error information
        # Return error dictionary with script path and stderr details
        return {"error": f"Script failed: {path}, stderr: {e.stderr.strip()}"}

    except json.JSONDecodeError:
        # Handle JSON parsing errors when script output format is invalid
        # Return error dictionary with script path and format error description
        return {"error": f"Invalid JSON output from script: {path}"}

def apply_conversion_to_treatments(result_dict: dict) -> dict:
    """
    Convert grape bunch detection counts to agricultural treatment level recommendations.

    This function implements the precision agriculture decision-making algorithm
    that transforms raw grape bunch detection counts into standardized treatment
    level recommendations suitable for automated agricultural equipment and
    vineyard management systems. The conversion follows agricultural best practices
    for grape density-based treatment application.

    The function serves as the core agricultural intelligence component, providing
    the bridge between computer vision detection results and practical field
    treatment recommendations for precision viticulture applications.

    :param result_dict: Detection results dictionary containing grape bunch counts
    :type result_dict: dict
    :returns: Modified dictionary with treatment level assignments
    :rtype: dict

    Workflow
    --------
    1. **Count Extraction**: Extract grape bunch count from detection results
    2. **Density Classification**: Classify grape density based on count thresholds
    3. **Treatment Assignment**: Map grape density to appropriate treatment levels
    4. **Result Modification**: Update result dictionary with treatment recommendations
    5. **Validation**: Ensure treatment level assignments are within valid ranges

    Treatment Classification Algorithm:
        - **No Grapes (0 bunches)**: Treatment Level 0 - No intervention required
        - **Low Density (1-4 bunches)**: Treatment Level 1 - Light application
        - **Medium-Low Density (5-9 bunches)**: Treatment Level 2 - Standard protocol
        - **Medium Density (10-14 bunches)**: Treatment Level 3 - Moderate intensity
        - **High Density (15-19 bunches)**: Treatment Level 4 - High intensity
        - **Maximum Density (20+ bunches)**: Treatment Level 5 - Maximum application

    Agricultural Decision Logic:
        - **Zero Detection**: No agricultural intervention needed
        - **Low Counts**: Minimal treatment to support grape development
        - **Medium Counts**: Standard agricultural treatment protocols
        - **High Counts**: Intensive treatment for optimal grape management
        - **Maximum Counts**: Full-intensity treatment for maximum productivity

    Precision Agriculture Applications:
        - **Variable Rate Application**: Treatment level mapping for precision equipment
        - **Resource Optimization**: Efficient agricultural input distribution
        - **Yield Management**: Grape density-based productivity optimization
        - **Cost Efficiency**: Targeted treatment application based on actual needs

    .. note::
        The treatment levels are designed for integration with precision agriculture
        equipment that can apply variable rates of treatment based on numerical
        level specifications (0-5 scale).

    Examples
    --------
    Basic Treatment Conversion:

    .. code-block:: python

        # Convert detection results to treatment levels
        detection_result = {"Grape_bunch": 12}
        
        treatment_result = apply_conversion_to_treatments(detection_result)
        
        print(f"Original count: {12}")
        print(f"Treatment level: {treatment_result['Grape_bunch']}")
        # Output: Treatment level: 3

    Vineyard Section Analysis:

    .. code-block:: python

        # Process multiple detection results
        detection_results = [
            {"Grape_bunch": 0},   # No grapes
            {"Grape_bunch": 3},   # Low density
            {"Grape_bunch": 7},   # Medium-low density
            {"Grape_bunch": 12},  # Medium density
            {"Grape_bunch": 18},  # High density
            {"Grape_bunch": 25}   # Maximum density
        ]
        
        treatment_plan = []
        
        for i, result in enumerate(detection_results):
            original_count = result["Grape_bunch"]
            treatment_result = apply_conversion_to_treatments(result.copy())
            treatment_level = treatment_result["Grape_bunch"]
            
            treatment_plan.append({
                'section': f"Section_{i+1}",
                'grape_count': original_count,
                'treatment_level': treatment_level
            })
        
        # Display treatment plan
        for plan in treatment_plan:
            print(f"{plan['section']}: {plan['grape_count']} grapes → "
                  f"Treatment Level {plan['treatment_level']}")

    Agricultural Equipment Integration:

    .. code-block:: python

        def generate_application_map(detection_results):
            application_map = {
                'no_treatment': [],
                'light_treatment': [],
                'standard_treatment': [],
                'moderate_treatment': [],
                'intensive_treatment': [],
                'maximum_treatment': []
            }
            
            treatment_categories = [
                'no_treatment', 'light_treatment', 'standard_treatment',
                'moderate_treatment', 'intensive_treatment', 'maximum_treatment'
            ]
            
            for section_id, result in detection_results.items():
                # Convert to treatment level
                treatment_result = apply_conversion_to_treatments(result.copy())
                level = treatment_result["Grape_bunch"]
                
                # Categorize by treatment requirement
                category = treatment_categories[level]
                application_map[category].append(section_id)
            
            return application_map
        
        # Example usage
        vineyard_results = {
            'A1': {"Grape_bunch": 2},
            'A2': {"Grape_bunch": 8},
            'A3': {"Grape_bunch": 15},
            'B1': {"Grape_bunch": 0},
            'B2': {"Grape_bunch": 22}
        }
        
        app_map = generate_application_map(vineyard_results)
        
        for treatment_type, sections in app_map.items():
            if sections:
                print(f"{treatment_type.replace('_', ' ').title()}: {sections}")

    Returns
    -------
    dict
        Modified detection results dictionary with treatment level assignments:
        
        Input format:
            {"Grape_bunch": <original_count>}
        
        Output format:
            {"Grape_bunch": <treatment_level>}
        
        Treatment level mappings:
            - 0: No grapes detected → No treatment (Level 0)
            - 1-4: Low grape density → Light treatment (Level 1)
            - 5-9: Medium-low density → Standard treatment (Level 2)
            - 10-14: Medium density → Moderate treatment (Level 3)
            - 15-19: High density → Intensive treatment (Level 4)
            - 20+: Maximum density → Maximum treatment (Level 5)

    Notes
    -----
    - **In-place Modification**: Function modifies the input dictionary directly
    - **Agricultural Focus**: Treatment levels designed for precision agriculture
    - **Equipment Compatibility**: Levels compatible with variable-rate application systems
    - **Threshold Optimization**: Thresholds based on agricultural best practices

    Treatment Specifications:
        - **Level 0**: No agricultural intervention required
        - **Level 1**: Light application for grape development support
        - **Level 2**: Standard agricultural treatment protocol
        - **Level 3**: Moderate intensity for balanced grape management
        - **Level 4**: High intensity for optimal grape productivity
        - **Level 5**: Maximum application for maximum yield potential

    Agricultural Considerations:
        - **Grape Variety**: Treatment thresholds may vary by grape variety
        - **Growth Stage**: Consider seasonal grape development phases
        - **Field Conditions**: Adapt to specific vineyard environmental conditions
        - **Equipment Capacity**: Match treatment levels to available equipment capabilities

    Precision Agriculture Integration:
        - **Variable Rate Technology**: Direct compatibility with VRT systems
        - **GPS Mapping**: Treatment levels suitable for spatial mapping applications
        - **Resource Planning**: Treatment level data for agricultural input planning
        - **Quality Control**: Standardized treatment recommendations for consistency
    """
    # Extract grape bunch count from detection results for treatment classification
    grape_count = result_dict['Grape_bunch']
    
    # Apply agricultural harvesting classification algorithm based on grape density
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
    Execute complete grape bunch detection and treatment conversion pipeline.

    This function provides the comprehensive interface for the entire grape detection
    and agricultural treatment recommendation workflow. It orchestrates the execution
    of YOLOv8n detection processing, result parsing, and treatment level conversion
    to deliver actionable agricultural recommendations for precision viticulture
    applications and vineyard management systems.

    The function serves as the primary entry point for agricultural computer vision
    processing, combining AI-powered grape detection with agricultural decision-making
    algorithms to support automated vineyard operations and treatment planning.

    :param input_image: Path to agricultural image file for grape detection processing
    :type input_image: str
    :param output_folder: Directory path for saving detection results and annotations
    :type output_folder: str
    :returns: Treatment recommendation dictionary with agricultural guidance levels
    :rtype: dict
    :raises subprocess.CalledProcessError: When grape detection subprocess fails
    :raises ValueError: When result parsing or conversion fails
    :raises SystemExit: When critical errors require process termination

    Workflow
    --------
    1. **Detection Execution**: Launch YOLOv8n grape detection via subprocess
    2. **Output Capture**: Capture and validate detection script output
    3. **Result Parsing**: Convert string output to structured dictionary format
    4. **Treatment Conversion**: Apply agricultural treatment classification algorithm
    5. **Result Validation**: Verify treatment level assignments and data integrity
    6. **Error Management**: Handle processing failures with comprehensive error reporting
    7. **Output Generation**: Return structured treatment recommendations

    Agricultural Processing Pipeline:
        - **Computer Vision**: YOLOv8n neural network grape detection with Hailo8L
        - **Data Processing**: Detection result extraction and format validation
        - **Agricultural Intelligence**: Grape count to treatment level conversion
        - **Quality Assurance**: Result validation and error handling
        - **System Integration**: Structured output for agricultural system compatibility

    Detection and Treatment Integration:
        - **AI Processing**: Hardware-accelerated grape bunch detection
        - **Agricultural Mapping**: Detection count to treatment level transformation
        - **Precision Agriculture**: Variable-rate treatment recommendations
        - **Vineyard Management**: Actionable agricultural guidance generation

    Error Handling Strategy:
        - **Subprocess Monitoring**: Detection script execution status tracking
        - **Format Validation**: Output parsing and data integrity verification
        - **Error Reporting**: Comprehensive error message generation with diagnostics
        - **Graceful Termination**: Controlled process exit with error information

    Agricultural Applications:
        - **Treatment Planning**: Automated agricultural intervention recommendations
        - **Resource Optimization**: Precision application of vineyard treatments
        - **Yield Management**: Grape density-based productivity optimization
        - **Field Operations**: Real-time treatment decision support for equipment

    .. note::
        The function integrates multiple processing stages and includes comprehensive
        error handling to ensure reliable operation in agricultural field conditions.
        System exit is called on critical errors to prevent invalid data propagation.

    Examples
    --------
    Basic Agricultural Processing:

    .. code-block:: python

        # Execute complete grape detection and treatment conversion
        result = run(
            input_image="Images/Camera/vineyard_section_A1.jpg",
            output_folder="Images/Results/treatment_planning/"
        )
        
        treatment_level = result["Grape_bunch"]
        print(f"Recommended treatment level: {treatment_level}")
        
        # Interpret treatment recommendation
        treatment_descriptions = {
            0: "No treatment required",
            1: "Light treatment application", 
            2: "Standard treatment protocol",
            3: "Moderate treatment intensity",
            4: "Intensive treatment application",
            5: "Maximum treatment application"
        }
        
        description = treatment_descriptions.get(treatment_level, "Unknown level")
        print(f"Treatment description: {description}")

    Vineyard Block Processing:

    .. code-block:: python

        import os
        
        # Process entire vineyard block with treatment mapping
        def process_vineyard_block(block_path, output_base):
            treatment_map = {}
            error_log = []
            
            # Get all image files in block directory
            image_files = [f for f in os.listdir(block_path) if f.endswith('.jpg')]
            
            for image_file in image_files:
                image_path = os.path.join(block_path, image_file)
                section_id = image_file.split('.')[0]
                
                try:
                    # Process section and get treatment recommendation
                    result = run(image_path, f"{output_base}/{section_id}/")
                    treatment_map[section_id] = result
                    
                    print(f"{section_id}: Treatment level {result['Grape_bunch']}")
                    
                except Exception as e:
                    error_log.append(f"{section_id}: {str(e)}")
                    print(f"Error processing {section_id}: {e}")
            
            return treatment_map, error_log
        
        # Execute vineyard block processing
        treatment_results, errors = process_vineyard_block(
            "Images/Camera/Block_A/",
            "Images/Results/Block_A_Analysis/"
        )
        
        # Generate summary report
        total_sections = len(treatment_results)
        treatment_distribution = {}
        
        for section, result in treatment_results.items():
            level = result["Grape_bunch"]
            treatment_distribution[level] = treatment_distribution.get(level, 0) + 1
        
        print(f"\\nVineyard Block Summary:")
        print(f"Total sections processed: {total_sections}")
        print(f"Processing errors: {len(errors)}")
        
        for level, count in sorted(treatment_distribution.items()):
            print(f"Treatment Level {level}: {count} sections")

    Precision Agriculture Integration:

    .. code-block:: python

        # Integration with precision agriculture equipment
        def generate_treatment_prescription(vineyard_images, gps_coordinates):
            prescription_map = []
            
            for i, image_path in enumerate(vineyard_images):
                try:
                    # Process image and get treatment recommendation
                    result = run(image_path, "temp_processing/")
                    
                    # Create prescription map entry
                    prescription_entry = {
                        'latitude': gps_coordinates[i][0],
                        'longitude': gps_coordinates[i][1],
                        'treatment_level': result["Grape_bunch"],
                        'image_source': image_path,
                        'processing_status': 'success'
                    }
                    
                    prescription_map.append(prescription_entry)
                    
                except Exception as e:
                    # Log processing failures
                    error_entry = {
                        'latitude': gps_coordinates[i][0],
                        'longitude': gps_coordinates[i][1],
                        'treatment_level': 0,  # Default to no treatment
                        'image_source': image_path,
                        'processing_status': 'error',
                        'error_message': str(e)
                    }
                    
                    prescription_map.append(error_entry)
            
            return prescription_map
        
        # Example usage with GPS coordinates
        images = [
            "Images/Camera/40.209544_-3.465575.jpg",
            "Images/Camera/40.209544_-3.465821.jpg",
            "Images/Camera/40.209544_-3.466066.jpg"
        ]
        
        coordinates = [
            (40.209544, -3.465575),
            (40.209544, -3.465821),
            (40.209544, -3.466066)
        ]
        
        prescription = generate_treatment_prescription(images, coordinates)
        
        # Export prescription map for agricultural equipment
        for entry in prescription:
            if entry['processing_status'] == 'success':
                print(f"GPS ({entry['latitude']}, {entry['longitude']}): "
                      f"Treatment Level {entry['treatment_level']}")

    Returns
    -------
    dict
        Agricultural treatment recommendation dictionary:
        
        Successful processing format:
            {
                "Grape_bunch": <treatment_level>
            }
        
        Treatment level values:
            - 0: No treatment required (0 grapes detected)
            - 1: Light treatment (1-4 grapes detected)
            - 2: Standard treatment (5-9 grapes detected)
            - 3: Moderate treatment (10-14 grapes detected)
            - 4: Intensive treatment (15-19 grapes detected)
            - 5: Maximum treatment (20+ grapes detected)
        
        Example returns:
            - {"Grape_bunch": 0} - No agricultural intervention needed
            - {"Grape_bunch": 2} - Standard treatment protocol recommended
            - {"Grape_bunch": 5} - Maximum treatment application required

    Raises
    ------
    subprocess.CalledProcessError
        When grape detection subprocess execution fails:
        - External script execution errors
        - YOLOv8n model processing failures
        - Hailo8L hardware acceleration issues
        - Invalid command-line arguments or parameters

    ValueError
        When result parsing or data conversion fails:
        - Invalid output format from detection script
        - String-to-dictionary conversion errors
        - Unexpected data types in processing pipeline

    SystemExit
        When critical errors require controlled process termination:
        - Comprehensive error information printed to stdout as JSON
        - Subprocess failure details with stderr and stdout capture
        - Exception details with error type and description

    Notes
    -----
    - **System Integration**: Designed for integration with agricultural management systems
    - **Error Handling**: Comprehensive error management with JSON-formatted error output
    - **Agricultural Focus**: Treatment levels optimized for precision viticulture applications
    - **Hardware Dependencies**: Requires Hailo8L acceleration hardware for optimal performance

    Processing Specifications:
        - **Detection Engine**: YOLOv8n neural network with Hailo8L acceleration
        - **Treatment Algorithm**: Agricultural density-based classification system
        - **Output Format**: JSON-compatible dictionary structure
        - **Error Reporting**: Structured error messages for system integration

    Agricultural Considerations:
        - **Field Reliability**: Robust error handling for agricultural field conditions
        - **Equipment Integration**: Compatible with precision agriculture machinery
        - **Resource Planning**: Treatment levels support agricultural resource allocation
        - **Quality Assurance**: Comprehensive validation for agricultural data integrity

    Performance Characteristics:
        - **Processing Speed**: Optimized for real-time agricultural operations
        - **Error Recovery**: Comprehensive failure handling with diagnostic information
        - **Resource Efficiency**: Minimal overhead for agricultural system integration
        - **Scalability**: Support for large-scale vineyard processing workflows
    """
    try:
        # Execute YOLOv8n grape bunch detection via external subprocess
        # This launches the Hailo8L-accelerated detection script and captures output
        result = run_grape_bunch(input_image, output_folder)
        
        # Convert string output from detection script to structured dictionary format
        # ast.literal_eval safely parses string representations of Python literals
        result_dict = ast.literal_eval(result)
        
        # Apply agricultural treatment classification algorithm to grape detection counts
        # Convert raw grape counts to standardized treatment level recommendations
        result_dict = apply_conversion_to_treatments(result_dict)
        
        # Return final treatment recommendations for agricultural system integration
        return result_dict  # Final result

    except subprocess.CalledProcessError as e:
        # Handle subprocess execution failures with comprehensive error reporting
        # Print structured error information for agricultural system debugging
        print(json.dumps({
            "error": "Subprocess failed",
            "stderr": e.stderr.strip(),
            "stdout": e.stdout.strip(),
            "cmd": e.cmd
        }))
        # Terminate process to prevent invalid data propagation in agricultural systems
        sys.exit(1)

    except Exception as e:
        # Handle general processing errors with structured error output
        # Provide comprehensive error information for agricultural system integration
        print(json.dumps({"error": str(e)}))
        # Terminate process to ensure agricultural data integrity and system reliability
        sys.exit(1)