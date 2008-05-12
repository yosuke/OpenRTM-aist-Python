#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
  \file  OutPortCorbaConsumer.py
  \brief OutPortCorbaConsumer class
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
 
from omniORB import any
from omniORB import CORBA

import OpenRTM
import RTC, RTC__POA 


class OutPortCorbaConsumer(OpenRTM.OutPortConsumer,OpenRTM.CorbaConsumer):
	"""
	\if jp
	\class OutPortCorbaConsumer
	\brief OutPortCorbaConsumer クラス
	\else
	\class OutPortCorbaConsumer
	\brief OutPortCorbaConsumer class
	\endif
	"""

	def __init__(self, buffer_):
		"""
		\if jp
		\brief コンストラクタ
		\param buffer_(OpenRTM.BufferBase)
		\else
		\brief Constructor
		\param buffer_(OpenRTM.BufferBase)
		\endif
		"""
		self._buffer = buffer_
		OpenRTM.CorbaConsumer.__init__(self)


	def __del__(self):
		"""
		\if jp
		\brief デストラクタ
		\else
		\brief Destructor
		\endif
		"""
		pass


	def get(self, data):
		"""
		 \param data(data)
		 \return bool
		"""
		try:
			obj = self._ptr()._narrow(RTC.OutPortAny)
			if CORBA.is_nil(obj):
				return False
			d = any.from_any(obj.get(), keep_structs=True)
			data[0] = d
			return True
		except:
			return False
		
		return False


	def pull(self):
		data = [None]
		if self.get(data):
			self._buffer.write(data[0])
    

	def subscribeInterface(self, properties):
		"""
		 \param properties(SDOPackage.NVList)
		 \return bool
		"""
		index = OpenRTM.NVUtil.find_index(properties,
										  "dataport.corba_any.outport_ref")
		if index < 0:
			return False

		try:
			obj = any.from_any(properties[index].value, keep_structs=True)
			self.setObject(obj)
			return True
		except:
			return False

		return False


	def unsubscribeInterface(self, properties):
		"""
		 \param properties(SDOPackage.NVList)
		"""
		index = OpenRTM.NVUtil.find_index(properties,
										  "dataport.corba_any.outport_ref")
		if index < 0:
			return

		try:
			obj = any.from_any(properties[index].value, keep_structs=True)
			if self.getObject()._is_equivalent(obj):
				self.releaseObject()
		except:
			return
