AI HAT+ with Hailo8-8L and Pi Camera Module Installation
========================================================

Update the system
-----------------

First, make sure your Raspberry Pi is running the latest software:

.. code-block:: bash

   sudo apt update && sudo apt full-upgrade

Then, update the firmware:

.. code-block:: bash

   sudo rpi-eeprom-update -a

Reboot the system to apply the changes:

.. code-block:: bash

   sudo reboot

Configure PCIe and Pi Camera Module
-----------------------------------

Connect the RPI Camera, then open the configuration tool:

.. code-block:: bash

   sudo raspi-config

Follow these steps:

1. Select ``Advanced Options``.
2. Select ``PCIe Speed``.
3. Choose ``Yes`` to enable PCIe Gen 3 mode.
4. Select ``Finish`` to exit.
5. Reboot your Raspberry Pi for your changes to take effect.

.. code-block:: bash

   sudo reboot

Install Hailo Dependencies
--------------------------

Install the required packages for the Hailo AI module:

.. code-block:: bash

   sudo apt install hailo-all

Reboot again after installation:

.. code-block:: bash

   sudo reboot

Verify Hailo Installation
-------------------------

To confirm that the NPU and its software dependencies are working correctly, run:

.. code-block:: bash

   hailortcli fw-control identify

You should see output similar to:

.. code-block:: text

   Executing on device: 0000:01:00.0
   Identifying board
   Control Protocol Version: 2
   Firmware Version: 4.17.0 (release,app,extended context switch buffer)
   Logger Version: 0
   Board Name: Hailo-8
   Device Architecture: HAILO8L (or HAILO8)
   Serial Number: HLDDLBB234500054
   Part Number: HM21LB1C2LAE
   Product Name: HAILO-8L AI ACC M.2 B+M KEY MODULE EXT TMP

Getting N/A for Serial Number, Part Number, and Product Name is normal for the AI HAT.

Test the Pi Camera Module
-------------------------

To verify the camera is functioning properly, run:

.. code-block:: bash

   sudo rpicam-hello -t 10s

Run Demos (Optional)
--------------------

You can try out sample demos by visiting:

`Demos - AI Kit and AI HAT+ software <https://www.raspberrypi.com/documentation/computers/ai.html>`_

References
----------

- Raspberry Pi – AI Kit and HAT+ Software Demos: https://www.raspberrypi.com/documentation/computers/ai.html
- Raspberry Pi – AI HAT+ Documentation: https://www.raspberrypi.com/documentation/accessories/ai-hat-plus.html
