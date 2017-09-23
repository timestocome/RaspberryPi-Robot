# http://github.com/timestocome


# train a raspberry pi robot to wander the house while avoiding obstacles
# this robot has a servo for steering ~90' range
# rear wheel drive with separate controls for the wheels 





import tensorflow as tf
import tensorflow.contrib.slim as slim
import numpy as np

import RPi.GPIO as gpio
import Adafruit_PCA9685

import time
from time import sleep


###############################################################################
# set up hardware
###############################################################################
gpio.setmode(gpio.BOARD)        # use pin numbers not gpio numbers

# ultrasonic sensor -------------------------------------------------
trigger = 11
echo = 13

max_distance = 100    # sensor can read ~400 cm cap this to reduce state space

gpio.setup(trigger, gpio.OUT)
gpio.setup(echo, gpio.IN)


# wheels ( 2wd, rear wheels) -----------------------------------------
reverse_left = 38
reverse_right = 37
forward_left = 26
forward_right = 35

gpio.setup(reverse_left, gpio.OUT)  
gpio.setup(forward_left, gpio.OUT)  
gpio.setup(forward_right, gpio.OUT) 
gpio.setup(reverse_right, gpio.OUT) 

wheel_pulse = 0.5


# servo steering -------------------------------------------------
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)

# which servo is being sent the signal
channel = 0                    # using first of 16 channels

servo_min = 300
servo_max = 450
servo_center = (servo_min + servo_max) // 2


##############################################################################
# load data from HC-SR204 UltraSonic distance sensor
# this is the input to the network
##############################################################################

# init 
pulse_start = 0.
pulse_end = 0.


# flush sensor
gpio.output(trigger, False)
time.sleep(0.5)


# distance to obstacle in path
def get_state(sleep_time=wheel_pulse):

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
    
    # check if beyond sensor range 400 cm or beyond where we care about 
    if distance >= max_distance:    
        distance = max_distance - 1

    # less than 2cm means bad data
    if distance <= 2:
        distance = 2

    return int(distance)





##############################################################################
# actions robot can take
# to reduce state space servo using discrete positions
# and wheels only set to move forward or reverse
# 
# wheels can also be coded to:
# right reverse
# left reverse
# right forward
# left forward
# right forward, left reverse
# right reverse, left forward
#
# servo can be positioned to any int between 300 and 450
##############################################################################
actions = ['center_forward', 'hard_right_forward', 'right_forward', 'left_forward', 'hard_left_forward',
            'center_reverse', 'hard_right_reverse', 'right_reverse', 'left_reverse', 'hard_left_reverse']

def center_forward():
    pwm.set_pwm(0, 0, 375)
    forward()

def hard_right_forward():
    pwm.set_pwm(0, 0, 300)
    forward()

def right_forward():
    pwm.set_pwm(0, 0, 340)
    forward()

def left_forward():
    pwm.set_pwm(0, 0, 410)
    forward()

def hard_left_forward():
    pwm.set_pwm(0, 0, 450)
    forward()


def center_reverse():
    pwm.set_pwm(0, 0, 375)
    reverse()

def hard_right_reverse():
    pwm.set_pwm(0, 0, 300)
    reverse()

def right_reverse():
    pwm.set_pwm(0, 0, 340)
    reverse()

def left_reverse():
    pwm.set_pwm(0, 0, 410)
    reverse()

def hard_left_reverse():
    pwm.set_pwm(0, 0, 450)
    reverse()



def forward(t=wheel_pulse):
    
    gpio.output(forward_right, gpio.HIGH)
    gpio.output(forward_left, gpio.HIGH)
    
    sleep(t)
    gpio.output(forward_right, gpio.LOW)
    gpio.output(forward_left, gpio.LOW)
    


def reverse(t=wheel_pulse/2):
    
    gpio.output(reverse_left, gpio.HIGH)
    gpio.output(reverse_right, gpio.HIGH)
    
    sleep(t)
    gpio.output(reverse_left, gpio.LOW)
    gpio.output(reverse_right, gpio.LOW)
    
    



##########################################################################
# cleanup
##########################################################################

def cleanup():

    gpio.cleanup()

    pwm.set_pwm(channel, 0, servo_center)
    pwm = None





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
        
        

        # penalty for being too closes to an obstacle
        if state <= 5:   # buffer zone in cm
            reward = -4.0

        if action == 0:         
            center_forward()
            reward += 3
        elif action == 1:       
            hard_right_forward()
            reward += 1
        elif action == 2:       
            right_forward()
            reward += 2
        elif action == 3:      
            left_forward()
            reward += 2
        elif action == 4:       
            hard_left_forward()
            reward += 1
        elif action == 5:       
            center_reverse()
            reward += 0
        elif action == 6:
            hard_right_reverse()
            reward += 0
        elif action == 7:      
            right_reverse()
            reward += 0
        elif action == 8:       
            left_reverse()
            reward += 0
        elif action == 9:       
            hard_left_reverse()
            reward += 0
       


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
    
    # use to restore previous saved weights instead of random start after
    # everything works
    #saver.restore(sess, 'save/model.ckpt')
    

    while i < total_episodes:
        s = get_state()
        e *= 0.95        # reduce random searching over time
        e = max(e, .2)   # keep epislon over 10%, higher for more random behavior

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
            print("Distance: ", distance)       # forward distance covered
            print("Choices: ", choices)         # make sure not locking onto one choice
        # end debugging statements



        # save weights
        if i % 100 == 0:
            save_path = saver.save(sess, 'save/model.ckpt')
            
        i += 1


cleanup()
