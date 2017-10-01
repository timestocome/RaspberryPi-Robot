# Cat id uses MobileNet to identify our two cats


Google directions ( start here to be sure you understand how to use and load models):

https://github.com/tensorflow/models/tree/master/research

list of models:

https://github.com/tensorflow/models/blob/master/research/slim/nets/mobilenet_v1.md

directions to train a model on your images:

https://hackernoon.com/creating-insanely-fast-image-classifiers-with-mobilenet-in-tensorflow-f030ce0a2991


Training is best done on your desktop computer. Once it's complete copy the model, labels and label.py to 
the Raspberry Pi to run it.

While training Tensorflow will put the saved model and label files in your /tmp dir


On the Pi:
- Tensorflow must be installed
- output_graph.pb   ( your model )
- output_labels.txt (your labels )
- label_cats.py ( Python script to load graph and 'test.jpg' to see if it is Min, Merlin, No cat )


