Getting Started with RPI5 and Hailo8-8L
=======================================

Verify Installation
-------------------

After :doc:`ai_hat`, check if the Hailo chip is recognized by the system:

.. code-block:: bash

   hailortcli fw-control identify

If everything is OK, it should output something like this:

.. code-block:: text

   Executing on device: 0000:01:00.0
   Identifying board
   Control Protocol Version: 2
   Firmware Version: 4.17.0 (release,app,extended context switch buffer)
   Logger Version: 0
   Board Name: Hailo-8
   Device Architecture: HAILO8L
   Serial Number: N/A
   Part Number: N/A
   Product Name: N/A

Getting ``N/A`` for Serial Number, Part Number, and Product Name is normal for the AI HAT.

Test TAPPAS Core installation by running the following commands:

**Hailotools** (TAPPAS GStreamer elements):

.. code-block:: bash

   gst-inspect-1.0 hailotools

Expected result:

.. code-block:: text

   Plugin Details:
     Name                     hailotools
     Description              hailo tools plugin
     Filename                 /lib/aarch64-linux-gnu/gstreamer-1.0/libgsthailotools.so
     Version                  3.28.2
     License                  unknown
     Source module            gst-hailo-tools
     Binary package           gst-hailo-tools
     Origin URL               https://hailo.ai/

     hailoaggregator: hailoaggregator - Cascading
     hailocounter: hailocounter - postprocessing element
     hailocropper: hailocropper
     hailoexportfile: hailoexportfile - export element
     hailoexportzmq: hailoexportzmq - export element
     hailofilter: hailofilter - postprocessing element
     hailogallery: Hailo gallery element
     hailograytonv12: hailograytonv12 - postprocessing element
     hailoimportzmq: hailoimportzmq - import element
     hailomuxer: Muxer pipeline merging
     hailonv12togray: hailonv12togray - postprocessing element
     hailonvalve: HailoNValve element

**Hailonet** (HailoRT inference GStreamer element):

.. code-block:: bash

   gst-inspect-1.0 hailo

Expected result:

.. code-block:: text

   Plugin Details:
     Name                     hailo
     Description              hailo gstreamer plugin
     Filename                 /lib/aarch64-linux-gnu/gstreamer-1.0/libgsthailo.so
     Version                  1.0
     License                  unknown
     Source module            hailo
     Binary package           GStreamer
     Origin URL               http://gstreamer.net/

     hailodevicestats: hailodevicestats element
     hailonet: hailonet element
     synchailonet: sync hailonet element

     3 features:
     +-- 3 elements

If ``hailo`` or ``hailotools`` are not found, try deleting the GStreamer registry:

.. code-block:: bash

   rm ~/.cache/gstreamer-1.0/registry.aarch64.bin

Hailo RPi5 Basic Pipelines
--------------------------

Clone the Repository:

.. code-block:: bash

   git clone https://github.com/hailo-ai/hailo-rpi5-examples.git

Navigate to the repository directory:

.. code-block:: bash

   cd hailo-rpi5-examples

Run the following script to automate the installation process:

.. code-block:: bash

   ./install.sh

Running the examples
--------------------

When opening a new terminal session, ensure you have sourced the environment setup script:

.. code-block:: bash

   source setup_env.sh

Detection Example
^^^^^^^^^^^^^^^^^

Run the **simple detection** example:

.. code-block:: bash

   python basic_pipelines/detection_simple.py

To close the application, press ``Ctrl+C``.

Run the **full detection** example:

.. code-block:: bash

   python basic_pipelines/detection.py

To close the application, press ``Ctrl+C``.

Running with Raspberry **Pi Camera input**:

.. code-block:: bash

   python basic_pipelines/detection.py --input rpi

Pose Estimation Example
^^^^^^^^^^^^^^^^^^^^^^^

Run the pose estimation example:

.. code-block:: bash

   python basic_pipelines/pose_estimation.py

To close the application, press ``Ctrl+C``. See Detection Example above for additional input options examples.

Instance Segmentation Example
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Run the instance segmentation example:

.. code-block:: bash

   python basic_pipelines/instance_segmentation.py

To close the application, press ``Ctrl+C``. See Detection Example above for additional input options examples.

Depth Estimation Example
^^^^^^^^^^^^^^^^^^^^^^^^

Run the depth estimation example:

.. code-block:: bash

   python basic_pipelines/depth.py

To close the application, press ``Ctrl+C``. See Detection Example above for additional input options examples.

References
----------

- Hailo Documentation - Getting started with RPI5-Hailo8L: https://community.hailo.ai/t/getting-started-with-rpi5-hailo8l/740
- Hailo Documentation - Hailo RPi5 Examples Repository: https://github.com/hailo-ai/hailo-rpi5-examples?tab=readme-ov-file
