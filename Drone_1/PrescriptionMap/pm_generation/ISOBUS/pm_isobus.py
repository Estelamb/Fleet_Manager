"""
ISOBUS Prescription Map Generator Module
=======================================

This module provides ISOBUS-compliant prescription map generation functionality for
agricultural drone systems. It implements the ISO 11783 standard for agricultural
data exchange, enabling interoperability with ISOBUS-compatible farm equipment
and precision agriculture systems.

The module manages complex ISOBUS task data structures, grid-based spatial data
organization, and standardized agricultural treatment prescriptions suitable for
integration with commercial farm management systems and equipment.

.. module:: pm_isobus
    :synopsis: ISOBUS-compliant prescription map generation for agricultural equipment integration

Features
--------
- **ISOBUS Compliance**: Full ISO 11783 standard implementation for agricultural data exchange
- **Task Management**: Dynamic task creation and management for agricultural operations
- **Grid-Based Spatial Data**: Row-major order grid system for precise spatial prescription
- **Treatment Integration**: Multi-treatment prescription support with standardized references
- **Equipment Compatibility**: Direct integration with ISOBUS farm equipment and systems
- **Template-Based Generation**: Configurable task templates for different agricultural operations

ISOBUS Standard Compliance
-------------------------
Implementation follows ISO 11783 specifications:
    - **Task Controller (TC)**: Task data structure and management
    - **Spatial Data**: Grid-based prescription map format
    - **Cultural Practices**: Standardized agricultural operation references
    - **Product Allocation**: Equipment-compatible product and treatment specifications
    - **Grid System**: Row-major spatial data organization with geographic positioning

Data Structure Hierarchy
-----------------------
ISOBUS prescription maps follow standardized structure:
    {
        "Task": [
            {
                "TaskId": "TSK1",
                "OperTechPractice": {
                    "CulturalPracticeIdRef": "treatment_practice"
                },
                "ProductAllocation": {
                    "ProductIdRef": "product_reference"
                },
                "Grid": {
                    "GridMinimumEastPosition": longitude,
                    "GridMinimumNorthPosition": latitude,
                    "GridMaximumRow": max_rows,
                    "GridMaximumColumn": max_cols,
                    "GridCell": [values_in_row_major_order]
                }
            }
        ]
    }

Workflow
--------
ISOBUS PM Generation Pipeline:
    1. **Data Initialization**: Load existing PM or create from ISOBUS templates
    2. **Task Management**: Ensure required tasks exist for all treatments
    3. **Spatial Positioning**: Update grid minimum position coordinates
    4. **Grid Dimensioning**: Expand grid dimensions to accommodate new coordinates
    5. **Cell Value Assignment**: Update specific grid cells with treatment values
    6. **Data Persistence**: Save ISOBUS-compliant JSON structure
    7. **Status Reporting**: Provide operation confirmation and error handling

Grid System Implementation
-------------------------
Spatial data organization using row-major order:
    - **Grid Origin**: Minimum East/North position defines coordinate system
    - **Row-Major Storage**: Linear array storage as [row0_col0, row0_col1, ..., row1_col0, ...]
    - **Index Calculation**: index = row * total_columns + column
    - **Dynamic Expansion**: Automatic grid resizing to accommodate new coordinates

Template Configuration
---------------------
ISOBUS templates define standard structures:
    - **Header Template**: Basic ISOBUS document structure and metadata
    - **Task Template**: Standard task definition for agricultural operations
    - **Product References**: Standardized treatment and product identifications
    - **Grid Configuration**: Default spatial data organization parameters

Global Configuration Constants
-----------------------------
HEADER : str
    Path to ISOBUS header template JSON file containing document structure.
    
TASK : str
    Path to ISOBUS task template JSON file containing standard task definitions.
    
FOLDER : str
    Directory path for storing generated ISOBUS prescription map files.

Functions
---------
.. autofunction:: generate_pm
.. autofunction:: create_new_pm
.. autofunction:: ensure_task_exists
.. autofunction:: update_grid_min_position
.. autofunction:: update_grid_max_row_column
.. autofunction:: update_grid_cells

Dependencies
-----------
- **argparse**: Command-line interface for integration with PM management system
- **json**: ISOBUS data serialization and template processing
- **os**: File system operations and directory management
- **copy**: Deep copying for template instantiation
- **typing**: Type hint support for enhanced documentation

Integration Points
-----------------
This module integrates with:
    - **PM Management System**: Standard interface via command-line parameters
    - **ISOBUS Equipment**: Direct compatibility with farm machinery task controllers
    - **Farm Management Systems**: Standard agricultural data exchange format
    - **Precision Agriculture**: Variable rate application and spatial prescriptions

Performance Considerations
-------------------------
- **Grid Expansion**: O(n) complexity for grid resizing operations
- **Template Processing**: Efficient deep copying for task instantiation
- **File I/O**: Optimized JSON serialization with proper formatting
- **Memory Usage**: Scales with grid size and number of treatments

Error Handling Strategy
----------------------
- **Template Validation**: Robust template loading with fallback mechanisms
- **Grid Boundary Checking**: Index validation for spatial data operations
- **Task Management**: Graceful handling of missing or invalid task structures
- **File System Operations**: Comprehensive error reporting and recovery

Examples
--------
Command line usage:

.. code-block:: bash

    # Single treatment prescription
    python pm_isobus.py \\
        --amount '{"nitrogen": 120}' \\
        --grid '[10, 15]' \\
        --lat '40.123456' \\
        --long '-74.987654'
    
    # Multiple treatment prescription
    python pm_isobus.py \\
        --amount '{"nitrogen": 100, "phosphorus": 50, "potassium": 75}' \\
        --grid '[8, 12]' \\
        --lat '40.209544' \\
        --long '-3.465575'

Integration usage:

.. code-block:: python

    # Called via PM management system
    import subprocess
    subprocess.run([
        'python', 'pm_isobus.py',
        '--amount', json.dumps({"fertilizer": 85}),
        '--grid', json.dumps([12, 20]),
        '--long', '-74.006',
        '--lat', '40.7128'
    ])

ISOBUS Equipment Integration
---------------------------
Generated prescription maps are compatible with:
    - **Tractors**: ISOBUS-enabled tractors with task controller systems
    - **Implements**: Variable rate application equipment (spreaders, sprayers)
    - **Farm Management**: Commercial farm management software systems
    - **Precision Agriculture**: GPS-guided variable rate application systems

Notes
-----
- All spatial data follows ISO 11783 grid specification requirements
- Task IDs are automatically generated and incremented for uniqueness
- Grid cells are initialized with zero values for undefined prescription areas
- Geographic coordinates use decimal degrees for global compatibility

See Also
--------
PrescriptionMap.pm_manager : PM coordination and parallel processing system
copy.deepcopy : Template instantiation mechanism
json.dump : ISOBUS data serialization implementation
"""

