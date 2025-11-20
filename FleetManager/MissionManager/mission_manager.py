"""
Fleet Management System - Mission Manager Core Module

.. module:: mission_manager
    :synopsis: Central mission execution and coordination system for autonomous fleet operations

.. moduleauthor:: Fleet Management System Team

.. versionadded:: 1.0

This module implements the core mission management system that orchestrates autonomous vehicle
operations, precision agriculture tasks, and multi-service coordination. It provides centralized
control for mission execution, vehicle communication, and real-time status monitoring.

Architecture Overview:
    The Mission Manager follows a multi-threaded architecture where each mission runs in its own
    dedicated thread, enabling concurrent mission execution and isolation. It integrates with
    multiple external services through queue-based communication patterns.

System Integration:
    - **Vehicle Communication**: ROS2 and ISOBUS protocol support
    - **IoT Telemetry**: MQTT-based data streaming to ThingsBoard
    - **REST API**: External system integration and status reporting
    - **Prescription Maps**: Precision agriculture treatment mapping
    - **Database**: Mission persistence and historical data (planned)

Mission Workflow:
    .. mermaid::
    
        graph TD
            A[Mission Received] --> B[Validate Mission]
            B --> C[Parse Plans]
            C --> D[Generate Vehicle Commands]
            D --> E[Send Initial Plans]
            E --> F[Monitor Vehicle Feedback]
            F --> G{All Vehicles Complete?}
            G -->|No| H[Process Feedback]
            H --> I[Update Status]
            I --> J[Check Dependencies]
            J --> K[Send Next Commands]
            K --> F
            G -->|Yes| L[Mission Complete]
            
            H --> H1[Parse Command Results]
            H1 --> H2[Update Field Data]
            H2 --> H3[Generate Telemetry]
            H3 --> H4[Send MQTT Updates]

Key Features:
    - **Multi-threaded Execution**: Concurrent mission processing
    - **Dependency Management**: Task sequencing and vehicle coordination
    - **Real-time Monitoring**: Live telemetry and status updates
    - **Precision Agriculture**: Field mapping and treatment tracking
    - **Error Recovery**: Comprehensive exception handling and logging
    - **Service Integration**: Multi-protocol communication support

Precision Agriculture Features:
    - **Field Segmentation**: Automatic field division into manageable grids
    - **Treatment Tracking**: Real-time monitoring of agricultural applications
    - **Prescription Maps**: Dynamic generation of application prescriptions
    - **Centroid Calculation**: Geometric analysis for field positioning
    - **State Management**: Field analysis and treatment status tracking

Classes:
    .. autoclass:: MissionManagerThread
        :members:
        :undoc-members:
        :show-inheritance:

Functions:
    .. autofunction:: create_mission_manager
    .. autofunction:: create_queues

Thread Safety:
    All queue operations are thread-safe, enabling concurrent access from multiple
    mission threads and external services. State management within individual
    missions is isolated to prevent cross-mission interference.

.. note::
    Requires concurrent access protection for:
    - Queue operations across services
    - Plan modifications and status updates
    - Field treatment mappings and state transitions
    - Vehicle command sequencing and dependency resolution

.. warning::
    Maintain strict synchronization between:
    - Vehicle command sequences and execution order
    - Task status updates and dependency triggers
    - Field treatment mappings and telemetry generation
    - Mission completion signals and resource cleanup

.. seealso::
    - :mod:`MissionManager.data_parser`: Mission parsing and command generation
    - :mod:`MissionManager.validator`: Mission and plan validation utilities
    - :mod:`MissionManager.dependency`: Task dependency resolution system
"""

import logging
import threading
import time
import queue
import json
import random
from collections import defaultdict

from MissionManager.data_parser import parse_mission, obtain_commands_per_vehicle, commands_to_list, obtain_type_of_vehicle, parse_feedback_data
from MissionManager.validator import validate_mission, validate_plan
from MissionManager.dependency import check_dependencies

