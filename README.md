# ReachOut platform
The following project describes the design, fabrication, assembly and use case of the open-source hardware platform
for mice reach-to-grasp task training and fine motor skill video analysis. We present the behavioral platform - 
automated mouse Reaching Box that was designed to be 3D printed and hence easily reproducible. 
The device is used to train animals to perform reach-to-grasp dexterity task: approach the proximal part of the reaching box
and reach for single sugar pellets disposed by motorized feeder disk located in front of the narrow slit. 
This task is used for studying planning and execution of fine motor skills requiring cortical control of the forepaw and finger movement. 
Behavioral platform allows to record the video and track the forepaw and fingers during the reaching movement. 
This tracking data (performed by DLC networks) can be analyzed further to extract different kinematic parameters 
(speed, acceleration, jerk, accuracy) and different moments of the reach (start, peak, end) 
to use them as behavioral keypoints (ex. peri-event analysis).]

Hardware used in the design of the platform, aside from the high-speed FLIR camera, 
consists of readily available open-source components that can be acquired relatively 
cheap or fabricated with the use of stereolithography 3D printer. Software is written in Python and organized in multiple Jupyter Notebooks.

###Hardware overview
All the schematics, 3D models and assembly instructions are provided in this repository. The assembled box is programmed with Arduino IDE for its use as a standalone device for automated/semi-automated animal training and behavioral data acquisition. The reaching box can log basic behavioral data (touch/beam sensors) and is designed to be connected to external devices to trigger in vivo imaging, optogenetic stimulation etc. It can stream the synchro signal from the behavioral events recorded by the onboard sensors with millisecond resolution, which makes it ideally fitted for synchronized behavioral-neurophysiology experiments. With the use of multiple mirrors, the system can acquire multiple close-up views for 3d trajectory reconstruction (triangulation) of the reach-to-grasp movement with a single high-speed FLIR camera when connected to the desktop PC. The output of the system is a behavioral video of the reaching movements throughout the learning session along with the tsv table of the synchronized data from Arduino.

###Software overview
In addition to the hardware part, we provide the complementary software data analysis pipeline which can be performed off-line with the acquired videos. Python package for the 3d trajectory reconstruction and kinematic analysis is organized in classes and modules implemented in a series of Jupyter Notebooks and based on the state-of-the-art solutions for the markerless pose estimation as well as original code
DeepLabCut (https://github.com/DeepLabCut/DeepLabCut) and 
Anipose Lib (https://github.com/lambdaloop/aniposelib). 
The pipeline guides the user through the number of steps to extract the parts from the video, track and triangulate the points of interest (paw, fingers), cluster the reaches, visualize and compare basic kinematic parameters for different reaching categories. User has the ability to export the final data on the kinematics (scalars for each reach) and reaching timestamps as a *.h5/.csv table for further analysis or synchronization with his own pipeline.





The repository contains all the materials to build the mouse reaching task and analyze the data acquired with this task
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

