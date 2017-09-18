
# http://github.com/timestocome
# Test servos SG90, TowerPro


# more info
# https://github.com/runmyrobot/runmyrobot/wiki/Adafruit-16-Channel-PWM---Servo-Hat


from time import sleep
import Adafruit_PCA9685



# init
pwm = Adafruit_PCA9685.PCA9685()


# which servo is being sent the signal
channel = 0                    # using first of 16 channels



# The SG90 I tested had a min value of 140 and a max of 600
# 480 is straight, 400-540 is about 90', 45' on each side of the center


servo_min = 380
servo_max = 560
servo_center = 480
for i in range(servo_min, servo_max, 5):
    print(i)
    pwm.set_pwm(channel, 0, i)
    sleep(0.1)


# cleanup
pwm.set_pwm(channel, 0, 480)
pwm = None

