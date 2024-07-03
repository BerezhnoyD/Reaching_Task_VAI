---
layout: default
title: Software Installation
parent: Software part
nav_order: 5
description: "This is a description of ReachOut software installation"
---

## Installation
### Recording toolbox
The recording toolbox contains two parts: 
- one on the **Arduino** side 

```
Choose one of the provided scripts, edit and upload to the microcontroller with the use of Arduino IDE
```

- and one on the **PC** side. This one is just the snippet to record from the FLIR camera and simultaneously record from Arduino.
The second part is taken with minor changes from the [PySpin] repository, so you should follow the installation instructions listed there.


> INSTALLATION: Most of the dependencies in the import statements are included in a standard Anaconda installation (i.e. PIL, Numpy, Tkinter) 
> and with your NVIDIA graphics card (i.e CUDA) for the GPU versions. PySpin and the Spinnaker API must be downloaded from the FLIR website (https://www.flir.com/products/spinnaker-sdk/);
> choose the appropriate version of Spinnaker and install first, then install the "Latest Python Spinnaker" version that is compatible with your version of Python (I've tested with Python 3.5 & 3.8) 
> using the instructions in the ReadMe file. An FFMPEG executable needs to be downlaoded (https://ffmpeg.org/download.html) and placed in a folder that you can point to in the import statements, 
> such as within the site-packages folder of your Python installation. Finally, scikit-video (http://www.scikit-video.org/stable/) can be added to your Python installation using pip.


After installing PySpinCapture simply run one of the scripts provided in the [ReachOut] repository [Recording Toolbox] like that:

```python
> cd path\to\the repository\
> python CameraRoll.py
```

### Analysis toolbox
Analysis toolbox included with this project can be used as a part of the proposed [STARs Protocols] pipeline or as a standalone application
The analysis toolbox is dependent on certain python libraries and programs (DEEPLABCUT, ANIPOSE) and Jupyter Notebook.
To make it easier for installation all the dependencies are included in the updated *DEEPLABCUT.yml conda environment file
contained in [ReachOut] repository [Analysis Toolbox].
After installing Anaconda just run the following commands:

```python
> cd path\to\the repository\Analysis toolbox\
> conda env create -f DEEPLABCUT.yml
```

## Q&A

If you still have questions after reading this and [STAR Protocols] please let us
know and we list it in this section. If you experience any bugs during the installation or
use please let us know ASAP so we can fix them in the next release. We appreciate your feedback

---