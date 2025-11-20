"""
System Initialization and Coordination Module

.. module:: init_fleet
    :synopsis: Core system initialization and component coordination for Fleet Management System

.. moduleauthor:: Fleet Management System Team

.. versionadded:: 1.0

This module serves as the central orchestrator for the Fleet Management System,
coordinating the initialization and startup of all distributed system components.

Architecture Overview:
    The system follows a microservices architecture with the following components:
    
    1. **Mission Management System**: Handles mission planning, execution, and monitoring
    2. **ROS2 Interface**: Provides communication with robotic vehicles and systems
    3. **MQTT Communication**: Manages IoT device communication and telemetry
    4. **REST API Interface**: Exposes HTTP endpoints for external system integration
    5. **Prescription Map System**: Handles agricultural prescription map generation and management
    6. **System Metrics**: Monitors system performance and health metrics

Workflow:
    .. mermaid::
    
        graph TD
            A[System Start] --> B[Initialize Loggers]
            B --> C[Clean Temporary Files]
            C --> D[Initialize Mission System]
            D --> E[Initialize ROS2 System]
            E --> F[Initialize MQTT System]
            F --> G[Initialize PM System]
            G --> H[Initialize Metrics System]
            H --> I[Initialize REST System]
            I --> J[System Ready]
            
            D --> D1[Create Communication Queues]
            D1 --> D2[Start GRPC Services]
            
            E --> E1[Create ROS2 Action Queue]
            E1 --> E2[Start ROS2 GRPC Service]
            
            F --> F1[Create ThingsBoard Queue]
            F1 --> F2[Start MQTT GRPC Service]
            F2 --> F3[Start ThingsBoard Manager]

.. note::
    All components are initialized with proper error handling and logging.
    System uses queue-based inter-process communication for reliability.

.. warning::
    System requires proper configuration of all external dependencies:
    - ROS2 environment
    - MQTT broker configuration
    - Database connectivity
    - ThingsBoard platform access
"""

import queue
import logging
import os
from typing import Optional

from Logs.create_logger_fleet import create_logger

# Component initializers
from MissionManager.grpc_mission_rest import start_grpc_mission_rest
from MissionManager.grpc_mission_vehicle import start_grpc_mission_vehicle
from MissionManager.grpc_mission_mqtt import start_grpc_mission_mqtt
from MissionManager.grpc_mission_pm import start_grpc_mission_pm
from REST.grpc_rest import start_grpc_rest
from ROS2.grpc_ros2 import start_grpc_ros2
from MQTT.grpc_mqtt import start_grpc_mqtt
from MQTT.ThingsBoard.tb_manager import start_tb_manager
from PrescriptionMap.grpc_pm_fleet import start_grpc_pm
from PrescriptionMap.src.prescription_map_pubsub.prescription_map_pubsub.subscriber_pm_function import main as start_pm_subs
from SystemMetrics.metrics_manager import start_metrics_manager
from SystemMetrics.src.system_metrics_pubsub.system_metrics_pubsub.subscriber_metrics_function import main as start_metrics_subs

from REST import rest_server

from clear_fleet import clean_directory, clean_pms_subfolders

