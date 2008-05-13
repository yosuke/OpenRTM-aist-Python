#!/usr/bin/env python
# -*- Python -*-

import OpenRTM

import RTC, RTC__POA

simplecomp_spec = ["implementation_id", "SimpleComp",
                   "type_name",         "SimpleComp",
                   "description",       "Test example component",
                   "version",           "1.0",
                   "vendor",            "Shinji Kurihara, AIST",
                   "category",          "example",
                   "activity_type",     "DataFlowComponent",
                   "max_instance",      "10",
                   "language",          "Python",
                   "lang_type",         "script"
                   ""]

class SimpleComp(OpenRTM.DataFlowComponentBase):
    def __init__(self, manager):
        OpenRTM.DataFlowComponentBase.__init__(self, manager)
        print "SimpleComp.__init__"

    def onExecute(self, ec_id):
        print "exec onExecute"
        return RTC.RTC_OK

def MyModuleInit(manager):
    print "MyModuleInit 0"
    profile = OpenRTM.Properties(defaults_str=simplecomp_spec)
    print "MyModuleInit 1"
    manager.registerFactory(profile,
                            SimpleComp,
                            OpenRTM.Delete)
    print "MyModuleInit 2"
    comp = manager.createComponent("SimpleComp")
    print "MyModuleInit 3"

    rtobj = manager.getPOA().servant_to_reference(comp)._narrow(RTC.RTObject)

    ecs = rtobj.get_execution_context_services()
    print "ecs.size: ", len(ecs), ":", ecs

    
    print "Component Kind: ", ecs[0].get_kind()
    print "rtobj: ", rtobj
    print "Component State: ", ecs[0].get_component_state(rtobj)



    
import sys

print "debug 0"
mgr = OpenRTM.Manager.init(len(sys.argv), sys.argv)
print "debug 1"
mgr.setModuleInitProc(MyModuleInit)
print "debug 2"
print mgr.activateManager()
print "debug 3"
mgr.runManager()
print "debug 4"
