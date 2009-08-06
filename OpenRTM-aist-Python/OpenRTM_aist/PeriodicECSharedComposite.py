#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file PeriodicECSharedComposite.h
# @brief Periodic Execution Context Shared Composite Component class
# @date $Date$
# @author Noriaki Ando <n-ando@aist.go.jp>
#
# Copyright (C) 2008
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.
#
# $Id$
#

import string
import sys
import time

from omniORB import CORBA
import OpenRTM, OpenRTM__POA
import RTC,RTC__POA
import OpenRTM_aist


periodicecsharedcomposite_spec = ["implementation_id", "PeriodicECSharedComposite",
                                  "type_name",         "PeriodicECSharedComposite",
                                  "description",       "PeriodicECSharedComposite",
                                  "version",           "1.0",
                                  "vendor",            "jp.go.aist",
                                  "category",          "composite.PeriodicECShared",
                                  "activity_type",     "DataFlowComponent",
                                  "max_instance",      "0",
                                  "language",          "Python",
                                  "lang_type",         "script",
                                  "exported_ports",    "",
                                  "conf.default.members", "",
                                  "conf.default.exported_ports", "",
                                  ""]
                                  


def stringToStrVec(v, _is):
    str = [_is]
    OpenRTM_aist.eraseBlank(str)
    v[0] = str[0].split(",")
    return True


class setCallback(OpenRTM_aist.OnSetConfigurationSetCallback):
    def __init__(self, org):
        self._org = org
        pass

    def __call__(self, config_set):
        self._org.updateDelegatedPorts()



class addCallback(OpenRTM_aist.OnAddConfigurationAddCallback):
    def __init__(self, org):
        self._org = org
        pass

    def __call__(self, config_set):
        self._org.updateDelegatedPorts()