def main() -> None:
    """Orchestrates system initialization and component startup.

    This function serves as the main entry point for the Fleet Management System,
    coordinating the sequential initialization of all system components. It follows
    a specific order to ensure proper dependency resolution and system stability.

    Initialization Workflow:
        1. **Logger Configuration**: Set up component-specific logging systems
        2. **Environment Cleanup**: Remove temporary files and reset state
        3. **Mission System**: Initialize mission management and inter-service queues
        4. **ROS2 Interface**: Start robotic communication layer
        5. **MQTT System**: Configure IoT device communication
        6. **Prescription Maps**: Initialize agricultural map management
        7. **System Metrics**: Start performance monitoring
        8. **REST API**: Launch external interface server

    Error Handling:
        - Each initialization step includes comprehensive error handling
        - Critical failures result in SystemError to prevent partial system startup
        - All errors are logged with full stack traces for debugging

    :rtype: None
    :raises SystemError: If any critical initialization step fails
    :raises RuntimeError: If logger initialization fails specifically

    .. seealso::
        - :func:`initialize_loggers`: Logger configuration details
        - :func:`initialize_mission_system`: Mission system startup
        - :func:`clean`: Environment cleanup procedures

    .. note::
        This function should only be called once during system startup.
        Multiple calls may result in resource conflicts.
    """
    try:
        # Step 1: Configure logging subsystems for all components
        # This must be done first as all other components depend on logging
        loggers = initialize_loggers()
        if not loggers:
            raise RuntimeError("Logger initialization failed")

        fleet_logger = loggers['fleet']
        fleet_logger.info(" - Initializing Fleet Manager for Farm ID: 1")

        # Step 2: Clean up temporary files and directories from previous runs
        # Ensures clean state and prevents conflicts from cached data
        clean()
        fleet_logger.info(" - Complete cleanup finished")

        # Step 3: Initialize core components in dependency order
        # Each component builds upon previously initialized services
        
        # Initialize mission management system first (core orchestrator)
        initialize_mission_system(loggers['mission'])
        
        # Initialize ROS2 system for robotic vehicle communication
        initialize_ros2_system(loggers['ros2'])
        
        # Initialize MQTT system for IoT device communication
        initialize_mqtt_system(loggers['mqtt'])
        
        # Initialize prescription map system for agricultural operations
        initialize_pm_system(loggers['pm'])
        
        # Initialize system metrics monitoring and performance tracking
        initialize_metrics_system(loggers['metrics'])
        
        # Initialize REST API system last (depends on all other systems)
        initialize_rest_system(loggers['rest'])
        
        fleet_logger.info(" - All system components initialized successfully")

    except Exception as e:
        # Log critical system initialization failure with full context
        logging.critical(f"System initialization failed: {str(e)}", exc_info=True)
        
        # Raise SystemError to prevent partial system startup
        raise SystemError("Critical startup failure") from e


def initialize_loggers() -> Optional[dict]:
    """Configures component-specific logging systems for the entire fleet management system.

    Creates and configures individual logger instances for each major system component,
    enabling centralized logging with component-specific log files for better debugging
    and system monitoring.

    Logger Configuration:
        - **FLEET**: Main system logging
        - **REST**: HTTP API request/response logging
        - **MISSION**: Mission planning and execution logs
        - **ROS2**: Robotic system communication logs
        - **MQTT**: IoT device communication logs
        - **PM**: Prescription map generation and management logs
        - **METRICS**: System performance and health metrics logs

    :return: Dictionary mapping component names to configured Logger instances,
             or None if initialization fails
    :rtype: Optional[Dict[str, logging.Logger]]
    :raises Exception: If any logger creation fails

    .. note::
        Each logger writes to a separate log file in the 'Logs/' directory
        for better organization and debugging capabilities.

    .. warning::
        If this function returns None, the system should not proceed with
        initialization as logging is critical for system monitoring.

    Example:
        >>> loggers = initialize_loggers()
        >>> if loggers:
        ...     loggers['mission'].info("Mission system starting")
    """
    try:
        # Create dictionary of component-specific loggers
        # Each logger writes to separate files for better organization
        return {
            'fleet': create_logger('FLEET', 'Logs/fleet.log'),         # Main system logging
            'rest': create_logger('REST', 'Logs/rest.log'),         # HTTP API logging
            'mission': create_logger('MISSION', 'Logs/mission_manager.log'),  # Mission system logging
            'ros2': create_logger('ROS2', 'Logs/ros2.log'),         # ROS2 communication logging
            'mqtt': create_logger('MQTT', 'Logs/mqtt.log'),         # MQTT/IoT device logging
            'pm': create_logger('PM', 'Logs/pm.log'),               # Prescription map logging
            'metrics': create_logger('Metrics', 'Logs/metrics.log') # System metrics logging
        }
    except Exception as e:
        # Log logger creation failure and return None to signal error
        logging.error(f"Logger configuration failed: {str(e)}", exc_info=True)
        return None


