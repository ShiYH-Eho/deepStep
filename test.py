#coding=utf-8
import xml.dom.minidom
from readRoadNet import *
import numpy as np
from const import *
from coordTransform_utils import *
from readData import *

import tensorflow as tf 

a = tf.constant([1,2])
b = tf.constant([2,4])
c = tf.multiply(a, b)
sess = tf.Session()
print sess.run(c)
sess.close()