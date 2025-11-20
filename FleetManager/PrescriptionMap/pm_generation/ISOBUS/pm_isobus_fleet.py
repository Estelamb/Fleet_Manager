"""
ISOBUS Prescription Map Generator Module
=======================================

This module provides prescription map generation functionality specifically for
ISOBUS-compatible agricultural vehicles in the fleet management system. It creates
ISOBUS-compliant prescription maps based on treatment specifications, field grids,
and geographic coordinates.

The module generates ISO 11783 compliant prescription maps that can be directly
used by ISOBUS-enabled agricultural machinery for precise application of treatments
such as fertilizers, pesticides, and other agricultural inputs.

Key Features:
    - ISOBUS ISO 11783 standard compliance
    - Grid-based prescription map generation
    - Multiple treatment support (fertilizer, pesticide, etc.)
    - Dynamic task creation and management
    - Coordinate-based field positioning
    - JSON-based configuration and output
    - Command-line interface for external integration

ISOBUS Compliance:
    The generated prescription maps follow the ISO 11783 standard for agricultural
    data exchange, ensuring compatibility with ISOBUS-enabled farm equipment from
    various manufacturers.

File Structure:
    - Header template: Contains ISOBUS header information
    - Task template: Defines treatment task structure
    - Output directory: Stores generated prescription maps

Usage Example:
    ::

        # Command line usage
        python pm_isobus_fleet.py --vehicle_id TRACTOR_001 
                                  --amount '{"nitrogen": 120, "phosphorus": 80}' 
                                  --grid '[10, 15]' 
                                  --long -3.7038 
                                  --lat 40.4168

        # Programmatic usage
        generate_pm("TRACTOR_001", {"nitrogen": 120}, [10, 15], -3.7038, 40.4168)

Author: Fleet Management System
Date: 2025

.. note::
    This module requires:
    - ISOBUS header and task template files
    - Write permissions to the output directory
    - Valid JSON template configurations
    
.. warning::
    Generated prescription maps must be validated with target ISOBUS equipment
    before field deployment to ensure compatibility and safety.
"""

import argparse
import json
import os
import copy

# Configuration paths for ISOBUS templates and output
HEADER = "PrescriptionMap/pm_generation/ISOBUS/isobus_header.json"
TASK = "PrescriptionMap/pm_generation/ISOBUS/isobus_task.json"
FOLDER = "PrescriptionMap/pm_generation/ISOBUS/PMs"


def generate_pm(vehicle_id, amount: dict, grid: list, long: float, lat: float) -> None:
    """
    Generate ISOBUS-compliant prescription map for a specific vehicle.
    
    This function creates or updates an ISOBUS prescription map file for the
    specified vehicle, incorporating treatment amounts, field grid positions,
    and geographic coordinates. The generated map follows ISO 11783 standards
    for compatibility with ISOBUS agricultural equipment.
    
    Processing Workflow:
    1. Load or create prescription map data structure
    2. Ensure tasks exist for all specified treatments
    3. Update grid positioning based on coordinates
    4. Configure grid dimensions based on field layout
    5. Populate grid cells with treatment amounts
    6. Save ISOBUS-compliant JSON file
    
    Args:
        vehicle_id (str): Unique identifier for the target vehicle/implement
        amount (dict): Treatment amounts mapped by treatment type, e.g.,
                      {"nitrogen": 120, "phosphorus": 80}
        grid (list): Grid position as [row, column] coordinates for the
                    prescription map cell location
        long (float): Longitude coordinate for field positioning
        lat (float): Latitude coordinate for field positioning
        
    Example:
        ::
        
            # Generate PM for nitrogen application
            generate_pm(
                vehicle_id="TRACTOR_001",
                amount={"nitrogen": 120, "phosphorus": 80},
                grid=[10, 15],
                long=-3.7038,
                lat=40.4168
            )
            
    Note:
        The function automatically creates the output directory if it doesn't
        exist and handles file corruption by creating new prescription maps
        when necessary.
        
    Warning:
        Template files (header and task) must be valid JSON and contain the
        required ISOBUS structure. Missing or corrupted templates will cause
        generation to fail.
    """
    # Construct output file path for vehicle-specific prescription map
    path = os.path.join(FOLDER, f"{vehicle_id}_isobus_pm.json")
    
    # Load existing prescription map or initialize new one
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print("[WARNING] - PM file corrupted or not found, creating new one")
            data = create_new_pm()
    else:
        data = create_new_pm()
    
    # Exit if data initialization failed
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
        
    # Process each treatment and ensure corresponding tasks exist
    for treatment in amount:
        data = ensure_task_exists(treatment, data, task_template)
        
    # Update prescription map with coordinate and grid information
    data = update_grid_min_position(data, long, lat)
    data = update_grid_max_row_column(data, grid)
    data = update_grid_cells(data, amount, grid)
    
    # Save updated prescription map to file
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
        
    print(f"ISOBUS PM updated at {path} with treatments: {amount} at grid: {grid}")


