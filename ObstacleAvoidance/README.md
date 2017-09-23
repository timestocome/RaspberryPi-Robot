
Both robots learn to avoid obstacles using reinforcement learning in less than 1000 time steps


Training tricks:

Choose rewards that favor forward motion, heavily penalize getting close to objects

Slowly reduce random choices over time

Choose a very small state space 
--- the sensor can read 2cm - 400, reducing the far distance reduces the state machine and speeds up learning