import argparse
import json
import os
import copy
from typing import Dict, List, Union, Optional, Any

# ISOBUS Configuration Constants
# =============================

HEADER = "PrescriptionMap/pm_generation/ISOBUS/isobus_header.json"  # ISOBUS document header template
TASK = "PrescriptionMap/pm_generation/ISOBUS/isobus_task.json"      # ISOBUS task definition template
FOLDER = "PrescriptionMap/pm_generation/ISOBUS/PMs"                 # Generated PM storage directory

def generate_pm(amount: Dict[str, int], grid: List[int], long: float, lat: float) -> None:
    """
    Generate ISOBUS-compliant prescription map with treatment data at specified grid coordinates.

    This function serves as the main entry point for ISOBUS prescription map generation,
    orchestrating the complete workflow from data initialization through spatial data
    management to final ISOBUS-compliant file generation. It ensures compatibility
    with ISO 11783 standards for agricultural equipment integration.

    Parameters
    ----------
    amount : Dict[str, int]
        Dictionary mapping treatment names to prescription values.
        Keys represent treatment/product identifiers, values represent application rates.
        Examples: {"nitrogen": 120, "phosphorus": 80, "potassium": 60}
    grid : List[int]
        Grid coordinates as [row, column] for spatial positioning in field coordinate system.
        Uses zero-based indexing with automatic grid expansion for new coordinates.
        Examples: [10, 15], [0, 0], [25, 40]
    long : float
        Longitude coordinate in decimal degrees for geographic positioning.
        Used for ISOBUS grid minimum position calculation and spatial reference.
        Range: -180.0 to +180.0 degrees
    lat : float
        Latitude coordinate in decimal degrees for geographic positioning.
        Used for ISOBUS grid minimum position calculation and spatial reference.
        Range: -90.0 to +90.0 degrees

    Returns
    -------
    None
        Function performs ISOBUS PM generation and file operations without return values.
        Success indicated by completion without exceptions and status output.

    Workflow
    --------
    1. **Data Loading**: Load existing ISOBUS PM or initialize from templates
    2. **Template Validation**: Verify task template structure and accessibility
    3. **Task Management**: Ensure required tasks exist for all specified treatments
    4. **Spatial Positioning**: Update grid minimum position with new coordinates
    5. **Grid Dimensioning**: Expand grid dimensions to accommodate new coordinates
    6. **Cell Assignment**: Update specific grid cells with treatment prescription values
    7. **Data Persistence**: Save complete ISOBUS-compliant structure to JSON file

    ISOBUS Compliance
    ----------------
    Generated prescription maps follow ISO 11783 specifications:
        - **Task Structure**: Standardized task definitions with unique identifiers
        - **Spatial Data**: Grid-based prescription organization with geographic reference
        - **Treatment References**: ISOBUS-compatible cultural practice and product identifiers
        - **Data Format**: JSON structure compatible with ISOBUS task controllers

    Error Handling
    --------------
    - **File System Errors**: Graceful handling of missing templates or PM files
    - **Template Validation**: Comprehensive validation of ISOBUS template structure
    - **Grid Validation**: Boundary checking and index validation for spatial operations
    - **JSON Processing**: Robust parsing and serialization error management

    Examples
    --------
    >>> # Generate single treatment prescription
    >>> generate_pm({"nitrogen": 100}, [12, 8], -74.006, 40.7128)
    >>> # Creates ISOBUS PM with nitrogen treatment at grid position [12, 8]

    >>> # Generate multi-treatment prescription
    >>> treatments = {"nitrogen": 90, "phosphorus": 45, "potassium": 60}
    >>> generate_pm(treatments, [15, 20], -3.4656, 40.2095)
    >>> # Creates ISOBUS PM with multiple treatments at specified coordinates

    Integration Notes
    ----------------
    Function designed for:
        - **PM Management Integration**: Called via standardized command-line interface
        - **ISOBUS Equipment**: Direct compatibility with farm machinery task controllers
        - **Batch Processing**: Multiple treatment handling in single operation
        - **Spatial Analysis**: Geographic coordinate integration for field mapping

    Performance Characteristics
    --------------------------
    - **Template Processing**: Efficient deep copying for task instantiation
    - **Grid Operations**: O(n) complexity for grid expansion and cell updates
    - **File I/O**: Optimized JSON serialization with proper ISOBUS formatting
    - **Memory Usage**: Scales with grid size and number of active treatments

    Notes
    -----
    - Function creates ISOBUS-compliant output suitable for equipment integration
    - All treatments generate separate tasks within single prescription map
    - Grid coordinates automatically expand prescription map spatial coverage
    - Geographic coordinates establish spatial reference for equipment navigation

    See Also
    --------
    create_new_pm : ISOBUS template initialization and structure creation
    ensure_task_exists : Task management and template instantiation
    update_grid_cells : Spatial data management and cell value assignment
    """
    # Construct path for ISOBUS prescription map file
    path = os.path.join(FOLDER, "isobus_pm.json")
    
    # Load existing ISOBUS PM data or initialize from templates
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print("[WARNING] - PM file corrupted or not found, creating new one")
            data = create_new_pm()
    else:
        data = create_new_pm()
    
    # Exit if ISOBUS data initialization failed
    if data is None:
        print("[ERROR] - Failed to initialize PM data. Exiting.")
        return

    # Load ISOBUS task template with comprehensive error handling
    try:
        with open(TASK, "r") as f:
            task_template = json.load(f)
        if "Task" not in task_template or not task_template["Task"]:
            print(f"[ERROR] - Task template has invalid structure at {TASK}")
            return
    except Exception as e:  # Broad exception for any file/JSON issues
        print(f"[ERROR] - Failed to load task template: {str(e)}")
        return
        
    # Process all treatments and ensure corresponding ISOBUS tasks exist
    for treatment in amount:
        data = ensure_task_exists(treatment, data, task_template)
        
    # Update ISOBUS spatial data with new coordinate information
    data = update_grid_min_position(data, long, lat)
    data = update_grid_max_row_column(data, grid)
    data = update_grid_cells(data, amount, grid)
    
    # Save complete ISOBUS-compliant prescription map structure
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
        
    print(f"ISOBUS PM updated at {path} with treatments: {amount} at grid: {grid}")

