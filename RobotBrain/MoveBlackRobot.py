# http://github.com/timestocome

# move 2wd robot using wheels to steer

import RPi.GPIO as gpio
import time
from time import sleep




class MoveRobot(object):


    def __init__(self):

        print('init robot gpio')
        # set up hardware
        gpio.setmode(gpio.BOARD)        # use pin numbers not gpio numbers


        # wheels ( 4 wheel motors )
        self.reverse_left = 38
        self.reverse_right = 35
        self.forward_left = 40
        self.forward_right = 37

        gpio.setup(self.reverse_left, gpio.OUT)  
        gpio.setup(self.forward_left, gpio.OUT)  
        gpio.setup(self.forward_right, gpio.OUT) 
        gpio.setup(self.reverse_right, gpio.OUT) 

        self.wheel_pulse = 0.2
        #self.actions = ['forward', 'reverse', 'turn_left', 'turn_right', 'hard_left', 'hard_right']
        self.actions = ['forward', 'reverse', 'hard_left', 'hard_right']


    def forward(self):
    
        gpio.output(self.forward_right, gpio.HIGH)
        gpio.output(self.forward_left, gpio.HIGH)
    
        sleep(self.wheel_pulse)
        gpio.output(self.forward_right, gpio.LOW)
        gpio.output(self.forward_left, gpio.LOW)
    
    '''
    def turn_left(self):
        
        gpio.output(self.forward_right, gpio.HIGH)
    
        sleep(self.wheel_pulse)
        gpio.output(self.forward_right, gpio.LOW)
    


    def turn_right(self):
        gpio.output(self.forward_left, gpio.HIGH)
    
        sleep(self.wheel_pulse)
        gpio.output(self.forward_left, gpio.LOW)
    
    '''

    def reverse(self):
    
        gpio.output(self.reverse_left, gpio.HIGH)
        gpio.output(self.reverse_right, gpio.HIGH)
    
        sleep(self.wheel_pulse)
        gpio.output(self.reverse_left, gpio.LOW)
        gpio.output(self.reverse_right, gpio.LOW)
    
    

    def hard_right(self):
       
        gpio.output(self.forward_left, gpio.HIGH)
        gpio.output(self.reverse_right, gpio.HIGH)
    
        sleep(self.wheel_pulse)
        gpio.output(self.forward_left, gpio.LOW)
        gpio.output(self.reverse_right, gpio.LOW)
    


    def hard_left(self):
        
        gpio.output(self.forward_right, gpio.HIGH)
        gpio.output(self.reverse_left, gpio.HIGH)
    
        sleep(self.wheel_pulse)
        gpio.output(self.forward_right, gpio.LOW)
        gpio.output(self.reverse_left, gpio.LOW)
    


    def cleanup(self):
        gpio.cleanup()



#######################################################################
# test
'''
move_robot = MoveRobot()
move_robot.forward()
move_robot.reverse()
move_robot.turn_left()
move_robot.turn_right()
move_robot.hard_left()
move_robot.hard_right()

'''


