#coding=utf-8
import math

def dis(x,y):
	return sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)

def getGradient(nodeList):
	node1 = nodeList[0]
	node2 = nodeList[0]
	t = 0
	for node in nodeList:
		mDis = dis(node1,node)
		if mDis > t:
			t = mDis
			node2 = node
	for node in nodeList:
		mDis = dis(node2,node)
		if mDis > t:
			t = mDis
			node1 = node
	return (node1[1] - node2[1]) / (node1[0] - node2[0])

def getRange(nodeList):
	nodeList.sort(key = lambda x : x[0],reverse = False)
	list1 = []
	list1.extend(nodeList)
	nodeList.sort(key = lambda x : x[1],reverse = False)
	list2 = nodeList
	return [list1[0][0],list1[-1][0]],[list2[0][1],list2[-1][1]]

def judgeInRoad(pos,roadRange):
	if pos[0] >= roadRange[0][0] and pos[0] <= roadRange[0][1] and pos[1] >= roadRange[1][0] and pos[1] <= roadRange[1][1]:
		return True
	return False

def getRoadPos(roadRange):
	x = (float(roadRange[0][0]) + float(roadRange[0][1])) / 2
	y = (float(roadRange[1][0]) + float(roadRange[1][1])) / 2
	return [x,y]