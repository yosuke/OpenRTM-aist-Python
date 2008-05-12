#!/usr/bin/env python
# -*- coding: euc-jp -*-


"""
  \file  InPortCorbaProvider.py
  \brief InPortCorbaProvider class
  \date  $Date: 2007/09/25 $
  \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
 
  Copyright (C) 2006
      Noriaki Ando
      Task-intelligence Research Group,
      Intelligent Systems Research Institute,
      National Institute of
          Advanced Industrial Science and Technology (AIST), Japan
      All rights reserved.
"""
 

from  omniORB import any
import sys
import traceback

import OpenRTM
import RTC,RTC__POA



class InPortCorbaProvider(OpenRTM.InPortProvider, RTC__POA.InPortAny):
	"""
	\if jp
	\class InPortCorbaProvider
	\brief InPortCorbaProvider クラス
	\else
	\class InPortCorbaProvider
	\brief InPortCorbaProvider class
	\endif
	"""


	def __init__(self, buffer_):
		"""
		\if jp
		\brief コンストラクタ
		このクラスのインスタンス生成時には、ポートオブジェクトを
		引数のbuffer_として渡す必要がある。
		\param buffer_(OpenRTM.BufferBase)
		\else
		\brief Constructor
		\param buffer_(OpenRTM.BufferBase)
		\endif
		"""
		OpenRTM.InPortProvider.__init__(self)
		self._buffer = buffer_

		# PortProfile setting
		self.setDataType(self._buffer.getPortDataType())
		self.setInterfaceType("CORBA_Any")
		self.setDataFlowType("Push, Pull")
		self.setSubscriptionType("Any")

		# ConnectorProfile setting
		self._objref = self._this()


	# prop : SDOPackage.NameValueのリスト
	def publishInterface(self, prop):
		"""
		 \brief publish interface
		 \param prop(SDOPackage::NameValueのリスト)
		"""
		if not OpenRTM.NVUtil.isStringValue(prop,
						    "dataport.interface_type",
						    "CORBA_Any"):
			return

		nv = self._properties
		OpenRTM.CORBA_SeqUtil.push_back(nv,
						OpenRTM.NVUtil.newNV("dataport.corba_any.inport_ref",
								     self._objref))
		OpenRTM.NVUtil.append(prop, nv)


	def __del__(self):
		pass


	def put(self, data):
		"""
		 \brief put オペレーションの実装
		 \param data(CORBA::Any)
		"""
		try:
			tmp = any.from_any(data, keep_structs=True)
			self._buffer.write(tmp)
		except:
			traceback.print_exception(*sys.exc_info())
			return

		return
