#!/usr/bin/env python
# -#- Python -#-
#
# \file test_TimeValue.py
# \brief test for TimeValue class
# \date $Date: $
# \author Shinji Kurihara
#
# Copyright (C) 2007
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.
#

import sys
sys.path.insert(1,"../")

import unittest
import time

from TimeValue import *

class TestTimeValue(unittest.TestCase):
	
	def setUp(self):
		self.tm = TimeValue(usec=1000000)


	def tearDown(self):
		pass


	def test_set_time(self):
		tm = time.time()
		ret = self.tm.set_time(tm)


	def test_toDouble(self):
		self.test_set_time()
		print  self.tm.toDouble()


	def test__str__(self):
		self.test_set_time()
		print self.tm
	
############### test #################
if __name__ == '__main__':
        unittest.main()
