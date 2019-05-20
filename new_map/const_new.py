#coding=utf-8
import math
from xml.dom.minidom import parse
import xml.dom.minidom
timeStart = 1475251200 #2016.10.1 0:00

latStart = 30.65
latEnd = 30.73
lonStart = 104.04
lonEnd = 104.13

wayNum = 1357
channelNum = 23
markChannelNum = 3173

history = 12

H = 800
W = 800

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

def getWayByPos(lon,lat,netWayInfo):
	lon = float(lon)
	lat = float(lat)
	[x,y] = getPos(lon,lat)
	if x < 0 or y < 0:
		return []
	targetWay = []
	mDis = 1
	xList = [0]
	yList = [0]
	for i in range(3):
		find = False
		for x_ in xList:
			for y_ in yList:
				if len(netWayInfo[x + x_][y + y_]) > 0:
					for wayId in netWayInfo[x + x_][y + y_]:
						#print wayId
						if wayId not in targetWay:
							targetWay.append(wayId)
					find = True
		if find:
			break
		xList.extend([-i-1,i+1])
		yList.extend([-i-1,i+1])
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

def DDA(x0,y0,x1,y1):
	dx = float(x1 - x0)
	dy = float(y1 - y0)
	xmin = min(x0,x1)
	xmax = max(x0,x1)
	ymin = min(y0,y1)
	ymax = max(y0,y1)
	res = []
	if x1 == x0:
		for i in range(ymin,ymax + 1):
			res.append([x0,i])
		return res
	elif y1 == y0:
		for i in range(xmin,xmax + 1):
			res.append([i,y0])
		return res
	k = dy/dx

	if k > 0:
		if k <= 1:
			y_ = ymin
			for i in range(xmin,xmax + 1):
				y_ += k
				res.append([i,int(round(y_))])
			return res
		else:
			x_ = xmin
			for i in range(ymin,ymax + 1):
				x_ += 1/k
				res.append([int(round(x_)),i])
			return res
	else:
		if k >= -1:
			y_ = ymax
			for i in range(xmin,xmax + 1):
				y_ += k
				res.append([i,int(round(y_))])
			return res
		else:
			x_ = xmax
			for i in range(ymin,ymax + 1):
				x_ += 1/k
				res.append([int(round(x_)),i])
			return res


