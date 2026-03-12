#!/bin/bash

# Ensure Linux line endings
sed -i 's/\r$//' "$0"

# Check if an ID was provided
if [ -z "$1" ]; then
    echo "Error: No drone ID provided."
    echo "Usage: ./launch_drone.sh <id>"
    exit 1
fi

ID=$1
SESSION="drone_${ID}_session"

# 1. Clean up existing sessions for this specific drone
tmux kill-session -t $SESSION 2>/dev/null
sleep 1

# Function to wait for Docker
wait_for_docker() {
    local DRONE_ID=$1
    echo "Waiting for Drone $DRONE_ID Docker container..."
    
    # Poll until the container name containing 'drone' and the ID appears as running
    while [ -z "$(docker ps --filter "status=running" --format "{{.Names}}" | grep -i "drone.*$DRONE_ID")" ]; do
        sleep 1
    done
    
    echo "Drone $DRONE_ID Docker is ready."
}

echo "Deploying Drone $ID from FleetManager..."

# --- STEP 1: START ROS2 (Docker) ---
# We enter the specific drone's ROS2 folder
tmux new-session -d -s $SESSION -n "Drone$ID" "cd Drone_$ID/ROS2 && docker compose up --build; exec bash"

# --- STEP 2: WAIT FOR DOCKER ---
wait_for_docker $ID
sleep 10 # Extra buffer for ROS stability

# --- STEP 3: SPLIT HORIZONTALLY FOR PYTHON ---
# We enter the specific drone's folder to find the .venv and script
tmux split-window -h -t $SESSION "cd Drone_$ID && source .venv/bin/activate && python init_drone.py --drone_id $ID; exec bash"

# Ensure equal width panes
tmux select-layout even-horizontal

# Attach to the session
tmux attach-session -t $SESSION