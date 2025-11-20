"""
REST API Default Controller Module
=================================

This module provides the core REST API functionality for mission management in the
Fleet Management System. It implements HTTP endpoints for mission submission and
integrates with gRPC services for processing agricultural mission data.

The module serves as the primary entry point for external systems to submit
agricultural missions to the fleet management system, handling JSON validation,
data transformation, and integration with the backend processing pipeline.

Key Features:
    - RESTful mission submission endpoint
    - JSON schema validation and deserialization
    - gRPC client integration for backend processing
    - Comprehensive error handling and status reporting
    - Thread-safe concurrent logging with file rotation
    - HTTP status code compliance for API standards

Architecture Overview:
    The controller follows a layered architecture where:
    - HTTP requests are received via Connexion framework
    - JSON payloads are validated against OpenAPI schemas
    - Mission objects are deserialized and processed
    - Data is forwarded to gRPC services for distribution
    - Responses include mission IDs or detailed error messages

API Endpoints:
    - POST /mission: Submit agricultural mission for processing

Integration Points:
    - Mission validation using OpenAPI schema definitions
    - gRPC communication for backend service coordination
    - Centralized logging for operation monitoring and debugging

Usage Example:
    ::

        # Submit mission via HTTP POST
        curl -X POST http://localhost:8080/mission \\
             -H "Content-Type: application/json" \\
             -d '{
                 "mission_id": "MISSION_001",
                 "fields": [...],
                 "vehicles": [...],
                 "tasks": [...]
             }'

Author: Fleet Management System
Date: 2025

.. note::
    This module requires:
    - Connexion framework for OpenAPI integration
    - Valid mission schema definitions
    - gRPC service availability for backend processing
    
.. warning::
    Ensure proper error handling for production deployments as mission
    submission failures can impact agricultural operations scheduling.
"""

import connexion
import six
import json
import logging
from concurrent_log_handler import ConcurrentRotatingFileHandler

from REST.models.mission import Mission  # noqa: E501
from REST.models.mission_id_response import MissionIdResponse  # noqa: E501
from REST import util
from REST.grpc_rest import run_rest_client


def mission_post(body):  # noqa: E501
    """
    Submit an agricultural mission and receive the mission ID confirmation.

    This endpoint serves as the primary interface for external systems to submit
    agricultural missions to the Fleet Management System. It handles complete
    mission processing workflow including validation, transformation, and
    forwarding to backend gRPC services for execution.

    Processing Workflow:
    1. **Request Validation**: Verify JSON content type and payload structure
    2. **Schema Validation**: Deserialize JSON against Mission schema
    3. **Data Transformation**: Convert Mission object to JSON for gRPC transport
    4. **Backend Integration**: Forward mission to gRPC services for processing
    5. **Response Generation**: Return mission ID or detailed error information

    Mission Schema Requirements:
    The mission payload must conform to the OpenAPI Mission schema including:
    - mission_id: Unique identifier for the agricultural mission
    - fields: Array of field definitions with coordinates and properties
    - vehicles: Array of assigned vehicles with capabilities and status
    - tasks: Array of agricultural tasks with treatment specifications

    Error Handling Strategy:
    - 400: Invalid JSON format or missing required fields
    - 500: Backend processing failures or gRPC communication errors
    - 200: Successful mission submission with confirmation ID

    Args:
        body: The mission data payload from HTTP request. Expected to be JSON
              format conforming to the Mission schema definition. Contains
              complete agricultural mission specification including fields,
              vehicles, and task definitions.

    Returns:
        tuple: A tuple containing either:
            - Success: (MissionIdResponse(mission_id=str), 200)
            - Client Error: (str error_message, 400)
            - Server Error: (str error_message, 500)

    Raises:
        ValidationError: When input data doesn't match the expected Mission schema
        JSONDecodeError: When payload contains invalid JSON syntax
        ConnectionError: When gRPC backend services are unavailable

    Example:
        ::

            # Successful mission submission
            response, status = mission_post({
                "mission_id": "MISSION_001",
                "fields": [
                    {
                        "field_id": "F001",
                        "coordinates": [[lat, lng], ...],
                        "area": 100.5,
                        "crop_type": "wheat"
                    }
                ],
                "vehicles": [
                    {
                        "vehicle_id": "DRONE_001", 
                        "type": "drone",
                        "capabilities": ["spraying", "monitoring"]
                    }
                ],
                "tasks": [
                    {
                        "task_id": "T001",
                        "type": "pesticide_application",
                        "field_id": "F001",
                        "vehicle_id": "DRONE_001"
                    }
                ]
            })
            # Returns: (MissionIdResponse(mission_id="MISSION_001"), 200)

    Note:
        The function creates a logger instance for each request to ensure
        proper request tracking and debugging capabilities.

    Warning:
        Mission submission failures can impact agricultural operation scheduling.
        Ensure proper monitoring and retry mechanisms for production deployments.
    """
    rest_logger = create_rest_logger()
    
    if connexion.request.is_json:
        rest_logger.info("[REST Server] - Received Mission")
        
        # Deserialize JSON input to Mission object
        mission = Mission.from_dict(connexion.request.get_json())  # noqa: E501

        # Convert Mission object to dictionary and then to JSON string
        mission_json = json.dumps(mission.to_dict())

        # Send the mission to gRPC client and get confirmation
        confirmation = run_rest_client(mission_json, rest_logger)
        
        if confirmation:
            return MissionIdResponse(mission_id=confirmation), 200
        else:
            rest_logger.error("Failed to send mission to gRPC client")
            return 'Failed to process mission submission', 500
    
    rest_logger.error("Received invalid JSON payload")
    return 'Invalid request format - expected JSON', 400


def create_rest_logger():
    """Create and configure a concurrent logger for REST operations.

    Configures a logger with:
    - Rotating file handler (max 1MB per file, 5 backups)
    - Console stream handler
    - Unified formatting with timestamp, name, and log level

    :return: Configured logger instance ready for use
    :rtype: logging.Logger
    """
    rest_logger = logging.getLogger('REST')
    rest_logger.setLevel(logging.INFO)
    
    # Configure rotating file handler
    file_rest = ConcurrentRotatingFileHandler(
        "Logs/rest.log",
        maxBytes=1000000,
        backupCount=5
    )
    
    # Configure console handler
    console_rest = logging.StreamHandler()
    
    # Create unified formatter
    formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s]%(message)s')
    
    # Apply formatter to handlers
    file_rest.setFormatter(formatter)
    console_rest.setFormatter(formatter)
    
    # Add handlers to logger
    rest_logger.addHandler(file_rest)
    rest_logger.addHandler(console_rest)
    
    return rest_logger