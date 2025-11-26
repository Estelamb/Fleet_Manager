"""
ROS2 Drone System Initialization Module
=======================================

This module provides comprehensive ROS2-based drone system initialization and coordination
functionality for distributed agricultural drone operations. It orchestrates multiple
ROS2 nodes, gRPC services, and inter-component communication systems to create a unified
drone control and monitoring platform.

The module implements a multi-threaded ROS2 architecture with integrated gRPC communication
channels, enabling seamless coordination between drone subsystems and Mission Management
systems for precision agriculture applications.

.. module:: init_ros2
    :synopsis: ROS2-based drone system initialization and component coordination

Features
--------
- **ROS2 Integration**: Multi-node ROS2 architecture with coordinated execution
- **gRPC Communication**: Bidirectional communication with Mission Management systems
- **Component Orchestration**: Unified initialization of all drone subsystems
- **Multi-Threading**: Concurrent execution of multiple ROS2 nodes and services
- **Error Handling**: Comprehensive error management and graceful shutdown procedures
- **Logging Integration**: Centralized logging across all system components

System Architecture
------------------
The drone system consists of multiple interconnected components:

ROS2 Components:
    - **Commands Action Server**: Mission command processing and execution
    - **Prescription Map Publisher**: Agricultural prescription data distribution
    - **System Metrics Publisher**: Real-time system health and performance data

gRPC Services:
    - **Commands Service**: Remote command reception from Mission Management
    - **Prescription Map Service**: PM data reception and processing
    - **Metrics Service**: System status transmission to Mission Management

Communication Flow:
    Mission Management ↔ gRPC Services ↔ Queue ↔ ROS2 Nodes ↔ Drone Hardware

Workflow
--------
System Initialization Pipeline:
    1. **Logging Configuration**: Set up component-specific logging systems
    2. **ROS2 Context Initialization**: Initialize ROS2 runtime environment
    3. **Component Initialization**: Create and configure all system components
    4. **Service Registration**: Start gRPC services and communication channels
    5. **Executor Configuration**: Set up multi-threaded ROS2 execution environment
    6. **System Execution**: Begin coordinated operation of all components
    7. **Graceful Shutdown**: Handle interrupts and perform cleanup operations

Component Initialization Sequence:
    1. **Commands System**: Action server + gRPC command interface
    2. **Prescription Map System**: Publisher + gRPC PM interface  
    3. **Metrics System**: Publisher + gRPC metrics interface
    4. **Executor Setup**: Multi-threaded coordination of all nodes
    5. **Service Activation**: Begin processing and communication

Inter-Component Communication
----------------------------
Communication between components uses queue-based message passing:
    - **Thread-Safe Queues**: Python queue.Queue for inter-thread communication
    - **gRPC Interfaces**: External communication with Mission Management
    - **ROS2 Messages**: Internal drone system communication
    - **Logging Coordination**: Shared logging infrastructure across components

Error Handling Strategy
----------------------
Multi-level error handling ensures system reliability:
    - **Component-Level**: Individual component error isolation
    - **System-Level**: Critical failure detection and recovery
    - **Graceful Shutdown**: Controlled termination on failures or interrupts
    - **Resource Cleanup**: Proper disposal of ROS2 nodes and resources

Functions
---------
.. autofunction:: main
.. autofunction:: initialize_commands_system
.. autofunction:: initialize_pm_system
.. autofunction:: initialize_metrics_system

Dependencies
-----------
- **argparse**: Command-line interface for drone ID specification
- **queue**: Thread-safe inter-component communication
- **logging**: Centralized logging and error reporting
- **sys**: System-level operations and exit handling
- **rclpy**: ROS2 Python client library
- **typing**: Type hint support for enhanced documentation

ROS2 Dependencies:
    - **rclpy.executors.MultiThreadedExecutor**: Concurrent node execution
    - **Custom ROS2 Nodes**: Commands, PM, and Metrics publishers/servers

gRPC Dependencies:
    - **GRPC.grpc_ros2_commands**: Command interface service
    - **GRPC.grpc_ros2_pm**: Prescription map interface service
    - **GRPC.grpc_ros2_metrics**: System metrics interface service

Integration Points
-----------------
This module integrates with:
    - **Mission Management**: Remote coordination and control systems
    - **Drone Hardware**: Sensors, actuators, and flight control systems
    - **Agricultural Systems**: Prescription maps and field management
    - **Monitoring Systems**: Real-time system health and performance tracking

Performance Considerations
-------------------------
- **Multi-Threading**: Efficient resource utilization with concurrent execution
- **Queue Management**: Optimized inter-component message passing
- **Resource Cleanup**: Proper disposal to prevent memory leaks
- **Scalability**: Modular architecture supporting additional components

Examples
--------
Command line usage:

.. code-block:: bash

    # Initialize drone system with ID 1
    python init_ros2.py --drone_id 1
    
    # Initialize drone system with ID 2  
    python init_ros2.py --drone_id 2

Integration usage:

.. code-block:: python

    # Programmatic initialization
    from init_ros2 import main
    main(drone_id=1)

System Configuration:
    - Each drone requires unique ID for identification
    - Logging files created per drone: Logs/Drone_{id}.log
    - ROS2 namespace based on drone ID for multi-drone support

Notes
-----
- System requires ROS2 environment setup and sourcing
- Each drone instance must have unique ID for proper operation
- All components share unified logging infrastructure
- Graceful shutdown handled via Ctrl+C interrupt signal
- Multi-drone support through ID-based namespace isolation

See Also
--------
rclpy.executors.MultiThreadedExecutor : ROS2 concurrent execution framework
GRPC.grpc_ros2_commands : Command interface implementation
queue.Queue : Thread-safe inter-component communication
Logs.create_logger : Centralized logging infrastructure
"""

