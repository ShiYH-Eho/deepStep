#coding=utf-8
import xml.dom.minidom
from readRoadNet_new import *
import numpy as np
from const_new import *

nodeMap = readXml('../../data/map/node.xml')
wayMap = readXml('../../data/map/way.xml')
infoNodes = readNode(nodeMap) #dict
infoWays = readWayNode(wayMap) #dict

#node-way
nodeWay = {}
nodeNet = {}

for wayId in infoWays:
	for nodeId in infoWays[wayId]:
		if nodeId not in nodeWay:
			nodeWay[nodeId] = []
		if wayId not in nodeWay[nodeId]:
			nodeWay[nodeId].append(wayId)

#net-node

netNode = []
for i in range(W):
	netNode.append([])
	for j in range(H):
		netNode[i].append({})
for nodeId in nodeWay:
	[x,y] = getPos(infoNodes[nodeId][0],infoNodes[nodeId][1])
	if x < 0 or y < 0:
		continue
	#netNode[x][y][nodeId] = infoNodes[nodeId]
	nodeNet[nodeId] = [x,y]

dom1 = xml.dom.minidom.Document()
root1 = dom1.createElement('root')
dom1.appendChild(root1)

for i in range(W):
	for j in range(H):
		net = dom1.createElement('net')
		net.setAttribute('x',str(i))
		net.setAttribute('y',str(j))
		#net.setAttribute('lon_range',"%f-%f"%(lonStart + lonUnit * i,lonStart + lonUnit * (i + 1)))
		#net.setAttribute('lat_range',"%f-%f"%(latStart + latUnit * j,latStart + latUnit * (j + 1)))
		root1.appendChild(net)
		for nodeId in netNode[i][j]:
			t = dom1.createElement('node')
			t.setAttribute('id',nodeId)
			t.setAttribute('lon',netNode[i][j][nodeId][0])
			t.setAttribute('lat',netNode[i][j][nodeId][1])
			net.appendChild(t)

f = open('../../data/map/net_node_new.xml','w')
dom1.writexml(f,indent='',addindent='\t',newl='\n',encoding='UTF-8')
f.close()


#net-way

dom1 = xml.dom.minidom.Document()
root1 = dom1.createElement('root')
dom1.appendChild(root1)

netWay = []
for i in range(W):
	netWay.append([])
	for j in range(H):
		netWay[i].append([])
	#netWay[i] = [[] for j in range[H]]

for wayId in infoWays:
	for i in range(len(infoWays[wayId]) - 1):
		node1 = infoWays[wayId][i]
		node2 = infoWays[wayId][i + 1]
		if (node1 not in nodeNet) or (node2 not in nodeNet):
			continue
		[x1,y1] = nodeNet[node1]
		[x2,y2] = nodeNet[node2]

		posList = DDA(x1,y1,x2,y2)
		for pos in posList:
			if wayId not in netWay[pos[0]][pos[1]]:
				netWay[pos[0]][pos[1]].append(wayId)
for i in range(W):
	for j in range(H):
		net = dom1.createElement('net')
		net.setAttribute('x',str(i))
		net.setAttribute('y',str(j))
		root1.appendChild(net)
		wayList = netWay[i][j]
		wayList.sort()
		for wayId in wayList:
			t = dom1.createElement('way')
			t.setAttribute('id',wayId)
			net.appendChild(t)

f = open('../../data/map/net_way_new.xml','w')
dom1.writexml(f,indent='',addindent='\t',newl='\n',encoding='UTF-8')
f.close()


#way-net
dom1 = xml.dom.minidom.Document()
root1 = dom1.createElement('root')
dom1.appendChild(root1)

wayNet = {}

for i in range(W):
	for j in range(H):
		for wayId in netWay[i][j]:
			if wayId not in wayNet:
				wayNet[wayId] = []
			wayNet[wayId].append([i,j])

for wayId in wayNet:
	way = dom1.createElement('way')
	way.setAttribute('id',wayId)
	root1.appendChild(way)
	for pos in wayNet[wayId]:
		net = dom1.createElement('net')
		net.setAttribute('x',str(pos[0]))
		net.setAttribute('y',str(pos[1]))
		way.appendChild(net)

f = open('../../data/map/way_net_new.xml','w')
dom1.writexml(f,indent='',addindent='\t',newl='\n',encoding='UTF-8')
f.close()

