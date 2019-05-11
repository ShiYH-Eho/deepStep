#coding=utf-8
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data 
import numpy as np
from const import *
import readData

batchSize = 12


def weight_variable(shape):
	initial = tf.truncated_normal(shape, stddev=0.1)
	return tf.Variable(initial)

def bias_variable(shape):
	initial = tf.constant(0.1, shape=shape)
	return tf.Variable(initial)

def conv3d(x, W, pad):
	return tf.nn.conv3d(x, W, strides=[1, 1, 1, 1, 1], padding=pad)

#x = tf.placeholder("float", [None, history, H * W])
#y_ = tf.placeholder("float", [None, H * W])

x = tf.placeholder("float", [None, history, W, H, channelNum])
y_ = tf.placeholder("float", [None, W, H, channelNum])
sess = tf.InteractiveSession()

#x_input = tf.reshape(x,[-1,history,W,H,channelNum])
#y_ = tf.reshape(y_,[-1,W*H*channelNum])


W_time_1 = weight_variable([4, 1, 1, channelNum, 128])
b_time_1 = bias_variable([128])
'''
W_time_2 = weight_variable([5, 1, 1, 256, 128])
b_time_2 = bias_variable([128])
'''
#W_time_3 = weight_variable([history, 1, 1, 64, 2])
#b_time_3 = bias_variable([2])

#W_time_3 = weight_variable([history, 1, 1, 64, channelNum])
#b_time_3 = bias_variable([channelNum])

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

W_output = weight_variable([history, 1, 1, 64, channelNum])
b_output = bias_variable([channelNum])

h_time_conv_1 = tf.nn.relu(conv3d(x,W_time_1,'SAME') + b_time_1)
h_spatial_conv_1 = tf.nn.relu(conv3d(h_time_conv_1, W_spatial_1,'SAME') + b_spatial_1)
h_spatial_temporal_conv_1 = tf.nn.relu(conv3d(h_spatial_conv_1, W_spatial_temporal_1,'SAME') + b_spatial_temporal_1)
'''
h_time_conv_2 = tf.nn.relu(conv3d(h_spatial_temporal_conv_1,W_time_2,'SAME') + b_time_2)
h_spatial_conv_2 = tf.nn.relu(conv3d(h_time_conv_2, W_spatial_2,'SAME') + b_spatial_2)
h_spatial_temporal_conv_2 = tf.nn.relu(conv3d(h_spatial_conv_2, W_spatial_temporal_2,'SAME') + b_spatial_temporal_2)
'''

h_output = tf.nn.relu(conv3d(h_spatial_temporal_conv_1,W_output,'VALID') + b_output)
'''
W_fc1 = weight_variable([W * H * channelNum, 1024])
b_fc1 = bias_variable([1024])

h_flat = tf.reshape(h_time_conv_3, [-1, W * H * channelNum])
h_fc1 = tf.nn.relu(tf.matmul(h_flat, W_fc1) + b_fc1)

keep_prob = tf.placeholder("float")
h_drop = tf.nn.dropout(h_fc1, keep_prob)

W_fc2 = weight_variable([1024, W * H * channelNum])
b_fc2 = bias_variable([W * H * channelNum])

y = tf.nn.relu(tf.matmul(h_drop, W_fc2) + b_fc2 + 0.5)
y = tf.reshape(y,[-1,W,H,channelNum])
'''
h_flat = tf.reshape(h_output, [-1, W * H * channelNum])

W_fc1 = weight_variable([W * H * channelNum, 1024])
b_fc1 = bias_variable([1024])
h_fc1 = tf.nn.relu(tf.matmul(h_flat, W_fc1) + b_fc1)

keep_prob = tf.placeholder("float")
h_drop = tf.nn.dropout(h_fc1, keep_prob)

W_fc2 = weight_variable([1024, W * H * channelNum])
b_fc2 = bias_variable([W * H * channelNum])

y = tf.nn.relu(tf.matmul(h_drop, W_fc2) + b_fc2 + 0.5)
y = tf.reshape(y,[-1,W,H,channelNum])

loss = tf.sqrt(tf.reduce_mean(tf.square(tf.subtract(y,y_))))
train_step = tf.train.AdamOptimizer(1e-4).minimize(loss)
lossValue = tf.divide(tf.reduce_sum(tf.abs(tf.subtract(y,y_))),tf.reduce_sum(y_))
#accuracy = 1 - tf.reduce_sum(tf.divide(tf.abs(tf.subtract(y,y_)),y_))
sess.run(tf.initialize_all_variables())
for i in range(1,31):
	readData.readData('../data/traffic_30min_32*32/traffic_11%02d' % i)
for i in range(5000):
	batch = readData.readNetBatch(batchSize)
	if i%20 == 0:
		#train_accuracy = accuracy.eval(feed_dict={x:batch[0], y_: batch[1], keep_prob: 1.0})
		#print "step %d, training accuracy %g"%(i, train_accuracy)
		loss_accuracy = lossValue.eval(feed_dict={x:batch[0], y_: batch[1], keep_prob: 1.0})
		print "step %d, training loss %g%%"%(i, loss_accuracy * 100)
	train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})	

