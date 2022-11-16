# Reaching_Task_Chu_lab
This repository contains all the materials to build the mouse reaching task and analyze the data acquired with this task
- Bill of materials to build the reaching box
- 3D models for the components of the box
- Schematics for the reaching box Arduino-based controller
- Scripts to run the video recording from the FLIR Camera and logging the data from Arduino
- Scripts for the full analysis dataflow: detecting body parts with DLC and getting the reaching trajectories

## Installation
### Recording toolbox
The recording toolbox contains two parts: 
- one on the Arduino side (script should be uploaded to the microcontroller with the use of Arduino IDE)
- and one on the PC side. This one is just the snippet to record from the FLIR camera and simultaneously record from Arduino.
The second part is taken with minor changes from the PySpin repository, so you should follow the installation instructions listed there
(https://github.com/neurojak/pySpinCapture)


### Analysis toolbox
The analysis toolbox is dependent on certain python libraries and programs (DEEPLABCUT, ANIPOSE) and Jupyter Notebook.
DEEPLABCUT (https://github.com/DeepLabCut/DeepLabCut)
ANIPOSE (https://github.com/lambdaloop/anipose)

To make it easier for installation all the dependencies are included in the updated *DEEPLABCUT.yml conda environment file.

