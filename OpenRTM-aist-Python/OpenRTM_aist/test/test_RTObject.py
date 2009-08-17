#!/usr/bin/env python
# -*- Python -*-


## \file test_RTObject.py
## \brief test for RT component base class
## \date $Date: $
## \author Shinji Kurihara
#
# Copyright (C) 2006
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.
#

import sys,time
sys.path.insert(1,"../")
sys.path.insert(1,"../RTM_IDL")

import RTC
import SDOPackage
import OpenRTM_aist
from omniORB import any

import unittest

configsample_spec = ["implementation_id", "TestComp",
		     "type_name",         "TestComp",
		     "description",       "Test example component",
		     "version",           "1.0",
		     "vendor",            "Shinji Kurihara, AIST",
		     "category",          "example",
		     "activity_type",     "DataFlowComponent",
		     "max_instance",      "10",
		     "language",          "Python",
		     "lang_type",         "script",
		     # Configuration variables
		     "conf.default.int_param0", "0",
		     "conf.default.int_param1", "1",
		     "conf.default.double_param0", "0.11",
		     "conf.default.double_param1", "9.9",
		     "conf.default.str_param0", "hoge",
		     "conf.default.str_param1", "dara",
		     "conf.default.vector_param0", "0.0,1.0,2.0,3.0,4.0",
		     ""]

com = None

class TestComp(OpenRTM_aist.DataFlowComponentBase):
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

	def onInitialize(self):
		print "onInitialize"
		return RTC.RTC_OK

	def onFinalize(self):
		print "onFinalize"
		return RTC.RTC_OK
		
	def onStartup(self, ec_id):
		print "onStartup"
		return RTC.RTC_OK

	def onShutdown(self, ec_id):
		print "onSutdown"
		return RTC.RTC_OK

	def onActivated(self, ec_id):
		print "onActivated"
		return RTC.RTC_OK

	def onDeactivated(self, ec_id):
		print "onDeactivated"
		return RTC.RTC_OK

	def onExecute(self, ec_id):
		print "onExecute"
		return RTC.RTC_OK

	def onAborting(self, ec_id):
		print "onAborting"
		return RTC.RTC_OK

	def onReset(self, ec_id):
		print "onReset"
		return RTC.RTC_OK
		
	def onStateUpdate(self, ec_id):
		print "onStateUpdate"
		return RTC.RTC_OK

	def onRateChanged(self, ec_id):
		print "onRateChanged"
		return RTC.RTC_OK

		
def TestCompInit(manager):
	print "TestCompInit"
	global com
	profile = OpenRTM_aist.Properties(defaults_str=configsample_spec)
	manager.registerFactory(profile,
				TestComp,
				OpenRTM_aist.Delete)
	com = manager.createComponent("TestComp")


class TestRTObject_impl(unittest.TestCase):
	def setUp(self):
		global com
		time.sleep(0.1)
		if not com:
			self.manager = OpenRTM_aist.Manager.init(sys.argv)
			self.manager.setModuleInitProc(TestCompInit)
			self.manager.activateManager()
			self.manager.runManager(True)
		self.rtobj = com
		return

	def tearDown(self):
		#self.rtobj.exit()
		time.sleep(0.1)
		return

	def test_is_alive(self):
		ec = self.rtobj.get_context(0)
		self.assertEqual(self.rtobj.is_alive(ec),True)
		return

	def test_get_owned_contexts(self):
		self.assertNotEqual(self.rtobj.get_owned_contexts(),[])
		return

	def test_get_participating_contexts(self):
		self.assertEqual(self.rtobj.get_participating_contexts(),[])
		return

	def test_get_context(self):
		print self.rtobj.get_context(0)
		return

	def test_get_component_profile(self):
		prof = self.rtobj.get_component_profile()
		self.assertEqual(prof.instance_name, "TestComp0")
		return

	def test_get_ports(self):
		self.assertEqual(self.rtobj.get_ports(), [])
		return


	def test_attach_context(self):
		ec = OpenRTM_aist.PeriodicExecutionContext(self.rtobj, 10)
		id = self.rtobj.attach_context(ec.getObjRef())
		print "attach_context: ", id
		print self.rtobj.detach_context(id)
		return

	def test_get_owned_organizations(self):
		self.assertEqual(self.rtobj.get_owned_organizations(),[])
		return
		
	def test_get_sdo_id(self):
		self.assertEqual(self.rtobj.get_sdo_id(), "TestComp0")
		return

	def test_get_sdo_type(self):
		self.assertEqual(self.rtobj.get_sdo_type(), "Test example component")
		return

	def test_get_device_profile(self):
		prof = self.rtobj.get_device_profile()
		self.assertEqual(prof.device_type, "")
		return

	def test_get_service_profiles(self):
		#self.assertEqual(self.rtobj.get_service_profiles(),[])
		return


	def test_get_service_profile(self):
		#self.rtobj.get_service_profile("TestComp")
		return


	def test_get_sdo_service(self):
		#self.rtobj.get_sdo_service(None)
		return

	def test_get_configuration(self):
		print self.rtobj.get_configuration()
		return

	def test_get_monitoring(self):
		#self.rtobj.get_monitoring()
		return

	def test_get_organizations(self):
		self.assertEqual(self.rtobj.get_organizations(), [])
		return

	def test_get_status_list(self):
		self.assertEqual(self.rtobj.get_status_list(), [])
		return

	def test_get_status(self):
		#self.rtobj.get_status("status")
		return

	def test_getPropTestCase(self):
		self.assertEqual(self.rtobj.getInstanceName(), "TestComp0")
		self.rtobj.setInstanceName("TestComp0")
		self.assertEqual(self.rtobj.getInstanceName(), "TestComp0")
		self.assertEqual(self.rtobj.getTypeName(), "TestComp")
		self.assertEqual(self.rtobj.getDescription(), "Test example component")
		self.assertEqual(self.rtobj.getVersion(), "1.0")
		self.assertEqual(self.rtobj.getVendor(), "Shinji Kurihara, AIST")
		self.assertEqual(self.rtobj.getCategory(), "example")
		self.assertEqual(self.rtobj.getNamingNames(),["TestComp0.rtc"])
		return

	def test_setObjRef(self):
		self.rtobj.setObjRef("test")
		self.assertEqual(self.rtobj.getObjRef(),"test")
		return


	def test_bindParameter(self):
		conf_ = [123]
		self.assertEqual(self.rtobj.bindParameter("config", conf_, 0), True)
		self.rtobj.updateParameters("")
		return

	def test_PortTestCase(self):
		ringbuf = OpenRTM_aist.RingBuffer(8)
		outp = OpenRTM_aist.OutPort("out", RTC.TimedLong(RTC.Time(0,0),0), ringbuf)
		self.rtobj.registerOutPort("out",outp)

		ringbuf = OpenRTM_aist.RingBuffer(8)
		inp = OpenRTM_aist.InPort("in", RTC.TimedLong(RTC.Time(0,0),0), ringbuf)
		self.rtobj.registerInPort("in",inp)
		
		self.rtobj.deletePort(outp)
		self.rtobj.deletePort(inp)

		self.rtobj.finalizePorts()
		return




############### test #################
if __name__ == '__main__':
        unittest.main()
