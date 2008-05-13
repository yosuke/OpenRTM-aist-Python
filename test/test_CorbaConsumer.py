#!/usr/bin/env python
# -*- Python -*-

#
#  \file test_CorbaConsumer.py
#  \brief CORBA Consumer class
#  \date $Date: 2007/09/20 $
#  \author Shinji Kurihara
# 
#  Copyright (C) 2006
#      Noriaki Ando
#      Task-intelligence Research Group,
#      Intelligent Systems Research Institute,
#      National Institute of
#          Advanced Industrial Science and Technology (AIST), Japan
#      All rights reserved.


import CORBA
from omniORB import any

import sys
sys.path.insert(1,"../")

import unittest

from CorbaConsumer import *

import RTC, RTC__POA

class InPortTest(RTC__POA.InPortAny):
	def __init__(self):
		self.orb = CORBA.ORB_init()
		self.poa = self.orb.resolve_initial_references("RootPOA")
		poaManager = self.poa._get_the_POAManager()
		poaManager.activate()
		
		
	def put(self, data):
		print "put data: ", data


class TestCorbaConsumer(unittest.TestCase):
	def setUp(self):		

		self._cc = CorbaConsumer()

	def test_case(self):
		self._cc.setObject(InPortTest()._this())
		obj = self._cc._ptr()._narrow(RTC.InPortAny)
		args = any.to_any("hoge")
		obj.put(args)
		self._cc.releaseObject()
		self.assertEqual(self._cc._ptr(), None)
		


############### test #################
if __name__ == '__main__':
        unittest.main()
