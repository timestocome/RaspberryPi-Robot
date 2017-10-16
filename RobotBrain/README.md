# Main Robot Loop  (WIP)

This section will contain the reinforcement network that allows the robot to respond to the environment



The robot's actions and input from sensors have been broken into classes


<strike>The robot loop will be built on the TF one that the robot uses to avoid obstacles but will 
use multiple sensor inputs not just distance.</strike>

I gave up on the tf.contrib.slim library. The contrib libraries all work until you make the slightest change.


Current status:

Main loop reads distance to nearest obstacle and checks to see if cat1 or cat2 or no cat is in view.


Working on:

I still haven't gotten the RL algorithm to work with multiple rewards


Useful information:

https://github.com/MorvanZhou/Reinforcement-learning-with-tensorflow

https://sites.google.com/view/deep-rl-bootcamp/lectures


ToDo:

- speed things up 
- get RL algorithm to work on multiple targets (don't hit things, find cats)


The robot is going to have to be a quick learner to survive Merlin
<img src="https://github.com/timestocome/RaspberryPi-Robot/blob/master/RobotBrain/MerlinRobot.jpg"/>
