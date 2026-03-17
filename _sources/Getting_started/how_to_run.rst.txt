Drone Fleet Manager Guide
=============================

This guide covers the initial installation and the subsequent steps to run the drone fleet management project using Raspberry Pi 5, ThingsBoard, and Docker.

Hardware Requirements
---------------------
* **Raspberry Pi 5** with Raspberry Pi OS (64-bit).
* **AI HAT+** with Hailo8/Hailo8L.
* **Pi Camera Module**.

Credentials & Environment
-------------------------

**Raspberry Pi 5**
* **Hostname:** ``grysberry5ai26``
* **User:** ``estela``
* **Password:** ``estela``

**ThingsBoard Platform**
* **URL:** https://srv-iot.diatel.upm.es/
* **User:** ``estela.mora.barba@alumnos.upm.es``
* **Password:** ``fleet_manager``

Installation (First Time Only)
------------------------------

Before running the project for the first time, ensure the following components are installed:

* :doc:`ai_hat`
* :doc:`hailo_rpi5`
* :doc:`docker`

**Docker Permissions**
Allow Docker to run without ``sudo``:

.. code-block:: bash

   sudo groupadd docker
   sudo usermod -aG docker $USER
   newgrp docker

**System Dependencies**
Run these commands in the ``Drone`` directory to prepare the OS:

.. code-block:: bash

   sudo apt update && sudo apt full-upgrade -y
   sudo apt install -y libssl-dev libcap-dev libcamera-dev python3-libcamera python3-picamera2 libraspberrypi-bin
   sudo usermod -aG video $USER
   sudo reboot

Operational Quick Start
-----------------------

1. Launch Cloud Server
~~~~~~~~~~~~~~~~~~~~~~
Start the server to enable the interface and mission management:

.. code-block:: bash

   cd Fleet_Manager/Cloud
   python server_8090.py

* **UI Access:** Open ``http://<IP_RPI5>:8090`` in your web browser.
* **Missions:** Upload mission files from ``Fleet_Manager/Cloud/Missions``.

2. Launch Fleet Manager
~~~~~~~~~~~~~~~~~~~~~~~
In the ``FleetManager`` directory, create the network (if it doesn't exist) and start the services:

.. code-block:: bash

   docker network create --driver=bridge --subnet=192.168.100.0/24 --gateway=192.168.100.1 fleet_net
   cd Fleet_Manager/FleetManager
   docker compose up --build

3. Launch Drones
~~~~~~~~~~~~~~~~
From the ``Fleet_Manager`` root directory, choose a launch method:

+--------------------+----------------------------------+-----------------------------+
| Method             | Description                      | Command                     |
+====================+==================================+=============================+
| MobaXterm SSH      | Launch all drones simultaneously | ``./launch_moba.sh``        |
+--------------------+----------------------------------+-----------------------------+
| Raspbian           | Launch all drones simultaneously | ``./launch_drones.sh``      |
+--------------------+----------------------------------+-----------------------------+
| VSCode             | Launch drones one by one         | ``./launch_vscode.sh <ID>`` |
+--------------------+----------------------------------+-----------------------------+

Manual Drone Control (Individual)
---------------------------------

If you need to launch a specific drone manually, follow this **strict order**:

**Step A: ROS2 Interface (Terminal 1)**

.. code-block:: bash

   cd FleetManager/Drone_<ID>/ROS2
   docker compose up --build

**Step B: Drone Logic (Terminal 2)**

.. code-block:: bash

   cd FleetManager/Drone_<ID>
   source .venv/bin/activate
   python init_drone.py --drone_id <ID>

.. warning::
   It is critical to execute the **ROS2-Drone** part before the **Drone Logic** (init_drone) part.

Sending Missions via API
------------------------

Alternatively, you can send a mission using ``curl``:

.. code-block:: bash

   cd Missions
   curl -X POST -H "Content-Type: application/json" --data-binary @<json file>.json http://127.0.0.1:8082/mission

*Replace <json file> with the name of your file (without the .json extension).*