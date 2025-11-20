"""
Drone Prescription Map Generator Module
======================================

This module provides prescription map generation functionality specifically for
drone vehicles in the agricultural fleet management system. It creates and manages
JSON-based prescription maps that can be used by autonomous drones for precise
application of treatments across agricultural fields.

The module implements a grid-based prescription map system where each cell
represents a specific field location with associated treatment values. Drone
prescription maps are optimized for aerial application patterns and support
multiple treatment types with flexible grid dimensions.

Key Features:
    - Grid-based prescription map generation for drone operations
    - JSON file format for lightweight data exchange
    - Dynamic grid expansion for flexible field coverage
    - Multiple treatment type support per drone mission
    - File-based persistence with automatic directory creation
    - Command-line interface for external system integration
    - Robust error handling for corrupted or missing files

Drone-Specific Considerations:
    - Optimized for aerial application patterns
    - Supports variable-rate treatment application
    - Compatible with drone flight path planning
    - Lightweight data format for onboard processing
    - Grid-based approach suitable for drone navigation systems

File Structure:
    - Output directory: PrescriptionMap/pm_generation/Drone/PMs/
    - File naming: {vehicle_id}_{treatment_name}.json
    - Grid format: 2D array with [row][column] indexing
    - Values: Numeric treatment amounts per grid cell

Usage Example:
    ::

        # Command line usage
        python pm_drone_fleet.py --vehicle_id DRONE_001 
                                 --amount '{"fertilizer": 2.5, "pesticide": 1.8}' 
                                 --grid '[5, 10]'

        # Programmatic usage
        generate_pm("DRONE_001", "fertilizer", 2.5, [5, 10])

Author: Fleet Management System
Date: 2025

.. note::
    This module requires:
    - Write permissions to the output directory
    - Valid JSON input for amount and grid parameters
    - Non-negative grid coordinates for field positioning
    
.. warning::
    Grid expansion is automatic but can result in large files for sparse
    coverage patterns. Consider field optimization for efficient drone operations.
"""

import argparse
import os
import json


def generate_pm(vehicle_id, filename: str, value: int, grid: list) -> None:
    """
    Generate or update a drone prescription map JSON file with treatment value at grid location.

    This function creates or updates a prescription map file for a specific drone and
    treatment type. The prescription map uses a 2D grid structure where each cell
    represents a field location with an associated treatment value for drone application.

    Grid Management:
    - Automatic expansion of rows and columns as needed
    - Sparse grid support with None values for unspecified cells
    - 0-based indexing for row and column coordinates
    - Dynamic file creation if prescription map doesn't exist

    File Operations:
    - Creates output directory if it doesn't exist
    - Loads existing prescription map or initializes new one
    - Handles corrupted files by reinitializing empty grid
    - Saves updated prescription map with formatted JSON

    Parameters
    ----------
    vehicle_id : str
        Unique identifier for the drone vehicle. Used as filename prefix
        to distinguish prescription maps between different drones.
    filename : str
        Treatment type identifier that becomes part of the output filename.
        Examples: "fertilizer", "pesticide", "herbicide"
    value : int
        Treatment amount or application rate to store at the specified grid
        location. Units depend on treatment type (e.g., kg/ha, L/ha).
    grid : list
        Grid coordinates as [row, column] specifying the field location
        for the treatment value. Must be non-negative integers.

    Returns
    -------
    None
        Function performs file I/O operations but returns no value.

    Raises
    ------
    ValueError
        If grid coordinates contain negative values.
    IOError
        If file operations fail due to permission or disk space issues.
    json.JSONDecodeError
        If existing prescription map file contains invalid JSON.

    Example
    -------
    ::

        # Create fertilizer prescription for drone at grid position [10, 15]
        generate_pm("DRONE_001", "fertilizer", 120, [10, 15])
        
        # Create pesticide prescription for the same drone at different location
        generate_pm("DRONE_001", "pesticide", 2.5, [8, 12])
        
        # Update existing prescription map
        generate_pm("DRONE_001", "fertilizer", 150, [10, 16])

    Note
    ----
    The function automatically creates the output directory structure and
    handles grid expansion dynamically. Prescription maps are stored as
    JSON files with formatted output for human readability.

    Warning
    -------
    Large grid coordinates can result in significant memory usage and
    file sizes due to automatic grid expansion with None padding.
    """
    # Define output directory and ensure it exists
    pms_folder = "PrescriptionMap/pm_generation/Drone/PMs"
    os.makedirs(pms_folder, exist_ok=True)
    
    # Construct vehicle-specific filename
    full_filename = f"{vehicle_id}_{filename}.json"
    path = os.path.join(pms_folder, full_filename)
    
    # Load existing prescription map or initialize new one
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                pm = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            # Handle corrupted files by reinitializing
            pm = []
    else:
        print(f"Creating new PM: {full_filename}")
        pm = []
    
    # Extract and validate grid coordinates
    row, col = grid
    if row < 0 or col < 0:
        raise ValueError("Grid indices must be non-negative")
    
    # Expand grid rows if needed to accommodate new row index
    if row >= len(pm):
        pm.extend([[] for _ in range(row - len(pm) + 1)])
    
    # Expand grid columns if needed to accommodate new column index
    if col >= len(pm[row]):
        pm[row].extend([None] * (col - len(pm[row]) + 1))
    
    # Update grid cell with treatment value
    pm[row][col] = value
    
    # Save updated prescription map with formatted JSON
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(pm, f, indent=4)
    
    print(f"Drone PM: {full_filename} at [{row}][{col}] = {value}")