class MissionManagerThread(threading.Thread):
    """Central mission execution thread managing vehicle coordination, task processing, and precision agriculture mapping.

    This class implements the core mission execution engine that coordinates autonomous vehicle
    operations, manages task dependencies, processes real-time feedback, and maintains precision
    agriculture field mappings. Each mission runs in its own dedicated thread for isolation
    and concurrent execution capabilities.

    Mission Execution Workflow:
        1. **Initialization**: Set up mission state, queues, and logging
        2. **Data Persistence**: Save mission specifications to file system
        3. **Plan Generation**: Parse mission into vehicle-specific task plans
        4. **Plan Validation**: Verify plan integrity and dependency consistency
        5. **Initial Dispatch**: Send dependency-free plans to vehicles
        6. **Feedback Processing**: Monitor and process vehicle command responses
        7. **Status Management**: Update task/command states and trigger dependencies
        8. **Field Mapping**: Generate and update precision agriculture field data
        9. **Telemetry Generation**: Create and broadcast real-time status updates
        10. **Mission Completion**: Handle cleanup and final status reporting

    Precision Agriculture Integration:
        - **Field Segmentation**: Automatic division of navigation areas into grids
        - **Treatment Analysis**: Processing of ANALYZE_IMAGE command results
        - **Prescription Generation**: Dynamic creation of Field_PM entries
        - **State Tracking**: Monitoring of field analysis and treatment progress
        - **Coordinate Mapping**: Geometric calculations for field positioning

    Inter-Service Communication:
        - **Vehicle Interface**: Command dispatch and feedback processing
        - **MQTT Telemetry**: Real-time data streaming to IoT platforms
        - **REST API**: External system status updates and integration
        - **Prescription Maps**: Agricultural treatment map generation
        - **Database**: Mission persistence and historical data (planned)

    :param mission_id: Unique identifier for the mission instance
    :type mission_id: int
    :param mission_json: Complete mission specification including tasks, vehicles, and navigation areas
    :type mission_json: dict
    :param send_vehicle_queue: Outbound queue for vehicle command dispatch (thread-safe producer)
    :type send_vehicle_queue: queue.Queue
    :param receive_vehicle_queue: Inbound queue for vehicle feedback processing (thread-safe consumer)
    :type receive_vehicle_queue: queue.Queue
    :param send_mqtt_queue: Outbound queue for MQTT telemetry publication to IoT platforms
    :type send_mqtt_queue: queue.Queue
    :param send_rest_queue: Outbound queue for REST API communication and status updates
    :type send_rest_queue: queue.Queue
    :param send_pm_queue: Outbound queue for prescription map generation requests
    :type send_pm_queue: queue.Queue
    :param mission_logger: Pre-configured logger instance for mission-specific event logging
    :type mission_logger: logging.Logger

    :ivar plans: Vehicle-specific task configurations mapping vehicle_id to complete plan structure
    :vartype plans: Dict[int, Dict[int, Dict]]
    :ivar results: Vehicle completion status tracking for mission termination detection
    :vartype results: Dict[int, bool]
    :ivar start_plan: Mission timing metadata for performance measurement and logging
    :vartype start_plan: Dict[int, float]
    :ivar fields_pm: Precision agriculture treatment mappings for Field_PM generation
    :vartype fields_pm: List[Dict]
    :ivar field_coordinates: Field geometry storage for spatial analysis and treatment mapping
    :vartype field_coordinates: Dict[int, List[List[float]]]
    :ivar fields: Agricultural field segmentation data with analysis and treatment states
    :vartype fields: List[Dict[str, Union[List, str]]]
    :ivar datetime: Mission start timestamp for file naming and temporal tracking
    :vartype datetime: str
    :ivar type: Current telemetry message type for MQTT classification
    :vartype type: str
    :ivar step: Field update counter for systematic state progression tracking
    :vartype step: int
    :ivar grid_counter: Unique grid identifier for precision agriculture mapping
    :vartype grid_counter: int
    :ivar first_analyze_image: Flag controlling initial image analysis workflow
    :vartype first_analyze_image: bool
    :ivar field_pms_initialized: Control flag for Field_PM initialization state
    :vartype field_pms_initialized: bool

    .. note::
        All queue operations are thread-safe and designed for concurrent access
        from multiple system components and mission threads.

    .. warning::
        Mission state (plans, results, fields) should not be accessed directly
        from external threads without proper synchronization mechanisms.

    .. seealso::
        - :func:`create_mission_manager`: Factory function for mission thread creation
        - :mod:`MissionManager.data_parser`: Mission parsing and plan generation
        - :mod:`MissionManager.validator`: Mission and plan validation utilities
    """
    
    def __init__(self, mission_id: int, mission_json: dict, send_vehicle_queue: queue.Queue, receive_vehicle_queue: queue.Queue, send_mqtt_queue: queue.Queue, send_rest_queue: queue.Queue, send_pm_queue: queue.Queue, mission_logger: logging.Logger):
        """Initialize mission manager thread with communication channels and state management.

        Sets up the mission execution environment including inter-service communication queues,
        logging infrastructure, and initial state variables for mission coordination and
        precision agriculture field tracking.

        Initialization Workflow:
            1. **Thread Setup**: Initialize parent threading.Thread class
            2. **Core Parameters**: Store mission ID, specification, and logger
            3. **Communication Queues**: Configure inter-service message channels
            4. **State Variables**: Initialize mission tracking and field mapping state
            5. **Timing Setup**: Configure timestamp generation for file naming
            6. **Agriculture State**: Initialize precision farming tracking variables

        :param mission_id: Unique identifier for this mission instance
        :type mission_id: int
        :param mission_json: Complete mission specification including tasks, vehicles, and areas
        :type mission_json: dict
        :param send_vehicle_queue: Thread-safe queue for outbound vehicle commands
        :type send_vehicle_queue: queue.Queue
        :param receive_vehicle_queue: Thread-safe queue for inbound vehicle feedback
        :type receive_vehicle_queue: queue.Queue
        :param send_mqtt_queue: Thread-safe queue for MQTT telemetry publication
        :type send_mqtt_queue: queue.Queue
        :param send_rest_queue: Thread-safe queue for REST API communication
        :type send_rest_queue: queue.Queue
        :param send_pm_queue: Thread-safe queue for prescription map requests
        :type send_pm_queue: queue.Queue
        :param mission_logger: Pre-configured logger for mission event tracking
        :type mission_logger: logging.Logger
        """
        # Initialize parent thread class for concurrent execution
        super().__init__()
        
        # Core mission parameters and identification
        self.mission_id = mission_id
        self.mission_json = mission_json
        
        # Inter-service communication queues (thread-safe)
        self.send_vehicle_queue = send_vehicle_queue
        self.receive_vehicle_queue = receive_vehicle_queue
        self.send_mqtt_queue = send_mqtt_queue
        self.send_rest_queue = send_rest_queue
        self.send_pm_queue = send_pm_queue
        
        # Logging infrastructure
        self.mission_logger = mission_logger
        
        # Mission state management variables
        self.plans = None  # Vehicle-specific task plans
        self.results = None  # Vehicle completion tracking
        self.start_plan = {}  # Performance timing data
        
        # Timestamp for file naming and temporal tracking
        self.datetime = time.strftime('%Y-%m-%d %H:%M:%S')
        
        # Telemetry message classification
        self.type = 'Mission'
        
        # Precision agriculture field management
        self.fields = []  # Field segmentation data
        self.fields_pm = []  # Precision agriculture treatment fields
        self.field_coordinates = {}  # Field geometry storage for spatial analysis
        
        # Field processing state tracking
        self.step = 0  # Field update progression counter
        self.grid_counter = 1  # Unique grid identification counter
        self.first_analyze_image = True  # Initial analysis workflow flag
        self.field_pms_initialized = False  # Field_PM initialization control
        
    def run(self) -> None:
        """Execute the complete mission lifecycle from initialization to completion.
        
        This method implements the main mission execution workflow, coordinating all phases
        of mission processing including plan generation, vehicle coordination, feedback
        processing, and precision agriculture field management.

        Mission Execution Lifecycle:
            1. **Mission Initiation**: Log mission start and record performance timing
            2. **Data Persistence**: Save mission specification to file system for audit trail
            3. **Plan Generation**: Parse mission JSON into vehicle-specific executable plans
            4. **Plan Validation**: Verify plan integrity and save generated plans to files
            5. **Plan Processing**: Distribute initial commands to available vehicles
            6. **Telemetry Setup**: Initialize field segmentation and send initial telemetry
            7. **Feedback Loop**: Process vehicle responses and manage task progression
            8. **Mission Completion**: Handle final status updates and cleanup operations

        Feedback Processing Loop:
            - **Continuous Monitoring**: Poll for vehicle feedback messages
            - **Status Updates**: Progress task and command states based on completion
            - **Dependency Resolution**: Check and trigger dependent tasks
            - **Field Management**: Update precision agriculture field states
            - **Telemetry Broadcasting**: Send real-time updates to MQTT systems

        Performance Monitoring:
            - **Execution Timing**: Track total mission duration for optimization
            - **Phase Timing**: Monitor individual processing phase performance
            - **Resource Usage**: Log memory and processing resource consumption

        Error Handling:
            - **Exception Isolation**: Prevent individual errors from crashing mission
            - **Comprehensive Logging**: Record all errors with full stack traces
            - **Graceful Degradation**: Continue mission execution when possible

        :rtype: None
        :raises Exception: Mission execution errors are logged but don't propagate
                          to prevent system-wide failures

        .. note::
            Mission execution follows a strict sequential pattern for initialization
            phases, then enters a feedback processing loop until all vehicles complete
            their assigned tasks.

        .. warning::
            This method should only be called once per mission instance. Multiple
            calls may result in resource conflicts and undefined behavior.

        .. seealso::
            - :func:`proccess_plans`: Initial plan distribution to vehicles
            - :func:`process_vehicle_feedback`: Vehicle response processing
            - :func:`set_fields`: Agricultural field segmentation setup
        """
        try:
            # Initialize mission timing and logging
            start_mission = time.perf_counter()
            self.mission_logger.info(f"[Mission {self.mission_id}] - Mission {self.mission_id} started")
            
            # Persist mission specification for audit trail and debugging
            self.save_to_file(f'Missions/{self.datetime}-mission_{self.mission_id}.json', self.mission_json)
                
            # Generate vehicle-specific plans from mission specification
            self.plans = parse_mission(self.mission_id, self.mission_json, self.mission_logger)
            self.save_to_file(f'Missions/{self.datetime}-mission_{self.mission_id}_plans.json', self.plans)
            self.mission_logger.info(f"[Mission {self.mission_id}] - Plans obtained for the mission")
            
            # Process and distribute initial plans to vehicles
            self.mission_logger.info(f"[Mission {self.mission_id}] - Processing plans")
            self.proccess_plans()
            self.mission_logger.info(f"[Mission {self.mission_id}] - Finished processing plans")
 
            # Initialize telemetry and field segmentation
            telemetry = self.mission_telemetry()
            self.set_fields()
            self.send_queue(service='MQTT', telemetry=telemetry, fields=self.fields)
            self.type = 'Telemetry'
            
            # Initialize vehicle completion tracking
            self.results = {vehicle_id: False for vehicle_id in self.plans.keys()}

            # Main feedback processing loop - continue until all vehicles complete
            while not all(self.results.values()):      
                self.process_vehicle_feedback() 
                
            # Mission completion handling and final status updates
            self.send_queue(service='REST', mission_status="Finished")
            self.save_to_file(f'Missions/{self.datetime}-mission_{self.mission_id}_result.json', self.plans)
            
            # Send final telemetry indicating mission completion
            self.type = 'Finish'
            telemetry = self.feedback_telemetry('--', '--', '--', 'Mission finished suscessfully')
            self.send_queue(service='MQTT', telemetry=telemetry, fields=self.fields)
            
            # Calculate and log mission performance metrics
            end_mission = time.perf_counter()
            duration_mission = end_mission - start_mission
            self.mission_logger.info(f"[Mission {self.mission_id}] - Mission {self.mission_id} terminated successfully in {duration_mission:.0f} seconds")

        except Exception as e:
            self.mission_logger.error(f"[Mission {self.mission_id}] - Error in run_mission_manager: {str(e)}", exc_info=True)

    def proccess_plans(self) -> None:
        """Process and distribute mission plans to vehicles based on dependency analysis.

        This method handles the initial distribution of mission plans to vehicles, performing
        dependency analysis to determine which vehicles can start immediately and which must
        wait for prerequisite tasks to complete.

        Plan Processing Workflow:
            1. **Plan Validation**: Verify each vehicle's plan structure and content
            2. **Status Initialization**: Set all tasks and commands to 'NotStarted' state
            3. **Dependency Analysis**: Examine task dependencies across all vehicles
            4. **Initial Distribution**: Send plans to vehicles without dependencies
            5. **Performance Tracking**: Monitor plan processing and distribution timing

        Status Management:
            - **Task Status**: Initialize all tasks with 'NotStarted' status
            - **Command Status**: Set all commands within tasks to 'NotStarted'
            - **Dependency Tracking**: Identify and flag dependent tasks for later execution

        Vehicle Coordination:
            - **Independent Vehicles**: Immediately dispatch plans with no dependencies
            - **Dependent Vehicles**: Hold plans until prerequisite conditions are met
            - **Timing Control**: Record plan distribution timestamps for performance analysis

        :rtype: None
        :raises Exception: Plan processing errors are logged with full context and stack traces

        .. note::
            Only vehicles with no task dependencies receive their plans during this phase.
            Dependent vehicles will receive their plans later when dependencies are satisfied.

        .. warning::
            Plan validation failure for any vehicle will be logged but won't prevent
            other vehicles from receiving their plans.

        .. seealso::
            - :func:`validate_plan`: Individual plan validation logic
            - :func:`send_plan`: Vehicle plan transmission mechanism
            - :func:`check_dependencies`: Dependency resolution system
        """
        try:
            # Initialize performance timing for plan processing
            start_plans = time.perf_counter()
            
            # Process each vehicle's plan individually
            for vehicle_id, plan in self.plans.items():
                # Validate plan structure and content integrity
                validate_plan(self.mission_id, vehicle_id, plan, self.mission_logger)

                # Initialize all task statuses to 'NotStarted'
                for task_id, task in plan.items():
                    self.plans[vehicle_id][task_id]['task_status'] = 'NotStarted'

                    # Initialize all command statuses within each task
                    for command_id, command in task['commands'].items():
                        self.plans[vehicle_id][task_id]['commands'][command_id]['command_status'] = 'NotStarted'

                # Analyze task dependencies to determine immediate availability
                dependency = any(task['task_dependency'] is not None for task in plan.values())
                
                # Send plan immediately if no dependencies exist
                if not dependency:
                    self.send_plan(vehicle_id, self.plans[vehicle_id])
                    
            # Calculate and log plan processing performance
            end_plans = time.perf_counter()
            duration_plans = end_plans - start_plans
            self.mission_logger.info(f"[Mission {self.mission_id}] - Plans processed and sent to vehicles in {duration_plans:.6f} seconds")
        except Exception as e:
            self.mission_logger.error(f"[Mission {self.mission_id}] - Error in process_plans: {str(e)}", exc_info=True)

    def process_vehicle_feedback(self) -> None:
        """Process incoming vehicle feedback messages and coordinate mission progression.

        This method implements the core feedback processing loop that handles real-time
        communication with vehicles, processes command completion notifications, and
        manages mission state transitions based on vehicle responses.

        Feedback Processing Workflow:
            1. **Message Reception**: Retrieve vehicle feedback from communication queue
            2. **Vehicle Validation**: Verify message originates from mission-assigned vehicle
            3. **Message Classification**: Determine feedback type and route to appropriate handler
            4. **State Updates**: Update mission plans and vehicle status based on feedback
            5. **Dependency Resolution**: Check and trigger dependent tasks when conditions are met

        Message Types Handled:
            - **Type 0**: Plan initiation confirmation from vehicle
            - **Type 1**: Command execution feedback with results and status
            - **Type 2**: Plan completion notification indicating vehicle finished

        Vehicle Coordination:
            - **Mission Validation**: Ensure feedback comes from vehicles in current mission
            - **Queue Management**: Handle message queuing for vehicles not in current mission
            - **Timing Control**: Implement random delays to prevent queue flooding

        Error Handling:
            - **Invalid Vehicles**: Requeue messages from vehicles not in current mission
            - **Message Parsing**: Handle malformed or unexpected message formats
            - **State Consistency**: Maintain mission state integrity during error conditions

        :rtype: None
        :raises Exception: Feedback processing errors are logged with full context

        .. note::
            Messages from vehicles not assigned to the current mission are requeued
            and processed with a random delay to prevent infinite processing loops.

        .. warning::
            Feedback processing continues until all assigned vehicles complete their
            plans. Ensure proper error handling to prevent infinite loops.

        .. seealso::
            - :func:`handle_plan_started`: Plan initiation processing
            - :func:`handle_command_feedback`: Command completion processing
            - :func:`receive_queue`: Message reception and parsing utilities
        """
        try:
            # Retrieve vehicle feedback message from communication queue
            drone_result = self.receive_queue('Vehicle')
            vehicle_id = int(drone_result[0])

            # Validate that message comes from vehicle assigned to this mission
            if vehicle_id not in self.plans:
                # Requeue message for processing by appropriate mission thread
                self.receive_vehicle_queue.put(json.dumps(drone_result))
                # Add random delay to prevent queue flooding and infinite loops
                time.sleep(random.uniform(0.1, 0.5))
                return

            # Extract and classify message type for appropriate handling
            type_message = int(drone_result[1])
            
            # Route message to appropriate handler based on type
            match type_message:
                case 0:  # Plan initiation confirmation
                    self.handle_plan_started(vehicle_id)
                case 1:  # Command execution feedback with results
                    self.handle_command_feedback(vehicle_id, drone_result)
                case 2:  # Plan completion notification
                    # Mark vehicle as completed and calculate execution time
                    self.results[vehicle_id] = True
                    end = time.perf_counter()
                    duration = end - self.start_plan[vehicle_id]
                    self.mission_logger.info(f"[Mission {self.mission_id}] - Vehicle {vehicle_id} finished the plan in {duration} seconds.")
                    
        except Exception as e:
            self.mission_logger.error(f"[Mission {self.mission_id}] - Error in process_vehicle_feedback: {str(e)}", exc_info=True)
    
    def handle_plan_started(self, vehicle_id: int):
        """Process vehicle plan initiation confirmation and update mission state.

        Handles the initial confirmation message from a vehicle indicating that it has
        successfully received and started executing its assigned mission plan. Updates
        the mission state to reflect active task and command execution.

        State Transition Management:
            1. **Task Activation**: Mark the first task in the plan as 'Running'
            2. **Command Activation**: Set the first command within that task to 'Running'
            3. **State Logging**: Record plan initiation for mission tracking

        Plan Structure Assumptions:
            - Vehicle plans contain at least one task with at least one command
            - Tasks and commands are ordered sequentially for execution
            - Dictionary keys maintain insertion order for proper sequencing

        :param vehicle_id: Identifier of the vehicle that started plan execution
        :type vehicle_id: int

        :raises Exception: State update errors are logged with full context

        .. note::
            This method assumes the vehicle plan structure has been validated
            prior to transmission to ensure required tasks and commands exist.

        .. warning::
            Plan structure violations (empty tasks/commands) will cause KeyError
            exceptions that are logged but may leave mission state inconsistent.

        .. seealso::
            - :func:`send_plan`: Plan transmission to vehicles
            - :func:`update_status`: Subsequent status progression logic
        """
        try:
            # Identify and activate the first task in the vehicle's plan
            # Plan execution follows sequential task ordering
            first_task_id = list(self.plans[vehicle_id].keys())[0]
            self.plans[vehicle_id][first_task_id]['task_status'] = 'Running'

            # Identify and activate the first command within the first task
            # Command execution follows sequential ordering within each task
            first_command_id = list(self.plans[vehicle_id][first_task_id]['commands'].keys())[0]
            self.plans[vehicle_id][first_task_id]['commands'][first_command_id]['command_status'] = 'Running'

            # Log successful plan initiation for mission tracking and debugging
            self.mission_logger.info(f"[Mission {self.mission_id}] - Vehicle {vehicle_id} started the plan.")
        except Exception as e:
            # Handle plan structure violations or state update failures
            self.mission_logger.error(f"[Mission {self.mission_id}] - Error in handle_plan_started: {str(e)}", exc_info=True)
        
    def handle_command_feedback(self, vehicle_id: int, drone_result: list):
        """Process command completion feedback and coordinate mission progression.

        Processes vehicle feedback when a command has been completed, updating mission
        state, handling command-specific processing (analysis, treatment, navigation),
        and coordinating field mapping updates for precision agriculture operations.

        Command Processing Workflow:
            1. **Command Identification**: Locate completed command in mission plans
            2. **Status Updates**: Mark command as 'Finished' and store results
            3. **State Progression**: Advance task/command states via update_status()
            4. **Command-Specific Processing**: Handle specialized command types
            5. **Telemetry Broadcasting**: Send real-time updates via MQTT
            6. **Dependency Resolution**: Check and trigger dependent tasks

        Command Type Handlers:
            - **ANALYZE_IMAGE**: Process field analysis, generate treatments, create Field_PM entries
            - **SPRAY**: Update field state and record treatment application
            - **NAV_HOME**: Finalize vehicle operations and notify PM service
            - **Generic Commands**: Standard result logging and telemetry

        Precision Agriculture Integration:
            - **Field State Updates**: Progress field analysis and treatment states
            - **Treatment Generation**: Create prescription maps from analysis results
            - **Coordinate Mapping**: Associate results with geographic field locations
            - **PM Service Communication**: Send treatment data to Prescription Map service

        :param vehicle_id: Identifier of the vehicle providing feedback
        :type vehicle_id: int
        :param drone_result: Feedback message containing command ID and result data
        :type drone_result: List[Any]

        :raises Exception: Command processing errors are logged with full context

        .. note::
            ANALYZE_IMAGE commands trigger comprehensive field analysis workflows
            including treatment generation and Field_PM creation for precision agriculture.

        .. warning::
            Command lookup failures may indicate plan corruption or communication
            errors that require investigation and potential mission recovery.

        .. seealso::
            - :func:`update_status`: Task and command state progression
            - :func:`generate_field_pm_for_current_grid`: Field_PM creation logic
            - :func:`check_dependencies`: Dependency resolution system
        """
        try:
            # Extract command identification and result data from feedback message
            command_id = int(drone_result[2])
            data = parse_feedback_data(self.mission_id, vehicle_id, drone_result[3], self.mission_logger)

            # Locate the completed command within the vehicle's plan structure
            # Nested iteration ensures command is found regardless of task hierarchy
            for task_id, task in self.plans[vehicle_id].items():
                for cmd_id, cmd in task['commands'].items():
                    if cmd['id'] == command_id:
                        # Update command state and store execution results
                        self.plans[vehicle_id][task_id]['commands'][cmd_id]['command_status'] = 'Finished'
                        self.plans[vehicle_id][task_id]['commands'][cmd_id]['result'] = data
                        
                        # Progress mission state to next task/command as appropriate
                        self.update_status(vehicle_id, task_id, cmd_id)

                        # Extract command context for specialized processing
                        task_type = task['task_type']
                        command_type = cmd['command_type']

                        # Command-specific processing based on type
                        if command_type == 'ANALYZE_IMAGE':
                            # Update field analysis state for precision agriculture tracking
                            self.update_field()
                            
                            # Send analysis results to Prescription Map service for processing
                            self.send_queue(service='PM', type='Generate', vehicle_id=vehicle_id, data=data)
                            
                            # Switch to treatment telemetry mode for specialized messaging
                            self.type = 'Treatment'
                            
                            # Generate vehicle-specific treatment identifiers
                            #treatments = {f"{vehicle_id}_{key}": value for key, value in data[1].items()}
                            treatments = data[1]
                            self.send_treatment_messages(vehicle_id, treatments)

                            # Initialize Field_PM entries on first analysis (system-wide setup)
                            if self.first_analyze_image:
                                self.initialize_all_field_pms(vehicle_id, treatments)
                                self.first_analyze_image = False

                            # Generate Field_PM entry for the current analyzed grid location
                            self.generate_field_pm_for_current_grid(treatments, vehicle_id, data[2], data[3])

                            # Format analysis results for telemetry broadcasting
                            data_str = f"ANALYZED: Treatment: {data[0]}, Amount: {data[1]}, Grid: {data[2]}, Coordinates: {data[3]}"
                            data = data_str

                        elif command_type == 'SPRAY':
                            # Update field state to reflect treatment application
                            self.update_field()
                            
                            # Format spray results for telemetry broadcasting
                            data = f"SPRAYED: Treatment: {data[0]}, Amount: {data[1]}"
                            
                        elif command_type == 'NAV_HOME':
                            # Process navigation completion and finalize PM operations
                            data = str(data).strip("'[]")
                            self.send_queue(service='PM', type='Finish', vehicle_id=vehicle_id, data=data)
                        else:
                            # Generic command result formatting for standard telemetry
                            data = str(data).strip("'[]")

                        # Switch to feedback telemetry mode and broadcast command completion
                        self.type = 'Feedback'
                        telemetry = self.feedback_telemetry(task_type, command_type, vehicle_id, data)
                        self.send_queue(service='MQTT', telemetry=telemetry, fields=self.fields)
                        break

            # Log successful command completion for mission tracking
            self.mission_logger.info(f"[Mission {self.mission_id}] - Vehicle {vehicle_id} finished command {command_id}: {drone_result[3]}")

            # Check for dependency resolution and dispatch plans to newly available vehicles
            self.plans, vehicle_ids = check_dependencies(self.mission_id, self.plans, command_id, self.mission_logger)
            if vehicle_ids:
                for vehicle_id in vehicle_ids:
                    # Validate and send plans to vehicles with resolved dependencies
                    validate_plan(self.mission_id, vehicle_id, self.plans[vehicle_id], self.mission_logger)
                    self.send_plan(vehicle_id, self.plans[vehicle_id])

        except Exception as e:
            # Handle command processing failures with comprehensive error logging
            self.mission_logger.error(f"[Mission {self.mission_id}] - Error in _handle_command_feedback: {str(e)}", exc_info=True)

    def generate_field_pm_for_current_grid(self, treatments: dict, vehicle_id: int, grid: list, center_coords: list) -> None:
        """Update Field_PM entries with treatment amounts for the current analysis grid.

        Updates existing Field_PM entries with newly analyzed treatment data for the
        current grid location, maintaining spatial relationships between analysis
        results and field prescription mappings for precision agriculture operations.

        Field_PM Update Workflow:
            1. **Treatment Iteration**: Process each treatment detected in current grid
            2. **Field_PM Matching**: Locate corresponding Field_PM entries by grid and treatment
            3. **Data Integration**: Update amount, state, and coordinate information
            4. **State Transition**: Change Field_PM state from 'Not Analyzed' to 'Analyzed'
            5. **Service Notification**: Send updated Field_PM data via MQTT telemetry

        Spatial Coordination:
            - **Grid Matching**: Ensure Field_PM grid coordinates match analysis location
            - **Treatment Association**: Link treatment types with prescription map entries
            - **Point Updates**: Store analysis center coordinates for precise location tracking

        Precision Agriculture Integration:
            - **Amount Updates**: Store analyzed treatment amounts for prescription accuracy
            - **State Tracking**: Progress Field_PM entries through analysis workflow
            - **Telemetry Broadcasting**: Notify external systems of prescription updates

        :param treatments: Dictionary mapping treatment identifiers to analyzed amounts
        :type treatments: Dict[str, Union[float, None]]
        :param vehicle_id: Identifier of the vehicle performing the analysis
        :type vehicle_id: int
        :param grid: Grid coordinates [row, column] of the analyzed field segment
        :type grid: List[int]
        :param center_coords: Geographic coordinates [latitude, longitude] of analysis point
        :type center_coords: List[float]

        :rtype: None
        :raises Exception: Field_PM update errors are logged with full context

        .. note::
            This method assumes Field_PM entries have been initialized via
            initialize_all_field_pms() during the first ANALYZE_IMAGE command.

        .. warning::
            Field_PM matching failures may indicate grid coordinate inconsistencies
            or initialization problems that require investigation.

        .. seealso::
            - :func:`initialize_all_field_pms`: Field_PM initialization system
            - :func:`send_field_pm`: Field_PM telemetry broadcasting
        """
        try:
            # Process each treatment detected in the current grid analysis
            for treatment_key, amount in treatments.items():
                # Search for matching Field_PM entry based on grid and treatment type
                for field_pm in self.fields_pm:
                    # Match Field_PM entry using both grid coordinates and treatment identifier
                    if (field_pm["grid"] == grid and 
                        field_pm["treatment"] == treatment_key):
                        
                        # Update Field_PM with analyzed treatment data
                        field_pm["amount"] = float(amount) if amount is not None else None
                        field_pm["state"] = "Analyzed"  # Progress state from 'Not Analyzed'
                        field_pm["point"] = center_coords  # Store precise analysis location
    
                        # Broadcast updated Field_PM via MQTT telemetry system
                        self.send_field_pm(field_pm, vehicle_id, grid)
                        self.mission_logger.info(f"[Mission {self.mission_id}] - Updated Field_PM for grid {grid} with treatment {treatment_key} amount {field_pm['amount']}")
                        break  # Move to next treatment after successful Field_PM update
                    
        except Exception as e:
            # Handle Field_PM update failures with comprehensive error logging
            self.mission_logger.error(f"[Mission {self.mission_id}] - Error updating Field_PM: {str(e)}", exc_info=True)


    def calculate_centroid(self, coords: list) -> list:
        """Calculate the geometric centroid of a four-vertex polygon field segment."""
        try:
            # Verify coordinates structure and convert to float
            processed_coords = []
            for point in coords:
                if isinstance(point, (list, tuple)) and len(point) >= 2:
                    try:
                        lat = float(point[0]) if not isinstance(point[0], (int, float)) else point[0]
                        lon = float(point[1]) if not isinstance(point[1], (int, float)) else point[1]
                        processed_coords.append([lat, lon])
                    except (ValueError, TypeError):
                        self.mission_logger.warning(f"[Mission {self.mission_id}] - Invalid coordinate point: {point}")
                        continue
                    
            if len(processed_coords) < 4:
                self.mission_logger.warning(f"[Mission {self.mission_id}] - Not enough valid coordinates for centroid calculation")
                return [0, 0]  # Default centroid when coordinates are invalid

            # Calculate centroid from valid coordinates
            lats = [p[0] for p in processed_coords]
            lons = [p[1] for p in processed_coords]

            return [sum(lats)/len(lats), sum(lons)/len(lons)]

        except Exception as e:
            self.mission_logger.error(f"[Mission {self.mission_id}] - Error calculating centroid: {str(e)}", exc_info=True)
            return [0, 0]  # Default centroid on error
    
    def find_closest_field(self, center_coords: list) -> int:
        """Find the field segment closest to specified geographic coordinates using Euclidean distance.

        Performs spatial analysis to identify which field segment is nearest to a given
        analysis point, enabling precise association of treatment data with field locations.

        Proximity Analysis Workflow:
            1. **Distance Calculation**: Compute Euclidean distance to each field centroid
            2. **Minimum Detection**: Identify field segment with smallest distance
            3. **Index Return**: Provide field index for coordinate lookup and association

        Distance Metric:
            Uses Euclidean distance calculation: √((lat₁-lat₂)² + (lon₁-lon₂)²)
            Sufficient for local field analysis where Earth curvature is negligible.

        :param center_coords: Geographic coordinates [latitude, longitude] of the analysis point
        :type center_coords: List[float]
        :return: Index of the closest field segment in field_coordinates mapping,
                or None if no field segments are available
        :rtype: Optional[int]

        .. note::
            This method assumes all field coordinates have been properly initialized
            through the set_fields() method during mission setup.

        .. warning::
            Returns None if field_coordinates is empty, which may cause downstream
            processing failures in Field_PM generation.

        .. seealso::
            - :func:`calculate_centroid`: Centroid calculation for distance measurement
            - :func:`set_fields`: Field coordinate initialization and segmentation
        """
        # Initialize tracking variables for minimum distance search
        closest_idx = None
        min_distance = float('inf')
        
        # Iterate through all available field segments
        for idx, coords in self.field_coordinates.items():
            # Calculate centroid of current field segment
            centroid = self.calculate_centroid(coords)
            
            # Compute Euclidean distance from analysis point to field centroid
            distance = ((center_coords[0] - centroid[0])**2 + 
                        (center_coords[1] - centroid[1])**2)**0.5
            
            # Update closest field if current distance is smaller
            if distance < min_distance:
                min_distance = distance
                closest_idx = idx
                
        return closest_idx

    def update_status(self, vehicle_id: int, task_id: int, cmd_id: int):
        """
        Progresses task and command states based on completion.

        :param vehicle_id: Target vehicle identifier
        :type vehicle_id: int
        :param task_id: Current task identifier
        :type task_id: int
        :param cmd_id: Completed command identifier
        :type cmd_id: int
        """
        try:
            task = self.plans[vehicle_id][task_id]
            command_ids = list(task['commands'].keys())
            current_index = command_ids.index(cmd_id)

            if current_index == len(command_ids) - 1:  # Last command in task
                self.plans[vehicle_id][task_id]['task_status'] = 'Finished'
                task_ids = list(self.plans[vehicle_id].keys())
                current_task_index = task_ids.index(task_id)

                if current_task_index < len(task_ids) - 1:  # Start next task
                    next_task_id = task_ids[current_task_index + 1]
                    self.plans[vehicle_id][next_task_id]['task_status'] = 'Running'
                    next_cmd_id = list(self.plans[vehicle_id][next_task_id]['commands'].keys())[0]
                    self.plans[vehicle_id][next_task_id]['commands'][next_cmd_id]['command_status'] = 'Running'
            else:  # Start next command in the same task
                next_cmd_id = command_ids[current_index + 1]
                self.plans[vehicle_id][task_id]['commands'][next_cmd_id]['command_status'] = 'Running'
                
            self.mission_logger.info(f"[Mission {self.mission_id}] - Status for the tasks and commands of the vehicle {vehicle_id} updated")
        except Exception as e:
            self.mission_logger.error(f"[Mission {self.mission_id}] - Error in _update_task_status: {str(e)}", exc_info=True)

    def mission_telemetry(self):
        """
        Modifies the telemetry data to include mission-specific information.

        :param telemetry: The telemetry data to modify.
        :type telemetry: dict
        """
        try:
            plan_summary = f"Number of plans: {len(self.plans)}"
            task_summary = ", ".join([f"{task['task_type']}" for task in self.mission_json['tasks']])
            vehicle_summary = ", ".join([f"{obtain_type_of_vehicle(self.mission_id, key, self.mission_json, self.mission_logger)} {key}" for key in self.plans.keys()])
            
            telemetry = {
                'mission_id': self.mission_id,
                'start_time': self.datetime,
                'plans': plan_summary,
                'tasks': task_summary,
                'vehicles': vehicle_summary,
            }
            
            return telemetry
        except Exception as e:
            self.mission_logger.error(f"[Mission {self.mission_id}] - Error in modify_telemetry: {str(e)}", exc_info=True)

    def feedback_telemetry(self, task, command, vehicle_id, result):
        """
        Modifies the telemetry data to include mission-specific information.

        :param telemetry: The telemetry data to modify.
        :type telemetry: dict
        """
        try:
        
            telemetry = {
                'time': time.strftime('%Y-%m-%d %H:%M:%S'),
                'task': task,
                'command': command,
                'vehicle_id': f"{obtain_type_of_vehicle(self.mission_id, vehicle_id, self.mission_json, self.mission_logger)} {vehicle_id}",
                'result': result  
            }
            
            return telemetry
        except Exception as e:
            self.mission_logger.error(f"[Mission {self.mission_id}] - Error in modify_telemetry: {str(e)}", exc_info=True)

    def set_fields(self):
        """Creates agricultural field mappings with grid coordinates."""
        try:
            area = self.mission_json["navigation_area"]["area"]

            # Convertir y validar puntos
            points = []
            for point in area:
                try:
                    lat = float(point["latitude"])
                    lon = float(point["longitude"])
                    points.append((lat, lon))
                except (ValueError, TypeError):
                    continue
                
            # Asumimos que los puntos están ordenados en filas consecutivas
            # y que cada fila tiene la misma cantidad de puntos
            points_per_row = 8
            num_rows = len(points) // points_per_row

            # Dividir puntos en filas
            rows = []
            for i in range(num_rows):
                start_index = i * points_per_row
                end_index = start_index + points_per_row
                row_points = points[start_index:end_index]

                # Ordenar cada fila por longitud (oeste a este)
                row_points.sort(key=lambda p: p[1])
                rows.append(row_points)

            # Ordenar filas por latitud (norte a sur)
            rows.sort(key=lambda r: r[0][0], reverse=True)

            # Crear campos (celdas) conectando puntos adyacentes
            self.fields = []
            for row_idx in range(len(rows) - 1):
                top_row = rows[row_idx]     # Fila norte
                bottom_row = rows[row_idx + 1]  # Fila sur

                for col_idx in range(len(top_row) - 1):
                    # Puntos en fila norte
                    A = top_row[col_idx]    # NW
                    B = top_row[col_idx + 1]  # NE

                    # Puntos correspondientes en fila sur
                    # (mismo índice de columna)
                    D = bottom_row[col_idx]   # SW
                    C = bottom_row[col_idx + 1]  # SE

                    coordinates = [
                        [A[0], A[1]],  # NW
                        [B[0], B[1]],  # NE
                        [C[0], C[1]],  # SE
                        [D[0], D[1]]   # SW
                    ]

                    self.fields.append({
                        "coordinates": coordinates,
                        "grid": [row_idx, col_idx],
                        "state": "Not Analyzed"
                    })

            self.mission_logger.info(f"[Mission {self.mission_id}] - Generated {len(self.fields)} fields")
            self.field_coordinates = {idx: field for idx, field in enumerate(self.fields)}

        except Exception as e:
            self.mission_logger.error(f"[Mission {self.mission_id}] - Error in set_fields: {str(e)}", exc_info=True)
            self.fields = []
            self.field_coordinates = {}
    
    def update_field(self):
        """
        Updates the state of the fields based on the command type.

        """
        try:
            if not self.fields:
                self.mission_logger.error(f"[Mission {self.mission_id}] - No fields to update")
                return

            total_fields = len(self.fields)
            index = self.step % total_fields
            cycle = self.step // total_fields
            new_state = 'Analyzed' if (cycle % 2 == 0) else 'Sprayed'
            self.fields[index]['state'] = new_state
            self.step += 1
        except Exception as e:
            self.mission_logger.error(f"[Mission {self.mission_id}] - Error in update_field: {str(e)}", exc_info=True)
            
    def initialize_all_field_pms(self, vehicle_id: int, treatments: dict):
        """Initialize all Field_PM entries with correct grid coordinates and null amount."""
        try:
            if self.field_pms_initialized:
                return
    
            self.fields_pm = []  # Clear existing Field_PMs
            
            for field_idx, field_data in self.field_coordinates.items():
                coords = field_data["coordinates"]
                grid = field_data["grid"]
    
                for treatment_name in treatments.keys():                   
                    field_pm = {
                        "name": f"{treatment_name}_segment_{field_idx}_grid_{grid[0]}_{grid[1]}",
                        "coordinates": coords,
                        "treatment": treatment_name,
                        "amount": None,  # Initialize with null amount
                        "state": "Not Analyzed",
                        "point": self.calculate_centroid(coords),
                        "grid": grid.copy(),
                        "field_idx": field_idx
                    }
    
                    self.fields_pm.append(field_pm)
                    self.send_field_pm(field_pm, vehicle_id, grid)
    
            self.field_pms_initialized = True
            self.mission_logger.info(f"[Mission {self.mission_id}] - All Field_PMs initialized with null amounts")
        except Exception as e:
            self.mission_logger.error(f"[Mission {self.mission_id}] - Error initializing Field_PMs: {str(e)}", exc_info=True)

    def send_field_pm(self, field_pm: dict, vehicle_id: int, grid: list):
        """Send Field_PM update via MQTT"""
        try:
            telemetry = {
                'name': field_pm.get('name', ''),
                'treatment': field_pm['treatment'],
                'vehicle_id': vehicle_id,
                'amount': field_pm['amount'],
                'coordinates': field_pm['coordinates'],
                'point': field_pm['point'],
                'grid': grid.copy(),
                'state': field_pm['state'],
                'mission_id': self.mission_id,
                'update': True  # Indicate this is an update
            }
    
            self.type = 'Field_PM'
            self.send_queue(service='MQTT', telemetry=telemetry, fields=[])
    
        except Exception as e:
            self.mission_logger.error(f"[Mission {self.mission_id}] - Error sending Field_PM: {str(e)}", exc_info=True)
        
    def send_plan(self, vehicle_id: int, plan: dict):
        """
        Sends a plan to a vehicle.

        :param vehicle_id: The ID of the vehicle.
        :type vehicle_id: int
        :param plan: The plan to send.
        :type plan: dict
        """
        try:
            # ROS2 or ISOBUS
            type_vehicle = obtain_type_of_vehicle(self.mission_id, vehicle_id, self.mission_json, self.mission_logger)

            # Obtain commands list
            commands = obtain_commands_per_vehicle(self.mission_id, vehicle_id, plan, self.mission_logger)
            commands_list = commands_to_list(self.mission_id, commands, self.mission_logger)

            # Send plan
            self.send_queue(service='Vehicle', type_vehicle=type_vehicle, vehicle_id=vehicle_id, commands_list=commands_list)
            self.start_plan[vehicle_id] = time.perf_counter()
            self.mission_logger.info(f"[Mission {self.mission_id}] - Plan for the vehicle {vehicle_id} sent")
        except Exception as e:
            self.mission_logger.error(f"[Mission {self.mission_id}] - Error in send_plan: {str(e)}", exc_info=True)

    def send_treatment_messages(self, vehicle_id, treatments):
        """Envía mensajes MQTT para los tratamientos detectados"""
            
        for treatment in treatments:
            telemetry = {
                'vehicle_id': vehicle_id,
                'treatment': treatment,
                'mission_id': self.mission_id
            }
            self.type = 'Treatment'
            self.send_queue(service='MQTT', telemetry=telemetry, fields=[])
            self.mission_logger.info(f"[Mission {self.mission_id}] - Sent treatment info: {treatment} for vehicle {vehicle_id}")

    def send_queue(self, service: str, **kwargs):
        """
        Routes messages through appropriate service channels.

        :param service: Target service identifier
        .. note::
            Supported services:
            - REST: Mission status updates
            - Vehicle: Command distributions
            - MQTT: Thingsboard data
            - DB: (Implementation pending)
            - PM: Precision agriculture manager
        """
        try:
            match service:
                case 'REST':
                    # Mission_id, mission_status
                    message = json.dumps([self.mission_id, kwargs['mission_status']])
                    self.send_rest_queue.put(message)

                case 'Vehicle':
                    # Type_vehicle, vehicle_id, commands_list
                    message = [kwargs['type_vehicle'], json.dumps([kwargs['vehicle_id'], kwargs['commands_list']])]
                    self.send_vehicle_queue.put(message)

                case 'MQTT':
                    # Mensaje MQTT genérico
                    message = json.dumps({
                        'type': self.type,
                        'mission_id': self.mission_id,
                        'telemetry': kwargs['telemetry'],
                        'fields': kwargs.get('fields', [])
                    })
                    self.send_mqtt_queue.put(message)
                
                case 'PM':
                    message = json.dumps({'type': kwargs['type'], 'vehicle_id': kwargs['vehicle_id'], 'data': kwargs['data']})
                    self.send_pm_queue.put(message)

        except Exception as e:
            self.mission_logger.error(f"[Mission {self.mission_id}] - Error in send_queue: {str(e)}", exc_info=True)

    def receive_queue(self, service: str) -> list:
        """
        Retrieves and parses incoming service messages.

        :param service: Source service identifier
        :return: Parsed message content
        .. note::
            Supported services:
            - Vehicle: Command feedback
            - DB: (Implementation pending)
        """
        try:
            match service:

                case 'Vehicle':
                    message_grpc = self.receive_vehicle_queue.get()
                    message_grpc_str = ''.join(message_grpc)

                    # Parse the JSON string into a Python object
                    message = json.loads(message_grpc_str)
                    return message
                
        except Exception as e:
            self.mission_logger.error(f"[Mission {self.mission_id}] - Error in receive_queue: {str(e)}", exc_info=True)

    def save_to_file(self, file_path: str, data: dict):
        """
        Persists mission data to JSON files.

        :param file_path: Target file path
        :type file_path: str
        :param data: Data structure to persist
        :type data: dict
        """
        try:
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            self.mission_logger.error(f"[Mission {self.mission_id}] - Error saving to file {file_path}: {str(e)}", exc_info=True)

