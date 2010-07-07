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
from omniORB import CORBA, PortableServer
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

class TestComp(OpenRTM_aist.RTObject_impl):
  def __init__(self, orb_, poa_):
    OpenRTM_aist.RTObject_impl.__init__(self, orb=orb_, poa=poa_)

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
    self._orb = CORBA.ORB_init(sys.argv)
    self._poa = self._orb.resolve_initial_references("RootPOA")
    self._poa._get_the_POAManager().activate()
    return

  def tearDown(self):
    #global com
    #self.rtobj.exit()
    #self.manager.terminate()
    time.sleep(0.1)
    OpenRTM_aist.Manager.instance().shutdownManager()
    #com = None
    return

  def test_is_alive(self):
    rtobj = TestComp(self._orb, self._poa)
    ec = rtobj.getObjRef().get_context(0)
    self.assertEqual(ec,None)
    ec_args = "PeriodicExecutionContext"+"?" + "rate=1000"
    ec=OpenRTM_aist.Manager.instance().createContext(ec_args)
    ec.bindComponent(rtobj)
    self.assertNotEqual(rtobj.getObjRef().get_owned_contexts(),[])
    self.assertEqual(rtobj.is_alive(ec.getObjRef()),True)
    ec.remove_component(rtobj.getObjRef())
    ec.stop()
    del ec

    return

  def test_get_owned_contexts(self):
    rtobj = TestComp(self._orb, self._poa)
    self.assertEqual(rtobj.getObjRef().get_owned_contexts(),[])
    ec_args = "PeriodicExecutionContext"+"?" + "rate=1000"
    ec=OpenRTM_aist.Manager.instance().createContext(ec_args)
    ec.bindComponent(rtobj)
    self.assertNotEqual(rtobj.getObjRef().get_owned_contexts(),[])
    ec.remove_component(rtobj.getObjRef())
    ec.stop()
    del ec

    return

  def test_get_participating_contexts(self):
    rtobj = TestComp(self._orb, self._poa)
    self.assertEqual(rtobj.getObjRef().get_participating_contexts(),[])
    return

  def test_get_context(self):
    rtobj = TestComp(self._orb, self._poa)
    print rtobj.getObjRef().get_context(0)
    return

  def test_get_component_profile(self):
    rtobj = TestComp(self._orb, self._poa)
    rtobj.setInstanceName("TestComp0")
    prof = rtobj.getObjRef().get_component_profile()
    self.assertEqual(prof.instance_name, "TestComp0")
    return

  def test_get_ports(self):
    rtobj = TestComp(self._orb, self._poa)
    self.assertEqual(rtobj.getObjRef().get_ports(), [])
    return


  def test_attach_context(self):
    rtobj = TestComp(self._orb, self._poa)
    ec = OpenRTM_aist.PeriodicExecutionContext(rtobj.getObjRef(), 10)
    id = rtobj.getObjRef().attach_context(ec.getObjRef())
    print "attach_context: ", id
    print rtobj.getObjRef().detach_context(id)
    poa = OpenRTM_aist.Manager.instance().getPOA()
    poa.deactivate_object(poa.servant_to_id(ec))
    return

  def test_get_owned_organizations(self):
    rtobj = TestComp(self._orb, self._poa)
    self.assertEqual(rtobj.getObjRef().get_owned_organizations(),[])
    return
    
  def test_get_sdo_id(self):
    rtobj = TestComp(self._orb, self._poa)
    rtobj.setInstanceName("TestComp0")
    self.assertEqual(rtobj.getObjRef().get_sdo_id(), "TestComp0")
    return

  def test_get_sdo_type(self):
    rtobj = TestComp(self._orb, self._poa)
    prop = OpenRTM_aist.Properties(defaults_str=configsample_spec)
    rtobj.setProperties(prop)
    self.assertEqual(rtobj.getObjRef().get_sdo_type(), "Test example component")
    return

  def test_get_device_profile(self):
    rtobj = TestComp(self._orb, self._poa)
    prof = rtobj.getObjRef().get_device_profile()
    self.assertEqual(prof.device_type, "")
    return

  def test_get_service_profiles(self):
    rtobj = TestComp(self._orb, self._poa)
    self.assertEqual(rtobj.getObjRef().get_service_profiles(),[])
    return


  def test_get_service_profile(self):
    #rtobj.getObjRef().get_service_profile("TestComp")
    return


  def test_get_sdo_service(self):
    #rtobj.getObjRef().get_sdo_service(None)
    return

  def test_get_configuration(self):
    rtobj = TestComp(self._orb, self._poa)
    print rtobj.getObjRef().get_configuration()
    return

  def test_get_monitoring(self):
    #rtobj.getObjRef().get_monitoring()
    return

  def test_get_organizations(self):
    rtobj = TestComp(self._orb, self._poa)
    self.assertEqual(rtobj.getObjRef().get_organizations(), [])
    return

  def test_get_status_list(self):
    rtobj = TestComp(self._orb, self._poa)
    self.assertEqual(rtobj.getObjRef().get_status_list(), [])
    return

  def test_get_status(self):
    #rtobj.getObjRef().get_status("status")
    return

  def test_getPropTestCase(self):
    rtobj = TestComp(self._orb, self._poa)
    self.assertEqual(rtobj.getInstanceName(), "")
    prop = OpenRTM_aist.Properties(defaults_str=configsample_spec)
    rtobj.setInstanceName("TestComp0")
    rtobj.setProperties(prop)
    self.assertEqual(rtobj.getInstanceName(), "TestComp0")
    self.assertEqual(rtobj.getTypeName(), "TestComp")
    self.assertEqual(rtobj.getDescription(), "Test example component")
    self.assertEqual(rtobj.getVersion(), "1.0")
    self.assertEqual(rtobj.getVendor(), "Shinji Kurihara, AIST")
    self.assertEqual(rtobj.getCategory(), "example")
    self.assertNotEqual(rtobj.getNamingNames(),["TestComp0.rtc"])
    return

  def test_setObjRef(self):
    rtobj = TestComp(self._orb, self._poa)
    rtobj.setObjRef("test")
    self.assertEqual(rtobj.getObjRef(),"test")
    return

  def test_bindParameter(self):
    rtobj = TestComp(self._orb, self._poa)
    conf_ = [123]
    self.assertEqual(rtobj.bindParameter("config", conf_, 0), True)
    rtobj.updateParameters("")
    return

  def test_PortTestCase(self):
    rtobj = TestComp(self._orb, self._poa)
    ringbuf = OpenRTM_aist.RingBuffer(8)
    outp = OpenRTM_aist.OutPort("out", RTC.TimedLong(RTC.Time(0,0),0), ringbuf)
    rtobj.registerOutPort("out",outp)

    ringbuf = OpenRTM_aist.RingBuffer(8)
    inp = OpenRTM_aist.InPort("in", RTC.TimedLong(RTC.Time(0,0),0), ringbuf)
    rtobj.registerInPort("in",inp)
    
    rtobj.deletePort(outp)
    rtobj.deletePort(inp)

    rtobj.finalizePorts()
    return




############### test #################
if __name__ == '__main__':
  unittest.main()
