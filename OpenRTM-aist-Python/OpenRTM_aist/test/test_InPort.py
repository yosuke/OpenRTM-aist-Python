#!/usr/bin/env python
# -*- Python -*-


#  \file test_InPort.py
#  \brief test for InPort template class
#  \date $Date: 2007/09/20 $
#  \author Shinji Kurihara
# 
#  Copyright (C) 2003-2005
#      Task-intelligence Research Group,
#      Intelligent Systems Research Institute,
#      National Institute of
#          Advanced Industrial Science and Technology (AIST), Japan
#      All rights reserved.
 

import sys
sys.path.insert(1,"../")

import unittest

from InPort import *

import RTC, RTC__POA
import OpenRTM_aist

class OnRWTest:
	def __init__(self):
		pass

	def echo(self, value=None):
		print "OnRW Called"

class OnRWConvertTest:
	def __init__(self):
		pass

	def echo(self, value=None):
		print "OnRWConvert Called"


class TestInPort(unittest.TestCase):
	def setUp(self):
		OpenRTM_aist.Manager.instance()
		self._ipn = InPort("in", RTC.TimedLong(RTC.Time(0,0), 0), OpenRTM_aist.NullBuffer())
	
	def test_name(self):
		self.assertEqual(self._ipn.name(), "in")

	def test_case(self):
		self.assertEqual(self._ipn.read().data, 0)
		self._ipn.update()




############### test #################
if __name__ == '__main__':
        unittest.main()

