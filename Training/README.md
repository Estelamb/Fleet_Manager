# How to Train

## Object Detection Model Training and Hailo Compilation Tutorial

**Based on**: [`LukeDitria/RasPi_YOLO`](https://github.com/LukeDitria/RasPi_YOLO)  

**Datasets used**:
- [`Leaf Detection`](https://www.kaggle.com/datasets/alexo98/leaf-detection)
- [`PlantVillage (Grape classes only)`](https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset?select=color)
- [`Grape Grapes`](https://www.kaggle.com/datasets/nicolaasregnier/grape-grapes)

This tutorial shows how to train three different object detection models, export them to ONNX, and compile them for Hailo. Variable placeholders like `<DATASET_PATH>` or `<MODEL_NAME>` are used instead of real values.

---

## Requirements

Install the necessary Python packages:

```
pip install ultralytics
pip uninstall torch torchvision -y
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install onnx onnxruntime-gpu onnxslim
pip install onnxsim
```

## Prepare the Dataset
Organize your data like this:

```
<DATASET_PATH>/
├── images/
│   ├── <CLASS_1>/
│   │   ├── image1.jpg
│   │   └── ...
│   └── <CLASS_2>/
│       ├── image1.jpg
│       └── ...
└── classes.json
```

Generate YOLO labels:
```
python <DATASET_PATH>/<LABELS_SCRIPT>.py
```

After this, your structure should be:
```
<DATASET_PATH>/
├── images/
│   ├── <CLASS_1>/
│   └── <CLASS_2>/
├── labels/
│   ├── <CLASS_1>/
│   └── <CLASS_2>/
└── classes.json
```

Create a configs/ folder and run the next script to set up configuration YAMLs and data splits:
```
python create_data_splits.py --data_dir <DATA_DIRECTORY_PATH>

# For ONNX export configuration:
python create_data_splits.py --data_dir <DATA_DIRECTORY_PATH> --onnx_config
```

After this, your structure should be:
```
<MODEL_DIR>/
├── configs/
│   ├── data_directory_config.yaml
│   └── data_directory_onnx_config.yaml
```

## Training the Model
Use the training script:

```
python yolo_train.py --config <DATA_CONFIG>.yaml --init_model yolov8n.pt --name <DATASET_NAME> --epochs 20 --device 0
The output will be in the runs/detect/<DATASET>/weights folder and it is the best.pt file.
```

## Export to ONNX
Convert the trained model to ONNX by editing the Python module with your model:
```
python export_to_onnx.py
```

## Generate Calibration Data for Hailo Converter
Create the folder calib and run:
```
python hailo_calibration_data.py --data_dir <DATA_DIRECTORY> --image_size 640 640 --num_images 1024
```

## Compile the Model for Hailo
Follow the install_compiler instructions and run the Docker. It will generate the shared_with_docker folder. Then, copy and paste the ONNX model and the calib folder and run in the local directory:
```
hailomz compile --ckpt shared_with_docker/<ONNX_MODEL>.onnx --calib-path shared_with_docker/<PATH_TO_CALIB_FOLDER> --yaml workspace/hailo_model_zoo/hailo_model_zoo/cfg/networks/yolov8n.yaml --classes <NUMBER_OF_CLASSES> --hw-arch <HAILO8 OR HAILO8L>
```

The resulting .hef file is the model compiled for Hailo.