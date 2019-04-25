#coding=utf-8
import xml.dom.minidom
from readRoadNet import *
import numpy as np
from const import *

nodeMap = readXml('../data/map/node.xml')
wayMap = readXml('../data/map/way.xml')
infoNodes = readNode(nodeMap) #dict
infoWays = readWayNode(wayMap) #dict

#node-way
nodeWay = {}

for wayId in infoWays:
	for nodeId in infoWays[wayId]:
		if nodeId not in nodeWay:
			nodeWay[nodeId] = []
		if wayId not in nodeWay[nodeId]:
			nodeWay[nodeId].append(wayId)

dom1 = xml.dom.minidom.Document()
root1 = dom1.createElement('root')
dom1.appendChild(root1)

for nodeId in nodeWay:
	node = dom1.createElement('node')
	node.setAttribute('id',nodeId)
	root1.appendChild(node)
	for wayId in nodeWay[nodeId]:
		t = dom1.createElement('way')
		t.setAttribute('id',wayId)
		node.appendChild(t)

f = open('../data/map/node_way.xml','w')
dom1.writexml(f,indent='',addindent='\t',newl='\n',encoding='UTF-8')
f.close()

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
	netNode[x][y][nodeId] = infoNodes[nodeId]

dom1 = xml.dom.minidom.Document()
root1 = dom1.createElement('root')
dom1.appendChild(root1)

for i in range(W):
	for j in range(H):
		net = dom1.createElement('net')
		net.setAttribute('x',str(i))
		net.setAttribute('y',str(j))
		net.setAttribute('lon_range',"%f-%f"%(lonStart + lonUnit * i,lonStart + lonUnit * (i + 1)))
		net.setAttribute('lat_range',"%f-%f"%(latStart + latUnit * j,latStart + latUnit * (j + 1)))
		root1.appendChild(net)
		for nodeId in netNode[i][j]:
			t = dom1.createElement('node')
			t.setAttribute('id',nodeId)
			t.setAttribute('lon',netNode[i][j][nodeId][0])
			t.setAttribute('lat',netNode[i][j][nodeId][1])
			net.appendChild(t)

f = open('../data/map/net_node.xml','w')
dom1.writexml(f,indent='',addindent='\t',newl='\n',encoding='UTF-8')
f.close()


#net-way

dom1 = xml.dom.minidom.Document()
root1 = dom1.createElement('root')
dom1.appendChild(root1)

for i in range(W):
	for j in range(H):
		net = dom1.createElement('net')
		net.setAttribute('x',str(i))
		net.setAttribute('y',str(j))
		root1.appendChild(net)
		wayList = []
		for nodeId in netNode[i][j]:
			for wayId in nodeWay[nodeId]:
				if wayId not in wayList:
					wayList.append(wayId)
		for wayId in wayList:
			t = dom1.createElement('way')
			t.setAttribute('id',wayId)
			net.appendChild(t)

f = open('../data/map/net_way.xml','w')
dom1.writexml(f,indent='',addindent='\t',newl='\n',encoding='UTF-8')
f.close()


