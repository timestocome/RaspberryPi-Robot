# http://github.com/timestocome


# train a raspberry pi robot to wander the house while avoiding obstacles
# and looking for cats

# this robot uses wheels for steering
# 4 wheel drive with separate controls each side


import numpy as np
from pathlib import Path



from FindCats import FindCats
from FindDistance import FindDistance
from MoveBlackRobot import MoveRobot

#import datetime




# init
cat_finder = FindCats()
min_cat = cat_finder.min_cat
merlin = cat_finder.merlin
no_cat = cat_finder.no_cat

distance_finder = FindDistance()
max_distance = distance_finder.max_distance


moveRobot = MoveRobot()
actions = moveRobot.actions




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
    min_distance = 12.
                
    # penalty for being too closes to an obstacle
    if distance <= min_distance:   # buffer zone in cm
        reward -= min_distance / distance
            
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
        moveRobot.turn_left()
        reward += 1
    elif action == 3:      
        moveRobot.turn_right()
        reward += 1
    elif action == 4:       
        moveRobot.hard_left()
        reward += 1
    elif action == 5:       
        moveRobot.hard_right()
        reward += 1


    #print("state %d %d,  action %d,  reward %d" % (distance, cat, action, reward))

    return reward 






###############################################################################
    # q learning happens here
###############################################################################

n_distance_states = max_distance + 1
n_cat_states = 3
n_actions = len(actions)

# training vars
lr = 0.1            # learning rate
gamma = 0.9         # memory (gamma^n_steps)
n_loops = 500       # training loops to perform




# new q-table
def init_q_table(n_distance_states, n_cat_states, n_actions):
    
    table = np.zeros((n_distance_states, n_cat_states, n_actions))
    return table



# load saved q table
def load_q_table():
    
    t_1d = np.load('qTable.npy')
    table = t_1d.reshape(n_distance_states, n_cat_states, n_actions)
    
    return table




def save_q_table(t):
    
    t_1d = t.reshape(n_distance_states * n_cat_states * n_actions, 1)
    np.save('qTable.npy', t_1d)
    


def choose_action(d, c, q_table, epsilon):

    state_actions = q_table[d][c][:]

    # random move or no data recorded for this state yet
    if (np.random.uniform() < epsilon) or (np.sum(state_actions) == 0):
        action_chose = np.random.randint(n_actions)
        #epsilon *= .99         # lots of random searching when table is zero 
        if epsilon >  0.1: epsilon *= 0.8
    else:
        action_chose = state_actions.argmax()
    
    return action_chose


def rl():
    
    # init new table if none found
    saved_table = Path('qTable.npy')
    if saved_table.is_file():
        q_table = load_q_table()
    else:
        q_table = init_q_table(n_distance_states, n_cat_states, n_actions)

        
    epsilon = 1.0       # random choice % decreases over time

    n_steps = 0
    d = get_distance()
    c = get_cat()
    
    
    while n_steps < n_loops:
        #start = datetime.datetime.now()
        #print('step %d epsilon %lf' %(n_steps, epsilon))

        # chose action and move robot
        a = choose_action(d, c, q_table, epsilon)
        reward = move(a, d, c)
        
        # update state
        d_next = get_distance()
        c_next = get_cat()
        
        # what robot thought would happen next
        q_predict = q_table[d][c][a]
        
        # what actually happened
        q_target = reward + gamma * q_table[d][c][a]
        
        # update q_table
        q_table[d][c][a] += lr * (q_target - q_predict)
        
        # wrap up
        d = d_next
        c = c_next
        
        n_steps += 1
        
        # save data
        if n_steps % 100 == 0:
            save_q_table(q_table)
        
        #print(datetime.datetime.now() - start)
        
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
        print('action values', q_table[i, j, :])
        
'''

#save_q_table()
#load_q_table()
