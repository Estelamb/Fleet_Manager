import os
import sys

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Fleet Manager'
copyright = '2025, Estela Mora Barba'
author = 'Estela Mora Barba'

version = '1.0'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

sys.path.insert(0, os.path.abspath('../../FleetManager'))
sys.path.insert(0, os.path.abspath('../../FleetManager/MissionManager'))
sys.path.insert(0, os.path.abspath('../../FleetManager/REST'))
sys.path.insert(0, os.path.abspath('../../FleetManager/ROS2'))
sys.path.insert(0, os.path.abspath('../../FleetManager/ROS2/src/commands_action_interface/commands_action_interface'))
sys.path.insert(0, os.path.abspath('../../FleetManager/MQTT'))
sys.path.insert(0, os.path.abspath('../../FleetManager/MQTT/ThingsBoard'))
sys.path.insert(0, os.path.abspath('../../FleetManager/MQTT/ThingsBoard/devices'))
sys.path.insert(0, os.path.abspath('../../FleetManager/PrescriptionMap'))
sys.path.insert(0, os.path.abspath('../../FleetManager/PrescriptionMap/pm_generation/Drone'))
sys.path.insert(0, os.path.abspath('../../FleetManager/PrescriptionMap/pm_generation/ISOBUS'))
sys.path.insert(0, os.path.abspath('../../FleetManager/PrescriptionMap/src/prescription_map_pubsub/prescription_map_pubsub'))
sys.path.insert(0, os.path.abspath('../../FleetManager/SystemMetrics'))
sys.path.insert(0, os.path.abspath('../../FleetManager/SystemMetrics/src/system_metrics_pubsub/system_metrics_pubsub'))
sys.path.insert(0, os.path.abspath('../../FleetManager/Logs'))

sys.path.insert(0, os.path.abspath('../../Drone'))
sys.path.insert(0, os.path.abspath('../../Drone/Commands'))
sys.path.insert(0, os.path.abspath('../../Drone/GRPC'))
sys.path.insert(0, os.path.abspath('../../Drone/Init'))
sys.path.insert(0, os.path.abspath('../../Drone/Images'))
sys.path.insert(0, os.path.abspath('../../Drone/Images/Models/Grape_Bunch_Hailo8'))
sys.path.insert(0, os.path.abspath('../../Drone/Images/Models/Grape_Bunch_Hailo8L'))
sys.path.insert(0, os.path.abspath('../../Drone/Images/Models/Grape_Diseases_Hailo8'))
sys.path.insert(0, os.path.abspath('../../Drone/Images/Models/Grape_Diseases_Hailo8/Grape_Diseases'))
sys.path.insert(0, os.path.abspath('../../Drone/Images/Models/Grape_Diseases_Hailo8/Leaf_Detection'))
sys.path.insert(0, os.path.abspath('../../Drone/Images/Models/Grape_Diseases_Hailo8L'))
sys.path.insert(0, os.path.abspath('../../Drone/Images/Models/Grape_Diseases_Hailo8L/Grape_Diseases'))
sys.path.insert(0, os.path.abspath('../../Drone/Images/Models/Grape_Diseases_Hailo8L/Leaf_Detection'))
sys.path.insert(0, os.path.abspath('../../Drone/PrescriptionMap'))
sys.path.insert(0, os.path.abspath('../../Drone/PrescriptionMap/pm_generation/Drone'))
sys.path.insert(0, os.path.abspath('../../Drone/PrescriptionMap/pm_generation/ISOBUS'))
sys.path.insert(0, os.path.abspath('../../Drone/Sensors'))
sys.path.insert(0, os.path.abspath('../../Drone/Sensors/Cameras'))
sys.path.insert(0, os.path.abspath('../../Drone/SystemMetrics'))
sys.path.insert(0, os.path.abspath('../../Drone/ROS2'))
sys.path.insert(0, os.path.abspath('../../Drone/ROS2/GRPC'))
sys.path.insert(0, os.path.abspath('../../Drone/ROS2/src/commands_action_interface/commands_action_interface'))
sys.path.insert(0, os.path.abspath('../../Drone/ROS2/src/prescription_map_pubsub/prescription_map_pubsub'))
sys.path.insert(0, os.path.abspath('../../Drone/ROS2/src/system_metrics_pubsub/system_metrics_pubsub'))

sys.path.insert(0, os.path.abspath('../../Training/Common_py_modules'))
sys.path.insert(0, os.path.abspath('../../Training/Grape_bunch'))
sys.path.insert(0, os.path.abspath('../../Training/Grape_diseases'))
sys.path.insert(0, os.path.abspath('../../Training/Leaf_detection'))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx_copybutton',
    'sphinx.ext.autosummary',
    'sphinx_simplepdf',
    'sphinxcontrib.mermaid'
]

# Enable automatic member detection
autodoc_default_options = {
    'members': True,          # Auto-document all members
    'member-order': 'bysource', # Follow source order
    'undoc-members': True,    # Show undocumented members
    'show-inheritance': True, # Display inheritance
    'special-members': '__init__', # Document __init__ methods
}

autodoc_mock_imports = [
    'rosidl_runtime_py',
    'rclpy',
    'std_msgs',
    'grpc', 
    'rosidl_generator_py',
    'action_msgs',
    'google',
    'commands_action_interface',
    'concurrent_log_handler',
    'mariadb',
    'paho',
    'connexion',
    'six',
    'flask',
    'GRPC',
    'cv2',
    'numpy',
    'picamera2',
    'pandas',
    'PIL',
    'ultralytics',
    'tqdm'
]

# Enable automatic module discovery
autosummary_generate = True

templates_path = ['_templates']
exclude_patterns = []
suppress_warnings = ['epub.unknown_project_files']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
