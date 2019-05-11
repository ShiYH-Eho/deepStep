#coding=utf-8
import xml.dom.minidom
from readRoadNet import *
import numpy as np
from const import *
from coordTransform_utils import *
from readData import *

modSize = channelNum
mMap = readXml('../data/map/way_net.xml')
wayNet = readWayNet(mMap)

mMap = readXml('../data/map/way.xml')
wayName = readWayName(mMap)

mMap = readXml('../data/map/net_way.xml')
netWay = readNetWay(mMap)

wayHash = {}

for wayId in wayName:
	wayHash[wayId] = int(wayId) % modSize

netMark = []

def changeHash(wayId):
	nets = wayNet[wayId]
	for i in range(modSize):
		find = True
		for net in nets:
			if netMark[net[0]][net[1]][i]:
				find = False
				break
		if find:
			wayHash[wayId] = i
			print 'deal wayId:%s' % wayId
			for net in nets:
				netMark[net[0]][net[1]][i] = True
			return True
	print 'NOT deal wayId:%s' % wayId
	return False

deal = False
while True:
	deal = True
	#print 'input c to continue'
	a = input('input 1 to continue:')
	if a != 1:
		break
	netMark = [[] for i in range(W)]
	for i in range(W):
		netMark[i] = [[] for j in range(H)]
		for j in range(H):
			netMark[i][j] = [False for k in range(modSize)]
	for wayId in wayHash:
		if wayId not in wayNet:
			continue
		order = wayHash[wayId]
		nets = wayNet[wayId]
		find = True
		for net in nets:
			[i,j] = net
			if netMark[i][j][order]:
				find = False
				print 'find net[%d,%d] wayId:%s' % (i,j,wayId)
				if not changeHash(wayId):
					deal = False
		if find:
			for net in nets:
				[i,j] = net
				netMark[i][j][order] = True
	a = input('input 2 to continue:')
	if deal:
		break

toWrite = json.dumps(wayHash)
f = open('../data/map/wayHash.js','w')
f.write(toWrite)
f.close()
'''

wayHash = {}
with open('../data/map/wayHash') as f:
	wayHash = json.load(f)
netMark = [[] for i in range(W)]
for i in range(W):
	netMark[i] = [[] for j in range(H)]
	for j in range(H):
		netMark[i][j] = [False for k in range(modSize)]

for wayId in wayHash:
	if wayId not in wayNet:
		continue
	order = wayHash[wayId]
	nets = wayNet[wayId]
	for net in nets:
		[i,j] = net
		if netMark[i][j][order]:
			print 'find net[%d,%d] wayId:%s' % (i,j,wayId)
		netMark[i][j][order] = True
'''