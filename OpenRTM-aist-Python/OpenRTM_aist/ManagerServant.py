#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file ManagerServant.py
# @brief RTComponent manager servant implementation class
# @date $Date: 2007-12-31 03:08:04 $
# @author Noriaki Ando <n-ando@aist.go.jp>
#
# Copyright (C) 2008
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

from omniORB import CORBA
import OpenRTM_aist
import RTC,RTM,RTM__POA
import SDOPackage


class ManagerServant(RTM__POA.Manager):

    # standard constructor
    def __init__(self):
        self._mgr = OpenRTM_aist.Manager.instance()
        self._objref = self._this()


    def __del__(self):
        pass


    # ReturnCode_t load_module(const char* pathname, const char* initfunc)
    def load_module(self, pathname, initfunc):
        self._mgr.load(pathname, initfunc)
        return RTC.RTC_OK

  
    # ReturnCode_t unload_module(const char* pathname)
    def unload_module(self, pathname):
        self._mgr.unload(pathname)
        return RTC.RTC_OK
  

    # ModuleProfileList* get_loadable_modules()
    def get_loadable_modules(self):
        prof = self._mgr.getLoadableModules()
        cprof = [RTM.ModuleProfile([]) for i in prof]

        for i in range(len(prof)):
            OpenRTM_aist.NVUtil.copyFromProperties(cprof_l, prof[i])

        return cprof

  
    # ModuleProfileList* get_loaded_modules()
    def get_loaded_modules(self):
        prof = self._mgr.getLoadedModules()
        cprof = [RTM.ModuleProfile([]) for i in prof]
    
        for i in range(len(prof)):
            OpenRTM_aist.NVUtil.copyFromProperties(cprof[i].properties, prof[i])

        return cprof

  
    # ModuleProfileList* get_factory_profiles()
    def get_factory_profiles(self):
        prof = self._mgr.getFactoryProfiles()
        cprof = [RTM.ModuleProfile([]) for i in prof]
    
        for i in range(len(prof)):
            OpenRTM_aist.NVUtil.copyFromProperties(cprof[i].properties, prof[i])

        return cprof


    # RTObject_ptr create_component(const char* module_name)
    def create_component(self, module_name):
        rtc = self._mgr.createComponent(module_name)
        if rtc == None:
            print "RTC not found: ", module_name
            return RTC.RTObject._nil
        return rtc.getObjRef()

  
    # ReturnCode_t delete_component(const char* instance_name)
    def delete_component(self, instance_name):
        self._mgr.deleteComponent(instance_name)
        return RTC.RTC_OK
  

    # RTCList* get_components()
    def get_components(self):
        rtcs = self._mgr.getComponents()
        crtcs = [rtc.getObjRef() for rtc in rtcs]
        return crtcs
  

    # ComponentProfileList* get_component_profiles()
    def get_component_profiles(self):
        rtcs = self._mgr.getComponents()
        cprofs = [rtc.get_component_profile() for rtc in rtcs]
        return cprofs


    # ManagerProfile* get_profile()
    def get_profile(self):
        prof = RTM.ModuleProfile([])
        OpenRTM_aist.NVUtil.copyFromProperties(prof.properties, self._mgr.getConfig().getNode("manager"))

        return prof
  

    # NVList* get_configuration()
    def get_configuration(self):
        nvlist = []
        OpenRTM_aist.NVUtil.copyFromProperties(nvlist, self._mgr.getConfig())
        return nvlist
  

    # ReturnCode_t set_configuration(const char* name, const char* value)
    def set_configuration(self, name, value):
        self._mgr.getConfig().setProperty(name, value)
        return RTC.RTC_OK
  

    # Manager_ptr get_owner()
    def get_owner(self):
        return RTM.Manager._nil

  
    # Manager_ptr set_owner(RTM::Manager_ptr mgr)
    def set_owner(self, mgr):
        return RTM.Manager._nil
  

    # Manager_ptr get_child()
    def get_child(self):
        return RTM.Manager._nil

  
    # Manager_ptr set_child(RTM::Manager_ptr mgr)
    def set_child(self, mgr):
        return RTM.Manager._nil

  
    # ReturnCode_t fork()
    def fork(self):
        # self._mgr.fork()
        return RTC.RTC_OK

  
    # ReturnCode_t shutdown()
    def shutdown(self):
        self._mgr.terminate()
        return RTC.RTC_OK

  
    # ReturnCode_t restart()
    def restart(self):
        # self._mgr.restart()
        return RTC.RTC_OK
  

    # Object_ptr get_service(const char* name)
    def get_service(self, name):
        return CORBA.Object._nil

  
    # Manager_ptr getObjRef() const
    def getObjRef(self):
        return self._objref
