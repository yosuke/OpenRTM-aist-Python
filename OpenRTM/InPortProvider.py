#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
  \file  InPortProvider.py
  \brief InPortProvider class
  \date  $Date: 2007/09/20 $
  \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
 
  Copyright (C) 2006
      Noriaki Ando
      Task-intelligence Research Group,
      Intelligent Systems Research Institute,
      National Institute of
          Advanced Industrial Science and Technology (AIST), Japan
      All rights reserved.
"""


import OpenRTM
import SDOPackage, SDOPackage__POA



class InPortProvider:
	"""
	\if jp
	\class InPortProvider
	\brief InPortProvider クラス
	\else
	\class InPortProvider
	\brief InPortProvider class
	\endif
	"""


	def __init__(self):
		"""
		\if jp
		\brief コンストラクタ
		\else
		\brief Constructor
		\endif
		"""
		self._properties = []
		self._dataType = ""
		self._interfaceType = ""
		self._dataflowType = ""
		self._subscriptionType = ""


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
		 \brief publish interface
		 \param prop(SDOPackage::NameValueのリスト)
		"""
		OpenRTM.NVUtil.appendStringValue(prop, "dataport.data_type",
						 self._dataType)
		OpenRTM.NVUtil.appendStringValue(prop, "dataport.interface_type",
						 self._interfaceType)
		OpenRTM.NVUtil.appendStringValue(prop, "dataport.dataflow_type",
						 self._dataflowType)
		OpenRTM.NVUtil.appendStringValue(prop, "dataport.subscription_type",
						 self._subscriptionType)


	def publishInterface(self, prop):
		"""
		 \brief publish interface
		 \param prop(SDOPackage::NameValueのリスト)
		"""
		if not OpenRTM.NVUtil.isStringValue(prop,
						    "dataport.interface_type",
						    self._interfaceType):
			return

		OpenRTM.NVUtil.append(prop, self._properties)


	def setDataType(self, data_type):
		"""
		 \brief set data type
		 \param data_type(string)
		"""
		self._dataType = data_type


	def setInterfaceType(self, interface_type):
		"""
		 \brief set interface type
		 \param interface_type(string)
		"""
		self._interfaceType = interface_type


	def setDataFlowType(self, dataflow_type):
		"""
		 \brief set data flow type
		 \param dataflow_type(string)
		"""
		self._dataflowType = dataflow_type


	def setSubscriptionType(self, subs_type):
		"""
		 \brief set subscription type
		 \param subs_type(string)
		"""
		self._subscriptionType = subs_type
