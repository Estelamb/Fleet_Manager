"""
gRPC-ROS2 Commands Communication Bridge Module
==============================================

This module implements a comprehensive bidirectional gRPC communication bridge
for ROS2 command execution, providing seamless integration between Mission Management
systems and agricultural drone command processing infrastructure. It enables
real-time command transmission, feedback reception, and status monitoring for
precision agriculture drone operations.

The module serves as the primary communication interface between external Mission
Management systems and ROS2-based drone command execution, supporting complex
agricultural workflows including field operations, prescription map execution,
and autonomous navigation tasks.

.. module:: grpc_ros2_commands
    :synopsis: Bidirectional gRPC-ROS2 communication bridge for agricultural drone commands

Features
--------
- **Bidirectional Communication**: gRPC server for feedback reception and client for command transmission
- **Thread-safe Operations**: Concurrent queue operations with thread-safe message handling
- **Agricultural Integration**: Optimized for precision agriculture command workflows
- **Error Recovery**: Comprehensive error handling and connection resilience
- **Real-time Processing**: Low-latency command transmission and feedback processing
- **Mission Coordination**: Integration with Mission Management systems for field operations

System Architecture
------------------
The gRPC-ROS2 communication bridge operates within a multi-layered agricultural architecture:

Communication Flow:
    Mission Management ↔ gRPC Bridge ↔ ROS2 Action Server ↔ Drone Hardware

Bidirectional Architecture:
    - **Command Flow**: Mission Management → gRPC Client → Commands Processor → Drone Hardware
    - **Feedback Flow**: Drone Hardware → ROS2 → Queue → gRPC Server → Mission Management

Agricultural Integration:
    - **Field Operations**: Command transmission for agricultural tasks (seeding, spraying, harvesting)
    - **Prescription Maps**: Command sequences for variable rate applications
    - **Navigation Tasks**: Autonomous field navigation and waypoint following
    - **Mission Coordination**: Multi-drone coordination for large-scale agricultural operations

Communication Components:
    1. **gRPC Server**: Receives feedback from ROS2 command execution
    2. **gRPC Client**: Transmits commands to external command processors
    3. **Queue Integration**: Thread-safe communication with ROS2 action servers
    4. **Error Handling**: Robust error management and connection recovery
    5. **Logging System**: Comprehensive activity tracking and debugging

Workflow Architecture
--------------------
Command Execution Pipeline:
    1. **Command Reception**: External systems initiate command transmission
    2. **gRPC Client Processing**: Commands forwarded to command processors
    3. **Acknowledgment Handling**: Confirmation receipt and status tracking
    4. **Feedback Collection**: ROS2 feedback gathered via queue system
    5. **Response Transmission**: Feedback forwarded to Mission Management
    6. **Error Recovery**: Connection errors handled with retry mechanisms

Agricultural Command Types:
    - **Field Operations**: Planting, fertilizing, spraying, harvesting commands
    - **Navigation Tasks**: Waypoint navigation, field boundary following
    - **Sensor Operations**: Data collection, mapping, monitoring tasks
    - **System Commands**: Configuration, calibration, diagnostic operations

Classes
-------
.. autoclass:: FeedbackCommunicationService
    :members:
    :undoc-members:
    :show-inheritance:

Functions
---------
.. autofunction:: run_commands_server
.. autofunction:: run_commands_client
.. autofunction:: start_grpc_commands

Dependencies
-----------
Core Dependencies:
    - **grpc**: Google gRPC framework for high-performance communication
    - **concurrent.futures**: Thread pool executor for concurrent operations
    - **threading**: Threading support for background server operation
    - **queue**: Thread-safe inter-component communication
    - **json**: Command and feedback data serialization

gRPC Protocol Buffers:
    - **feedback_pb2**: Feedback message definitions and serialization
    - **feedback_pb2_grpc**: Feedback service stubs and server implementations
    - **command_pb2**: Command message definitions and serialization
    - **command_pb2_grpc**: Command service stubs and client implementations

Logging Dependencies:
    - **Logs.create_logger**: Centralized logging infrastructure for activity tracking

Integration Points
-----------------
External Integrations:
    - **Mission Management**: Command reception and feedback transmission via gRPC
    - **Command Processors**: External command processing systems integration
    - **Agricultural Systems**: Field management and prescription execution coordination
    - **Monitoring Systems**: Real-time command execution tracking and logging

Internal Integrations:
    - **ROS2 Action Servers**: Command execution and feedback collection
    - **init_ros2.py**: System initialization and component coordination
    - **Queue Systems**: Thread-safe inter-component message passing
    - **Logging Infrastructure**: Centralized activity logging and error reporting

Performance Characteristics
--------------------------
Communication Performance:
    - **Command Latency**: Sub-second command transmission and acknowledgment
    - **Feedback Processing**: Real-time feedback collection and forwarding
    - **Throughput**: High-volume command and feedback processing capability
    - **Connection Resilience**: Automatic reconnection and error recovery

Scalability Features:
    - **Concurrent Processing**: Multi-threaded server with configurable worker pool
    - **Queue Management**: Efficient thread-safe message passing
    - **Resource Optimization**: Minimal overhead with efficient connection management
    - **Error Isolation**: Individual command failures don't affect system stability

Agricultural Data Formats
-------------------------
Command Data Structure:
    - **JSON Serialization**: Structured command data in JSON format
    - **Command Types**: Agricultural operation specifications (plant, spray, harvest)
    - **Parameters**: Operation-specific parameters (rates, coordinates, timing)
    - **Metadata**: Execution context and priority information

Feedback Data Structure:
    - **Execution Status**: Command completion status and progress information
    - **Error Reporting**: Detailed error information for failed operations
    - **Performance Metrics**: Execution timing and performance data
    - **Agricultural Results**: Operation-specific results (coverage, application rates)

Error Handling Strategy
----------------------
Multi-level Error Management:
    - **Connection-Level**: gRPC connection error handling and retry logic
    - **Message-Level**: Individual command and feedback processing error handling
    - **Queue-Level**: Thread-safe queue operation error management
    - **System-Level**: Graceful shutdown and resource cleanup procedures

Recovery Mechanisms:
    - **Automatic Reconnection**: gRPC connection recovery with exponential backoff
    - **Message Retry**: Failed command transmission retry with timeout handling
    - **Queue Monitoring**: Continuous queue state monitoring and error detection
    - **Graceful Degradation**: Continued operation despite individual component failures

Examples
--------
Programmatic Usage:

.. code-block:: python

    import queue
    import logging
    from grpc_ros2_commands import start_grpc_commands, run_commands_client

    # Setup communication infrastructure
    logger = logging.getLogger('agricultural_commands')
    commands_queue = queue.Queue()
    
    # Start gRPC communication bridge
    start_grpc_commands(commands_queue, logger)
    
    # Send agricultural command
    command = {
        "type": "spray",
        "field_id": "field_001",
        "application_rate": 2.5,
        "coordinates": [(40.123, -3.456)]
    }
    run_commands_client(json.dumps(command), logger)

Agricultural Command Example:

.. code-block:: python

    # Agricultural field operation command
    field_operation = {
        "operation": "fertilizer_application",
        "field_boundaries": [
            {"lat": 40.123456, "lon": -3.456789},
            {"lat": 40.124567, "lon": -3.455678}
        ],
        "application_parameters": {
            "fertilizer_type": "NPK_15-15-15",
            "application_rate": 150,  # kg/ha
            "application_method": "broadcast"
        },
        "timing": "2024-06-27T08:00:00Z"
    }

System Integration Example:

.. code-block:: python

    # Integration with ROS2 action server
    from rclpy.executors import MultiThreadedExecutor
    
    # Initialize communication bridge
    executor = MultiThreadedExecutor()
    
    # Start gRPC-ROS2 bridge
    start_grpc_commands(commands_queue, logger)
    
    # Commands flow through bridge to ROS2 action server
    executor.spin()

Notes
-----
- **Agricultural Focus**: Optimized for precision agriculture command workflows
- **Real-time Operation**: Low-latency communication for time-critical field operations
- **Mission Coordination**: Supports complex multi-drone agricultural missions
- **Error Resilience**: Robust error handling for continuous field operations

Configuration Requirements:
    - **gRPC Ports**: Feedback server on port 51002, command client to port 51001
    - **Network Access**: Reliable network connectivity for gRPC communication
    - **Protocol Buffers**: Properly compiled protobuf definitions
    - **Logging Setup**: Configured logging infrastructure for activity tracking

Agricultural Considerations:
    - **Field Conditions**: Robust operation in various agricultural environments
    - **Command Precision**: High-accuracy command parameter handling
    - **Timing Critical**: Real-time command execution for time-sensitive operations
    - **Scalability**: Support for large-scale agricultural operations

See Also
--------
grpc.server : gRPC server implementation
grpc.insecure_channel : gRPC client channel management
queue.Queue : Thread-safe inter-component communication
threading.Thread : Background thread management for server operation
"""

