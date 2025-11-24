"""
GPS Simulator Module
===================

This module provides GPS coordinate simulation and storage functionality for drone
navigation systems. It implements a lightweight in-memory coordinate storage system
suitable for testing, simulation, and basic GPS coordinate management during
drone operations.

The module serves as a simplified GPS interface for development and testing environments
where actual GPS hardware is not available or when simulating specific coordinate
sequences for mission planning and testing scenarios.

.. module:: gps_simulator
    :synopsis: GPS coordinate simulation and storage for drone navigation systems

Features
--------
- **Coordinate Storage**: In-memory storage of latest GPS coordinates
- **Simple Interface**: Minimal API for coordinate save/retrieve operations
- **Error Handling**: Validation for uninitialized coordinate access
- **Type Safety**: Full type hints for coordinate data integrity
- **Thread Safety**: Global state management with simple access patterns

Workflow
--------
GPS Coordinate Management Pipeline:
    1. **Coordinate Reception**: Accept latitude/longitude from external sources
    2. **Data Validation**: Ensure coordinate data meets expected format
    3. **Storage Update**: Store coordinates in global memory location
    4. **Retrieval Service**: Provide access to most recent coordinates
    5. **Error Management**: Handle requests for uninitialized coordinates

Use Cases
---------
- **Mission Simulation**: Test flight paths with predefined coordinates
- **Development Testing**: Provide GPS data without hardware dependencies
- **Coordinate Logging**: Simple storage for waypoint tracking
- **System Integration**: Interface for GPS-dependent drone subsystems

Data Format
-----------
Coordinates are stored and retrieved as decimal degrees:
    - **Latitude**: -90.0 to +90.0 degrees (negative = South, positive = North)
    - **Longitude**: -180.0 to +180.0 degrees (negative = West, positive = East)
    - **Precision**: Full floating-point precision maintained
    - **Storage**: Tuple format (latitude, longitude)

Functions
---------
.. autofunction:: save_coordinates
.. autofunction:: get_latest_coordinates

Global Variables
----------------
latest_coordinates : tuple
    Global storage for the most recently saved GPS coordinates.
    Initialized to (None, None) indicating no coordinates have been set.

Exceptions
----------
ValueError
    Raised when attempting to retrieve coordinates before any have been saved.
    Indicates that the coordinate storage is in an uninitialized state.

Examples
--------
>>> # Save GPS coordinates
>>> save_coordinates(40.7128, -74.0060)  # New York City
>>> 
>>> # Retrieve saved coordinates
>>> lat, lon = get_latest_coordinates()
>>> print(f"Current position: {lat}, {lon}")
Current position: 40.7128, -74.006
>>> 
>>> # Handle uninitialized state
>>> try:
>>>     coords = get_latest_coordinates()
>>> except ValueError as e:
>>>     print(f"GPS Error: {e}")
GPS Error: Coordinates have not been set yet.

Integration Points
-----------------
This module integrates with:
    - **Sensors.take_photo**: GPS coordinates for image geotagging
    - **Mission Planning**: Waypoint validation and tracking
    - **GRPC Services**: Coordinate transmission to Mission Management
    - **Logging Systems**: Position tracking for flight analysis

Performance Notes
----------------
- **Memory Usage**: Minimal footprint with single tuple storage
- **Access Time**: O(1) constant time for save/retrieve operations
- **Thread Safety**: Global state requires external synchronization for concurrent access
- **Persistence**: In-memory only, coordinates lost on application restart

Limitations
----------
- **Single Coordinate**: Only stores most recent position
- **No History**: Previous coordinates are overwritten
- **No Persistence**: Data lost on application termination
- **No Validation**: Accepts any float values without coordinate validation

See Also
--------
Sensors.take_photo : GPS coordinate integration for image geotagging
GRPC.grpc_drone_metrics : GPS data transmission to Mission Management
"""

latest_coordinates = (None, None)  # Global variable storing latest GPS coordinates (lat, lon)

