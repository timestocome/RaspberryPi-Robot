

# http://github.com/timestocome
# 
# convert a jpg to a numpy array, save it 
# read it back in to be sure it saved correctly


import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

image = Image.open('camera_images/image_cat.jpg')
image_out = np.empty((240, 320, 3), dtype=np.uint8)
np.save('image_cat.npy', np.array(image))

load_array = np.load('image_cat.npy')


plt.imshow(load_array, interpolation='nearest')
plt.show()
