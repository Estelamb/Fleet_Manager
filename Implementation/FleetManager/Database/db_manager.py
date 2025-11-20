"""
Database operation handler module.

This module provides functionality for:
- Managing MariaDB connections and transactions
- Processing different types of database requests
- Handling state vector data insertion
- Comprehensive error handling and logging
"""

import json
import mariadb
import logging
from typing import Any, Tuple, Dict, List

def run_db_manager(db_request: List[str], db_logger: logging.Logger) -> None:
    """Execute database operations for incoming requests.

    Handles the full database operation lifecycle:
    1. Parse incoming request data
    2. Establish database connection
    3. Generate appropriate SQL statement
    4. Execute transaction
    5. Handle connection cleanup

    Args:
        db_request (List[str]): List of string elements comprising the request
        db_logger (logging.Logger): Configured logger instance

    Raises:
        json.JSONDecodeError: If invalid JSON is received
        mariadb.Error: For database connection/operation failures

    Example:
        >>> run_db_manager(['StateVector', '{"time": "2023-01-01"}'], logger)
    """
    config = {
        'user': 'fleet',
        'password': 'fleet',
        'host': 'localhost',
        'database': 'fleet_database'
    }

    try:
        message_grpc_str = ''.join(db_request)
        db_data = json.loads(message_grpc_str)
    except json.JSONDecodeError as e:
        db_logger.error(f"[DB Manager] - JSON decode error: {str(e)}")
        raise

    try:
        with mariadb.connect(**config) as conn:
            with conn.cursor() as cursor:
                sql, values, log_msg = message_management(db_data, db_logger)
                cursor.execute(sql, values)
                conn.commit()
                db_logger.info(log_msg)

    except mariadb.Error as e:
        db_logger.error(f"[DB Manager] - Database error: {str(e)}")
        raise
    finally:
        db_logger.info("[DB Manager] - Connection closed" if 'conn' in locals() 
                      else "[DB Manager] - Connection never established")

def message_management(
    db_data: Tuple[str, Dict[str, Any]],
    db_logger: logging.Logger
) -> Tuple[str, tuple, str]:
    """Generate SQL statements and values based on request type.

    Args:
        db_data (Tuple[str, Dict[str, Any]]): Tuple containing:
            - Request type identifier as string
            - Data dictionary with field/value pairs
        db_logger (logging.Logger): Configured logger instance

    Returns:
        Tuple[str, tuple, str]: Contains:
            - SQL query string
            - Parameter values tuple
            - Log message

    Raises:
        ValueError: For unsupported request types

    Example:
        >>> message_management(('StateVector', {...}), logger)
    """
    request_type, data = db_data
    
    if request_type == 'StateVector':
        db_logger.info("[DB Manager] - State Vector data received")
        
        insert_sql = """
        INSERT INTO state_vector (
            time, vehicle_id, vehicle_status, battery_capacity, battery_percentage,
            last_update, longitude, latitude, altitude, roll, pitch, yaw,
            gimbal_pitch, linear_speed
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        values = (
            data['time'], data['vehicle_id'], data['vehicle_status'],
            data['battery_capacity'], data['battery_percentage'],
            data['last_update'], data['longitude'], data['latitude'],
            data['altitude'], data['roll'], data['pitch'], data['yaw'],
            data['gimbal_pitch'], data['linear_speed']
        )
        
        return insert_sql, values, "[DB Manager] - State Vector data inserted successfully"
    
    else:
        error_msg = f"Unsupported request type: {request_type}"
        db_logger.error(f"[DB Manager] - {error_msg}")
        raise ValueError(error_msg)