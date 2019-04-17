#coding=utf-8
import xml.dom.minidom
from readRoadNet import *
import numpy as np
from const import *

mMap = readXml('../data/map/map.xml')
infoNodes = readNodes(mMap)
infoWays = readWays(mMap)
infoRelations = readRelations(mMap)
'''
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
'''
nodeNet = []
for i in range(W):
	nodeNet.append([])
	for j in range(H):
		nodeNet[i].append([])
for nodeId in infoNodes:
	[x,y] = getPos(infoNodes[nodeId][1],infoNodes[nodeId][0])
	if x < 0 or y < 0:
		continue
	nodeNet[x][y].append([nodeId,infoNodes[nodeId]])

dom1 = xml.dom.minidom.Document()
root1 = dom1.createElement('root')
dom1.appendChild(root1)

for i in range(W):
	for j in range(H):
		net = dom1.createElement('net')
		net.setAttribute('x',str(i))
		net.setAttribute('y',str(j))
		root1.appendChild(net)
		for node in nodeNet[i][j]:
			t = dom1.createElement('node')
			t.setAttribute('id',node[0])
			t.setAttribute('lat',node[1][0])
			t.setAttribute('lon',node[1][1])
			net.appendChild(t)

f = open('../data/map/net_node.xml','w')
dom1.writexml(f,indent='',addindent='\t',newl='\n',encoding='UTF-8')
f.close()

'''
dom1 = xml.dom.minidom.Document()
root1 = dom1.createElement('root')
dom1.appendChild(root1)

for wayId in infoWays:
	print 'Writing way %s' % wayId
	way = dom1.createElement('way')
	way.setAttribute('id',wayId)
	root1.appendChild(way)
	for nodeId in infoWays[wayId]:
		node = dom1.createElement('node')
		node.setAttribute('id',nodeId)
		node.setAttribute('lat',infoNodes[nodeId][0])
		node.setAttribute('lon',infoNodes[nodeId][1])
		way.appendChild(node)

f = open('../data/way_node.xml','w')
dom1.writexml(f,indent='',addindent='\t',newl='\n',encoding='UTF-8')
f.close()

dom2 = xml.dom.minidom.Document()
root2 = dom2.createElement('root')
dom2.appendChild(root2)

for relationId in infoRelations:
	print 'Writing relation %s' % relationId
	relation = dom2.createElement('relation')
	relation.setAttribute('id',relationId)
	root2.appendChild(relation)
	for wayId in infoRelations[relationId]:
		way = dom2.createElement('way')
		way.setAttribute('id',wayId)
		relation.appendChild(way)

f = open('../data/relation_way.xml','w')
dom2.writexml(f,indent='',addindent='\t',newl='\n',encoding='UTF-8')
f.close()

wayRelations = {}
for relationId in infoRelations:
	for wayId in infoRelations[relationId]:
		if wayId not in wayRelations:
			wayRelations[wayId] = []
		wayRelations[wayId].append(relationId)

dom3 = xml.dom.minidom.Document()
root3 = dom3.createElement('root')
dom3.appendChild(root3)

for wayId in wayRelations:
	print 'Writing way_relation %s' % wayId
	way = dom3.createElement('way')
	way.setAttribute('id',wayId)
	root3.appendChild(way)
	for relationId in wayRelations[wayId]:
		relation = dom3.createElement('relation')
		relation.setAttribute('id',relationId)
		way.appendChild(relation)

f = open('../data/way_relation.xml','w')
dom3.writexml(f,indent='',addindent='\t',newl='\n',encoding='UTF-8')
f.close()
'''