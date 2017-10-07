

import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BOARD)

print('test distance sensor')



# set up  and init 
trigger = 11
echo = 13

gpio.setup(trigger, gpio.OUT)
gpio.setup(echo, gpio.IN)

pulse_start = 0.
pulse_end = 0.


speed_of_sound = 343 * 100
print("speed of sound in cm", speed_of_sound)

car_length = 4

# run forever

while True:
    
    
    # clear trigger
    gpio.output(trigger, False)
    time.sleep(0.5)
    
    print('send pulse')
    # send pulse to trigger
    gpio.output(trigger, True)
    time.sleep(0.00001)
    gpio.output(trigger, False)
    
    # check echo for return signal
    while gpio.input(echo) == 0:
        pulse_start = time.time()
    
    while gpio.input(echo) == 1:
        pulse_end = time.time()
        
    pulse_duration = pulse_end - pulse_start
    distance = speed_of_sound / 2. * pulse_duration
    distance = round(distance, 2)
    distance /= 2.54    # inches
    
    # filter out things far away
    if distance < 300:
        print("distance (in) ", distance - car_length)
    
       
    
    
gpio.cleanup()
    