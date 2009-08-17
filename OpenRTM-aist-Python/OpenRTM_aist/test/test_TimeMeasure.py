#!/usr/bin/env python
# -*- coding: euc-jp -*-

# @file test_TimeMeasure.py
# @brief test for TimeMeasure class
# @date $Date: 2009/02/18$
# @author Shinji Kurihara
#
# Copyright (C) 2009
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.
#

import time
import sys
sys.path.insert(1,"../")

import unittest
from TimeMeasure import *



class TestTimeMeasure(unittest.TestCase):
	def setUp(self):
		self._tm = TimeMeasure(10)
	
	def test_tick_tack(self):
		for i in range(10):
			self._tm.tick()
			time.sleep(0.01)
			self._tm.tack()
		_max    = [0]
		_min    = [0]
		_mean   = [0]
		_stddev = [0]
		print "count: ", self._tm.count()
		print "result: ", self._tm.getStatistics(_max, _min, _mean, _stddev)
		print "max: ", _max[0]
		print "min: ", _min[0]
		print "mean: ", _mean[0]
		print "stddev: ", _stddev[0]

		

############### test #################
if __name__ == '__main__':
	unittest.main()
