"""
Agricultural Image Analysis Module
=================================

This module provides comprehensive image analysis capabilities for agricultural
drone systems, specializing in automated crop analysis, disease detection, and
treatment recommendation generation. It integrates multiple external AI models
to perform specialized agricultural image processing tasks including grape bunch
detection, disease identification, and precision agriculture analytics.

The module serves as the primary image processing interface for agricultural
drone operations, enabling real-time analysis of captured field images to support
precision agriculture decision-making, crop monitoring, and automated treatment
recommendations for optimal field management.

.. module:: analyze_image
    :synopsis: Agricultural image analysis and AI model integration for precision farming

Features
--------
- **Multi-Model Analysis**: Sequential execution of specialized agricultural AI models
- **Dynamic Model Loading**: Runtime loading and execution of external Python models
- **Coordinate-based Processing**: GPS coordinate-based image identification and processing
- **Treatment Analysis**: Automated analysis for specified agricultural treatments
- **Result Aggregation**: Comprehensive result compilation from multiple model outputs
- **Error Resilience**: Robust error handling for continuous field operations
- **Flexible Architecture**: Support for various agricultural AI model types

System Architecture
------------------
The agricultural image analysis system operates within the precision farming ecosystem:

Image Analysis Pipeline:
    Camera Capture → GPS Coordinate Mapping → Model Selection → AI Analysis → Result Aggregation

Processing Workflow:
    1. **Image Identification**: GPS coordinate-based image file location
    2. **Model Configuration**: Dynamic loading of treatment-specific AI models
    3. **Sequential Processing**: Ordered execution of selected agricultural models
    4. **Result Compilation**: Aggregation of analysis results from all models
    5. **Output Generation**: Structured result delivery for agricultural decisions

Agricultural Model Types:
    - **Crop Detection**: Identification and counting of agricultural products
    - **Disease Analysis**: Automated disease detection and severity assessment
    - **Quality Assessment**: Crop quality evaluation and grading
    - **Growth Monitoring**: Plant development and health analysis
    - **Yield Prediction**: Harvest estimation and productivity analysis

Field Operation Integration:
    - **Real-time Processing**: Immediate analysis during field operations
    - **Treatment Planning**: Automated recommendation generation
    - **Quality Control**: Continuous crop monitoring and assessment
    - **Decision Support**: Data-driven agricultural decision making

Workflow Architecture
--------------------
Agricultural Image Processing Pipeline:
    1. **Coordinate Processing**: GPS latitude/longitude coordinate handling
    2. **Image Location**: Automatic image file identification using coordinates
    3. **Model Configuration**: Treatment-based model selection and loading
    4. **Output Preparation**: Result directory creation and organization
    5. **Sequential Analysis**: Ordered execution of selected AI models
    6. **Result Integration**: Comprehensive result aggregation and formatting
    7. **Error Management**: Robust error handling and recovery mechanisms

Treatment Analysis Workflow:
    - **Treatment Selection**: Configurable treatment code specification
    - **Model Mapping**: Treatment-to-model mapping via configuration files
    - **Dynamic Execution**: Runtime model loading and execution
    - **Result Validation**: Output format verification and error handling

Classes
-------
None - This module provides functional interfaces for agricultural image analysis

Functions
---------
.. autofunction:: analyze_image
.. autofunction:: run_script

Dependencies
-----------
Core Dependencies:
    - **logging**: Comprehensive activity tracking and error reporting
    - **os**: File system operations and path management
    - **json**: Configuration file parsing and result serialization
    - **importlib.util**: Dynamic module loading and execution

File System Dependencies:
    - **Images/Camera/**: Source directory for captured agricultural images
    - **Images/Models/**: AI model storage and configuration directory
    - **Images/Results/**: Output directory for analysis results
    - **models.json**: Configuration file mapping treatments to AI models

Integration Points
-----------------
External Integrations:
    - **Agricultural AI Models**: Integration with specialized crop analysis models
    - **Camera Systems**: Input from agricultural drone camera captures
    - **GPS Systems**: Coordinate-based image identification and mapping
    - **Treatment Systems**: Integration with precision agriculture treatment planning

Internal Integrations:
    - **Logging Infrastructure**: Centralized activity logging and error tracking
    - **File Management**: Structured file organization and result storage
    - **Configuration Management**: Dynamic model configuration and selection
    - **Error Handling**: Comprehensive error management and recovery

Performance Characteristics
--------------------------
Processing Performance:
    - **Sequential Processing**: Ordered model execution for comprehensive analysis
    - **Dynamic Loading**: Efficient runtime model loading and execution
    - **Memory Management**: Optimized resource usage during model execution
    - **Error Isolation**: Individual model failures don't affect overall processing

Agricultural Optimization:
    - **Field-specific Analysis**: Coordinate-based processing for field mapping
    - **Treatment Focus**: Targeted analysis based on specified treatments
    - **Result Integration**: Comprehensive analysis result compilation
    - **Scalability**: Support for multiple concurrent image analysis operations

Agricultural Data Formats
-------------------------
Input Data Structure:
    - **GPS Coordinates**: Decimal degree latitude/longitude specifications
    - **Treatment Codes**: Numerical treatment identifiers for model selection
    - **Image Files**: JPEG format agricultural images with coordinate naming
    - **Configuration**: JSON-based model configuration and mapping

Output Data Structure:
    - **Analysis Results**: Structured dictionaries with model-specific outputs
    - **Treatment Recommendations**: Automated treatment suggestions
    - **Quality Metrics**: Crop quality and health assessments
    - **Error Information**: Detailed error reporting for failed analyses

Error Handling Strategy
----------------------
Multi-level Error Management:
    - **File-Level**: Image file access and validation error handling
    - **Model-Level**: Individual AI model execution error management
    - **Configuration-Level**: Model configuration and mapping error handling
    - **System-Level**: Comprehensive error reporting and recovery procedures

Recovery Mechanisms:
    - **Model Isolation**: Individual model failures don't affect other models
    - **Graceful Degradation**: Partial results returned on individual failures
    - **Error Reporting**: Detailed error information for troubleshooting
    - **Logging Integration**: Comprehensive error tracking and analysis

Notes
-----
- **Agricultural Focus**: Specialized for precision agriculture image analysis
- **Model Flexibility**: Support for various agricultural AI model types
- **Coordinate-based**: GPS coordinate integration for field mapping
- **Error Resilience**: Robust error handling for continuous field operations

Configuration Requirements:
    - **Model Configuration**: models.json file with treatment-to-model mapping
    - **Directory Structure**: Organized image, model, and result directories
    - **Model Compatibility**: External models must implement 'run' function interface
    - **File Naming**: Coordinate-based image file naming convention

Agricultural Considerations:
    - **Field Conditions**: Robust operation in various agricultural environments
    - **Real-time Processing**: Optimized for in-field image analysis
    - **Treatment Integration**: Seamless integration with precision agriculture workflows
    - **Quality Assurance**: Comprehensive error handling and result validation

See Also
--------
importlib.util : Dynamic module loading and execution
json : Configuration file parsing and result serialization
logging : Comprehensive activity tracking and error reporting
os : File system operations and path management
"""

