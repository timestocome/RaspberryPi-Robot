# http://github.com/timestocome


# train a raspberry pi robot to wander the house while avoiding obstacles
# and looking for cats
# 2WD robot with a servo to control steering



import numpy as np
#from pathlib import Path
import os.path

from FindCats import FindCats
from FindDistance import FindDistance
from MoveClearRobot import MoveRobot

import datetime



# led light for cat
import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BOARD)
gpio.setup(12, gpio.OUT)



# test cat found led
gpio.output(12, gpio.HIGH)
time.sleep(5)
gpio.output(12, gpio.LOW)




'''

#################################################################################################
# utilities
#################################################################################################

def save_state(s):
    np.save('state.npy', s)
    
    
def load_state():
    
    if os.path.isfile('state.npy'):
    
        state = np.load('state.npy')
        return state.reshape((n_cat, n_distance, n_actions))
        
    else:   
        return np.zeros((n_cat, n_distance, n_actions))
    

    



################################################################################################
# init
################################################################################################

# init
cat_finder = FindCats()
min_cat = cat_finder.min_cat
merlin = cat_finder.merlin
no_cat = cat_finder.no_cat
n_cat = 3


distance_finder = FindDistance()
max_distance = distance_finder.max_distance
n_distance = max_distance + 1


moveRobot = MoveRobot()
actions = moveRobot.actions
n_actions = len(actions)


# possible states
# rows min, merlin, no cat
# columns are obstacle distance 0 - max distance +1 because arrays start at zero
#state = np.zeros((n_cat, n_distance, n_actions))

# load saved state if it exists, else init to zeros
state = load_state()

# store moves here until we get a reward 
states_visited = []



# arrays are much easier and faster to work with than trees, so set up tree as arrays
# tree needs each state, number of times visted and reward
state_rewards = np.zeros((n_cat, n_distance))
action_rewards = np.zeros((n_cat, n_distance, n_actions))


# fill in rewards for various states
state_rewards[min_cat,:] = 10        # found min
state_rewards[merlin, :] = 10        # found merlin


# too close to an obstacle
buffer_distance = 12                # cm
state_rewards[:, 0:buffer_distance] = -3


# distance covered
distance_traveled = 0



# robot environment
def get_distance():
    # returns distance 1-50
    distance = distance_finder.get_distance()
    
    if distance < 1: distance = 1
    return int(distance)



def get_cat():
    # returns 0 for Min, 1 for Merlin, 2 for no cat
    cat = cat_finder.is_cat()
    
    found = np.argmax([cat[0][1], cat[1][1], cat[2][1]])
    
        # turns on led when cat in sight, off otherwise
    if found == no_cat:
        gpio.output(12, gpio.LOW)
    else:
        gpio.output(12, gpio.HIGH)
    
    return found




def update_values(r, dt, lr):

    # use number of steps required to get reward as lr
    # over many passes this will give actions closer to reward higher reward/penalty
    
    reward_per_state = (r + dt)/lr
    
    for i in range(len(states_visited)):
        c = states_visited[i][0]
        d = states_visited[i][1]
        a = states_visited[i][2]
        
        action_rewards[c][d][a] += reward_per_state
        #print(action_rewards[c][d][a])
    
    
    
    
    

# robot moves and reward is returned
# robot receives reward for moving with out hitting obstacles
# gets a large reward for catching either cat in its camera view
# penatly for getting too close to obstacles
# scale rewards from -1 to 1

def move(action, distance, cat):

    global states_visited
    global distance_traveled

    reward = state_rewards[cat, distance]
    states_visited.append((cat, distance, action))
    
    
    if reward != 0:
        update_values(reward, distance_traveled, len(states_visited))
        states_visited = []
        distance_traveled = 0
        
    #self.actions = ['center_forward', 'right_forward', 'left_forward', 
    #        'center_reverse', 'right_reverse', 'left_reverse']

            
    if action == 0:         
        moveRobot.center_forward()
    elif action == 1:            
        moveRobot.right_forward()
    elif action == 2:      
        moveRobot.left_forward()
    elif action == 3:       
        moveRobot.center_reverse()
    elif action == 4:
        moveRobot.right_reverse()
    elif action == 5:
        moveRobot.left_reverse()
    
    if action < 3: distance_traveled += 1
    else: distance_traveled -= 2
    # useful for adjusting rewards as needed
    #print("state %d %d,  action %d,  reward %d epsilon %lf" % (distance, cat, action, reward, epsilon))


    return reward 






###############################################################################
    # training
###############################################################################

random_choice = .9
for i in range(1000):
#while(True):
    
    current_distance = get_distance()
    current_cat = get_cat()
    
    #print('distance %d cat %d' % (current_distance, current_cat))
    
    action = np.random.randint(n_actions)
    
    if np.random.rand() > random_choice:
        action = np.argmax(action_rewards[current_cat, current_distance, :])
        
    if random_choice > .1:
        random_choice *= .99
        
    move(action, current_distance, current_cat)

    if i%50 == 0:
        save_state(action_rewards)




###############################################################################
# clean shut down of hardware
###############################################################################
def cleanup():
        
     cat_finder.cleanup()
     distance_finder.cleanup()
     moveRobot.cleanup()






###############################################################################
# wrap things up
###############################################################################

save_state(action_rewards)
cleanup()


# print actions by distance by cat
z = np.zeros(n_distance)
for i in range(n_distance-1):
    for j in range(n_cat-1):
        if j == 0:   # no cat
            z[i] = np.argmax(action_rewards[i, j, :])
            
            
            
for i in range(len(z)):
    a = int(z[i])
    print(i, actions[a])

'''

