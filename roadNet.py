#code=utf-8
from xml.dom.minidom import parse
import xml.dom.minidom

def readXml(name):
   xmlDom = xml.dom.minidom.parse(name)
   mMap = xmlDom.documentElement
   return mMap

def readNodes(mMap):
   nodes = mMap.getElementsByTagName("node")
   infoNode = {}
   for node in nodes:
      id = node.getAttribute('id')
      lat = node.getAttribute('lat')
      lon = node.getAttribute('lon')
      infoNode[id] = [lat,lon]
   return infoNode
 
def readWays(mMap):
   ways = mMap.getElementsByTagName("way")
   infoWay = {}
   for way in ways:
      wayId = way.getAttribute('id')
      infoWay[wayId] = []
      nds = way.getElementsByTagName('nd')
      for nd in nds:
         infoWay[wayId].append(nd.getAttribute('ref'))
   return infoWay

def readRelations(mMap):
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