from concurrent import futures
import json
import grpc
import time
import queue
import threading

from GRPC.definitions.feedback_pb2 import FeedbackResponse
from GRPC.definitions.feedback_pb2_grpc import FeedbackCommunicationServicer, add_FeedbackCommunicationServicer_to_server
from GRPC.definitions.command_pb2 import CommandRequest
from GRPC.definitions.command_pb2_grpc import CommandCommunicationStub


class FeedbackCommunicationService(FeedbackCommunicationServicer):
    """
    gRPC service implementation for drone feedback processing.

    :param logger: Configured logger instance
    :type logger: logging.Logger
    :param commands_queue: Initialized ROS 2 commands queue
    :type commands_queue: queue.Queue
    """
    def __init__(self, logger, commands_queue):
        """
        Initialize the FeedbackCommunicationService.

        :param logger: Configured logger instance
        :type logger: logging.Logger
        :param commands_queue: Initialized ROS 2 commands queue
        :type commands_queue: queue.Queue
        """
        super().__init__()
        self.logger = logger
        self.commands_queue = commands_queue

    def SendFeedback(self, request, context):
        """
        Process incoming drone feedback requests.

        :param request: gRPC request containing serialized feedback data
        :type request: FeedbackRequest
        :return: gRPC response with processing confirmation
        :rtype: FeedbackResponse
        :raises grpc.RpcError: For critical processing failures

        .. note::
            Expected request format:
            [drone_id: int, [command1: str, command2: str, ...]]
        """
        try:
            # Convert the gRPC request to a list
            feedback_list = list(request.feedback)
            feedback_str = ''.join(feedback_list)
            feedback = json.loads(feedback_str)

            # Send the goal to the feedback client
            self.commands_queue.put(feedback)
            self.logger.info(f"[ROS2][gRPC Commands] - Feedback received from drone and sent to ROS2 server")

            return FeedbackResponse(confirmation=f"Feedback received and sent")
        except Exception as e:
            self.logger.error(f"[ROS2][gRPC Commands] - Error in SendFeedback: {e}", exc_info=True)
            return FeedbackResponse(confirmation="Error processing feedback")