def create_new_pm():
    """
    Create a new ISOBUS prescription map data structure.
    
    This function initializes a new prescription map by loading the ISOBUS
    header template and setting up the basic data structure required for
    ISO 11783 compliance. It ensures that the Task list is properly
    initialized for subsequent treatment additions.
    
    The function handles missing or corrupted header files gracefully by
    creating a minimal valid structure that can be extended with treatments
    and grid information.
    
    Returns:
        dict or None: Initialized prescription map data structure with header
                     information and empty task list, or None if critical
                     errors prevent initialization
                     
    Example:
        ::
        
            # Create new prescription map structure
            pm_data = create_new_pm()
            if pm_data:
                print("Prescription map initialized successfully")
            else:
                print("Failed to initialize prescription map")
                
    Note:
        The function automatically creates an empty Task list if the header
        template doesn't contain one or if it's not in the correct format.
        
    Warning:
        Header template corruption or missing files will result in a minimal
        data structure that may lack important ISOBUS metadata.
    """
    # Initialize data structure
    data = {}
    
    # Load ISOBUS header template if available
    try:
        if os.path.exists(HEADER):
            with open(HEADER, "r") as f:
                loaded = json.load(f)
                if isinstance(loaded, dict):
                    data = loaded
                else:
                    print(f"[WARNING] - Header file is not a dictionary, using empty structure")
    except Exception as e:
        print(f"[ERROR] - Failed to load header: {str(e)}")
    
    # Ensure Task list exists and is properly initialized
    if "Task" not in data or not isinstance(data["Task"], list):
        data["Task"] = []
    
    return data


def ensure_task_exists(treatment, data, task_template):
    """
    Ensure that a task exists for the specified treatment in the prescription map.
    
    This function checks if a task for the given treatment already exists in the
    prescription map data. If not found, it creates a new task based on the
    provided template, configuring it with treatment-specific identifiers and
    references according to ISOBUS standards.
    
    Task Creation Process:
    1. Check for existing task with matching treatment reference
    2. If not found, create new task from template
    3. Configure task ID with sequential numbering
    4. Set treatment-specific cultural practice reference
    5. Configure product allocation reference
    6. Add task to prescription map data structure
    
    Args:
        treatment (str): Treatment identifier (e.g., "nitrogen", "phosphorus")
        data (dict): Current prescription map data structure
        task_template (dict): ISOBUS task template with required structure
        
    Returns:
        dict: Updated prescription map data with task ensured for treatment
        
    Example:
        ::
        
            # Ensure nitrogen treatment task exists
            data = ensure_task_exists("nitrogen", pm_data, task_template)
            
            # Multiple treatments
            for treatment in ["nitrogen", "phosphorus", "potassium"]:
                data = ensure_task_exists(treatment, data, task_template)
                
    Note:
        Tasks are assigned sequential IDs (TSK1, TSK2, etc.) based on the
        current number of tasks in the prescription map.
        
    Warning:
        Template structure must contain valid ISOBUS task format. Missing
        required keys will result in error messages and partial task creation.
    """
    # Generate cultural practice reference for treatment
    cultural_practice_ref = f"{treatment}_treatment"
    
    # Check if task already exists for this treatment
    for task in data["Task"]:
        if task["OperTechPractice"]["CulturalPracticeIdRef"] == cultural_practice_ref:
            return data

    # Create new task from template for the treatment
    try:
        new_task = copy.deepcopy(task_template["Task"][0])
        number_of_tasks = len(data["Task"])+1
        
        # Configure task with treatment-specific identifiers
        new_task["TaskId"] = f"TSK{number_of_tasks}"
        new_task["OperTechPractice"]["CulturalPracticeIdRef"] = cultural_practice_ref
        new_task["ProductAllocation"]["ProductIdRef"] = f"{treatment}_product"
        
        # Add configured task to prescription map
        data["Task"].append(new_task)

    except KeyError as e:
        print(f"[ERROR] - Missing key in task template: {str(e)}")
    
    return data


