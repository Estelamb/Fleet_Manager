"""
This module implements the central mission management system featuring:
- Multi-threaded mission execution
- Vehicle communication coordination
- Plan processing and validation
- Feedback handling and status updates
- Cross-service integration (REST, MQTT, Database)

Classes
-------
MissionManagerThread
    Core mission execution thread
CommandsActionServer
    ROS 2 action server implementation (external)

Functions
---------
create_mission_manager
    Mission thread factory function
create_logger
    Concurrent-safe logging configuration
create_queues
    Inter-service communication setup

.. note::
    Requires concurrent access protection for:
    - Queue operations
    - Plan modifications
    - Status updates

.. warning::
    Maintain strict synchronization between:
    - Vehicle command sequences
    - Task status updates
    - Dependency resolutions
"""

import threading
import time
import queue
import json
import random
import logging
from concurrent_log_handler import ConcurrentRotatingFileHandler

from MissionManager.data_parser import parse_mission, obtain_commands_per_vehicle, commands_to_list, obtain_type_of_vehicle, parse_feedback_data
from MissionManager.validator import validate_mission, validate_plan
from MissionManager.dependency import check_dependencies

class MissionManagerThread(threading.Thread):
    """Central mission execution thread managing vehicle coordination and task processing.

    :param mission_id: Unique mission identifier
    :type mission_id: int
    :param mission_json: Complete mission specification
    :type mission_json: dict
    :param send_vehicle_queue: Outbound vehicle command queue (producer)
    :type send_vehicle_queue: queue.Queue
    :param receive_vehicle_queue: Inbound vehicle feedback queue (consumer)
    :type receive_vehicle_queue: queue.Queue
    :param send_db_queue: Database write queue (unimplemented)
    :type send_db_queue: queue.Queue
    :param receive_db_queue: Database read queue (unimplemented)
    :type receive_db_queue: queue.Queue
    :param send_mqtt_queue: MQTT telemetry publication queue
    :type send_mqtt_queue: queue.Queue
    :param send_rest_queue: REST API communication queue
    :type send_rest_queue: queue.Queue
    :param mission_logger: Configured mission logger instance
    :type mission_logger: logging.Logger

    :ivar plans: Current vehicle task configurations (vehicle_id → plan)
    :vartype plans: dict
    :ivar results: Vehicle completion status tracking (vehicle_id → bool)
    :vartype results: dict
    :ivar start_plan: Mission timing metadata (vehicle_id → timestamp)
    :vartype start_plan: dict
    """
    
    def __init__(self, mission_id, mission_json, send_vehicle_queue, receive_vehicle_queue, send_db_queue, receive_db_queue, send_mqtt_queue, send_rest_queue, mission_logger):
        super().__init__()
        self.mission_id = mission_id
        self.mission_json = mission_json
        self.send_vehicle_queue = send_vehicle_queue
        self.receive_vehicle_queue = receive_vehicle_queue
        self.send_db_queue = send_db_queue
        self.receive_db_queue = receive_db_queue
        self.send_mqtt_queue = send_mqtt_queue
        self.send_rest_queue = send_rest_queue
        self.mission_logger = mission_logger
        self.plans = None
        self.results = None
        self.start_plan = {}
        self.datetime = time.strftime('%Y-%m-%d %H:%M:%S')
        self.type = 'Mission'
        self.fields = []
        self.step = 0
        
    def run(self):
        """
        Executes the mission by managing plans, processing feedback, and communicating with vehicles.
        
        .. note::
            Lifecycle phases:
            1. Mission data persistence
            2. Plan generation & validation
            3. Vehicle command distribution
            4. Feedback processing loop
            5. Mission termination & cleanup
        """
        try:
            start_mission = time.perf_counter()
            self.mission_logger.info(f"[Mission {self.mission_id}] - Mission {self.mission_id} started")
            
            # Save the received mission into a file
            self.save_to_file(f'Missions/{self.datetime}-mission_{self.mission_id}.json', self.mission_json)
                
            # Obtain the plans for the mission and save them into a file
            self.plans = parse_mission(self.mission_id, self.mission_json, self.mission_logger)
            self.save_to_file(f'Missions/{self.datetime}-mission_{self.mission_id}_plans.json', self.plans)
            self.mission_logger.info(f"[Mission {self.mission_id}] - Plans obtained for the mission")
            
            self.mission_logger.info(f"[Mission {self.mission_id}] - Processing plans")
            self.proccess_plans()
            self.mission_logger.info(f"[Mission {self.mission_id}] - Finished processing plans")
            
            telemetry = self.mission_telemetry()
            self.set_fields()
            self.send_queue(service='MQTT', telemetry=telemetry, fields=self.fields)
            self.type = 'Telemetry'
            
            self.results = {vehicle_id: False for vehicle_id in self.plans.keys()}

            while not all(self.results.values()):      
                self.process_vehicle_feedback() 
                
            self.send_queue(service='REST', mission_status="Finished")
            self.save_to_file(f'Missions/{self.datetime}-mission_{self.mission_id}_result.json', self.plans)
            
            self.type = 'Finish'
            telemetry = self.feedback_telemetry('--', '--', '--', 'Mission finished suscessfully')
            self.send_queue(service='MQTT', telemetry=telemetry, fields=self.fields)
            
            end_mission = time.perf_counter()
            duration_mission = end_mission - start_mission
            self.mission_logger.info(f"[Mission {self.mission_id}] - Mission {self.mission_id} terminated successfully in {duration_mission:.0f} seconds")

        except Exception as e:
            self.mission_logger.error(f"[Mission {self.mission_id}] - Error in run_mission_manager: {str(e)}", exc_info=True)

    def proccess_plans(self):
        """
        Processes the mission plans and sends initial commands to vehicles.

        :param plans: The mission plans.
        :type plans: dict
        :param results: A dictionary to track the completion status of vehicles.
        :type results: dict
        """
        try:
            start_plans = time.perf_counter()
            
            # Obtain commands for vehicles without dependencies and send them
            for vehicle_id, plan in self.plans.items():
                # Validate plan
                validate_plan(self.mission_id, vehicle_id, plan, self.mission_logger)

                for task_id, task in plan.items():
                    self.plans[vehicle_id][task_id]['task_status'] = 'NotStarted'

                    for command_id, command in task['commands'].items():
                        self.plans[vehicle_id][task_id]['commands'][command_id]['command_status'] = 'NotStarted'

                dependency = any(task['task_dependency'] is not None for task in plan.values())
                
                if not dependency:
                    self.send_plan(vehicle_id, self.plans[vehicle_id])
                    
            end_plans = time.perf_counter()
            duration_plans = end_plans - start_plans
            self.mission_logger.info(f"[Mission {self.mission_id}] - Plans processed and sent to vehicles in {duration_plans:.6f} seconds")
        except Exception as e:
            self.mission_logger.error(f"[Mission {self.mission_id}] - Error in process_plans: {str(e)}", exc_info=True)

    def process_vehicle_feedback(self):
        """
        Processes incoming vehicle feedback and updates mission plans.

        .. note::
            Handles message types:
            0: Plan initiation confirmation
            1: Command execution feedback
            2: Plan completion notice
        """
        try:
            drone_result = self.receive_queue('Vehicle')
            vehicle_id = int(drone_result[0])

            if vehicle_id not in self.plans:
                self.receive_vehicle_queue.put(json.dumps(drone_result))
                time.sleep(random.uniform(0.1, 0.5))
                return

            type_message = int(drone_result[1])
            
            match type_message:
                case 0:
                    self.handle_plan_started(vehicle_id)
                case 1:
                    self.handle_command_feedback(vehicle_id, drone_result)
                case 2:
                    self.results[vehicle_id] = True
                    end = time.perf_counter()
                    duration = end - self.start_plan[vehicle_id]
                    self.mission_logger.info(f"[Mission {self.mission_id}] - Vehicle {vehicle_id} finished the plan in {duration} seconds.")
                    
        except Exception as e:
            self.mission_logger.error(f"[Mission {self.mission_id}] - Error in process_vehicle_feedback: {str(e)}", exc_info=True)

    def handle_plan_started(self, vehicle_id: int):
        """
        Handles the event when a vehicle starts its plan.

        :param vehicle_id: Target vehicle identifier
        :type vehicle_id: int
        """
        try:
            first_task_id = list(self.plans[vehicle_id].keys())[0]
            self.plans[vehicle_id][first_task_id]['task_status'] = 'Running'

            first_command_id = list(self.plans[vehicle_id][first_task_id]['commands'].keys())[0]
            self.plans[vehicle_id][first_task_id]['commands'][first_command_id]['command_status'] = 'Running'

            self.mission_logger.info(f"[Mission {self.mission_id}] - Vehicle {vehicle_id} started the plan.")
        except Exception as e:
            self.mission_logger.error(f"[Mission {self.mission_id}] - Error in handle_plan_started: {str(e)}", exc_info=True)
        
    def handle_command_feedback(self, vehicle_id: int, drone_result: list):
        """
        Handles command feedback from a vehicle

        :param vehicle_id: The ID of the vehicle.
        :type vehicle_id: int
        :param drone_result: The feedback data from the vehicle.
        :type drone_result: list
        """
        try:
            command_id = int(drone_result[2])
            data = parse_feedback_data(self.mission_id, vehicle_id, drone_result[3], self.mission_logger)

            for task_id, task in self.plans[vehicle_id].items():
                for cmd_id, cmd in task['commands'].items():
                    if cmd['id'] == command_id:
                        self.plans[vehicle_id][task_id]['commands'][cmd_id]['command_status'] = 'Finished'
                        self.plans[vehicle_id][task_id]['commands'][cmd_id]['result'] = data
                        self.update_status(vehicle_id, task_id, cmd_id)
                        
                        task_type = task['task_type']
                        command_type = cmd['command_type']
                        
                        if command_type == 'ANALYZE_IMAGE':
                            self.update_field()
                            data = f"ANALYZED: Treatment: {data[0]}, Amount: {data[1]}"
                        elif command_type == 'SPRAY':
                            self.update_field()
                            data = f"SPRAYED: Treatment: {data[0]}, Amount: {data[1]}"
                        else:
                            data = str(data).strip("'[]")
                        
                        telemetry = self.feedback_telemetry(task_type, command_type, vehicle_id, data)
                        self.send_queue(service='MQTT', telemetry=telemetry, fields=self.fields)
                        break

            self.mission_logger.info(f"[Mission {self.mission_id}] - Vehicle {vehicle_id} finished command {command_id}: {drone_result[3]}")

            self.plans, vehicle_ids = check_dependencies(self.mission_id, self.plans, command_id, self.mission_logger)
            if vehicle_ids:
                for vehicle_id in vehicle_ids:
                    validate_plan(self.mission_id, vehicle_id, self.plans[vehicle_id], self.mission_logger)
                    self.send_plan(vehicle_id, self.plans[vehicle_id])
                    
        except Exception as e:
            self.mission_logger.error(f"[Mission {self.mission_id}] - Error in _handle_command_feedback: {str(e)}", exc_info=True)

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
        try:
            
            coordinates_1 = [[self.mission_json['navigation_area']['area'][0]['latitude'], self.mission_json['navigation_area']['area'][0]['longitude']], [self.mission_json['navigation_area']['area'][1]['latitude'], self.mission_json['navigation_area']['area'][1]['longitude']], [self.mission_json['navigation_area']['area'][4]['latitude'], self.mission_json['navigation_area']['area'][4]['longitude']], [self.mission_json['navigation_area']['area'][3]['latitude'], self.mission_json['navigation_area']['area'][3]['longitude']]]
            
            coordinates_2 = [[self.mission_json['navigation_area']['area'][1]['latitude'], self.mission_json['navigation_area']['area'][1]['longitude']], [self.mission_json['navigation_area']['area'][2]['latitude'], self.mission_json['navigation_area']['area'][2]['longitude']], [self.mission_json['navigation_area']['area'][5]['latitude'], self.mission_json['navigation_area']['area'][5]['longitude']], [self.mission_json['navigation_area']['area'][4]['latitude'], self.mission_json['navigation_area']['area'][4]['longitude']]]
            
            coordinates_3 = [[self.mission_json['navigation_area']['area'][4]['latitude'], self.mission_json['navigation_area']['area'][4]['longitude']], [self.mission_json['navigation_area']['area'][5]['latitude'], self.mission_json['navigation_area']['area'][5]['longitude']], [self.mission_json['navigation_area']['area'][8]['latitude'], self.mission_json['navigation_area']['area'][8]['longitude']], [self.mission_json['navigation_area']['area'][7]['latitude'], self.mission_json['navigation_area']['area'][7]['longitude']]]
            
            coordinates_4 = [[self.mission_json['navigation_area']['area'][3]['latitude'], self.mission_json['navigation_area']['area'][3]['longitude']], [self.mission_json['navigation_area']['area'][4]['latitude'], self.mission_json['navigation_area']['area'][4]['longitude']], [self.mission_json['navigation_area']['area'][7]['latitude'], self.mission_json['navigation_area']['area'][7]['longitude']], [self.mission_json['navigation_area']['area'][6]['latitude'], self.mission_json['navigation_area']['area'][6]['longitude']]]
            
            self.fields = [
                {'coordinates': coordinates_1, 'state': 'Not Analyzed'},
                {'coordinates': coordinates_2, 'state': 'Not Analyzed'},
                {'coordinates': coordinates_3, 'state': 'Not Analyzed'},
                {'coordinates': coordinates_4, 'state': 'Not Analyzed'}
            ]
            
        except Exception as e:
            self.mission_logger.error(f"[Mission {self.mission_id}] - Error in set_fields: {str(e)}", exc_info=True)
            pass
    
    def update_field(self):
        """
        Updates the state of the fields based on the command type.

        """
        try:
            total_fields = len(self.fields)
            index = self.step % total_fields  # Which field to update
            cycle = self.step // total_fields  # Determines Analyzed/Sprayed

            new_state = 'Analyzed' if (cycle % 2 == 0) else 'Sprayed'
            self.fields[index]['state'] = new_state

            self.step += 1  
        except Exception as e:
            self.mission_logger.error(f"[Mission {self.mission_id}] - Error in update_field: {str(e)}", exc_info=True)
    
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
            self.send_queue(service = 'Vehicle', type_vehicle = type_vehicle, vehicle_id = vehicle_id, commands_list = commands_list)
            self.start_plan[vehicle_id] = time.perf_counter()
            self.mission_logger.info(f"[Mission {self.mission_id}] - Plan for the vehicle {vehicle_id} sent")
        except Exception as e:
            self.mission_logger.error(f"[Mission {self.mission_id}] - Error in send_plan: {str(e)}", exc_info=True)

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

                case 'DB':
                    #message = json.dumps[] # TODO: Message
                    #self.send_db_queue.put(message)
                    pass
                case 'MQTT':
                    message = json.dumps({'type': self.type, 'mission_id': self.mission_id, 'telemetry': kwargs['telemetry'], 'fields': kwargs['fields'], 'vehicles': list(self.plans.keys())}) # TODO: Message
                    self.send_mqtt_queue.put(message)
                    pass
        
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

                case 'DB':
                    #message_grpc = self.receive_db_queue.get()
                    #message = [json.loads(message) for message in message_grpc]
                    #return message   
                    pass 
                
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

