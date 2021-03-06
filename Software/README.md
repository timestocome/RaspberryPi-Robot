# RaspberryPi setup for machine learning robotics 


### -----     Setup     -----

RaspberryPi Software Guide (basic OS directions and images) 

https://www.raspberrypi.org/learning/software-guide/quickstart/



Download SD Formatter

https://www.sdcard.org/



Download Raspbian

https://www.raspberrypi.org/downloads/


Download Etcher.io

https://etcher.io/


Insert SD card into your computer (16GB+)

- If your computer won't read it ( My Surface and iMac wouldn't load some of the cards I tried)
--- Stick the card in a camera and format it
--- Then plug camera into computer and format with SD Formatter


Use the SD Formatter to do a full format

Use Etcher.io to flash the OS onto the card ( be sure to unzip Raspbian first )




### -----     Install Emacs     -----
Emacs is much easier to use than vi for editing system files

> sudo apt-get install emacs



### -----     Setup the Pi Camera    -----

Enable the camera
> sudo raspi-config at a command prompt in the terminal
- Select 5. Interfacing options
- Select P1 Enable/Disable Camera
- Select 'Finish' to save changes and reboot


Python library and basics for accessing the camera

https://www.raspberrypi.org/documentation/usage/camera/python/README.md


### -----     Install OpenCV     -----

https://raspberrypi.stackexchange.com/questions/69169/how-to-install-opencv-on-raspberry-pi-3-in-raspbian-jessie


Access and test OpenCV with Python

http://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/


### -----     Setup fixed IP and VNC   -----


Set a fixed wireless ip on the RaspberryPi

https://www.modmypi.com/blog/how-to-give-your-raspberry-pi-a-static-ip-address-update



- edit /etc/dhcpcd.conf 
- add this to the bottom of the file, save it and reboot
* use your router ip and ip address, you can find these by typing ifconfig at a command prompt

#####

interface wlan0

static ip_address=192.168.0.200

static routers=192.168.0.1

static domain_name_servers=192.168.0.1

####


Set up a wireless VNC so you can access your RaspberriPi from your desktop computer

https://www.realvnc.com/en/connect/docs/raspberry-pi.html#raspberry-pi-setup

user: pi

passwd: raspberry



Set the VNC to run at boot every time you start your RaspberryPi

> sudo systemctl enable vncserver-x11-serviced.service



Edit /boot/config.txt on RaspberryPi to get a full screen resolution on your desktop

https://www.raspberrypi.org/forums/viewtopic.php?t=200196
----

hdmi_force_hotplug=1
hdmi_force_mode=1
hdmi_drive=2
hdmi_group=1
hdmi_mode=16

----


### -----     Install Mini Anaconda     -----

https://www.continuum.io/blog/developer/anaconda-raspberry-pi

https://stackoverflow.com/questions/39371772/how-to-install-anaconda-on-raspberry-pi-3-model-b


### -----     Install TensorFlow     -----

- First check to be sure you are using the Python V3.4 or 3.5

> python --version

- Then follow the directions:

sudo apt-get update &amp;&amp; sudo apt-get upgrade
sudo apt-get install python3-pip python3-dev
pip3 install tensorflow



- If you run into trouble check here:

https://www.raspberrypi.org/magpi/tensorflow-ai-raspberry-pi/



- TensorFlow Object Detection model and installation instructions

https://github.com/tensorflow/models/tree/master/research/object_detection



### -----     Backup and Restore SD Card   -----

https://thepihut.com/blogs/raspberry-pi-tutorials/17789160-backing-up-and-restoring-your-raspberry-pis-sd-card

Convert *.dmg to *.img

http://www.instructables.com/id/Restore-DMG-to-SD-Card-MAC-OS-X/


### -------     Transfer Files between Desktop and RaspberryPi     -------

VNC lets you move files between your computer and the Pi

https://www.realvnc.com/en/connect/docs/file-transfer.html

https://www.realvnc.com/en/connect/docs/file-transfer.html#file-transfer-troubleshoot


### -------     Misc     -------

none 

### -----     Change default Python version     -----

> cd /usr/bin

> sudo rm python

> sudo ln -s python2.7 python

or ...

> sudo ln -s python3.4 python




