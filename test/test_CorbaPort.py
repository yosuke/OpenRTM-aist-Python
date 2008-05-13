#!/usr/bin/env python
# -*- Python -*-

#
#  \file  test_CorbaPort.py
#  \brief test for CorbaPort class
#  \date  $Date: 2007/09/27 $
#  \author Shinji Kurihara
# 
#  Copyright (C) 2006
#      Noriaki Ando
#      Task-intelligence Research Group,
#      Intelligent Systems Research Institute,
#      National Institute of
#          Advanced Industrial Science and Technology (AIST), Japan
#      All rights reserved.

from omniORB import any
import CORBA

import OpenRTM
import RTC, RTC__POA

import sys
sys.path.insert(1,"../")

import unittest

from CorbaPort import *

import _GlobalIDL, _GlobalIDL__POA


class MyService_impl(_GlobalIDL__POA.MyService):
	def __init__(self):
		pass

	def echo(self, msg):
		print msg
		return msg

	
class TestCorbaPort(unittest.TestCase):
	def setUp(self):
		orb = CORBA.ORB_init(sys.argv)
		poa = orb.resolve_initial_references("RootPOA")
		poa._get_the_POAManager().activate()

		self._mysvc = MyService_impl()
		self._mycon = OpenRTM.CorbaConsumer()
		#self._mysvc._this()

		self._cpSvc = CorbaPort("MyService")
		self._cpCon = CorbaPort("MyService")


	def test_registerProvider(self):
		self._cpSvc.registerProvider("myservice0", "MyService", self._mysvc)


	def test_registerConsumer(self):
		self._cpCon.registerConsumer("myservice0", "MyService", self._mycon)


	def test_publishInterfaces(self):
		prof = RTC.ConnectorProfile("","",[],[])
		self._cpSvc.publishInterfaces(prof)


	def test_subscribeInterfaces(self):
		prof = RTC.ConnectorProfile("","",[],[])
		self._cpSvc.subscribeInterfaces(prof)


	def test_unsubscribeInterfaces(self):
		prof = RTC.ConnectorProfile("","",[],[])
		self._cpSvc.unsubscribeInterfaces(prof)



############### test #################
if __name__ == '__main__':
        unittest.main()
