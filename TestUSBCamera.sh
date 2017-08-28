
#!/bin/bash

# date stamp
timestamp=$(date +%Y_%m_%d_%H_%M)

# grab image
fswebcam --no-banner /home/pi/webcam/$timestamp.jpg

