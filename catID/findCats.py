# http://github.com/timestocome

# take photo with PiCamera
# determine if cat in photo

# takes ~3 seconds to load
# runs > 60fps, probably faster when not printing to screen



import sys
import numpy as np
import tensorflow as tf

import numpy as np
import picamera
import time

import datetime

print("Start ", datetime.datetime.now())

# set up constants
height = 128
width = 128
input_mean = 0
input_std = 255


# setup graph
# this is the saved graph that was trained on a desktop
model_file = "output_graph.pb"
label_file = "output_labels.txt"
input_layer = "input"
output_layer = "final_result"


# setup camera
camera = picamera.PiCamera()
camera.resolution = (width, height)
camera.vflip = True







def load_graph(model_file):
    
  graph = tf.Graph()
  graph_def = tf.GraphDef()

  with open(model_file, "rb") as f:
    graph_def.ParseFromString(f.read())

  with graph.as_default():
    tf.import_graph_def(graph_def)

  return graph




def load_labels(label_file):
    
  label = []
  proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
  
  for l in proto_as_ascii_lines:
    label.append(l.rstrip())
  
  return label





def capture_image():
    
  image = np.empty((width, height, 3), dtype=np.uint8)
  camera.capture(image, 'rgb')
  
  float_caster = tf.cast(image, tf.float32)
  dims_expander = tf.expand_dims(float_caster, 0);
  resized = tf.image.resize_bilinear(dims_expander, [height, width])
  
  normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
  sess = tf.Session()
  result = sess.run(normalized)

  return result




 
# load graph 
graph = load_graph(model_file)
labels = load_labels(label_file)
sess = tf.Session(graph=graph)

input_name = "import/" + input_layer
output_name = "import/" + output_layer

print('Graph loaded', datetime.datetime.now())



# loop forever
counter = 0

while(True):
  
  # take photo
  t = capture_image()
  
  # see if Min, Merlin or no cat in photo
  input_operation = graph.get_operation_by_name(input_name);
  output_operation = graph.get_operation_by_name(output_name);

  results = sess.run(output_operation.outputs[0], {input_operation.outputs[0]: t})
  results = np.squeeze(results)

  top_k = results.argsort()[-3:][::-1]
  
  # print results
  for i in top_k:
    print(labels[i], results[i])
    
  counter += 1
  print("next image", counter, datetime.datetime.now())
  
  
  
sess.close()



  