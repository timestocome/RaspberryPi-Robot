
# Hardware parts and test scripts 

Robot 1 (clear chassis)
- Smart Video Car Kit from SunFounderDirecthttps://www.amazon.com/gp/product/B014KK89BW/ (I couldn't get this kit to work so I just used it for parts)
- RaspberryPi 3 https://www.amazon.com/Raspberry-Model-1-2GHz-64-bit-quad-core/dp/B01CD5VC92/
- L298N Dual H Bridge Stepper Motor https://www.amazon.com/gp/product/B00AJGM37I
- PCA9685 16 Channel, 12 Bit PWM Servo Driver https://www.amazon.com/gp/product/B014KTSMLA
- Micro SD card 16 GB or larger
- 370, 440 Ohm resistors, small bread board
- Batteries, battery holder for wheel motor batteries
- Battery Power Pack Expansion Board for Pi https://www.amazon.com/gp/product/B06Y2XBV8Q
- misc wires https://www.amazon.com/gp/product/B01IB7UOFE
- camera mounting bracket (https://www.adafruit.com/product/1434)
- ultrasonic sensor mounting bracket ( https://www.amazon.com/gp/product/B01FDGU0GY/)


Robot 2 (black chassis)
- Actobatics Whippersnapper Rover http://www.frys.com/product/8458148?site=sr:SEARCH:MAIN_RSLT_PG 
- RaspberryPi 3 https://www.amazon.com/Raspberry-Model-1-2GHz-64-bit-quad-core/dp/B01CD5VC92/
- SainSmart L298N Dual H Bridge Stepper Motor https://www.amazon.com/gp/product/B00AJGM37I/
- Micro SD card 16 GB or larger
- 370, 440 Ohm resistors, small bread board
- Battery case and batteries
- Battery Power Pack Expansion Board for Pi https://www.amazon.com/gp/product/B06Y2XBV8Q
- RaspberryPi Camera Module V2 - 8 MP https://www.amazon.com/Raspberry-Pi-Camera-Module-Megapixel/dp/B01ER2SKFS/
- misc wires https://www.amazon.com/gp/product/B01IB7UOFE
- camera mounting bracket
- ultrasonic sensor mounting bracket



Python script to test wheels:

https://github.com/timestocome/RaspberryPi/blob/master/testWheels.py


Source:

http://deepaksinghviblog.blogspot.com/2014/08/raspberrypi-to-run-dc-motor-using-l298n.html




------- RaspberryPi camera -------

Turn on the camera in Raspberry Pi Configuration ( under preferences )

Python script to test camera video and image capture:

https://github.com/timestocome/RaspberryPi/blob/master/TestPiCamera.py


Source:

https://www.raspberrypi.org/learning/getting-started-with-picamera/requirements/



------- Ultra sonic sensor HC204 ---------

Test script and notes to check SR204 is working

https://github.com/timestocome/RaspberryPi/blob/master/test%20hardware%20scripts/TestUltraSonic.py


------- Handy things to know for debugging -------

Turn on i2c interface so you can connect and run accessories off your RaspberryPi

https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c

> sudo raspi-config
-> i2c
-> enable


Check i2c connections and locations 
> sudo i2cdetect -y 1


Check GPIU
> gpio readall