##
# @if jp
# @namespace SDOPacakge
#
# @brief SDO
#
# @else
#
# @namespace SDOPackage
#
# @brief SDO
#
# @endif
#
class PeriodicECOrganization(OpenRTM_aist.Organization_impl):


    def __init__(self, rtobj):
        OpenRTM_aist.Organization_impl.__init__(self,rtobj.getObjRef())
        self._rtobj      = rtobj
        self._ec         = None
        self._rtcMembers = []
        self._rtcout = OpenRTM_aist.Manager.instance().getLogbuf("rtobject.PeriodicECOrganization")
        self._expPorts = []


    ##
    # @if jp
    # 
    # @brief [CORBA interface] Organizationメンバーを追加する
    #
    # Organization が保持するメンバーリストに与えられたSDOListを追加する。
    # 
    # @param sdo_list 追加される SDO メンバーのリスト
    # @return 追加が成功したかどうかがboolで返される
    #
    # @else
    # 
    # @brief [CORBA interface] Add Organization member
    #
    # This operation adds the given SDOList to the existing organization's 
    # member list
    # 
    # @param sdo_list SDO member list to be added
    # @return boolean will returned if the operation succeed
    #
    # @endif
    #
    # Boolean add_members(const SDOList& sdo_list)
    def add_members(self, sdo_list):
        self._rtcout.RTC_DEBUG("add_members()")
        self.updateExportedPortsList()
        for sdo in sdo_list:
            dfc = [None]
            if not self.sdoToDFC(sdo, dfc):
                continue
            member = self.Member(dfc[0])
            self.stopOwnedEC(member)
            self.addOrganizationToTarget(member)
            self.addParticipantToEC(member)
            self.addPort(member, self._expPorts)
            self._rtcMembers.append(member)

        result = OpenRTM_aist.Organization_impl.add_members(self,sdo_list)

        return result


    ##
    # @if jp
    # 
    # @brief [CORBA interface] Organizationメンバーをセットする
    #
    # Organization が保持するメンバーリストを削除し、与えられた
    # SDOListを新規にセットする。
    # 
    # @param sdo_list 新規にセットされる SDO メンバーのリスト
    # @return 追加が成功したかどうかがboolで返される
    #
    # @else
    # 
    # @brief [CORBA interface] Set Organization member
    #
    # This operation removes existing member list and sets the given
    # SDOList to the existing organization's member list
    # 
    # @param sdo_list SDO member list to be set
    # @return boolean will returned if the operation succeed
    #
    # @endif
    #
    # Boolean set_members(const SDOList& sdo_list)
    def set_members(self, sdo_list):
        self._rtcout.RTC_DEBUG("set_members()")
        self._rtcMembers = []
        self.removeAllMembers()
        self.updateExportedPortsList()

        for sdo in sdo_list:
            dfc = [None]
            if not self.sdoToDFC(sdo, dfc):
                continue

            member = self.Member(dfc[0])
            self.stopOwnedEC(member)
            self.addOrganizationToTarget(member)
            self.addParticipantToEC(member)
            self.addPort(member, self._expPorts)
            self._rtcMembers.append(member)

        result = OpenRTM_aist.Organization_impl.set_members(self, sdo_list)

        return result


    ##
    # @if jp
    # 
    # @brief [CORBA interface] Organizationメンバーを削除する
    #
    # Organization が保持するメンバーリスト内の特定のSDOを削除する。
    # 
    # @param id 削除される SDO の ID
    # @return 追加が成功したかどうかがboolで返される
    #
    # @else
    # 
    # @brief [CORBA interface] Remove a member of Organization
    #
    # This operation removes a SDO from existing member list by specified ID.
    # 
    # @param id The ID of the SDO to be removed
    # @return boolean will returned if the operation succeed
    #
    # @endif
    #
    # Boolean remove_member(const char* id)
    def remove_member(self, id):
        self._rtcout.RTC_DEBUG("remove_member(id = %d)", id)
        rm_rtc = []
        for member in self._rtcMembers:
            if str(id) != str(member._profile.instance_name):
                continue
            self.removePort(member, self._expPorts)
            #prop = self._rtobj.getProperties().getProperty("conf.default.exported_ports")
            #prop.setProperty("conf.default.exported_ports", OpenRTM_aist.flatten(self._expPorts)) 
            self._rtobj.getProperties().setProperty("conf.default.exported_ports", OpenRTM_aist.flatten(self._expPorts))
            self.removeParticipantFromEC(member)
            self.removeOrganizationFromTarget(member)
            self.startOwnedEC(member)
            rm_rtc.append(member)

        for m in rm_rtc:
            self._rtcMembers.remove(m)
            
        result = OpenRTM_aist.Organization_impl.remove_member(self, id)
        return result


    def removeAllMembers(self):
        self._rtcout.RTC_DEBUG("removeAllMembers()")
        self.updateExportedPortsList()
        for member in self._rtcMembers:
            self.removePort(member, self._expPorts)
            self.removeParticipantFromEC(member)
            self.removeOrganizationFromTarget(member)
            self.startOwnedEC(member)
            OpenRTM_aist.Organization_impl.remove_member(self, member._profile.instance_name)

        self._rtcMembers = []
        self._expPorts   = []

        
    ##
    # @if jp
    # @brief SDOからDFCへの変換
    # @else
    # @brief Conversion from SDO to DFC
    # @endif
    #
    # bool sdoToDFC(const SDO_ptr sdo, ::OpenRTM::DataFlowComponent_ptr& dfc);
    def sdoToDFC(self, sdo, dfc):
        if CORBA.is_nil(sdo):
            return False

        dfc[0] = sdo._narrow(OpenRTM.DataFlowComponent)
        if CORBA.is_nil(dfc[0]):
            return False

        return True


    ##
    # @if jp
    # @brief Owned ExecutionContext を停止させる
    # @else
    # @brief Stop Owned ExecutionContexts
    # @endif
    #
    # void stopOwnedEC(Member& member);
    def stopOwnedEC(self, member):
        ecs = member._eclist
        for ec in ecs:
            ret = ec.stop()

        return


    ##
    # @if jp
    # @brief Owned ExecutionContext を起動する
    # @else
    # @brief Start Owned ExecutionContexts
    # @endif
    #
    def startOwnedEC(self, member):
        ecs = member._eclist
        for ec in ecs:
            ret = ec.start()

        return


    ##
    # @if jp
    # @brief DFC に Organization オブジェクトを与える
    # @else
    # @brief Set Organization object to target DFC 
    # @endif
    #
    # void addOrganizationToTarget(Member& member);
    def addOrganizationToTarget(self, member):
        conf = member._config
        if CORBA.is_nil(conf):
            return

        conf.add_organization(self._objref)


    ##
    # @if jp
    # @brief Organization オブジェクトを DFCから削除する
    # @else
    # @brief Remove Organization object from a target DFC 
    # @endif
    #
    # void removeOrganizationFromTarget(Member& member)
    def removeOrganizationFromTarget(self, member):
        # get given RTC's configuration object
        conf = member._config
        if CORBA.is_nil(conf):
            return
    
        # set organization to target RTC's conf
        ret = conf.remove_organization(self._pId)


    ##
    # @if jp
    # @brief Composite の ExecutionContext を DFC にセットする
    # @else
    # @brief Set CompositeRTC's ExecutionContext to the given DFC
    # @endif
    #
    # void addParticipantToEC(Member& member)
    def addParticipantToEC(self, member):
        if CORBA.is_nil(self._ec) or self._ec is None:
            ecs = self._rtobj.get_owned_contexts()
            if len(ecs) > 0:
                self._ec = ecs[0]
            else:
                return
        # set ec to target RTC
        ret = self._ec.add_component(member._rtobj)


    ##
    # @if jp
    # @brief Composite の ExecutionContext から DFC を削除する
    # @else
    # @brief Remove participant DFC from CompositeRTC's ExecutionContext
    # @endif
    #
    # void PeriodicECOrganization::removeParticipantFromEC(Member& member)
    def removeParticipantFromEC(self, member):
        if CORBA.is_nil(self._ec) or self._ec is None:
            ecs = self._rtobj.get_owned_contexts()
            if len(ecs) > 0:
                self._ec = ecs[0]
            else:
                return
        self._ec.remove_component(member._rtobj)


    ##
    # @if jp
    # @brief Composite の ExecutionContext を DFC にセットする
    # @else
    # @brief Set CompositeRTC's ExecutionContext to the given DFC
    # @endif
    #
    # void setCompositeECToTarget(::OpenRTM::DataFlowComponent_ptr dfc);
    #def setCompositeECToTarget(self, dfc):
    #    if CORBA.is_nil(dfc):
    #        return
    #
    #    if CORBA.is_nil(self._ec) or self._ec is None:
    #        ecs = self._rtobj.get_owned_contexts()
    #        if len(ecs) > 0:
    #            self._ec = ecs[0]
    #        else:
    #            return
    #
    #    self._ec.add_component(dfc)

    ##
    # @if jp
    # @brief ポートを委譲する
    # @else
    # @brief Delegate given RTC's ports to the Composite
    # @endif
    #
    # void addPort(Member& member, PortList& portlist);
    def addPort(self, member, portlist):
        self._rtcout.RTC_TRACE("addPort(%s)", OpenRTM_aist.flatten(portlist))
        if len(portlist) == 0:
            return
        
        comp_name = member._profile.instance_name
        plist = member._profile.port_profiles
      
        # port delegation
        for prof in plist:
            # port name -> comp_name.port_name
            port_name = comp_name
            port_name += "."
            port_name += prof.name

            self._rtcout.RTC_DEBUG("port_name: %s is in %s?", (port_name,OpenRTM_aist.flatten(portlist)))
            if port_name in portlist:
                pos = portlist.index(port_name)
            else:
                self._rtcout.RTC_DEBUG("Not found: %s is in %s?", (port_name,OpenRTM_aist.flatten(portlist)))
                continue

            self._rtcout.RTC_DEBUG("Found: %s is in %s", (port_name,OpenRTM_aist.flatten(portlist)))
            self._rtobj.registerPortByReference(prof.port_ref)
            self._rtcout.RTC_DEBUG("Port %s was delegated.", port_name)


    ##
    # @if jp
    # @brief 委譲していたポートを削除する
    # @else
    # @brief Remove delegated participatns's ports from the composite
    # @endif
    #
    # void removePort(Member& member, PortList& portlist)
    def removePort(self, member, portlist):
        self._rtcout.RTC_DEBUG("removePort()")
        if len(portlist) == 0:
            return

        comp_name = member._profile.instance_name
        plist = member._profile.port_profiles
    
        # port delegation
        for prof in plist:
            # port name -> comp_name.port_name
            port_name = comp_name
            port_name += "."
            port_name += prof.name
        
            self._rtcout.RTC_DEBUG("port_name: %s is in %s?", (port_name,OpenRTM_aist.flatten(portlist)))
            if port_name in portlist:
                pos = portlist.index(port_name)
            else:
                self._rtcout.RTC_DEBUG("Not found: %s is in %s?", (port_name,OpenRTM_aist.flatten(portlist)))
                continue

            self._rtcout.RTC_DEBUG("Found: %s is in %s", (port_name,OpenRTM_aist.flatten(portlist)))
            self._rtobj.deletePort(prof.port_ref)
            portlist.remove(port_name)
            self._rtcout.RTC_DEBUG("Port %s was deleted.", port_name)


    def updateExportedPortsList(self):
        plist = self._rtobj.getProperties().getProperty("conf.default.exported_ports")
        if plist:
            p = [plist]
            OpenRTM_aist.eraseBlank(p)
            self._expPorts = p[0].split(",")


    def updateDelegatedPorts(self):
        oldPorts = self._expPorts
        ports = self._rtobj.getProperties().getProperty("conf.default.exported_ports")
        newPorts = ports.split(",")

        set_difference = lambda a, b: [x for x in a if not x in b]
        removedPorts = set_difference(oldPorts,newPorts)
        createdPorts = set_difference(newPorts,oldPorts)

        self._rtcout.RTC_VERBOSE("old    ports: %s", OpenRTM_aist.flatten(oldPorts))
        self._rtcout.RTC_VERBOSE("new    ports: %s", OpenRTM_aist.flatten(newPorts))
        self._rtcout.RTC_VERBOSE("remove ports: %s", OpenRTM_aist.flatten(removedPorts))
        self._rtcout.RTC_VERBOSE("add    ports: %s", OpenRTM_aist.flatten(createdPorts))

        for member in self._rtcMembers:
            self.removePort(member, removedPorts)
            self.addPort(member, createdPorts)

        self._expPorts = newPorts



    class Member:
        def __init__(self, rtobj):
            self._rtobj   = rtobj
            self._profile = rtobj.get_component_profile()
            self._eclist  = rtobj.get_owned_contexts()
            self._config  = rtobj.get_configuration()

            
        def __call__(self, x):
            tmp = x
            tmp.swap(self)
            return self

        
        def swap(self, x):
            rtobj   = x._rtobj
            profile = x._profile
            eclist  = x._eclist
            config  = x._config

            x._rtobj   = self._rtobj
            x._profile = self._profile
            x._eclist  = self._eclist
            x._config  = self._config

            self._rtobj   = rtobj
            self._profile = profile
            self._eclist  = eclist
            self._config  = config

            
