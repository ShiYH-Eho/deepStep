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

def getWayByPos(lon,lat):
	lon = float(lon)
	lat = float(lat)
	[x,y] = getPos(lon,lat)
	targetWay = ''
	mDis = 1
	if x < 0 or y < 0 or x >= W or y >= H:
		return ''
	for wayId in netWayInfo[x][y]:
		wayDis = 1
		for i in range(len(wayNodeInfo[wayId]) - 1):
			id1 = wayNodeInfo[wayId][i]
			id2 = wayNodeInfo[wayId][i + 1]
			if id1 not in nodeInfo or id2 not in nodeInfo:
				print 'way_node info error'
				continue;
			[x1,y1] = nodeInfo[id1]
			[x2,y2] = nodeInfo[id2]
			x1 = float(x1)
			y1 = float(y1)
			x2 = float(x2)
			y2 = float(y2)
			'''
			xmin = min(x1,x2)
			xmax = max(x1,x2)
			ymin = min(y1,y2)
			ymax = max(y1,y2)
			'''
			A = y2 - y1
			B = x1 - x2
			C = y1*(x2-x1)-x1*(y2-y1)
			x0 = (B**2 * lon - A*B*lat - A*C) / (A**2 + B**2)
			y0 = (A**2 * lat - A*B*lon - B*C) / (A**2 + B**2)
			t = mDis
		#	if x < xmin or x > xmax or y < ymin or y > ymax:
		#		t = min(dis(lon,lat,x1,y1),dis(lon,lat,x2,y2))
			#else:
			t = dis(lon,lat,x0,y0)
			if t < mDis:
				mDis = t
				targetWay = wayId
	#print 'targetWay:%s dis:%s' % (targetWay,mDis)
	return targetWay

roadSpeedList = {}

savePath = '../data/traffic_%dmin_%d*%d' % (timeUnit / 60,H,W)
#savePath = '../data/speed_%dmin_%d*%d' % (timeUnit / 60,H,W)
if not os.path.exists(savePath):
	os.mkdir(savePath)

def orderToSpeed(orderList,startTime):
	newList = sorted(orderList,key = lambda x : x[2])
	speedList = []
	mList = []
	t = int(math.floor((int(newList[0][2]) - startTime) / timeUnit))
	wayId = getWayByPos(newList[0][3],newList[0][4])
	timeStamp = t
	targetWay = wayId
	wayCount = {}
	for i in range(len(newList) - 1):
		#t = 
		t = int(math.floor((int(newList[i][2]) - startTime) / timeUnit))
		wayId = getWayByPos(newList[i][3],newList[i][4])
		if wayId not in wayCount:
			wayCount[wayId] = 0
		wayCount[wayId] += 1
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
			#print 'related way:%s' % wayNameInfo[targetWay]
			mList.append(speed)
		elif len(mList) < 1 or wayCount[targetWay] < 3:
			targetWay = wayId
			timeStamp = t
			mList = [speed]
		else:
			#print 'related way:%s' % wayNameInfo[targetWay]
			speedMean = np.mean(mList)
			speedList.append([timeStamp,targetWay,speedMean])
			targetWay = wayId
			timeStamp = t
			mList = [speed]
			
	if len(mList) >= 1:
		speedMean = np.mean(mList)
		speedList.append([timeStamp,wayId,speedMean])
	return speedList

def orderToTraffic(newList,startTime):
	wayList = {}
	mList = []
	lenth = len(newList)
	start = 0
	end = lenth - 1
	way1 = getWayByPos(newList[start][3],newList[start][4])
	way2 = getWayByPos(newList[end][3],newList[end][4])
	t1 = int(math.floor((int(newList[start][2]) - startTime) / timeUnit))
	t2 = int(math.floor((int(newList[end][2]) - startTime) / timeUnit))
	if t2 < 0:
		t2 = 0
	elif t2 >= T:
		t2 = T - 1
	if t1 < 0:
		t1 = 0
	elif t1 >= T:
		t1 = T - 1
	if way1 == way2 and t1 == t2:
		#print 'related way:%s' % wayNameInfo[way1]
		wayList[way1 + ',' + str(t1)] = lenth
	else:
		wayList1 = orderToTraffic(newList[0:lenth / 2],startTime)
		wayList2 = orderToTraffic(newList[lenth/2:],startTime)
		for key in wayList1:
			if key not in wayList:
				wayList[key] = 0
			wayList[key] += wayList1[key]
		for key in wayList2:
			if key not in wayList:
				wayList[key] = 0
			wayList[key] += wayList2[key]
	#wayList = list(set(wayList))
	return wayList

