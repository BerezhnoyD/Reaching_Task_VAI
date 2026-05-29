---
layout: page
title: Headfixed software
parent: Bonus Headfixed setup
nav_order: 8
description: "This is a description of software and testing for headfixed setup"
---


# Testing the setup

Initially we have tried to follow the protocol from the Galinanes 2018 article [^1], which includes
gradual shaping of the spontaneous reaching/licking response to water in water-deprived animals. For us
the success of the protocol heavily depended on the level of animal handling (stress response to head restraint),
motivation (water deprivation) and individual differences and the % of animals learned was never more than 50.
Here is the schematic of our initial learning protocol.
 
<img src="{{ site.baseurl }}/images/Training1.png" alt="drawing" width="400" height="400"/> 


Hence, we had to switch to another way of evoking the reaching response that depended less on the internal animal state
and other variables. We actually found the "Pavlovian" way (relying on the innate reaction) to induce reaching more consistent in our hands. 
The innate paw reaction, e.g. grooming/washing response, was consistently induced by touching animal whiskers with the water droplet being delivered.
This reaction, thought initially far from the purposeful reaching for water, can be transformed into a skilled response by the same shaping approach
as was employed in Galinanes 2018 article [^1]. Hence our final protocol looked like this.

<img src="{{ site.baseurl }}/images/Training2.png" alt="drawing" width="400" height="400"/> 


## Videos showing different optimization steps 
In the following videos you can see various stages of the protocol and device testing that may give you insights on how to implement the protocol. 
***Note*** that before starting the training protocol animal should be handled and accustomed to the experimenter, to water deprivation, to being restrained in the 
behavioral setup, and licking water from the syringe tip. The device and the protocol should be extensively tested before starting any actual animal work.

First step is to test the water delivery system and determine the optimal ~20-50mkl size of the water droplet before starting any animal work (adjusting the number
of stepper steps and the syringe size mounted in the pump)
<iframe width="600" height="600" src="{{ site.baseurl }}/images/Water1.mp4" frameborder="0" allowfullscreen></iframe>

The goal of the second step is to determine the optimal distance from the snout to the syringe tip (~5mm) to induce the licking and reaching responses
(generally the key is to touch the whiskers at first as it induces the grooming/washing response, and then gradually increase the distance). 
<iframe width="600" height="600" src="{{ site.baseurl }}/images/Water2.mp4" frameborder="0" allowfullscreen></iframe>

The actual training should be performed only when the animal has a stable reaching response and is devoted to pairing up conditioned stimulus (buzzer,
here paired with an LED for illustrative purposes) with the response.
<iframe width="600" height="600" src="{{ site.baseurl }}/images/Water3.mp4" frameborder="0" allowfullscreen></iframe>


----

[^1]: [Directional Reaching for Water as a Cortex-Dependent Behavioral Framework for Mice](https://pubmed.ncbi.nlm.nih.gov/29514103/)