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
sum = 0
for item1 in netMark:
	for item2 in item1:
		for num in item2:
			sum += num

print sum