"""
REST API module for mission management.

Provides endpoints for mission submission and integrates with gRPC services for processing.
Includes comprehensive logging configuration for both file and console outputs.
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
    """Submit a mission and receive the mission ID.

    This endpoint accepts a mission in JSON format, processes it, and sends it to the gRPC REST client.
    If successful, it returns the mission ID.

    :param body: The mission data in JSON format. Must match the Mission schema.
    :type body: dict | bytes
    :return: Response object containing mission ID or error message with status code
    :rtype: tuple(MissionIdResponse, int) or tuple(str, int)
    
    :raises ValidationError: If input data doesn't match the expected schema
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
    formatter = logging.Formatter('[%(asctime)s] - [%(name)s][%(levelname)s]%(message)s')
    
    # Apply formatter to handlers
    file_rest.setFormatter(formatter)
    console_rest.setFormatter(formatter)
    
    # Add handlers to logger
    rest_logger.addHandler(file_rest)
    rest_logger.addHandler(console_rest)
    
    return rest_logger