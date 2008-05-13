#!/usr/bin/env python
# -*- Python -*-

#
# \file test_NamingManager.py
# \brief test for naming Service helper class
# \date $Date: 2007/08/27$
# \author Shinji Kurihara
#
# Copyright (C) 2006
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.
#

import sys
sys.path.insert(1,"../")
from omniORB import CORBA

import unittest

import OpenRTM

from NamingManager import *


class test_comp(OpenRTM.RTObject_impl):
	def __init__(self):
		pass
		
	def echo(self, msg):
		print msg
		return msg
		

class TestNamingOnCorba(unittest.TestCase):
	def setUp(self):
		orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)
#		self._noc = NamingOnCorba(orb,"iyou.a02.aist.go.jp")
		self._noc = NamingOnCorba(orb,"localhost")
		self._mgr = OpenRTM.Manager.init(sys.argv)
		self._nm  = NamingManager(self._mgr)
		self._obj = test_comp()
		
	def __del__(self):
		pass

	def test_bindObject(self):
		self._noc.bindObject("test_comp",self._obj)

	def test_unbindObject(self):
		self._noc.unbindObject("test_comp")


	def test_registerNameServer(self):
		self._nm.registerNameServer("test_comp","iyou.a02.aist.go.jp")

	def test_bindObject(self):
		self._nm.bindObject("test_comp",self._obj)


	def test_update(self):
		self._nm.update()
	
	def test_unbindObject(self):
		self._nm.unbindObject("test_comp")

	def test_unbindAll(self):
		self._nm.unbindAll()

	def test_getObjects(self):
		self._nm.bindObject("test_comp",self._obj)
		self.assertEqual(len(self._nm.getObjects()),1)

	def test_createNamingObj(self):
		self._nm.createNamingObj("test", "iyou.a02.aist.go.jp")

	def test_bindCompsTo(self):
		self._nm.bindCompsTo(self._obj)

	def test_registerCompName(self):
		self._nm.registerCompName("rest",self._obj)

	def test_unregisterCompName(self):
		self._nm.registerCompName("rest",self._obj)
		self._nm.unregisterCompName("rest")


############### test #################
if __name__ == '__main__':
        unittest.main()
