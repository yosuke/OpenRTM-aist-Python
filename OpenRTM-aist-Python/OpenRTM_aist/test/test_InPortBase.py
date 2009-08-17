#!/usr/bin/env python
# -*- coding: euc-jp -*-


#  \file test_InPortBase.py
#  \brief test for InPortBase class
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

from omniORB import CORBA, PortableServer
from omniORB import any

import unittest

from InPortBase import *

import RTC, RTC__POA
import OpenRTM_aist


class InPortMock(InPortBase):
	def __init__(self, name, data_type):
		InPortBase.__init__(self, name, data_type)
		return

	def getThebuffer(self):
		return self._thebuffer

	def getProviderTypes(self):
		return self._providerTypes

	def getConsumerTypes(self):
		return self._consumerTypes

	def publishInterfaces_public(self, connector_profile):
		return self.publishInterfaces(connector_profile)



class TestInPortBase(unittest.TestCase):
	def setUp(self):
		#mgr=OpenRTM_aist.Manager.instance()
		self._orb = CORBA.ORB_init(sys.argv)
		self._poa = self._orb.resolve_initial_references("RootPOA")
		self._poa._get_the_POAManager().activate()

		self._inport = InPortMock("in", OpenRTM_aist.toTypename(RTC.TimedLong(RTC.Time(0,0), 0)))
		self._outport = OpenRTM_aist.OutPort("out",RTC.TimedLong(RTC.Time(0,0), 0))

		return


	def tearDown(self):
		return

	def test_properties(self):
		self.assertEqual(isinstance(self._inport.properties(),OpenRTM_aist.Properties),True)
		return

	def test_init(self):
		self.assertEqual(self._inport.getThebuffer(),None)
		profile = self._inport.getPortProfile()
		prop    = OpenRTM_aist.NVUtil.toProperties(profile.properties)

		self.assertEqual(prop.getProperty("dataport.dataflow_type"),"")
		self.assertEqual(prop.getProperty("dataport.interface_type"),"")
		
		pstr = self._inport.getProviderTypes()
		self.assertEqual(len(pstr),0)
		cstr = self._inport.getConsumerTypes()
		self.assertEqual(len(cstr),0)

		self._inport.init()
		
		# self._singlebufferがTrueの場合self._thebufferが取得される
		self.assertNotEqual(self._inport.getThebuffer(),None)
		profile = self._inport.getPortProfile()
		prop    = OpenRTM_aist.NVUtil.toProperties(profile.properties)

		# getPortProfileのpropertiesに以下が追加される
		val = any.from_any(prop.getProperty("dataport.dataflow_type"),keep_structs=True)
		self.assertEqual(val,"push, pull")
		val = any.from_any(prop.getProperty("dataport.interface_type"),keep_structs=True)
		self.assertEqual(val,"corba_cdr")
		
		# ProviderTypes,ConsumerTypesが取得される
		pstr = self._inport.getProviderTypes()
		self.assertEqual(pstr[0],"corba_cdr")
		cstr = self._inport.getConsumerTypes()
		self.assertEqual(cstr[0],"corba_cdr")

		return

	def test_activate_deactivateInterfaces(self):
		self._inport.init()
		nvlist = [OpenRTM_aist.NVUtil.newNV("dataport.interface_type","corba_cdr"),
			  OpenRTM_aist.NVUtil.newNV("dataport.dataflow_type","push"),
			  OpenRTM_aist.NVUtil.newNV("dataport.subscription_type","flush")]
		prof = RTC.ConnectorProfile("InPortBaseTest0",
					    "id0",
					    [self._inport.get_port_profile().port_ref],
					    nvlist)

		self._inport.publishInterfaces_public(prof)
		prof.connector_id = "id1"
		prof.name = "InPortBaseTest1"
		self._inport.publishInterfaces_public(prof)

		self._inport.activateInterfaces()
		self._inport.deactivateInterfaces()


		return

	def test_subscribe_unsubscribeInterfaces(self):
		self._inport.init()
		nvlist = [OpenRTM_aist.NVUtil.newNV("dataport.interface_type","corba_cdr"),
			  OpenRTM_aist.NVUtil.newNV("dataport.dataflow_type","push"),
			  OpenRTM_aist.NVUtil.newNV("dataport.subscription_type","flush")]
		prof = RTC.ConnectorProfile("InPortBaseTest0",
					    "id0",
					    [self._inport.get_port_profile().port_ref,self._outport.get_port_profile().port_ref],
					    nvlist)
		self._outport.connect(prof)
		self.assertEqual(self._inport.subscribeInterfaces(prof),RTC.RTC_OK)
		self._inport.unsubscribeInterfaces(prof)
		return
		




############### test #################
if __name__ == '__main__':
        unittest.main()