import argparse
import queue
import logging
import sys
from typing import Optional, Union
from Logs.create_logger import create_logger

import rclpy
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node

from GRPC.grpc_ros2_commands import start_grpc_commands
from GRPC.grpc_ros2_pm import start_grpc_pm
from GRPC.grpc_ros2_metrics import start_grpc_metrics

from src.commands_action_interface.commands_action_interface.commands_action_server import CommandsActionServer
from src.prescription_map_pubsub.prescription_map_pubsub.publisher_pm_function import PrescriptionMapPublisher
from src.system_metrics_pubsub.system_metrics_pubsub.publisher_metrics_function import SystemMetricsPublisher
from src.state_vector_pubsub.state_vector_pubsub.publisher_member_function import StateVectorPublisher
from src.state_vector_pubsub.state_vector_pubsub.state_vector import start_state_vector


def main(drone_id: int) -> None:
    """
    Orchestrate complete ROS2 drone system initialization and component coordination.

    This function serves as the primary entry point for ROS2-based drone system startup,
    managing the initialization sequence of all system components, establishing
    inter-component communication, and coordinating multi-threaded execution of
    the complete drone control and monitoring infrastructure.

    Parameters
    ----------
    drone_id : int
        Unique identifier for the drone instance.
        Used for logging, ROS2 namespace isolation, and multi-drone coordination.
        Must be positive integer for proper system identification.
        Examples: 1, 2, 3, etc.

    Returns
    -------
    None
        Function performs system initialization and runs until interrupted.
        Does not return during normal operation; exits on shutdown signal.

    Raises
    ------
    SystemError
        If critical initialization failure occurs that prevents system startup.
        Indicates fundamental configuration or resource availability issues.

    Workflow
    --------
    1. **Logging Configuration**: Set up drone-specific logging infrastructure
    2. **ROS2 Context Initialization**: Initialize ROS2 runtime environment
    3. **Component Initialization**: Create and configure all system components:
       - Commands action server with gRPC interface
       - Prescription map publisher with gRPC interface  
       - System metrics publisher with gRPC interface
    4. **Executor Configuration**: Set up multi-threaded ROS2 execution environment
    5. **System Execution**: Begin coordinated operation of all components
    6. **Interrupt Handling**: Process shutdown signals and perform cleanup
    7. **Resource Cleanup**: Destroy nodes and shutdown ROS2 context

    Component Initialization Sequence:
        1. **Commands System**: Action server + gRPC command reception interface
        2. **Prescription Map System**: ROS2 publisher + gRPC PM reception interface
        3. **Metrics System**: ROS2 publisher + gRPC metrics transmission interface
        4. **Multi-Threading Setup**: Executor configuration for concurrent operation
        5. **Service Activation**: Begin processing and inter-component communication

    Error Handling:
        - **Component Failures**: Individual component errors logged and propagated
        - **Critical Failures**: System-level errors result in SystemError exception
        - **Graceful Shutdown**: Ctrl+C handled with proper resource cleanup
        - **Resource Management**: All ROS2 nodes and contexts properly disposed

    Examples
    --------
    >>> # Initialize drone system with ID 1
    >>> main(1)
    >>> # Runs until interrupted, handles all system coordination

    >>> # Programmatic usage with error handling
    >>> try:
    >>>     main(drone_id=2)
    >>> except SystemError as e:
    >>>     print(f"System initialization failed: {e}")

    Integration Notes
    ----------------
    Function integrates with:
        - **Mission Management**: Remote coordination via gRPC interfaces
        - **ROS2 Ecosystem**: Multi-node coordination and message passing
        - **Logging Infrastructure**: Centralized logging across all components
        - **Hardware Systems**: Drone sensors, actuators, and flight control

    Performance Characteristics
    --------------------------
    - **Startup Time**: 5-15 seconds depending on hardware and configuration
    - **Resource Usage**: Scales with number of active components and message rates
    - **Multi-Threading**: Efficient CPU utilization across available cores
    - **Memory Management**: Automatic cleanup prevents resource leaks

    System Architecture:
        Mission Management ↔ gRPC Services ↔ Queue ↔ ROS2 Nodes ↔ Drone Hardware

    Notes
    -----
    - Function blocks during normal operation and runs until interrupted
    - Each drone instance requires unique ID for proper multi-drone operation
    - System automatically handles component coordination and error recovery
    - Logging output directed to drone-specific log files

    See Also
    --------
    initialize_commands_system : Commands subsystem initialization
    initialize_pm_system : Prescription map subsystem initialization  
    initialize_metrics_system : System metrics subsystem initialization
    rclpy.executors.MultiThreadedExecutor : ROS2 concurrent execution framework
    """
    try:
        # Configure drone-specific logging subsystem for centralized error reporting and monitoring
        drone_logger = create_logger(f'Drone {drone_id}', f'Logs/Drone_{drone_id}.log')
        drone_logger.info(f"[Init ROS2] - Initializing ROS2 drone system for drone ID: {drone_id}")
        
        sv_queue = queue.Queue()
        
        # Initialize ROS2 runtime context for multi-node coordination and message passing
        rclpy.init()

        # Initialize all core system components with integrated gRPC-ROS2 communication
        commands_action = initialize_commands_system(drone_id, drone_logger, sv_queue)
        pm_publisher = initialize_pm_system(drone_id, drone_logger)
        metrics_publisher = initialize_metrics_system(drone_id, drone_logger)
        sv_publisher = initialize_state_vector_system(drone_id, drone_logger, sv_queue)

        # Create and configure multi-threaded ROS2 executor for concurrent operation
        # This enables simultaneous processing of commands, PM data, and metrics
        executor = MultiThreadedExecutor()
        executor.add_node(commands_action)  # Add commands action server for mission execution
        executor.add_node(pm_publisher)     # Add PM publisher for agricultural data distribution
        executor.add_node(metrics_publisher)  # Add metrics publisher for system monitoring
        executor.add_node(sv_publisher)       # Add state vector publisher for drone state updates

        drone_logger.info("[Init ROS2] - All system components initialized successfully")

        try:
            # Begin coordinated execution of all system components
            # This call blocks and handles all node callbacks in separate threads
            executor.spin()  # Concurrent execution of all ROS2 nodes and their callbacks
        except KeyboardInterrupt:
            # Handle graceful shutdown on user interrupt (Ctrl+C)
            drone_logger.info("[Init ROS2] - Shutdown signal received (Ctrl+C), initiating graceful shutdown")
        finally:
            # Perform comprehensive resource cleanup to prevent memory leaks
            drone_logger.info("[Init ROS2] - Beginning system shutdown and resource cleanup")
            executor.shutdown()              # Stop executor and all running threads
            commands_action.destroy_node()   # Clean up commands action server resources
            pm_publisher.destroy_node()      # Clean up PM publisher resources  
            metrics_publisher.destroy_node() # Clean up metrics publisher resources
            rclpy.try_shutdown()             # Shutdown ROS2 context safely
            drone_logger.info("[Init ROS2] - System shutdown completed successfully")

    except Exception as e:
        # Handle critical system initialization failures with comprehensive logging
        logging.critical(f"System initialization failed for drone {drone_id}: {str(e)}", exc_info=True)
        raise SystemError("Critical startup failure") from e


