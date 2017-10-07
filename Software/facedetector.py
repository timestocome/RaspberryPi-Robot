
# http://github.com/timestocome

# use the raspberri pi camera to stream a small image, slowly and check for faces.



# adapted from 
# https://github.com/DeligenceTechnologies/Face-detection-using-OpenCV-With-Raspberry-PI/blob/master/face%20detection.py

import io
import picamera
import cv2
import numpy as np
from time import sleep


camera = picamera.PiCamera()
camera.resolution = (320, 320)
camera.framerate = 10
sleep(2)

while True:
    
    output = np.empty((320, 320, 3), dtype=np.uint8)
    camera.capture(output, 'bgr')
    
    

    #Now creates an OpenCV image
    #image = cv2.imdecode(output, 1)
    image = output.reshape((320, 320, 3))

    #Load a cascade file for detecting faces
    face_cascade = cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml')

    #Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #Look for faces in the image using the loaded cascade file
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    print ("Found ", len(faces))


# save for later .......
#Draw a rectangle around every found face
    #for (x,y,w,h) in faces:
    #    cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2)