def update_grid_min_position(data, long, lat):
    """
    Update grid minimum position coordinates for all tasks in the prescription map.
    
    This function updates the minimum east (longitude) and north (latitude)
    positions for the prescription map grid. It ensures that the grid boundaries
    are correctly set to encompass all field areas where treatments will be applied.
    
    The function processes all tasks in the prescription map and updates their
    grid minimum positions if the provided coordinates represent new minimum
    values (further west for longitude, further south for latitude).
    
    Args:
        data (dict): Prescription map data structure containing tasks
        long (float): Longitude coordinate (east position)
        lat (float): Latitude coordinate (north position)
        
    Returns:
        dict: Updated prescription map data with corrected grid minimum positions
        
    Example:
        ::
        
            # Update grid boundaries for new field area
            data = update_grid_min_position(pm_data, -3.7038, 40.4168)
            
        Note:
            The function only updates minimum positions if the new coordinates
            represent actual minimums (westernmost longitude, southernmost latitude).
            
        Warning:
            Coordinate system must be consistent throughout the prescription map.
            Mixed coordinate systems will result in incorrect grid positioning.
    """
    # Update minimum position coordinates for all tasks
    for task in data["Task"]:
        grid = task["Grid"]
        
        # Update minimum east position (longitude) if new value is more western
        current_east = grid["GridMinimumEastPosition"]
        if current_east is None or current_east > long:
            grid["GridMinimumEastPosition"] = long
        
        # Update minimum north position (latitude) if new value is more southern
        current_north = grid["GridMinimumNorthPosition"]
        if current_north is None or current_north > lat:
            grid["GridMinimumNorthPosition"] = lat

    return data


def update_grid_max_row_column(data, grid):
    """
    Update maximum row and column values for the prescription map grid.
    
    This function updates the grid dimensions by setting maximum row and column
    values based on the provided grid coordinates. It ensures that the grid
    boundaries are sufficient to contain all specified positions.
    
    The function processes all tasks and updates their grid maximum dimensions
    if the provided coordinates exceed the current maximum values. Grid
    indexing is adjusted to be 1-based as required by ISOBUS standards.
    
    Args:
        data (dict): Prescription map data structure containing tasks
        grid (list): Grid coordinates as [row, column] (0-based indexing)
        
    Returns:
        dict: Updated prescription map data with corrected grid maximum dimensions
        
    Example:
        ::
        
            # Update grid dimensions for position [10, 15]
            data = update_grid_max_row_column(pm_data, [10, 15])
            # Results in GridMaximumRow = 11, GridMaximumColumn = 16
            
    Note:
        The function adds 1 to grid coordinates to convert from 0-based to
        1-based indexing as required by ISOBUS specification.
        
    Warning:
        Grid coordinates must be non-negative integers. Invalid coordinates
        may result in incorrect grid dimensions.
    """
    # Extract row and column from grid coordinates
    row, col = grid
    
    # Update maximum row and column for all tasks
    for task in data["Task"]:
        grid_info = task["Grid"]
        
        # Update maximum row (convert to 1-based indexing)
        if grid_info["GridMaximumRow"] is None or grid_info["GridMaximumRow"] < row:
            grid_info["GridMaximumRow"] = row + 1
        
        # Update maximum column (convert to 1-based indexing)
        if grid_info["GridMaximumColumn"] is None or grid_info["GridMaximumColumn"] < col:
            grid_info["GridMaximumColumn"] = col + 1

    return data


