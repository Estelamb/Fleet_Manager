# In Drone: 
python -m init_drone --drone_id 1 
python -m Test_Modules.commands_test 1 Test_Modules/mission_1.json
 
# In ROS2
sudo docker compose up

sudo apt install python3-pip python3-venv  # Basic Python environment
sudo apt install libssl-dev  # For SSL/TLS support (required for port 8883)
sudo apt install -y libcap-dev libcamera-dev python3-libcamera python3-picamera2

sudo reboot

deactivate
rm -rf .venv  # Remove existing environment
python3 -m venv --system-site-packages .venv
source .venv/bin/activate

pip install -r requirements.txt

sudo usermod -aG video $USER

## Check camera detection
libcamera-hello

hailomz compile --ckpt shared_with_docker/Grape_Diseases/grape_diseases_best.onnx --calib-path shared_with_docker/Grape_Diseases/calib --yaml workspace/hailo_model_zoo/hailo_model_zoo/cfg/networks/yolov8n.yaml --classes 4 --hw-arch hailo8 

hailomz compile --ckpt shared_with_docker/Leaf_Detection/leaf_detection_best.onnx --calib-path shared_with_docker/Leaf_Detection/calib --yaml workspace/hailo_model_zoo/hailo_model_zoo/cfg/networks/yolov8n.yaml --classes 1 --hw-arch hailo8 

hailomz compile --ckpt shared_with_docker/Grape_Bunch/grape_bunch_best.onnx --calib-path shared_with_docker/Grape_Bunch/calib --yaml workspace/hailo_model_zoo/hailo_model_zoo/cfg/networks/yolov8n.yaml --classes 3 --hw-arch hailo8


hailomz compile --ckpt shared_with_docker/Grape_Diseases/grape_diseases_best.onnx --calib-path shared_with_docker/Grape_Diseases/calib --yaml workspace/hailo_model_zoo/hailo_model_zoo/cfg/networks/yolov8n.yaml --classes 4 --hw-arch hailo8l 

hailomz compile --ckpt shared_with_docker/Leaf_Detection/leaf_detection_best.onnx --calib-path shared_with_docker/Leaf_Detection/calib --yaml workspace/hailo_model_zoo/hailo_model_zoo/cfg/networks/yolov8n.yaml --classes 1 --hw-arch hailo8l 

hailomz compile --ckpt shared_with_docker/Grape_Bunch/grape_bunch_best.onnx --calib-path shared_with_docker/Grape_Bunch/calib --yaml workspace/hailo_model_zoo/hailo_model_zoo/cfg/networks/yolov8n.yaml --classes 3 --hw-arch hailo8l