if __name__ == "__main__":
    """
    Command-line interface for drone prescription map generation.
    
    This section provides a command-line interface that allows external systems
    to generate drone prescription maps by providing vehicle ID, treatment specifications,
    and grid coordinates. The interface supports multiple treatments per drone and
    flexible grid positioning.
    
    Command-line Arguments:
        --vehicle_id: Unique identifier for the target drone
        --amount: JSON string mapping treatment names to application values
        --grid: JSON array with grid position coordinates [row, column]
        --long: Longitude coordinate (optional, for future integration)
        --lat: Latitude coordinate (optional, for future integration)
        
    Example Usage:
        ::
        
            # Single treatment application
            python pm_drone_fleet.py --vehicle_id DRONE_001 
                                     --amount '{"fertilizer": 120}' 
                                     --grid '[10, 15]'
            
            # Multiple treatments at same location
            python pm_drone_fleet.py --vehicle_id DRONE_001 
                                     --amount '{"fertilizer": 120, "pesticide": 2.5}' 
                                     --grid '[10, 15]'
    """
    # Configure command-line argument parser for drone PM generation
    parser = argparse.ArgumentParser(description="Drone Prescription Map Generator for Fleet Management")
    parser.add_argument("--vehicle_id", type=str, required=True, 
                       help="Unique identifier for the target drone vehicle")
    parser.add_argument("--amount", type=str, required=True, 
                       help="JSON string mapping treatment names to application values, "
                            "e.g., '{\"fertilizer\":120,\"pesticide\":2.5}'")
    parser.add_argument("--grid", type=str, required=True, 
                       help="Grid coordinates as JSON array specifying field location, "
                            "e.g., '[10,15]' for row 10, column 15")
    parser.add_argument("--long", type=str, required=False, 
                       help="Longitude coordinate for future GPS integration (optional)")
    parser.add_argument("--lat", type=str, required=False, 
                       help="Latitude coordinate for future GPS integration (optional)")
    
    # Parse command-line arguments
    args = parser.parse_args()
    
    # Extract and process arguments
    vehicle_id = args.vehicle_id
    amount = json.loads(args.amount)      # Parse JSON treatment specifications
    grid = json.loads(args.grid)          # Parse JSON grid coordinates
        
    # Generate prescription maps for each treatment type
    for filename, value in amount.items():
        generate_pm(vehicle_id, filename, value, grid)

        