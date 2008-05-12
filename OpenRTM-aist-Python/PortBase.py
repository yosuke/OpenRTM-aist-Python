#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
  \file PortBase.py
  \brief RTC's Port base class
  \date $Date: 2007/09/18 $
  \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
 
  Copyright (C) 2006
      Task-intelligence Research Group,
      Intelligent Systems Research Institute,
      National Institute of
          Advanced Industrial Science and Technology (AIST), Japan
      All rights reserved.
"""


import threading

import OpenRTM
import RTC, RTC__POA


class ScopedLock:
	def __init__(self, mutex):
		self.mutex = mutex
		self.mutex.acquire()

	def __del__(self):
		self.mutex.release()



class PortBase(RTC__POA.Port):
	"""
	\if jp
	\class PortBase
	\brief Port の基底クラス

	RTC::Port の基底となるクラス。
	RTC::Port はほぼ UML Port の概念を継承しており、ほぼ同等のものとみなす
	ことができる。RT コンポーネントのコンセプトにおいては、
	Port はコンポーネントに付属し、コンポーネントが他のコンポーネントと相互作用
	を行う接点であり、通常幾つかのインターフェースと関連付けられる。
	コンポーネントは Port を通して外部に対しインターフェースを提供または要求
	することができ、Portはその接続を管理する役割を担う。
	<p>
	Port の具象クラスは、通常 RT コンポーネントインスタンス生成時に同時に
	生成され、提供・要求インターフェースを登録した後、RT コンポーネントに
	登録され、外部からアクセス可能な Port として機能することを想定している。
	<p>
	RTC::Port は CORBA インターフェースとして以下のオペレーションを提供する。

	- get_port_profile()
	- get_connector_profiles()
	- get_connector_profile()
	- connect()
	- notify_connect()
	- disconnect()
	- notify_disconnect()
	- disconnect_all()

	このクラスでは、これらのオペレーションの実装を提供する。
	<p>
	これらのオペレーションのうち、get_port_profile(), get_connector_profiles(),
	get_connector_profile(), connect(), disconnect(), disconnect_all() は、
	サブクラスにおいて特に振る舞いを変更する必要がないため、オーバーライド
	することは推奨されない。
	<p>
	notify_connect(), notify_disconnect() については、サブクラスが提供・要求
	するインターフェースの種類に応じて、振る舞いを変更する必要が生ずる
	かもしれないが、これらを直接オーバーライドすることは推奨されず、
	後述の notify_connect(), notify_disconnect() の項においても述べられる通り
	これらの関数に関連した protected 関数をオーバーライドすることにより
	振る舞いを変更することが推奨される。

	\else


	\endif
	"""


	def __init__(self, name=None):
		"""
		\if jp
		\brief コンストラクタ

		PortBase のコンストラクタは Port 名 name を引数に取り初期化を行う
		と同時に、自分自身を CORBA Object として活性化し、自身の PortProfile
		の port_ref に自身のオブジェクトリファレンスを格納する。

		\param name(string) Port の名前

		\else

		\brief Constructor

		The constructor of the ProtBase class is given the name of this Port
		and initialized. At the same time, the PortBase activates itself
		as CORBA object and stores its object reference to the PortProfile's 
		port_ref member.

		\param name(string) The name of Port 

		\endif
		"""
		self._profile = RTC.PortProfile("", [], RTC.Port._nil, [], RTC.RTObject._nil,[])
		
		if name == None:
			self._profile.name = ""
		else:
			self._profile.name = name
			
		self._objref = self._this()
		self._profile.port_ref = self._objref
		self._profile.owner = RTC.RTObject._nil
		self._profile_mutex = threading.RLock()


	def __del__(self):
		"""
		\if jp
		\brief デストラクタ
		\else
		\brief Destructor
		\endif
		"""
		pass


	def get_port_profile(self):
		"""
		\if jp

		\brief [CORBA interface] PortProfileを取得する

		Portが保持するPortProfileを返す。
		PortProfile 構造体は以下のメンバーを持つ。

		- name              [string 型] Port の名前。
		- interfaces        [PortInterfaceProfileList 型] Port が保持する
			PortInterfaceProfile のシーケンス
		- port_ref          [Port Object 型] Port 自身のオブジェクトリファレンス
		- connector_profile [ConnectorProfileList 型] Port が現在保持する
			ConnectorProfile のシーケンス
		- owner             [RTObject Object 型] この Port を所有する
			RTObjectのリファレンス
		- properties        [NVList 型] その他のプロパティ。

		\return この Port の PortProfile

		\else

		\brief [CORBA interface] Get the PortProfile of the Port

		This operation returns the PortProfile of the Port.
		PortProfile struct has the following members,

		- name              [string ] The name of the Port.
		- interfaces        [PortInterfaceProfileList 型] The sequence of 
			PortInterfaceProfile owned by the Port
		- port_ref          [Port Object] The object reference of the Port.
		- connector_profile [ConnectorProfileList 型] The sequence of 
			ConnectorProfile owned by the Port.
		- owner             [RTObject Object] The object reference of 
			RTObject that is owner of the Port.
		- properties        [NVList] The other properties.

		\return the PortProfile of the Port

		\endif
		"""
		guard = ScopedLock(self._profile_mutex)
		prof = RTC.PortProfile(self._profile.name,
							   self._profile.interfaces,
							   self._profile.port_ref,
							   self._profile.connector_profiles,
							   self._profile.owner,
							   self._profile.properties)

		return prof


	def get_connector_profiles(self):
		"""
		\if jp

		\brief [CORBA interface] ConnectorProfileListを取得する

		Portが保持する ConnectorProfile の sequence を返す。
		ConnectorProfile は Port 間の接続プロファイル情報を保持する構造体であり、
		接続時にPort間で情報交換を行い、関連するすべての Port で同一の値が
		保持される。
		ConnectorProfile は以下のメンバーを保持している。

		- name         [string 型] このコネクタの名前。
		- connector_id [string 型] ユニークなID
		- ports        [Port sequnce] このコネクタに関連する Port のオブジェクト
			リファレンスのシーケンス。
		- properties   [NVList 型] その他のプロパティ。

		\return この Port の ConnectorProfile

		\else

		\brief [CORBA interface] Get the ConnectorProfileList of the Port

		This operation returns a list of the ConnectorProfiles of the Port.
		ConnectorProfile includes the connection information that describes 
		relation between (among) Ports, and Ports exchange the ConnectionProfile
		on connection process and hold the same information in each Port.
		ConnectionProfile has the following members,

		- name         [string] The name of the connection.
		- connector_id [string] Unique identifier.
		- ports        [Port sequnce] The sequence of Port's object reference
			that are related the connection.
		- properties   [NVList] The other properties.

		\return the ConnectorProfileList of the Port

		\endif
		"""
		guard = ScopedLock(self._profile_mutex)
		return self._profile.connector_profiles


	def get_connector_profile(self, connector_id):
		"""
		\if jp

		\brief [CORBA interface] ConnectorProfile を取得する

		connector_id で指定された ConnectorProfile を返す。

		\param connector_id(string) ConnectorProfile の ID
		\return connector_id を持つ ConnectorProfile

		\else

		\brief [CORBA interface] Get the ConnectorProfile

		This operation returns the ConnectorProfiles specified connector_id.

		\param connector_id(string) ID of the ConnectorProfile
		\return the ConnectorProfile identified by the connector_id

		\endif
		"""
		guard = ScopedLock(self._profile_mutex)
		index = OpenRTM.CORBA_SeqUtil.find(self._profile.connector_profiles,
										   self.find_conn_id(connector_id))
		if index < 0:
			conn_prof = RTC.ConnectorProfile("","",[],[])
			return conn_prof

		conn_prof = RTC.ConnectorProfile(self._profile.connector_profiles[index].name,
										 self._profile.connector_profiles[index].connector_id,
										 self._profile.connector_profiles[index].ports,
										 self._profile.connector_profiles[index].properties)
		return conn_prof


	def connect(self, connector_profile):
		"""
		\if jp

		\brief [CORBA interface] Port の接続を行う

		与えられた ConnectoionProfile にしたがって、Port間の接続を確立する。
		アプリケーションプログラム側は、幾つかのコンポーネントが持つ複数の
		Port を接続したい場合、適切な値をセットした ConnectorProfile を
		connect() の引数として与えてコールすることにより、関連する Port の
		接続を確立する。

		connect() に与える ConnectorProfile のメンバーのうち、name, ports, 
		(properties) メンバーに対してデータをセットしなければならない。

		\param connector_profile(RTC.ConnectorProfile) ConnectorProfile
		\return ReturnCode_t オペレーションのリターンコード

		\else

		\brief [CORBA interface] Connect the Port

		This operation establishes connection according to the given 
		ConnectionProfile inforamtion. 
		Application programs, which is going to establish the connection 
		among Ports owned by RT-Components, have to set valid values to the 
		ConnectorProfile and give it to the argument of connect() operation.

		name, ports, (properties) members of ConnectorProfile should be set
		valid values before giving to the argument of connect() operation.

		\param connector_profile(RTC.ConnectorProfile) The ConnectorProfile.
		\return ReturnCode_t The return code of this operation.

		\endif
		"""
		if self.isEmptyId(connector_profile):
			self.setUUID(connector_profile)
			assert(not self.isExistingConnId(connector_profile.connector_id))

		try:
			retval,connector_profile = connector_profile.ports[0].notify_connect(connector_profile)
			return (retval, connector_profile)
			#return connector_profile.ports[0].notify_connect(connector_profile)
		except:
			return (RTC.BAD_PARAMETER, connector_profile)

		return (RTC.RTC_ERROR, connector_profile)


	def notify_connect(self, connector_profile):
		"""
		\if jp

		\brief [CORBA interface] Port の接続通知を行う

		このオペレーションは、Port間の接続が行われる際に、Port間で内部的に
		呼ばれるオペレーションである。

		\param connector_profile(RTC.ConnectorProfile) ConnectorProfile
		\return ReturnCode_t オペレーションのリターンコード

		\else

		\brief [CORBA interface] Notify the Ports connection

		This operation is invoked between Ports internally when the connection
		is established.

		\param connector_profile(RTC.ConnectorProfile) The ConnectorProfile.
		\return ReturnCode_t The return code of this operation.

		\endif
		"""
		# publish owned interface information to the ConnectorProfile
		retval = self.publishInterfaces(connector_profile)

		if retval != RTC.RTC_OK:
			return (retval, connector_profile)

		# call notify_connect() of the next Port
		retval, connector_profile = self.connectNext(connector_profile)
		if retval != RTC.RTC_OK:
			return (retval, connector_profile)

		# subscribe interface from the ConnectorProfile's information
		retval = self.subscribeInterfaces(connector_profile)
		if retval != RTC.RTC_OK:
			#cleanup this connection for downstream ports
			self.notify_disconnect(connector_profile.connector_id)
			return (retval, connector_profile)

		# update ConnectorProfile
		index = self.findConnProfileIndex(connector_profile.connector_id)
		if index < 0:
			OpenRTM.CORBA_SeqUtil.push_back(self._profile.connector_profiles,
											connector_profile)
		else:
			self._profile.connector_profiles[index] = connector_profile

		return (retval, connector_profile)


	def disconnect(self, connector_id):
		"""
		\if jp

		\brief [CORBA interface] Port の接続を解除する

		このオペレーションは接続確立時に接続に対して与えられる connector_id に
		対応するピア Port との接続を解除する。

		\param connector_id(string) ConnectorProfile の ID
		\return ReturnCode_t オペレーションのリターンコード

		\else

		\brief [CORBA interface] Connect the Port

		This operation destroys connection between this port and the peer port
		according to given id that is given when the connection established.

		\param connector_id(string) The ID of the ConnectorProfile.
		\return ReturnCode_t The return code of this operation.

		\endif
		"""
		# find connector_profile
		if not self.isExistingConnId(connector_id):
			return RTC.BAD_PARAMETER

		index = self.findConnProfileIndex(connector_id)
		prof = RTC.ConnectorProfile(self._profile.connector_profiles[index].name,
									self._profile.connector_profiles[index].connector_id,
									self._profile.connector_profiles[index].ports,
									self._profile.connector_profiles[index].properties)
		return prof.ports[0].notify_disconnect(connector_id)


	def notify_disconnect(self, connector_id):
		"""
		\if jp

		\brief [CORBA interface] Port の接続解除通知を行う

		このオペレーションは、Port間の接続解除が行われる際に、Port間で内部的に
		呼ばれるオペレーションである。

		\param connector_id(string) ConnectorProfile の ID
		\return ReturnCode_t オペレーションのリターンコード

		\else

		\brief [CORBA interface] Notify the Ports disconnection

		This operation is invoked between Ports internally when the connection
		is destroied.

		\param connector_id(string) The ID of the ConnectorProfile.
		\return ReturnCode_t The return code of this operation.

		\endif
		"""

		# The Port of which the reference is stored in the beginning of
		# connectorProfile's PortList is master Port.
		# The master Port has the responsibility of disconnecting all Ports.
		# The slave Ports have only responsibility of deleting its own
		# ConnectorProfile.

		# find connector_profile
		if not self.isExistingConnId(connector_id):
			return RTC.BAD_PARAMETER

		index = self.findConnProfileIndex(connector_id)
		prof = RTC.ConnectorProfile(self._profile.connector_profiles[index].name,
									self._profile.connector_profiles[index].connector_id,
									self._profile.connector_profiles[index].ports,
									self._profile.connector_profiles[index].properties)

		self.unsubscribeInterfaces(prof)
		retval = self.disconnectNext(prof)

		OpenRTM.CORBA_SeqUtil.erase(self._profile.connector_profiles, index)
    
		return retval


	def disconnect_all(self):
		"""
		\if jp

		\brief [CORBA interface] Port の全接続を解除する

		このオペレーションはこの Port に関連した全ての接続を解除する。

		\return ReturnCode_t オペレーションのリターンコード

		\else

		\brief [CORBA interface] Connect the Port

		This operation destroys all connection channels owned by the Port.

		\return ReturnCode_t The return code of this operation.

		\endif
		"""
		guard = ScopedLock(self._profile_mutex)
		# disconnect all connections
		# Call disconnect() for each ConnectorProfile.
		f = OpenRTM.CORBA_SeqUtil.for_each(self._profile.connector_profiles,
										   self.disconnect_all_func(self))
		return f.return_code



	#============================================================
	# Local operations
	#============================================================

	def setName(self, name):
		"""
		\if jp
		\brief Port の名前を設定する

		Port の名前を設定する。この名前は Port が保持する PortProfile.name
		に反映される。

		\param name(string) Port の名前

		\else
		\brief Set the name of this Port

		This operation sets the name of this Port. The given Port's name is
		applied to Port's PortProfile.name.

		\param name(string) The name of this Port.

		\endif
		"""
		guard = ScopedLock(self._profile_mutex)
		self._profile.name = name


	def getProfile(self):
		"""
		\if jp
		\brief PortProfileを取得する

		Portが保持する PortProfile の const 参照を返す。

		\return この Port の PortProfile

		\else
		\brief Get the PortProfile of the Port

		This operation returns const reference of the PortProfile.

		\return the PortProfile of the Port

		\endif
		"""
		guard = ScopedLock(self._profile_mutex)
		return self._profile


	def setPortRef(self, port_ref):
		"""
		\if jp

		\brief Port のオブジェクト参照を設定する

		このオペレーションは Port の PortProfile にこの Port 自身の
		オブジェクト参照を設定する。

		\param port_ref(RTC.Port) この Port のオブジェクト参照

		\else

		\brief Set the object reference of this Port

		This operation sets the object reference itself
		to the Port's PortProfile.

		\param port_ref(RTC.Port) The object reference of this Port.

		\endif
		"""
		guard = ScopedLock(self._profile_mutex)
		self._profile.port_ref = port_ref


	def getPortRef(self):
		"""
		\if jp

		\brief Port のオブジェクト参照を取得する

		このオペレーションは Port の PortProfile が保持している
		この Port 自身のオブジェクト参照を取得する。

		\return この Port のオブジェクト参照

		\else

		\brief Get the object reference of this Port

		This operation returns the object reference
		that is stored in the Port's PortProfile.

		\return The object reference of this Port.

		\endif
		"""
		guard = ScopedLock(self._profile_mutex)
		return self._profile.port_ref


	def setOwner(self, owner):
		"""
		\if jp

		\brief Port の owner の RTObject を指定する

		このオペレーションは Port の PortProfile.owner を設定する。

		\param owner(RTC.RTObject) この Port を所有する RTObject の参照

		\else

		\brief Set the owner RTObject of the Port

		This operation sets the owner RTObject of this Port.

		\param owner(RTC.RTObject) The owner RTObject's reference of this Port

		\endif
		"""
		guard = ScopedLock(self._profile_mutex)
		self._profile.owner = owner


	"""
      \if jp
     
      \brief Interface 情報を公開する
     
      このオペレーションは、notify_connect() 処理シーケンスの始めにコール
      される純粋仮想関数である。
      notify_connect() では、
     
      - publishInterfaces()
      - connectNext()
      - subscribeInterfaces()
      - updateConnectorProfile()
     
      の順に protected 関数がコールされ接続処理が行われる。
      <br>
      具象 Port ではこのオペレーションをオーバーライドし、引数として
      与えられた ConnectorProfile に従い処理を行い、パラメータが不適切
      であれば、RteurnCode_t 型のエラーコードを返す。
      通常 publishInterafaces() 内においては、この Port に属する
      インターフェースに関する情報を ConnectorProfile に対して適切に設定し
      他の Port に通知しなければならない。
      <br>
      また、この関数がコールされる段階では、他の Port の Interface に関する
      情報はすべて含まれていないので、他の Port の Interface を取得する処理
      は subscribeInterfaces() 内で行われるべきである。
      <br>
      このオペレーションは、新規の connector_id に対しては接続の生成、
      既存の connector_id に対しては更新が適切に行われる必要がある。
     
      \param connector_profile 接続に関するプロファイル情報
      \return ReturnCode_t 型のリターンコード
     
      \else
     
      \brief Publish interface information
     
      This operation is pure virutal method that would be called at the
      beginning of the notify_connect() process sequence.
      In the notify_connect(), the following methods would be called in order.
     
      - publishInterfaces()
      - connectNext()
      - subscribeInterfaces()
      - updateConnectorProfile() 
     
      In the concrete Port, this method should be overridden. This method
      processes the given ConnectorProfile argument and if the given parameter
      is invalid, it would return error code of ReturnCode_t.
      Usually, publishInterfaces() method should set interfaces information
      owned by this Port, and publish it to the other Ports.
      <br>
      When this method is called, other Ports' interfaces information may not
      be completed. Therefore, the process to obtain other Port's interfaces
      information should be done in the subscribeInterfaces() method.
      <br>
      This operation should create the new connection for the new
      connector_id, and should update the connection for the existing
      connection_id.
     
      \param connector_profile The connection profile information
      \return The return code of ReturnCode_t type.
     
      \endif

	def publishInterfaces(self, connector_profile):
		pass
	"""    


	def connectNext(self, connector_profile):
		"""
		\if jp

		\brief 次の Port に対して notify_connect() をコールする

		ConnectorProfile の port_ref 内に格納されている Port のオブジェクト
		リファレンスのシーケンスの中から、自身の Port の次の Port に対して
		notify_connect() をコールする。

		\param connector_profile(RTC.ConnectorProfile) 接続に関するプロファイル情報
		\return ReturnCode_t 型のリターンコード

		\else

		\brief Call notify_connect() of the next Port

		This operation calls the notify_connect() of the next Port's 
		that stored in ConnectorProfile's port_ref sequence.

		\param connector_profile(RTC.ConnectorProfile) The connection profile information
		\return The return code of ReturnCode_t type.

		\endif
		"""
		index = OpenRTM.CORBA_SeqUtil.find(connector_profile.ports,
										   self.find_port_ref(self._profile.port_ref))
		if index < 0:
			return RTC.BAD_PARAMETER, connector_profile

		index += 1
		if index < len(connector_profile.ports):
			p = connector_profile.ports[index]
			return p.notify_connect(connector_profile)

		return RTC.RTC_OK, connector_profile


	def disconnectNext(self, connector_profile):
		"""
		\if jp

		\brief 次の Port に対して notify_disconnect() をコールする

		ConnectorProfile の port_ref 内に格納されている Port のオブジェクト
		リファレンスのシーケンスの中から、自身の Port の次の Port に対して
		notify_disconnect() をコールする。

		\param connector_profile(RTC.ConnectorProfile) 接続に関するプロファイル情報
		\return ReturnCode_t 型のリターンコード

		\else

		\brief Call notify_disconnect() of the next Port

		This operation calls the notify_disconnect() of the next Port's 
		that stored in ConnectorProfile's port_ref sequence.

		\param connector_profile(RTC.ConnectorProfile) The connection profile information
		\return The return code of ReturnCode_t type.

		\endif
		"""
		index = OpenRTM.CORBA_SeqUtil.find(connector_profile.ports,
										   self.find_port_ref(self._profile.port_ref))
		if index < 0:
			return RTC.BAD_PARAMETER

		index += 1
		
		if index < len(connector_profile.ports):
			p = connector_profile.ports[index]
			return p.notify_disconnect(connector_profile.connector_id)

		self.unsubscribeInterfaces(connector_profile)
		return RTC.RTC_OK


	"""
      \if jp
     
      \brief Interface 情報を取得する
     
      このオペレーションは、notify_connect() 処理シーケンスの中間にコール
      される純粋仮想関数である。
      notify_connect() では、
     
      - publishInterfaces()
      - connectNext()
      - subscribeInterfaces()
      - updateConnectorProfile()
     
      の順に protected 関数がコールされ接続処理が行われる。
      <br>
      具象 Port ではこのオペレーションをオーバーライドし、引数として
      与えられた ConnectorProfile に従い処理を行い、パラメータが不適切
      であれば、RteurnCode_t 型のエラーコードを返す。
      引数 ConnectorProfile には他の Port の Interface に関する情報が
      全て含まれている。
      通常 subscribeInterafaces() 内においては、この Port が使用する
      Interface に関する情報を取得し、要求側のインターフェースに対して
      情報を設定しなければならない。
      <br>
      このオペレーションは、新規の connector_id に対しては接続の生成、
      既存の connector_id に対しては更新が適切に行われる必要がある。
     
      \param connector_profile 接続に関するプロファイル情報
      \return ReturnCode_t 型のリターンコード
     
      \else
     
      \brief Publish interface information
     
      This operation is pure virutal method that would be called at the
      mid-flow of the notify_connect() process sequence.
      In the notify_connect(), the following methods would be called in order.
     
      - publishInterfaces()
      - connectNext()
      - subscribeInterfaces()
      - updateConnectorProfile()
     
      In the concrete Port, this method should be overridden. This method
      processes the given ConnectorProfile argument and if the given parameter
      is invalid, it would return error code of ReturnCode_t.
      The given argument ConnectorProfile includes all the interfaces
      information in it.
      Usually, subscribeInterafaces() method obtains information of interfaces
      from ConnectorProfile, and should set it to the interfaces that require
      them.
      <br>
      This operation should create the new connection for the new
      connector_id, and should update the connection for the existing
      connection_id.
     
      \param connector_profile The connection profile information
      \return The return code of ReturnCode_t type.
     
      \endif

	def subscribeInterfaces(self, connector_profile):
		pass
	"""    
    
	"""
      \if jp
     
      \brief Interface の接続を解除する
     
      このオペレーションは、notify_disconnect() 処理シーケンスの終わりにコール
      される純粋仮想関数である。
      notify_disconnect() では、
      - disconnectNext()
      - unsubscribeInterfaces()
      - eraseConnectorProfile()
      の順に protected 関数がコールされ接続解除処理が行われる。
      <br>
      具象 Port ではこのオペレーションをオーバーライドし、引数として
      与えられた ConnectorProfile に従い接続解除処理を行う。
     
      \param connector_profile 接続に関するプロファイル情報
     
      \else
     
      \brief Disconnect interface connection
     
      This operation is pure virutal method that would be called at the
      end of the notify_disconnect() process sequence.
      In the notify_disconnect(), the following methods would be called.
      - disconnectNext()
      - unsubscribeInterfaces()
      - eraseConnectorProfile() 
       <br>
      In the concrete Port, this method should be overridden. This method
      processes the given ConnectorProfile argument and disconnect interface
      connection.
     
      \param connector_profile The connection profile information
     
      \endif

	def unsubscribeInterfaces(self, connector_profile):
		pass
	"""


	def isEmptyId(self, connector_profile):
		"""
		\if jp
		\brief ConnectorProfile の connector_id フィールドが空かどうか判定
		\param connector_profile(RTC.ConnectorProfile)
		\return 引数で与えられた ConnectorProfile の connector_id が空であれば、
			true、そうでなければ false を返す。

		\else
		\brief Whether connector_id of ConnectorProfile is empty
		\param connector_profile(RTC.ConnectorProfile)
		\return If the given ConnectorProfile's connector_id is empty string,
			it returns true.
		\endif
		"""
		return connector_profile.connector_id == ""


	def getUUID(self):
		"""
		\if jp

		\brief UUIDを生成する

		このオペレーションは UUID を生成する。

		\return uuid

		\else

		\brief Get the UUID

		This operation generates UUID.

		\return uuid

		\endif
		"""
		return str(OpenRTM.uuid1())


	def setUUID(self, connector_profile):
		"""
		\if jp

		\brief UUIDを生成し ConnectorProfile にセットする

		このオペレーションは UUID を生成し、ConnectorProfile にセットする。

		\param connector_profile(RTC.ConnectorProfile) connector_id をセットする ConnectorProfile

		\else

		\brief Create and set the UUID to the ConnectorProfile

		This operation generates and set UUID to the ConnectorProfile.

		\param connector_profile(RTC.ConnectorProfile) ConnectorProfile to be set connector_id

		\endif
		"""
		connector_profile.connector_id = self.getUUID()
		assert(connector_profile.connector_id != "")


	def isExistingConnId(self, id_):
		"""
		\if jp

		\brief id が既存の ConnectorProfile のものかどうか判定する

		このオペレーションは与えられた ID が既存の ConnectorProfile のリスト中に
		存在するかどうか判定する。

		\param id_(string) 判定する connector_id

		\else

		\brief Whether the given id exists in stored ConnectorProfiles

		This operation returns boolean whether the given id exists in 
		the Port's ConnectorProfiles.

		\param id_(string) connector_id to be find in Port's ConnectorProfiles

		\endif
		"""
		return OpenRTM.CORBA_SeqUtil.find(self._profile.connector_profiles,
										  self.find_conn_id(id_)) >= 0


	def findConnProfile(self, id_):
		"""
		\if jp

		\brief id を持つ ConnectorProfile を探す

		このオペレーションは与えられた ID を持つ ConnectorProfile を Port が
		もつ ConnectorProfile のリスト中から探す。
		もし、同一の id を持つ ConnectorProfile がなければ、空の ConnectorProfile
		が返される。

		\param id_(string) 検索する connector_id
		\return connector_id を持つ ConnectorProfile

		\else

		\brief Find ConnectorProfile with id

		This operation returns ConnectorProfile with the given id from Port's
		ConnectorProfiles' list.
		If the ConnectorProfile with connector id that is identical with the
		given id does not exist, empty ConnectorProfile is returned.

		\param id_(string) the connector_id to be searched in Port's ConnectorProfiles
		\return CoonectorProfile with connector_id

		\endif
		"""
		index = OpenRTM.CORBA_SeqUtil.find(self._profile.connector_profiles,
										   self.find_conn_id(id_))
		if index < 0 or index >= len(self._profile.connector_profiles):
			return RTC.ConnectorProfile("","",[],[])

		return self._profile.connector_profiles[index]


	def findConnProfileIndex(self, id_):
		"""
		\if jp

		\brief id を持つ ConnectorProfile を探す

		このオペレーションは与えられた ID を持つ ConnectorProfile を Port が
		もつ ConnectorProfile のリスト中から探しインデックスを返す。
		もし、同一の id を持つ ConnectorProfile がなければ、-1 を返す。

		\param id_(string) 検索する connector_id
		\return Port の ConnectorProfile リストのインデックス

		\else

		\brief Find ConnectorProfile with id

		This operation returns ConnectorProfile with the given id from Port's
		ConnectorProfiles' list.
		If the ConnectorProfile with connector id that is identical with the
		given id does not exist, empty ConnectorProfile is returned.

		\param id_(string) the connector_id to be searched in Port's ConnectorProfiles
		\return The index of ConnectorProfile of the Port

		\endif
		"""
		return OpenRTM.CORBA_SeqUtil.find(self._profile.connector_profiles,
										  self.find_conn_id(id_))


	def updateConnectorProfile(self, connector_profile):
		"""
		\if jp

		\brief ConnectorProfile の追加もしくは更新

		このオペレーションは与えられた ConnectorProfile をPort に追加もしくは
		更新保存する。
		与えられた ConnectorProfile の connector_id と同じ ID を持つ
		ConnectorProfile がリストになければ、リストに追加し、
		同じ ID が存在すれば ConnectorProfile を上書き保存する。

		\param coonector_profile(RTC.ConnectorProfile) 追加もしくは更新する ConnectorProfile

		\else

		\brief Append or update the ConnectorProfile list

		This operation appends or updates ConnectorProfile of the Port
		by the given ConnectorProfile.
		If the connector_id of the given ConnectorProfile does not exist
		in the Port's ConnectorProfile list, the given ConnectorProfile would be
		append to the list. If the same id exists, the list would be updated.

		\param connector_profile(RTC.ConnectorProfile) the ConnectorProfile to be appended or updated

		\endif
		"""
		index = OpenRTM.CORBA_SeqUtil.find(self._profile.connector_profiles,
										   self.find_conn_id(connector_profile.connector_id))

		if index < 0:
			OpenRTM.CORBA_SeqUtil.push_back(self._profile.connector_profiles,
											self.connector_profile)
		else:
			self._profile.connector_profiles[index] = connector_profile


	def eraseConnectorProfile(self, id_):
		"""
		\if jp

		\brief ConnectorProfile を削除する

		このオペレーションは Port の PortProfile が保持している
		ConnectorProfileList のうち与えられた id を持つ ConnectorProfile
		を削除する。

		\param id_(string) 削除する ConnectorProfile の id

		\else

		\brief Delete the ConnectorProfile

		This operation deletes a ConnectorProfile specified by id from
		ConnectorProfileList owned by PortProfile of this Port.

		\param id_(string) The id of the ConnectorProfile to be deleted.

		\endif
		"""
		guard = ScopedLock(self._profile_mutex)

		index = OpenRTM.CORBA_SeqUtil.find(self._profile.connector_profiles,
										   self.find_conn_id(id_))

		if index < 0:
			return False

		OpenRTM.CORBA_SeqUtil.erase(self._profile.connector_profiles, index)

		return True


	def appendInterface(self, instance_name, type_name, pol):
		"""
		\if jp

		\brief PortInterfaceProfile に インターフェースを登録する

		このオペレーションは Port が持つ PortProfile の、PortInterfaceProfile
		にインターフェースの情報を追加する。
		この情報は、get_port_profile() によって得られる PortProfile のうち
		PortInterfaceProfile の値を変更するのみであり、実際にインターフェースを
		提供したり要求したりする場合には、サブクラスで、publishInterface(),
		subscribeInterface() 等の関数を適切にオーバーライドしインターフェースの
		提供、要求処理を行わなければならない。

		インターフェース(のインスタンス)名は Port 内で一意でなければならない。
		同名のインターフェースがすでに登録されている場合、この関数は false を
		返す。

		\param name(string) インターフェースのインスタンスの名前
		\param type_name(string) インターフェースの型の名前
		\param pol(RTC.PortInterfacePolarity) インターフェースの属性 (RTC::PROVIDED もしくは RTC:REQUIRED)
		\return 同名のインターフェースが既に登録されていれば false を返す。

		\else

		\brief Append an interface to the PortInterfaceProfile

		This operation appends interface information to the PortInterfaceProfile
		that is owned by the Port.
		The given interfaces information only updates PortInterfaceProfile of
		PortProfile that is obtained through get_port_profile().
		In order to provide and require interfaces, proper functions (for
		example publishInterface(), subscribeInterface() and so on) should be
		overridden in subclasses, and these functions provide concrete interface
		connection and disconnection functionality.

		The interface (instance) name have to be unique in the Port.
		If the given interface name is identical with stored interface name,
		this function returns false.

		\param name(string) The instance name of the interface.
		\param type_name(string) The type name of the interface.
		\param pol(RTC.PortInterfacePolarity) The interface's polarity (RTC::PROVIDED or RTC:REQUIRED)
		\return false would be returned if the same name is already registered.

		\endif
		"""
		index = OpenRTM.CORBA_SeqUtil.find(self._profile.interfaces,
										   self.find_interface(instance_name, pol))

		if index >= 0:
			return False

		# setup PortInterfaceProfile
		prof = RTC.PortInterfaceProfile(instance_name, type_name, pol)
		OpenRTM.CORBA_SeqUtil.push_back(self._profile.interfaces, prof)

		return True


	def deleteInterface(self, name, pol):
		"""
		\if jp

		\brief PortInterfaceProfile からインターフェース登録を削除する

		このオペレーションは Port が持つ PortProfile の、PortInterfaceProfile
		からインターフェースの情報を削除する。

		\param name(string) インターフェースのインスタンスの名前
		\param pol(RTC.PortInterfacePolarity) インターフェースの属性 (RTC::PROVIDED もしくは RTC:REQUIRED)
		\return インターフェースが登録されていなければ false を返す。

		\else

		\brief Delete an interface from the PortInterfaceProfile

		This operation deletes interface information from the
		PortInterfaceProfile that is owned by the Port.

		\param name(string) The instance name of the interface.
		\param pol(RTC.PortInterfacePolarity) The interface's polarity (RTC::PROVIDED or RTC:REQUIRED)
		\return false would be returned if the given name is not registered.

		\endif
		"""
		index = OpenRTM.CORBA_SeqUtil.find(self._profile.interfaces,
										   self.find_interface(name, pol))

		if index < 0:
			return False

		OpenRTM.CORBA_SeqUtil.erase(self._profile.interfaces, index)
		return True


	def addProperty(self, key, value):
		"""
		\if jp

		\brief PortProfile の properties に NameValue 値を追加する

		\param key(string) properties の name
		\param value(data) properties の value

		\else

		\brief Add NameValue data to PortProfile's properties

		\param key(string) The name of properties
		\param value(data) The value of properties

		\endif
		"""
		OpenRTM.CORBA_SeqUtil.push_back(self._profile.properties,
										OpenRTM.NVUtil.newNV(key, value))


	#============================================================
	# Functor
	#============================================================

	class if_name:
		"""
		\if jp
		\brief instance_name を持つ PortInterfaceProfile を探す Functor
		\else
		\brief A functor to find a PortInterfaceProfile named instance_name
		\endif
		"""
		def __init__(self, name):
			self._name = name

		def __call__(self, prof):
			return str(self._name) == str(prof.instance_name)
    

	class find_conn_id:
		"""
		\if jp
		\brief id を持つ ConnectorProfile を探す Functor
		\else
		\brief A functor to find a ConnectorProfile named id
		\endif
		"""
		def __init__(self, id_):
			"""
			 \param id_(string)
			"""
			self._id = id_

		def __call__(self, cprof):
			"""
			 \param cprof(RTC.ConnectorProfile)
			"""
			return str(self._id) == str(cprof.connector_id)


	class find_port_ref:
		"""
		\if jp
		\brief コンストラクタ引数 port_ref と同じオブジェクト参照を探す Functor
		\else
		\brief A functor to find the object reference that is identical port_ref
		\endif
		"""
		def __init__(self, port_ref):
			"""
			 \param port_ref(RTC.Port)
			"""
			self._port_ref = port_ref

		def __call__(self, port_ref):
			"""
			 \param port_ref(RTC.Port)
			"""
			return self._port_ref._is_equivalent(port_ref)


	class connect_func:
		"""
		\if jp
		\brief Port の接続を行う Functor
		\else
		\brief A functor to connect Ports
		\endif
		"""
		def __init__(self, p, prof):
			"""
			 \param p(RTC.Port)
			 \param prof(RTC.ConnectorProfile)
			"""
			self._port_ref = p
			self._connector_profile = prof
			self.return_code = RTC.RTC_OK

		def __call__(self, p):
			"""
			 \param p(RTC.Port)
			"""
			if not self._port_ref._is_equivalent(p):
				retval = p.notify_connect(self._connector_profile)
				if retval != RTC.RTC_OK:
					self.return_code = retval


	class disconnect_func:
		"""
		\if jp
		\brief Port の接続解除を行う Functor
		\else
		\brief A functor to disconnect Ports
		\endif
		"""
		def __init__(self, p, prof):
			"""
			 \param p(RTC.Port)
			 \param prof(RTC.ConnectorProfile)
			"""
			self._port_ref = p
			self._connector_profile = prof
			self.return_code = RTC.RTC_OK
			
		def __call__(self, p):
			"""
			 \param p(RTC.Port)
			"""
			if not self._port_ref._is_equivalent(p):
				retval = p.disconnect(self._connector_profile.connector_id)
				if retval != RTC.RTC_OK:
					self.return_code = retval


	class disconnect_all_func:
		"""
		\if jp
		\brief Port の全接続解除を行う Functor
		\else
		\brief A functor to disconnect all Ports
		\endif
		"""
		def __init__(self, p):
			"""
			 \param p(OpenRTM.PortBase)
			"""
			self.return_code = RTC.RTC_OK
			self._port = p

		def __call__(self, p):
			"""
			 \param p(RTC.ConnectorProfile)
			"""
			retval = self._port.disconnect(p.connector_id)
			if retval != RTC.RTC_OK:
				self.return_code = retval
				
	class find_interface:
		"""
		\if jp
		\brief name と polarity から interface を探す Functor
		\else
		\brief A functor to find interface from name and polarity
		\endif
		"""
		def __init__(self, name, pol):
			"""
			 \param name(string)
			 \param pol(RTC.PortInterfacePolarity)
			"""
			self._name = name
			self._pol = pol

		def __call__(self, prof):
			"""
			 \param prof(RTC.PortInterfaceProfile)
			"""
			name = prof.instance_name
			return (str(self._name) == str(name)) and (self._pol == prof.polarity)
