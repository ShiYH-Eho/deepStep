#coding=utf-8
import numpy as np
import math
import sys
import os
from const import *
from readRoadNet import *

nodeWay = readXml('../data/map/node_way.xml')
netNode = readXml('../data/map/net_node.xml')

nodeWayInfo = readNodeWay(nodeWay)
netNodeInfo = readNetNodes(netNode)

savePath = '../data/traffic_%dmin_%d*%d' % (timeUnit / 60,H,W)
if not os.path.exists(savePath):
	os.mkdir(savePath)

def handleData(filename):
	trafficGraph = np.zeros((T,W,H),dtype = int)
	f = open(filename,'r')
	count = 0
	size = 0
	orderId = ''
	tSet = []
	for line in f.readlines():
		data = line.split(',')
		if count % 100000 == 0:
			count = 0
			size += 1
			print '%d.handle message of %s' % (size,data[0])
		startTime = timeStart + (60*60*24) * (int(filename[-2:]) - 1) + (60*60*24*31) * int(filename[-3:-2])
		#t = getTimeStamp(int(data[2]),startTime)
		t = int(math.floor((int(data[2]) - startTime) / timeUnit))
		pos = getPos(float(data[3]),float(data[4]))
		if pos[0] < 0 or pos[1] < 0:
			print 'error: %s' % str(data)
			continue
		if orderId != data[1]:
			orderId = data[1]
			tSet = []
		if t < 0:
			t = 0
		elif t >= T:
			t = T - 1
		if t not in tSet:
			tSet.append(t)
			trafficGraph[t][pos[0]][pos[1]] += 1
		count += 1
	f.close()
	toWrite = trafficGraph.reshape(T,W*H)
	print 'Writing file %s' % filename
	np.savetxt(savePath + '/traffic_%s' % (filename[-4:]), toWrite,fmt = '%d')

def dataToSpeed(filename):
	trafficGraph = np.zeros((T,W,H),dtype = int)
	f = open(filename,'r')
	count = 0
	size = 0
	infoList = []
	orderId = ''
	tSet = []
	for line in f.readlines():
		data = line.split(',')
		if count % 100000 == 0:
			count = 0
			size += 1
			print '%d.handle message of %s' % (size,data[0])
		startTime = timeStart + (60*60*24) * (int(filename[-2:]) - 1) + (60*60*24*31) * int(filename[-3:-2])
		#t = getTimeStamp(int(data[2]),startTime)
		t = int(math.floor((int(data[2]) - startTime) / timeUnit))
		pos = getPos(float(data[3]),float(data[4]))
		if pos[0] < 0 or pos[1] < 0:
			print 'error: %s' % str(data)
			continue
		if orderId != data[1]:
			orderId = data[1]
			tSet = []
		if t < 0:
			t = 0
		elif t >= T:
			t = T - 1
		if t not in tSet:
			tSet.append(t)
			trafficGraph[t][pos[0]][pos[1]] += 1
		count += 1
	f.close()
	toWrite = trafficGraph.reshape(T,W*H)
	print 'Writing file %s' % filename
	np.savetxt(savePath + '/traffic_%s' % (filename[-4:]), toWrite,fmt = '%d')

for i in range(1,32):
	handleData('../data/gps/gps_201610%02d' % i)

for i in range(1,31):
	handleData('../data/gps/gps_201611%02d' % i)
