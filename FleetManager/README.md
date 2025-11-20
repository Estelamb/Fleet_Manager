curl -X POST -H "Content-Type: application/json" --data-binary @mission_1.json

docker network create \
  --driver=bridge \
  --subnet=192.168.100.0/24 \
  --gateway=192.168.100.1 \
  fleet_net

sudo usermod -aG docker $USER
newgrp docker  # Apply group changes without logout
# Get full network ID
NET_ID=$(docker network inspect fleet_net -f '{{.Id}}')

# Extract first 12 characters for interface name
BRIDGE_NAME="br-${NET_ID:0:12}"
echo "Bridge interface: $BRIDGE_NAME"
sudo ufw allow in on $BRIDGE_NAME