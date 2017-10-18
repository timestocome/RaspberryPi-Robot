# http://github.com/timestocome

# take photo with PiCamera
# determine if cat in photo

# takes ~3 seconds to load
# runs > 60fps, probably faster when not printing to screen



import numpy as np
import tensorflow as tf
import picamera

import datetime

class FindCats(object):
    
    def __init__(self):

        print('init cats')
        # set up constants
        self.height = 128
        self.width = 128
        self.input_mean = 0
        self.input_std = 255

        self.min_cat = 0
        self.merlin = 1
        self.no_cat = 2

        # setup graph
        # this is the saved graph that was trained on a desktop
        self.model_file = "output_graph.pb"
        self.label_file = "output_labels.txt"
        self.input_layer_name = "import/input"
        self.output_layer_name = "import/final_result"


        # setup camera
        camera = picamera.PiCamera()
        camera.resolution = (self.width, self.height)
        camera.vflip = True
        self.camera = camera



        # load saved, trained nn    
        graph = tf.Graph()
        graph_def = tf.GraphDef()

        with open(self.model_file, "rb") as f:
            graph_def.ParseFromString(f.read())

        with graph.as_default():
            tf.import_graph_def(graph_def)

        self.graph = graph


        # load labels    
        label = []
        proto_as_ascii_lines = tf.gfile.GFile(self.label_file).readlines()
  
        for l in proto_as_ascii_lines:
            label.append(l.rstrip())
  
        self.labels = label
        
        self.min_cat = 0
        self.merlin = 1
        self.no_cat = 2


        # create session
        self.sess = tf.Session(graph=self.graph)
        self.camera_sess = tf.Session()
    

    
    def capture_image(self):
    
      image = np.empty((self.width, self.height, 3), dtype=np.uint8)
      self.camera.capture(image, 'rgb')
  
      float_caster = tf.cast(image, tf.float32)
      dims_expander = tf.expand_dims(float_caster, 0);
      resized = tf.image.resize_bilinear(dims_expander, [self.height, self.width])
  
      normalized = tf.divide(tf.subtract(resized, [self.input_mean]), [self.input_std])
      result = self.camera_sess.run(normalized)

      return result
    


    def is_cat(self):
        
        now = datetime.datetime.now()
        
        # take photo
        t = self.capture_image()
  
        # see if Min, Merlin or no cat in photo
        input_operation = self.graph.get_operation_by_name(self.input_layer_name);
        output_operation = self.graph.get_operation_by_name(self.output_layer_name);

        results = self.sess.run(output_operation.outputs[0], {input_operation.outputs[0]: t})
        results = np.squeeze(results)

        
        
        found = []
        for i in range(3):
            found.append((self.labels[i], results[i]))
            
            
        print(datetime.datetime.now() - now)
        return found
        
    
    
    
    def cleanup(self):
        self.sess.close()




##################################################
# run graph in loop
#################################################

# test
'''
loop = FindCats()

for i in range(100):
    found_cat = loop.is_cat()
    print(found_cat)
    print(found_cat[0][0], found_cat[0][1])

loop.cleanup()
'''
