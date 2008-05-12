#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
  \file DataOutPort.py
  \brief Base class of OutPort
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


class DataOutPort(OpenRTM.PortBase):
	
	"""
	\if jp
	\class DataOutPort
	\brief InPort 用 Port
	\else
	\class DataOutPort
	\brief InPort abstruct class
	\endif
	"""


	def __init__(self, name, outport):
		"""
		\if jp
		\brief コンストラクタ
		\param name(string)
		\param outport(OpenRTM.OutPort)
		\else
		\brief Constructor
		\param name(string)
		\param outport(OpenRTM.OutPort)
		\endif
		"""
		OpenRTM.PortBase.__init__(self, name)
		self._outport = outport
		# PortProfile::properties を設定
		self.addProperty("port.port_type", "DataOutPort")
		self._providers = []
		self._providers.append(OpenRTM.OutPortCorbaProvider(outport))
		self._providers[-1].publishInterfaceProfile(self._profile.properties)
		self._consumers = []
		self._consumers.append(OpenRTM.InPortCorbaConsumer(outport))
		self._pf = OpenRTM.PublisherFactory()


	def __del__(self):
		"""
		\if jp
		\brief デストラクタ
		\else
		\brief Destructor
		\endif
		"""
		pass

    
	"""
      \if jp
      \brief [CORBA interface] Port の接続を行う
     
      OutPort と InPort との接続を行う。
     
      OutPort 側の connect() では以下のシーケンスで処理が行われる。
     
      1. OutPort に関連する connector 情報の生成およびセット
     
      2. InPortに関連する connector 情報の取得
       - ConnectorProfile::properties["dataport.corba_any.inport_ref"]に
         OutPortAny のオブジェクトリファレンスが設定されている場合、
         リファレンスを取得してConsumerオブジェクトにセットする。
         リファレンスがセットされていなければ無視して継続。
         (OutPortがconnect() 呼び出しのエントリポイントの場合は、
         InPortのオブジェクトリファレンスはセットされていないはずである。)
      3. PortBase::connect() をコール
         Portの接続の基本処理が行われる。
      4. 上記2.でInPortのリファレンスが取得できなければ、再度InPortに
         関連する connector 情報を取得する。
     
      5. ConnectorProfile::properties で与えられた情報から、
         OutPort側の初期化処理を行う。
     
      - [dataport.interface_type]
      -- CORBA_Any の場合: 
         InPortAny を通してデータ交換される。
         ConnectorProfile::properties["dataport.corba_any.inport_ref"]に
         InPortAny のオブジェクトリファレンスをセットする。
      -- RawTCP の場合: Raw TCP socket を通してデータ交換される。
         ConnectorProfile::properties["dataport.raw_tcp.server_addr"]
         にInPort側のサーバアドレスをセットする。
     
      - [dataport.dataflow_type]
      -- Pushの場合: Subscriberを生成する。Subscriberのタイプは、
         dataport.subscription_type に設定されている。
      -- Pullの場合: InPort側がデータをPull型で取得するため、
         特に何もする必要が無い。
     
      - [dataport.subscription_type]
      -- Onceの場合: SubscriberOnceを生成する。
      -- Newの場合: SubscriberNewを生成する。
      -- Periodicの場合: SubscriberPeriodicを生成する。
     
      - [dataport.push_interval]
      -- dataport.subscription_type=Periodicの場合周期を設定する。
     
      6. 上記の処理のうち一つでもエラーであれば、エラーリターンする。
         正常に処理が行われた場合はRTC::RTC_OKでリターンする。
       
      \else
      \brief [CORBA interface] Connect the Port
      \endif
	"""


	def publishInterfaces(self, connector_profile):
		"""
		\if jp

		\brief Interface 情報を公開する

		このオペレーションは、notify_connect() 処理シーケンスの始めにコール
		される関数である。
		notify_connect() では、

		- publishInterfaces()
		- connectNext()
		- subscribeInterfaces()
		- updateConnectorProfile()

		の順に関数がコールされ接続処理が行われる。
		<br>
		このオペレーションは、新規の connector_id に対しては接続の生成、
		既存の connector_id に対しては更新が適切に行われる必要がある。

		\param connector_profile(RTC.ConnectorProfile) 接続に関するプロファイル情報
		\return ReturnCode_t 型のリターンコード

		\else

		\brief Publish interface information

		This operation is method that would be called at the
		beginning of the notify_connect() process sequence.
		In the notify_connect(), the following methods would be called in order.

		- publishInterfaces()
		- connectNext()
		- subscribeInterfaces()
		- updateConnectorProfile() 

		This operation should create the new connection for the new
		connector_id, and should update the connection for the existing
		connection_id.

		\param connector_profile(RTC.ConnectorProfile) The connection profile information
		\return The return code of ReturnCode_t type.

		\endif
		"""
		publish = self.publish(connector_profile.properties)
		for provider in self._providers:
			publish(provider)
		return RTC.RTC_OK


	def subscribeInterfaces(self, connector_profile):
		"""
		\if jp

		\brief Interface 情報を取得する

		このオペレーションは、notify_connect() 処理シーケンスの中間にコール
		される関数である。
		notify_connect() では、

		- publishInterfaces()
		- connectNext()
		- subscribeInterfaces()
		- updateConnectorProfile()

		の順に関数がコールされ接続処理が行われる。

		\param connector_profile(RTC.ConnectorProfile) 接続に関するプロファイル情報
		\return ReturnCode_t 型のリターンコード

		\else

		\brief Publish interface information

		This operation is method that would be called at the
		mid-flow of the notify_connect() process sequence.
		In the notify_connect(), the following methods would be called in order.

		- publishInterfaces()
		- connectNext()
		- subscribeInterfaces()
		- updateConnectorProfile()

		\param connector_profile(RTC.ConnectorProfile) The connection profile information
		\return The return code of ReturnCode_t type.

		\endif
		"""
		subscribe = self.subscribe(prof=connector_profile)
		for consumer in self._consumers:
			subscribe(consumer)


		if not subscribe._consumer:
			return RTC.RTC_OK

    
		# Publisherを生成
		prop = OpenRTM.NVUtil.toProperties(connector_profile.properties)
		publisher = self._pf.create(subscribe._consumer.clone(), prop)

		# PublisherをOutPortにアタッチ
		self._outport.attach(connector_profile.connector_id, publisher)

		return RTC.RTC_OK


	def unsubscribeInterfaces(self, connector_profile):
		"""
		\if jp

		\brief Interface の接続を解除する

		このオペレーションは、notify_disconnect() 処理シーケンスの終わりにコール
		される関数である。
		notify_disconnect() では、
		- disconnectNext()
		- unsubscribeInterfaces()
		- eraseConnectorProfile()
		の順に protected 関数がコールされ接続解除処理が行われる。

		\param connector_profile(RTC.ConnectorProfile) 接続に関するプロファイル情報

		\else

		\brief Disconnect interface connection

		This operation is method that would be called at the
		end of the notify_disconnect() process sequence.
		In the notify_disconnect(), the following methods would be called.
		- disconnectNext()
		- unsubscribeInterfaces()
		- eraseConnectorProfile() 

		\param connector_profile(RTC.ConnectorProfile) The connection profile information

		\endif
		"""
		publisher = self._outport.detach(connector_profile.connector_id)
		self._pf.destroy(publisher)
		return


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
			 \param provider(OpenRTM.OutPortProvider)
			"""
			provider.publishInterface(self._prop)


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
			 \param consumer(OpenRTM.InPortConsumer)
			"""
			consumer.unsubscribeInterface(self._prop)


	class subscribe:
		
		def __init__(self, prof=None, subs=None):
			"""
			 \brief functor
			 \param prof(RTC.ConnectorProfile)
			 \param subs(subscribe)
			"""
			if prof and not subs:
				self._prof = prof
				self._consumer = None
			elif not prof and subs:
				self._prof = subs._prof
				self._consumer = subs._consumer
			else:
				print "DataOutPort.subscribe: Invalid parameter."


		def __call__(self, cons):
			"""
			 \brief operator()の実装
			 \param cons(OpenRTM.InPortConsumer)
			"""
			if cons.subscribeInterface(self._prof.properties):
				self._consumer = cons