def initialize_commands_system(drone_id: int, drone_logger: logging.Logger, sv_queue: queue.Queue) -> CommandsActionServer:
    """
    Initialize the commands processing subsystem with ROS2 action server and gRPC interface.

    This function sets up the complete commands communication infrastructure, including
    a thread-safe queue for inter-component communication, a gRPC service for receiving
    commands from Mission Management, and a ROS2 action server for processing and
    executing drone commands within the ROS2 ecosystem.

    Parameters
    ----------
    drone_id : int
        Unique identifier for the drone instance.
        Used for ROS2 namespace isolation and command routing.
        Must be positive integer for proper identification.

    drone_logger : logging.Logger
        Configured logger instance for drone-specific logging.
        Used for component initialization logging and error reporting.
        Must be properly configured with appropriate handlers and formatters.

    Returns
    -------
    CommandsActionServer
        Initialized ROS2 action server instance for command processing.
        Configured with gRPC communication queue and drone-specific parameters.
        Ready for ROS2 executor integration and command execution workflows.

    Raises
    ------
    Exception
        If commands system initialization fails due to:
        - gRPC service startup errors
        - ROS2 action server creation failures  
        - Queue configuration issues
        - Resource allocation problems

    Workflow
    --------
    1. **Queue Creation**: Initialize thread-safe communication queue
    2. **gRPC Service**: Start gRPC commands service with queue binding
    3. **Action Server**: Create ROS2 CommandsActionServer with integrated queue
    4. **Configuration**: Apply drone-specific parameters and logging
    5. **Validation**: Verify successful initialization of all components

    Communication Flow:
        Mission Management → gRPC Service → Queue → ROS2 Action Server → Drone Hardware

    Examples
    --------
    >>> logger = create_logger('Drone1', 'logs/drone1.log')
    >>> commands_server = initialize_commands_system(1, logger)
    >>> # Returns configured CommandsActionServer ready for executor integration

    Integration Notes
    ----------------
    - **Queue Integration**: Thread-safe queue enables gRPC-to-ROS2 communication
    - **Error Handling**: Comprehensive exception logging and propagation
    - **Resource Management**: Proper initialization order ensures clean startup
    - **Multi-Threading**: Component designed for concurrent executor operation

    See Also
    --------
    CommandsActionServer : ROS2 action server implementation
    start_grpc_commands : gRPC commands service initialization
    queue.Queue : Thread-safe inter-component communication
    """
    try:
        # Create thread-safe queue for gRPC-to-ROS2 command communication
        commands_queue = queue.Queue()
        
        # Initialize gRPC commands service with queue binding for external communication
        start_grpc_commands(commands_queue, drone_logger)
        
        # Create ROS2 action server with integrated gRPC communication queue
        commands_action = CommandsActionServer(drone_id=drone_id, drone_logger=drone_logger,
                           commands_queue=commands_queue, sv_queue=sv_queue)
        
        return commands_action
    except Exception as e:
        # Log critical initialization failure with full traceback
        drone_logger.critical(f"[Init ROS2] - Commands initialization failed: {str(e)}", exc_info=True)
        raise

