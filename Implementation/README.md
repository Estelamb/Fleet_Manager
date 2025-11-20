# venv (cd Implementation)
pip3 install -r requirements.txt
source ROS2/install/setup.bash
source StateVector/install/setup.bash
python3 init_fleet.py

# Drones (cd Drone)
```
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
source install/setup.bash
python3 init_drone.py --drone_id 1
```

ros2 action send_goal /drone1/commands commands_action_interface/action/Commands "{commands_list: ['TAKEOFF']}"
ros2 action send_goal /drone2/commands commands_action_interface/action/Commands "{commands_list: ['LAND']}"

## GRPC (cd FleetManager)
pip install grpcio grpcio-tools

python -m grpc_tools.protoc -IGRPC/ --python_out=GRPC/ --grpc_python_out=GRPC/ mission.proto
python -m grpc_tools.protoc -IGRPC/ --python_out=GRPC/ --grpc_python_out=GRPC/ rest.proto
python -m grpc_tools.protoc -IGRPC/ --python_out=GRPC/ --grpc_python_out=GRPC/ plan.proto
python -m grpc_tools.protoc -IGRPC/ --python_out=GRPC/ --grpc_python_out=GRPC/ result.proto
python -m grpc_tools.protoc -IGRPC/ --python_out=GRPC/ --grpc_python_out=GRPC/ db_request.proto
python -m grpc_tools.protoc -IGRPC/ --python_out=GRPC/ --grpc_python_out=GRPC/ db_response.proto
python -m grpc_tools.protoc -IGRPC/ --python_out=GRPC/ --grpc_python_out=GRPC/ mqtt.proto

## REST (cd Cloud)
Client: curl -X POST -H "Content-Type: application/json" --data-binary @Missions/mission_1.json http://127.0.0.1:8082/mission

pip install flask requests
python3 server_8081.py  # Starts on port 8081
http://localhost:8081

sudo apt install libmariadb-dev


Clean Existing Shared Memory Resources

# Remove all existing SHM files
sudo rm -rf /dev/shm/*
sudo rm -f /tmp/ros2_*.shm

# Restart the shared memory manager
sudo systemctl restart systemd-udevd

# Sphinx
## Install Required Packages
pip install sphinx sphinx-rtd-theme
To requirements:
    sphinx==7.3.7
    sphinx-rtd-theme==2.0.0
    imghdr-fix==1.3.0

## Build Documentation
cd docs
rm -rf build/  
sphinx-build -b html source build


# DB
sudo mysql_secure_installation
root: root

Create Database and User
sudo mariadb -u root -p

CREATE DATABASE IF NOT EXISTS fleet_database;
CREATE USER 'fleet'@'localhost' IDENTIFIED BY 'fleet';
GRANT ALL PRIVILEGES ON fleet_database.* TO 'fleet'@'localhost';
FLUSH PRIVILEGES;
EXIT;

sudo mariadb -u fleet -p fleet_database
SHOW TABLES;
DESCRIBE state_vector;
SELECT * FROM state_vector;

SHOW DATABASES;
DROP DATABASE IF EXISTS fleet_database;