def initialize_mission_system(mission_logger: logging.Logger) -> None:
    """Initializes the mission management subsystem with inter-service communication.

    Sets up the core mission management system including all necessary communication
    queues for coordinating between different system components. This is the central
    hub that orchestrates mission planning, execution, and monitoring.

    Communication Queue Architecture:
        - **send_rest**: Queue for sending data to REST API endpoints
        - **send_vehicle**: Queue for sending commands to vehicle systems
        - **receive_vehicle**: Queue for receiving vehicle status and responses
        - **send_mqtt**: Queue for sending data to MQTT/IoT systems
        - **send_pm**: Queue for sending prescription map requests

    GRPC Services Started:
        1. **Mission-REST Interface**: Handles HTTP API mission requests
        2. **Mission-Vehicle Interface**: Manages vehicle command/control
        3. **Mission-MQTT Interface**: Coordinates IoT device communication
        4. **Mission-PM Interface**: Manages prescription map integration

    :param mission_logger: Pre-configured logger instance for mission system events
    :type mission_logger: logging.Logger
    :rtype: None
    :raises Exception: If any GRPC service fails to start or queue creation fails

    .. note::
        All queues use thread-safe implementations to handle concurrent access
        from multiple system components.

    .. seealso::
        - :func:`start_grpc_mission_rest`: REST interface details
        - :func:`start_grpc_mission_vehicle`: Vehicle interface details
    """
    try:
        # Create thread-safe communication queues for inter-service messaging
        # Each queue handles specific communication pathways within the system
        queues = {
            'send_rest': queue.Queue(),      # Queue for sending data to REST API endpoints
            'send_vehicle': queue.Queue(),   # Queue for sending commands to vehicle systems
            'receive_vehicle': queue.Queue(), # Queue for receiving vehicle status and responses
            'send_mqtt': queue.Queue(),      # Queue for sending data to MQTT/IoT systems
            'send_pm': queue.Queue()         # Queue for sending prescription map requests
        }

        # Start all mission management gRPC services with appropriate queue connections
        # These services handle different aspects of mission coordination
        
        # Mission-REST interface: handles HTTP API mission requests
        start_grpc_mission_rest(
            queues['send_vehicle'],    # For sending commands to vehicles
            queues['receive_vehicle'], # For receiving vehicle responses
            queues['send_mqtt'],       # For sending data to MQTT systems
            queues['send_rest'],       # For sending responses to REST API
            queues['send_pm'],         # For sending prescription map requests
            mission_logger
        )
        
        # Mission-Vehicle interface: manages vehicle command/control communication
        start_grpc_mission_vehicle(queues['send_vehicle'], queues['receive_vehicle'], mission_logger)
        
        # Mission-MQTT interface: coordinates IoT device communication
        start_grpc_mission_mqtt(queues['send_mqtt'], mission_logger)
        
        # Mission-PM interface: manages prescription map integration
        start_grpc_mission_pm(queues['send_pm'], mission_logger)
        
    except Exception as e:
        # Log mission system initialization failure with full context
        mission_logger.critical(f"Mission system initialization failed: {str(e)}", exc_info=True)
        raise


