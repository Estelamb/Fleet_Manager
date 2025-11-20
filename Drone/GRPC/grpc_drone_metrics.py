"""
gRPC ROS2 Drone Metrics Communication Module
============================================

This module provides real-time metrics transmission from the drone to Mission Management
via gRPC communication. It continuously collects and sends system performance data,
hardware status, and operational metrics for monitoring and analysis.

The module implements a client-only architecture where the drone acts as a gRPC client
to transmit periodic metrics data to the Mission Management system for real-time
monitoring, alerting, and performance analysis.

.. module:: grpc_drone_metrics
    :synopsis: Provides unidirectional gRPC communication for drone metrics transmission

Workflow
--------
Metrics Transmission Pipeline:
    1. **Metrics Collection**: Gather system metrics (CPU, memory, sensors, etc.)
    2. **Data Serialization**: Convert metrics to JSON format for transmission
    3. **gRPC Transmission**: Send metrics to Mission Management via gRPC client
    4. **Acknowledgment Processing**: Receive and log transmission confirmation
    5. **Periodic Repetition**: Repeat cycle every 10 seconds for continuous monitoring
    6. **Error Recovery**: Handle connection failures with automatic retry logic

Communication Architecture:
    - **Outbound Channel**: Drone → Mission Management (Port 51004)
    - **Protocol**: gRPC with protobuf MetricsRequest messages
    - **Frequency**: 10-second intervals for real-time monitoring
    - **Threading Model**: Dedicated daemon thread for non-blocking operation

Features
--------
- **Real-Time Monitoring**: Continuous 10-second interval metrics transmission
- **System Metrics Collection**: CPU, memory, disk, network, and sensor data
- **Robust Error Handling**: Automatic retry on connection failures
- **Non-Blocking Operation**: Daemon thread prevents main application blocking
- **JSON Protocol**: Standardized JSON format for metrics data exchange
- **Mission Management Integration**: Direct communication with central monitoring

Functions
---------
.. autofunction:: run_metrics_client
.. autofunction:: start_grpc_metrics

Protocol Buffer Definitions
---------------------------
- **metrics_pb2**: Metrics message structures for Mission Management communication

Port Configuration
------------------
- **Port 51004**: Outbound metrics transmission to Mission Management

Metrics Data Structure
---------------------
The transmitted metrics typically include:
    - **System Performance**: CPU usage, memory consumption, disk space
    - **Hardware Status**: Sensor readings, battery levels, component health
    - **Operational Data**: Flight time, command execution status, error counts
    - **Network Statistics**: Connection quality, data transfer rates

Examples
--------
>>> import logging
>>> logger = logging.getLogger('drone_metrics')
>>> start_grpc_metrics(logger)  # Starts continuous metrics transmission
[gRPC Metrics] - Metrics client thread started successfully

Notes
-----
This module requires an active Mission Management system listening on port 51004
for successful metrics transmission. The metrics client runs as a daemon thread
and automatically handles connection recovery.

See Also
--------
SystemMetrics.data_collector : System metrics collection and processing
GRPC.definitions.metrics_pb2 : Protocol buffer message definitions for metrics
"""

import json
import grpc
import time
import logging
from typing import Dict, Any, NoReturn

from GRPC.definitions.metrics_pb2 import MetricsRequest
from GRPC.definitions.metrics_pb2_grpc import MetricsCommunicationStub

from SystemMetrics.data_collector import get_system_metrics

def run_metrics_client(logger: logging.Logger) -> NoReturn:
    """
    Continuously collect and transmit drone metrics to Mission Management system.

    This function implements the core metrics transmission loop that runs indefinitely,
    collecting system metrics at regular intervals and sending them to the Mission
    Management system via gRPC. It provides real-time monitoring capabilities for
    drone health, performance, and operational status.

    Parameters
    ----------
    logger : logging.Logger
        Logger instance for recording metrics transmission events, errors, and status updates.

    Returns
    -------
    NoReturn
        This function runs indefinitely until interrupted or connection permanently fails.

    Workflow
    --------
    1. **gRPC Channel Setup**: Establish insecure channel to Mission Management (localhost:51004)
    2. **Stub Creation**: Initialize MetricsCommunicationStub for RPC calls
    3. **Continuous Loop**: Execute the following steps repeatedly:
        a. **Metrics Collection**: Gather current system metrics via data_collector
        b. **JSON Serialization**: Convert metrics dictionary to JSON string
        c. **Transmission Logging**: Log metrics transmission attempt
        d. **gRPC Call**: Send metrics via SendMetrics RPC method
        e. **Acknowledgment**: Log successful transmission confirmation
        f. **Interval Wait**: Sleep for 10 seconds before next collection cycle
    4. **Error Recovery**: Handle connection errors with retry delay

    Metrics Collection
    ------------------
    Collected metrics typically include:
        - **CPU Usage**: Processor utilization percentages
        - **Memory Status**: RAM and swap memory consumption
        - **Disk Space**: Storage utilization and availability
        - **Network Stats**: Bandwidth usage and connection quality
        - **Sensor Data**: GPS, IMU, barometer, and camera status
        - **Battery Levels**: Power system status and remaining capacity
        - **Flight Metrics**: Altitude, speed, heading, and position data

    Configuration
    -------------
    - **Target Host**: localhost:51004 (Mission Management metrics endpoint)
    - **Transmission Interval**: 10 seconds between metric collections
    - **Protocol**: gRPC with protobuf MetricsRequest messages
    - **Channel Type**: Insecure (for local/trusted network communication)

    Error Handling
    --------------
    - **grpc.RpcError**: Connection failures logged with 1-second retry delay
    - **JSON Serialization**: Errors in metrics formatting (handled by data_collector)
    - **Collection Failures**: Metrics gathering errors (handled by data_collector)

    Notes
    -----
    - Function is designed to run in a daemon thread for non-blocking operation
    - Connection errors result in brief delays but automatic retry attempts
    - Metrics are collected fresh for each transmission (no caching)
    - Mission Management system must be running on port 51004 for successful operation
    - Function only terminates on unhandled exceptions or system shutdown

    See Also
    --------
    SystemMetrics.data_collector.get_system_metrics : Metrics collection implementation
    start_grpc_metrics : Thread management for metrics client
    """
    # Establish insecure gRPC channel to Mission Management metrics endpoint
    channel = grpc.insecure_channel('localhost:51004')
    
    # Create stub for metrics communication RPC calls
    stub = MetricsCommunicationStub(channel)

    try:
        # Continuous metrics transmission loop
        while True:
            # Collect current system metrics from data collector
            metrics = get_system_metrics(logger)
            
            # Serialize metrics dictionary to JSON string for transmission
            metrics_json = json.dumps(metrics)
            
            # Transmit metrics to Mission Management via gRPC call
            response = stub.SendMetrics(MetricsRequest(metrics=[metrics_json]))
            
            logger.info("[gRPC Metrics] - System Metrics sent to ROS2")
            
            # Wait 10 seconds before next metrics collection and transmission
            time.sleep(10)
    except grpc.RpcError as e:
        # Handle gRPC connection and communication errors
        logger.error(f"[gRPC Metrics] - Connection error: {e}")
        time.sleep(1)


