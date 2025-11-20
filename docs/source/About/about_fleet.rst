About the Fleet Manager
=======================

The Fleet Manager is the core component of the system developed for managing and executing autonomous UAV missions in precision agriculture. It acts as the brain of the architecture, coordinating the flow of mission data, communication between drones, and interaction with cloud-based services. This software module is responsible for interpreting mission plans, resolving task dependencies, dispatching commands to drones via ROS2, and collecting operational feedback.

Internally, the Fleet Manager is composed of several microservices each handling a distinct part of the workflow. It is designed to work with JSON-based mission inputs from the AFarCloud server and provides real-time updates to a ThingsBoard dashboard for visualization.

For more information about the Fleet Manager, please refer to the following page: https://estelamb.github.io/PFG_Telematica/
