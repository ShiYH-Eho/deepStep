#coding=utf-8
import xml.dom.minidom
from readRoadNet import *
import numpy as np
from const import *
from coordTransform_utils import *


netWay = readXml('../data/map/net_way.xml')
info = readNetWay(netWay)

size = 0
pos = []
for x in range(W):
	for y in range(H):
		if len(info[x][y]) > size:
			size = len(info[x][y])
			pos = [x,y]

print '%s : %s' % (str(pos),size)