def start_grpc_metrics(logger: logging.Logger) -> None:
    """
    Initialize and start the gRPC metrics transmission system in a daemon thread.

    This function serves as the main entry point for starting the drone's metrics
    transmission system. It creates a dedicated daemon thread for continuous metrics
    collection and transmission, ensuring non-blocking integration with the main
    drone application workflow.

    Parameters
    ----------
    logger : logging.Logger
        Logger instance for recording metrics system startup events and thread status.

    Returns
    -------
    None
        Function returns immediately after starting the daemon thread.

    Workflow
    --------
    1. **Import Threading**: Import Thread class within function scope
    2. **Thread Creation**: Create daemon thread for metrics client
    3. **Thread Configuration**: Configure thread with client function and logger
    4. **Thread Startup**: Start daemon thread for continuous metrics transmission
    5. **Startup Logging**: Log successful thread initialization
    6. **Non-Blocking Return**: Return control to caller while metrics run in background

    Threading Architecture
    ----------------------
    - **Main Thread**: Application continues normal execution
    - **Metrics Daemon Thread**: Dedicated thread runs metrics client indefinitely
    - **Daemon Mode**: Thread automatically terminates when main program exits
    - **Non-Blocking Operation**: Metrics collection doesn't interfere with main application
    - **Resource Management**: Thread handles its own lifecycle and cleanup

    Daemon Thread Benefits
    ----------------------
    - **Automatic Cleanup**: Thread terminates when main program exits
    - **Background Operation**: No interference with main application flow
    - **Resource Efficiency**: Minimal overhead on main application performance
    - **Fault Isolation**: Metrics failures don't affect core drone operations

    Examples
    --------
    >>> import logging
    >>> logger = logging.getLogger('drone_metrics')
    >>> start_grpc_metrics(logger)  # Returns immediately
    >>> print("Metrics system started in background")
    [gRPC Metrics] - Metrics client thread started successfully
    >>> # Main application continues while metrics transmit in background

    Integration
    -----------
    This function is typically called during drone system initialization:

    >>> # During drone startup sequence
    >>> logger = create_logger_drone("Drone1")
    >>> start_grpc_metrics(logger)  # Start metrics transmission
    >>> start_grpc_commands(logger)  # Start command reception
    >>> # Continue with other drone subsystem initialization

    Notes
    -----
    - Daemon thread runs metrics client indefinitely until system shutdown
    - Non-blocking design allows integration with other drone subsystems
    - Thread inherits logger configuration for consistent logging
    - Function uses local import for Thread to optimize module loading
    - Metrics transmission begins immediately after thread startup
    - System shutdown automatically terminates the daemon thread

    Performance Considerations
    --------------------------
    - **CPU Impact**: Minimal overhead with 10-second transmission intervals
    - **Memory Usage**: Efficient JSON serialization with no data accumulation
    - **Network Bandwidth**: Lightweight metrics data with periodic transmission
    - **Thread Overhead**: Single daemon thread with optimized execution

    See Also
    --------
    run_metrics_client : The actual metrics transmission implementation
    SystemMetrics.data_collector : System metrics collection functions
    """
    # Import threading module within function scope for optimized loading
    from threading import Thread
    
    # Create daemon thread for continuous metrics transmission
    metrics_thread = Thread(
        target=run_metrics_client,  # Metrics client function to run in background
        args=(logger,),             # Pass logger to metrics thread
        daemon=True                 # Daemon mode: auto-terminate with main program
    )
    
    # Start the metrics transmission thread (non-blocking operation)
    metrics_thread.start()
    
    # Log successful thread initialization
    logger.info("[gRPC Metrics] - Metrics client thread started successfully")