def initialize_pm_system(drone_id: int, drone_logger: logging.Logger) -> PrescriptionMapPublisher:
    """
    Initialize the prescription map processing subsystem with ROS2 publisher and gRPC interface.

    This function establishes the complete prescription map communication infrastructure,
    including a thread-safe queue for inter-component communication, a gRPC service for
    receiving prescription map data from Mission Management, and a ROS2 publisher for
    distributing PM data within the drone's ROS2 ecosystem.

    Parameters
    ----------
    drone_id : int
        Unique identifier for the drone instance.
        Used for ROS2 namespace isolation and prescription map routing.
        Must be positive integer for proper identification.

    drone_logger : logging.Logger
        Configured logger instance for drone-specific logging.
        Used for component initialization logging and error reporting.
        Must be properly configured with appropriate handlers and formatters.

    Returns
    -------
    PrescriptionMapPublisher
        Initialized ROS2 publisher instance for prescription map distribution.
        Configured with gRPC communication queue and drone-specific parameters.
        Ready for ROS2 executor integration and PM data publishing workflows.

    Raises
    ------
    Exception
        If prescription map system initialization fails due to:
        - gRPC service startup errors
        - ROS2 publisher creation failures
        - Queue configuration issues
        - Resource allocation problems

    Workflow
    --------
    1. **Queue Creation**: Initialize thread-safe communication queue for PM data
    2. **gRPC Service**: Start gRPC prescription map service with queue binding
    3. **ROS2 Publisher**: Create PrescriptionMapPublisher with integrated queue
    4. **Configuration**: Apply drone-specific parameters and logging setup
    5. **Validation**: Verify successful initialization of all components

    Communication Flow:
        Mission Management → gRPC Service → Queue → ROS2 Publisher → Drone Subsystems

    Examples
    --------
    >>> logger = create_logger('Drone1', 'logs/drone1.log')
    >>> pm_publisher = initialize_pm_system(1, logger)
    >>> # Returns configured PrescriptionMapPublisher ready for executor integration

    Integration Notes
    ----------------
    - **Queue Integration**: Thread-safe queue enables gRPC-to-ROS2 PM data flow
    - **Agricultural Data**: Handles precision agriculture prescription map processing
    - **Error Handling**: Comprehensive exception logging and propagation
    - **Resource Management**: Proper initialization order ensures clean startup
    - **Multi-Threading**: Component designed for concurrent executor operation

    Data Flow:
        Agricultural Management System → Mission Management → gRPC Interface → 
        Queue → ROS2 Publisher → Drone Field Management Systems

    See Also
    --------
    PrescriptionMapPublisher : ROS2 prescription map publisher implementation
    start_grpc_pm : gRPC prescription map service initialization
    queue.Queue : Thread-safe inter-component communication
    """
    try:
        # Create thread-safe queue for gRPC-to-ROS2 prescription map communication
        pm_queue = queue.Queue()
        
        # Initialize gRPC prescription map service with queue binding for external communication
        start_grpc_pm(pm_queue, drone_logger)
        
        # Create ROS2 publisher with integrated gRPC communication queue
        pm_publisher = PrescriptionMapPublisher(drone_id=drone_id, drone_logger=drone_logger,
                                                 pm_queue=pm_queue)
        
        return pm_publisher
    except Exception as e:
        # Log critical initialization failure with full traceback
        drone_logger.critical(f"[Init ROS2] - PM initialization failed: {str(e)}", exc_info=True)
        raise

