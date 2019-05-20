#coding=utf-8
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data 
import numpy as np
from const import *
import json
import readData

batchSize = 20

netMark = []
with open('../data/map/netMark.js') as f:
	netMark = json.load(f)
netTrans = []
with open('../data/map/netTrans.js') as f:
	netTrans = json.load(f)

def weight_variable(shape):
	initial = tf.truncated_normal(shape, stddev=0.1)
	return tf.Variable(initial)

def bias_variable(shape):
	initial = tf.constant(0.1, shape=shape)
	return tf.Variable(initial)

def conv3d(x, W, pad):
	return tf.nn.conv3d(x, W, strides=[1, 1, 1, 1, 1], padding=pad)

sess = tf.InteractiveSession()

x = tf.placeholder("float", [None, history, W, H, channelNum])
y_ = tf.placeholder("float", [None, W, H, channelNum])

W_time_1 = weight_variable([3, 1, 1, channelNum, 2 * channelNum])
b_time_1 = bias_variable([2 * channelNum])

#W_time_2 = weight_variable([5, 1, 1, 4 * channelNum, 4 * channelNum])
#b_time_2 = bias_variable([4 * channelNum])


W_spatial_1 = weight_variable([1, 3, 3, 2 * channelNum, 4 * channelNum])
b_spatial_1 = bias_variable([4 * channelNum])

#W_spatial_2 = weight_variable([1, 3, 3, 4 * channelNum, 2 * channelNum])
#b_spatial_2 = bias_variable([2 * channelNum])


W_spatial_temporal_1 = weight_variable([2, 2, 2, 4 * channelNum, 2 * channelNum])
b_spatial_temporal_1 = bias_variable([2 * channelNum])

#W_spatial_temporal_2 = weight_variable([3, 3, 3, 2 * channelNum, 2 * channelNum])
#b_spatial_temporal_2 = bias_variable([2 * channelNum])


W_output = weight_variable([history, 1, 1, 2 * channelNum, channelNum])
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
#dropout
W_netMark = tf.constant(netMark,dtype = tf.float32)
W_netTrans = tf.constant(netTrans,dtype = tf.float32)

h_flat = tf.reshape(h_output, [-1, W * H * channelNum])

#W_fc1 = weight_variable([W * H * channelNum, markChannelNum])
b_fc1 = bias_variable([markChannelNum])
h_fc1 = tf.nn.relu(tf.matmul(h_flat, W_netTrans) + b_fc1)

keep_prob = tf.placeholder("float")
h_drop = tf.nn.dropout(h_fc1, keep_prob)

W_fc2 = weight_variable([markChannelNum, W * H * channelNum])
b_fc2 = bias_variable([W * H * channelNum])

h_fc2 = tf.nn.relu(tf.matmul(h_drop, W_fc2) + b_fc2)

y_fc2 = tf.reshape(h_fc2,[-1,W,H,channelNum])

y = tf.multiply(y_fc2,W_netMark)

loss = tf.sqrt(tf.reduce_mean(tf.square(tf.subtract(y,y_))))
train_step = tf.train.AdamOptimizer(1e-4).minimize(loss)
lossValue = tf.divide(tf.reduce_sum(tf.abs(tf.subtract(y,y_))),tf.reduce_sum(y_))

sess.run(tf.initialize_all_variables())
for i in range(1,31):
	readData.readData('../data/traffic_30min_32*32/traffic_11%02d' % i)
for i in range(30000):
	batch = readData.readNetBatch(batchSize)
	#print('step %d' % i)
	
	if i%20 == 0:
		RMSE_loss = loss.eval(feed_dict={x:batch[0], y_: batch[1], keep_prob: 1.0})
		#print "step %d, RMSE_loss %g"%(i, RMSE_loss)
		loss_accuracy = lossValue.eval(feed_dict={x:batch[0], y_: batch[1], keep_prob: 1.0})
		print "step %d, RMSE_loss %-6g, training loss %g%%"%(i, RMSE_loss, loss_accuracy * 100)
	train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})
	'''
	if i%20 == 0:
		RMSE_loss = loss.eval(feed_dict={x:batch[0], y_: batch[1]})
		#print "step %d, RMSE_loss %g"%(i, RMSE_loss)
		loss_accuracy = lossValue.eval(feed_dict={x:batch[0], y_: batch[1]})
		print("step %d, RMSE_loss %-6g, training loss %g%%"%(i, RMSE_loss, loss_accuracy * 100))
	train_step.run(feed_dict={x: batch[0], y_: batch[1]})	
	'''
