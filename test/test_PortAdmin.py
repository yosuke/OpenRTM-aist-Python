#!/usr/bin/env python
# -*- Python -*-

#
# \file test_PortAdmin.py
# \brief test for RTC's Port administration class
# \date $Date: 2007/09/03 $
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

import unittest
import OpenRTM
from PortAdmin import *

import RTC, RTC__POA
import OpenRTM

import CORBA

class PortBase(OpenRTM.PortBase):
	def __init__(self):
		OpenRTM.PortBase.__init__(self)

	def publishInterfaces(self, prof):
		return RTC.RTC_OK

	def subscribeInterfaces(self, prof):
		return RTC.RTC_OK

	def unsubscribeInterfaces(self, prof):
		return RTC.RTC_OK

		
class TestPortAdmin(unittest.TestCase):
	def setUp(self):
		self._orb = CORBA.ORB_init(sys.argv)
		self._poa = self._orb.resolve_initial_references("RootPOA")
		self._poa._get_the_POAManager().activate()

		self._pa = PortAdmin(self._orb, self._poa)

		self._pb1 = PortBase()
		self._pb2 = PortBase()

		self._pb1.setName("port0")
		self._pb2.setName("port1")

		self._pa.registerPort(self._pb1)
		self._pa.registerPort(self._pb2)


	def test_getPortList(self):
		plist = self._pa.getPortList()

		prof0 = plist[0].get_port_profile()
		self.assertEqual(prof0.name, "port0")

		prof1 = plist[1].get_port_profile()
		self.assertEqual(prof1.name, "port1")
		

	def test_getPortRef(self):
		
		getP = self._pa.getPortRef("")
		self.assertEqual(CORBA.is_nil(getP), True)

		getP = self._pa.getPortRef("port1")
		self.assertEqual(CORBA.is_nil(getP), False)
		self.assertEqual(getP.get_port_profile().name, "port1")

		getP = self._pa.getPortRef("port0")
		self.assertEqual(CORBA.is_nil(getP), False)
		self.assertEqual(getP.get_port_profile().name, "port0")
		

	def test_getPort(self):
		pb = self._pa.getPort("port0")
		prof = pb.get_port_profile()
		self.assertEqual(prof.name, "port0")

		pb = self._pa.getPort("port1")
		prof = pb.get_port_profile()
		self.assertEqual(prof.name, "port1")


	def test_deletePort(self):
		self._pa.deletePort(self._pb1)
		plist = self._pa.getPortList()
		self.assertEqual(len(plist), 1)

		prof = plist[0].get_port_profile()
		self.assertEqual(prof.name, "port1")


	def test_deletePortByName(self):
		plist = self._pa.getPortList()
		self.assertEqual(len(plist), 2)

		self._pa.deletePortByName("port1")

		plist = self._pa.getPortList()
		self.assertEqual(len(plist), 1)
		

	def test_finalizePorts(self):
		plist = self._pa.getPortList()
		self.assertEqual(len(plist), 2)

		self._pa.finalizePorts()
		
		plist = self._pa.getPortList()
		self.assertEqual(len(plist), 0)
		


############### test #################
if __name__ == '__main__':
        unittest.main()

