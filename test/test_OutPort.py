#!/usr/bin/env python
# -*- Python -*-

#
#  \file test_OutPort.py
#  \brief test for OutPort class
#  \date $Date: 2007/09/19$
#  \author Shinji Kurihara
# 
#  Copyright (C) 2006
#      Noriaki Ando
#      Task-intelligence Research Group,
#      Intelligent Systems Research Institute,
#      National Institute of
#          Advanced Industrial Science and Technology (AIST), Japan
#      All rights reserved.
# 

import sys
sys.path.insert(1,"../")

import unittest
from OutPort import *

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


class TestOutPort(unittest.TestCase):
	def setUp(self):
		self._op8 = OutPort("out", RTC.TimedLong(RTC.Time(0,0), 0),OpenRTM.RingBuffer(8))
		self._op256 = OutPort("out", RTC.TimedLong(RTC.Time(0,0), 0), OpenRTM.RingBuffer(256))

	def test_read_write(self):
		self.assertEqual(self._op8.write(RTC.TimedLong(RTC.Time(0,0), 123)), True)
		self.assertEqual(self._op256.write(RTC.TimedLong(RTC.Time(0,0), 456)), True)
		read_data = [RTC.TimedLong(RTC.Time(0,0), 0)]
		self._op8.read(read_data)
		self.assertEqual(read_data[0].data,123)
		self._op256.read(read_data)
		self.assertEqual(read_data[0].data,456)

	"""
	def test_OnWrite(self):
		self._op8.setOnWrite(OnRWTest().echo)
		self._op8.setOnWriteConvert(OnRWConvertTest().echo)
		self.assertEqual(self._op8.write(RTC.TimedLong(RTC.Time(0,0), 123)), True)
		self._op256.setOnWrite(OnRWTest().echo)
		self._op256.setOnWriteConvert(OnRWConvertTest().echo)
		self.assertEqual(self._op256.write(RTC.TimedLong(RTC.Time(0,0), 456)), True)
	"""

	def test_OnRead(self):
		self._op8.setReadBlock(True)
		self._op8.setReadTimeout(1000000) # 1sec 
		self._op8.setOnRead(OnRWTest().echo)
		self._op8.setOnReadConvert(OnRWConvertTest().echo)
		read_data = [RTC.TimedLong(RTC.Time(0,0), 0)]
		self._op8.read(read_data)

	def test_getPortDataType(self):
		print self._op8.getPortDataType()


############### test #################
if __name__ == '__main__':
        unittest.main()
