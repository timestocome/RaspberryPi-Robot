
# http://github.com/timestocome
# Test servos SG90, TowerPro
# Hooked up using PCA9865


# java code but nice details and explainations
# http://www.lediouris.net/RaspberryPI/servo/readme.html

from time import sleep
import Adafruit_PCA9685



# init
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)

# which servo is being sent the signal
channel = 0                    # using first of 16 channels



# The SG90 has a min value of 150 and a max of 600
# 375 is straight, 300-450 is about 90', 45' on each side of the center



servo_min = 300
servo_max = 450
servo_center = (servo_min + servo_max) // 2



position = servo_center
pwm.set_pwm(channel, 0, position)
print("? moved to ", position)



for i in range(servo_min, servo_max, 5):
    print(i)
    pwm.set_pwm(channel, 0, i)
    sleep(0.1)


# cleanup
pwm.set_pwm(channel, 0, servo_center)
pwm = None

