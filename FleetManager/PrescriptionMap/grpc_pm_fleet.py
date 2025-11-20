"""
gRPC Prescription Map Fleet Communication Module
===============================================

This module provides gRPC communication services for prescription map (PM) 
management in the agricultural fleet management system. It handles bidirectional
communication between the fleet manager and ROS2-based vehicle systems for
prescription map distribution and execution feedback.

The module implements a gRPC server that receives prescription map requests
and mission completion signals from the mission management system, delegating
the actual processing to the prescription map manager fleet module.

Key Features:
    - gRPC server for prescription map communication
    - Bidirectional communication with ROS2 systems
    - Thread-safe queue-based message handling
    - Graceful connection management and error handling
    - Comprehensive logging system for debugging and monitoring
    - Integration with prescription map generation and validation workflows

Architecture:
    The module follows a service-oriented architecture where:
    - PMCommunicationService handles incoming gRPC requests
    - Message routing based on type ('Generate', 'Finish')
    - Delegation to pm_manager_fleet for actual processing
    - Thread-based server management for concurrent operations

Usage Example:
    ::

        # Initialize and start the gRPC PM communication service
        import logging
        pm_logger = logging.getLogger('pm_fleet')
        start_grpc_pm(pm_logger)

Author: Fleet Management System
Date: 2025

.. note::
    This module requires the following dependencies:
    - grpc and grpcio-tools for gRPC communication
    - GRPC.pm_pb2 and GRPC.pm_pb2_grpc (generated from .proto files)
    - PrescriptionMap.pm_manager_fleet for business logic
    
.. warning::
    The gRPC server runs on port 50087. Ensure this port is available
    and properly configured in firewall settings for production deployments.
"""

import json
import logging
import queue
import threading
import time
from concurrent import futures
import grpc

from GRPC.pm_pb2 import PMResponse
from GRPC.pm_pb2_grpc import PMCommunicationServicer, add_PMCommunicationServicer_to_server
from PrescriptionMap.pm_manager_fleet import handle_generate, handle_finish


class PMCommunicationService(PMCommunicationServicer):
    """
    gRPC service handler for prescription map communication from ROS2 systems.
    
    This class implements the gRPC service interface for receiving prescription map
    requests and mission completion signals from ROS2-based vehicle systems. It
    serves as the communication bridge between the fleet management system and
    individual vehicle controllers.
    
    The service processes two main types of messages:
    - 'Generate': Requests for prescription map generation
    - 'Finish': Signals indicating mission completion
    
    All incoming messages are delegated to the appropriate handlers in the
    pm_manager_fleet module for processing, maintaining separation of concerns
    between communication and business logic.
    
    Attributes:
        pm_logger: Configured logger instance for operation tracking and debugging
        
    Example:
        ::
        
            # Service is typically instantiated by the gRPC server
            service = PMCommunicationService(pm_logger)
            # Messages are handled automatically by gRPC infrastructure
            
    Note:
        This class inherits from PMCommunicationServicer which is automatically
        generated from the .proto file definitions.
        
    See Also:
        :mod:`PrescriptionMap.pm_manager_fleet`: Business logic for PM processing
        :mod:`GRPC.pm_pb2_grpc`: Generated gRPC service definitions
    """
    
    def __init__(self, pm_logger):
        """
        Initialize the PM communication service.
        
        Sets up the gRPC service handler with the provided logger for
        comprehensive operation tracking and debugging.
        
        Args:
            pm_logger: Configured logger instance for tracking PM operations,
                      should be properly configured with appropriate log levels
                      and output handlers
                      
        Example:
            ::
            
                import logging
                pm_logger = logging.getLogger('pm_fleet')
                pm_logger.setLevel(logging.INFO)
                service = PMCommunicationService(pm_logger)
        """
        super().__init__()
        self.pm_logger = pm_logger
        
    def SendPM(self, request, context):
        """
        Process incoming prescription map requests from ROS2 systems.
        
        This method handles gRPC requests containing prescription map messages
        from ROS2-based vehicle systems. It parses the incoming message, determines
        the message type, and delegates processing to the appropriate handler
        in the pm_manager_fleet module.
        
        The method supports two main message types:
        - 'Generate': Triggers prescription map generation for a vehicle
        - 'Finish': Signals mission completion and triggers validation
        
        Message Processing Flow:
        1. Extract message data from gRPC request
        2. Parse JSON message content
        3. Determine message type and extract vehicle ID
        4. Delegate to appropriate handler function
        5. Return confirmation response
        
        Args:
            request: gRPC request object containing prescription map message data.
                    The request should have a 'pm_message' field containing
                    JSON-encoded message data as a list of characters.
            context: gRPC connection context providing request metadata and
                    connection management capabilities
                    
        Returns:
            PMResponse: gRPC response object with confirmation message indicating
                       successful message receipt and processing initiation
                       
        Example:
            ::
            
                # This method is called automatically by gRPC infrastructure
                # when a client sends a PM message
                
                # Example message structure:
                {
                    "type": "Generate",
                    "vehicle_id": "VEHICLE_001",
                    "data": [treatments, amounts, grid, coords, pm_types]
                }
                
        Note:
            The method expects the pm_message to be a list of characters that
            forms a valid JSON string when joined together. This is a common
            pattern in gRPC for transmitting complex data structures.
            
        Warning:
            Invalid JSON in the pm_message will cause JSON parsing errors.
            Missing required fields (type, vehicle_id) may cause downstream
            processing failures that are handled by the delegate functions.
        """
        # Extract and reconstruct message data from gRPC request
        pm_message = list(request.pm_message)
        self.pm_logger.info(f"[gRPC PM] - Data PM received from Mission Management")
        pm_message_str = ''.join(pm_message)

        # Parse JSON message content
        pm_message = json.loads(pm_message_str)
        message_type = pm_message.get('type')
        
        # Route message to appropriate handler based on type
        if message_type == 'Generate':
            handle_generate(pm_message.get('vehicle_id'), pm_message, self.pm_logger)
        elif message_type == 'Finish':
            handle_finish(pm_message.get('vehicle_id'), self.pm_logger)
            
        return PMResponse(confirmation=f"Feedback received")


