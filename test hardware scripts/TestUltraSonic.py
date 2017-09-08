# http://github.com/timestocome


# hook up and read ultra sonic SR204 sensors to Raspberry Pi
# needs calibration still 
# I used 470 Ohm (R2) and 330 Ohm (R1) resisters
# some one else said   R2/2 <  R1 * 2 < R2  idk, I haven't verified this 

# photo of test wiring 
# https://github.com/timestocome/RaspberryPi/blob/master/photos_of_robots/Test%20SR204%20.jpg


# source for starting project
# https://electrosome.com/hc-sr04-ultrasonic-sensor-raspberry-pi/ 3/9





import RPi.GPIO as gpio
import time
from time import sleep

gpio.setmode(gpio.BOARD)

trigger = 13
echo = 11

gpio.setup(trigger, gpio.OUT)    # trigger
gpio.setup(echo, gpio.IN)    # echo


pulse_start = 0.
pulse_end = 0.

# adjust sensor location
distance_sensor_to_car_front = 4 * 2.54   # inches to cm



while True:
    
    #print('init sensor....')
    gpio.output(trigger, False)
    time.sleep(0.5)
    
    #print('trigger...')
    gpio.output(trigger, True)
    time.sleep(0.00001)
    gpio.output(trigger, False)
    
    while gpio.input(echo) == 0:
        pulse_start = time.time()
        
    while gpio.input(echo) == 1:
        pulse_end = time.time()
        
    pulse_duration = pulse_end - pulse_start
    #print('duration... ', pulse_duration)
    
    
    distance = pulse_duration * 34000 / 2.      # round trip so cut in half
    distance = round(distance, 2)
    
    if distance < 1000:
        print('Distance ', distance - distance_sensor_to_car_front)
    else:
        print('Out of range')
        
        


gpio.cleanup()