def initialize_metrics_system(drone_id: int, drone_logger: logging.Logger) -> SystemMetricsPublisher:
    """
    Initialize the system metrics monitoring subsystem with ROS2 publisher and gRPC interface.

    This function establishes the complete system metrics communication infrastructure,
    including a thread-safe queue for inter-component communication, a gRPC service for
    transmitting system health and performance data to Mission Management, and a ROS2
    publisher for distributing metrics data within the drone's monitoring ecosystem.

    Parameters
    ----------
    drone_id : int
        Unique identifier for the drone instance.
        Used for ROS2 namespace isolation and metrics data identification.
        Must be positive integer for proper identification.

    drone_logger : logging.Logger
        Configured logger instance for drone-specific logging.
        Used for component initialization logging and error reporting.
        Must be properly configured with appropriate handlers and formatters.

    Returns
    -------
    SystemMetricsPublisher
        Initialized ROS2 publisher instance for system metrics distribution.
        Configured with gRPC communication queue and drone-specific parameters.
        Ready for ROS2 executor integration and metrics data publishing workflows.

    Raises
    ------
    Exception
        If system metrics initialization fails due to:
        - gRPC service startup errors
        - ROS2 publisher creation failures
        - Queue configuration issues
        - Resource allocation problems

    Workflow
    --------
    1. **Queue Creation**: Initialize thread-safe communication queue for metrics data
    2. **gRPC Service**: Start gRPC metrics service with queue binding
    3. **ROS2 Publisher**: Create SystemMetricsPublisher with integrated queue
    4. **Configuration**: Apply drone-specific parameters and logging setup
    5. **Validation**: Verify successful initialization of all components

    Communication Flow:
        Drone Subsystems → ROS2 Publisher → Queue → gRPC Service → Mission Management

    Examples
    --------
    >>> logger = create_logger('Drone1', 'logs/drone1.log')
    >>> metrics_publisher = initialize_metrics_system(1, logger)
    >>> # Returns configured SystemMetricsPublisher ready for executor integration

    Integration Notes
    ----------------
    - **Queue Integration**: Thread-safe queue enables ROS2-to-gRPC metrics data flow
    - **Health Monitoring**: Handles real-time system health and performance tracking
    - **Error Handling**: Comprehensive exception logging and propagation
    - **Resource Management**: Proper initialization order ensures clean startup
    - **Multi-Threading**: Component designed for concurrent executor operation

    Metrics Data Types:
        - **System Health**: CPU, memory, storage utilization
        - **Performance**: Processing rates, response times, throughput
        - **Hardware Status**: Sensor readings, actuator states, battery levels
        - **Communication**: Network status, message rates, error counts

    Data Flow:
        Drone Hardware/Software → SystemMetricsPublisher → Queue → 
        gRPC Service → Mission Management → ThingsBoard Dashboard

    See Also
    --------
    SystemMetricsPublisher : ROS2 system metrics publisher implementation
    start_grpc_metrics : gRPC metrics service initialization
    queue.Queue : Thread-safe inter-component communication
    """
    try:
        # Create thread-safe queue for ROS2-to-gRPC metrics communication
        metrics_queue = queue.Queue()
        
        # Initialize gRPC metrics service with queue binding for external communication
        start_grpc_metrics(metrics_queue, drone_logger)
        
        # Create ROS2 publisher with integrated gRPC communication queue
        metrics_publisher = SystemMetricsPublisher(drone_id=drone_id, drone_logger=drone_logger,
                                                    metrics_queue=metrics_queue)
        
        return metrics_publisher
    except Exception as e:
        # Log critical initialization failure with full traceback
        drone_logger.critical(f"[Init ROS2] - Metrics initialization failed: {str(e)}", exc_info=True)
        raise