##
# @if jp
# @namespace RTC
#
# @brief RTコンポーネント
#
# @else
#
# @namespace RTC
#
# @brief RT-Component
#
# @endif
#

##
# @if jp
# @class PeriodicECSharedComposite
# @brief PeriodicECSharedComposite クラス
#
# データフロー型RTComponentの基底クラス。
# 各種データフロー型RTComponentを実装する場合は、本クラスを継承する形で実装
# する。
#
# @since 0.4.0
#
# @else
# @class PeriodicECSharedComposite
# @brief PeriodicECSharedComposite class
#
# This is a base class of the data flow type RT-Component.
# Inherit this class when implementing various data flow type RT-Components.
#
# @since 0.4.0
#
# @endif
#
class PeriodicECSharedComposite(OpenRTM_aist.RTObject_impl):


    ##
    # @if jp
    # @brief コンストラクタ
    #
    # コンストラクタ
    #
    # @param manager マネージャオブジェクト
    #
    # @else
    # @brief Constructor
    #
    # Constructor
    #
    # @param manager Manager object
    #
    # @endif
    #
    def __init__(self, manager):
        OpenRTM_aist.RTObject_impl.__init__(self,manager)
        self._ref = self._this()
        self._objref = self._ref
        self._org = OpenRTM_aist.PeriodicECOrganization(self)
        OpenRTM_aist.CORBA_SeqUtil.push_back(self._sdoOwnedOrganizations,
                                             self._org.getObjRef())

        self._members = [[]]
        self.bindParameter("members", self._members, "", stringToStrVec)
        self._rtcout = OpenRTM_aist.Manager.instance().getLogbuf("rtobject.periodic_ec_shared")
        self._configsets.setOnSetConfigurationSet(setCallback(self._org))
        self._configsets.setOnAddConfigurationSet(addCallback(self._org))
        self._configsets.update("default")

    ##
    # @if jp
    # @brief デストラクタ
    #
    # デストラクタ
    #
    # @else
    # @brief Destructor
    #
    # Destructor
    #
    # @endif
    #
    def __del__(self):
        self._rtcout.RTC_TRACE("destructor of PeriodicECSharedComposite")
        pass

    
    ##
    # @if jp
    # @brief 初期化
    #
    # データフロー型 RTComponent の初期化を実行する。
    # 実際の初期化処理は、各具象クラス内に記述する。
    #
    # @else
    # @brief Initialization
    #
    # Initialization the data flow type RT-Component.
    # Write the actual initialization code in each concrete class.
    #
    # @endif
    #
    def onInitialize(self):
        self._rtcout.RTC_TRACE("onInitialize()")
        mgr = OpenRTM_aist.Manager.instance()

        #comps = mgr.getComponents()
        #for comp in comps:
        #    print comp.getInstanceName()

        sdos = []
        for member in self._members[0]:
            rtc = mgr.getComponent(member)

            if rtc is None:
                print "no RTC found: ", member
                continue

            print "RTC found: ", rtc.getInstanceName()
            sdo = rtc.getObjRef()
            if CORBA.is_nil(sdo):
                continue

            OpenRTM_aist.CORBA_SeqUtil.push_back(sdos, sdo)
    
        try:
            self._org.set_members(sdos)
        except:
            print "exception caught"

        return RTC.RTC_OK


    def onActivated(self, exec_handle):
        self._rtcout.RTC_TRACE("onActivated(%d)", exec_handle)
        ecs = self.get_owned_contexts()
        sdos = self._org.get_members()

        for sdo in sdos:
            rtc = sdo._narrow(RTC.RTObject)
            ecs[0].activate_component(rtc)

        _s=""
        _len = len(self._members[0])
        if _len > 1:
            s="s were"
        else:
            s=" was"
        self._rtcout.RTC_DEBUG("%d member RTC%s activated.", (_len,_s))

        return RTC.RTC_OK


    def onDeactivated(self, exec_handle):
        self._rtcout.RTC_TRACE("onDeactivated(%d)", exec_handle)
        ecs = self.get_owned_contexts()
        sdos = self._org.get_members()

        for sdo in sdos:
            rtc = sdo._narrow(RTC.RTObject)
            ecs[0].deactivate_component(rtc)

        return RTC.RTC_OK


    def onReset(self, exec_handle):
        self._rtcout.RTC_TRACE("onReset(%d)", exec_handle)
        ecs = self.get_owned_contexts()
        sdos = self._org.get_members()

        for sdo in sdos:
            rtc = sdo._narrow(RTC.RTObject)
            ecs[0].reset_component(rtc)

        return RTC.RTC_OK


    def onFinalize(self):
        self._rtcout.RTC_TRACE("onFinalize()")
        self._org.removeAllMembers()
        self._rtcout.RTC_PARANOID("onFinalize() done")
        return RTC.RTC_OK


    
def PeriodicECSharedCompositeInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=periodicecsharedcomposite_spec)
    manager.registerFactory(profile,
                            OpenRTM_aist.PeriodicECSharedComposite,
                            OpenRTM_aist.Delete)