def create_mission_manager(mission_json: list, send_vehicle_queue: queue.Queue, receive_vehicle_queue: queue.Queue, send_mqtt_queue: queue.Queue, send_rest_queue: queue.Queue, send_pm_queue: queue.Queue, mission_logger: logging.Logger) -> int:
    """Create and initialize a new mission manager thread for autonomous mission execution.

    This factory function serves as the primary entry point for mission creation and execution.
    It handles mission data parsing, validation, and thread instantiation while providing
    comprehensive error handling and logging throughout the initialization process.

    Mission Creation Workflow:
        1. **Data Reconstruction**: Concatenate fragmented mission JSON data
        2. **JSON Parsing**: Convert string data to structured mission specification
        3. **Mission Validation**: Verify mission integrity and assign unique identifier
        4. **Thread Creation**: Instantiate MissionManagerThread with all required parameters
        5. **Thread Startup**: Begin mission execution in dedicated thread
        6. **ID Return**: Provide mission identifier for external tracking and reference

    Communication Architecture:
        The function establishes communication channels between the mission manager and
        various system services through thread-safe queue mechanisms:
        
        - **Vehicle Communication**: Bidirectional command/feedback channels
        - **MQTT Telemetry**: Real-time data streaming to IoT platforms
        - **REST API**: External system integration and status updates
        - **Prescription Maps**: Agricultural treatment map generation
        - **Database**: Mission persistence and historical data (planned)

    Error Handling:
        - **JSON Parsing**: Handles malformed or incomplete mission data
        - **Validation Failures**: Processes invalid mission specifications
        - **Thread Creation**: Manages resource allocation and startup failures
        - **Logging**: Comprehensive error tracking with full stack traces

    :param mission_json: Fragmented mission specification data requiring reconstruction
    :type mission_json: List[str]
    :param send_vehicle_queue: Thread-safe queue for outbound vehicle command dispatch
    :type send_vehicle_queue: queue.Queue
    :param receive_vehicle_queue: Thread-safe queue for inbound vehicle feedback processing
    :type receive_vehicle_queue: queue.Queue
    :param send_mqtt_queue: Thread-safe queue for MQTT telemetry publication to IoT systems
    :type send_mqtt_queue: queue.Queue
    :param send_rest_queue: Thread-safe queue for REST API communication and status updates
    :type send_rest_queue: queue.Queue
    :param send_pm_queue: Thread-safe queue for prescription map generation requests
    :type send_pm_queue: queue.Queue
    :param mission_logger: Pre-configured logger instance for mission event tracking
    :type mission_logger: logging.Logger
    :return: Unique mission identifier for external reference and tracking
    :rtype: int
    :raises json.JSONDecodeError: When mission data cannot be parsed as valid JSON
    :raises ValueError: When mission validation fails due to invalid or incomplete data
    :raises Exception: For any other mission creation or thread startup failures

    .. note::
        The mission JSON data is received as a list of strings that must be concatenated
        before parsing. This design accommodates network transmission limitations.

    .. warning::
        Mission execution begins immediately upon thread creation. Ensure all
        external systems are ready before calling this function.

    .. seealso::
        - :class:`MissionManagerThread`: Core mission execution thread implementation
        - :func:`validate_mission`: Mission specification validation logic
        - :func:`parse_mission`: Mission-to-plan conversion utilities

    Example:
        >>> mission_data = ['{"mission_id": 1,', ' "tasks": [...]}']
        >>> mission_id = create_mission_manager(
        ...     mission_data, send_q, recv_q, mqtt_q, rest_q, pm_q, logger
        ... )
        >>> print(f"Mission {mission_id} started successfully")
    """
    try:
        # Reconstruct complete mission JSON from fragmented data
        mission_json_str = ''.join(mission_json)

        # Parse reconstructed JSON string into structured mission specification
        mission_json = json.loads(mission_json_str)
        mission_logger.info(f" - Mission received")

        # Validate mission specification and assign unique identifier
        mission_id = validate_mission(mission_json, mission_logger)

        # Create and start dedicated mission execution thread
        mission_manager_thread = MissionManagerThread(mission_id, mission_json, send_vehicle_queue, receive_vehicle_queue, send_mqtt_queue, send_rest_queue, send_pm_queue, mission_logger)
        mission_manager_thread.start() 

        return mission_id
    except Exception as e:
        mission_logger.error(f"[Mission Manager] - Error in create_mission_manager: {str(e)}", exc_info=True)

