
Object Detection on RaspberryPi using Google's TensorFlow Object Detection Model


You'll need to download TensorFlow Models

https://github.com/tensorflow/models


Follow the directions here to install, test the model

https://github.com/tensorflow/models/tree/master/research/object_detection


Once it all works you can move the 'object_detection' directory out to your home directory

Re-run from one directory up from your object_detection directory

protoc object_detection/protos/*.proto --python_out=.


Change line 22

from: ---> 22 from object_detection.protos import string_int_label_map_pb2

to: ---> 22 from protos import string_int_label_map_pb2



To test your Raspberry Pi Images

Take an image using 

https://github.com/timestocome/RaspberryPi/blob/master/test%20hardware%20scripts/TestPiCamera.py



Copy the image to 

object_detection/test_images/image3.jpg



Run the Object Detector

* line 73 TEST_IMAGE_PATHS will need to have the range set to (1,4) or as many images as you're testing
