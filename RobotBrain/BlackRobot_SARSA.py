# http://github.com/timestocome


# train a raspberry pi robot to wander the house while avoiding obstacles
# and looking for cats

# this robot uses wheels for steering
# 4 wheel drive with separate controls each side


# change from off policy learning in first try
# adapted from https://morvanzhou.github.io/tutorials/


import numpy as np
from pathlib import Path



from FindCats import FindCats
from FindDistance import FindDistance
from MoveBlackRobot import MoveRobot

import datetime



# init
cat_finder = FindCats()
min_cat = cat_finder.min_cat
merlin = cat_finder.merlin
no_cat = cat_finder.no_cat

distance_finder = FindDistance()
max_distance = distance_finder.max_distance


moveRobot = MoveRobot()
actions = moveRobot.actions

qTable = 'qTable.npy'
epsilon = 1.0


# robot environment
def get_distance():
    # returns distance 1-50
    distance = distance_finder.get_distance()
    return int(distance)


def get_cat():
    # returns 0 for Min, 1 for Merlin, 2 for no cat
    cat = cat_finder.is_cat()
    return np.argmax([cat[0][1], cat[1][1], cat[2][1]])



# robot actions   
def move(action, distance, cat):

    reward = 0.001
    buffer_distance = 12.
                
    # penalty for being too closes to an obstacle
    if distance <=buffer_distance:   # buffer zone in cm
        reward -= buffer_distance 
        
            
    # reward for locating cat
    if cat == merlin:
        reward += 10
    if cat == min_cat:
        reward += 10
            
            
    # get reward for moving or robot will eventually park itself in middel of the room
    if action == 0:         
        moveRobot.forward()
        reward += 3       # reward robot for covering distance
    elif action == 1:       
        moveRobot.reverse()
        reward += 0.0      # discourage reverse, no sensors on back of robot
    elif action == 2:       
        moveRobot.hard_left()
        reward += 1
    elif action == 3:      
        moveRobot.hard_right()
        reward += 1
    '''
    elif action == 4:       
        moveRobot.turn_left()
        reward += 1
    elif action == 5:       
        moveRobot.turn_right()
        reward += 1
    '''


    #print("state %d %d,  action %d,  reward %d" % (distance, cat, action, reward))

    return reward 






###############################################################################
    # q learning happens here
###############################################################################

n_distance_states = max_distance + 1
n_cat_states = 3
n_actions = len(actions)


# training vars
lr = 0.01               # learning rate
gamma = 0.9             # memory (gamma^n_steps)
n_loops = 500           # training loops to perform



# init new table
def init_q_table(n_distance_states, n_cat_states, n_actions):
    
    table = np.zeros((n_distance_states, n_cat_states, n_actions))
    return table



# load saved table from file
def load_q_table():
    
    t_1d = np.load(qTable)
    table = t_1d.reshape(n_distance_states, n_cat_states, n_actions)
    
    return table



# write table to disk
def save_q_table(t):
    
    t_1d = t.reshape(n_distance_states * n_cat_states * n_actions, 1)
    np.save(qTable, t_1d)
    


def choose_action(d, c, q_table):

    global epsilon
    state_actions = q_table[d][c][:]

    # random move or no data recorded for this state yet
    if (np.random.uniform() < epsilon) or (np.sum(state_actions) == 0):
        
        action_chose = np.random.randint(n_actions)
    
        # decrease random moves over time to a minimum of 10%
        if epsilon >  0.1:
            epsilon *= 0.9
        
    else:
        action_chose = state_actions.argmax()
    
    return action_chose





def rl():
    
    # init new table if none found
    saved_table = Path(qTable)
    if saved_table.is_file():
        q_table = load_q_table()
    else:
        q_table = init_q_table(n_distance_states, n_cat_states, n_actions)

        
    n_steps = 0
    
    
    # prime loop with first action
    d = get_distance()
    c = get_cat()
    a = choose_action(d, c, q_table)
    start_time = datetime.datetime.now()
    
    while n_steps < n_loops:

        # move robot and update state
        reward = move(a, d, c)
        d_next = get_distance()
        c_next = get_cat()
        
        
        # chose action based on next observation
        a_ = choose_action(d_next, c_next, q_table)
        
        # SARSA learning
        s_target = reward + gamma + q_table[d_next][c_next][a_]
        
        
        # what robot thought would happen next
        s_predict = q_table[d][c][a]
        
       
        # update q_table to reflect new knowledge
        q_table[d][c][a] += lr * (s_target - s_predict)
        
        
        # update state for next loop
        d = d_next
        c = c_next
        a = a_
        
        n_steps += 1
        
        # save data every 100 steps incase of failure
        if n_steps % 100 == 0:
            save_q_table(q_table)
            print(datetime.datetime.now() - start_time)
            start_time = datetime.datetime.now()
        
    return q_table




###############################################################################
# clean shut down of hardware
###############################################################################
def cleanup():
        
     cat_finder.cleanup()
     distance_finder.cleanup()
     moveRobot.cleanup()






###############################################################################
# run code
###############################################################################

q_table = rl()

cleanup()


'''
#q_table = load_q_table()
print('--------------------------------')
print('Final Q Table')

for i in range(n_distance_states):
    for j in range(n_cat_states):
        print('distance %d, cat %d' %(i, j))
        print('action values', s_table[i, j, :])
        
'''


# print actions by distance by cat
z = np.zeros(n_distance_states)
for i in range(n_distance_states):
    for j in range(n_cat_states):
        if j == 2:   # no cat
            z[i] = np.argmax(q_table[i, j, :])
            
print('distance, action')
for i in range(len(z)):
    a = int(z[i])
    print(i, actions[a])
    
    

