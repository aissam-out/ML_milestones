import scipy
import matplotlib
import numpy as np
from PIL import Image
import tensorflow as tf
matplotlib.use('TkAgg')
from scipy import ndimage
from tf_cnn_d_utils import *
import matplotlib.pyplot as plt
from tensorflow.python.framework import ops

def create_placeholders(n_H0, n_W0, n_C0, n_y):
    """
    Creates the placeholders for the tensorflow session.

    Arguments:  n_H0 -- scalar, height of an input image
                n_W0 -- scalar, width of an input image
                n_C0 -- scalar, number of channels of the input
                n_y -- scalar, number of classes

    Returns:    X -- placeholder for the data input, of shape [None, n_H0, n_W0, n_C0] and dtype "float"
                Y -- placeholder for the input labels, of shape [None, n_y] and dtype "float"
    """

    X = tf.placeholder(tf.float32, shape=[None, n_H0, n_W0, n_C0])
    Y = tf.placeholder(tf.float32, shape=[None, n_y])

    return X, Y

def initialize_parameters():
    """
    Initializes weight parameters to build a neural network with tensorflow with predefined shapes :
    W1 : [4, 4, 3, 8] and W2 : [2, 2, 8, 16]

    Returns:
    parameters -- a dictionary of tensors containing W1, W2
    """

    tf.set_random_seed(1)

    W1 = tf.get_variable('W1',[4, 4, 3, 8], initializer = tf.contrib.layers.xavier_initializer(seed = 0))
    W2 = tf.get_variable('W2',[2, 2, 8, 16], initializer = tf.contrib.layers.xavier_initializer(seed = 0))

    parameters = {"W1": W1,
                  "W2": W2}

    return parameters

def forward_propagation(X, parameters):
    """
    Implements the forward propagation for the model:
    CONV2D -> RELU -> MAXPOOL -> CONV2D -> RELU -> MAXPOOL -> FLATTEN -> FULLYCONNECTED

    Arguments:  X -- input dataset placeholder, of shape (input size, number of examples)
                parameters -- python dictionary containing your parameters "W1", "W2"
                the shapes are given in initialize_parameters

    Returns:    Z3 -- the output of the last LINEAR unit
    """

    # Retrieve the parameters from the dictionary "parameters"
    W1 = parameters['W1']
    W2 = parameters['W2']

    # CONV2D: stride of 1, padding 'SAME'
    Z1 = tf.nn.conv2d(X,W1, strides = [1,1,1,1], padding = 'SAME')
    # RELU
    A1 = tf.nn.relu(Z1)
    # MAXPOOL: window 8x8, sride 8, padding 'SAME'
    P1 = tf.nn.max_pool(A1, ksize = [1,8,8,1], strides = [1,8,8,1], padding = 'SAME')
    # CONV2D: filters W2, stride 1, padding 'SAME'
    Z2 = tf.nn.conv2d(P1,W2, strides = [1,1,1,1], padding = 'SAME')
    # RELU
    A2 = tf.nn.relu(Z2)
    # MAXPOOL: window 4x4, stride 4, padding 'SAME'
    P2 = tf.nn.max_pool(A2, ksize = [1,4,4,1], strides = [1,4,4,1], padding = 'SAME')
    # FLATTEN
    P2 = tf.contrib.layers.flatten(P2)
    # FULLY-CONNECTED without non-linear activation function
    # 6 neurons in output layer
    Z3 = tf.contrib.layers.fully_connected(P2, 6, activation_fn=None)

    return Z3

def compute_cost(Z3, Y):
    """
    Computes the cost

    Arguments:  Z3 -- output of forward propagation (output of the last LINEAR unit), of shape (6, number of examples)
                Y -- "true" labels vector placeholder, same shape as Z3

    Returns:    cost - Tensor of the cost function
    """

    cost = tf.nn.softmax_cross_entropy_with_logits_v2(logits = Z3, labels = Y)
    cost = tf.reduce_mean(cost)

    return cost

def model(X_train, Y_train, X_test, Y_test, learning_rate = 0.009, num_epochs = 400, minibatch_size = 64, print_cost = True):
    """
    Implements a three-layer ConvNet in Tensorflow:
    CONV2D -> RELU -> MAXPOOL -> CONV2D -> RELU -> MAXPOOL -> FLATTEN -> FULLYCONNECTED

    Arguments:  X_train -- training set, of shape (None, 64, 64, 3)
                Y_train -- test set, of shape (None, n_y = 6)
                X_test -- training set, of shape (None, 64, 64, 3)
                Y_test -- test set, of shape (None, n_y = 6)

    Returns:    train_accuracy -- real number, accuracy on the train set (X_train)
                test_accuracy -- real number, testing accuracy on the test set (X_test)
                parameters -- parameters learnt by the model. They can then be used to predict.
    """

    ops.reset_default_graph()                               # to be able to rerun the model without overwriting tf variables
    tf.set_random_seed(1)                                   # to keep results consistent (tensorflow seed)
    seed = 3                                                # to keep results consistent (numpy seed)
    (m, n_H0, n_W0, n_C0) = X_train.shape
    n_y = Y_train.shape[1]                                  # number of classes
    costs = []                                              # To keep track of the cost

    # Create Placeholders of the correct shape
    X, Y = create_placeholders(n_H0, n_W0, n_C0, n_y)

    # Initialize parameters
    parameters = initialize_parameters()

    # Forward propagation: Build the forward propagation in the tensorflow graph
    Z3 = forward_propagation(X, parameters)

    # Cost function: Add cost function to tensorflow graph
    cost = compute_cost(Z3, Y)

    # Backpropagation: Define the tensorflow optimizer. Use an AdamOptimizer that minimizes the cost.
    optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

    # Initialize all the variables globally
    init = tf.global_variables_initializer()

    # Start the session to compute the tensorflow graph
    with tf.Session() as sess:

        # Run the initialization
        sess.run(init)

        # Do the training loop
        for epoch in range(num_epochs):

            minibatch_cost = 0.
            num_minibatches = int(m / minibatch_size) # number of minibatches of size minibatch_size in the train_set
            seed = seed + 1
            minibatches = random_mini_batches(X_train, Y_train, minibatch_size, seed)

            for minibatch in minibatches:
                # Select a minibatch
                (minibatch_X, minibatch_Y) = minibatch
                # IMPORTANT: The line that runs the graph on a minibatch.
                # Run the session to execute the optimizer and the cost, the feedict should contain a minibatch for (X,Y).
                _ , temp_cost = sess.run([optimizer, cost], feed_dict={X: minibatch_X, Y: minibatch_Y})

                minibatch_cost += temp_cost / num_minibatches

            # Print the cost every epoch
            if print_cost == True and epoch % 10 == 0:
                print ("Cost after epoch %i: %f" % (epoch, minibatch_cost))
            if print_cost == True and epoch % 2 == 0:
                costs.append(minibatch_cost)

        # plot the cost
        plt.plot(np.squeeze(costs))
        plt.ylabel('cost')
        plt.xlabel('iterations (per tens)')
        plt.title("Learning rate =" + str(learning_rate))
        #plt.savefig('cost.png')
        plt.show()

        # save the parameters in a variable
        parameters = sess.run(parameters)
        print("Parameters have been trained!")

        # Calculate the correct predictions
        correct_prediction = tf.equal(tf.argmax(Z3, 1), tf.argmax(Y, 1))

        # Calculate accuracy on the test set
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

        print("Train Accuracy:", accuracy.eval({X: X_train, Y: Y_train}))
        print("Test Accuracy:", accuracy.eval({X: X_test, Y: Y_test}))

        return parameters
