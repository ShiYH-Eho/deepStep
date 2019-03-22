#coding=utf-8
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data 
import numpy as np
import readData

H = 32
W = 32
k = 6
history = 12
batchSize = 12


def weight_variable(shape):
	initial = tf.truncated_normal(shape, stddev=0.1)
	return tf.Variable(initial)

def bias_variable(shape):
	initial = tf.constant(0.1, shape=shape)
	return tf.Variable(initial)

def conv3d(x, W, pad):
	return tf.nn.conv3d(x, W, strides=[1, 1, 1, 1, 1], padding=pad)

x = tf.placeholder("float", [None, history, H * W])
y_ = tf.placeholder("float", [None, H * W])

sess = tf.InteractiveSession()
#data = readData.read()

x_input = tf.reshape(x,[-1,history,H,W,1])


W_time_1 = weight_variable([4, 1, 1, 1, 128])
b_time_1 = bias_variable([128])
'''
W_time_2 = weight_variable([5, 1, 1, 256, 128])
b_time_2 = bias_variable([128])
'''
W_time_3 = weight_variable([history, 1, 1, 64, 2])
b_time_3 = bias_variable([2])

W_spatial_1 = weight_variable([1, 3, 3, 128, 128])
b_spatial_1 = bias_variable([128])
'''
W_spatial_2 = weight_variable([1, 3, 3, 128, 128])
b_spatial_2 = bias_variable([128])
'''

W_spatial_temporal_1 = weight_variable([3, 3, 3, 128, 64])
b_spatial_temporal_1 = bias_variable([64])
'''
W_spatial_temporal_2 = weight_variable([3, 3, 3, 128, 64])
b_spatial_temporal_2 = bias_variable([64])
'''
W_output = weight_variable([history, 1, 1, 2, 1])
b_output = bias_variable([1])

h_time_conv_1 = tf.nn.relu(conv3d(x_input,W_time_1,'SAME') + b_time_1)
h_spatial_conv_1 = tf.nn.relu(conv3d(h_time_conv_1, W_spatial_1,'SAME') + b_spatial_1)
h_spatial_temporal_conv_1 = tf.nn.relu(conv3d(h_spatial_conv_1, W_spatial_temporal_1,'SAME') + b_spatial_temporal_1)
'''
h_time_conv_2 = tf.nn.relu(conv3d(h_spatial_temporal_conv_1,W_time_2,'SAME') + b_time_2)
h_spatial_conv_2 = tf.nn.relu(conv3d(h_time_conv_2, W_spatial_2,'SAME') + b_spatial_2)
h_spatial_temporal_conv_2 = tf.nn.relu(conv3d(h_spatial_conv_2, W_spatial_temporal_2,'SAME') + b_spatial_temporal_2)
'''
h_time_conv_3 = tf.nn.relu(conv3d(h_spatial_temporal_conv_1,W_time_3,'VALID') + b_time_3)

W_fc1 = weight_variable([H * W * 2, 1024])
b_fc1 = bias_variable([1024])

h_flat = tf.reshape(h_time_conv_3, [-1, H*W*2])
h_fc1 = tf.nn.relu(tf.matmul(h_flat, W_fc1) + b_fc1)

keep_prob = tf.placeholder("float")
h_drop = tf.nn.dropout(h_fc1, keep_prob)

W_fc2 = weight_variable([1024, H*W])
b_fc2 = bias_variable([H*W])

#y = tf.nn.softmax(tf.matmul(h_drop, W_fc2) + b_fc2)


y = tf.nn.relu(tf.matmul(h_drop, W_fc2) + b_fc2)

loss = tf.sqrt(tf.divide(tf.reduce_sum(tf.square(tf.subtract(y,y_))),tf.reduce_sum(y_)))
#loss = tf.divide(tf.sqrt(tf.reduce_sum(tf.square(tf.subtract(y,y_)))),tf.reduce_sum(y_))
#loss = tf.divide(tf.reduce_sum(tf.divide(tf.abs(tf.subtract(y,y_)),y_)),batchSize)
#loss = tf.divide(tf.sqrt(tf.reduce_sum(tf.square(tf.subtract(y,y_)))),tf.reduce_sum(y_))
train_step = tf.train.AdamOptimizer(1e-4).minimize(loss)
accuracy = 1 - loss

sess.run(tf.initialize_all_variables())
readData.read()
for i in range(5000):
	batch = readData.readBatch(batchSize)
	if i%20 == 0:
		train_accuracy = accuracy.eval(feed_dict={x:batch[0], y_: batch[1], keep_prob: 1.0})
		print "step %d, training accuracy %g"%(i, train_accuracy)
		#print "step %d, training loss %g"%(i, train_accuracy)
	train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})	

#print "test accuracy %g"%accuracy.eval(feed_dict={x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0})

'''
correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
sess.run(tf.initialize_all_variables())
for i in range(1000):
	batch = mnist.train.next_batch(50)
	if i%100 == 0:
		train_accuracy = accuracy.eval(feed_dict={x:batch[0], y_: batch[1], keep_prob: 1.0})
		print "step %d, training accuracy %g"%(i, train_accuracy)
	train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})	

print "test accuracy %g"%accuracy.eval(feed_dict={x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0})
'''