def update_grid_cells(data, amount, grid):
    """
    Update grid cell values with treatment amounts for the prescription map.
    
    This function populates the prescription map grid cells with the specified
    treatment amounts at the given grid coordinates. It handles grid cell
    initialization, extension, and value assignment for each treatment type.
    
    Cell Management Process:
    1. Calculate total grid size based on maximum row/column dimensions
    2. Initialize or extend grid cell arrays as needed
    3. Calculate linear index from row/column coordinates
    4. Update cell values with treatment amounts
    5. Handle boundary conditions and error cases
    
    Args:
        data (dict): Prescription map data structure containing tasks
        amount (dict): Treatment amounts by treatment type
        grid (list): Grid coordinates as [row, column] for cell positioning
        
    Returns:
        dict: Updated prescription map data with populated grid cell values
        
    Example:
        ::
        
            # Update grid cell at position [10, 15] with treatment amounts
            amounts = {"nitrogen": 120, "phosphorus": 80}
            data = update_grid_cells(pm_data, amounts, [10, 15])
            
    Note:
        Grid cells use row-major ordering for linear indexing. The function
        automatically extends grid cell arrays if they're too small for the
        current grid dimensions.
        
    Warning:
        Grid coordinates must be within the maximum row/column boundaries.
        Out-of-bounds coordinates will result in error messages and skipped
        cell updates.
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

    # To test correct comparison
    #row, col = grid
    #
    ## Process each treatment and update corresponding grid cells
    #for treatment, value in amount.items():
    #    cultural_practice_ref = f"{treatment}_treatment"
    #    task_found = False
    #    
    #    # Find the task corresponding to this treatment
    #    for task in data["Task"]:
    #        if task["OperTechPractice"]["CulturalPracticeIdRef"] == cultural_practice_ref:
    #            task_found = True
    #            grid_dict = task["Grid"]
    #            max_row = grid_dict["GridMaximumRow"] or 0
    #            max_col = grid_dict["GridMaximumColumn"] or 0
    #            
    #            # Calculate total grid dimensions and cell count
    #            total_rows = max_row
    #            total_cols = max_col
    #            total_cells = total_rows * total_cols
    #            
    #            # Initialize or extend grid cell array as needed
    #            if not grid_dict.get("GridCell"):
    #                grid_dict["GridCell"] = [0] * total_cells
    #            elif len(grid_dict["GridCell"]) < total_cells:
    #                # Extend with zeros if current array is too small
    #                grid_dict["GridCell"].extend([0] * (total_cells - len(grid_dict["GridCell"])))
    #            
    #            # Calculate linear index using row-major ordering
    #            index = row * total_cols + col
    #            
    #            # Update the specific grid cell with treatment value
    #            if index < len(grid_dict["GridCell"]):
    #                grid_dict["GridCell"][index] = value
    #            else:
    #                print(f"[ERROR] - Index {index} out of range for {treatment} grid (size: {len(grid_dict['GridCell'])})")
    #    
    #    # Log warning if no matching task was found for treatment
    #    if not task_found:
    #        print(f"[WARNING] - Task for {cultural_practice_ref} not found, skipping grid cell update")
    #
    #return data


if __name__ == "__main__":
    """
    Command-line interface for ISOBUS prescription map generation.
    
    This section provides a command-line interface that allows external systems
    to generate ISOBUS prescription maps by providing vehicle ID, treatment amounts,
    grid coordinates, and field positioning information as arguments.
    
    Command-line Arguments:
        --vehicle_id: Unique identifier for the target vehicle/implement
        --amount: JSON string containing treatment amounts by type
        --grid: JSON array with grid position coordinates [row, column]
        --long: Longitude coordinate for field positioning
        --lat: Latitude coordinate for field positioning
        
    Example Usage:
        ::
        
            python pm_isobus_fleet.py --vehicle_id TRACTOR_001 
                                      --amount '{"nitrogen": 120, "phosphorus": 80}' 
                                      --grid '[10, 15]' 
                                      --long -3.7038 
                                      --lat 40.4168
    """
    # Configure command-line argument parser
    parser = argparse.ArgumentParser(description="ISOBUS Prescription Map Generator for Fleet Management")
    parser.add_argument("--vehicle_id", type=str, required=True, 
                       help="Unique identifier for the target vehicle/implement")
    parser.add_argument("--amount", type=str, required=True, 
                       help='JSON string of treatment amounts, e.g., \'{"nitrogen":120,"phosphorus":80}\'')
    parser.add_argument("--grid", type=str, required=True, 
                       help='JSON array of grid position coordinates, e.g., \'[10,15]\'')
    parser.add_argument("--long", type=str, required=True, 
                       help="Longitude coordinate for field positioning")
    parser.add_argument("--lat", type=str, required=True, 
                       help="Latitude coordinate for field positioning")
    
    # Parse command-line arguments
    args = parser.parse_args()

    # Extract and process arguments
    vehicle_id = args.vehicle_id
    amount = json.loads(args.amount)      # Parse JSON treatment amounts
    grid = json.loads(args.grid)          # Parse JSON grid coordinates
    long = args.long                      # Longitude coordinate
    lat = args.lat                        # Latitude coordinate
    
    # Generate ISOBUS prescription map with provided parameters
    generate_pm(vehicle_id, amount, grid, long, lat)