def save_coordinates(lat: float, lon: float) -> None:
    """
    Save the latest GPS coordinates to global storage.

    This function updates the global coordinate storage with new latitude and
    longitude values, replacing any previously stored coordinates. It serves
    as the primary interface for updating the drone's current position data
    from GPS sensors or simulation sources.

    Parameters
    ----------
    lat : float
        Latitude coordinate in decimal degrees.
        Valid range: -90.0 to +90.0 degrees
        - Negative values represent Southern hemisphere
        - Positive values represent Northern hemisphere
        - Zero represents the Equator
    lon : float
        Longitude coordinate in decimal degrees.
        Valid range: -180.0 to +180.0 degrees
        - Negative values represent Western hemisphere
        - Positive values represent Eastern hemisphere
        - Zero represents the Prime Meridian

    Returns
    -------
    None
        Function performs in-place update of global coordinate storage.

    Workflow
    --------
    1. **Global Access**: Access the global coordinate storage variable
    2. **Coordinate Update**: Replace existing coordinates with new values
    3. **Storage Confirmation**: New coordinates immediately available for retrieval

    Examples
    --------
    >>> # Save coordinates for New York City
    >>> save_coordinates(40.7128, -74.0060)
    >>> 
    >>> # Save coordinates for London
    >>> save_coordinates(51.5074, -0.1278)
    >>> 
    >>> # Save coordinates with high precision
    >>> save_coordinates(40.123456789, -74.987654321)

    Notes
    -----
    - Function overwrites previous coordinates without validation
    - No coordinate range validation is performed
    - Thread safety requires external synchronization for concurrent access
    - Coordinates are immediately available via get_latest_coordinates()

    See Also
    --------
    get_latest_coordinates : Retrieve stored coordinates
    """
    global latest_coordinates
    # Update global coordinate storage with new latitude and longitude values
    latest_coordinates = (lat, lon)

def get_latest_coordinates() -> tuple:
    """
    Retrieve the most recently saved GPS coordinates from global storage.

    This function provides access to the latest GPS coordinates stored in the
    global coordinate storage. It serves as the primary interface for accessing
    current position data for navigation, logging, and mission management systems.

    Returns
    -------
    tuple
        Tuple containing the latest GPS coordinates in the format (latitude, longitude).
        - **tuple[0]** (float): Latitude in decimal degrees (-90.0 to +90.0)
        - **tuple[1]** (float): Longitude in decimal degrees (-180.0 to +180.0)
        Both values maintain full floating-point precision as originally stored.

    Raises
    ------
    ValueError
        Raised when coordinates have not been initialized (still set to (None, None)).
        This indicates that save_coordinates() has not been called yet or the
        system is in an uninitialized state.

    Workflow
    --------
    1. **State Validation**: Check if coordinates have been initialized
    2. **Error Handling**: Raise ValueError if coordinates are uninitialized
    3. **Data Retrieval**: Return coordinate tuple if available
    4. **Type Consistency**: Ensure returned data matches expected format

    Examples
    --------
    >>> # Retrieve coordinates after saving
    >>> save_coordinates(40.7128, -74.0060)
    >>> lat, lon = get_latest_coordinates()
    >>> print(f"Latitude: {lat}, Longitude: {lon}")
    Latitude: 40.7128, Longitude: -74.006

    >>> # Handle uninitialized state
    >>> try:
    >>>     coords = get_latest_coordinates()
    >>>     print(f"Current position: {coords}")
    >>> except ValueError as e:
    >>>     print(f"GPS not ready: {e}")
    GPS not ready: Coordinates have not been set yet.

    >>> # Unpack coordinates directly
    >>> try:
    >>>     current_lat, current_lon = get_latest_coordinates()
    >>>     distance = calculate_distance(current_lat, current_lon, target_lat, target_lon)
    >>> except ValueError:
    >>>     print("GPS coordinates not available for navigation")

    Error Conditions
    ---------------
    - **Uninitialized State**: (None, None) indicates no coordinates have been saved
    - **System Restart**: Coordinates lost and must be re-initialized
    - **Memory Corruption**: Unexpected coordinate values require error handling

    Performance Characteristics
    --------------------------
    - **Access Time**: O(1) constant time retrieval
    - **Memory Usage**: No additional memory allocation
    - **Thread Safety**: Read operation safe but requires synchronization with writes

    Integration Usage
    ----------------
    Commonly used by:
        - **Navigation Systems**: Current position for flight path calculation
        - **Image Geotagging**: Coordinate embedding in captured photos
        - **Mission Logging**: Position tracking for flight analysis
        - **GRPC Services**: Coordinate transmission to Mission Management

    Notes
    -----
    - Coordinates are returned exactly as stored without validation
    - Function does not verify coordinate validity or range
    - Consider implementing coordinate validation in calling code
    - Thread safety requires external synchronization for concurrent access

    See Also
    --------
    save_coordinates : Store new GPS coordinates
    ValueError : Exception raised for uninitialized coordinates
    """
    # Validate that coordinates have been initialized before retrieval
    if latest_coordinates == (None, None):
        raise ValueError("Coordinates have not been set yet.")
    
    # Return the stored coordinate tuple
    return latest_coordinates