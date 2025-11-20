Hailo AI SW Suite Installation
==============================

Requirements
------------

- WSL - Ubuntu 24.04, 64 bit.
- 16+ GB RAM (32+ GB recommended).
- NVIDIA GPU.

CUDA Toolkit Installation
-------------------------

In WSL - Ubuntu, run:

.. code-block:: bash

   wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-wsl-ubuntu.pin
   sudo mv cuda-wsl-ubuntu.pin /etc/apt/preferences.d/cuda-repository-pin-600
   wget https://developer.download.nvidia.com/compute/cuda/12.9.1/local_installers/cuda-repo-wsl-ubuntu-12-9-local_12.9.1-1_amd64.deb
   sudo dpkg -i cuda-repo-wsl-ubuntu-12-9-local_12.9.1-1_amd64.deb
   sudo cp /var/cuda-repo-wsl-ubuntu-12-9-local/cuda-*-keyring.gpg /usr/share/keyrings/
   sudo apt-get update
   sudo apt-get -y install cuda-toolkit-12-9

Docker Engine Installation
--------------------------

In WSL - Ubuntu, set up Docker's ``apt`` repository:

.. code-block:: bash

   # Add Docker's official GPG key:
   sudo apt-get update
   sudo apt-get install ca-certificates curl
   sudo install -m 0755 -d /etc/apt/keyrings
   sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
   sudo chmod a+r /etc/apt/keyrings/docker.asc

   # Add the repository to Apt sources:
   echo \
     "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
     $(. /etc/os-release && echo \"${UBUNTU_CODENAME:-$VERSION_CODENAME}\") stable" | \
     sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   sudo apt-get update

Install the Docker packages. To install the latest version, run:

.. code-block:: bash

   sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

Verify that the installation is successful by running the ``hello-world`` image:

.. code-block:: bash

   sudo docker run hello-world

Add your user to the docker group:

.. code-block:: bash

   sudo usermod -aG docker ${USER}

Log out and log in.

Hailo AI SW Suite Installation
------------------------------

Download the suite from `Developer Zone <https://hailo.ai/developer-zone/sw-downloads/>`_.

Extract the suite archive, then run the script – which opens a new container and attaches to it:

.. code-block:: bash

   unzip hailo_ai_sw_suite_<version>.zip
   ./hailo_ai_sw_suite_docker_run.sh

If this error occurs:

.. code-block:: text

   INFO: Checking system requirements...
   ERROR: The Dataflow Compiler requires 16 GB of RAM (32 GB recommended), while this system has only 15 GB.
   ERROR: System requirements check failed.

Increase WSL Memory Allocation by creating/updating ``C:\Users\<Your_Windows_Username>\.wslconfig`` with:

.. code-block:: ini

   [wsl2]
   memory=18GB
   swap=12GB

Restart WSL:

.. code-block:: bash

   wsl --shutdown

Run the suite again:

.. code-block:: bash

   ./hailo_ai_sw_suite_docker_run.sh

You can exit the Docker container by using the ``exit`` command.

Other Docker commands:

- **Resume**: Go back to the existing container:

  .. code-block:: bash

     ./hailo_ai_sw_suite_docker_run.sh --resume

- **Override**: Delete the existing container and create a new one:

  .. code-block:: bash

     ./hailo_ai_sw_suite_docker_run.sh --override

References
----------

- Hailo Documentation - Hailo Software Suite 2025-04: https://hailo.ai/developer-zone/documentation/hailo-sw-suite-2025-04/?sp_referrer=suite/suite_install.html#docker-installation
- NVIDIA Documentation - NVIDIA CUDA Downloads: https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=WSL-Ubuntu&target_version=2.0&target_type=deb_local
- Docker Documentation - Docker Engine Installation: https://docs.docker.com/engine/install/ubuntu/