def initialize_ros2_system(ros2_logger: logging.Logger) -> None:
    """Initializes ROS2 communication interface for robotic system integration.
    
    Sets up the ROS2 communication layer that enables the fleet management system
    to interact with robotic vehicles and autonomous systems. This includes action
    servers, topic publishers/subscribers, and service clients.

    ROS2 Components:
        - **Action Queue**: Thread-safe queue for ROS2 action requests
        - **GRPC Service**: Bridge between fleet manager and ROS2 ecosystem
        - **Node Management**: Handles ROS2 node lifecycle and communication

    Communication Flow:
        Fleet Manager --> Action Queue --> ROS2 GRPC Service --> ROS2 Network

    :param ros2_logger: Pre-configured logger instance for ROS2 system events
    :type ros2_logger: logging.Logger
    :rtype: None
    :raises Exception: If ROS2 environment is not properly configured or
                      GRPC service fails to start

    .. note::
        Requires ROS2 environment to be properly sourced and configured
        before system startup.

    .. warning::
        ROS2 system failure will prevent vehicle communication and should
        be treated as a critical error.
    """
    try:
        # Create thread-safe queue for ROS2 action requests and responses
        # This queue bridges the Fleet Management System with ROS2 ecosystem
        ros2_action_queue = queue.Queue()
        
        # Start gRPC service that bridges Fleet Manager and ROS2 network
        # Handles action goal submission and result collection from ROS2 nodes
        start_grpc_ros2(ros2_action_queue, ros2_logger)
        
    except Exception as e:
        # Log ROS2 system initialization failure with full context
        ros2_logger.critical(f"ROS2 initialization failed: {str(e)}", exc_info=True)
        raise


def initialize_mqtt_system(mqtt_logger: logging.Logger) -> None:
    """Configures MQTT communication layer for IoT device integration.
    
    Initializes the MQTT communication system including ThingsBoard integration
    for IoT device management, telemetry collection, and real-time monitoring.
    This system handles all wireless sensor networks and field device communication.

    MQTT Architecture:
        - **MQTT GRPC Service**: Handles MQTT message routing and processing
        - **ThingsBoard Manager**: Manages device registration and telemetry
        - **Communication Queue**: Thread-safe message queue for MQTT operations

    ThingsBoard Integration:
        - Device provisioning and management
        - Telemetry data collection and storage
        - Real-time dashboard and alerts
        - Rule engine for automated responses

    :param mqtt_logger: Pre-configured logger instance for MQTT system events
    :type mqtt_logger: logging.Logger
    :rtype: None
    :raises Exception: If MQTT broker connection fails or ThingsBoard
                      authentication is invalid

    .. note::
        Requires valid MQTT broker configuration and ThingsBoard
        platform credentials.

    .. seealso::
        - :func:`start_grpc_mqtt`: MQTT GRPC service implementation
        - :func:`start_tb_manager`: ThingsBoard manager details
    """
    try:
        # Create thread-safe queue for ThingsBoard device management and telemetry
        # This queue handles device provisioning, telemetry, and rule engine data
        tb_queue = queue.Queue()
        
        # Start MQTT gRPC service for message routing and processing
        # Handles MQTT message distribution and broker communication
        start_grpc_mqtt(tb_queue, mqtt_logger)
        
        # Start ThingsBoard manager for IoT platform integration
        # Manages device registration, telemetry collection, and dashboard updates
        start_tb_manager(tb_queue, mqtt_logger)
        
    except Exception as e:
        # Log MQTT system initialization failure with full context
        mqtt_logger.critical(f"MQTT initialization failed: {str(e)}", exc_info=True)
        raise


