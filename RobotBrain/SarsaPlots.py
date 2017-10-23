# http://github.com/timestocome


# train a raspberry pi robot to wander the house while avoiding obstacles
# and looking for cats

# this robot uses wheels for steering
# 4 wheel drive with separate controls each side


# change from off policy learning in first try
# adapted from https://morvanzhou.github.io/tutorials/


import numpy as np



###############################################################################
    # q learning happens here
###############################################################################
actions = ['forward', 'reverse', 'turn_left', 'turn_right', 'hard_left', 'hard_right']
n_distance_states = 100 + 1
n_cat_states = 3
n_actions = 6

qTable = 'qTable.npy'



# load saved table from file
def load_q_table():
    
    t_1d = np.load(qTable)
    table = t_1d.reshape(n_distance_states, n_cat_states, n_actions)
    
    return table





q_table = load_q_table()
print('--------------------------------')
print('Final Q Table')

for i in range(n_distance_states):
    for j in range(n_cat_states):
        print('distance %d, cat %d' %(i, j))
        print('action values', q_table[i, j, :])
        



# print actions by distance no cat
z = np.zeros(n_distance_states)
for i in range(n_distance_states):
    for j in range(n_cat_states):
        if j == 2:  # no cat
            z[i] = np.argmax(q_table[i, j, :])
            
print('---------  distance/ action -------------')
for i in range(len(z)):
    a = int(z[i])
    print(i, actions[a])