def run_server_pm(pm_logger):
    """
    Initialize and run the gRPC server for prescription map communication.
    
    This function creates and starts a gRPC server that listens for prescription map
    requests from ROS2 systems. The server uses a thread pool executor for handling
    concurrent requests and runs continuously until interrupted.
    
    Server Configuration:
    - Port: 50087 (insecure connection)
    - Max workers: 10 concurrent threads
    - Service: PMCommunicationService for handling PM requests
    - Graceful shutdown on KeyboardInterrupt
    
    The server runs in an infinite loop, sleeping for 24 hours between iterations
    to maintain the connection while being responsive to shutdown signals.
    
    Args:
        pm_logger: Configured logger instance for server operation tracking.
                  Should be properly configured with appropriate log levels
                  and output handlers for production deployments.
                  
    Example:
        ::
        
            import logging
            pm_logger = logging.getLogger('pm_server')
            pm_logger.setLevel(logging.INFO)
            
            # This will block until KeyboardInterrupt
            run_server_pm(pm_logger)
            
    Note:
        The server uses insecure connections (no SSL/TLS). For production
        deployments, consider implementing secure connections with proper
        certificate management.
        
    Warning:
        This function runs indefinitely until interrupted. It should typically
        be run in a separate thread or process to avoid blocking the main
        application thread.
        
    Raises:
        KeyboardInterrupt: Gracefully handled to stop the server
        Exception: Any other exceptions during server startup or operation
                  should be handled by the calling code
    """
    # Create and configure gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_PMCommunicationServicer_to_server(
        PMCommunicationService(pm_logger), server)
    server.add_insecure_port('[::]:50087')
    server.start()
    pm_logger.info("[gRPC PM] - Server running on port [::]:50087")

    try:
        # Keep server running with long sleep intervals
        while True:
            time.sleep(86400)  # Sleep for 24 hours
    except KeyboardInterrupt:
        # Graceful shutdown on interrupt signal
        server.stop(0)


def start_grpc_pm(pm_logger):
    """
    Initialize and start gRPC communication components for prescription map management.
    
    This function sets up and starts the complete gRPC communication infrastructure
    for prescription map management. It creates a daemon thread to run the gRPC
    server, allowing the main application to continue running while the server
    handles incoming PM requests in the background.
    
    The function configures:
    - A daemon thread for running the gRPC server
    - Automatic thread cleanup when the main process exits
    - Non-blocking startup for integration with larger applications
    
    Thread Management:
    - Server runs in a daemon thread (automatically terminated on main exit)
    - Non-blocking startup allows immediate return to caller
    - Thread-safe operation with concurrent request handling
    
    Args:
        pm_logger: Configured logger instance for tracking PM communication
                  operations. Should be properly configured with appropriate
                  log levels and output handlers for production use.
                  
    Example:
        ::
        
            import logging
            from Logs.create_logger_fleet import create_logger
            
            # Create configured logger
            pm_logger = create_logger('pm_fleet', logging.INFO)
            
            # Start PM communication service (non-blocking)
            start_grpc_pm(pm_logger)
            
            # Main application continues...
            print("PM communication service started in background")
            
    Note:
        This function returns immediately after starting the daemon thread.
        The gRPC server will continue running in the background until the
        main process exits or is terminated.
        
    Warning:
        Since the server thread is a daemon thread, it will be forcefully
        terminated when the main process exits. Ensure proper application
        lifecycle management for graceful shutdowns if needed.
        
    See Also:
        :func:`run_server_pm`: The server function executed in the daemon thread
        :class:`PMCommunicationService`: The gRPC service implementation
    """
    # Create and start server thread as daemon
    server_thread = threading.Thread(target=run_server_pm, args=(pm_logger,))

    # Configure as daemon thread for automatic cleanup
    server_thread.daemon = True

    # Start the server thread (non-blocking)
    server_thread.start()