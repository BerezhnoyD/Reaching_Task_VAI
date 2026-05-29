---
layout: page
title: Bonus Headfixed setup
nav_order: 6
description: "This is a description of the HeadFixed Reaching setup (ReachOut v.2.0)"
has_children: true

---

# ReachOut v.2.0 (Headfixed setup for reaching and treadmill activity)

<img src="{{ site.baseurl }}/images/reaching.gif" alt="drawing" width="400" height="400"/>

As a follow-up to the ReachOut project we have developed its full ***headfixed*** counterpart, which we ended up never using. 
But as a bonus here we provide all the details of this side project in a good spirit of open science. We have added a
corresponding section to the original GitHub repository (**/Headfixed_Setup**) and all the contents are described here. Feel free
to hit us with any questions that might save you the trial-and-error process we went through.


## Project overview

The ***contents*** of the project folder in GitHub repository:
 - **WaterDelivery**
	- /Water_delivery_3d_models/ (all the models you need for the water delivery system: DIY pump and actuator)
	- /Water_delivery_code/ (various Arduino programs corresponding to different protocols)
	- /Water_delivery_pictures/ (pictures showing the overview of the system, also Materials Source table) 
	- /Water_delivery_tests/ (pictures and tests for the system)
 - **Headplate designs** (the designs for the headplates for head fixation, modified after A.Ribic [^1] lab)

The ***following sections*** lead you through different parts of the setup: 
 - Hardware, 
 - Electrical Components, 
 - Code to run the protocol, 
 - Device testing and animal training  


<img src="{{ site.baseurl }}/images/Headfixed1.png" alt="drawing" width="400" height="400"/>
 
This setup allows you to study cortical circuitry of the reaching movement in more detail using 2-photon microscopy or
other methods requiring more stability than you can achieve with freely moving behavior. It is heavily inspired by the one from 
Galinanes 2018 article [^2] and Carlsen 2022 article [^3] so for further details we point you to their work. 
In short, animal is fixed by the head with only the forepaws freely moving, and the water reinforcement is delivered through 
a blunt syringe needle within reaching distance. The distance is gradually increased during training
and the position of the needle changed to shape the proper directional response. 


## About the project

ReachOut is maintained &copy; 2022-{{ "now" | date: "%Y" }} by [Daniil Berezhnoi](https://www.linkedin.com/in/daniil-berezhnoi-a4039844/).
All the materials are OpenSource and Authors would be happy to help you with any questions on the code.




----

[^1]: [Headplate designs from the Ribic lab](https://ribicneurolab.com/headplate-designs)
[^2]: [Directional Reaching for Water as a Cortex-Dependent Behavioral Framework for Mice](https://pubmed.ncbi.nlm.nih.gov/29514103/)
[^3]: [Versatile treadmill system for measuring locomotion and neural activity in head-fixed mice](https://www.sciencedirect.com/science/article/pii/S2666166722005810)
