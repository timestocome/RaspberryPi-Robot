# Machine Learning on a Raspberry Pi

Project goal is to set up a robot car with a camera to interact with household members and pets and provide home security. This is where it all started, though it hasn't been nearly as easy as he makes it sound ( https://www.oreilly.com/learning/how-to-build-a-robot-that-sees-with-100-and-tensorflow )

- autonomous motion tracking and following
- autonomously recognize human and pet residents
- interactive chat
- send notifications of problems when humans not in the house
- autonomous animated face ( eyes, ? ) 

Progress:
- Robot learns to avoid obstacles using Reinforcement learning
- Robot can ID both the cats from photos it takes


Pending:
- waiting on sturdier camera and sonic sensor mounting before adding cat tracking
- waiting on Google AIY voice kit to see if it'll work for chat, notifications


Next To do:
- track cats
- feedback ? face, text, some type of visual output
- loop to run obstacle avoidance, cat id, tracking, feedback all together


SoftwareSetup.txt has links to any software I use along with any instructions needed to set it up

HardwareSetup.txt has links to detailed directions to get hardware running

PartsList.txt has parts listed as I acquire and add them

test*.py are simple scripts to make sure hardware is on and connecting to the RaspberryPi

Test hardware scripts contains very simple Python scripts to separately test robot hardware

Obstacle Avoidance uses reinforcement learning to train each robot wander around while avoiding obstacles

Tracking Scripts will store OpenCV scripts used to ID and follow or avoid humans and pets

Utility scripts are misc data cleaning and other random scripts that are necessary but not part of main project

Object Detection contains instructions and a script to do object detection on the Pi - WIP still needs a script to take photos every x time steps and act on objects it recognizes ( ie follow a human, run from a cat... )


Photos and movies
https://photos.app.goo.gl/OZ2WZesJWuyISXQD3

