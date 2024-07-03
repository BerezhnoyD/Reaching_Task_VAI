---
layout: default
title: Hardware part
nav_order: 3
description: "This is a description of ReachOut behavioral box electronics"

---

## Hardware overview

Here is the design of the whole setup, everything on the box side is controlled by **Arduino**,
and the experiment can be performed event without the the computer, but you will need **the PC** to 
save the streaming data from the camera and the box sensors.  

<img src="{{ site.baseurl }}/images/Overview.PNG" alt="drawing" width="600" height="600"/>


The **control** of the behavioral protocol, all the **stimuli** and **reinforcement** (food pellets) presentation, 
**data logging** from the sensors and video camera stream activation is handled by the custom circuit, connected to all the components of the reaching box. 
The schematics are housed in a small 3d printed box and soldered together on a simple breadboard. Most of the components are ready available cicuit modules, which
you just need to put together (no extensive knowledge of electronics needed).

## Main circuit components

![Image]({{ site.baseurl }}/images/circuit.PNG)

The same schematics can be found in the Repository and [STAR Protocols] article, supplementary materials.
The main components of the system are the **Arduino Nano** controller autonomously performing the programmed experimental protocol (written in C++ using Arduino IDE) 
with different **Adafruit shields** connected to it. Hence, powered with an external 5V source this behavioral system can be used autonomously for automatic/semi-automatic 
training of mice to perform the reach-to-grasp task, freeing the experimenter from the manual handling of behavioral protocol, and allowing seamless integration with 
*in vivo* electrophysiology recording or other current brain recording/stimulation methods. 

At the same time, connected to the **computer with a USB cable** and a simple 
**Python program** on the computer side this system saves two data streams and allows live monitoring of the data: basic behavioral data from the touch sensors 
(position of the animal, paw placement, time spent in front of the slit, timing and number of trials) and 3d view of the reaching movement (from the front camera and two side mirrors) 
that allows for more sophisticated kinematic analysis of both left and right-hand reaches. 

## Uploading the experimental protocol

The assembled box is programmed with [Arduino IDE] for its use as a standalone device for automated/semi-automated
animal training and behavioral data acquisition. The reaching box can log basic behavioral data (touch/beam sensors)
and is designed to be connected to external devices to trigger in vivo imaging, optogenetic stimulation etc. 
It can stream the synchro signal from the behavioral events recorded by the onboard sensors with millisecond resolution,
which makes it ideally fitted for synchronized behavioral-neurophysiology experiments. With the use of multiple mirrors, 
the system can acquire multiple close-up views for 3d trajectory reconstruction (triangulation) of the reach-to-grasp movement 
with a single high-speed **FLIR camera** when connected to the **desktop PC**. The output of the system is a behavioral video of the 
reaching movements throughout the learning session along with the *.tsv* table of the synchronized data from **Arduino**. 

After a single upload of the program the board will perform it autonomously on every power up without any actions needed from the user. 
To switch to another protocol, we’ll need to upload another program using Arduino IDE. The Arduino programming environment can be downloaded from the
official website [Arduino IDE] and is used to write compile and upload the C++ code for Arduino controllers. 

### List of the programs provided in the repository:
 
1.	***Reaching_Task_Draft*** – basic protocol with initialization for all the components to explore the structure of the program.
2.	***Reaching_Task_Manual*** - Feeder makes one step clockwise or counterclockwise when the experimenter presses the left or right button respectively.
3.	***Reaching_Task_Feeder_Training*** – Feeder takes one step every 10sec while animal is in the front part of the box.
4.	***Reaching_Task_Door_Training*** – If animal is detected in the front part of the box and grabs the elevated front rod, the feeder takes one step and the door blocking the slit opens (need additional servo motor connected, see Fig.3D).
5.	***Reaching_Task_CS_Training***  - If animal is detected in the front part of the box the speaker delivers 5s beep sound (CS trial) with intertrial intervals of 5s (ITI) and if the animal grabs the elevated front rod during this sound (trial) the feeder makes one step and the door blocking the slit opens

## Q&A

If you still have questions after reading this and [STAR Protocols] please let us
know and we list it in this section.




---

[STAR Protocols]: https://star-protocols.cell.com/protocols/3539
[Arduino IDE]: https://www.arduino.cc/en/software 

