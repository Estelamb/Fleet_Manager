FROM ubuntu:24.04

# Prevent interactive prompts during package installs
ENV DEBIAN_FRONTEND=noninteractive

# Set locale environment variables
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV ROS_DOMAIN_ID=1

# Install locales and set locale
RUN apt-get update && \
    apt-get install -y locales software-properties-common curl && \
    locale-gen en_US en_US.UTF-8 && \
    update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8

# Add Ubuntu universe repository
RUN add-apt-repository universe

# Add ROS 2 GPG key and repository
RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" \
    > /etc/apt/sources.list.d/ros2.list

# Update and install development tools and ROS 2 packages
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y ros-dev-tools ros-jazzy-desktop ros-jazzy-ros-base

# Source ROS2 setup and set ROS_DOMAIN_ID on container start
RUN echo "source /opt/ros/jazzy/setup.bash" >> /root/.bashrc && \
    echo "export ROS_DOMAIN_ID=1" >> /root/.bashrc

# Default shell when container runs
CMD [ "bash" ]

RUN apt-get update && apt-get install -y \
    apt-utils \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/
RUN pip install --break-system-packages -r /tmp/requirements.txt

# Crear workspace y copiar proyecto
RUN mkdir -p /home/FleetManager
WORKDIR /home/FleetManager

COPY . /home/FleetManager/

WORKDIR /home/FleetManager/ROS2
RUN /bin/bash -c "source /opt/ros/jazzy/setup.bash && colcon build"

WORKDIR /home/FleetManager/PrescriptionMap
RUN /bin/bash -c "source /opt/ros/jazzy/setup.bash && colcon build"

WORKDIR /home/FleetManager/SystemMetrics
RUN /bin/bash -c "source /opt/ros/jazzy/setup.bash && colcon build"

WORKDIR /home/FleetManager

EXPOSE 8082
EXPOSE 8080
EXPOSE 8883

CMD ["bash", "-c", "source /opt/ros/jazzy/setup.bash && source ROS2/install/setup.bash && source PrescriptionMap/install/setup.bash && source SystemMetrics/install/setup.bash && python3 init_fleet.py"]
