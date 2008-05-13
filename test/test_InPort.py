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
import OpenRTM

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
		self._ipn = InPort("nullbuf", RTC.TimedLong(RTC.Time(0,0), 0), OpenRTM.NullBuffer())
		self._ipr = InPort("ringbuf", RTC.TimedLong(RTC.Time(0,0), 0), OpenRTM.RingBuffer(8))
	
	def test_name(self):
		self.assertEqual(self._ipn.name(), "nullbuf")
		self.assertEqual(self._ipr.name(), "ringbuf")

	def test_case(self):
		self.assertEqual(self._ipn.write(RTC.TimedLong(RTC.Time(0,0), 123)), True)
		self.assertEqual(self._ipr.write(RTC.TimedLong(RTC.Time(0,0), 456)), True)
		self.assertEqual(self._ipn.read().data, 123)
		self.assertEqual(self._ipr.read().data, 456)
		self._ipn.update()
		self._ipr.update()

	"""
	def test_setOnWrite(self):
		self._ipn.setOnWrite(OnRWTest().echo)
		self._ipn.setOnWriteConvert(OnRWConvertTest().echo)
		self.assertEqual(self._ipn.write(RTC.TimedLong(RTC.Time(0,0), 123)), True)
		self._ipr.setOnWrite(OnRWTest().echo)
		self._ipr.setOnWriteConvert(OnRWConvertTest().echo)
		self.assertEqual(self._ipr.write(RTC.TimedLong(RTC.Time(0,0), 456)), True)
	"""

	def test_setOnRead(self):
		self.assertEqual(self._ipn.write(RTC.TimedLong(RTC.Time(0,0), 123)), True)
		self.assertEqual(self._ipr.write(RTC.TimedLong(RTC.Time(0,0), 456)), True)
		self._ipn.setOnRead(OnRWTest().echo)
		self.assertEqual(self._ipn.read().data, 123)
		self._ipr.setOnRead(OnRWTest().echo)
		self.assertEqual(self._ipr.read().data, 456)



############### test #################
if __name__ == '__main__':
        unittest.main()

