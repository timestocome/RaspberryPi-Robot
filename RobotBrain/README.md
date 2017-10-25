# Main Robot Loop  (WIP)

This section will contain the reinforcement network that allows the robot to respond to the environment

Current status:

Main loop reads distance to nearest obstacle and checks to see if cat1 or cat2 or no cat is in view.
Both robots are using a simplified QLearning Value algorithm to learn.

If the files are reloaded each time the learning should improve with each run


To do:
- reducing the number of states so the robots will train faster
- speed things up, ~~cat id is still very slow~~ fixed, now steady at ~2 FPS
- explore other RL algorithms

WIP:
- The SARSA algorithm creates a timid robot:
-- What the robot learned in 500 loops:
Timid robot being trained to hunt cats and avoid obstacles using RL Sarsa 

- distance(cm) action if no cat
- 1 right
- 2 right
- 14 hard_right
- 15 left
- 17 left
- 24 hard_left
- 25 right
- 28 hard_left
- 29 right
- 30 left
- 33 hard_left
- 38 hard_right
- 41 right
- 42 hard_right
- 44 right
- 46 hard_right
- 48 left
- 49 right
- 53 left
- 54 hard_right
- 55 hard_left
- 56 hard_right
- 61 left
- 63 right
- 67 hard_right
- 68 left
- 73 left
- 74 hard_right
- 75 right
- 76 hard_right
- 78 left
- 80 hard_left
- 83 hard_left
- 87 right
- 93 hard_left
- 96 hard_right
- 97 right

Useful information:

https://github.com/MorvanZhou/Reinforcement-learning-with-tensorflow

https://sites.google.com/view/deep-rl-bootcamp/lectures



The robot is going to have to be a quick learner to survive Merlin
<img src="https://github.com/timestocome/RaspberryPi-Robot/blob/master/RobotBrain/MerlinRobot.jpg"/>
