# http://github.com/timestocome


# movement functions for robot
# this robot has a servo for steering ~90' range
# rear wheel drive with separate controls for the wheels 


import RPi.GPIO as gpio
import Adafruit_PCA9685

import time
from time import sleep




class MoveRobot(object):


    def __init__(self):
        
        # set up hardware
        gpio.setmode(gpio.BOARD)        # use pin numbers not gpio numbers

        # wheels ( 2wd, rear wheels) 
        self.reverse_left = 38
        self.reverse_right = 37
        self.forward_left = 26
        self.forward_right = 35

        gpio.setup(self.reverse_left, gpio.OUT)  
        gpio.setup(self.forward_left, gpio.OUT)  
        gpio.setup(self.forward_right, gpio.OUT) 
        gpio.setup(self.reverse_right, gpio.OUT) 

        self.wheel_pulse = 0.5


        # servo steering 
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(60)

        # which servo is being sent the signal
        self.channel = 0                    # using first of 16 channels

        self.servo_min = 300
        self.servo_max = 450
        self.servo_center = (self.servo_min + self.servo_max) // 2

    
        # actions robot can take 
        self.actions = ['center_forward', 'right_forward', 'left_forward', 
            'center_reverse','right_reverse', 'left_reverse']


        def forward(self):
    
            gpio.output(self.forward_right, gpio.HIGH)
            gpio.output(self.forward_left, gpio.HIGH)
    
            sleep(self.wheel_pulse/2)
            gpio.output(self.forward_right, gpio.LOW)
            gpio.output(self.forward_left, gpio.LOW)
        
        self.forward = forward
    

        def reverse(self):
    
            gpio.output(self.reverse_left, gpio.HIGH)
            gpio.output(self.reverse_right, gpio.HIGH)
    
            sleep(self.wheel_pulse/2)
            gpio.output(self.reverse_left, gpio.LOW)
            gpio.output(self.reverse_right, gpio.LOW)
    
        self.reverse = reverse
    
    
            
    

    def center_forward(self):
        self.pwm.set_pwm(0, 0, 375)
        self.forward(self)


    def hard_right_forward(self):
        self.pwm.set_pwm(0, 0, 300)
        self.forward(self)
        

    def right_forward(self):
        self.pwm.set_pwm(0, 0, 340)
        self.forward(self)
        

    def left_forward(self):
        self.pwm.set_pwm(0, 0, 410)
        self.forward(self)
        

    def hard_left_forward(self):
        self.pwm.set_pwm(0, 0, 450)
        self.forward(self)
        

    def center_reverse(self):
        self.pwm.set_pwm(0, 0, 375)
        self.reverse(self)
        
        
    def hard_right_reverse(self):
        self.pwm.set_pwm(0, 0, 300)
        self.reverse(self)
        

    def right_reverse(self):
        self.pwm.set_pwm(0, 0, 340)
        self.reverse(self)
        

    def left_reverse(self):
        self.pwm.set_pwm(0, 0, 410)
        self.reverse(self)
        
    
    def hard_left_reverse(self):
        self.pwm.set_pwm(0, 0, 450)
        self.reverse(self)
        

        
    
    
    
    def cleanup(self):

        gpio.cleanup()

        self.pwm.set_pwm(0, 0, self.servo_center)
        self.pwm = None


##################################################################
# test

'''
move_robot = MoveRobot()


move_robot.center_forward()
move_robot.hard_right_forward()
move_robot.right_forward()
move_robot.left_forward()
move_robot.hard_left_forward()
move_robot.center_reverse()
move_robot.hard_right_reverse()
move_robot.right_reverse()
move_robot.left_reverse()
move_robot.hard_left_reverse()
'''

