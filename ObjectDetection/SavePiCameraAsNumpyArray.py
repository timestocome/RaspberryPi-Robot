# http://github.com/timestocome


# test Raspberry Pi camera
# save image as numpy array 
# reload it to be sure it saved correctly




from picamera import PiCamera
from time import sleep
import numpy as np



camera = PiCamera()
#camera.rotation = 180
camera.resolution = (320, 240)

camera.framerate = 10
image_out = np.empty((240, 320, 3), dtype=np.uint8)
camera.capture(image_out, 'rgb')
np.save('image.npy', image_out)


# test save
from PIL import Image
import matplotlib.pyplot as plt

load_array = np.load('image.npy')
plt.imshow(load_array, interpolation='nearest')
plt.show()

