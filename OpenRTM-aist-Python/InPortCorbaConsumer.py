#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
  \file  InPortCorbaConsumer.py
  \brief InPortCorbaConsumer class
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
 

from omniORB import CORBA
from omniORB import any
import sys
import traceback

import RTC, RTC__POA
import OpenRTM
 


class InPortCorbaConsumer(OpenRTM.InPortConsumer,OpenRTM.CorbaConsumer):
	
	def __init__(self, buffer_, consumer=None):
		"""
		 \brief コンストラクタ
		 \param buffer_(OpenRTM.BufferBase)
		 \param consumer(InPortCorbaConsumer)
		"""
		if consumer:
			OpenRTM.CorbaConsumer.__init__(self, consumer=consumer)
			self._buffer = consumer._buffer
			return
		
		OpenRTM.CorbaConsumer.__init__(self)
		self._buffer = buffer_

	# operator=(const InPortCorbaConsumer<DataType>& consumer) の実装
	def equal_operator(self, consumer):
		"""
		 \brief operator=()の実装
		 \param consumer(InPortCorbaConsumer)
		"""
		if self == consumer:
			return self

		self._buffer = consumer._buffer


	def put(self, data):
		"""
		 \brief putオペレーション呼び出し
		 \param data(RTC.BasicDataType)
		"""
		tmp = any.to_any(data)
		obj = self._ptr()._narrow(RTC.InPortAny)
		obj.put(tmp)


	def push(self):
		"""
		 \brief putオペレーション呼び出し
		"""
		data = [None]
		self._buffer.read(data)
		tmp = any.to_any(data[0])

		if not self._ptr():
			return

		obj = self._ptr()._narrow(RTC.InPortAny)

		# 本当はエラー処理をすべき
		if CORBA.is_nil(obj):
			return
		try:
			obj.put(tmp)
		except:
			# オブジェクトが無効になったらdisconnectすべき
			traceback.print_exception(*sys.exec_info())
			return


	def clone(self):
		return OpenRTM.InPortCorbaConsumer(self, consumer=self)


	def subscribeInterface(self, properties):
		"""
		 \brief subscribe interface
		 \param properties(SDOPackage::NameValueのリスト)
		"""
		if not OpenRTM.NVUtil.isStringValue(properties,
											"dataport.dataflow_type",
											"Push"):
			return False

		index = OpenRTM.NVUtil.find_index(properties,
										  "dataport.corba_any.inport_ref")
      
		if index < 0:
			return False

		obj = None
		try:
			obj = any.from_any(properties[index].value,keep_structs=True)
		except:
			return False

		if not CORBA.is_nil(obj):
			self.setObject(obj)
			return True

		return False


	def unsubscribeInterface(self, properties):
		pass
