#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
  \file DataInPort.py
  \brief RTC::Port implementation for Data InPort
  \date $Date: 2007/09/20 $
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
import RTC, RTC__POA


class DataInPort(OpenRTM.PortBase):
	
	"""
	\if jp
	\class DataInPort
	\brief InPort 用 Port
	\else
	\class DataInPort
	\brief InPort abstruct class
	\endif
	"""


	def __init__(self, name, inport):
		"""
		 \if jp
		 \brief クラスコンストラクタ
		 \param name(string)
		 \param inport(OpenRTM.InPort)

		 \else
		 \brief class constructor
		 \param name(string)
		 \param inport(OpenRTM.InPort)
		 \endif
		"""
		OpenRTM.PortBase.__init__(self, name)

		# PortProfile::properties を設定
		self.addProperty("port.port_type", "DataInPort")
		self._providers = []
		self._providers.append(OpenRTM.InPortCorbaProvider(inport))
		self._providers[-1].publishInterfaceProfile(self._profile.properties)
		self._consumers = []
		self._consumers.append(OpenRTM.OutPortCorbaConsumer(inport))
		self._dummy = [1]


	def __del__(self):
		pass


	###################################################################
	#                    Functor class                                #
	#                                                                 #
	class publish:
		
		def __init__(self, prop):
			"""
			 \brief functor
			 \param prop(SDOPackage::NameValueのリスト)
			"""
			self._prop = prop

		def __call__(self, provider):
			"""
			 \brief operator()の実装
			 \param provider(OpenRTM.InPortProvider)
			"""
			provider.publishInterface(self._prop)

	class subscribe:
		
		def __init__(self, prop):
			"""
			 \brief functor
			 \param prop(SDOPackage::NameValueのリスト)
			"""
			self._prop = prop

		def __call__(self, consumer):
			"""
			 \brief operator()の実装
			 \param provider(OpenRTM.OutPortConsumer)
			"""
			consumer.subscribeInterface(self._prop)

	class unsubscribe:
		
		def __init__(self, prop):
			"""
			 \brief functor
			 \param prop(SDOPackage::NameValueのリスト)
			"""
			self._prop = prop

		def __call__(self, consumer):
			"""
			 \brief operator()の実装
			 \param provider(OpenRTM.OutPortConsumer)
			"""
			consumer.unsubscribeInterface(self._prop)

	#                                                                 #
	###################################################################


	def publishInterfaces(self, connector_profile):
		"""
		 \brief publish interface
		 \param connector_profile(RTC.ConnectorProfile)
		"""
		if len(self._dummy) != 1:
			print "Memory access violation was detected."
			print "dummy.size(): ", len(self._dummy)
			print "size() should be 1."

		publish = self.publish(connector_profile.properties)
		for provider in self._providers:
			publish(provider)

		return RTC.RTC_OK
			

	def subscribeInterfaces(self, connector_profile):
		"""
		 \brief subscribe interface
		 \param connector_profile(RTC.ConnectorProfile)
		"""
		subscribe = self.subscribe(connector_profile.properties)
		for consumer in self._consumers:
			subscribe(consumer)

		return RTC.RTC_OK


	def unsubscribeInterfaces(self, connector_profile):
		"""
		 \brief unsubscribe interface
		 \param connector_profile(RTC.ConnectorProfile)
		"""
		unsubscribe = self.unsubscribe(connector_profile.properties)
		for consumer in self._consumers:
			unsubscribe(consumer)
		
    
