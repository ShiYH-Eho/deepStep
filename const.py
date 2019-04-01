#coding=utf-8
import math
timeStart = 1475251200 #2016.10.1 0:00

latStart = 30.65
latEnd = 30.73
lonStart = 104.04
lonEnd = 104.13

H = 32
W = 32

latUnit = (latEnd - latStart) / H
lonUnit = (lonEnd - lonStart) / W
timeUnit = 60 * 30
T = (60*60*24) / timeUnit

def posFind(target,size,dataStart,dataUnit):
	res = math.floor((target - dataStart) / dataUnit)
	if res < 0 or res >= size:
		print 'out of range error %s' % target
		return -1
	return int(res)

def getPos(lon,lat):
	x = posFind(float(lon),W,lonStart,lonUnit)
	y = posFind(float(lat),H,latStart,latUnit)
	return [x,y]

def getTimeStamp(t,startTime):
	timeStamp = posFind(t,T,startTime,timeUnit)
	return timeStamp

def dis(pos1,pos2):
	return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