def dataToTraffic(filename):
	trafficGraph = {}
	f = open(filename,'r')
	count = -1
	size = 0
	data = ''# f.readline().split(',')
	orderId = ''
	wayTimeMark = {}
	wayCount = {}
	startTime = timeStart + (60*60*24) * (int(filename[-2:]) - 1) + (60*60*24*31) * int(filename[-3:-2])
	for line in f.readlines():
		data = line.split(',')
		count += 1
		if len(data) != 5:#or count % 3 != 0:
			continue
		if count % 10000 == 0:
			count = 0
			size += 1
			print '%d.handle message of %s' % (size,data[0])
		#count += 1
		t = int(math.floor((int(data[2]) - startTime) / timeUnit))
		wayId = getWayByPos(float(data[3]),float(data[4]))
		if wayId == '':
			continue
		if t < 0:
			t = 0
		elif t >= T:
			t = T - 1

		if orderId != data[1]:
			orderId = data[1]
			wayTimeMark = {}
			wayCount = {}
		
		if wayId not in wayCount:
			wayCount[wayId] = 0
		wayCount[wayId] += 1
		if wayCount[wayId] < 3:
			continue
		
		if wayId not in wayTimeMark:
			wayTimeMark[wayId] = [False for i in range(T)]
		if wayId not in trafficGraph:
			trafficGraph[wayId] = [0 for i in range(T)]
		if not wayTimeMark[wayId][t]:
			#print 'related way:%s' % wayNameInfo[wayId]
			trafficGraph[wayId][t] += 1
		wayTimeMark[wayId][t] = True
	f.close()
	toWrite = json.dumps(trafficGraph,indent = 4)
	print 'Writing file %s' % filename
	f = open(savePath + '/traffic_%s' % (filename[-4:]),'w')
	f.write(toWrite)


'''
def dataToTraffic(filename):
	trafficGraph = {}
	f = open(filename,'r')
	count = -1
	size = 0
	data = f.readline().split(',')
	orderId = data[1]
	orderList = [data]
	wayTimeMark = {}
	wayCount = {}
	startTime = timeStart + (60*60*24) * (int(filename[-2:]) - 1) + (60*60*24*31) * int(filename[-3:-2])
	for line in f.readlines():
		data = line.split(',')
		count += 1
		if len(data) != 5:
			continue
		if count % 10000 == 0:
			count = 0
			size += 1
			print '%d.handle message of %s' % (size,data[0])
		if orderId == data[1]:
			orderList.append(data)
		else:
			newList = sorted(orderList,key = lambda x : x[2])
			infoList = orderToTraffic(newList,startTime)
			for item in infoList:
				if infoList[item] < 4:
					continue
				[wayId,t] = item.split(',')
				if wayId not in trafficGraph:
					trafficGraph[wayId] = [0 for i in range(T)]
				trafficGraph[wayId][int(t)] += 1
			orderList = [data]
			orderId = data[1]
	f.close()
	if len(orderList) >= 1:
		newList = sorted(orderList,key = lambda x : x[2])
		infoList = orderToTraffic(newList,startTime)
		for item in infoList:
			if infoList[item] < 4:
				continue
			[wayId,t] = item.split(',')
			#print 'related way:%s' % wayNameInfo[wayId]
			if wayId not in trafficGraph:
				trafficGraph[wayId] = [0 for i in range(T)]
			trafficGraph[wayId][int(t)] += 1
	
	toWrite = json.dumps(trafficGraph,indent = 4)
	print 'Writing file %s' % filename
	f = open(savePath + '/traffic_%s' % (filename[-4:]),'w')
	f.write(toWrite)
'''
def dataToSpeed(filename):
	trafficGraph = {}
	f = open(filename,'r')
	count = 0
	size = 0
	data = f.readline().split(',')
	orderId = data[1]
	orderList = [data]
	startTime = timeStart + (60*60*24) * (int(filename[-2:]) - 1) + (60*60*24*31) * int(filename[-3:-2])
	for line in f.readlines():
		data = line.split(',')
		if len(data) != 5:
			continue
		if count % 10000 == 0:
			count = 0
			size += 1
			print '%d.handle message of %s' % (size,data[1])
		if orderId == data[1]:
			orderList.append(data)
		else:
			if len(orderList) <= 1:
				continue
			speedList = orderToSpeed(orderList,startTime)
			for speedInfo in speedList:
				t = speedInfo[0]
				mWay = speedInfo[1]
				mSpeed = float(speedInfo[2])
				if mWay not in trafficGraph:
					trafficGraph[mWay] = [[] for i in range(T)]
				trafficGraph[mWay][t].append(mSpeed)
			orderId = data[1]
			orderList = [data]
		count += 1
	f.close()
	if len(orderList) > 1:
		speedList = orderToSpeed(orderList,startTime)
		for speedInfo in speedList:
			t = speedInfo[0]
			mWay = speedInfo[1]
			mSpeed = float(speedInfo[2])
			if mWay not in trafficGraph:
				trafficGraph[mWay] = [[] for i in range(T)]
			trafficGraph[mWay][t].append(mSpeed)
	
	for way in trafficGraph:
		for t in range(T):
			if len(trafficGraph[way][t]) < 1:
				trafficGraph[way][t] = -1
			else:
				trafficGraph[way][t] = np.mean(trafficGraph[way][t])
	toWrite = json.dumps(trafficGraph,indent = 4)
	print 'Writing file %s' % filename
	f = open(savePath + '/speed_%s' % (filename[-4:]),'w')
	f.write(toWrite)
	#np.savetxt(savePath + '/traffic_%s' % (filename[-4:]), toWrite,fmt = '%d')

#dataToSpeed('../data/20161013')
#dataToTraffic('../data/20161013')
'''
for i in range(31,32):
	#dataToSpeed('../data/gps/gps_201610%02d' % i)
	dataToTraffic('../data/gps/gps_201610%02d' % i)
'''
for i in range(7,8):
	#dataToSpeed('../data/gps/gps_201611%02d' % i)
	dataToTraffic('../data/gps/gps_201611%02d' % i)

