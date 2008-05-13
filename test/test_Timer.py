#!/usr/bin/env/python
# -*- Python -*-

#
# \file Timer.py
# \brief Timer class
# \date $Date: $
# \author Noriaki Ando <n-ando@aist.go.jp>
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
import OpenRTM

from Timer import *


class test:
	def func():
		print "test.hello."

		
class TestTimer(unittest.TestCase):
	def setUp(self):
		self.tm = Timer(OpenRTM.TimeValue())


	def test_start_stop(self):
		self.tm.start()
		self.tm.stop()
    

	def test_invoke(self):
		self.tm.registerListenerFunc(test().func, OpenRTM.TimeValue())
		self.tm.invoke()
    

	def test_registerListener(self):
		pass

		
	def test_registerListenerObj(self):
		self.tm.registerListenerObj(test(), test.func, OpenRTM.TimeValue())
		self.tm.invoke()
    

	def test_registerListenerFunc(self):
		self.tm.registerListenerFunc(test().func, OpenRTM.TimeValue())
		self.tm.invoke()


	def test_unregisterListener(self):
		obj = OpenRTM.ListenerObject(test(),test.func)
		self.tm.registerListener(obj, OpenRTM.TimeValue())
		self.assertEqual(self.tm.unregisterListener(obj),True)
		self.assertEqual(self.tm.unregisterListener(obj),False)


############### test #################
if __name__ == '__main__':
        unittest.main()
