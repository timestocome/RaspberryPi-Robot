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
- The SARSA algorithm trains significantly faster than the original


Useful information:

https://github.com/MorvanZhou/Reinforcement-learning-with-tensorflow

https://sites.google.com/view/deep-rl-bootcamp/lectures



The robot is going to have to be a quick learner to survive Merlin
<img src="https://github.com/timestocome/RaspberryPi-Robot/blob/master/RobotBrain/MerlinRobot.jpg"/>
