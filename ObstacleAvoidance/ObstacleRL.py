# http://github.com/timestocome



import tensorflow as tf
import tensorflow.contrib.slim as slim
import numpy as np
import RPi.GPIO as gpio
import time
from time import sleep




###############################################################################
# set up hardware
###############################################################################

gpio.setmode(gpio.BOARD)        # use pin numbers not gpio numbers


# ultrasonic sensor
trigger = 13
echo = 11

max_distance = 152    # sensor can read 400 cm we only need 5'

gpio.setup(trigger, gpio.OUT)
gpio.setup(echo, gpio.IN)


# wheels ( 2 wheel motors, front wheel drive )
reverse_left = 38
reverse_right = 33
forward_left = 40
forward_right = 35

gpio.setup(reverse_left, gpio.OUT)  
gpio.setup(forward_left, gpio.OUT)  
gpio.setup(forward_right, gpio.OUT) 
gpio.setup(reverse_right, gpio.OUT) 



##############################################################################
# load data from HC-SR204 UltraSonic distance sensor
##############################################################################

# init 
pulse_start = 0.
pulse_end = 0.
distance_from_sensor_to_car_front = 4 * 2.54


# flush sensor
gpio.output(trigger, False)
time.sleep(0.5)


# distance to obstacle in path
def get_state(sleep_time=0.1):

    # clear trigger sensor
    gpio.output(trigger, False)
    time.sleep(sleep_time)

    # send trigger pulse
    gpio.output(trigger, True)
    time.sleep(0.00001)
    gpio.output(trigger, False)

    while gpio.input(echo) == 0:
        pulse_start = time.time()

    while gpio.input(echo) == 1:
        pulse_end = time.time()

    
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 343 * 100 / 2.  # speed of sound m/s * m to cm / round trip
    
    if distance > 2 and distance < 400:         # sensor range
        distance = distance - distance_from_sensor_to_car_front

    # don't worry about things further 4'
    # this also reduces the size of the state machine
    if distance > max_distance:    
        distance = max_distance - distance_from_sensor_to_car_front

    return int(distance)





##############################################################################
# perform action
##############################################################################
actions = ['forward', 'reverse', 'turn_left', 'turn_right']


def forward(t=1.):
    
    gpio.output(forward_right, gpio.HIGH)
    gpio.output(forward_left, gpio.HIGH)
    
    sleep(t)
    gpio.output(forward_right, gpio.LOW)
    gpio.output(forward_left, gpio.LOW)
    

def turn_left(t=1.):
    gpio.output(forward_right, gpio.HIGH)
    
    sleep(t)
    gpio.output(forward_right, gpio.LOW)
    


def turn_right(t=1.):
    gpio.output(forward_left, gpio.HIGH)
    
    sleep(t)
    gpio.output(forward_left, gpio.LOW)
    


def reverse(t=1.):
    
    gpio.output(reverse_left, gpio.HIGH)
    gpio.output(reverse_right, gpio.HIGH)
    
    sleep(t)
    gpio.output(reverse_left, gpio.LOW)
    gpio.output(reverse_right, gpio.LOW)
    
    

def hard_right(t=1.):
    gpio.output(forward_left, gpio.HIGH)
    gpio.output(reverse_right, gpio.HIGH)
    
    sleep(t)
    gpio.output(forward_left, gpio.LOW)
    gpio.output(reverse_right, gpio.LOW)
    


def hard_left(t=1.):
    gpio.output(forward_right, gpio.HIGH)
    gpio.output(reverse_left, gpio.HIGH)
    
    sleep(t)
    gpio.output(forward_right, gpio.LOW)
    gpio.output(reverse_left, gpio.LOW)
    


##########################################################################
# cleanup
##########################################################################

def cleanup():

    gpio.cleanup()




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
        
        # robot doesn't know it is stuck at wall if wheels
        # still spinning forward
        if state <= 2.5 * distance_from_sensor_to_car_front:
            reward -= 3.0

        if action == 0:         
            forward(1)
            reward = 1
        elif action == 1:       
            reverse(1)
            reward = -1
        elif action == 2:       
            turn_left(2)
            reward = 1
        elif action == 3:      
            turn_right(2)
            reward = 1
            
        '''
        elif action == 4:       
            turn_right()
            reward = 1
        elif action == 5:       
            turn_left()
            reward = 1
        '''
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
random_actions = np.random.random_integers(0, 3, total_episodes)


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
        e = max(e, .1)   # keep epislon over 10%

        if np.random.rand(1) < e:
            action = random_actions[i]
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
