# Machine Learning on a Raspberry Pi Robot

Project goal is to set up an autonomous wheeled robot that can move about the house and track pets 

This is where it all started, though it hasn't been nearly as easy as he makes it sound 
( https://www.oreilly.com/learning/how-to-build-a-robot-that-sees-with-100-and-tensorflow )





Finished Parts:
- robot can ID both the cats, if a cat in photo, from photos it takes
- robot can tell how far it is from obstacles and learns to avoid them using reinforcement learning
- robot uses simple QLearning RL algorithm to avoid obstacles and interact with cats
- cat/no cat id + distance check + update RL values is running at a steady 2 FPS


Run robot on boot with out logging on

Add the following lines to the end of your .bashrc file

* if you don't cd into the directory and just run python /home/pi/directoryOfCode it won't find your .pb model

cd /home/pi/directoryOfCode

python ClearRobot.py


WIP:
- put cats to work training robots
- test other RL algorithms



Photos of robots and movies
https://photos.app.goo.gl/OZ2WZesJWuyISXQD3


![robots](https://github.com/timestocome/RaspberryPi-Robot/blob/master/robots.jpg)


Robot with clear body has a servo to turn front wheels and rear wheel drive

Robot with black body has 4 wheel drive and uses wheels to steer




