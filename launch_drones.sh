#!/bin/bash

# Array of Drone IDs
DRONES=(1 2 3)

for ID in "${DRONES[@]}"
do
    echo "------------------------------------------"
    echo "Deploying Drone_$ID..."
    echo "------------------------------------------"

    # 1. Launch Docker Compose in a new terminal
    # This builds and starts the containers for the specific drone
    lxterminal --title="D$ID: Docker Logs" -e "bash -c 'cd Drone_$ID/ROS2 && docker compose up --build; exec bash'" &

    echo "Waiting for Drone_$ID container to be 'running'..."

    # 2. Sync Loop: Wait until the container is active
    # Note: Ensure your docker-compose.yml defines a container_name or service name 
    # that matches the filter below.
    while [ -z "$(docker ps -q -f status=running -f name=drone_$ID)" ]; do
        sleep 2
        echo "  ...still waiting for Docker $ID"
    done

    echo "Docker $ID is UP. Launching Python script..."

    # 3. Launch Python script in a separate terminal
    # Activates the venv and runs the init script
    lxterminal --title="D$ID: Python Script" -e "bash -c 'cd Drone_$ID && source .venv/bin/activate && python init_drone.py --drone_id $ID; exec bash'" &

    # Short delay to prevent CPU spikes when starting the next drone
    sleep 2
done

echo "------------------------------------------"
echo "All 6 terminals have been initialized."
echo "------------------------------------------"