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

import sys
sys.path.insert(1,"../")

import RTC
import SDOPackage
import OpenRTM
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

class TestComp(OpenRTM.DataFlowComponentBase):
	def __init__(self, manager):
		OpenRTM.DataFlowComponentBase.__init__(self, manager)

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
	global com
	profile = OpenRTM.Properties(defaults_str=configsample_spec)
	manager.registerFactory(profile,
							TestComp,
							OpenRTM.Delete)
	com = manager.createComponent("TestComp")


class TestRTObject_impl(unittest.TestCase):
	def setUp(self):
		global com
		self.manager = OpenRTM.Manager.init(sys.argv)
		self.manager.setModuleInitProc(TestCompInit)
		self.manager.activateManager()
		self.rtobj = com
		self.manager.runManager(True)


	"""
	def test_onInitialize(self):
		slef.assertEqual(self.rtobj.onInitialize(), RTC.RTC_OK)

	def test_onFinalize(self):
		slef.assertEqual(self.rtobj.onFinalize(), RTC.RTC_OK)

	def test_onStartup(self):
		slef.assertEqual(self.rtobj.onStartup(0), RTC.RTC_OK)
	
	def test_onShutdown(self):
		slef.assertEqual(self.rtobj.onStartup(0), RTC.RTC_OK)

	def test_onActivated(self):
		slef.assertEqual(self.rtobj.onActivated(0), RTC.RTC_OK)

	
	def test_onDeactivated(self):
		slef.assertEqual(self.rtobj.onDeactivated(0), RTC.RTC_OK)


	def test_onExecute(self):
		slef.assertEqual(self.rtobj.onExecute(0), RTC.RTC_OK)


	def test_onAborting(self):
		slef.assertEqual(self.rtobj.onAborting(0), RTC.RTC_OK)

	
	def test_onError(self):
		slef.assertEqual(self.rtobj.onError(0), RTC.RTC_OK)


	def test_onReset(self):
		slef.assertEqual(self.rtobj.onReset(0), RTC.RTC_OK)


	def test_onStateUpdate(self):
		slef.assertEqual(self.rtobj.onStateUpdate(0), RTC.RTC_OK)

	
	def test_onRateChanged(self):
		slef.assertEqual(self.rtobj.onRateChanged(0), RTC.RTC_OK)


	def test_initialize(self):
		self.rtobj.initialize()

	def test_finalize(self):
		self.rtobj.finalize()

	def test_exit(self):
		self.rtobj.exit()
	
	def test_is_alive(self):
		print self.rtobj.is_alive()

	def test_get_contexts(self):
		print self.rtobj.get_contexts()

	def test_get_context(self):
		print self.rtobj.get_context(0)

	def test_get_component_profile(self):
		prof = self.rtobj.get_component_profile()
		self.assertEqual(prof.instance_name, "TestComp0")

	def test_get_ports(self):
		self.assertEqual(self.rtobj.get_ports(), [])

	def test_get_execution_context_services(self):
		print self.rtobj.get_execution_context_services()


	def test_attach_executioncontext(self):
		ec = OpenRTM.PeriodicExecutionContext(self.rtobj, 10)
		self.rtobj.attach_executioncontext(ec.getRef())
		self.rtobj.detach_executioncontext(0)

	def test_get_owned_organizations(self):
		self.assertEqual(self.rtobj.get_owned_organizations(),[])
		
	def test_get_sdo_id(self):
		self.assertEqual(self.rtobj.get_sdo_id(), "TestComp0")

	def test_get_sdo_type(self):
		self.assertEqual(self.rtobj.get_sdo_type(), "Test example component")

	def test_get_device_profile(self):
		prof = self.rtobj.get_device_profile()
		self.assertEqual(prof.device_type, "example")

	def test_get_service_profiles(self):
		self.assertEqual(self.rtobj.get_service_profiles(),[])


	def test_get_service_profile(self):
		#self.rtobj.get_service_profile("TestComp")
		pass


	def test_get_sdo_service(self):
		pass

	def test_get_configuration(self):
		print self.rtobj.get_configuration()

	def test_get_monitoring(self):
		#self.rtobj.get_monitoring()
		pass

	def test_get_organizations(self):
		self.assertEqual(self.rtobj.get_organizations(), [])

	def test_get_status_list(self):
		self.assertEqual(self.rtobj.get_status_list(), [])

	def test_get_status(self):
		#self.rtobj.get_status("status")
		pass

	def test_getPropTestCase(self):
		self.assertEqual(self.rtobj.getInstanceName(), "TestComp0")
		self.rtobj.setInstanceName("test")
		self.assertEqual(self.rtobj.getInstanceName(), "test")
		self.assertEqual(self.rtobj.getTypeName(), "TestComp")
		self.assertEqual(self.rtobj.getDescription(), "Test example component")
		self.assertEqual(self.rtobj.getVersion(), "1.0")
		self.assertEqual(self.rtobj.getVendor(), "Shinji Kurihara, AIST")
		self.assertEqual(self.rtobj.getCategory(), "example")
		self.assertEqual(self.rtobj.getNamingNames(),["TestComp0.rtc"])
	"""

	def test_setObjRef(self):
		self.rtobj.setObjRef("test")
		self.assertEqual(self.rtobj.getObjRef(),"test")

		
	"""
	def test_bindParameter(self):
		conf_ = [123]
		self.assertEqual(self.rtobj.bindParameter("config", conf_, 0), True)
		self.rtobj.updateParameters("")

	def test_PortTestCase(self):
		ringbuf = OpenRTM.RingBuffer(8)
		outp = OpenRTM.OutPort("out", RTC.TimedLong(RTC.Time(0,0),0), ringbuf)
		self.rtobj.registerOutPort("out",outp)

		ringbuf = OpenRTM.RingBuffer(8)
		inp = OpenRTM.InPort("in", RTC.TimedLong(RTC.Time(0,0),0), ringbuf)
		self.rtobj.registerInPort("in",inp)
		
		self.rtobj.deletePort(outp)
		self.rtobj.deletePort(inp)

		self.rtobj.deletePortByName("out")
		self.rtobj.deletePortByName("in")

		self.rtobj.finalizePorts()


	def test_shutdown(self):
		self.rtobj.shutdown()
	"""



############### test #################
if __name__ == '__main__':
        unittest.main()
