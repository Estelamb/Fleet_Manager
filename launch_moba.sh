#!/bin/bash

# Drone IDs
DRONES=(1 2 3)

# Function to check if a container is running
wait_for_docker() {
    local ID=$1
    echo "Waiting for Drone_$ID container..."
    # Adjust 'drone_$ID' if your container name is different in docker-compose.yml
    while [ -z "$(docker ps -q -f status=running -f name=drone_$ID)" ]; do
        sleep 2
    done
    echo "Docker $ID is UP!"
}

for ID in "${DRONES[@]}"
do
    echo "Launching Drone_$ID deployment..."

    # 1. Open XTerm for Docker Compose
    # -title: Sets the window title
    # -hold: Keeps the window open if the process exits
    xterm -T "D$ID: DOCKER LOGS" -e "bash -c 'cd Drone_$ID/ROS2 && docker compose up --build; exec bash'" &

    # 2. Wait for the container to actually start
    wait_for_docker $ID

    # 3. Open XTerm for Python Script
    # Loads the virtual environment and runs the init script
    xterm -T "D$ID: PYTHON INIT" -e "bash -c 'cd Drone_$ID && source .venv/bin/activate && python init_drone.py --drone_id $ID; exec bash'" &

    # Small delay between drones to prevent X11 server lag
    sleep 1
done

echo "All 6 windows have been forwarded to MobaXterm."