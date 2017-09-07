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

gpio.setmode(gpio.BOARD)

print('test distance sensor')



# set up  and init 
trigger = 16
echo = 18

gpio.setup(trigger, gpio.OUT)
gpio.setup(echo, gpio.IN)

pulse_start = 0.
pulse_end = 0.


speed_of_sound = 343 * 100
print("speed of sound in cm", speed_of_sound)



# run forever

while True:
    
    # clear trigger
    gpio.output(trigger, False)
    time.sleep(2)
        
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
    
    # filter out things far away
    if distance < 300:
        print("distance (cm) ", distance)
    
    
       
    
    
gpio.cleanup()
    