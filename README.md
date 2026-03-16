# Fleet Manager Project

This repository contains the configuration and launch scripts for drone fleet management using Raspberry Pi 5, ThingsBoard, and Docker.

---

## Credentials & Environment

### Raspberry Pi 5
- **Hostname:** `grysberry5ai26`
- **User:** `estela`
- **Password:** `estela`

### ThingsBoard Platform
- **URL:** [https://srv-iot.diatel.upm.es/](https://srv-iot.diatel.upm.es/)
- **User:** `estela.mora.barba@alumnos.upm.es`
- **Password:** `fleet_manager`

---

## Quick Start Guide

### 1. Launch Cloud Server
Start the server to enable the interface and mission management:
```bash
cd Fleet_Manager/Cloud
python server_8090.py
```

- UI Access: Open http://<IP_RPI5>:8090 in your web browser.
- Missions: Upload mission files from Fleet_Manager/Cloud/Missions.

### 2. Launch Fleet Manager
Bring up the main services using Docker Compose:

```bash
cd Fleet_Manager/FleetManager
sudo docker compose up --build
```

### 3. Launch Drones
From the Fleet_Manager root directory, choose the launch method that fits your environment:

| Method | Description | Command |
| :--- | :--- | :--- |
| MobaXterm SSH | Launch all the drones at the same time | `./launch_moba.sh` |
| Raspbian | Launch all the drones at the same time | `./launch_drones.sh` |
| VSCode (Individual) | Launch drones one by one | `./launch_vscode.sh <ID>` |

#### Manual Drone Control
If you need to launch a specific drone in separate terminals, follow this order:

Step A: ROS2 Interface (Terminal 1)
```bash
cd FleetManager/Drone_<ID>/ROS2
sudo docker compose up --build
```

Step B: Drone Logic (Terminal 2)
```bash
cd FleetManager/Drone_<ID>
python init_drone.py --drone_id <ID>
```
