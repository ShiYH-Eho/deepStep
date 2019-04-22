#coding=utf-8
import xml.dom.minidom
from readRoadNet import *
import numpy as np
from const import *

mMap = readXml('../data/map/net_way.xml')

count = {}

t = 0
pos = ''

nets = mMap.getElementsByTagName('net')
for net in nets:
	x = net.getAttribute('x')
	y = net.getAttribute('y')
	ways = net.getElementsByTagName('way')
	lenth = len(ways)
	if lenth > t:
		t = lenth
		pos = str([x,y])
print pos