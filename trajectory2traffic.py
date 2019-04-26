#coding=utf-8
import numpy as np
import math
import sys
import os
import json
from const import *
from readRoadNet import *

#nodeWay = readXml('../data/map/node_way.xml')
#netNode = readXml('../data/map/net_node.xml')
wayMap = readXml('../data/map/way.xml')
netWay = readXml('../data/map/net_way.xml')
nodeMap = readXml('../data/map/node.xml')
#nodeWayInfo = readNodeWay(nodeWay)
#netNodeInfo = readNetNode(netNode)
netWayInfo = readNetWay(netWay)
wayNameInfo = readWayName(wayMap)
wayNodeInfo = readWayNode(wayMap)
nodeInfo = readNode(nodeMap)


roadSpeedList = {}

savePath = '../data/speed_%dmin_%d*%d' % (timeUnit / 60,H,W)
if not os.path.exists(savePath):
	os.mkdir(savePath)

def handleOrder(orderList,startTime):
	newList = sorted(orderList,key = lambda x : x[2])
	speedList = []
	mList = []
	t = int(math.floor((int(newList[0][2]) - startTime) / timeUnit))
	wayId = getWayByPos(newList[0][3],newList[0][4],netWayInfo,wayNodeInfo,nodeInfo)
	timeStamp = t
	targetWay = wayId
	for i in range(len(newList) - 1):
		#t = 
		t = int(math.floor((int(newList[i][2]) - startTime) / timeUnit))
		wayId = getWayByPos(newList[i][3],newList[i][4],netWayInfo,wayNodeInfo,nodeInfo)
		#print 'related way:%s' % wayNameInfo[wayId]
		#print '-----------------------------------------------------------------'
		#print '%s '
		if t < 0:
			t = 0
		elif t >= T:
			t = T - 1
		deltaT = int(newList[i + 1][2]) - int(newList[i][2])
		distance = dis(float(newList[i][3]),float(newList[i][4]),float(newList[i + 1][3]),float(newList[i + 1][4]))
		speed = distance / deltaT * 3600
		if t == timeStamp and targetWay == wayId:
			mList.append([t,wayId,speed])
		else:
			sum = 0.0
			for item in mList:
				sum += item[2]
			sum /= len(mList)
			speedList.append([timeStamp,wayId,sum])
			targetWay = wayId
			timeStamp = t
			mList = [[t,wayId,speed]]
	if len(mList) != 1:
		sum = 0.0
		for item in mList:
			sum += item[2]
		sum /= len(mList)
		speedList.append([timeStamp,wayId,sum])
	return speedList

def handleData(filename):
	trafficGraph = np.zeros((T,W,H),dtype = int)
	f = open(filename,'r')
	count = 0
	size = 0
	orderId = ''
	tSet = []
	startTime = timeStart + (60*60*24) * (int(filename[-2:]) - 1) + (60*60*24*31) * int(filename[-3:-2])
	for line in f.readlines():
		data = line.split(',')
		if count % 100000 == 0:
			count = 0
			size += 1
			print '%d.handle message of %s' % (size,data[0])
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
	trafficGraph = []
	for i in range(T):
		trafficGraph.append({})
	f = open(filename,'r')
	count = 0
	size = 0
	data = f.readline().split(',')
	orderId = data[1]
	orderList = [data]
	startTime = timeStart + (60*60*24) * (int(filename[-2:]) - 1) + (60*60*24*31) * int(filename[-3:-2])
	for line in f.readlines():
		data = line.split(',')
		if count % 1 == 0:
			count = 0
			size += 1
			print '%d.handle message of %s' % (size,data[1])
		if orderId == data[1]:
			orderList.append(data)
		else:
			speedList = handleOrder(orderList,startTime)
			for speedInfo in speedList:
				t = speedInfo[0]
				mWay = speedInfo[1]
				mSpeed = float(speedInfo[2])
				trafficGraph[t][mWay] = mSpeed
			orderId = data[1]
			orderList = [data]
		count += 1
	f.close()
	if len(orderList) != 1:
		speedList = handleOrder(orderList,startTime)
		for speedInfo in speedList:
			t = speedInfo[0]
			mWay = speedInfo[1]
			mSpeed = float(speedInfo[2])
			trafficGraph[t][mWay] = mSpeed
	toWrite = json.dumps(trafficGraph)
	print 'Writing file %s' % filename
	f = open(savePath + '/speed_%s' % (filename[-4:]),'w')
	f.write(toWrite)
	#np.savetxt(savePath + '/traffic_%s' % (filename[-4:]), toWrite,fmt = '%d')

dataToSpeed('../data/20161013')
'''
for i in range(1,32):
	dataToSpeed('../data/gps/gps_201610%02d' % i)
	#handleData('../data/gps/gps_201610%02d' % i)

for i in range(1,31):
	dataToSpeed('../data/gps/gps_201611%02d' % i)
	#handleData('../data/gps/gps_201611%02d' % i)
'''