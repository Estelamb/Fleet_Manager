# PFG_Electronica

# RPI5
Name: grysberry5ai16
User: estela
Password: estela

# ThingsBoard
https://srv-iot.diatel.upm.es/

User: estela.mora.barba@alumnos.upm.es
Password: fleet_manager

# Launch Cloud
cd Fleet_Manager/Cloud
python server_8090.py

Go to http://<IP RPI5>:8090

Upload missions from FleetManager/Cloud/Missions

# Launch Fleet Manager
cd Fleet_Manager/FleetManager
sudo docker compose up --build

# Launch Drones
cd Fleet_Manager

## MobaXterm ssh
./launch_moba.sh

## Raspbian
./launch_drones.sh

## VSCode (One by one)
./launch_vscode.sh <ID>

# Launch only one drone in separate terminals (in this order)
## ROS2 Drone
cd FleetManager/Drone_<ID>/ROS2
sudo docker compose up --build

## Drone
cd FleetManager/Drone_<ID>
python init_drone.py --drone_id <ID>
