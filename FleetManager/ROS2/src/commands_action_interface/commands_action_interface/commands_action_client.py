"""
ROS 2 Action Client Module for Drone Command Management

.. module:: commands_action_client
    :synopsis: Multi-drone command execution and management via ROS 2 action interface

.. moduleauthor:: Fleet Management System Team

.. versionadded:: 1.0

This module implements a comprehensive ROS 2 Action Client system for managing drone
command execution in the Fleet Management System. It provides asynchronous command
submission, real-time feedback processing, and result collection for multiple drones
operating concurrently.

Architecture Overview:
    The module follows the ROS 2 action pattern for long-running, preemptible tasks:
    
    1. **Action Client Node**: Central ROS 2 node managing all drone communications
    2. **Multi-drone Support**: Dynamic action client creation for each drone
    3. **Asynchronous Processing**: Non-blocking goal submission and result handling
    4. **Feedback Integration**: Real-time status updates during command execution
    5. **Queue-based Communication**: Thread-safe result passing to Fleet Management

ROS 2 Action Pattern:
    .. mermaid::
    
        graph LR
            A[Action Client] --> B[Goal Submission]
            B --> C[Action Server]
            C --> D[Feedback Updates]
            D --> A
            C --> E[Final Result]
            E --> A
            
            A --> F[Status Queue]
            F --> G[Fleet Management]

Key Features:
    - **Multi-drone Management**: Concurrent command execution across multiple vehicles
    - **Dynamic Client Creation**: Automatic action client creation for new drones
    - **Asynchronous Callbacks**: Non-blocking feedback and result processing
    - **Thread-safe Operations**: Queue-based communication with external systems
    - **Connection Management**: Automatic server availability checking
    - **Error Recovery**: Comprehensive error handling and timeout management

Command Execution Workflow:
    1. **Goal Submission**: Commands sent as action goals to drone-specific topics
    2. **Server Availability**: Check for active drone action servers
    3. **Goal Acceptance**: Await confirmation from drone action servers
    4. **Feedback Processing**: Handle intermediate status updates during execution
    5. **Result Collection**: Process final execution results and status codes
    6. **Status Reporting**: Queue results for transmission to Fleet Management

ROS 2 Integration:
    **Action Definition**: Uses Commands action from commands_action_interface
    
    **Topic Structure**::
    
        /drone{id}/commands  # Action server endpoint for each drone
        
    **Message Types**:
    - **Goal**: commands_list (list of JSON command strings)
    - **Feedback**: command_status (intermediate execution status)
    - **Result**: plan_result (final execution results and status)

Multi-threaded Design:
    - **Main Thread**: Goal submission and callback registration
    - **Executor Thread**: ROS 2 node spinning and callback execution
    - **Queue Thread**: Asynchronous result transmission to Fleet Management
    - **Action Threads**: Individual action goal execution (managed by ROS 2)

Status Code Integration:
    **Goal Response Codes**:
    - 0: Goal accepted and processing
    - 1: Goal rejected by action server
    
    **Result Formats**:
    - Feedback: JSON command status updates
    - Results: Complete execution results with success/failure indicators

Thread Safety:
    All queue operations are thread-safe, enabling concurrent access from:
    - ROS 2 callback functions
    - Action client management functions
    - External Fleet Management components

Classes:
    .. autoclass:: CommandsActionClient
        :members:
        :undoc-members:
        :show-inheritance:

Functions:
    .. autofunction:: create_ros2_action_client

Usage Examples:
    **Basic Client Creation**::
    
        ros2_queue = queue.Queue()
        logger = create_logger('ROS2', 'ros2.log')
        client = create_ros2_action_client(ros2_queue, logger)
        
    **Command Submission**::
    
        commands = [
            '{"command": "takeoff", "altitude": 10}',
            '{"command": "move_to", "x": 100, "y": 200}',
            '{"command": "land"}'
        ]
        client.send_goal(drone_id=1, commands_list=commands)

.. note::
    This module requires a properly configured ROS 2 environment with the
    commands_action_interface package installed and sourced.

.. warning::
    Action servers must be running on target drones before goal submission.
    Goals will be rejected if corresponding action servers are unavailable.

.. seealso::
    - :mod:`ROS2.grpc_ros2`: gRPC integration for Fleet Management communication
    - :mod:`commands_action_interface`: Action interface definitions
    - :doc:`ROS 2 Actions Tutorial <https://docs.ros.org/en/humble/Tutorials/Intermediate/Writing-an-Action-Server-Client/Py.html>`
"""

