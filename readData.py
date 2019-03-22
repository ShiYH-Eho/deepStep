#coding=utf-8
import numpy as np

timeUnit = 60 * 30
T = (60*60*24) / timeUnit
H = 32
W = 32
data = np.empty([T,H*W])

def read():
	global data
	for i in range(1,31):
		t = np.loadtxt('../data/traffic_30min_%d*%d/traffic_11%02d' % (H,W,i),dtype = int)
		data = np.concatenate((data,t))
	data = data[48:]
	return data
	

def readBatch(size):
	res1 = []
	res2 = []
	for i in range(size):
		pos = np.random.randint(48*30 - 12)
		a = data[pos:pos + 12]
		b = data[pos + 12]
		res1.append(a)
		res2.append(b)
	return [res1,res2]