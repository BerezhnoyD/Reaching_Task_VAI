---
layout: default
title: Home
nav_order: 1
description: "Documentation for the ReachOut project"
permalink: /
---

<div style="text-align: center"><img src="{{ site.baseurl }}/icon.png" alt="drawing" width="300" height="300"/></div>


ReachOut project is an open-source hardware-software platform for analyzing reaching movement kinematics in mice. 
The whole design consists of 3 main parts described here:
{: .fs-6 .fw-200 }
- ***3D printed box*** for training mice to perform reach-to-grasp task & acquire behavioral videos for kinematic analysis
- ***Arduino-based controller*** for executing behavioral protocol & recording animal behavior
- ***ReachOut software (analysis pipeline)*** to analyze videos & perform kinematic analysis on reconstructed forepaw trajectory
{: .fs-6 .fw-200 }
[![DOI](https://zenodo.org/badge/517810120.svg)](https://zenodo.org/doi/10.5281/zenodo.7383917)

There is an Article in STAR Protocols with all the details and Repository on GitHub with all materials
to recreate the setup
{: .fs-6 .fw-200 }
[View it in the Article][STAR Protocols]{: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View it on GitHub][ReachOut]{: .btn .fs-5 .mb-4 .mb-md-0 }
 
{: .warning }
> This website documents the features of the current `main` branch accompanying the STARs Protocol article. For the code described in the article use
> alpha or beta release in the [ReachOut] repository

---

### Getting Started
Did you know that mice are pretty good at using their forepaws? Well, probably you do
and can skip the [Science background](#science-background) section and go straight to [Project overview](#project-overview)
or to one of the sections provided in the docs (*Navigation on the left sidebar*).

<img src="{{ site.baseurl }}/reachout.gif" alt="drawing" width="600" height="600"/>

But how to dissect and study this complex movement? 
We tried to provide the comprehensive solution to this problem that can be
implemented in-lab with a little background knowledge in *3d printing, Arduino and Python Coding*.
  
All the installation instructions are currently in the [Software part](#software.html) section. 
You can use the analysis part separately for your project by copying the Jupyter Notebooks.






### Science background
Reach-to-grasp task in rodents first developed by Ian Whishaw [^1] has recently became the gold standard for the study of fine motor behavior in rodents.
The structure of the movement and the neurocircuitry behind it can be well translated between rodents and higher primates including humans [^2][^3] which makes this task
very popular for the study of cortical motor control. There is an increasing use of reach-to-grasp task along current neurophysiological tools like 2-photon imaging
or optogenetics for the study of neural activity during execution of the planned motor command [^4]. However, there are not many designs available for the reach-to-grasp task in freely behaving mice. 

With the dawn of DIY electronic kits (**Arduino**) and stereolithography 3D printer technology (**OpenCAD**) we see the field of open-source behavioral box design rapidly expanding and
being a major driver for neuroscience discoveries. There are multiple designs for Skinner boxes and rodent operant chambers proposed by different laboratories. However, there are fewer 
solutions to study fine motor skills, probably due to the difficulties in *precise presentation of the reinforcement* and *quantifying the kinematics* of the small animal movements. 
The second problem has been recently solved with the use of deep-learning video analysis [DeepLabCut]. However, the solutions specifically tailored for the behavior-neurophysiology coupling often use
head-fixed animals and focused on precise synchronization of the animal behavior, heavily constrained, with the neurophysiology recording. 
Training animals in such setups can be *problematic and labor-intensive*. On the other side, apparatuses proposed to study reaching in freely behaving animals, 
following the line of operant boxes research, usually lack the precision and time resolution needed to synchronize with external devices used in neurophysiology research. Moreover, research with 
automatic learning boxes, even ReachingBots [^5], generally focus on simple metrics like the number of trials and success rate of reaching and overlook more sophisticated kinematic analysis which requires better video quality, 
precision and post-processing of the behavioral data. Thus, there is always a tight balance between the *open-source (ease of manufacture)* and *research-grade (temporal precision)* needed for neurophysiology 
and precise kinematic studies.
  
***Trying to fill this gap we have developed a comprehensive hardware-software setup for mice, using the current state-of-the-art solutions in 3D printing and DNN data analysis and made it accessible to the large open-science community.***


### Project overview
This website describes the basics of design, fabrication, assembly and use case for the open-source hardware platform
for mice reach-to-grasp task training and fine motor skill video analysis. You are free to use either the [Software part](#software.html)
of this project for kinematic analysis ***(ReachOut pipeline)*** on the videos from your setup or build the whole behavioral apparatus setup 
using the instructions provided in the [STAR Protocols] article.


***Behavioral apparatus*** - automated mouse Reaching Box that is 3D printed and hence easily reproducible. 
The device is used to train animals to perform reach-to-grasp dexterity task: approach the proximal part of the reaching box
and reach for single sugar pellets disposed by motorized feeder disk located in front of the narrow slit. 
This task is used for studying planning and execution of fine motor skills requiring cortical control of the forepaw and finger movement. 
The semi-automated setup allows to record the video and track the forepaw and fingers during the reaching movement. 

***Hardware*** used in the design of the task, aside from the high-speed FLIR camera, 
consists of readily available open-source components that can be acquired relatively 
cheap or fabricated with the use of stereolithography 3D printer. 

The [ReachOut] repository contains all the materials to build the mouse reaching task and analyze the data acquired with this task
- 3D models for the components of the box
- Schematics for the reaching box Arduino-based controller
- Scripts to run the video recording from the FLIR Camera and logging the data from Arduino
- Scripts for the full analysis dataflow: detecting body parts with DLC and getting the reaching trajectories

***Analysis software*** can be used with the behavioral box to analyze reaching kinematics or as a standalone application for kinematic
analysis for the action of your choice (walking, whisker movement, you name it) in your project with certain adaptations. The aim of this part
is to simplify keypoint tracking (performed by DLC networks), reviewing tracking results along with the videos and extract different kinematic parameters 
(speed, acceleration, jerk, accuracy) and different moments of the reach (start, peak, end) to use them as behavioral keypoints (ex. peri-event analysis).

We gathered all the code in a series of annotated [Jupyter Notebooks] for you to use. All the necessary
libraries can be installed using provided *DEEPLABCUT.yml* environment file for **Anaconda**.
For the quick overview and instructions go straight to [Software part](#Software part) section.


## About the project

ReachOut is maintained &copy; 2022-{{ "now" | date: "%Y" }} by [Daniil Berezhnoi](https://www.researchgate.net/profile/Daniil-Berezhnoy).
All the materials are OpenSource and Authors would be happy to help you with any questions on the code.

----

[^1]: [The structure of skilled forelimb reaching in the rat: A proximally driven movement with a single distal rotatory component](https://www.sciencedirect.com/science/article/pii/016643289090053H#:~:text=(1)%20Most%20of%20the%20first,the%20midline%20of%20the%20body.).
[^2]: [Post-stroke kinematic analysis in rats reveals similar reaching abnormalities as humans](https://www.nature.com/articles/s41598-018-27101-0)
[^3]: [Quantitative kinematic characterization of reaching impairments in mice after a stroke](https://pubmed.ncbi.nlm.nih.gov/25323462/)
[^4]: [Online control of reach accuracy in mice](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7814908/)
[^5]: [ReachingBot: An automated and scalable benchtop device for highly parallel Single Pellet Reach-and-Grasp training and assessment in mice](https://www.sciencedirect.com/science/article/pii/S0165027023001279?via%3Dihub)

[STAR Protocols]: https://star-protocols.cell.com/protocols/3539
[DeepLabCut]: https://github.com/DeepLabCut/DeepLabCut/
[Anipose Lib]: https://github.com/lambdaloop/aniposelib/
[ReachOut]: https://github.com/BerezhnoyD/Reaching_Task_VAI/
[Jupyter Notebooks]: https://github.com/BerezhnoyD/Reaching_Task_VAI/tree/main/Analysis toolbox/2D pipeline/
[Just the Docs]: https://just-the-docs.github.io/just-the-docs/
[GitHub Pages]: https://docs.github.com/en/pages
[README]: https://github.com/just-the-docs/just-the-docs-template/blob/main/README.md
[Jekyll]: https://jekyllrb.com
[GitHub Pages / Actions workflow]: https://github.blog/changelog/2022-07-27-github-pages-custom-github-actions-workflows-beta/
[use this template]: https://github.com/just-the-docs/just-the-docs-template/generate