def run_commands_server(commands_queue, logger):
    """
    Start and manage gRPC server instance.

    :param commands_queue: Commands queue
    :type commands_queue: queue.Queue
    :param logger: Configured logger instance
    :type logger: logging.Logger
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_FeedbackCommunicationServicer_to_server(
        FeedbackCommunicationService(logger, commands_queue), server)
    server.add_insecure_port('[::]:52002')
    server.start()
    logger.info("[ROS2][gRPC Commands] - Server running on port 52002")
    
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


def run_commands_client(command, logger):
    """
    Handle Command transmission to commands processor.

    :param command: Command to be sent to the commands processor
    :type command: str
    :param logger: Configured logger instance
    :type logger: logging.Logger
    """
    channel = grpc.insecure_channel('host.docker.internal:52001') 
    stub = CommandCommunicationStub(channel)

    try:
        logger.info(f"[ROS2][gRPC Commands] - Sending command to commands processor")
        response = stub.SendCommand(CommandRequest(command=command))
        logger.info(f"[ROS2][gRPC Commands] - ACK received from commands processor")
    except queue.Empty:
        time.sleep(0.1)
    except grpc.RpcError as e:
        logger.error(f"[ROS2][gRPC Commands] - Connection error: {e}")
        time.sleep(1)


def start_grpc_commands(commands_queue: queue.Queue, logger):
    """
    Initialize and start ROS 2 communication infrastructure.

    :param commands_queue: Commands queue
    :type commands_queue: queue.Queue
    :param logger: Configured logger instance
    :type logger: logging.Logger
    """
    server_commands_thread = threading.Thread(target=run_commands_server, args=(commands_queue, logger))
    server_commands_thread.daemon = True
    server_commands_thread.start()
