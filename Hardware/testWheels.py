

# http://github.com/timestocome


# pins 3, 5, 7, 24, 29, 31
# gpio 0-8 are on by default on boot


# more info
# http://www.mcmanis.com/chuck/robotics/tutorial/h-bridge/
# http://www.bristolwatch.com/L298N/index.htm


import RPi.GPIO as gpio
from time import sleep

gpio.setmode(gpio.BOARD)


# 35, 36, 37, 38

left_forward = 36
right_forward = 35
left_reverse = 38
right_reverse = 37


gpio.setup(left_forward, gpio.OUT) 
gpio.setup(right_forward, gpio.OUT)

gpio.setup(left_reverse, gpio.OUT)   
gpio.setup(right_reverse, gpio.OUT)   




def go_forward(t):
    
    print('forward')
    
    gpio.output(right_forward, gpio.HIGH)
    gpio.output(left_forward, gpio.HIGH)
    
    sleep(t)
    gpio.output(right_forward, gpio.LOW)
    gpio.output(left_forward, gpio.LOW)
    

def turn_left(t):
    
    print('left')
    gpio.output(right_forward, gpio.HIGH)
    
    sleep(t)
    gpio.output(right_forward, gpio.LOW)
    


def turn_right(t):
    print('right')
    gpio.output(left_forward, gpio.HIGH)
    
    sleep(t)
    gpio.output(left_forward, gpio.LOW)
    


def go_backward(t):
    
    print('reverse')
    
    gpio.output(right_reverse, gpio.HIGH)
    gpio.output(left_reverse, gpio.HIGH)
    
    sleep(t)
    gpio.output(right_reverse, gpio.LOW)
    gpio.output(left_reverse, gpio.LOW)
    
    

def reverse_turn_right(t):
    print('reverse right')
    gpio.output(right_reverse, gpio.HIGH)
    
    sleep(t)
    gpio.output(right_reverse, gpio.LOW)
    


def reverse_turn_left(t):
    print('reverse left')
    gpio.output(left_reverse, gpio.HIGH)
    
    sleep(t)
    gpio.output(left_reverse, gpio.LOW)
    
 

def hard_right(t=1.):
    print('hard right')
    gpio.output(left_forward, gpio.HIGH)
    gpio.output(right_reverse, gpio.HIGH)
    
    sleep(t)
    gpio.output(left_forward, gpio.LOW)
    gpio.output(right_reverse, gpio.LOW)
    


def hard_left(t=1.):
    print('hard left')
    gpio.output(right_forward, gpio.HIGH)
    gpio.output(left_reverse, gpio.HIGH)
    
    sleep(t)
    gpio.output(right_forward, gpio.LOW)
    gpio.output(left_reverse, gpio.LOW)
      
    
def stop1(t=1):
    print('stop1')
    gpio.output(left_forward, gpio.HIGH)
    gpio.output(left_reverse, gpio.HIGH)
    
    sleep(t)
    gpio.output(left_forward, gpio.LOW)
    gpio.output(left_reverse, gpio.LOW)
      
    
def stop2(t=1):
    print('stop2')
    gpio.output(right_forward, gpio.HIGH)
    gpio.output(right_reverse, gpio.HIGH)
    
    sleep(t)
    gpio.output(right_forward, gpio.LOW)
    gpio.output(right_reverse, gpio.LOW)
      
  

# test

'''
go_forward(2.)
go_backward(2.)


stop1(1)

reverse_turn_right(2.)
reverse_turn_left(2.)
'''
turn_left(2.)
turn_right(2.)

stop2(1)
'''
hard_left(2.)
hard_right(2.)
'''


# clean up
gpio.cleanup()