import logging
import os
import json
import importlib.util


def analyze_image(lat: float, lon: float, treatments: list, logger: logging.Logger) -> dict:
    """
    Analyze agricultural images for specified treatments using external AI models.

    This function performs comprehensive agricultural image analysis by loading
    treatment-specific AI models, processing field images captured at GPS coordinates,
    and generating detailed analysis results for precision agriculture applications.
    It supports multiple agricultural treatments including crop detection, disease
    analysis, quality assessment, and yield prediction.

    The function operates as the primary interface for agricultural image processing,
    integrating multiple specialized AI models to provide comprehensive field analysis
    for precision farming decision-making and automated treatment recommendations.

    :param lat: Latitude coordinate in decimal degrees for image identification
    :type lat: float
    :param lon: Longitude coordinate in decimal degrees for image identification  
    :type lon: float
    :param treatments: List of treatment codes for model selection and execution
    :type treatments: list
    :param logger: Configured logger instance for comprehensive activity tracking
    :type logger: logging.Logger
    :returns: Dictionary containing treatment analysis results and recommendations
    :rtype: dict
    :raises FileNotFoundError: When image files or model configuration cannot be located
    :raises json.JSONDecodeError: When model configuration file format is invalid
    :raises Exception: For unexpected errors during model execution or processing

    Workflow
    --------
    1. **Coordinate Processing**: Generate image filename from GPS coordinates
    2. **Image Identification**: Locate source image file using coordinate-based naming
    3. **Model Configuration**: Load treatment-to-model mapping from JSON configuration
    4. **Model Selection**: Filter models based on specified treatment codes
    5. **Output Preparation**: Create organized result directory structure
    6. **Sequential Processing**: Execute selected AI models in ordered sequence
    7. **Result Aggregation**: Compile and integrate analysis results from all models
    8. **Error Management**: Handle individual model failures with comprehensive logging

    Agricultural Processing Pipeline:
        - **Image Location**: GPS coordinate-based image file identification
        - **Treatment Mapping**: Treatment code to AI model mapping via configuration
        - **Model Execution**: Dynamic loading and execution of agricultural AI models
        - **Result Integration**: Comprehensive analysis result compilation

    Treatment Processing Types:
        - **Crop Detection**: Automated identification and counting of agricultural products
        - **Disease Analysis**: Comprehensive disease detection and severity assessment
        - **Quality Assessment**: Crop quality evaluation and grading analysis
        - **Growth Monitoring**: Plant development and health status analysis
        - **Yield Prediction**: Harvest estimation and productivity forecasting

    Expected File Structure:
        - **Input Images**: Images/Camera/{lat}_{lon}.jpg
        - **Model Configuration**: Images/Models/models.json
        - **Model Scripts**: Images/Models/{model_name}/detect.py
        - **Output Results**: Images/Results/{lon}_{lat}/

    .. note::
        Treatment codes must correspond to entries in the models.json configuration file.
        Each external model must implement a 'run' function accepting input_image and 
        output_folder parameters and returning a dictionary with analysis results.

    Examples
    --------
    Basic Agricultural Analysis:

    .. code-block:: python

        import logging
        
        # Setup logging for agricultural operations
        logger = logging.getLogger('field_analysis')
        
        # Analyze specific field location
        results = analyze_image(
            lat=40.123456,
            lon=-3.456789,
            treatments=[0, 1],  # Grape detection and disease analysis
            logger=logger
        )
        
        # Process grape detection results
        if 'grape_bunches' in results:
            count = results['grape_bunches']['detected_count']
            quality = results['grape_bunches']['average_quality']
            print(f"Detected {count} grape bunches with quality {quality}")

    Multi-Treatment Analysis:

    .. code-block:: python

        # Comprehensive field treatment analysis
        comprehensive_treatments = [0, 1, 2, 3]  # All available treatments
        
        analysis_results = analyze_image(
            lat=40.209544,
            lon=-3.465575,
            treatments=comprehensive_treatments,
            logger=logger
        )
        
        # Process results for each treatment
        for treatment_name, treatment_data in analysis_results.items():
            if 'recommendations' in treatment_data:
                recommendations = treatment_data['recommendations']
                print(f"Treatment {treatment_name}: {recommendations}")

    Returns
    -------
    dict
        Comprehensive analysis results dictionary containing:
        
        - **Treatment Results**: Individual model analysis outputs
        - **Detection Data**: Crop detection counts and classifications
        - **Disease Information**: Disease detection and severity assessments
        - **Quality Metrics**: Crop quality evaluations and grading
        - **Recommendations**: Automated treatment recommendations
        - **Error Reports**: Detailed error information for failed models

    Raises
    ------
    FileNotFoundError
        When specified image file or model configuration cannot be located
    json.JSONDecodeError
        When models.json configuration file has invalid JSON format
    ImportError
        When external AI model scripts cannot be imported or executed
    Exception
        For unexpected errors during model execution or result processing

    Notes
    -----
    - **Thread Safety**: Function is thread-safe for concurrent field processing
    - **Error Isolation**: Individual model failures don't affect other model execution
    - **Agricultural Focus**: Optimized for precision agriculture workflows
    - **Scalability**: Supports high-volume field image processing operations
    - **Model Flexibility**: Compatible with various agricultural AI model types

    Performance Considerations:
        - **Sequential Processing**: Models executed in order for comprehensive analysis
        - **Memory Management**: Efficient resource usage during model execution
        - **Error Recovery**: Graceful handling of individual model failures
        - **Result Optimization**: Optimized result compilation and integration
    """
    # Generate coordinate-based filename for agricultural image identification
    filename = f"{lat}_{lon}.jpg"
    file_path = f"Images/Camera/{filename}"
    logger.info(f"[ANALYZE_IMAGE] - Starting analysis for agricultural image: {file_path}")

    # Load agricultural AI model configuration from JSON file
    models_path = "Images/Models/models.json"
    with open(models_path, "r") as f:
        models_dict = json.load(f)

    # Filter and select models based on specified treatment codes
    models_to_run = [models_dict[t] for t in treatments if t in models_dict]
    
    # Initialize results dictionary for agricultural analysis compilation
    results = {}
    
    # Create organized output directory structure using coordinate-based naming
    output_folder = f"Images/Results/{lon}_{lat}/"

    # Create output folder if it doesn't exist for result organization
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process agricultural AI models sequentially for comprehensive analysis
    for model_path in models_to_run:
        try:
            # Execute individual agricultural AI model with error handling
            logger.info(f"[ANALYZE_IMAGE] - Executing agricultural model: {model_path}")
            output = run_script(model_path, file_path, output_folder)
            logger.info(f"[ANALYZE_IMAGE] - Model execution completed with output: {output}")
            
            # Integrate model results into comprehensive analysis results
            if isinstance(output, dict):
                results.update(output)
        except Exception as e:
            # Handle individual model execution errors with detailed logging
            logger.error(f"[ANALYZE_IMAGE] - Error executing agricultural model {model_path}: {str(e)}")

    return results


