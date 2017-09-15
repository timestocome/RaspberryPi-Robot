

# http://github.com/timestocome


# pins 3, 5, 7, 24, 29, 31
# gpio 0-8 are on by default on boot


# more info
# http://www.mcmanis.com/chuck/robotics/tutorial/h-bridge/
# http://www.bristolwatch.com/L298N/index.htm


import RPi.GPIO as gpio
from time import sleep

gpio.setmode(gpio.BOARD)




gpio.setup(38, gpio.OUT)    # go in reverse left wheel
gpio.setup(40, gpio.OUT)    # go forward left wheel

gpio.setup(35, gpio.OUT)    # go forward right wheel
gpio.setup(33, gpio.OUT)    # go in reverse right wheel




def go_forward(t):
    
    gpio.output(40, gpio.HIGH)
    gpio.output(35, gpio.HIGH)
    
    sleep(t)
    gpio.output(40, gpio.LOW)
    gpio.output(35, gpio.LOW)
    

def turn_left(t):
    gpio.output(35, gpio.HIGH)
    
    sleep(t)
    gpio.output(35, gpio.LOW)
    


def turn_right(t):
    gpio.output(40, gpio.HIGH)
    
    sleep(t)
    gpio.output(40, gpio.LOW)
    


def go_backward(t):
    
    gpio.output(38, gpio.HIGH)
    gpio.output(33, gpio.HIGH)
    
    sleep(t)
    gpio.output(38, gpio.LOW)
    gpio.output(33, gpio.LOW)
    
    

def reverse_turn_right(t):
    gpio.output(33, gpio.HIGH)
    
    sleep(t)
    gpio.output(33, gpio.LOW)
    


def reverse_turn_left(t):
    gpio.output(38, gpio.HIGH)
    
    sleep(t)
    gpio.output(38, gpio.LOW)
    
 

def hard_right(t=1.):
    gpio.output(40, gpio.HIGH)
    gpio.output(33, gpio.HIGH)
    
    sleep(t)
    gpio.output(40, gpio.LOW)
    gpio.output(33, gpio.LOW)
    


def hard_left(t=1.):
    gpio.output(35, gpio.HIGH)
    gpio.output(38, gpio.HIGH)
    
    sleep(t)
    gpio.output(35, gpio.LOW)
    gpio.output(38, gpio.LOW)
      
    
def stop1(t=1):
    gpio.output(40, gpio.HIGH)
    gpio.output(38, gpio.HIGH)
    
    sleep(t)
    gpio.output(40, gpio.LOW)
    gpio.output(38, gpio.LOW)
      
    
def stop2(t=1):
    gpio.output(35, gpio.HIGH)
    gpio.output(33, gpio.HIGH)
    
    sleep(t)
    gpio.output(35, gpio.LOW)
    gpio.output(33, gpio.LOW)
      
  

# test


go_forward(2.)
go_backward(2.)

stop1(1)

reverse_turn_right(2.)
reverse_turn_left(2.)

turn_left(2.)
turn_right(2.)

stop2(1)

hard_left(2.)
hard_right(2.)



# clean up
gpio.cleanup()

