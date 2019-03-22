#coding=utf-8
import xml.dom.minidom
from roadNet import *
import readData
import numpy as np

for i in range(30):
	print np.random.randint(100)
'''
mMap = readXml('../data/chengduMap.xml')
infoNodes = readNodes(mMap)
infoWays = readWays(mMap)
infoRelations = readRelations(mMap)

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