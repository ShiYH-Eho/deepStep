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

def getNodeByPos(lon,lat,netNodeInfo):
	pos = getPos(lon,lat)
	targetNode = ''
	mDis = -1
	for nodeId in netNodeInfo[pos[0]][pos[1]]:
		t = dis(lon,lat,netNodeInfo[pos[0]][pos[1]][nodeId][1],netNodeInfo[pos[0]][pos[1]][nodeId][0])
		if mDis > t or mDis == -1:
			mDis = t
			targetNode = nodeId
	return targetNode

def dis(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(math.radians, [float(lon1), float(lat1), float(lon2), float(lat2)])
    # haversine公式
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    r = 6371 # 地球平均半径，单位为公里
    return c * r * 1000