def create_mission_manager(mission_json: list, send_vehicle_queue: queue, receive_vehicle_queue: queue, send_db_queue: queue, receive_db_queue: queue, send_mqtt_queue: queue, send_rest_queue: queue, mission_logger: logging.Logger) -> int:
    """
    Creates and starts a MissionManagerThread.

    :param mission_json: The JSON data of the mission.
    :type mission_json: dict
    :param send_vehicle_queue: Queue for sending data to vehicles.
    :type send_vehicle_queue: queue
    :param receive_vehicle_queue: Queue for receiving data from vehicles.
    :type receive_vehicle_queue: queue
    :param send_db_queue: Queue for sending data to the database.
    :type send_db_queue: queue
    :param receive_db_queue: Queue for receiving data from the database.
    :type receive_db_queue: queue
    :param send_mqtt_queue: Queue for sending data via MQTT.
    :type send_mqtt_queue: queue
    :param send_rest_queue: Queue for sending data via REST.
    :type send_rest_queue: queue
    :param mission_logger: Logger for logging mission manager activities.
    :type mission_logger: logging.Logger
    :return: The ID of the created mission.
    :rtype: int
    """
    try:
        # Concatenate the letter-by-letter mission_json into a single string
        mission_json_str = ''.join(mission_json)

        # Parse the JSON string into a Python object
        mission_json = json.loads(mission_json_str)
        mission_logger.info(f" - Mission received")

        # Validate the mission
        mission_id = validate_mission(mission_json, mission_logger)

        mission_manager_thread = MissionManagerThread(mission_id, mission_json, send_vehicle_queue, receive_vehicle_queue, send_db_queue, receive_db_queue, send_mqtt_queue, send_rest_queue, mission_logger)
        mission_manager_thread.start() 

        return mission_id
    except Exception as e:
        mission_logger.error(f"[Mission Manager] - Error in create_mission_manager: {str(e)}", exc_info=True)

