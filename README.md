# RaspberryPi
Machine Learning on a Raspberry Pi


-----     Setup     -----

RaspberryPi Software Guide (basic OS directions and images) 

- https://www.raspberrypi.org/learning/software-guide/quickstart/



Download SD Formatter

- https://www.sdcard.org/


Download Raspbian

- https://www.raspberrypi.org/downloads/


Download Etcher.io

- https://etcher.io/


Insert SD card into your computer (16GB+)

- If your computer won't read it ( My Surface and iMac wouldn't see it)

--- Stick the card in a camera and format it

--- Then plug camera into computer and format with SD Formatter


Use the SD Formatter to do a full format

Use Etcher.io to flash the OS onto the card ( be sure to unzip Raspbian first )


Install Mini Anaconda

- https://www.continuum.io/blog/developer/anaconda-raspberry-pi

- https://stackoverflow.com/questions/39371772/how-to-install-anaconda-on-raspberry-pi-3-model-b


Install TensorFlow

- First check to be sure you are using the Python V3.4 installed with Mini Anaconda

- https://github.com/samjabrahams/tensorflow-on-raspberry-pi


Enable the camera
- Type raspi-config at a command prompt in the terminal
- Select 5. Interfacing options
- Select P1 Enable/Disable Camera
- Select 'Finish' to save changes and reboot


Python library and basics for accessing the camera
- https://www.raspberrypi.org/documentation/usage/camera/python/README.md


Setup the wifi on the RaspberryPi
- https://howtoraspberrypi.com/connect-wifi-raspberry-pi-3-others/