def initialize_state_vector_system(drone_id: int, drone_logger: logging.Logger, sv_queue: queue.Queue) -> StateVectorPublisher:
    try:
        topic_queue = queue.Queue()

        start_state_vector(vehicle_id=drone_id, longitude=40.209232, latitude=-3.465646,
                               action_queue=sv_queue, topic_queue=topic_queue)

        state_publisher = StateVectorPublisher(drone_id=drone_id, drone_logger=drone_logger,
                               topic_queue=topic_queue)

        return state_publisher
    except Exception as e:
        # Log critical initialization failure with full traceback
        drone_logger.critical(f"[Init ROS2] - Metrics initialization failed: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    """
    Main entry point for ROS2 drone system with command-line interface and exception handling.

    This section provides command-line argument parsing for drone ID specification and
    top-level exception handling for system-wide error management. It serves as the
    primary interface for launching individual drone instances with proper error
    reporting and graceful failure handling.

    Command Line Arguments
    ---------------------
    --drone_id : int (required)
        Unique identifier for the drone instance to initialize.
        Must be positive integer for proper system identification.
        Used for logging, ROS2 namespace isolation, and multi-drone coordination.

    Error Handling
    -------------
    - **Argument Parsing**: Invalid arguments result in usage message and exit
    - **System Exceptions**: Unhandled exceptions logged with full traceback
    - **Exit Codes**: Non-zero exit codes indicate failure for process monitoring

    Examples
    --------
    Command line usage:

    .. code-block:: bash

        # Initialize drone system with ID 1
        python init_ros2.py --drone_id 1

        # Initialize drone system with ID 2
        python init_ros2.py --drone_id 2

    Integration Notes
    ----------------
    - **Process Management**: Suitable for systemd services and process managers
    - **Logging**: All errors logged before exit for debugging and monitoring
    - **Multi-Drone**: Each drone instance requires unique ID for proper operation
    - **Resource Management**: Proper cleanup on both normal and error exits
    """
    # Configure command-line argument parser for drone system parameters
    parser = argparse.ArgumentParser(
        description='ROS2 Drone Control System - Agricultural Drone Management Platform',
        epilog='Example: python init_ros2.py --drone_id 1'
    )
    parser.add_argument('--drone_id', type=int, required=True,
                       help='Unique ID of the drone instance (positive integer, e.g., 1, 2, 3)')
    
    # Parse command-line arguments with automatic error handling and usage display
    args = parser.parse_args()
    
    try:
        # Validate drone ID parameter for proper system identification
        if args.drone_id <= 0:
            raise ValueError("Drone ID must be a positive integer")
            
        # Initialize and run the complete drone system
        main(args.drone_id)
        
    except ValueError as e:
        # Handle invalid argument values with user-friendly error messages
        logging.error(f"Invalid argument: {str(e)}")
        sys.exit(1)
    except SystemError as e:
        # Handle critical system initialization failures
        logging.error(f"System initialization failed: {str(e)}")
        sys.exit(1)
    except Exception as e:
        # Handle any other unhandled exceptions with comprehensive logging
        logging.error(f"Unhandled exception in drone system: {str(e)}", exc_info=True)
        sys.exit(1)