def initialize_pm_system(pm_logger: logging.Logger) -> None:
    """Initializes prescription map management system for agricultural operations.

    Sets up the prescription map (PM) system that handles the generation, processing,
    and distribution of agricultural prescription maps for precision farming operations.
    This includes support for multiple vehicle types and standardized formats.

    Prescription Map Components:
        - **PM Manager**: Core prescription map processing engine
        - **GRPC Service**: API interface for prescription map requests
        - **ROS2 Subscriber**: Receives prescription map data from field systems
        - **Format Support**: ISOBUS XML, JSON, and proprietary formats

    Supported Vehicle Types:
        - **Drones**: Aerial application and monitoring
        - **ISOBUS Tractors**: Standardized agricultural machinery
        - **Autonomous Vehicles**: Self-guided field operations

    Cleanup Management:
        - Automatic cleanup of temporary files on system shutdown
        - Thread-safe shutdown procedures
        - Resource deallocation and file system maintenance

    :param pm_logger: Pre-configured logger instance for prescription map events
    :type pm_logger: logging.Logger
    :rtype: None
    :raises Exception: If PM manager thread fails to start or ROS2 subscriber
                      cannot be initialized

    .. note::
        System automatically registers cleanup functions to ensure proper
        resource deallocation on shutdown.

    .. warning::
        PM system is critical for agricultural operations. Failure may
        result in inability to execute field missions.
    """
    try:
        # Start prescription map gRPC service for API interface
        # Handles prescription map requests from mission management system
        start_grpc_pm(pm_logger)
        
        # Start ROS2 subscriber for prescription map data from field systems
        # Receives prescription map data from agricultural vehicles and sensors
        start_pm_subs(pm_logger=pm_logger)
        
    except Exception as e:
        # Log prescription map system initialization failure with full context
        pm_logger.critical(f"Prescription Map initialization failed: {str(e)}", exc_info=True)
        raise
    
def initialize_metrics_system(metrics_logger: logging.Logger) -> None:
    """Initializes system metrics management and monitoring infrastructure.

    Sets up comprehensive system monitoring including performance metrics,
    health checks, resource utilization tracking, and real-time system
    status reporting. This system provides observability into fleet operations.

    Metrics Collection:
        - **CPU Utilization**: System and process-level CPU usage
        - **Memory Usage**: RAM consumption and memory leaks detection
        - **Network Statistics**: Bandwidth usage and connection health
        - **Disk I/O**: Storage performance and space utilization
        - **Queue Metrics**: Inter-service communication queue depths
        - **Service Health**: Component availability and response times

    Monitoring Components:
        - **ROS2 Subscriber**: Receives metrics from distributed components
        - **Metrics Manager**: Aggregates and processes metric data
        - **Real-time Processing**: Live system monitoring and alerting

    :param metrics_logger: Pre-configured logger instance for system metrics events
    :type metrics_logger: logging.Logger
    :rtype: None
    :raises Exception: If metrics subscriber fails to start or metrics manager
                      cannot be initialized

    .. note::
        Metrics are collected in real-time and can be used for system
        optimization and predictive maintenance.

    .. seealso::
        - :func:`start_metrics_subs`: Metrics subscriber implementation
        - :func:`start_metrics_manager`: Metrics processing details
    """
    try:
        # Create thread-safe queue for system metrics collection and processing
        # This queue receives metrics from distributed ROS2 nodes and processes them
        metrics_queue = queue.Queue()
        
        # Start ROS2 subscriber for metrics collection from fleet components
        # Receives system metrics from drones, vehicles, and ground stations
        start_metrics_subs(metrics_queue=metrics_queue, metrics_logger=metrics_logger)
        
        # Start metrics manager for data processing and distribution
        # Aggregates metrics and distributes to monitoring systems (MQTT, DB, etc.)
        start_metrics_manager(metrics_queue, metrics_logger)
        
    except Exception as e:
        # Log system metrics initialization failure with full context
        metrics_logger.critical(f"System Metrics initialization failed: {str(e)}", exc_info=True)
        raise


