#coding=utf-8
import xml.dom.minidom
from readRoadNet import *
import numpy as np
from const import *
from coordTransform_utils import *
from readData import *
import json
import tensorflow as tf

netMark = []
with open('../data/map/netMark.js') as f:
	netMark = json.load(f)
netTrans = [[] for i in range(W*H*channelNum)]
for i in range(W*H*channelNum):
	netTrans[i] = [0 for j in range(markChannelNum)]
#print netTrans
pos = 0
for i in range(W):
	for j in range(H):
		for k in range(channelNum):
			if netMark[i][j][k] == 0:
				continue
			netTrans[i * H * channelNum + j * channelNum + k][pos] = 1
			print pos
			pos += 1
toWrite = json.dumps(netTrans)
f = open('../data/map/netTrans.js','w')
f.write(toWrite)
f.close()