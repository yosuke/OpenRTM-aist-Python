#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
 \file  OutPortProvider.py
 \brief OutPortProvider class
 \date  $Date: 2007/09/05$
 \author Noriaki Ando <n-ando@aist.go.jp>

 Copyright (C) 2006
     Noriaki Ando
     Task-intelligence Research Group,
     Intelligent Systems Research Institute,
     National Institute of
         Advanced Industrial Science and Technology (AIST), Japan
     All rights reserved.
"""



import OpenRTM

class OutPortProvider:
	"""
	\if jp

	\brief OutPort

	- Port に対して何を提供しているかを宣言する。
		PortProfile の properties に Provider に関する情報を追加する。
	(例) OutPort を Provide する場合

	OutPortCorbaProvider が以下を宣言
	dataport.interface_type = CORBA_Any
	dataport.dataflow_type = Push, Pull
	dataport.subscription_type = Once, New, Periodic

	OutPortRawTCPProviderが以下を宣言
	dataport.interface_type = RawTCP
	dataport.dataflow_type = Push, Pull
	dataport.subscription_type = Once, New, Periodic

	最終的に PortProfile::properties は
	dataport.interface_type = CORBA_Any, RawTCP
	dataport.dataflow_type = Push, Pull
	dataport.subscription_type = Once, New, Periodic
	\else
	\endif
	"""
	def __init__(self):
		self._properties = []

		
	def __del__(self):
		"""
		\if jp
		\brief デストラクタ
		\else
		\brief Destructor
		\endif
		"""
		pass


	def publishInterfaceProfile(self, prop):
		"""
		 \param prop(SDOPackage.NVList)
		"""
		OpenRTM.NVUtil.appendStringValue(prop, "dataport.data_type", self._dataType)
		OpenRTM.NVUtil.appendStringValue(prop, "dataport.interface_type", self._interfaceType)
		OpenRTM.NVUtil.appendStringValue(prop, "dataport.dataflow_type", self._dataflowType)
		OpenRTM.NVUtil.appendStringValue(prop, "dataport.subscription_type", self._subscriptionType)
		

	def publishInterface(self, prop):
		"""
		 \param prop(SDOPackage.NVList)
		"""
		if not OpenRTM.NVUtil.isStringValue(prop,"dataport.interface_type",self._interfaceType):
			return

		OpenRTM.NVUtil.append(prop,self._properties)
    

	def setPortType(self, port_type):
		"""
		 \param port_type(string)
		"""
		self._portType = port_type


	def setDataType(self, data_type):
		"""
		 \param data_type(string)
		"""
		self._dataType = data_type
		

	def setInterfaceType(self, interface_type):
		"""
		 \param interface_type(string)
		"""
		self._interfaceType = interface_type


	def setDataFlowType(self, dataflow_type):
		"""
		 \param dataflow_type(string)
		"""
		self._dataflowType = dataflow_type
		

	def setSubscriptionType(self, subs_type):
		"""
		 \param subs_type(string)
		"""
		self._subscriptionType = subs_type


