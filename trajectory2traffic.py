#coding=utf-8
import numpy as np
import math
timeStart = 1477929600

latStart = 30.649
latEnd = 30.731
lonStart = 104.039
lonEnd = 104.131

H = 32
W = 32

latUnit = (latEnd - latStart) / H
lonUnit = (lonEnd - lonStart) / W
timeUnit = 60 * 30

T = (60*60*24) / timeUnit

def divFind(target,size,dataStart,dataUnit):
	res = math.floor((target - dataStart) / dataUnit)
	if res < 0 or res >= size:
		print 'out of range error %s' % target
		return -1
	return int(res)

def getPos(lon,lat):
	x = divFind(lon,W,lonStart,lonUnit)
	y = divFind(lat,H,latStart,latUnit)
	return [x,y]

def getTimeStamp(t,startTime):
	timeStamp = divFind(t,T,startTime,timeUnit)
	return timeStamp

def handleData(filename):
	trafficGraph = np.zeros((T,W,H),dtype = int)
	f = open(filename,'r')
	count = 0
	size = 0
	for line in f.readlines():
		data = line.split(',')
		if count % 100000 == 0:
			count = 0
			size += 1
			print '%d.handle message of %s' % (size,data[0])
		startTime = timeStart + (60*60*24) * (int(filename[-2:]) - 1)
		t = getTimeStamp(int(data[2]),startTime)
		pos = getPos(float(data[3]),float(data[4]))
		if t < 0 or pos[0] < 0 or pos[1] < 0:
			print 'error: %s' % str(data)
			continue
		trafficGraph[t][pos[0]][pos[1]] += 1
		count += 1
	f.close()
	toWrite = trafficGraph.reshape(T,W*H)
	print 'Writing file %s' % filename
	np.savetxt('../data/traffic_%s' % filename[-4:], toWrite,fmt = '%d')

for i in range(1,31):
	handleData('../data/wgs84_201611%02d' % i)