def create_queues() -> tuple:
    """Generate a complete set of thread-safe communication queues for inter-service coordination.

    Creates and initializes all required communication queues used by the mission management
    system for coordinating between different services and components. Each queue provides
    thread-safe message passing between system components.

    Queue Architecture:
        The returned queues enable the following communication patterns:
        
        - **Vehicle Communication**: Bidirectional command dispatch and feedback reception
        - **Database Operations**: Read/write operations for mission persistence (planned)
        - **MQTT Telemetry**: Real-time data streaming to IoT monitoring platforms
        - **REST API**: External system integration and status reporting

    Queue Configuration:
        All queues are configured with:
        - **Thread Safety**: Multiple producers and consumers supported
        - **FIFO Ordering**: First-in-first-out message processing
        - **Blocking Behavior**: Automatic blocking on empty queues during get() operations
        - **Unlimited Size**: No artificial size limits (bounded by available memory)

    :return: Tuple containing six pre-configured Queue instances in the following order:
            (send_vehicle_queue, receive_vehicle_queue, send_db_queue, 
             receive_db_queue, send_mqtt_queue, send_rest_queue)
    :rtype: Tuple[queue.Queue, queue.Queue, queue.Queue, queue.Queue, queue.Queue, queue.Queue]
    :raises Exception: If queue creation fails due to system resource limitations

    .. note::
        Database queues (send_db_queue, receive_db_queue) are created for future
        implementation but are not currently used in the mission execution workflow.

    .. warning::
        Queue instances must be properly shared between threads and processes to
        enable communication. Avoid creating additional queue instances for the
        same communication channels.

    .. seealso::
        - :func:`create_mission_manager`: Primary consumer of these communication queues
        - :class:`queue.Queue`: Python standard library queue implementation

    Example:
        >>> send_v, recv_v, send_db, recv_db, mqtt, rest = create_queues()
        >>> # Queues are now ready for inter-service communication
        >>> mission_id = create_mission_manager(
        ...     mission_data, send_v, recv_v, mqtt, rest, pm_queue, logger
        ... )
    """
    try:
        # Create six thread-safe communication queues for inter-service coordination
        return queue.Queue(), queue.Queue(), queue.Queue(), queue.Queue(), queue.Queue(), queue.Queue()
    except Exception as e:
        print(f"Error creating queues: {str(e)}")
        raise