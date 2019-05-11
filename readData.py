#coding=utf-8
import numpy as np
import json
from const import *
from readRoadNet import *

timeUnit = 60 * 30
T = (60*60*24) / timeUnit
H = 32
W = 32
wayHash = json.load(open('../data/map/wayHash.js'))
mMap = readXml('../data/map/net_way.xml')
netWay = readNetWay(mMap)
data = {}

def readData(filename):
	global data
	wayMark = {}
	for wayId in wayHash:
		wayMark[wayId] = False
	with open(filename) as f:
		t = json.load(f)
		
		for key in t:
			if key == '':
				continue
			wayMark[key] = True
			if key not in data:
				data[key] = []
			data[key].extend(t[key])
		f.close()
	for wayId in wayMark:
		if not wayMark[wayId]:
			if wayId not in data:
				data[wayId] = []
			data[wayId].extend([0] * 48)
	return data
	#return data

def readNetBatch(size):
	res1 = []
	res2 = []
	
	for i in range(size):
		pos = np.random.randint(48 * 30 - history)
		#pos = np.random.randint(48*30 - history)
		t1 = [0] * history
		for j in range(history):
			t1[j] = [[] for k in range(W)]
			for k in range(W):
				t1[j][k] = [[] for l in range(H)]
				for l in range(H):
					t1[j][k][l] = [0 for m in range(channelNum)]
		t2 = [[] for j in range(W)]
		for j in range(W):
			#t1[j] = [[] for k in range(H)]
			t2[j] = [[] for k in range(H)]
			for k in range(H):
				#t1[j][k] = [0 for l in range(channelNum)]
				t2[j][k] = [0 for l in range(channelNum)]
		for j in range(W):
			for k in range(H):
				for wayId in netWay[j][k]:
					'''
					if wayId in data:
						t1[j][k].append(data[wayId][pos:pos + history])
						t2[j][k].append(data[wayId][pos + history])
					else:
						t1[j][k].append([0] * history)
						t2[j][k].append(0)
					'''
					for l in range(history):
						t1[l][j][k][wayHash[wayId]] = data[wayId][pos + l]
					t2[j][k][wayHash[wayId]] = data[wayId][pos + history]
		res1.append(t1)
		res2.append(t2)

	return [res1,res2]	

def readBatch(size):
	res1 = []
	res2 = []
	
	for i in range(size):
		pos = np.random.randint(48 - history)
		#pos = np.random.randint(48*30 - history)
		t1 = [[] for j in range(wayNum)]
		t2 = [[] for j in range(wayNum)]
		for wayId in data:
			t1[wayPos[wayId]] = data[wayId][pos:pos + history]
			t2[wayPos[wayId]] = data[wayId][pos + history]
		for j in range(wayNum):
			if len(t1[j]) == 0:
				t1[j] = [0 for k in range(history)]
				t2[j] = 0
		res1.append(t1)
		res2.append(t2)

	return [res1,res2]