#!/usr/bin/env python
# -*- Python -*-

#
#  \file test_OutPortBase.py
#  \brief test for OutPortBase base class
#  \date $Date: 2007/09/19 $
#  \author Shinji Kurihara
# 
#  Copyright (C) 2003-2006
#      Task-intelligence Research Group,
#      Intelligent Systems Research Institute,
#      National Institute of
#          Advanced Industrial Science and Technology (AIST), Japan
#      All rights reserved.

import sys
sys.path.insert(1,"../")

import unittest
from OutPortBase import *

counter = 0

class PublisherTest:
	def __init__(self):
		global counter
		self.counter = counter
		counter+=1

	def update(self):
		print "update",self.counter

class TestOutPortBase(unittest.TestCase):
	def setUp(self):
		self._opb = OutPortBase("test")

	def test_name(self):
		self.assertEqual(self._opb.name(),"test")

	def test_case(self):
		self._opb.attach("test0",PublisherTest())
		self._opb.attach_front("test1",PublisherTest())
		self._opb.notify()
		self._opb.detach("test0")
		self._opb.notify()
		self._opb.detach("test1")
		self._opb.notify()
		self.assertEqual(self._opb.detach("test1"), None)



############### test #################
if __name__ == '__main__':
        unittest.main()