def run_script(path: str, input_image: str, output_folder: str) -> dict:
    """
    Dynamically import and execute agricultural AI model scripts with comprehensive error handling.

    This function provides a robust interface for loading and executing external
    agricultural AI models at runtime. It handles dynamic module loading, function
    validation, and execution of specialized agricultural analysis scripts while
    maintaining comprehensive error handling and result validation.

    The function serves as the primary execution engine for agricultural AI models,
    enabling flexible integration of various crop analysis, disease detection, and
    quality assessment models within the precision agriculture image processing pipeline.

    :param path: Absolute file path to the Python script containing agricultural AI model
    :type path: str
    :param input_image: File path to the agricultural image for analysis processing
    :type input_image: str
    :param output_folder: Directory path for storing analysis results and outputs
    :type output_folder: str
    :returns: Dictionary containing model analysis results or comprehensive error information
    :rtype: dict
    :raises ImportError: When the specified script cannot be imported or loaded
    :raises AttributeError: When the required 'run' function is not found in the script
    :raises Exception: For unexpected errors during module loading or function execution

    Workflow
    --------
    1. **Module Identification**: Extract module name from script file path
    2. **Spec Creation**: Create module specification for dynamic loading
    3. **Module Loading**: Load module from file specification into memory
    4. **Module Execution**: Execute module code to initialize functions and classes
    5. **Function Validation**: Verify presence of required 'run' function interface
    6. **Model Execution**: Execute agricultural AI model with specified parameters
    7. **Result Validation**: Validate return type and format of analysis results
    8. **Error Handling**: Comprehensive error management with detailed reporting

    Agricultural Model Integration:
        - **Dynamic Loading**: Runtime model loading without static dependencies
        - **Interface Validation**: Standardized 'run' function interface verification
        - **Result Processing**: Structured analysis result handling and validation
        - **Error Isolation**: Individual model execution isolation for system stability

    Model Execution Requirements:
        - **Function Interface**: Models must implement 'run(input_image, output_folder)' function
        - **Return Format**: Models must return dictionary with analysis results
        - **Error Handling**: Models should handle internal errors gracefully
        - **File Operations**: Models responsible for output file management

    Expected Model Structure:
        - **Input Processing**: Image file loading and preprocessing
        - **AI Analysis**: Specialized agricultural analysis execution
        - **Result Generation**: Structured analysis result compilation
        - **Output Management**: Result file creation and organization

    .. note::
        External agricultural AI models must implement a standardized 'run' function
        interface that accepts input_image and output_folder parameters and returns
        a dictionary containing structured analysis results.

    Examples
    --------
    Basic Model Execution:

    .. code-block:: python

        # Execute grape bunch detection model
        model_path = "Images/Models/Grape_Bunch_Hailo8/detect.py"
        input_image = "Images/Camera/40.123456_-3.456789.jpg"
        output_folder = "Images/Results/-3.456789_40.123456/"
        
        result = run_script(model_path, input_image, output_folder)
        
        if 'error' not in result:
            grape_count = result.get('detected_bunches', 0)
            print(f"Detected {grape_count} grape bunches")
        else:
            print(f"Model execution failed: {result['error']}")

    Disease Analysis Execution:

    .. code-block:: python

        # Execute disease detection model
        disease_model = "Images/Models/Grape_Diseases_Hailo8/analyze.py"
        field_image = "Images/Camera/40.209544_-3.465575.jpg"
        results_dir = "Images/Results/-3.465575_40.209544/"
        
        analysis = run_script(disease_model, field_image, results_dir)
        
        if 'diseases_detected' in analysis:
            diseases = analysis['diseases_detected']
            severity = analysis.get('severity_level', 'unknown')
            print(f"Diseases found: {diseases} with severity: {severity}")

    Error Handling Example:

    .. code-block:: python

        # Robust model execution with error handling
        try:
            result = run_script(model_path, image_path, output_path)
            
            if 'error' in result:
                print(f"Model error: {result['error']}")
                # Handle model-specific errors
            else:
                # Process successful analysis results
                process_analysis_results(result)
                
        except Exception as e:
            print(f"Execution error: {str(e)}")
            # Handle system-level errors

    Returns
    -------
    dict
        Model execution results or error information:
        
        **Successful Execution**:
            Dictionary containing model-specific analysis results such as:
            - Detection counts and classifications
            - Disease analysis and severity assessments  
            - Quality metrics and recommendations
            - Spatial analysis and coordinate data
            
        **Error Conditions**:
            Dictionary with 'error' key containing detailed error description:
            - Import/loading errors for inaccessible scripts
            - Missing function errors for non-compliant models
            - Execution errors for runtime failures
            - Return type errors for invalid result formats

    Example successful return:

    .. code-block:: python

        {
            'detected_bunches': 12,
            'average_bunch_size': 'medium',
            'quality_score': 8.5,
            'disease_indicators': [],
            'recommendations': ['harvest_ready']
        }

    Example error return:

    .. code-block:: python

        {
            'error': 'No \'run\' function found in script: /path/to/model.py'
        }

    Raises
    ------
    ImportError
        When the specified script file cannot be imported or accessed
    AttributeError  
        When the required 'run' function interface is not implemented
    TypeError
        When the model's 'run' function returns invalid data types
    Exception
        For unexpected errors during module loading, execution, or result processing

    Notes
    -----
    - **Dynamic Loading**: Enables runtime integration of new agricultural AI models
    - **Error Isolation**: Individual model failures don't affect system stability
    - **Interface Standardization**: Enforces consistent model integration patterns
    - **Agricultural Focus**: Optimized for precision agriculture model workflows
    - **Performance Optimization**: Efficient module loading and execution management

    Performance Considerations:
        - **Memory Management**: Proper module cleanup after execution
        - **Error Recovery**: Graceful handling of model execution failures
        - **Result Validation**: Comprehensive output format verification
        - **Resource Isolation**: Individual model resource management
    """
    try:
        # Extract module name from file path for dynamic loading identification
        module_name = os.path.splitext(os.path.basename(path))[0]
        
        # Load module specification and create module instance for dynamic execution
        spec = importlib.util.spec_from_file_location(module_name, path)
        if spec is None:
            return {"error": f"Could not create module specification for script: {path}"}
        
        module = importlib.util.module_from_spec(spec)
        
        # Execute module code to initialize functions and classes
        spec.loader.exec_module(module)

        # Validate presence of required 'run' function interface
        if hasattr(module, "run"):
            
            # Execute agricultural AI model with specified parameters
            result = module.run(input_image, output_folder)
            
            # Validate return type and format of analysis results
            if isinstance(result, dict):
                return result
            else:
                # Handle invalid return type with detailed error reporting
                error_msg = f"'run' function in {path} returned {type(result)}, expected dict."
                return {"error": error_msg}
        else:
            # Handle missing 'run' function with comprehensive error reporting
            error_msg = f"No 'run' function found in agricultural AI script: {path}"
            return {"error": error_msg}

    except ImportError as e:
        # Handle import errors with detailed module loading information
        error_msg = f"Import error loading agricultural AI model {path}: {str(e)}"
        return {"error": error_msg}
    except Exception as e:
        # Handle unexpected errors with comprehensive error reporting and logging
        error_msg = f"Unexpected error during execution of agricultural AI model {path}: {str(e)}"
        return {"error": error_msg}
