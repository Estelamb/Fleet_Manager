"""
This module provides database configuration and table creation functionality 
for the fleet management system using MariaDB.

.. warning::
    Contains hardcoded credentials - consider using environment variables
    or configuration files in production environments.
"""
import mariadb
import sys
import logging

def create_db(db_logger: logging.Logger):
    """Initialize database schema and create state vector table if not exists.

    Performs the following operations:
    1. Establishes database connection using configured credentials
    2. Creates state_vector table with defined schema
    3. Sets up proper indexing for common query patterns
    4. Handles connection cleanup and error states

    :param db_logger: Configured logger instance for database operations
    :type db_logger: logging.Logger

    :raises mariadb.Error: For database connection/execution errors
    :raises SystemExit: On fatal database connection failure

    Example:
        Basic usage::
            
            logger = logging.getLogger('DB')
            create_db(logger)

    .. note::
        Table Structure:
        - Stores real-time vehicle telemetry and status
        - Indexed on vehicle_id and time for temporal queries
        - Uses InnoDB engine for transaction support
        - UTF8mb4 encoding for full Unicode support
    """
    
    # Database configuration
    config = {
        'user': 'fleet',
        'password': 'fleet',
        'host': 'localhost',
        'database': 'fleet_database'
    }

    # Create table SQL (correct - no 'taken' column)
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS state_vector (
        id INT AUTO_INCREMENT PRIMARY KEY,
        time DATETIME,
        vehicle_id INT,
        vehicle_status VARCHAR(50),
        battery_capacity DOUBLE,
        battery_percentage DOUBLE,
        last_update DATETIME,
        longitude DOUBLE,
        latitude DOUBLE,
        altitude DOUBLE,
        roll DOUBLE,
        pitch DOUBLE,
        yaw DOUBLE,
        gimbal_pitch DOUBLE,
        linear_speed DOUBLE,
        INDEX idx_vehicle (vehicle_id),
        INDEX idx_time (time)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """

    try:
        # Establish connection
        conn = mariadb.connect(**config)
        cursor = conn.cursor()

        # Create table
        cursor.execute(create_table_sql)
        db_logger.info(" - Table created successfully!")

    except mariadb.Error as e:
        db_logger(" - Error connecting to MariaDB: {e}")
        sys.exit(1)

    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()
            db_logger.info(" - Connection closed.")