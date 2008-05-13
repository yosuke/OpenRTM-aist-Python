#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
 \file RTObject.py
 \brief RT component base class
 \date $Date: $
 \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara

 Copyright (C) 2006
     Task-intelligence Research Group,
     Intelligent Systems Research Institute,
     National Institute of
         Advanced Industrial Science and Technology (AIST), Japan
     All rights reserved.
"""


from omniORB import any
from omniORB import CORBA
import string
import sys
import traceback

import RTC,RTC__POA
import SDOPackage,SDOPackage__POA
import OpenRTM

default_conf = [
	"implementation_id","",
	"type_name",         "",
	"description",       "",
	"version",           "",
	"vendor",            "",
	"category",          "",
	"activity_type",     "",
	"max_instance",      "",
	"language",          "",
	"lang_type",         "",
	"conf",              "",
	"" ]

class RTObject_impl(RTC__POA.DataFlowComponent):
	def __init__(self, manager=None, orb=None, poa=None):
		"""
		 \param manager(OpenRTM.Manager)
		 \param orb(CORBA.ORB)
		 \param poa(CORBA.POA)
		"""
		if manager != None:
			self._manager = manager
			self._orb = self._manager.getORB()
			self._poa = self._manager.getPOA()
			self._portAdmin = OpenRTM.PortAdmin(self._manager.getORB(),self._manager.getPOA())
		else:
			self._manager = None
			self._orb = orb
			self._poa = poa
			self._portAdmin = OpenRTM.PortAdmin(self._orb,self._poa)
			
		self._created = True
		self._alive = False
		self._properties = OpenRTM.Properties(defaults_str=default_conf)
		self._configsets = OpenRTM.ConfigAdmin(self._properties.getNode("conf"))
		self._profile = RTC.ComponentProfile("","","","","","",[],None,[])
		
		self._SdoConfigImpl = OpenRTM.Configuration_impl(self._configsets)
		self._SdoConfig = self._SdoConfigImpl.getObjRef()
		self._execContexts = []
		self._objref = None
		self._sdoOwnedOrganizations = [] #SDOPackage.OrganizationList()
		self._sdoSvcProfiles        = [] #SDOPackage.ServiceProfileList()
		self._sdoOrganizations      = [] #SDOPackage.OrganizationList()
		self._sdoStatus             = [] #SDOPackage.NVList()

		return


	def __del__(self):
		return

    #============================================================
    # Overridden functions
    #============================================================
	def onInitialize(self):
		"""
		The initialize action (on CREATED->ALIVE transition)
		formaer rtc_init_entry() 
		"""
		return RTC.RTC_OK


	def onFinalize(self):
		"""
		The finalize action (on ALIVE->END transition)
		formaer rtc_exiting_entry()
		"""
		return RTC.RTC_OK


	def onStartup(self, ec_id):
		"""
		The startup action when ExecutionContext startup
		former rtc_starting_entry()

		\param ec_id(long)
		\return RTC.ReturnCode_t
		"""
		return RTC.RTC_OK


	def onShutdown(self, ec_id):
		"""
		The shutdown action when ExecutionContext stop
		former rtc_stopping_entry()

		\param ec_id(long)
		\return RTC.ReturnCode_t
		"""
		return RTC.RTC_OK


	def onActivated(self, ec_id):
		"""
		The activated action (Active state entry action)
		former rtc_active_entry()

		\param ec_id(long)
		\return RTC.ReturnCode_t
		"""
		return RTC.RTC_OK


	def onDeactivated(self, ec_id):
		"""
		The deactivated action (Active state exit action)
		former rtc_active_exit()

		\param ec_id(long)
		\return RTC.ReturnCode_t
		"""
		return RTC.RTC_OK


	def onExecute(self, ec_id):
		"""
		The execution action that is invoked periodically
		former rtc_active_do()

		\param ec_id(long)
		\return RTC.ReturnCode_t
		"""
		return RTC.RTC_OK


	def onAborting(self, ec_id):
		"""
		The aborting action when main logic error occurred.
		former rtc_aborting_entry()

		\param ec_id(long)
		\return RTC.ReturnCode_t
		"""
		return RTC.RTC_OK


	def onError(self, ec_id):
		"""
		The error action in ERROR state
		former rtc_error_do()

		\param ec_id(long)
		\return RTC.ReturnCode_t
		"""
		return RTC.RTC_OK


	def onReset(self, ec_id):
		"""
		The reset action that is invoked resetting
		This is same but different the former rtc_init_entry()

		\param ec_id(long)
		\return RTC.ReturnCode_t
		"""
		return RTC.RTC_OK


	def onStateUpdate(self, ec_id):
		"""
		The state update action that is invoked after onExecute() action
		no corresponding operation exists in OpenRTm-aist-0.2.0

		\param ec_id(long)
		\return RTC.ReturnCode_t
		"""
		return RTC.RTC_OK


	def onRateChanged(self, ec_id):
		"""
		The action that is invoked when execution context's rate is changed
		no corresponding operation exists in OpenRTm-aist-0.2.0

		\param ec_id(long)
		\return RTC.ReturnCode_t
		"""
		return RTC.RTC_OK 

    #============================================================
    # RTC::LightweightRTObject
    #============================================================

	def initialize(self):
		"""
		\if jp

		\breif RTCを初期化する

		このオペレーション呼び出しの結果として、ComponentAction::on_initialize
		コールバック関数が呼ばれる。
		制約
		Created状態にいるときにのみ、初期化が行われる。他の状態にいる場合には
		ReturnCode_t::PRECONDITION_NOT_MET が返され呼び出しは失敗する。
		このオペレーションはRTCのミドルウエアから呼ばれることを想定しており、
		アプリケーション開発者は直接このオペレーションを呼ぶことは想定
		されていない。

		\else

		\breif Initialize the RTC that realizes this interface.

		The invocation of this operation shall result in the invocation of the
		callback ComponentAction::on_initialize.

		Constraints
		- An RTC may be initialized only while it is in the Created state. Any
			attempt to invoke this operation while in another state shall fail
			with ReturnCode_t::PRECONDITION_NOT_MET.
		- Application developers are not expected to call this operation
			directly; it exists for use by the RTC infrastructure.

		\endif
		"""
		ret = self.on_initialize()
		self._created = False

		if ret == RTC.RTC_OK:
			if len(self._execContexts) > 0:
				self._execContexts[0].start()
			self._alive = True
		
		return ret


	def finalize(self):
		"""
		\if jp

		\brief RTCを解体準備のため終了させる

		このオペレーション呼び出しは結果としてComponentAction::on_finalize()
		を呼び出す。

		制約
		- この RTC が属する Running 状態の実行コンテキスト中、Active 状態にある
			ものがあればこの RTC は終了されない。その場合、このオペレーション呼び
			出しはいかなる場合も ReturnCode_t::PRECONDITION_NOT_ME で失敗する。
		- この RTC が Created 状態である場合、終了処理は行われない。
			その場合、このオペレーション呼び出しはいかなる場合も 
			ReturnCode_t::PRECONDITION_NOT_MET で失敗する。
		- アプリケーション開発者はこのオペレーションを直接的に呼び出すことは
			まれであり、たいていはRTCインフラストラクチャから呼び出される。

		\else

		\brief Finalize the RTC for preparing it for destruction

		This invocation of this operation shall result in the invocation of the
		callback ComponentAction::on_finalize.

		Constraints
		- An RTC may not be finalized while it is Active in any Running
			execution context. Any attempt to invoke this operation at such a time
			shall fail with ReturnCode_t::PRECONDITION_NOT_MET.
		- An RTC may not be finalized while it is in the Created state.
			Any attempt to invoke this operation while in that state shall fail
			with ReturnCode_t::PRECONDITION_NOT_MET.
		- Application developers are not expected to call this operation
			directly; it exists for use by the RTC infrastructure.

		\endif
		"""
		if self._created:
			return RTC.PRECONDITION_NOT_MET

		for execContext in self._execContexts:
			if execContext.is_running():
				return RTC.PRECONDITION_NOT_MET

		ret = self.on_finalize()
		self.shutdown()
		return ret


	def exit(self):
		"""
		\if jp

		\brief RTCを停止させ、そのコンテンツと共に終了させる

		この RTC がオーナーであるすべての実行コンテキストが停止される。
		この RTC が他の実行コンテキストを所有する RTC に属する実行コンテキスト
		(i.e. 実行コンテキストを所有する RTC はすなわちその実行コンテキストの
		オーナーである。)に参加している場合、当該 RTC はそれらのコンテキスト上
		で非活性化されなければならない。

		制約
		- RTC が初期化されていなければ、終了させることはできない。
			Created 状態にある RTC に exit() を呼び出した場合、
			ReturnCode_t::PRECONDITION_NOT_MET で失敗する。

		\else

		\brief Stop the RTC's and finalize it along with its contents.

		Any execution contexts for which the RTC is the owner shall be stopped. 
		If the RTC participates in any execution contexts belonging to another
		RTC that contains it, directly or indirectly (i.e. the containing RTC
		is the owner of the ExecutionContext), it shall be deactivated in those
		contexts.
		After the RTC is no longer Active in any Running execution context, it
		and any RTCs contained transitively within it shall be finalized.

		Constraints
		- An RTC cannot be exited if it has not yet been initialized. Any
			attempt to exit an RTC that is in the Created state shall fail with
			ReturnCode_t::PRECONDITION_NOT_MET.

		\endif
		"""
		if len(self._execContexts) > 0:
			self._execContexts[0].stop()
			self._alive = False

		OpenRTM.CORBA_SeqUtil.for_each(self._execContexts,
									   self.deactivate_comps(self._objref))
		return self.finalize()


	def is_alive(self):
		"""
		\if jp
		\brief
		\else
		\brief
		A component is alive or not regardless of the execution context from
		which it is observed. However, whether or not it is Active, Inactive,
		or in Error is dependent on the execution context(s) in which it is
		running. That is, it may be Active in one context but Inactive in
		another. Therefore, this operation shall report whether this RTC is
		either Active, Inactive or in Error; which of those states a component
		is in with respect to a particular context may be queried from the
		context itself.
		\endif
		"""
		return self._alive


	def get_contexts(self):
		"""
		\if jp
		\brief [CORBA interface] ExecutionContextListを取得する
		\else
		\brief [CORBA interface] Get ExecutionContextList.
		\endif
		"""
		execlist = []
		OpenRTM.CORBA_SeqUtil.for_each(self._execContexts, self.ec_copy(execlist))
		return execlist


	def get_context(self, ec_id):
		"""
		\if jp
		\brief [CORBA interface] ExecutionContextを取得する
		\param ec_id(long)
		\else
		\brief [CORBA interface] Get ExecutionContext.
		\param ec_id(long)
		\endif
		"""
		if ec_id > (len(self._execContexts) - 1):
			return RTC.ExecutionContext._nil

		return self._execContexts[ec_id]
    

    #============================================================
    # RTC::RTObject
    #============================================================

	def get_component_profile(self):
		"""
		\if jp
		\brief [RTObject CORBA interface] コンポーネントプロファイルの取得

		当該コンポーネントのプロファイル情報を返す。 
		\else
		\brief [RTObject CORBA interface] Get RTC's profile

		This operation returns the ComponentProfile of the RTC
		\endif
		"""
		try:
			return RTC.ComponentProfile(self._profile.instance_name,
										self._profile.type_name,
										self._profile.description,
										self._profile.version,
										self._profile.vendor,
										self._profile.category,
										self._profile.port_profiles,
										self._profile.parent,
										self._profile.properties)
		
		except:
			traceback.print_exception(*sys.exc_info())
		assert(False)
		return 0


	def get_ports(self):
		"""
		\if jp
		\brief [RTObject CORBA interface] ポートの取得

		当該コンポーネントが保有するポートの参照を返す。
		\else
		\brief [RTObject CORBA interface] Get Ports

		This operation returns a list of the RTCs ports.
		\endif
		"""
		try:
			return self._portAdmin.getPortList()
		except:
			traceback.print_exception(*sys.exc_info())

		assert(False)
		return 0


	def get_execution_context_services(self):
		"""
		\if jp
		\brief [RTObject CORBA interface] ExecutionContextAdmin の取得

		このオペレーションは当該　RTC が所属する ExecutionContextに関連した
		ExecutionContextAdmin のリストを返す。
		\else
		\brief [RTObject CORBA interface] Get ExecutionContextAdmin

		This operation returns a list containing an ExecutionContextAdmin for
		every ExecutionContext owned by the RTC.	
		\endif
		"""
		try:
			return self._execContexts
		except:
			traceback.print_exception(*sys.exc_info())

		assert(False)
		return 0


    # RTC::ComponentAction
	def attach_executioncontext(self, exec_context):
		"""
		 \param exec_context(RTC.ExecutionContext)
		"""
		ecs = exec_context._narrow(RTC.ExecutionContextService)
		if CORBA.is_nil(ecs):
			return -1

		self._execContexts.append(ecs)

		return long(len(self._execContexts) -1)

	
	def detach_executioncontext(self, ec_id):
		"""
		 \param exec_context(RTC.ExecutionContext)
		"""
		if ec_id > (len(self._execContexts) - 1):
			return RTC.BAD_PARAMETER

		if CORBA.is_nil(self._execContexts[ec_id]):
			return RTC.BAD_PARAMETER
		
		self._execContexts[ec_id] = RTC.ExecutionContextService._nil
		return RTC.RTC_OK

	
	def on_initialize(self):
		ret = RTC.RTC_ERROR
		try:
			ret = self.onInitialize()
		except:
			return RTC.RTC_ERROR
		
		return ret

	
	def on_finalize(self):
		ret = RTC.RTC_ERROR
		try:
			ret = self.onFinalize()
		except:
			return RTC.RTC_ERROR
		
		return ret

	
	def on_startup(self, ec_id):
		"""
		 \param ec_id(long)
		"""
		ret = RTC.RTC_ERROR
		try:
			ret = self.onStartup(ec_id)
		except:
			return RTC.RTC_ERROR
		
		return ret

	
	def on_shutdown(self, ec_id):
		"""
		 \param ec_id(long)
		"""
		ret = RTC.RTC_ERROR
		try:
			ret = self.onShutdown(ec_id)
		except:
			return RTC.RTC_ERROR
		
		return ret

	
	def on_activated(self, ec_id):
		"""
		 \param ec_id(long)
		"""
		ret = RTC.RTC_ERROR
		try:
			self._configsets.update()
			ret = self.onActivated(ec_id)
		except:
			return RTC.RTC_ERROR
		
		return ret

	
	def on_deactivated(self, ec_id):
		"""
		 \param ec_id(long)
		"""
		ret = RTC.RTC_ERROR
		try:
			ret = self.onDeactivated(ec_id)
		except:
			return RTC.RTC_ERROR
		
		return ret

	
	def on_aborting(self, ec_id):
		"""
		 \param ec_id(long)
		"""
		ret = RTC.RTC_ERROR
		try:
			ret = self.onAborting(ec_id)
		except:
			return RTC.RTC_ERROR
		
		return ret


	def on_error(self, ec_id):
		"""
		 \param ec_id(long)
		"""
		ret = RTC.RTC_ERROR
		try:
			ret = self.onError(ec_id)
		except:
			return RTC.RTC_ERROR
		
		return ret


	def on_reset(self, ec_id):
		"""
		 \param ec_id(long)
		"""
		ret = RTC.RTC_ERROR
		try:
			ret = self.onReset(ec_id)
		except:
			return RTC.RTC_ERROR
		
		return ret

	
	def on_execute(self, ec_id):
		"""
		 \param ec_id(long)
		"""
		ret = RTC.RTC_ERROR
		try:
			ret = self.onExecute(ec_id)
		except:
			return RTC.RTC_ERROR
		
		return ret


	def on_state_update(self, ec_id):
		"""
		 \param ec_id(long)
		"""
		ret = RTC.RTC_ERROR
		try:
			ret = self.onStateUpdate(ec_id)
			self._configsets.update()
		except:
			return RTC.RTC_ERROR
		
		return ret


	def on_rate_changed(self, ec_id):
		"""
		 \param ec_id(long)
		"""
		ret = RTC.RTC_ERROR
		try:
			ret = self.onRateChanged(ec_id)
		except:
			return RTC.RTC_ERROR
		
		return ret


    #============================================================
    # SDOPackage::SdoSystemElement
    #============================================================
	def get_owned_organizations(self):
		"""
		\if jp
		\brief [CORBA interface] Organization リストの取得 

		SDOSystemElement は0個もしくはそれ以上の Organization を所有することが
		出来る。 SDOSystemElement が1つ以上の Organization を所有している場合
		には、このオペレーションは所有する Organization のリストを返す。
		もしOrganizationを一つも所有していないければ空のリストを返す。
		\else
		\brief [CORBA interface] Getting Organizations

		SDOSystemElement can be the owner of zero or more organizations.
		If the SDOSystemElement owns one or more Organizations, this operation
		returns the list of Organizations that the SDOSystemElement owns.
		If it does not own any Organization, it returns empty list.
		\endif
		"""
		try:
			return self._sdoOwnedOrganizations
		except:
			raise SDOPackage.NotAvailable

		return []


    #============================================================
    # SDOPackage::SDO
    #============================================================
	def get_sdo_id(self):
		"""
		\if jp

		\brief [CORBA interface] SDO ID の取得

		SDO ID を返すオペレーション。
		このオペレーションは以下の型の例外を発生させる。

		\exception SDONotExists ターゲットのSDOが存在しない。
		\exception NotAvailable SDOは存在するが応答がない。
		\exception InternalError 内部的エラーが発生した。
		\return    リソースデータモデルで定義されている SDO の ID

		\else

		\brief [CORBA interface] Getting SDO ID

		This operation returns id of the SDO.
		This operation throws SDOException with one of the following types.

		\exception SDONotExists if the target SDO does not exist.
		\exception NotAvailable if the target SDO is reachable but cannot
			respond.
		\exception InternalError if the target SDO cannot execute the operation
			completely due to some internal error.
		\return    id of the SDO defined in the resource data model.

		\endif
		"""
		try:
			return self._profile.instance_name
		except:
			raise SDOPackage.InternalError("get_sdo_id()")


	def get_sdo_type(self):
		"""
		\if jp

		\brief [CORBA interface] SDO タイプの取得

		SDO Type を返すオペレーション。
		このオペレーションは以下の型の例外を発生させる。

		\exception SDONotExists ターゲットのSDOが存在しない。
		\exception NotAvailable SDOは存在するが応答がない。
		\exception InternalError 内部的エラーが発生した。
		\return    リソースデータモデルで定義されている SDO の Type

		\else

		\brief [CORBA interface] Getting SDO type

		This operation returns sdoType of the SDO.
		This operation throws SDOException with one of the following types.

		\exception SDONotExists if the target SDO does not exist.
		\exception NotAvailable if the target SDO is reachable but cannot
			respond.
		\exception InternalError if the target SDO cannot execute the operation
			completely due to some internal error.
		\return    Type of the SDO defined in the resource data model.

		\endif
		"""
		try:
			return self._profile.description
		except:
			raise SDOPackage.InternalError("get_sdo_type()")
		return ""


	def get_device_profile(self):
		"""
		\if jp

		\brief [CORBA interface] SDO DeviceProfile リストの取得 

		SDO の DeviceProfile を返すオペレーション。 SDO がハードウエアデバイス
		に関連付けられていない場合には、空の DeviceProfile が返される。
		このオペレーションは以下の型の例外を発生させる。

		\exception NotAvailable SDOは存在するが応答がない。
		\exception InternalError 内部的エラーが発生した。
		\return    SDO DeviceProfile

		\else

		\brief [CORBA interface] Getting SDO DeviceProfile

		This operation returns the DeviceProfile of the SDO. If the SDO does not
		represent any hardware device, then a DeviceProfile with empty values
		are returned.
		This operation throws SDOException with one of the following types.

		\exception NotAvailable if the target SDO is reachable but cannot
			respond.
		\exception InternalError if the target SDO cannot execute the operation
			completely due to some internal error.
		\return    The DeviceProfile of the SDO.

		\endif
		"""
		try:
			dprofile = SDOPackage.DeviceProfile(self._profile.category,
												self._profile.vendor,
												self._profile.type_name,
												self._profile.version,
												self._profile.properties)
			return dprofile
		except:
			raise SDOPackage.InternalError("get_device_profile()")

		return SDOPackage.DeviceProfile("","","","",[])


	def get_service_profiles(self):
		"""
		\if jp

		\brief [CORBA interface] SDO ServiceProfile の取得 

		SDO が所有している Service の ServiceProfile を返すオペレーション。
		SDO がサービスを一つも所有していない場合には、空のリストを返す。
		このオペレーションは以下の型の例外を発生させる。

		\exception SDONotExists ターゲットのSDOが存在しない。
		\exception NotAvailable SDOは存在するが応答がない。
		\exception InternalError 内部的エラーが発生した。
		\return    SDO が提供する全ての Service の ServiceProfile。

		\else

		\brief [CORBA interface] Getting SDO ServiceProfile

		This operation returns a list of ServiceProfiles that the SDO has.
		If the SDO does not provide any service, then an empty list is returned.
		This operation throws SDOException with one of the following types.

		\exception NotAvailable if the target SDO is reachable but cannot
			respond.
		\exception InternalError if the target SDO cannot execute the operation
			completely due to some internal error.
		\return    List of ServiceProfiles of all the services the SDO is
			providing.

		\endif
		"""
		try:
			return self._sdoSvcProfiles
		except:
			raise SDOPackage.InternalError("get_service_profiles()")

		return []


	def get_service_profile(self, _id):
		"""
		\if jp

		\brief [CORBA interface] 特定のServiceProfileの取得 

		引数 "id" で指定された名前のサービスの ServiceProfile を返す。

		\param     _id(string) SDO Service の ServiceProfile に関連付けられた識別子。
		\return    指定された SDO Service の ServiceProfile。
		\exception NotAvailable SDOは存在するが応答がない。
		\exception InternalError 内部的エラーが発生した。

		\else

		\brief [CORBA interface] Getting Organizations

		This operation returns the ServiceProfile that is specified by the
		argument "id."

		\param     _id(string) The identifier referring to one of the ServiceProfiles.
		\return    The profile of the specified service.
		\exception NotAvailable If the target SDO is reachable but cannot
			respond.
		\exception InternalError If the target SDO cannot execute the operation
			completely due to some internal error.

		\endif
		"""
		if not _id:
			raise SDOPackage.InvalidParameter("get_service_profile(): Empty name.")

		try:
			index = OpenRTM.CORBA_SeqUtil.find(self._sdoSvcProfiles, self.svc_name(_id))

			if index < 0:
				raise SDOPackage.InvalidParameter("get_service_profile(): Not found")

			return self._sdoSvcProfiles[index]
		except:
			raise SDOPackage.InternalError("get_service_profile()")

		return SDOPackage.ServiceProfile("", "", [], None)


	def get_sdo_service(self, _id):
		"""
		\if jp

		\brief [CORBA interface] 指定された SDO Service の取得

		このオペレーションは引数 "id" で指定された名前によって区別される
		SDO の Service へのオブジェクト参照を返す。 SDO により提供される
		Service はそれぞれ一意の識別子により区別される。

		\param _id(string) SDO Service に関連付けられた識別子。
		\return 要求された SDO Service への参照。

		\else

		\brief [CORBA interface] Getting specified SDO Service's reference

		This operation returns an object implementing an SDO's service that
		is identified by the identifier specified as an argument. Different
		services provided by an SDO are distinguished with different
		identifiers. See OMG SDO specification Section 2.2.8, "ServiceProfile,"
		on page 2-12 for more details.

		\param _id(string) The identifier referring to one of the SDO Service
		\return The object implementing the requested service.

		\endif
		"""
		if not _id:
			raise SDOPackage.InvalidParameter("get_service(): Empty name.")

		try:
			index = OpenRTM.CORBA_SeqUtil.find(self._sdoSvcProfiles, self.svc_name(_id))

			if index < 0:
				raise SDOPackage.InvalidParameter("get_service(): Not found")

			return self._sdoSvcProfiles[index].service
		except:
			raise SDOPackage.InternalError("get_service()")
		return SDOPackage.SDOService._nil


	def get_configuration(self):
		"""
		\if jp

		\brief [CORBA interface] Configuration オブジェクトの取得 

		このオペレーションは Configuration interface への参照を返す。
		Configuration interface は各 SDO を管理するためのインターフェースの
		ひとつである。このインターフェースは DeviceProfile, ServiceProfile,
		Organization で定義された SDO の属性値を設定するために使用される。
		Configuration インターフェースの詳細については、OMG SDO specification
		の 2.3.5節, p.2-24 を参照のこと。

		\return SDO の Configuration インターフェースへの参照
		\exception InterfaceNotImplemented SDOはConfigurationインターフェースを
			持たない。
		\exception SDONotExists ターゲットのSDOが存在しない。
		\exception NotAvailable SDOは存在するが応答がない。
		\exception InternalError 内部的エラーが発生した。

		\else

		\brief [CORBA interface] Getting Configuration object

		This operation returns an object implementing the Configuration
		interface. The Configuration interface is one of the interfaces thatreturn RTC.BAD_PARAMETER
		each SDO maintains. The interface is used to configure the attributes
		defined in DeviceProfile, ServiceProfile, and Organization.
		See OMG SDO specification Section 2.3.5, "Configuration Interface,"
		on page 2-24 for more details about the Configuration interface.

		\return The Configuration interface of an SDO.
		\exception InterfaceNotImplemented The target SDO has no Configuration
			interface.
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		if self._SdoConfig == None:
			raise SODPackage.InterfaceNotImplemented()
		try:
			return self._SdoConfig
		except:
			raise SDOPackage.InternalError("get_configuration()")
		return SDOPackage.Configuration._nil


	def get_monitoring(self):
		"""
		\if jp

		\brief [CORBA interface] Monitoring オブジェクトの取得 

		このオペレーションは Monitoring interface への参照を返す。
		Monitoring interface は SDO が管理するインターフェースの一つである。
		このインターフェースは SDO のプロパティをモニタリングするために
		使用される。
		Monitoring interface の詳細については OMG SDO specification の
		2.3.7節 "Monitoring Interface" p.2-35 を参照のこと。

		\return SDO の Monitoring interface への参照
		\exception InterfaceNotImplemented SDOはConfigurationインターフェースを
			持たない。
		\exception SDONotExists ターゲットのSDOが存在しない。
		\exception NotAvailable SDOは存在するが応答がない。
		\exception InternalError 内部的エラーが発生した。

		\else

		\brief [CORBA interface] Get Monitoring object

		This operation returns an object implementing the Monitoring interface.
		The Monitoring interface is one of the interfaces that each SDO
		maintains. The interface is used to monitor the properties of an SDO.
		See OMG SDO specification Section 2.3.7, "Monitoring Interface," on
		page 2-35 for more details about the Monitoring interface.

		\return The Monitoring interface of an SDO.
		\exception InterfaceNotImplemented The target SDO has no Configuration
			interface.
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		raise SDOPackage.InterfaceNotImplemented("Exception: get_monitoring")
		return SDOPackage.Monitoring._nil


	def get_organizations(self):
		"""
		\if jp

		\brief [CORBA interface] Organization リストの取得 

		SDO は0個以上の Organization (組織)に所属することができる。 もし SDO が
		1個以上の Organization に所属している場合、このオペレーションは所属する
		Organization のリストを返す。SDO が どの Organization にも所属していない
		場合には、空のリストが返される。

		\return SDO が所属する Organization のリスト。
		\exception SDONotExists ターゲットのSDOが存在しない。
		\exception NotAvailable SDOは存在するが応答がない。
		\exception InternalError 内部的エラーが発生した。
		\else

		\brief [CORBA interface] Getting Organizations

		An SDO belongs to zero or more organizations. If the SDO belongs to one
		or more organizations, this operation returns the list of organizations
		that the SDO belongs to. An empty list is returned if the SDO does not
		belong to any Organizations.

		\return The list of Organizations that the SDO belong to.
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		try:
			return self._sdoOrganizations
		except:
			raise SDOPackage.InternalError("get_organizations()")
		return []


	def get_status_list(self):
		"""
		\if jp

		\brief [CORBA interface] SDO Status リストの取得 

		このオペレーションは SDO のステータスを表す NVList を返す。

		\return SDO のステータス。
		\exception SDONotExists ターゲットのSDOが存在しない。
		\exception NotAvailable SDOは存在するが応答がない。
		\exception InternalError 内部的エラーが発生した。

		\else

		\brief [CORBA interface] Get SDO Status

		This operation returns an NVlist describing the status of an SDO.

		\return The actual status of an SDO.
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.

		\endif
		"""
		try:
			return self._sdoStatus
		except:
			raise SDOPackage.InternalError("get_status_list()")
		return []


	def get_status(self, name):
		"""
		\if jp

		\brief [CORBA interface] SDO Status の取得 

		This operation returns the value of the specified status parameter.

		\param name(string) SDO のステータスを定義するパラメータ。
		\return 指定されたパラメータのステータス値。
		\exception SDONotExists ターゲットのSDOが存在しない。
		\exception NotAvailable SDOは存在するが応答がない。
		\exception InvalidParameter 引数 "name" が null あるいは存在しない。
		\exception InternalError 内部的エラーが発生した。
		\else

		\brief [CORBA interface] Get SDO Status

		\param name(string) One of the parameters defining the "status" of an SDO.
		\return The value of the specified status parameter.
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InvalidParameter The parameter defined by "name" is null or
			does not exist.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.


		\endif
		"""
		index = OpenRTM.CORBA_SeqUtil.find(self._sdoStatus, self.nv_name(name))
		if index < 0:
			raise SDOPackage.InvalidParameter("get_status(): Not found")

		try:
			return any.to_any(self._sdoStatus[index].value)
		except:
			raise SDOPackage.InternalError("get_status()")
		return any.to_any("")


    #============================================================
    # Local interfaces
    #============================================================
	def getInstanceName(self):
		return self._profile.instance_name

	
	def setInstanceName(self, instance_name):
		"""
		 \param instance_name(string)
		"""
		self._properties.setProperty("instance_name",instance_name)
		self._profile.instance_name = self._properties.getProperty("instance_name")

	
	def getTypeName(self):
		return self._profile.type_name

	
	def getDescription(self):
		return self._profile.description

	
	def getVersion(self):
		return self._profile.version

	
	def getVendor(self):
		return self._profile.vendor

	
	def getCategory(self):
		return self._profile.category


	def getNamingNames(self):
		return string.split(self._properties.getProperty("naming.names"), ",")

	
	def setObjRef(self, rtobj):
		"""
		 \param rtobj(RTC.RTObject)
		"""
		self._objref = rtobj
		return

	
	def getObjRef(self):
		return self._objref


	def setProperties(self, prop):
		"""
		\if jp

		\brief [local interface] RTC のプロパティを設定する

		RTC が保持すべきプロパティを設定する。与えられるプロパティは、
		ComponentProfile 等に設定されるべき情報を持たなければならない。
		このオペレーションは通常 RTC が初期化される際に Manager から
		呼ばれることを意図している。

		\param prop(OpenRTM.Properties) RTC のプロパティ

		\else

		\brief [local interface] Set RTC property

		This operation sets the properties to the RTC. The given property
		values should include information for ComponentProfile.
		Generally, this operation is designed to be called from Manager, when
		RTC is initialized

		\param prop(OpenRTM.Properties) Property for RTC.

		\endif
		"""
		self._properties = self._properties.mergeProperties(prop)
		self._profile.instance_name = self._properties.getProperty("instance_name")
		self._profile.type_name     = self._properties.getProperty("type_name")
		self._profile.description   = self._properties.getProperty("description")
		self._profile.version       = self._properties.getProperty("version")
		self._profile.vendor        = self._properties.getProperty("vendor")
		self._profile.category      = self._properties.getProperty("category")


	def getProperties(self):
		"""
		\if jp

		\brief [local interface] RTC のプロパティを取得する

		RTC が保持しているプロパティを返す。
		RTCがプロパティを持たない場合は空のプロパティが返される。

		\return RTC のプロパティ

		\else

		\brief [local interface] Get RTC property

		This operation returns the properties of the RTC.
		Empty property would be returned, if RTC has no property.

		\return Property for RTC.

		\endif
		"""
		return self._properties


	def bindParameter(self, param_name, var,
					  def_val, trans=None):
		"""
		\brief
	    var はリストを渡す必要がある。
		\param param_name(string) name of Parameter.
		\param var(variable) object.
		\param def_val(string) stirng of parameter.
		"""
		if trans == None:
			_trans = OpenRTM.stringTo
		else:
			_trans = trans
		self._configsets.bindParameter(param_name, var, def_val, _trans)
		return True


	def updateParameters(self, config_set):
		self._configsets.update(config_set)
		return


	def registerPort(self, port):
		"""
		\if jp

		\brief [local interface] Port を登録する

		RTC が保持するPortを登録する。
		Port を外部からアクセス可能にするためには、このオペレーションにより
		登録されていなければならない。登録される Port はこの RTC 内部において
		PortProfile.name により区別される。したがって、Port は RTC 内において、
		ユニークな PortProfile.name を持たなければならない。
		登録された Port は内部で適切にアクティブ化された後、その参照と
		オブジェクト参照がリスト内に保存される。

		\param port(OpenRTM.PortBase) RTC に登録する Port

		\else

		\brief [local interface] Register Port

		This operation registers a Port to be held by this RTC.
		In order to enable access to the Port from outside of RTC, the Port
		must be registered by this operation. The Port that is registered by
		this operation would be identified by PortProfile.name in the inside of
		RTC. Therefore, the Port should have unique PortProfile.name in the RTC.
		The registering Port would be activated properly, and the reference
		and the object reference would be stored in lists in RTC.

		\param port(OpenRTM.PortBase) Port which is registered in the RTC

		\endif
		"""
		self._portAdmin.registerPort(port)
		return


	def registerInPort(self, name, inport):
		"""
		 \param name(string)
		 \param inport(OpenRTM.InPort)
		"""
		port = OpenRTM.DataInPort(name, inport)
		self.registerPort(port)
		return


	def registerOutPort(self, name, outport):
		"""
		 \param name(string)
		 \param outport(OpenRTM.OutPort)
		"""
		port = OpenRTM.DataOutPort(name, outport)
		self.registerPort(port)
		return


	def deletePort(self, port):
		"""
		\if jp
		\brief [local interface] Port の登録を削除する

		RTC が保持するPortの登録を削除する。
		\param port(OpenRTM.PortBase) RTC に登録する Port
		\else
		\brief [local interface] Register Port

		This operation registers a Port to be held by this RTC.
		In order to enable access to the Port from outside of RTC, the Port
		must be registered by this operation. The Port that is registered by
		this operation would be identified by PortProfile.name in the inside of
		RTC. Therefore, the Port should have unique PortProfile.name in the RTC.
		The registering Port would be activated properly, and the reference
		and the object reference would be stored in lists in RTC.
		\param port(OpenRTM.PortBase) Port which is registered in the RTC
		\endif
		"""
		self._portAdmin.deletePort(port)
		return


	def deletePortByName(self, port_name):
		"""
		 \param port_name(string)
		"""
		self._portAdmin.deletePortByName(port_name)
		return

	
	def finalizePorts(self):
		self._portAdmin.finalizePorts()
		return



	def shutdown(self):
		try:
			self.finalizePorts()
			self._poa.deactivate_object(self._poa.servant_to_id(self._SdoConfigImpl))
			self._poa.deactivate_object(self._poa.servant_to_id(self))
		except:
			traceback.print_exception(*sys.exc_info())

		if self._manager != None:
			self._manager.cleanupComponent(self)
			
		return



	class svc_name:
		"""
		\brief SDOService のプロファイルリストからidでサーチするための
		ファンクタクラス
		"""
		def __init__(self, _id):
			self._id= _id

		def __call__(self, prof):
			return self._id == prof.id

    #------------------------------------------------------------
    # Functor
    #------------------------------------------------------------
	class nv_name:
		def __init__(self, _name):
			self._name = _name

		def __call__(self, nv):
			return self._name == nv.name


	class ec_copy:
		def __init__(self, eclist):
			self._eclist = eclist

		def __call__(self, ecs):
			self._eclist.append(ecs)


	class deactivate_comps:
		def __init__(self, comp):
			self._comp = comp

		def __call__(self, ec):
			ec.deactivate_component(self._comp)


# RtcBase = RTObject_impl
