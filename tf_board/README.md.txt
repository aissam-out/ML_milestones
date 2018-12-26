# Tensorboard : Visualize your models

Tensorboard is a web app that will make your life easier if you are dealing with Tensorflow based programs. It is a visualization software that comes with any standard TensorFlow installation in order to make it easier to understand, debug, and optimize TensorFlow programs.


To store data from a computed result, say softmax weights, predications, loss, etc. Call :'''tf.summary.histogram("your_variable_name", your_variable)''' 


To visualize the program with TensorBoard, you have to write log files of the program. To do that, we first need to create a writer for those logs:
'''writer = tf.summary.FileWriter([logdir], [graph])'''


to visualize the graph, run the command line: '''# tensorboard --logdir=[tensorflow_logs]'''. Then navigate your web browser to '''http://localhost:6006''' to view the TensorBoard


Summary is a special operation TensorBoard that takes in a regular tensor and outputs the summarized data to your disk (i.e. in the event file). Basically, there are three main types of summaries:

1. tf.summary.scalar: used to write a single scalar-valued tensor (like a classificaion loss or accuracy value)

2. tf.summary.histogram: used to plot histogram of all the values of a non-scalar tensor (can be used to visualize weight or bias matrices of a neural network)

3. tf.summary.image: used to plot images (like input images of a network, or generated output images of an autoencoder or a GAN)