def create_logger(logger_name: str, log_file: str) -> logging.Logger:
    """
    Configures concurrent-safe logging infrastructure.

    :return: Configured logger instance
    """
    try:
        # Create a custom logger
        logger = logging.getLogger(logger_name)

        # Set level
        logger.setLevel(logging.INFO)

        # Create a file handler
        file_handler = ConcurrentRotatingFileHandler(log_file, maxBytes=1000000, backupCount=5)

        # Create a console handler
        console_handler = logging.StreamHandler()

        # Set formatter
        formatter = logging.Formatter('[%(asctime)s] - [%(name)s][%(levelname)s]%(message)s')

        # Attach formatter to handlers
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Attach handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger
    except Exception as e:
        print(f"Error creating logger: {str(e)}")
        raise

def create_queues() -> tuple:
    """
    Generates communication queue set.

    :return: Tuple of configured queues in order:
        (send_vehicle, receive_vehicle, send_db, receive_db, send_mqtt, send_rest)
    """
    try:
        return queue.Queue(), queue.Queue(), queue.Queue(), queue.Queue(), queue.Queue(), queue.Queue()
    except Exception as e:
        print(f"Error creating queues: {str(e)}")
        raise

if __name__ == "__main__":
    """Command-line execution entry point for testing purposes"""
    try:
        with open('mission_data.json', 'r') as f:
            mission_json = json.load(f)

        mission_logger = create_logger('Mission Manager', 'Logs/mission_manager.log')
        queues = create_queues()

        create_mission_manager(mission_json, *queues, mission_logger)
    except Exception as e:
        print(f"Critical error in main: {str(e)}")