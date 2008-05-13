#!/usr/bin/env python
# -*- Python -*-

#
#  \file  test_PublisherPeriodic.py
#  \brief test for PublisherPeriodic class
#  \date  $Date: 2007/09/28 $
#  \author Shinji Kurihara
# 
#  Copyright (C) 2006
#      Noriaki Ando
#      Task-intelligence Research Group,
#      Intelligent Systems Research Institute,
#      National Institute of
#          Advanced Industrial Science and Technology (AIST), Japan
#      All rights reserved.

import OpenRTM

import sys
sys.path.insert(1,"../")

import unittest

from PublisherPeriodic import *

class Consumer:
	def push(self):
		print "push"

class Property:
	def getProperty(self, id):
		return "1000"
	
class TestPublisherPeriodic(unittest.TestCase):

	def setUp(self):
		self._pp = PublisherPeriodic(Consumer(),Property())

	def test_case(self):
		import time
		time.sleep(1)
		self._pp.release()

############### test #################
if __name__ == '__main__':
        unittest.main()
