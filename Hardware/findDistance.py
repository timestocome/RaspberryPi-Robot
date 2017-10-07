# http://github.com/timestocome



import RPi.GPIO as gpio
import time


class findDistance(object):
    
    
    def __init__(self):

        gpio.setmode(gpio.BOARD)

        # set up  and init 
        self.trigger = 11
        self.echo = 13

        gpio.setup(self.trigger, gpio.OUT)
        gpio.setup(self.echo, gpio.IN)

        self.pulse_start = 0.
        self.pulse_end = 0.
        self.speed_of_sound = 343 * 100
        self.car_length = 1



    def get_distance(self):
        
        # clear trigger
        gpio.output(self.trigger, False)
        time.sleep(0.5)
    
        # send pulse to trigger
        gpio.output(self.trigger, True)
        time.sleep(0.00001)
        gpio.output(self.trigger, False)
    
    
        # check echo for return signal
        while gpio.input(self.echo) == 0:
            pulse_start = time.time()
    
        while gpio.input(self.echo) == 1:
            pulse_end = time.time()
        
        pulse_duration = pulse_end - pulse_start
        distance = self.speed_of_sound / 2. * pulse_duration
        distance = round(distance, 2)
        distance /= 2.54    # inches
    
        # filter out things far away
        if distance > 100:
            distance = 100
        
        # filter out junk
        if distance < 1:
            disance = 1
    
        return distance
    
    
    def cleanup(self):
        gpio.cleanup()
    
    
    
###################################################
# test class
'''
test_distance = findDistance()
distance = test_distance.get_distance()
print(distance)
test_distance.cleanup()
'''