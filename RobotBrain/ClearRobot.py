# http://github.com/timestocome


# train a raspberry pi robot to wander the house while avoiding obstacles
# this robot has a servo for steering ~90' range
# rear wheel drive with separate controls for the wheels 



import numpy as np
import FindCats
import FindDistance
import MoveClearRobot 







# init
cat_finder = FindCats.FindCats()
min_cat = cat_finder.min_cat
merlin = cat_finder.merlin
no_cat = cat_finder.no_cat

distance_finder = FindDistance.FindDistance()
max_distance = distance_finder.max_distance


moveRobot = MoveClearRobot.MoveRobot()
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





def move(action, distance, cat):

    reward = 0
    min_distance = 12.

    # penalty for being too closes to an obstacle
    if distance <= min_distance:   # buffer zone in cm
        reward -= min_distance / distance

    
    # reward for locating cat
    if cat == merlin:
        reward += 10
    if cat == min_cat:
        reward += 10
        

      
    # otherwise get reward for moving 
    if action == 0:         
        moveRobot.center_forward()
        reward += 3
    elif action == 1:       
        moveRobot.hard_right_forward()
        reward += 1
    elif action == 2:       
        moveRobot.right_forward()
        reward += 2
    elif action == 3:      
        moveRobot.left_forward()
        reward += 2
    elif action == 4:       
        moveRobot.hard_left_forward()
        reward += 1
    elif action == 5:       
        moveRobot.center_reverse()
        reward += 0
    elif action == 6:
        moveRobot.hard_right_reverse()
        reward += 0
    elif action == 7:      
        moveRobot.right_reverse()
        reward += 0
    elif action == 8:       
        moveRobot.left_reverse()
        reward += 0
    elif action == 9:       
        moveRobot.hard_left_reverse()
        reward += 0
       


    print("distance %d,  cat %d, action %d,  reward %d" % (distance, cat, action, reward))

    return reward




def cleanup():
        
    cat_finder.cleanup()
    distance_finder.cleanup()
    move_robot.cleanup()




###############################################################################
    # q learning happens here
###############################################################################

n_distance_states = max_distance + 1
n_cat_states = 3
n_actions = len(actions)

# training vars
lr = 0.1            # learning rate
gamma = 0.9         # memory (gamma^n_steps)
n_loops = 50       # training loops to perform




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
        epsilon *= .99
    else:
        action_chose = state_actions.argmax()
    
    return action_chose



def rl():
    
    # init new table
    q_table = init_q_table(n_distance_states, n_cat_states, n_actions)
    
    # or continue using previous data
    #q_table = load_q_table()
    
    
    epsilon = 1.0       # random choice % decreases over time

    n_steps = 0
    d = get_distance()
    c = get_cat()
    
    
    while n_steps < n_loops:
        
        print('step %d epsilon %lf' %(n_steps, epsilon))

        # chose action and move robot
        a = choose_action(d, c, q_table, epsilon)
        reward = move(action=a, distance=d, cat=c)
        
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
        if n_steps % 10 == 0:
            save_q_table(q_table)
            
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


print('--------------------------------')
print('Final Q Table')

for i in range(n_distance_states):
    for j in range(n_cat_states):
        print('distance %d, cat %d' %(i, j))
        print('action values', q_table[i, j, :])
        


save_q_table()
load_q_table()


