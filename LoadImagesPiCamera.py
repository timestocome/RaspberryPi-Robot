
# https://github.com/timestocome/RaspberryPi

# start grabbing video from RaspberryPi camera and saving to disk as numpy array
# if i > 5 saves 7 per loop (0...6)


# https://www.raspberrypi.org/learning/getting-started-with-picamera/worksheet/
# https://picamera.readthedocs.io/en/release-1.13/index.html

from picamera import PiCamera
from time import sleep
import numpy as np



# init
camera = PiCamera()
camera.rotation = 180      # rotate if image not upright

# default is 1920 x 1080  drop it way down for TF
height = 192
width = 192
camera.resolution = (width, height)
camera.framerate = 1

i = 0

while(True):
    if i > 5: i = 0
    else: i+=1
    filename = '/home/pi/videoFeed/image%s.npy' % i
    
    output = np.empty((width, height, 3 ), dtype=np.uint8)
    camera.capture(output, 'rgb')
    np.save(filename, output)
                      
                      
      
