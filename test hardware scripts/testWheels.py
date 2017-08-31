

import RPi.GPIO as gpio
from time import sleep

gpio.setmode(gpio.BOARD)
gpio.setup(13, gpio.OUT)
gpio.setup(15, gpio.OUT)
gpio.setup(29, gpio.OUT)
gpio.setup(31, gpio.OUT)


def forward(t):
  gpio.output(13, gpio.HIGH)
  gpio.output(29, gpio.HIGH)
  sleep(t)
  
  gpio.output(13, gpio.LOW)
  gpio.output(29, gpio.LOW)
  
  
def reverse(t):
  gpio.output(15, gpio.HIGH)
  gpio.output(31, gpio.HIGH)
  sleep(t)
  
  gpio.output(15, gpio.LOW)
  gpio.output(31, gpio.LOW)




forward(0.5)
sleep(1.)
reverse(0.5)

