# http://github.com/timestocome


# train a raspberry pi robot to wander the house while avoiding obstacles
# and looking for cats


# this robot uses wheels for steering
# 4 wheel drive with separate controls each side


import tensorflow as tf
import tensorflow.contrib.slim as slim
import numpy as np

import time
from time import sleep




######################################################################
# sensor input
######################################################################

from FindCats import FindCats
from FindDistance import FindDistance


cat_finder = FindCats()
min_cat = cat_finder.min_cat
merlin = cat_finder.merlin
no_cat = cat_finder.no_cat


distance_finder = FindDistance()
max_distance = distance_finder.max_distance
min_distance = distance_finder.min_distance


def get_distance():
    # returns distance 1-100
    distance = distance_finder.get_distance()
    return int(distance)


def get_cat():
    # returns 0 for Min, 1 for Merlin, 2 for no cat
    cat = cat_finder.is_cat()
    return np.argmax([cat[0][1], cat[1][1], cat[2][1]])


'''
# test
print("distance", get_distance())
print("min, max distance", min_distance, max_distance)

print('cat', get_cat())
print('min, merlin, no cat', min_cat, merlin, no_cat)

'''

'''
# cleanup
cat_finder.cleanup()
distance_finder.cleanup()
...



##########################################################################
# move robot
##########################################################################
from MoveBlackRobot import MoveRobot

move_robot = MoveRobot()

'''
# test
print("actions", move_robot.actions)

# cleanup
move_robot.cleanup()
'''


#---- you are here ------------------------------------------
'''

##########################################################################
# network
##########################################################################

class world():

    def __init__(self):

        self.state = get_state()
        self.states = np.zeros(max_distance + 1)
        self.num_states = len(self.states)
        self.num_actions = len(actions)

        print('state', self.state)
        print('num actions', self.num_actions)

    def move(self, action):

        state = get_state()
        reward = 0
        self.states[state] += 1
        
        # penatly for being too closes to an obstacle
        if state <= 2.54 * 5.:   # buffer zone converted to cm
            reward = -3.0

        if action == 0:         
            forward()
            reward = 1
        elif action == 1:       
            reverse()
            reward = 1
        elif action == 2:       
            turn_left()
            reward = 1
        elif action == 3:      
            turn_right()
            reward = 1
        elif action == 4:       
            hard_right()
            reward = 1
        elif action == 5:       
            hard_left()
            reward = 1
        
        print("state %d,  action %d,  reward %d" % (state, action, reward))

        return reward






class agent():

    def __init__(self, lr, s_size, a_size):

        self.state_in = tf.placeholder(shape=[1], dtype=tf.int32)
        state_in_OH = slim.one_hot_encoding(self.state_in, s_size)

        output = slim.fully_connected(state_in_OH, 
                                        a_size, 
                                        biases_initializer=None, 
                                        activation_fn=tf.nn.sigmoid,
                                        weights_initializer=tf.ones_initializer())
        self.output = tf.reshape(output, [-1])
        
        self.chosen_action = tf.argmax(self.output, 0)
        self.reward_holder = tf.placeholder(shape=[1], dtype=tf.float32)
        self.action_holder = tf.placeholder(shape=[1], dtype=tf.int32)
        
        self.responsible_weight = tf.slice(self.output, self.action_holder, [1])

        self.loss = -(tf.log(self.responsible_weight) * self.reward_holder)
        optimizer = tf.train.GradientDescentOptimizer(learning_rate=lr)
        self.update = optimizer.minimize(self.loss)



tf.reset_default_graph()

world = world()
robot = agent(lr=0.001, s_size = world.num_states, a_size = world.num_actions)
weights = tf.trainable_variables()[0]
e = 0.9     # % time random action chosen, decreases over time 

init = tf.global_variables_initializer()

total_episodes = 1000 + 1 # up this to loop forever once everything works
total_reward = np.zeros([world.num_states, world.num_actions])

# numpy was resetting? idk heavily favoring 0, this is a hack around it
random_actions = np.random.random_integers(0, world.num_actions-1, total_episodes)


# used for debugging - remove in final version to speed things up
distance = 0. # estimate how far robot has traveled
choices = np.zeros(len(actions))


with tf.Session() as sess:
    sess.run(init)
    i = 0
    saver = tf.train.Saver()
    

    #saver.restore(sess, 'save/model.ckpt')
    

    while i < total_episodes:
        s = get_state()
        e *= 0.95        # reduce random searching over time
        e = max(e, .2)   # keep epislon over 10%

        if np.random.rand(1) < e:
            action = random_actions[i]
            print('******      random action', action)
        else:
            action = sess.run(robot.chosen_action, feed_dict={robot.state_in:[s]})

        reward = world.move(action)
        
        feed_dict = { robot.reward_holder: [reward], robot.action_holder: [action], robot.state_in: [s]  }
        
        _, ww = sess.run([robot.update, weights], feed_dict = feed_dict)
        total_reward[s, action] += reward
        
        # used for debugging - comment out in final
        distance += reward
        choices[action] += 1

        if i % 1 == 0:
            print("Random tries: ", e)
            print("Distance: ", distance)
            print("Choices: ", choices)
        
        # save weights
        if i % 100 == 0:
            save_path = saver.save(sess, 'save/model.ckpt')
            
        i += 1


cleanup()
'''
