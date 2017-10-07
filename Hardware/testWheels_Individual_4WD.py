

import RPi.GPIO as gpio
from time import sleep

gpio.setmode(gpio.BOARD)

# rear left
gpio.setup(13, gpio.OUT)    # forward
gpio.setup(15, gpio.OUT)    # reverse

# rear right
gpio.setup(31, gpio.OUT)    # forward
gpio.setup(29, gpio.OUT)    # reverse

# front right
gpio.setup(40, gpio.OUT)    # forward
gpio.setup(7, gpio.OUT)     # reverse

# front left
gpio.setup(38, gpio.OUT)    # forward
gpio.setup(36, gpio.OUT)    # reverse




def forward_front(t):
    
    gpio.output(40, gpio.HIGH)
    gpio.output(38, gpio.HIGH)
    
    sleep(t)
    gpio.output(40, gpio.LOW)
    gpio.output(38, gpio.LOW)
    

def forward_rear(t):
    
    gpio.output(13, gpio.HIGH)
    gpio.output(31, gpio.HIGH)
    
    sleep(t)
    gpio.output(13, gpio.LOW)
    gpio.output(31, gpio.LOW)
    
    

def forward_right(t):
    gpio.output(40, gpio.HIGH)
    gpio.output(31, gpio.HIGH)
    
    sleep(t)
    gpio.output(40, gpio.LOW)
    gpio.output(31, gpio.LOW)
    


def forward_left(t):
    gpio.output(13, gpio.HIGH)
    gpio.output(38, gpio.HIGH)
    
    sleep(t)
    gpio.output(13, gpio.LOW)
    gpio.output(38, gpio.LOW)
    







def reverse_front(t):
    
    gpio.output(7, gpio.HIGH)
    gpio.output(36, gpio.HIGH)
    
    sleep(t)
    gpio.output(7, gpio.LOW)
    gpio.output(36, gpio.LOW)
    

def reverse_rear(t):
    
    gpio.output(15, gpio.HIGH)
    gpio.output(29, gpio.HIGH)
    
    sleep(t)
    gpio.output(15, gpio.LOW)
    gpio.output(29, gpio.LOW)
    
    

def reverse_right(t):
    gpio.output(29, gpio.HIGH)
    gpio.output(7, gpio.HIGH)
    
    sleep(t)
    gpio.output(29, gpio.LOW)
    gpio.output(7, gpio.LOW)
    


def reverse_left(t):
    gpio.output(15, gpio.HIGH)
    gpio.output(36, gpio.HIGH)
    
    sleep(t)
    gpio.output(15, gpio.LOW)
    gpio.output(36, gpio.LOW)
    











# test
forward_right(2.0)
forward_left(2.0)
forward_rear(2.0)
forward_front(2.0)

reverse_right(2.0)
reverse_left(2.0)
reverse_rear(2.0)
reverse_front(2.0)


# clean up
gpio.cleanup()

