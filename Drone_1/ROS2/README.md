pip install --break-system-packages -r requirements.txt

python -m grpc_tools.protoc -IGRPC/ --python_out=GRPC/definitions --grpc_python_out=GRPC/definitions command.proto
python -m grpc_tools.protoc -IGRPC/ --python_out=GRPC/definitions --grpc_python_out=GRPC/definitions feedback.proto
python -m grpc_tools.protoc -IGRPC/ --python_out=GRPC/definitions --grpc_python_out=GRPC/definitions metrics.proto
python -m grpc_tools.protoc -IGRPC/ --python_out=GRPC/definitions --grpc_python_out=GRPC/definitions pm.proto

source install/setup.bash
python init_ros2.py --drone_id 1

sudo docker compose down --remove-orphans
sudo docker compose build --no-cache
sudo docker compose up
sudo docker compose run ros2_drone bash

sudo ufw allow 51001  # Allow gRPC port
sudo ufw reload