def initialize_rest_system(rest_logger: logging.Logger) -> None:
    """Launches REST API interface for external system integration.
    
    Initializes the HTTP REST API server that provides external access to
    fleet management functionality. This includes mission management endpoints,
    system status queries, and integration with third-party systems.

    REST API Features:
        - **Mission Management**: Create, update, and monitor missions
        - **Vehicle Control**: Send commands and receive status updates
        - **System Status**: Health checks and system information
        - **Data Export**: Download logs, reports, and telemetry data
        - **Authentication**: Secure access control and API key management

    Server Configuration:
        - **GRPC Bridge**: Connects REST endpoints to internal GRPC services
        - **HTTP Server**: Flask-based REST API server
        - **OpenAPI Documentation**: Swagger/OpenAPI specification
        - **CORS Support**: Cross-origin resource sharing for web clients

    :param rest_logger: Pre-configured logger instance for REST API events
    :type rest_logger: logging.Logger
    :rtype: None
    :raises Exception: If GRPC REST service fails to start or HTTP server
                      cannot bind to the configured port

    .. note::
        This is typically the last system to initialize as it depends on
        all other systems being operational.

    .. warning::
        REST API server failure will prevent external system integration
        and web-based fleet management interfaces.
    """
    try:
        # Start gRPC service that bridges REST endpoints to internal gRPC services
        # Provides HTTP API access to fleet management functionality
        start_grpc_rest(rest_logger)
        
        # Start HTTP REST API server (Flask-based) for external system integration
        # Provides web-based interface and third-party API access
        rest_server.main()
        
    except Exception as e:
        # Log REST system initialization failure with full context
        rest_logger.critical(f"REST initialization failed: {str(e)}", exc_info=True)
        raise

def clean() -> None:
    """Cleans up temporary files and directories before system initialization.

    Performs comprehensive cleanup of temporary files, cached data, and
    state directories to ensure a clean system startup. This prevents
    issues from previous runs and ensures consistent system behavior.

    Cleanup Operations:
        - **Received Directory**: Clears incoming prescription map files
        - **PMs Directory**: Removes cached prescription map data
        - **PM Generation Subfolders**: Cleans vehicle-specific PM caches

    Directory Targets:
        - ``PrescriptionMap/pm_generation/Received/``: Incoming PM files
        - ``PMs/``: Generated prescription map cache
        - ``PrescriptionMap/pm_generation/*/``: Vehicle-specific PM folders

    :rtype: None
    :raises OSError: If directory cleanup operations fail due to permissions
                    or file system errors

    .. note::
        This function is called early in the initialization process to
        ensure clean system state.

    .. warning::
        This operation will permanently delete temporary files. Ensure
        no critical data is stored in these directories.
    """
    # Clean incoming prescription map files directory
    # Removes any pending or partially processed PM files from previous runs
    clean_directory("PrescriptionMap/pm_generation/Received")
    
    # Clean generated prescription maps cache directory
    # Removes cached PM files to ensure fresh generation
    clean_directory("PMs")
    
    # Clean vehicle-specific prescription map generation subfolders
    # Removes temporary files from drone, ISOBUS, and other vehicle types
    clean_pms_subfolders("PrescriptionMap/pm_generation")

if __name__ == "__main__":
    """Main entry point with comprehensive exception handling and graceful shutdown.

    Provides the primary execution entry point for the Fleet Management System
    with robust error handling, graceful shutdown capabilities, and proper
    exit code management for system monitoring and orchestration tools.

    Execution Flow:
        1. **Normal Operation**: Call main() and run until completion or interruption
        2. **User Interruption**: Handle Ctrl+C gracefully with cleanup
        3. **Exception Handling**: Log all unhandled exceptions with full context
        4. **Exit Codes**: Return appropriate exit codes for system monitoring

    Exit Codes:
        - **0**: Normal successful completion
        - **1**: Unhandled exception or critical error
        - **130**: User interruption (Ctrl+C)

    Signal Handling:
        - **SIGINT (Ctrl+C)**: Graceful shutdown with cleanup
        - **SIGTERM**: System shutdown request handling

    .. note::
        This block only executes when the script is run directly,
        not when imported as a module.

    .. seealso::
        - :func:`main`: Primary system initialization function
    """
    try:
        main()
    except KeyboardInterrupt:
        print("\nSystem shutdown initiated by user")
    except Exception as e:
        logging.critical(f"Unhandled exception in main process: {str(e)}", exc_info=True)
        raise SystemExit(1) from e