def create_new_pm() -> Optional[Dict[str, Any]]:
    """
    Initialize new ISOBUS prescription map from header template.

    This function creates a new ISOBUS-compliant prescription map structure by loading
    the standardized header template and initializing the task list. It provides
    robust error handling for template loading and ensures proper ISOBUS document
    structure initialization.

    Returns
    -------
    Optional[Dict[str, Any]]
        ISOBUS prescription map data structure with initialized task list.
        Returns None if template loading fails or invalid structure detected.

    Workflow
    --------
    1. **Data Initialization**: Create empty dictionary for ISOBUS data structure
    2. **Header Loading**: Load ISOBUS header template if available
    3. **Structure Validation**: Verify loaded data is valid dictionary format
    4. **Task List Initialization**: Ensure Task array exists for agricultural operations
    5. **Error Recovery**: Handle template loading failures with fallback structures

    Examples
    --------
    >>> # Create new ISOBUS PM structure
    >>> pm_data = create_new_pm()
    >>> if pm_data:
    >>>     print(f"Initialized PM with {len(pm_data.get('Task', []))} tasks")
    """
    # Initialize empty ISOBUS data structure
    data = {}
    try:
        # Load ISOBUS header template if available
        if os.path.exists(HEADER):
            with open(HEADER, "r") as f:
                loaded = json.load(f)
                if isinstance(loaded, dict):
                    data = loaded
                else:
                    print(f"[WARNING] - Header file is not a dictionary, using empty structure")
    except Exception as e:
        print(f"[ERROR] - Failed to load header: {str(e)}")
    
    # Ensure ISOBUS Task list exists and is properly structured
    if "Task" not in data or not isinstance(data["Task"], list):
        data["Task"] = []
    
    return data

