#!/usr/bin/env python
# -*- Python -*-

#
#  \file test_PortBase.py
#  \brief test for RTC's Port base class
#  \date $Date: 2007/09/18 $
#  \author Shinji Kurihara
# 
#  Copyright (C) 2006
#      Task-intelligence Research Group,
#      Intelligent Systems Research Institute,
#      National Institute of
#          Advanced Industrial Science and Technology (AIST), Japan
#      All rights reserved.
# 

import sys
sys.path.insert(1,"../")

import unittest
from PortBase import *

import CORBA
import OpenRTM
import RTC, RTC__POA


class OutPortObj(OpenRTM.RTObject_impl):
	def __init__(self):
		self._orb = CORBA.ORB_init()
		self._poa = self._orb.resolve_initial_references("RootPOA")
		OpenRTM.RTObject_impl.__init__(self, orb=self._orb, poa=self._poa)
		ringbuf = OpenRTM.RingBuffer(8)
		self.registerOutPort("out",OpenRTM.OutPort("out", RTC.TimedLong(RTC.Time(0,0),0), ringbuf))


class InPortObj(OpenRTM.RTObject_impl):
	def __init__(self):
		self._orb = CORBA.ORB_init()
		self._poa = self._orb.resolve_initial_references("RootPOA")
		OpenRTM.RTObject_impl.__init__(self, orb=self._orb, poa=self._poa)
		ringbuf = OpenRTM.RingBuffer(8)
		self.registerInPort("in",OpenRTM.InPort("in", RTC.TimedLong(RTC.Time(0,0),0), ringbuf))


class TestPortBase(unittest.TestCase):
	def setUp(self):
		self._orb = CORBA.ORB_init()
		self._poa = self._orb.resolve_initial_references("RootPOA")
		self._poa._get_the_POAManager().activate()
		self._pb = PortBase()

	"""
	def test_get_port_profile(self):
		self._pb.setName("test_connect")
		self._pb.setPortRef(self)
		self._pb.setOwner(self)
		self._pb.appendInterface("test_instance", "PERIODIC", RTC.PROVIDED)
		self._pb.addProperty("name","value")
		prof = self._pb.get_port_profile()
		print prof.name
		print prof.interfaces
		print prof.connector_profiles
		print prof.owner
		print prof.properties
	"""
		


	def test_get_connector_profiles(self):
		nvlist = [OpenRTM.NVUtil.newNV("dataport.interface_type","CORBA_Any"),
				  OpenRTM.NVUtil.newNV("dataport.dataflow_type","Push"),
				  OpenRTM.NVUtil.newNV("dataport.subscription_type","Flush")]

		outp = OutPortObj()._this()
		outp = outp.get_ports()
		print "port_list: ", outp

		inp  = InPortObj()._this()
		inp = inp.get_ports()
		print "port_list: ", inp
		prof = RTC.ConnectorProfile("connector0",
									"",
									[inp[0]._narrow(RTC.Port),outp[0]._narrow(RTC.Port)],
									nvlist)
		print "local prof: ", prof
		ret, prof = self._pb.connect(prof)
		#ret,prof = self._pb.notify_connect(prof)


	"""
	def test_get_connector_profile(self):
		pass


	def test_connect(self):
		nvlist = [OpenRTM.NVUtil.newNV("dataport.interface_type","CORBA_Any"),
				  OpenRTM.NVUtil.newNV("dataport.dataflow_type","Push"),
				  OpenRTM.NVUtil.newNV("dataport.subscription_type","Flush")]

		prof = RTC.ConnectorProfile("connector0","",[TestObj(),TestObj()],nvlist)
		self._pb.connect(prof)


	def test_notify_connect(self):
		pass


	def test_disconnect(self):
		pass


	def test_notify_disconnect(self):
		pass


	def test_disconnect_all(self):
		pass



	def test_getProfile(self):
		pass
    

	def test_getPortRef(self):
		pass


	def test_publishInterfaces(self):
		pass
    

	def test_connectNext(self):
		pass


	def test_disconnectNext(self):
		pass


	def test_subscribeInterfaces(self):
		pass
    
    
	def test_unsubscribeInterfaces(self):
		pass

	def test_isEmptyId(self):
		pass


	def test_getUUID(self):
		pass


	def test_setUUID(self):
		pass


	def test_isExistingConnId(self):
		pass


	def test_findConnProfile(self):
		pass
    

	def test_findConnProfileIndex(self):
		pass


	def test_updateConnectorProfile(self):
		pass


	def test_eraseConnectorProfile(self):
		pass



	def test_deleteInterface(self):
		pass
	"""
    



############### test #################
if __name__ == '__main__':
        unittest.main()
