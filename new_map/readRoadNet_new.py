#coding=utf-8
from xml.dom.minidom import parse
from const_new import *
from coordTransform_utils import *
import xml.dom.minidom

def readNode(mMap):
   nodes = mMap.getElementsByTagName("node")
   infoNode = {}
   for node in nodes:
      nodeId = node.getAttribute('id')
      lat = node.getAttribute('lat')
      lon = node.getAttribute('lon')
      infoNode[nodeId] = [lon,lat]
   return infoNode

def readWayNode(mMap):
   ways = mMap.getElementsByTagName("way")
   infoWay = {}
   for way in ways:
      wayId = way.getAttribute('id')
      infoWay[wayId] = []
      nds = way.getElementsByTagName('nd')
      for nd in nds:
         infoWay[wayId].append(nd.getAttribute('ref'))
   return infoWay

def readWayTag(mMap):
   ways = mMap.getElementsByTagName("way")
   infoWay = {}
   for way in ways:
      wayId = way.getAttribute('id')
      infoWay[wayId] = {}
      tags = way.getElementsByTagName('tag')
      for tag in tags:
         k = tag.getAttribute('k')
         v = tag.getAttribute('v')
         infoWay[wayId][k] = v
   return infoWay

def readRelation(mMap):
   relations = mMap.getElementsByTagName("relation")
   infoRelation = {}
   for relation in relations:
      relationId = relation.getAttribute('id')
      infoRelation[relationId] = []
      members = relation.getElementsByTagName('member')
      for member in members:
         if member.getAttribute('type') != 'way':
            continue
         infoRelation[relationId].append(member.getAttribute('ref'))
   return infoRelation

def readNetNode(mMap):
   nets = mMap.getElementsByTagName('net')
   infoNet = []
   for i in range(W):
      infoNet.append([])
      for j in range(H):
         infoNet[i].append({})
   for net in nets:
      x = int(net.getAttribute('x'))
      y = int(net.getAttribute('y'))
      nodes = net.getElementsByTagName('node')
      for node in nodes:
         nodeId = node.getAttribute('id')
         lat = node.getAttribute('lat')
         lon = node.getAttribute('lon')
         infoNet[x][y][nodeId] = [lon,lat]
   return infoNet

def readNetWay(mMap):
   nets = mMap.getElementsByTagName('net')
   infoNet = []
   for i in range(W):
      infoNet.append([])
      for j in range(H):
         infoNet[i].append([])
   for net in nets:
      x = int(net.getAttribute('x'))
      y = int(net.getAttribute('y'))
      ways = net.getElementsByTagName('way')
      for way in ways:
         wayId = way.getAttribute('id')
         infoNet[x][y].append(wayId)
   for i in range(W):
      for j in range(H):
         infoNet[i][j].sort()
   return infoNet
   

def readNodeWay(mMap):
   nodes = mMap.getElementsByTagName('node')
   nodeWay = {}
   for node in nodes:
      nodeId = node.getAttribute('id')
      if nodeId not in nodeWay:
         nodeWay[nodeId] = []
      ways = node.getElementsByTagName('way')
      for way in ways:
         wayId = way.getAttribute('id')
         nodeWay[nodeId].append(wayId)
   return nodeWay
def readWayName(mMap):
   wayName = {}
   ways = mMap.getElementsByTagName('way')
   for way in ways:
      hasName = False
      wayId = way.getAttribute('id')
      tags = way.getElementsByTagName('tag')
      for tag in tags:
         k = tag.getAttribute('k')
         v = tag.getAttribute('v').encode('utf-8')
         if 'name' == k:
            wayName[wayId] = v
            hasName = True
      if not hasName:
         wayName[wayId] = '未命名'
   return wayName

def readWayNet(mMap):
   wayNet = {}
   ways = mMap.getElementsByTagName('way')
   for way in ways:
      wayId = way.getAttribute('id')
      nets = way.getElementsByTagName('net')
      wayNet[wayId] = []
      for net in nets:
         x = net.getAttribute('x')
         y = net.getAttribute('y')
         wayNet[wayId].append([int(x),int(y)])
   return wayNet






