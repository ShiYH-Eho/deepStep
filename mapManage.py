#coding=utf-8
import xml.dom.minidom
from readRoadNet import *
import numpy as np
from const import *
from coordTransform_utils import *

mMap = readXml('../data/map/map.xml')

dom1 = xml.dom.minidom.Document()
root1 = dom1.createElement('root')
dom1.appendChild(root1)

nodeList = []

ways = mMap.getElementsByTagName('way')

for way in ways:
	tags = way.getElementsByTagName('tag')
	isRoad = False
	hasName = False
	newWay = dom1.createElement('way')
	wayId = way.getAttribute('id')
	newWay.setAttribute('id',wayId)
	
	for tag in tags:
		newTag = dom1.createElement('tag')

		k = tag.getAttribute('k').encode('utf-8')
		v = tag.getAttribute('v').encode('utf-8')
		
		newTag.setAttribute('k',k)
		newTag.setAttribute('v',v)
		newWay.appendChild(newTag)
		if k == 'highway':
			for item in roadType:
				if v == item:
					isRoad = True
		if k == 'name':
			hasName = True
	if not isRoad or not hasName:
		continue
	print 'get way %s' % wayId
	nds = way.getElementsByTagName('nd')
	for nd in nds:
		ndId = nd.getAttribute('ref')
		nodeList.append(ndId)
		newNd = dom1.createElement('nd')
		newNd.setAttribute('ref',ndId)
		newWay.appendChild(newNd)
	root1.appendChild(newWay)

f = open('../data/map/way.xml','w')
dom1.writexml(f,indent='',addindent='\t',newl='\n',encoding='UTF-8')
f.close()

dom1 = xml.dom.minidom.Document()
root1 = dom1.createElement('root')
dom1.appendChild(root1)

nodes = mMap.getElementsByTagName('node')
for node in nodes:
	nodeId = node.getAttribute('id')
	if nodeId not in nodeList:
		continue
	lon = node.getAttribute('lon')
	lat = node.getAttribute('lat')
	[gcj_lon,gcj_lat] = wgs84_to_gcj02(float(lon),float(lat))
	newNode = dom1.createElement('node')
	newNode.setAttribute('id',nodeId)
	newNode.setAttribute('lon',str(gcj_lon))
	newNode.setAttribute('lat',str(gcj_lat))
	root1.appendChild(newNode)
	print 'get node %s' % nodeId

f = open('../data/map/node.xml','w')
dom1.writexml(f,indent='',addindent='\t',newl='\n',encoding='UTF-8')
f.close()


