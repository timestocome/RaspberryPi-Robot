# start grabbing video from camera and saving to disk for use in other code


# https://www.raspberrypi.org/learning/getting-started-with-picamera/worksheet/
# https://picamera.readthedocs.io/en/release-1.13/index.html

from picamera import PiCamera
from time import sleep



# init
camera = PiCamera()
camera.rotation = 180      # rotate if image not upright


# default is 1920 x 1080  drop it way down for TF
camera.resolution = (180, 180)
camera.framerate = 5
print(camera.resolution)   


# loop capture a series of images
for i in range(5):
    sleep(1)
    camera.capture('/home/pi/videoFeed/image%s.jpg' % i)





'''
# test record video
camera.start_preview()
camera.start_recording('/home/pi/videoFeed.h264')

sleep(5)

camera.stop_recording()
camera.stop_preview()
'''