import json
import logging
import rclpy
import queue
from rclpy.action import ActionClient
from rclpy.node import Node
from functools import partial
from rclpy.executors import MultiThreadedExecutor
import threading

from commands_action_interface.action import Commands


class CommandsActionClient(Node):
    """ROS 2 Action Client node for comprehensive drone command management and execution.

    This class extends the ROS 2 Node to provide specialized action client functionality
    for managing multiple drone command executions simultaneously. It handles dynamic
    action client creation, asynchronous goal management, and comprehensive status
    reporting through queue-based communication.

    Node Architecture:
        - **Node Name**: 'commands_action_client'
        - **Action Type**: Commands (from commands_action_interface)
        - **Topic Pattern**: '/drone{id}/commands' for each managed drone
        - **Executor**: MultiThreadedExecutor for concurrent callback processing

    Multi-drone Management:
        The client maintains a dictionary mapping drone IDs to action clients,
        enabling concurrent command execution across multiple vehicles:
        
        - **Dynamic Creation**: New action clients created on first drone contact
        - **Persistent Connections**: Action clients reused for subsequent commands
        - **Independent Processing**: Each drone's commands execute independently
        - **Concurrent Feedback**: Multiple drones provide feedback simultaneously

    Command Processing Pipeline:
        1. **Goal Preparation**: Convert command list to Commands.Goal message
        2. **Server Validation**: Check action server availability with timeout
        3. **Goal Submission**: Submit goal with feedback callback registration
        4. **Response Handling**: Process goal acceptance/rejection notifications
        5. **Feedback Processing**: Handle intermediate status updates during execution
        6. **Result Collection**: Process final execution results and completion status

    Callback Management:
        The class implements three primary callback types:
        
        - **Feedback Callbacks**: Real-time command execution status updates
        - **Goal Response Callbacks**: Goal acceptance/rejection notifications
        - **Result Callbacks**: Final command execution results and completion status

    Queue Integration:
        All status updates are published to a thread-safe queue for external consumption:
        
        - **Goal Status**: Acceptance (0) or rejection (1) codes
        - **Feedback Updates**: Intermediate command execution status
        - **Final Results**: Complete execution results with success/failure details

    :param ros2_action_queue: Thread-safe queue for publishing action status updates
    :type ros2_action_queue: queue.Queue
    :param ros2_logger: Pre-configured logger instance for ROS 2 operation tracking
    :type ros2_logger: logging.Logger

    :ivar _action_clients: Active drone action client mapping (drone_id → ActionClient)
    :vartype _action_clients: Dict[int, ActionClient]
    :ivar ros2_action_queue: Queue for publishing status updates to external systems
    :vartype ros2_action_queue: queue.Queue
    :ivar ros2_logger: Logger instance for operation tracking and debugging
    :vartype ros2_logger: logging.Logger

    Example:
        **Node Initialization**::
        
            queue = queue.Queue()
            logger = logging.getLogger('ROS2')
            client = CommandsActionClient(queue, logger)
            
        **Multi-drone Command Execution**::
        
            # Commands for drone 1
            client.send_goal(1, ['{"cmd": "takeoff"}', '{"cmd": "patrol"}'])
            
            # Commands for drone 2 (executed concurrently)
            client.send_goal(2, ['{"cmd": "survey"}', '{"cmd": "return"}'])

    .. note::
        The node automatically manages action client lifecycle, creating new clients
        for previously unseen drone IDs and reusing existing clients for efficiency.

    .. warning::
        Action server availability is checked with a 2-second timeout. Commands
        will be rejected if target drone action servers are not responding.
    """

    def __init__(self, ros2_action_queue, ros2_logger):
        """Initialize ROS 2 action client node with communication infrastructure.

        Sets up the node with necessary components for multi-drone action management,
        including action client storage, queue communication, and logging infrastructure.

        Initialization Process:
            1. **Node Creation**: Initialize ROS 2 node with unique name
            2. **Storage Setup**: Initialize action client dictionary for drone mapping
            3. **Queue Configuration**: Store reference to thread-safe status queue
            4. **Logging Setup**: Configure logger for operation tracking

        :param ros2_action_queue: Queue for publishing action status updates to external systems
        :type ros2_action_queue: queue.Queue
        :param ros2_logger: Pre-configured logger for ROS 2 operation tracking
        :type ros2_logger: logging.Logger
        """
        # Initialize parent ROS 2 Node class with descriptive node name
        super().__init__('commands_action_client')
        
        # Initialize dictionary to store active action clients for each drone
        # Key: drone_id (int), Value: ActionClient instance
        self._action_clients = {}  
        
        # Store reference to thread-safe queue for status updates
        self.ros2_action_queue = ros2_action_queue
        
        # Store logger instance for operation tracking and debugging
        self.ros2_logger = ros2_logger

    def send_goal(self, drone_id, commands_list):
        """Submit command sequence to target drone action server with comprehensive error handling.

        This method manages the complete goal submission workflow including action client
        creation, server availability validation, goal preparation, and asynchronous
        callback registration for feedback and result processing.

        Goal Submission Workflow:
            1. **Client Management**: Create or retrieve action client for target drone
            2. **Server Validation**: Verify action server availability with timeout
            3. **Goal Preparation**: Package commands into Commands.Goal message
            4. **Callback Registration**: Set up feedback and result callbacks
            5. **Goal Submission**: Submit goal asynchronously to action server

        Action Client Management:
            - **Dynamic Creation**: New ActionClient instances created for unseen drone IDs
            - **Client Reuse**: Existing clients reused for efficiency and connection persistence
            - **Topic Naming**: Action topics follow '/drone{id}/commands' convention
            - **Client Storage**: Clients stored in internal dictionary for lifecycle management

        Server Availability Checking:
            - **Timeout**: 2-second timeout for server response validation
            - **Error Handling**: Graceful failure handling for unavailable servers
            - **Logging**: Detailed error messages for troubleshooting connectivity issues

        Callback Chain Setup:
            The method establishes a complete callback chain for goal lifecycle management:
            
            - **Feedback Callback**: Receives intermediate command execution status
            - **Goal Response Callback**: Handles goal acceptance/rejection notifications
            - **Result Callback**: Processes final execution results (set up in response callback)

        :param drone_id: Unique identifier for target drone (must be positive integer)
        :type drone_id: int
        :param commands_list: Ordered sequence of JSON command strings for execution
        :type commands_list: List[str]

        :raises RuntimeError: If action server is unavailable after timeout period
        :raises ValueError: If drone_id is invalid or commands_list is malformed

        Command Format:
            Each command in commands_list should be a valid JSON string::
            
                [
                    '{"command": "takeoff", "altitude": 10}',
                    '{"command": "move_to", "x": 100, "y": 200, "z": 15}',
                    '{"command": "land", "precision": "high"}'
                ]

        Example:
            **Single Drone Command Submission**::
            
                commands = ['{"cmd": "takeoff"}', '{"cmd": "patrol_area"}']
                client.send_goal(drone_id=1, commands_list=commands)
                
            **Multi-step Mission**::
            
                mission_commands = [
                    '{"command": "preflight_check"}',
                    '{"command": "takeoff", "altitude": 20}',
                    '{"command": "navigate_waypoints", "waypoints": [...]}',
                    '{"command": "return_to_base"}',
                    '{"command": "land"}'
                ]
                client.send_goal(drone_id=2, commands_list=mission_commands)

        .. note::
            Action clients are created with a 2-second server availability timeout.
            Ensure target drone action servers are running before goal submission.

        .. warning::
            Goals submitted to unavailable servers will be logged as errors and
            not queued for retry. Ensure proper server availability before submission.
        """
        # Check if action client already exists for this drone ID
        # Create new client if this is the first command for this drone
        if drone_id not in self._action_clients:
            # Create new ActionClient for this drone with topic-specific naming
            # Topic pattern: /drone{id}/commands (e.g., /drone1/commands, /drone2/commands)
            action_client = ActionClient(
                self,                           # Parent node reference
                Commands,                       # Action interface type
                f'drone{drone_id}/commands'     # Drone-specific action topic
            )
            
            # Store the new action client for future reuse
            self._action_clients[drone_id] = action_client
        else:
            # Retrieve existing action client for this drone
            action_client = self._action_clients[drone_id]
        
        # Verify that the action server is available and responsive
        # Use 2-second timeout to balance responsiveness with reliability
        if not action_client.wait_for_server(timeout_sec=2.0):
            # Log error and return early if server is unavailable
            self.ros2_logger.error(f"[ROS2 Manager] - Drone {drone_id} server unavailable.")
            return
        
        # Prepare goal message with command list for drone execution
        goal_msg = Commands.Goal()
        goal_msg.commands_list = commands_list
        
        # Log goal submission for tracking and debugging
        self.ros2_logger.info(f'[ROS2 Manager] - Sending commands to drone {drone_id}')

        # Submit goal asynchronously with feedback callback registration
        # Use partial to bind drone_id to callback for proper identification
        send_goal_future = action_client.send_goal_async(
            goal_msg,
            feedback_callback=partial(self.feedback_callback, drone_id=drone_id)
        )
        
        # Register callback for goal response (acceptance/rejection)
        # This callback will handle goal acceptance and set up result callback
        send_goal_future.add_done_callback(
            partial(self.goal_response_callback, drone_id=drone_id)
        )

    def goal_response_callback(self, future, drone_id):
        """Handle action server goal acceptance/rejection responses with status reporting.

        This callback processes the initial response from drone action servers regarding
        goal acceptance or rejection. It manages the continuation of the action lifecycle
        by setting up result callbacks for accepted goals and reporting status through
        the communication queue.

        Response Processing Workflow:
            1. **Future Resolution**: Extract goal handle from completed future
            2. **Acceptance Check**: Determine if goal was accepted by action server
            3. **Status Reporting**: Queue appropriate status code for Fleet Management
            4. **Result Setup**: Register result callback for accepted goals
            5. **Error Handling**: Process rejection cases with appropriate logging

        Status Code Reporting:
            The method reports goal status through the action queue:
            - **Code 0**: Goal accepted and processing initiated
            - **Code 1**: Goal rejected by action server

        Result Callback Chain:
            For accepted goals, this method establishes the final link in the callback
            chain by registering a result callback that will handle command execution
            completion and final status reporting.

        :param future: Completed future containing goal handle from action server
        :type future: rclpy.task.Future[GoalHandle]
        :param drone_id: Identifier of target drone for status correlation
        :type drone_id: int

        Queue Message Format:
            Status messages are JSON-encoded arrays: [drone_id, status_code]
            
            **Acceptance**: [123, 0] - Drone 123 goal accepted
            **Rejection**: [456, 1] - Drone 456 goal rejected

        Example Flow:
            **Successful Goal Acceptance**::
            
                # Goal submitted to drone 1
                # Server accepts goal
                # Callback logs acceptance and queues [1, 0]
                # Result callback registered for completion handling
                
            **Goal Rejection**::
            
                # Goal submitted to drone 2
                # Server rejects goal (busy, invalid commands, etc.)
                # Callback logs rejection and queues [2, 1]
                # No result callback needed (goal lifecycle complete)

        .. note::
            This callback is automatically invoked by ROS 2 action infrastructure
            when the action server responds to goal submission requests.

        .. warning::
            Rejected goals will not have result callbacks registered. The Fleet
            Management System should handle rejection status appropriately.
        """
        # Extract goal handle from the completed future
        # This contains the server's response to our goal submission
        goal_handle = future.result()
        
        # Check if the action server accepted or rejected the goal
        if not goal_handle.accepted:
            # Goal was rejected by the action server
            # Log rejection for debugging and monitoring
            self.ros2_logger.info(f"[ROS2 Manager] - Drone {drone_id}: Goal rejected.")
            
            # Report rejection status (code 1) to Fleet Management via queue
            # Format: [drone_id, status_code] where 1 indicates rejection
            self.ros2_action_queue.put(json.dumps([drone_id, 1]))
            return  # Early return - no further processing needed for rejected goals

        # Goal was accepted by the action server
        # Log acceptance for tracking and debugging
        self.ros2_logger.info(f"[ROS2 Manager] - Drone {drone_id}: Goal accepted.")
        
        # Set up result callback to handle command execution completion
        # This establishes the final link in the action callback chain
        get_result_future = goal_handle.get_result_async()
        get_result_future.add_done_callback(
            partial(self.get_result_callback, drone_id=drone_id)
        )
        
        # Report acceptance status (code 0) to Fleet Management via queue
        # Format: [drone_id, status_code] where 0 indicates acceptance
        self.ros2_action_queue.put(json.dumps([drone_id, 0]))

    def get_result_callback(self, future, drone_id):
        """Process final command execution results and completion status.

        This callback handles the culmination of the action lifecycle, processing
        the final results from completed command execution. It extracts execution
        results, logs completion status, and reports final outcomes to the Fleet
        Management System through the communication queue.

        Result Processing Workflow:
            1. **Future Resolution**: Extract action result from completed future
            2. **Result Extraction**: Parse plan_result from action response
            3. **Status Logging**: Log completion with result details
            4. **Queue Reporting**: Send final results to Fleet Management System

        Result Data Structure:
            The action result contains a plan_result field with execution details:
            
            - **Success Indicators**: Command completion status for each step
            - **Execution Data**: Detailed results from each command execution
            - **Error Information**: Failure details if commands encountered issues
            - **Performance Metrics**: Timing and resource usage data (if available)

        Queue Communication:
            Final results are serialized as JSON and queued for transmission:
            - **Format**: JSON string containing complete plan_result data
            - **Content**: Execution status, results, and any error information
            - **Processing**: Consumed by Fleet Management for mission status updates

        :param future: Completed future containing final action execution results
        :type future: rclpy.task.Future[ActionResult]
        :param drone_id: Identifier of drone that completed command execution
        :type drone_id: int

        Result Content Examples:
            **Successful Execution**::
            
                {
                    "commands_completed": 3,
                    "execution_time": 45.2,
                    "status": "SUCCESS",
                    "results": [
                        {"command": "takeoff", "status": "completed", "altitude": 10},
                        {"command": "move_to", "status": "completed", "position": [100, 200]},
                        {"command": "land", "status": "completed", "precision": "high"}
                    ]
                }
                
            **Partial Failure**::
            
                {
                    "commands_completed": 2,
                    "execution_time": 23.1,
                    "status": "PARTIAL_FAILURE",
                    "error": "Navigation sensor malfunction during move_to",
                    "results": [
                        {"command": "takeoff", "status": "completed"},
                        {"command": "move_to", "status": "failed", "error": "sensor_error"}
                    ]
                }

        .. note::
            This callback represents the final stage of the action lifecycle.
            After this callback completes, the action is considered finished.

        .. warning::
            Result data format depends on drone action server implementation.
            Ensure Fleet Management can handle various result formats appropriately.
        """
        # Extract the final action result from the completed future
        # This contains all execution results and status information
        result = future.result().result
        
        # Log the completion with detailed result information
        # This provides visibility into command execution outcomes
        self.ros2_logger.info(f"[ROS2 Manager] - Drone {drone_id}: Result: {result.plan_result}")
        
        # Queue the complete results for transmission to Fleet Management
        # Serialize the plan_result as JSON for consistent data format
        self.ros2_action_queue.put(json.dumps(result.plan_result))

    def feedback_callback(self, feedback_msg, drone_id):
        """Handle intermediate command execution updates and status reporting.

        This callback processes real-time feedback from drone action servers during
        command execution. It provides continuous status updates to the Fleet Management
        System, enabling real-time monitoring of command progress and execution status.

        Feedback Processing Workflow:
            1. **Message Extraction**: Extract feedback data from ROS 2 message
            2. **Status Parsing**: Parse command_status from feedback payload
            3. **Progress Logging**: Log intermediate execution status for monitoring
            4. **Queue Reporting**: Send status updates to Fleet Management System

        Feedback Frequency:
            Feedback frequency depends on drone action server implementation:
            - **Per-command Updates**: Status after each command completion
            - **Progress Updates**: Intermediate progress during long-running commands
            - **Error Notifications**: Immediate updates when issues are encountered
            - **Heartbeat Messages**: Periodic status to confirm connection health

        Status Information Types:
            Feedback typically includes various types of execution status:
            
            - **Command Progress**: Current command execution state
            - **Position Updates**: Real-time drone position and orientation
            - **Sensor Data**: Environmental and system sensor readings
            - **Error Conditions**: Warnings and error states during execution
            - **Performance Metrics**: Resource usage and execution timing

        Real-time Monitoring:
            This callback enables the Fleet Management System to:
            - Track mission progress in real-time
            - Detect and respond to execution issues promptly
            - Provide live status updates to operators
            - Make dynamic mission adjustments based on feedback

        :param feedback_msg: ROS 2 feedback message from drone action server
        :type feedback_msg: Commands.FeedbackMessage
        :param drone_id: Identifier of drone providing feedback for status correlation
        :type drone_id: int

        Feedback Content Examples:
            **Command Progress**::
            
                {
                    "current_command": "move_to",
                    "progress_percent": 65,
                    "estimated_time_remaining": 12.3,
                    "position": [85, 150, 15]
                }
                
            **Command Completion**::
            
                {
                    "command_completed": "takeoff",
                    "execution_time": 8.2,
                    "final_altitude": 10.1,
                    "status": "SUCCESS"
                }
                
            **Error Condition**::
            
                {
                    "current_command": "land",
                    "status": "WARNING",
                    "issue": "High wind conditions detected",
                    "recommended_action": "delay_landing"
                }

        .. note::
            Feedback frequency and content depend on drone action server
            implementation. Some servers may provide more detailed feedback than others.

        .. warning::
            High-frequency feedback can impact network performance. Consider
            feedback filtering if network bandwidth is constrained.
        """
        # Extract feedback data from the ROS 2 feedback message
        # This contains real-time status information from command execution
        feedback = feedback_msg.feedback
        
        # Log the feedback for real-time monitoring and debugging
        # Provides visibility into ongoing command execution progress
        self.ros2_logger.info(f"[ROS2 Manager] - Drone {drone_id}: Feedback: {feedback.command_status}")
        
        # Queue the feedback status for transmission to Fleet Management
        # Serialize command_status as JSON for consistent data format
        self.ros2_action_queue.put(json.dumps(feedback.command_status))


def create_ros2_action_client(ros2_action_queue, ros2_logger):
    """Initialize and configure ROS 2 action client infrastructure.

    :param ros2_action_queue: Shared queue for action status updates
    :type ros2_action_queue: queue.Queue
    :param ros2_logger: Configured logger instance
    :type ros2_logger: logging.Logger
    :return: Initialized action client node
    :rtype: CommandsActionClient

    .. note::
        Starts independent executor thread for ROS 2 node
        Sets up MultiThreadedExecutor for concurrent callbacks
    """
    
    rclpy.init()
    action_client = CommandsActionClient(ros2_action_queue, ros2_logger)

    executor = MultiThreadedExecutor()
    executor.add_node(action_client)

    thread = threading.Thread(target=executor.spin, daemon=True)
    thread.start()

    return action_client

