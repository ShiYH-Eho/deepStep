#coding=utf-8
import math
from xml.dom.minidom import parse
import xml.dom.minidom
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

roadType = '''motorway, trunk, primary, secondary, tertiary, unclassified, residential'''
#motorway_link, trunk_link, primary_link, secondary_link, living_street'''
roadType = roadType.split(',')
for i in range(len(roadType)):
	roadType[i] = roadType[i].strip()

def readXml(name):
	xmlDom = xml.dom.minidom.parse(name)
	mMap = xmlDom.documentElement
	return mMap

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
	timeStamp = posFind(int(t),T,startTime,timeUnit)
	return timeStamp

def getNodeByPos(lon,lat,netNodeInfo):
	[x,y] = getPos(lon,lat)
	targetNode = ''
	mDis = -1
	rangeX = [x]
	rangeY = [y]
	tx = 0
	ty = 0
	'''
	if x == 0:
		rangeX = [0,1]
	elif x == W:
		rangeX = [W - 1,W]
	else:
		rangeX = [x - 1,x,x + 1]
	if y == 0:
		rangeY = [0,1]
	elif y == H:
		rangeY = [H - 1,H]
	else:
		rangeY = [y - 1,y,y + 1]
	'''
	for mx in rangeX:
		for my in rangeY:
			for nodeId in netNodeInfo[mx][my]:
				t = dis(lon,lat,netNodeInfo[mx][my][nodeId][0],netNodeInfo[mx][my][nodeId][1])
				if mDis > t or mDis == -1:
					tx = mx
					ty = my
					mDis = t
					targetNode = nodeId
	#print '%s src:%s dst:%s dis:%f' % (targetNode,str([lon,lat]),str(netNodeInfo[tx][ty][targetNode]),mDis)
	return targetNode

def getWayByPos(lon,lat,netWayInfo,wayNodeInfo,nodeInfo):
	lon = float(lon)
	lat = float(lat)
	[x,y] = getPos(lon,lat)
	targetWay = ''
	mDis = 1
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
			A = y2 - y1
			B = x1 - x2
			C = y1*(x2-x1)-x1*(y2-y1)
			x0 = (B**2 * lon - A*B*lat - A*C) / (A**2 + B**2)
			y0 = (A**2 * lat - A*B*lon - B*C) / (A**2 + B**2)
			t = dis(lon,lat,x0,y0)
			if t < mDis:
				mDis = t
				targetWay = wayId
	#print 'targetWay:%s dis:%s' % (targetWay,mDis)
	return targetWay


def dis(lon1, lat1, lon2, lat2):
	lon1, lat1, lon2, lat2 = map(math.radians, [float(lon1), float(lat1), float(lon2), float(lat2)])
	# haversine公式
	dlon = lon2 - lon1 
	dlat = lat2 - lat1 
	a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
	c = 2 * math.asin(math.sqrt(a)) 
	r = 6371 # 地球平均半径，单位为公里
	return c * r

