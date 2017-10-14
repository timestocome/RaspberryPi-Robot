# http://github.com/timestocome


# train a raspberry pi robot to wander the house while avoiding obstacles
# and looking for cats


# this robot uses wheels for steering
# 4 wheel drive with separate controls each side


import tensorflow as tf
import numpy as np

from FindCats import FindCats
from FindDistance import FindDistance

from MoveBlackRobot import MoveRobot






##########################################################################
# network
##########################################################################

class World():

    def __init__(self):
        
        self.cat_finder = FindCats()
        self.min_cat = self.cat_finder.min_cat
        self.merlin = self.cat_finder.merlin
        self.no_cat = self.cat_finder.no_cat

        self.distance_finder = FindDistance()
        self.max_distance = self.distance_finder.max_distance
        self.min_distance = self.distance_finder.min_distance

        self.n_distance_states = self.max_distance + 2
        self.n_cat_states = 3
        self.n_states = self.n_distance_states + self.n_cat_states
        self.states = np.zeros(self.n_states)

        self.moveRobot = MoveRobot()
        self.actions = self.moveRobot.actions
        self.n_actions = len(self.actions)




    def get_distance(self):
        # returns distance 1-100
        distance = self.distance_finder.get_distance()
        return int(distance)


    def get_cat(self):
        # returns 0 for Min, 1 for Merlin, 2 for no cat
        cat = self.cat_finder.is_cat()
        return np.argmax([cat[0][1], cat[1][1], cat[2][1]])


    def get_state(self):    
        return self.get_distance(), self.get_cat()
    
    def convert_state_to_one_hot(self, d, c):
        
        state_array = np.zeros(world.n_states)
        state_array[d] = 1.
        state_array[self.n_states - c] = 1.
       
        return np.reshape(state_array, [1, world.n_states]) 
         
         
    def move(self, action, distance, cat):

        reward = 0
                

        # penalty for being too closes to an obstacle
        if distance <= 15:   # buffer zone in cm
            reward = -4.0
            
        # reward for locating cat
        if cat == self.merlin:
            reward += 10
        if cat == self.min_cat:
            reward += 10
            
            
        # otherwise get reward for moving 
        if action == 0:         
            self.moveRobot.forward()
            reward += 1
        elif action == 1:       
            self.moveRobot.reverse()
            reward += 1
        elif action == 2:       
            self.moveRobot.turn_left()
            reward += 1
        elif action == 3:      
            self.moveRobot.turn_right()
            reward += 1
        elif action == 4:       
            self.moveRobot.hard_left()
            reward += 1
        elif action == 5:       
            self.moveRobot.hard_right()
            reward += 1


        print("state %d %d,  action %d,  reward %d" % (distance, cat, action, reward))

        return reward




    def cleanup(self):
        
        self.cat_finder.cleanup()
        self.distance_finder.cleanup()
        self.moveRobot.cleanup()






##########################################################################
# network
##########################################################################

class Robot():

    def __init__(self, lr, s_size, a_size, n_hidden=32):
                
        
        self.state_in = tf.placeholder(tf.float32, [None, s_size])
        
        W1 = tf.Variable(tf.random_normal([s_size, n_hidden]))
        b1 = tf.Variable(tf.constant(0.1, shape=[n_hidden]))
        h1 = tf.nn.sigmoid(tf.matmul(self.state_in, W1) + b1)
        
        W2 = tf.Variable(tf.random_normal([n_hidden, a_size]))
        b2 = tf.Variable(tf.constant(0.1, shape=[a_size]))
        output = tf.nn.softmax(tf.matmul(h1, W2) + b2)        
        
        
        self.output = tf.reshape(output, [-1])
        
        
        self.chosen_action = tf.argmax(self.output, 0)
        self.reward_holder = tf.placeholder(shape=[1], dtype=tf.float32)
        self.action_holder = tf.placeholder(shape=[1], dtype=tf.int32)
        
        self.responsible_weight = tf.slice(self.output, self.action_holder, [1])

        self.loss = -(tf.log(self.responsible_weight) * self.reward_holder)
        optimizer = tf.train.GradientDescentOptimizer(learning_rate=lr)
        self.update = optimizer.minimize(self.loss)

        


tf.reset_default_graph()

world = World()
robot = Robot(lr=0.001, s_size = world.n_states, a_size = world.n_actions)
weights = tf.trainable_variables()[0]
e = 0.9     # % time random action chosen, decreases over time 

init = tf.global_variables_initializer()

total_episodes = 1000 + 1 # up this to loop forever once everything works
total_reward = np.zeros([world.n_states, world.n_actions])

# numpy was resetting? idk heavily favoring 0, this is a hack around it
random_actions = np.random.random_integers(0, world.n_actions-1, total_episodes)
z = 0    # random number pointer

# used for debugging - remove in final version to speed things up
distance = 0. # estimate how far robot has traveled
choices = np.zeros(world.n_actions)


with tf.Session() as sess:
    sess.run(init)
    i = 0
    saver = tf.train.Saver()
    

    #saver.restore(sess, 'save/model.ckpt')
    

    while i < total_episodes:
        
        s = world.get_state()
        state_in_OH = world.convert_state_to_one_hot(s[0], s[1])
        
        e *= 0.95        # reduce random searching over time
        e = max(e, .2)   # keep epislon over 10%

        if np.random.rand(1) < e:
            action = random_actions[z]
            z += 1
            print('******      random action', action)
        else:
            action = sess.run(robot.chosen_action, feed_dict={robot.state_in:state_in_OH})

        reward = world.move(action, s[0], s[1])
        
        feed_dict = { robot.reward_holder: [reward], robot.action_holder: [action], robot.state_in: state_in_OH}  
        
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
        

world.cleanup()

