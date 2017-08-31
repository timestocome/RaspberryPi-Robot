# test Raspberry Pi camera

from picamera import PiCamera
from time import sleep

camera = PiCamera()

# rotate camera view if needed
camera.rotation = 180

# live stream
camera.start_preview()
sleep(3)
camera.stop_preview()


# grab photo
camera.capture('/home/pi/test.jpg')