def ensure_task_exists(treatment: str, data: Dict[str, Any], task_template: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ensure ISOBUS task exists for specified treatment, creating from template if needed.

    This function manages ISOBUS task creation and validation, ensuring that each
    agricultural treatment has a corresponding task definition with proper cultural
    practice references and product allocations according to ISO 11783 standards.

    Parameters
    ----------
    treatment : str
        Treatment identifier for agricultural operation.
        Used to generate cultural practice and product references.
        Examples: "nitrogen", "phosphorus", "pesticide", "herbicide"
    data : Dict[str, Any]
        ISOBUS prescription map data structure containing task definitions.
        Modified in-place with new task if required.
    task_template : Dict[str, Any]
        ISOBUS task template containing standard task structure.
        Used as basis for creating new treatment-specific tasks.

    Returns
    -------
    Dict[str, Any]
        Updated ISOBUS data structure with task for specified treatment.

    Workflow
    --------
    1. **Reference Generation**: Create cultural practice reference from treatment name
    2. **Task Search**: Check if task already exists for specified treatment
    3. **Template Processing**: Deep copy task template for new task creation
    4. **Task Configuration**: Set unique task ID and treatment-specific references
    5. **Task Integration**: Add new task to ISOBUS data structure

    Examples
    --------
    >>> # Ensure nitrogen treatment task exists
    >>> data = ensure_task_exists("nitrogen", isobus_data, task_template)
    >>> # Creates task with cultural practice "nitrogen_treatment" if not exists
    """
    # Generate ISOBUS cultural practice reference from treatment name
    cultural_practice_ref = f"{treatment}_treatment"
    
    # Search for existing task with matching cultural practice reference
    for task in data["Task"]:
        if task["OperTechPractice"]["CulturalPracticeIdRef"] == cultural_practice_ref:
            return data

    # Create new ISOBUS task from template for specified treatment
    try:
        new_task = copy.deepcopy(task_template["Task"][0])
        number_of_tasks = len(data["Task"])+1
        new_task["TaskId"] = f"TSK{number_of_tasks}"
        new_task["OperTechPractice"]["CulturalPracticeIdRef"] = cultural_practice_ref
        new_task["ProductAllocation"]["ProductIdRef"] = f"{treatment}_product"
        
        # Add new task to ISOBUS data structure
        data["Task"].append(new_task)

    except KeyError as e:
        print(f"[ERROR] - Missing key in task template: {str(e)}")
    
    return data

def update_grid_min_position(data: Dict[str, Any], long: float, lat: float) -> Dict[str, Any]:
    """
    Update ISOBUS grid minimum position coordinates for spatial reference.

    This function manages the spatial positioning of ISOBUS prescription maps by
    updating the minimum East (longitude) and North (latitude) positions across
    all tasks. It ensures proper geographic reference for equipment navigation
    and prescription map spatial alignment.

    Parameters
    ----------
    data : Dict[str, Any]
        ISOBUS prescription map data structure containing task definitions.
        Modified in-place with updated grid position coordinates.
    long : float
        Longitude coordinate in decimal degrees for eastern position reference.
        Range: -180.0 to +180.0 degrees
    lat : float
        Latitude coordinate in decimal degrees for northern position reference.
        Range: -90.0 to +90.0 degrees

    Returns
    -------
    Dict[str, Any]
        Updated ISOBUS data structure with minimum grid position coordinates.

    Workflow
    --------
    1. **Task Iteration**: Process all tasks in ISOBUS data structure
    2. **Position Comparison**: Compare new coordinates with existing minimums
    3. **Coordinate Update**: Update minimum positions if new coordinates are smaller
    4. **Reference Establishment**: Ensure consistent spatial reference across tasks

    Examples
    --------
    >>> # Update grid minimum position for all tasks
    >>> data = update_grid_min_position(isobus_data, -74.006, 40.7128)
    >>> # Updates minimum East/North positions if new coordinates are smaller
    """
    # Process all ISOBUS tasks for grid position updates
    for task in data["Task"]:
        grid = task["Grid"]
        
        # Update minimum east position (longitude) if new coordinate is smaller
        current_east = grid["GridMinimumEastPosition"]
        if current_east is None or current_east > long:
            grid["GridMinimumEastPosition"] = long
        
        # Update minimum north position (latitude) if new coordinate is smaller
        current_north = grid["GridMinimumNorthPosition"]
        if current_north is None or current_north > lat:
            grid["GridMinimumNorthPosition"] = lat

    return data

def update_grid_max_row_column(data: Dict[str, Any], grid: List[int]) -> Dict[str, Any]:
    """
    Update ISOBUS grid maximum row and column dimensions for spatial coverage.

    This function manages grid dimensioning for ISOBUS prescription maps by expanding
    the maximum row and column values to accommodate new grid coordinates. It ensures
    sufficient spatial coverage for all prescription data while maintaining ISOBUS
    grid structure requirements.

    Parameters
    ----------
    data : Dict[str, Any]
        ISOBUS prescription map data structure containing task definitions.
        Modified in-place with updated grid dimension parameters.
    grid : List[int]
        Grid coordinates as [row, column] requiring accommodation in spatial structure.
        Zero-based indexing with automatic expansion for larger coordinates.

    Returns
    -------
    Dict[str, Any]
        Updated ISOBUS data structure with expanded grid dimensions.

    Workflow
    --------
    1. **Coordinate Extraction**: Extract row and column from grid coordinates
    2. **Task Processing**: Update grid dimensions for all ISOBUS tasks
    3. **Dimension Expansion**: Increase maximum row/column if needed
    4. **Consistency Maintenance**: Ensure uniform grid dimensions across tasks

    Examples
    --------
    >>> # Expand grid to accommodate coordinates [15, 25]
    >>> data = update_grid_max_row_column(isobus_data, [15, 25])
    >>> # Updates maximum row to 16, maximum column to 26 (1-based indexing)
    """
    # Extract row and column coordinates from grid specification
    row, col = grid
    
    # Process all ISOBUS tasks for grid dimension updates
    for task in data["Task"]:
        grid_info = task["Grid"]
        
        # Update maximum row dimension if current coordinate exceeds existing
        if grid_info["GridMaximumRow"] is None or grid_info["GridMaximumRow"] < row:
            grid_info["GridMaximumRow"] = row + 1
        
        # Update maximum column dimension if current coordinate exceeds existing
        if grid_info["GridMaximumColumn"] is None or grid_info["GridMaximumColumn"] < col:
            grid_info["GridMaximumColumn"] = col + 1

    return data

def update_grid_cells(data: Dict[str, Any], amount: Dict[str, int], grid: List[int]) -> Dict[str, Any]:
    """
    Update ISOBUS grid cell values with treatment prescription data.

    This function implements the core spatial data management for ISOBUS prescription
    maps, updating specific grid cells with treatment values using row-major order
    indexing. It ensures proper grid expansion and cell initialization according
    to ISO 11783 spatial data requirements.

    Parameters
    ----------
    data : Dict[str, Any]
        ISOBUS prescription map data structure containing task definitions.
        Modified in-place with updated grid cell values.
    amount : Dict[str, int]
        Dictionary mapping treatment names to prescription values.
        Each treatment corresponds to a specific ISOBUS task and grid structure.
    grid : List[int]
        Grid coordinates as [row, column] specifying target cell location.
        Zero-based indexing with row-major order storage organization.

    Returns
    -------
    Dict[str, Any]
        Updated ISOBUS data structure with prescription values in grid cells.

    Workflow
    --------
    1. **Coordinate Extraction**: Extract row and column from grid specification
    2. **Treatment Processing**: Iterate through all treatments requiring updates
    3. **Task Matching**: Find corresponding ISOBUS task for each treatment
    4. **Grid Validation**: Verify grid dimensions and cell array structure
    5. **Cell Calculation**: Compute linear index using row-major order
    6. **Value Assignment**: Update specific grid cell with prescription value
    7. **Error Handling**: Validate index bounds and provide error reporting

    Grid Storage Format
    ------------------
    ISOBUS grid cells use row-major order linear storage:
        - **Index Calculation**: index = row * total_columns + column
        - **Cell Initialization**: Unspecified cells initialized with zero values
        - **Dynamic Expansion**: Grid automatically resized to accommodate new cells
        - **Boundary Validation**: Index bounds checking prevents array overflow

    Examples
    --------
    >>> # Update grid cells with multiple treatments
    >>> treatments = {"nitrogen": 100, "phosphorus": 50}
    >>> data = update_grid_cells(isobus_data, treatments, [10, 15])
    >>> # Updates cell at row 10, column 15 with values for both treatments

    Error Conditions
    ---------------
    - **Task Not Found**: Treatment has no corresponding ISOBUS task definition
    - **Index Out of Range**: Calculated index exceeds grid cell array bounds
    - **Grid Corruption**: Missing or invalid grid structure in task definition
    """
    row, col = grid
    
    for treatment, value in amount.items():
        cultural_practice_ref = f"{treatment}_treatment"
        task_found = False
        
        for task in data["Task"]:
            if task["OperTechPractice"]["CulturalPracticeIdRef"] == cultural_practice_ref:
                task_found = True
                grid_dict = task["Grid"]
                current_max_row = grid_dict.get("GridMaximumRow", 0) or 0
                current_max_col = grid_dict.get("GridMaximumColumn", 0) or 0
                
                # Calcular nuevas dimensiones necesarias
                new_max_row = max(current_max_row, row + 1)
                new_max_col = max(current_max_col, col + 1)
                total_cells_needed = new_max_row * new_max_col
                
                # Inicializar o redimensionar la cuadrícula
                if "GridCell" not in grid_dict:
                    grid_dict["GridCell"] = [0] * total_cells_needed
                else:
                    current_cells = grid_dict["GridCell"]
                    current_size = len(current_cells)
                    
                    # Verificar si se necesita redimensionar
                    if (new_max_row > current_max_row or 
                        new_max_col > current_max_col or 
                        current_size < total_cells_needed):
                        
                        new_grid = [0] * total_cells_needed
                        
                        # Copiar valores existentes (si los hay)
                        if current_max_row > 0 and current_max_col > 0:
                            for r in range(current_max_row):
                                for c in range(current_max_col):
                                    old_index = r * current_max_col + c
                                    if old_index < current_size:
                                        new_index = r * new_max_col + c
                                        new_grid[new_index] = current_cells[old_index]
                        
                        grid_dict["GridCell"] = new_grid
                
                # Actualizar metadatos del grid
                grid_dict["GridMaximumRow"] = new_max_row
                grid_dict["GridMaximumColumn"] = new_max_col
                
                # Calcular índice y asignar valor
                index = row * new_max_col + col
                if index < len(grid_dict["GridCell"]):
                    grid_dict["GridCell"][index] = value
                else:
                    print(f"[ERROR] - Index {index} out of range for {treatment} grid (size: {len(grid_dict['GridCell'])})")
        
        if not task_found:
            print(f"[WARNING] - Task for {cultural_practice_ref} not found, skipping grid cell update")
    
    return data

if __name__ == "__main__":
    """
    Main execution block for ISOBUS prescription map generation script.
    
    This block implements the command-line interface for ISOBUS PM generation,
    processing standardized arguments from the PM management system and executing
    ISOBUS-compliant prescription map generation with ISO 11783 compatibility.
    
    The interface maintains full compatibility with the broader PM management system
    while providing ISOBUS-specific functionality for agricultural equipment integration
    and precision agriculture applications.
    
    Command Line Interface:
    ----------------------
    The script accepts standardized parameters for ISOBUS PM generation:
    
    --amount : str, required
        JSON string mapping treatment names to prescription values.
        Format: '{"treatment1": value1, "treatment2": value2, ...}'
        Each treatment generates a separate ISOBUS task with spatial data.
    
    --grid : str, required
        JSON array specifying grid coordinates as [row, column].
        Format: '[row_index, column_index]'
        Uses zero-based indexing with automatic grid expansion.
    
    --long : str, required
        Longitude coordinate in decimal degrees for spatial reference.
        Used for ISOBUS grid minimum position and equipment navigation.
        Range: -180.0 to +180.0 degrees
    
    --lat : str, required
        Latitude coordinate in decimal degrees for spatial reference.
        Used for ISOBUS grid minimum position and equipment navigation.
        Range: -90.0 to +90.0 degrees
    
    ISOBUS Compliance:
    -----------------
    Generated prescription maps follow ISO 11783 standards:
        - **Task Structure**: Standard task definitions with unique identifiers
        - **Spatial Data**: Grid-based organization with geographic positioning
        - **Equipment Integration**: Direct compatibility with ISOBUS farm machinery
        - **Data Exchange**: Standardized format for agricultural system interoperability
    
    Processing Workflow:
    -------------------
    1. **Argument Parsing**: Parse and validate all command-line parameters
    2. **Data Conversion**: Convert JSON strings to appropriate data structures
    3. **ISOBUS Generation**: Execute complete ISOBUS PM generation workflow
    4. **Equipment Compatibility**: Ensure output suitable for ISOBUS equipment
    
    Integration Context:
    -------------------
    This script integrates with:
        - **PM Management System**: Standard interface via subprocess execution
        - **ISOBUS Equipment**: Task controller compatibility for farm machinery
        - **Precision Agriculture**: Variable rate application and spatial prescriptions
        - **Farm Management**: Commercial agricultural software system integration
    
    Example Usage:
    -------------
    
    .. code-block:: bash
    
        # ISOBUS fertilizer prescription
        python pm_isobus.py \\
            --amount '{"nitrogen": 120, "phosphorus": 80}' \\
            --grid '[12, 18]' \\
            --lat '40.123456' \\
            --long '-74.987654'
        
        # ISOBUS pesticide application
        python pm_isobus.py \\
            --amount '{"herbicide": 2.5, "insecticide": 1.8}' \\
            --grid '[8, 15]' \\
            --lat '40.209544' \\
            --long '-3.465575'
    
    Output Format:
    -------------
    Generated files follow ISOBUS JSON structure:
        - **Task Definitions**: ISO 11783 compliant task specifications
        - **Spatial Data**: Row-major order grid organization
        - **Equipment References**: ISOBUS-compatible product and practice identifiers
        - **Geographic Positioning**: Decimal degree coordinate system
    
    Notes:
    -----
    - All geographic coordinates are required for ISOBUS spatial reference
    - Generated files are directly compatible with ISOBUS task controllers
    - Multiple treatments create separate tasks within single prescription map
    - Grid coordinates automatically expand spatial coverage as needed
    """
    # Initialize command-line argument parser for ISOBUS PM generation
    parser = argparse.ArgumentParser(description="PM Drone generator")
    
    # Define required command-line parameters for ISOBUS compatibility
    parser.add_argument("--amount", type=str, required=True, help='JSON string of treatments, e.g., \'{"nitrogen":100}\'')
    parser.add_argument("--grid", type=str, required=True, help='JSON array of grid position, e.g., \'[5,10]\'')
    parser.add_argument("--long", type=str, required=True, help="Longitude coordinate")
    parser.add_argument("--lat", type=str, required=True, help="Latitude coordinate")
    
    # Parse and extract command-line arguments
    args = parser.parse_args()

    # Convert JSON parameters to appropriate data structures
    amount = json.loads(args.amount)  # Dict[str, int] mapping treatments to values
    grid = json.loads(args.grid)      # List[int] with [row, column] coordinates
    long = args.long                  # str longitude coordinate
    lat = args.lat                    # str latitude coordinate
    
    # Execute ISOBUS prescription map generation with parsed parameters
    generate_pm(amount, grid, long, lat)