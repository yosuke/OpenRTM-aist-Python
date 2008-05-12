#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
  \file  CorbaPort.py
  \brief CorbaPort class
  \date  $Date: 2007/09/26 $
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
import traceback
import sys

import OpenRTM
import RTC, RTC__POA

class CorbaPort(OpenRTM.PortBase):
	
	"""
	\if jp
	\class CorbaPort
	\brief RT コンポーネント CORBA service/consumer 用 Port

	CorbaPort は RT コンポーネントにおいて、ユーザ定義の CORBA オブジェクト
	サービスおよびコンシューマを提供する Port 実装である。
	<p>
	RT コンポーネントは、Port を介してユーザが定義した CORBA サービスを提供
	することができ、これを RT Service (Provider) と呼ぶ。
	また、他の RT コンポーネントのサービスを利用するための CORBA オブジェクト
	のプレースホルダを提供することができ、これを RT Service Consumer と呼ぶ。
	<p>
	CorbaPort は任意の数の Provider および Consumer を管理することができ、
	Port 同士を接続する際に対応する Provider と Consumer を適切に関連付ける
	ことができる。
	<p>
	CorbaPort は通常以下のように利用される。

	<pre>
	self._myServiceProviderPort = OpenRTM.CorbaPort("MyService")
	self._myServiceConsumerPort = OpenRTM.CorbaPort("MyService")

	self._mysvc0 = MyServiceSVC_impl() # この Port が提供する Serivce Provider
	self._mycons0 = OpenRTM.CorbaConsumer(interfaceType=_GlobalIDL.MyService) # この Port の Consumer
	# Service Provider を Port に登録
	self._myServiceProbiderPort.registerProvider("MyService0", "MyService", self._mysvc0);
	# Service Consumer を Port に登録
	self._myServiceConsumerPort.registerConsumer("MyService0", "MyService", self._cons0 );

	# connect が行われた後

	self._cons0._ptr().my_service_function() # MyService の関数をコール

	</pre>

	このように、提供したい Service Provider を registerProvider() で登録
	することにより、他のコンポーネントから利用可能にし、他方、
	利用したい Service Consumer を registerConsumer() で登録することにより
	他のコンポーネントの Service をコンポーネント内で利用可能にすることが
	できる。

	\else
	\class CorbaPort
	\brief RT Conponent CORBA service/consumer Port

	CorbaPort is an implementation of the Port of RT-Component's that provides
	user-defined CORBA Object Service and Consumer.
	<p>
	RT-Component can provide user-defined CORBA serivces, which is called
	RT-Serivce (Provider), through the Ports.
	RT-Component can also provide place-holder, which is called RT-Serivce
	Consumer, to use other RT-Component's service.
	<p>
	The CorbaPort can manage any number of Providers and Consumers, can
	associate Consumers with correspondent Providers when establishing
	connection among Ports.
	<p>
	Usually, CorbaPort is used like the following.

	<pre>
	self._myServiceProviderPort = OpenRTM.CorbaPort("MyService")
	self._myServiceConsumerPort = OpenRTM.CorbaPort("MyService")

	self._mysvc0 = MyServiceSVC_impl() # Serivce Provider that is provided by the Port
	self._mycons0 = OpenRTM.CorbaConsumer(interfaceType=_GlobalIDL.MyService) # Consumer of the Port
	# register Service Provider to the Port
	self._myServiceProbiderPort.registerProvider("MyService0", "MyService", self._mysvc0);
	# register Service Consumer to the Port
	self._myServiceConsumerPort.registerConsumer("MyService0", "MyService", self._cons0 );

	# after connect established

	self._cons0._ptr().my_service_function() # call a MyService's function
	</pre>

	Registering Service Provider by registerProvider(), it can be used from
	other RT-Components.
	Registering Service Consumer by registerConsumer(), other RT-Component's
	services can be used through the consumer object.

	\endif
	"""


	def __init__(self, name):
		"""
		\if jp
		\brief コンストラクタ
		\param name(string) Port の名前
		\else
		\brief Constructor
		\param name(string) The name of Port 
		\endif
		"""
		OpenRTM.PortBase.__init__(self, name)
		self.addProperty("port.port_type", "CorbaPort")
		self._providers = []
		self._consumers = []


	def __del__(self):
		"""
		\if jp
		\brief デストラクタ
		\else
		\brief Destructor
		\endif
		"""
		pass


	def registerProvider(self, instance_name, type_name, provider):
		"""
		\if jp
		\brief Provider を登録する
		
		この Port において提供したいサーバントをこの Port に対して登録する。
		サーバントは、引数で与えられる instance_name, type_name を、
		サーバント自身のインスタンス名およびタイプ名として、サーバントに
		関連付けられる。
		\param instance_name(string) サーバントのインスタンス名
		\param type_name(string) サーバントのタイプ名
		\param provider CORBA サーバント
		\return 既に同名の instance_name が登録されていれば false を返す。
		\else

		\brief Register provider
		
		This operation registers a servant, which is provided in this Port,
		to the Port. The servant is associated with "instance_name" and
		"type_name" as the instance name of the servant and as the type name
		of the servant.
		\param instance_name(string) instance name of servant
		\param type_name(string) type of servant
		\param provider CORBA サーバント
		\return 既に同名の instance_name が登録されていれば false を返す。
		\endif
		"""
		if not self.appendInterface(instance_name, type_name, RTC.PROVIDED):
			return False

		oid = self._default_POA().activate_object(provider)
		obj = self._default_POA().id_to_reference(oid)

		key = "port"
		key = key + "." + str(type_name) + "." + str(instance_name)

		OpenRTM.CORBA_SeqUtil.push_back(self._providers,
										OpenRTM.NVUtil.newNV(key, obj))

		return True


	def registerConsumer(self, instance_name, type_name, consumer):
		"""
		\if jp
		\brief Consumer を登録する
		
		この Port が要求するサービスのプレースホルダであるコンシューマ
		(Consumer) を登録する。
		Consumer が関連付けられるサービスのインスタンス名およびタイプ名として、
		引数に instance_name, type_name および Consumer 自身を与えることにより、
		内部でこれらが関連付けられる。
		Port 間の接続 (connect) 時 には、同一の instance_name, type_name を持つ
		サービスが他の Port から提供 (Provide) されている場合、そのサービスの
		オブジェクト参照が自動的に Consumer にセットされる。
		\param instance_name(string) Consumer が要求するサービスのインスタンス名
		\param type_name(string) Consumer が要求するサービスのタイプ名
		\param consumer CORBA サービスコンシューマ
		\return 既に同名の instance_name が登録されていれば false を返す。
		\else
		\brief Register consumer
		
		This operation registers a consumer, which requiers a service,
		to the other Port. The consumer is associated with "instance_name" and
		"type_name" as the instance name of the service and as the type name
		of the service that is required.
		\param instance_name(string) An instance name of the service required
		\param type_name(string) An type name of the service required
		\param consumer CORBA service consumer
		\return False would be returned if the same instance_name is registered
		\endif
		"""
		if not self.appendInterface(instance_name, type_name, RTC.REQUIRED):
			return False

		cons = self.Consumer(instance_name, type_name, consumer)
		self._consumers.append(cons)

		return True


	def publishInterfaces(self, connector_profile):
		"""
		\if jp
		\brief Interface 情報を公開する
		
		この Portが所有する Provider に関する情報を ConnectorProfile::properties
		に代入する。
		代入する情報は、NVListの name と value として以下のものが格納される。
		
		- port.<type_name>.<instance_name>: <CORBA::Object_ptr>
		
		ここで、
		- <type_name>: PortInterfaceProfile::type_name
		- <instance_name>: PortInterfaceProfile::instance_name
		である。
		ConnectorProfile::properties では、これらを .(ドット)表記で、
		NameValue のキーとしている。したがって、
		
		<pre>
		PortInterfaceProfile
		{
        instance_name = "PA10_0";
        type_name     = "Manipulator";
        polarity      = PROVIDED;
		}
		</pre>
		
		ならば、
		
		<pre>
		NameValue = { "port.Manipulator.PA10_0": <Object reference> }
		</pre>
		
		といった値が ConnectorProfile::properties に格納され、他のポートに対して
		伝達される。他の Port でこのインターフェースを使用する Consumer が
		存在すれば、ConnectorProfile からこのキーからオブジェクトリファレンスを
		取得し何らかの形で使用される。
		\else
		\brief Publish interface information
		\endif
		"""
		OpenRTM.CORBA_SeqUtil.push_back_list(connector_profile.properties,
											 self._providers)
		return RTC.RTC_OK


	def subscribeInterfaces(self, connector_profile):
		"""
		\if jp

		\brief Interface に接続する

		この Portが所有する Consumer に適合する Provider に関する情報を
		ConnectorProfile::properties から抽出し Consumer にオブジェクト参照
		をセットする。

		今、Consumer が
		<pre>
			PortInterfaceProfile
			{
				instance_name = "PA10_0";
				type_name     = "Manipulator";
				polarity      = REQUIRED;
			}
		</pre>
		として登録されていれば、他の Port の
		<pre>
			PortInterfaceProfile
			{
				instance_name = "PA10_0";
				type_name     = "Manipulator";
				polarity      = PROVIDED;
			}
		</pre> 
		として登録されている Serivce Provider のオブジェクト参照を探し、
		Consumer にセットする。
		実際には、ConnectorProfile::properties に
		<pre>
		NameValue = { "port.Manipulator.PA10_0": <Object reference> }
		</pre>
		として登録されている NameValue を探し、そのオブジェクト参照を
		Consumer にセットする。
		\param connector_profile(RTC.ConnectorProfile)

		\else

		\brief Subscribe interfaces
		\param connector_profile(RTC.ConnectorProfile)
		\endif
		"""
		nv = connector_profile.properties
		OpenRTM.CORBA_SeqUtil.for_each(nv, self.subscribe(self._consumers))
		return RTC.RTC_OK


 	def unsubscribeInterfaces(self, connector_profile):
		"""
		\if jp
		\brief Interface への接続を解除する
		
		与えられた ConnectorProfile に関連する Consumer にセットされた
		すべての Object を解放し接続を解除する。
		\param connector_profile(RTC.ConnectorProfile)
		\else
		\brief Unsubscribe interfaces
		\param connector_profile(RTC.ConnectorProfile)
		\endif
		"""
		nv = connector_profile.properties

		OpenRTM.CORBA_SeqUtil.for_each(nv, self.unsubscribe(self._consumers))


 	class Consumer:
		
		"""
		\if jp
		\brief Consumer の情報を格納する構造体
		\param _instance_name(string)
		\param _type_name(string)
		\param _cons(OpenRTM.CorbaConsumerBase)
		\param _consumer(Consumer)
		\else
		\brief Consumer inforamtion struct
		\param _instance_name(string)
		\param _type_name(string)
		\param _cons(OpenRTM.CorbaConsumerBase)
		\param _consumer(Consumer)
		\endif
		"""
		def __init__(self, _instance_name, _type_name, _cons, _consumer=None):
			if _consumer:
				self.name = _consumer.name
				self.consumer = _consumer.consumer
				return
			
			self.name = "port."+str(_type_name)+"."+str(_instance_name)
			self.consumer = _cons


	class subscribe:
		
		"""
		\if jp
		\brief ConnectorProfile と Consuemr の比較をしオブジェクト参照を
		セットするための Functor
		\param cons(Consumerのリスト)
		\else
		\brief Subscription mutching functor for Consumer
		\param cons(list of Consumer)
		\endif
		"""
		def __init__(self, cons):
			self._cons = cons
			self._len  = len(cons)

		def __call__(self, nv):
			for i in range(self._len):
				name_ = nv.name
				if self._cons[i].name == name_:
					try:
						obj = any.from_any(nv.value, keep_structs=True)
						self._cons[i].consumer.setObject(obj)
					except:
						traceback.print_exception(*sis.exc_info())


	class unsubscribe:
		
		"""
		\if jp
		\brief Consumer のオブジェクトを解放するための Functor
		\param cons(Consumerのリスト)
		\else
		\brief Unsubscription functor for Consumer
		\param cons(list of Consumer)
		\endif
		"""
		def __init__(self, cons):
			self._cons = cons
			self._len  = len(cons)

		def __call__(self, nv):
			for i in range(self._len):
				name_ = nv.name
				if self._cons[i].name == name_:
					self._cons[i].consumer.releaseObject()
