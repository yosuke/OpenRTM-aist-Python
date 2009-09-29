#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file PortBase.py
# @brief RTC's Port base class
# @date $Date: 2007/09/18 $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.


import threading
import copy

import OpenRTM_aist
import RTC, RTC__POA



##
# @if jp
# @class PortBase
# @brief Port の基底クラス
#
# RTC::Port の基底となるクラス。
# RTC::Port はほぼ UML Port の概念を継承しており、ほぼ同等のものとみなす
# ことができる。RT コンポーネントのコンセプトにおいては、
# Port はコンポーネントに付属し、コンポーネントが他のコンポーネントと相互作用
# を行う接点であり、通常幾つかのインターフェースと関連付けられる。
# コンポーネントは Port を通して外部に対しインターフェースを提供または要求
# することができ、Portはその接続を管理する役割を担う。
# <p>
# Port の具象クラスは、通常 RT コンポーネントインスタンス生成時に同時に
# 生成され、提供・要求インターフェースを登録した後、RT コンポーネントに
# 登録され、外部からアクセス可能な Port として機能することを想定している。
# <p>
# RTC::Port は CORBA インターフェースとして以下のオペレーションを提供する。
#
# - get_port_profile()
# - get_connector_profiles()
# - get_connector_profile()
# - connect()
# - notify_connect()
# - disconnect()
# - notify_disconnect()
# - disconnect_all()
#
# このクラスでは、これらのオペレーションの実装を提供する。
# <p>
# これらのオペレーションのうち、get_port_profile(), get_connector_profiles(),
# get_connector_profile(), connect(), disconnect(), disconnect_all() は、
# サブクラスにおいて特に振る舞いを変更する必要がないため、オーバーライド
# することは推奨されない。
# <p>
# notify_connect(), notify_disconnect() については、サブクラスが提供・要求
# するインターフェースの種類に応じて、振る舞いを変更する必要が生ずる
# かもしれないが、これらを直接オーバーライドすることは推奨されず、
# 後述の notify_connect(), notify_disconnect() の項においても述べられる通り
# これらの関数に関連した 関数をオーバーライドすることにより振る舞いを変更する
# ことが推奨される。
#
# @since 0.4.0
#
# @else
#
#
# @endif
class PortBase(RTC__POA.PortService):
  """
  """



  ##
  # @if jp
  # @brief コンストラクタ
  #
  # PortBase のコンストラクタは Port 名 name を引数に取り初期化を行う
  # と同時に、自分自身を CORBA Object として活性化し、自身の PortProfile
  # の port_ref に自身のオブジェクトリファレンスを格納する。
  #
  # @param self
  # @param name Port の名前(デフォルト値:None)
  #
  # @else
  #
  # @brief Constructor
  #
  # The constructor of the ProtBase class is given the name of this Port
  # and initialized. At the same time, the PortBase activates itself
  # as CORBA object and stores its object reference to the PortProfile's 
  # port_ref member.
  #
  # @param name The name of Port 
  #
  # @endif
  def __init__(self, name=None):
    self._profile = RTC.PortProfile("", [], RTC.PortService._nil, [], RTC.RTObject._nil,[])
    
    if name is None:
      self._profile.name = ""
    else:
      self._profile.name = name
      
    self._objref = self._this()
    self._profile.port_ref = self._objref
    self._profile.owner = RTC.RTObject._nil
    self._profile_mutex = threading.RLock()
    self._rtcout = OpenRTM_aist.Manager.instance().getLogbuf(name)
    self._onPublishInterfaces = None
    self._onSubscribeInterfaces = None
    self._onConnected = None
    self._onUnsubscribeInterfaces = None
    self._onDisconnected = None
    self._onConnectionLost = None


  def __del__(self):
    self._rtcout.RTC_TRACE("PortBase.__del__()")
    try:
      mgr = OpenRTM_aist.Manager.instance().getPOA()
      oid = mgr.servant_to_id(self)
      mgr.deactivate_object(oid)
    except:
      self._rtcout.RTC_WARN("Unknown exception caught.")
    

  ##
  # @if jp
  #
  # @brief [CORBA interface] PortProfileを取得する
  #
  # Portが保持するPortProfileを返す。
  # PortProfile 構造体は以下のメンバーを持つ。
  #
  # - name              [string 型] Port の名前。
  # - interfaces        [PortInterfaceProfileList 型] Port が保持する
  #                     PortInterfaceProfile のシーケンス
  # - port_ref          [Port Object 型] Port 自身のオブジェクトリファレンス
  # - connector_profile [ConnectorProfileList 型] Port が現在保持する
  #                     ConnectorProfile のシーケンス
  # - owner             [RTObject Object 型] この Port を所有する
  #                     RTObjectのリファレンス
  # - properties        [NVList 型] その他のプロパティ。
  #
  # @param self
  #
  # @return PortProfile
  #
  # @else
  #
  # @brief [CORBA interface] Get the PortProfile of the Port
  #
  # This operation returns the PortProfile of the Port.
  # PortProfile struct has the following members,
  #
  # - name              [string ] The name of the Port.
  # - interfaces        [PortInterfaceProfileList 型] The sequence of 
  #                     PortInterfaceProfile owned by the Port
  # - port_ref          [Port Object] The object reference of the Port.
  # - connector_profile [ConnectorProfileList 型] The sequence of 
  #                     ConnectorProfile owned by the Port.
  # - owner             [RTObject Object] The object reference of 
  #                     RTObject that is owner of the Port.
  # - properties        [NVList] The other properties.
  #
  # @return the PortProfile of the Port
  #
  # @endif
  def get_port_profile(self):
    guard = OpenRTM_aist.ScopedLock(self._profile_mutex)

    prof = RTC.PortProfile(self._profile.name,
                           self._profile.interfaces,
                           self._profile.port_ref,
                           self._profile.connector_profiles,
                           self._profile.owner,
                           self._profile.properties)

    return prof


  def getPortProfile(self):
    self._rtcout.RTC_TRACE("getPortProfile()")
    return self._profile


  ##
  # @if jp
  #
  # @brief [CORBA interface] ConnectorProfileListを取得する
  #
  # Portが保持する ConnectorProfile の sequence を返す。
  # ConnectorProfile は Port 間の接続プロファイル情報を保持する構造体であり、
  # 接続時にPort間で情報交換を行い、関連するすべての Port で同一の値が
  # 保持される。
  # ConnectorProfile は以下のメンバーを保持している。
  #
  # - name         [string 型] このコネクタの名前。
  # - connector_id [string 型] ユニークなID
  # - ports        [Port sequnce] このコネクタに関連する Port のオブジェクト
  #                リファレンスのシーケンス。
  # - properties   [NVList 型] その他のプロパティ。
  #
  # @param self
  #
  # @return この Port が保持する ConnectorProfile
  #
  # @else
  #
  # @brief [CORBA interface] Get the ConnectorProfileList of the Port
  #
  # This operation returns a list of the ConnectorProfiles of the Port.
  # ConnectorProfile includes the connection information that describes 
  # relation between (among) Ports, and Ports exchange the ConnectionProfile
  # on connection process and hold the same information in each Port.
  # ConnectionProfile has the following members,
  #
  # - name         [string] The name of the connection.
  # - connector_id [string] Unique identifier.
  # - ports        [Port sequnce] The sequence of Port's object reference
  #                that are related the connection.
  # - properties   [NVList] The other properties.
  #
  # @return the ConnectorProfileList of the Port
  #
  # @endif
  # virtual ConnectorProfileList* get_connector_profiles()
  def get_connector_profiles(self):
    self._rtcout.RTC_TRACE("get_connector_profiles()")
    guard = OpenRTM_aist.ScopedLock(self._profile_mutex)
    return self._profile.connector_profiles


  ##
  # @if jp
  #
  # @brief [CORBA interface] ConnectorProfile を取得する
  #
  # connector_id で指定された ConnectorProfile を返す。
  # 指定した connector_id を持つ ConnectorProfile を保持していない場合は、
  # 空の ConnectorProfile を返す。
  #
  # @param self
  # @param connector_id ConnectorProfile の ID
  #
  # @return connector_id で指定された ConnectorProfile
  #
  # @else
  #
  # @brief [CORBA interface] Get the ConnectorProfile
  #
  # This operation returns the ConnectorProfiles specified connector_id.
  #
  # @param connector_id ID of the ConnectorProfile
  #
  # @return the ConnectorProfile identified by the connector_id
  #
  # @endif
  def get_connector_profile(self, connector_id):
    self._rtcout.RTC_TRACE("get_connector_profile(%s)", connector_id)
    guard = OpenRTM_aist.ScopedLock(self._profile_mutex)
    index = OpenRTM_aist.CORBA_SeqUtil.find(self._profile.connector_profiles,
                                            self.find_conn_id(connector_id))
    if index < 0:
      conn_prof = RTC.ConnectorProfile("","",[],[])
      return conn_prof

    conn_prof = RTC.ConnectorProfile(self._profile.connector_profiles[index].name,
                                     self._profile.connector_profiles[index].connector_id,
                                     self._profile.connector_profiles[index].ports,
                                     self._profile.connector_profiles[index].properties)
    return conn_prof


  ##
  # @if jp
  #
  # @brief [CORBA interface] Port の接続を行う
  #
  # 与えられた ConnectoionProfile の情報を基に、Port間の接続を確立する。
  # アプリケーションプログラム側は、幾つかのコンポーネントが持つ複数の
  # Port を接続したい場合、適切な値をセットした ConnectorProfile を
  # connect() の引数として与えてコールすることにより、関連する Port の
  # 接続を確立する。
  #
  # connect() に与える ConnectorProfile のメンバーのうち、name, ports, 
  # properties メンバーに対してデータをセットしなければならない。
  #
  # OutPort 側の connect() では以下のシーケンスで処理が行われる。
  #
  # 1. OutPort に関連する connector 情報の生成およびセット
  #
  # 2. InPortに関連する connector 情報の取得
  #  - ConnectorProfile::properties["dataport.corba_any.inport_ref"]に
  #    OutPortAny のオブジェクトリファレンスが設定されている場合、
  #    リファレンスを取得してConsumerオブジェクトにセットする。
  #    リファレンスがセットされていなければ無視して継続。
  #    (OutPortがconnect() 呼び出しのエントリポイントの場合は、
  #    InPortのオブジェクトリファレンスはセットされていないはずである。)
  #
  # 3. PortBase::connect() をコール
  #    Portの接続の基本処理が行われる。
  #
  # 4. 上記2.でInPortのリファレンスが取得できなければ、再度InPortに
  #    関連する connector 情報を取得する。
  #
  # 5. ConnectorProfile::properties で与えられた情報から、
  #    OutPort側の初期化処理を行う。
  #
  # - [dataport.interface_type]<BR>
  # -- CORBA_Any の場合: 
  #    InPortAny を通してデータ交換される。
  #    ConnectorProfile::properties["dataport.corba_any.inport_ref"]に
  #    InPortAny のオブジェクトリファレンスをセットする。<BR>
  #
  # - [dataport.dataflow_type]<BR>
  # -- Pushの場合: Subscriberを生成する。Subscriberのタイプは、
  #    dataport.subscription_type に設定されている。<BR>
  # -- Pullの場合: InPort側がデータをPull型で取得するため、
  #    特に何もする必要が無い。
  #
  # - [dataport.subscription_type]<BR>
  # -- Onceの場合: SubscriberOnceを生成する。<BR>
  # -- Newの場合: SubscriberNewを生成する。<BR>
  # -- Periodicの場合: SubscriberPeriodicを生成する。
  #
  # - [dataport.push_rate]<BR>
  # -- dataport.subscription_type=Periodicの場合周期を設定する。
  #
  # 6. 上記の処理のうち一つでもエラーであれば、エラーリターンする。
  #    正常に処理が行われた場合は RTC::RTC_OK でリターンする。
  #  
  # @param self
  # @param connector_profile ConnectorProfile
  #
  # @return ReturnCode_t 型のリターンコード
  #
  # @else
  #
  # @brief [CORBA interface] Connect the Port
  #
  # This operation establishes connection according to the given 
  # ConnectionProfile inforamtion. 
  # Application programs, which is going to establish the connection 
  # among Ports owned by RT-Components, have to set valid values to the 
  # ConnectorProfile and give it to the argument of connect() operation.
  # 
  # name, ports, properties members of ConnectorProfile should be set
  # valid values before giving to the argument of connect() operation.
  #
  # @param connector_profile The ConnectorProfile.
  #
  # @return ReturnCode_t The return code of this operation.
  #
  # @endif
  # virtual ReturnCode_t connect(ConnectorProfile& connector_profile)
  def connect(self, connector_profile):
    self._rtcout.RTC_TRACE("connect()")
    if self.isEmptyId(connector_profile):
      guard = OpenRTM_aist.ScopedLock(self._profile_mutex)
      self.setUUID(connector_profile)
      assert(not self.isExistingConnId(connector_profile.connector_id))
      del guard
    else:
      guard = OpenRTM_aist.ScopedLock(self._profile_mutex)
      if self.isExistingConnId(connector_profile.connector_id):
        self._rtcout.RTC_ERROR("Connection already exists.")
        return (RTC.PRECONDITION_NOT_MET,connector_profile)
      del guard

    try:
      retval,connector_profile = connector_profile.ports[0].notify_connect(connector_profile)
      if retval != RTC.RTC_OK:
        self._rtcout.RTC_ERROR("Connection failed. cleanup.")
        self.disconnect(connector_profile.connector_id)
    
      return (retval, connector_profile)
      #return connector_profile.ports[0].notify_connect(connector_profile)
    except:
      return (RTC.BAD_PARAMETER, connector_profile)

    return (RTC.RTC_ERROR, connector_profile)


  ##
  # @if jp
  #
  # @brief [CORBA interface] Port の接続通知を行う
  #
  # このオペレーションは、Port間の接続が行われる際に、Port間で内部的に
  # 呼ばれるオペレーションである。
  # ConnectorProfile には接続対象 Port のリスト情報が保持されている。Port は
  # ConnectorProfile を保持するとともに、リスト中の次 Port の notify_connect 
  # を呼び出す。そして、ポートをコネクタに追加した後、ConnectorProfile に
  # 呼びだし先の Port を設定し、呼びだし元に返す。このように ConnectorProfile
  # を使用して接続通知が伝達されていく。
  #
  # @param self
  # @param connector_profile ConnectorProfile
  #
  # @return ReturnCode_t 型のリターンコード
  #
  # @else
  #
  # @brief [CORBA interface] Notify the Ports connection
  #
  # This operation is invoked between Ports internally when the connection
  # is established.
  # This operation notifies this PortService of the connection between its 
  # corresponding port and the other ports and propagates the given 
  # ConnectionProfile.
  # A ConnectorProfile has a sequence of port references. This PortService 
  # stores the ConnectorProfile and invokes the notify_connect operation of 
  # the next PortService in the sequence. As ports are added to the 
  # connector, PortService references are added to the ConnectorProfile and
  # provided to the caller. In this way, notification of connection is 
  # propagated with the ConnectorProfile.
  #
  # @param connector_profile The ConnectorProfile.
  #
  # @return ReturnCode_t The return code of this operation.
  #
  # @endif
  def notify_connect(self, connector_profile):
    self._rtcout.RTC_TRACE("notify_connect()")

    # publish owned interface information to the ConnectorProfile
    retval = [RTC.RTC_OK for i in range(3)]

    retval[0] = self.publishInterfaces(connector_profile)
    if retval[0] != RTC.RTC_OK:
      self._rtcout.RTC_ERROR("publishInterfaces() in notify_connect() failed.")

    if self._onPublishInterfaces:
      self._onPublishInterfaces(connector_profile)

    # call notify_connect() of the next Port
    retval[1], connector_profile = self.connectNext(connector_profile)
    if retval[1] != RTC.RTC_OK:
      self._rtcout.RTC_ERROR("connectNext() in notify_connect() failed.")

    # subscribe interface from the ConnectorProfile's information
    if self._onSubscribeInterfaces:
      self._onSubscribeInterfaces(connector_profile)
    retval[2] = self.subscribeInterfaces(connector_profile)
    if retval[2] != RTC.RTC_OK:
      self._rtcout.RTC_ERROR("subscribeInterfaces() in notify_connect() failed.")
      #self.notify_disconnect(connector_profile.connector_id)

    self._rtcout.RTC_PARANOID("%d connectors are existing",
                              len(self._profile.connector_profiles))

    guard = OpenRTM_aist.ScopedLock(self._profile_mutex)
    # update ConnectorProfile
    index = self.findConnProfileIndex(connector_profile.connector_id)
    if index < 0:
      OpenRTM_aist.CORBA_SeqUtil.push_back(self._profile.connector_profiles,
                                           connector_profile)
      self._rtcout.RTC_PARANOID("New connector_id. Push backed.")

    else:
      self._profile.connector_profiles[index] = connector_profile
      self._rtcout.RTC_PARANOID("Existing connector_id. Updated.")

    for ret in retval:
      if ret != RTC.RTC_OK:
        return (ret, connector_profile)

    # connection established without errors
    if self._onConnected:
      self._onConnected(connector_profile)

    return (RTC.RTC_OK, connector_profile)


  ##
  # @if jp
  #
  # @brief [CORBA interface] Port の接続を解除する
  #
  # このオペレーションは接続確立時に接続に対して与えられる connector_id に
  # 対応するピア Port との接続を解除する。
  # Port は ConnectorProfile 中のポートリストに含まれる１つのポートの
  # notify_disconnect を呼びだす。接続解除の通知は notify_disconnect によって
  # 実行される。
  #
  # @param self
  # @param connector_id ConnectorProfile の ID
  #
  # @return ReturnCode_t 型のリターンコード
  #
  # @else
  #
  # @brief [CORBA interface] Connect the Port
  #
  # This operation destroys connection between this port and the peer port
  # according to given id that is given when the connection established.
  # This port invokes the notify_disconnect operation of one of the ports 
  # included in the sequence of the ConnectorProfile stored when the 
  # connection was established. The notification of disconnection is 
  # propagated by the notify_disconnect operation.
  #
  # @param connector_id The ID of the ConnectorProfile.
  #
  # @return ReturnCode_t The return code of this operation.
  #
  # @endif
  # virtual ReturnCode_t disconnect(const char* connector_id)
  def disconnect(self, connector_id):
    self._rtcout.RTC_TRACE("disconnect(%s)", connector_id)

    index = self.findConnProfileIndex(connector_id)

    if index < 0:
      self._rtcout.RTC_ERROR("Invalid connector id: %s", connector_id)
      return RTC.BAD_PARAMETER

    guard = OpenRTM_aist.ScopedLock(self._profile_mutex)
    prof = self._profile.connector_profiles[index]
    del guard
    
    if len(prof.ports) < 1:
      self._rtcout.RTC_FATAL("ConnectorProfile has empty port list.")
      return RTC.PRECONDITION_NOT_MET

    for i in range(len(prof.ports)):
      p = prof.ports[i]
      try:
        return p.notify_disconnect(connector_id)
      except:
        self._rtcout.RTC_WARN("Unknown exception caught.")
        continue

    self._rtcout.RTC_ERROR("notify_disconnect() for all ports failed.")
    return RTC.RTC_ERROR


  ##
  # @if jp
  #
  # @brief [CORBA interface] Port の接続解除通知を行う
  #
  # このオペレーションは、Port間の接続解除が行われる際に、Port間で内部的に
  # 呼ばれるオペレーションである。
  # このオペレーションは、該当する Port と接続されている他の Port に接続解除
  # を通知する。接続解除対象の Port はIDによって指定される。Port は
  # ConnectorProfile 中のポートリスト内の次 Port の notify_disconnect を呼び
  # 出す。ポートの接続が解除されると ConnectorProfile から該当する Port の
  # 情報が削除される。このように notify_disconnect を使用して接続解除通知が
  # 伝達されていく。
  #
  # @param self
  # @param connector_id ConnectorProfile の ID
  #
  # @return ReturnCode_t 型のリターンコード
  #
  # @else
  #
  # @brief [CORBA interface] Notify the Ports disconnection
  #
  # This operation is invoked between Ports internally when the connection
  # is destroied.
  # This operation notifies a PortService of a disconnection between its 
  # corresponding port and the other ports. The disconnected connector is 
  # identified by the given ID, which was given when the connection was 
  # established.
  # This port invokes the notify_disconnect operation of the next PortService
  # in the sequence of the ConnectorProfile that was stored when the 
  # connection was established. As ports are disconnected, PortService 
  # references are removed from the ConnectorProfile. In this way, 
  # the notification of disconnection is propagated by the notify_disconnect
  # operation.
  #
  # @param connector_id The ID of the ConnectorProfile.
  #
  # @return ReturnCode_t The return code of this operation.
  #
  # @endif
  # virtual ReturnCode_t notify_disconnect(const char* connector_id)
  def notify_disconnect(self, connector_id):
    self._rtcout.RTC_TRACE("notify_disconnect(%s)", connector_id)

    # The Port of which the reference is stored in the beginning of
    # connectorProfile's PortServiceList is master Port.
    # The master Port has the responsibility of disconnecting all Ports.
    # The slave Ports have only responsibility of deleting its own
    # ConnectorProfile.

    guard = OpenRTM_aist.ScopedLock(self._profile_mutex)

    index = self.findConnProfileIndex(connector_id)

    if index < 0:
      self._rtcout.RTC_ERROR("Invalid connector id: %s", connector_id)
      return RTC.BAD_PARAMETER

    prof = RTC.ConnectorProfile(self._profile.connector_profiles[index].name,
                                self._profile.connector_profiles[index].connector_id,
                                self._profile.connector_profiles[index].ports,
                                self._profile.connector_profiles[index].properties)

    retval = self.disconnectNext(prof)

    if self._onUnsubscribeInterfaces:
      self._onUnsubscribeInterfaces(prof)
    self.unsubscribeInterfaces(prof)

    if self._onDisconnected:
      self._onDisconnected(prof)

    OpenRTM_aist.CORBA_SeqUtil.erase(self._profile.connector_profiles, index)
    
    return retval


  ##
  # @if jp
  #
  # @brief [CORBA interface] Port の全接続を解除する
  #
  # このオペレーションはこの Port に関連した全ての接続を解除する。
  #
  # @param self
  #
  # @return ReturnCode_t 型のリターンコード
  #
  # @else
  #
  # @brief [CORBA interface] Connect the Port
  #
  # This operation destroys all connection channels owned by the Port.
  #
  # @return ReturnCode_t The return code of this operation.
  #
  # @endif
  # virtual ReturnCode_t disconnect_all()
  def disconnect_all(self):
    self._rtcout.RTC_TRACE("disconnect_all()")
    guard = OpenRTM_aist.ScopedLock(self._profile_mutex)
    plist = copy.deepcopy(self._profile.connector_profiles)
    del guard
    
    retcode = RTC.RTC_OK
    len_ = len(plist)
    self._rtcout.RTC_DEBUG("disconnecting %d connections.", len_)

    # disconnect all connections
    # Call disconnect() for each ConnectorProfile.
    for i in range(len_):
      tmpret = self.disconnect(plist[i].connector_id)
      if tmpret != RTC.RTC_OK:
        retcode = tmpret

    return retcode


  #============================================================
  # Local operations
  #============================================================

  ##
  # @if jp
  # @brief Port の名前を設定する
  #
  # Port の名前を設定する。この名前は Port が保持する PortProfile.name
  # に反映される。
  #
  # @param self
  # @param name Port の名前
  #
  # @else
  # @brief Set the name of this Port
  #
  # This operation sets the name of this Port. The given Port's name is
  # applied to Port's PortProfile.name.
  #
  # @param name The name of this Port.
  #
  # @endif
  # void setName(const char* name);
  def setName(self, name):
    self._rtcout.RTC_TRACE("setName(%s)", name)
    guard = OpenRTM_aist.ScopedLock(self._profile_mutex)
    self._profile.name = name


  ##
  # @if jp
  # @brief PortProfileを取得する
  #
  # Portが保持する PortProfile の const 参照を返す。
  #
  # @param self
  #
  # @return この Port の PortProfile
  #
  # @else
  # @brief Get the PortProfile of the Port
  #
  # This operation returns const reference of the PortProfile.
  #
  # @return the PortProfile of the Port
  #
  # @endif
  # const PortProfile& getProfile() const;
  def getProfile(self):
    self._rtcout.RTC_TRACE("getProfile()")
    guard = OpenRTM_aist.ScopedLock(self._profile_mutex)
    return self._profile


  ##
  # @if jp
  #
  # @brief Port のオブジェクト参照を設定する
  #
  # このオペレーションは Port の PortProfile にこの Port 自身の
  # オブジェクト参照を設定する。
  #
  # @param self
  # @param port_ref この Port のオブジェクト参照
  #
  # @else
  #
  # @brief Set the object reference of this Port
  #
  # This operation sets the object reference itself
  # to the Port's PortProfile.
  #
  # @param The object reference of this Port.
  #
  # @endif
  # void setPortRef(PortService_ptr port_ref);
  def setPortRef(self, port_ref):
    self._rtcout.RTC_TRACE("setPortRef()")
    guard = OpenRTM_aist.ScopedLock(self._profile_mutex)
    self._profile.port_ref = port_ref


  ##
  # @if jp
  #
  # @brief Port のオブジェクト参照を取得する
  #
  # このオペレーションは Port の PortProfile が保持している
  # この Port 自身のオブジェクト参照を取得する。
  #
  # @param self
  #
  # @return この Port のオブジェクト参照
  #
  # @else
  #
  # @brief Get the object reference of this Port
  #
  # This operation returns the object reference
  # that is stored in the Port's PortProfile.
  #
  # @return The object reference of this Port.
  #
  # @endif
  # PortService_ptr getPortRef();
  def getPortRef(self):
    self._rtcout.RTC_TRACE("getPortRef()")
    guard = OpenRTM_aist.ScopedLock(self._profile_mutex)
    return self._profile.port_ref


  ##
  # @if jp
  #
  # @brief Port の owner の RTObject を指定する
  #
  # このオペレーションは Port の PortProfile.owner を設定する。
  #
  # @param self
  # @param owner この Port を所有する RTObject の参照
  #
  # @else
  #
  # @brief Set the owner RTObject of the Port
  #
  # This operation sets the owner RTObject of this Port.
  #
  # @param owner The owner RTObject's reference of this Port
  #
  # @endif
  # void setOwner(RTObject_ptr owner);
  def setOwner(self, owner):
    self._rtcout.RTC_TRACE("setOwner()")
    guard = OpenRTM_aist.ScopedLock(self._profile_mutex)
    self._profile.owner = owner


  #============================================================
  # callbacks
  #============================================================

  ##
  # @if jp
  #
  # @brief インターフェースを公開する際に呼ばれるコールバックをセットする
  #
  # このオペレーションは、このポートが接続時に、ポート自身が持つサー
  # ビスインターフェース情報を公開するタイミングで呼ばれるコールバッ
  # クファンクタをセットする。
  #
  # コールバックファンクタの所有権は、呼び出し側にあり、オブジェクト
  # が必要なくなった時に解体するのは呼び出し側の責任である。
  #
  # このコールバックファンクタは、PortBaseクラスの仮想関数である
  # publishInterfaces() が呼ばれたあとに、同じ引数 ConnectorProfile と
  # ともに呼び出される。このコールバックを利用して、
  # publishInterfaces() が公開した ConnectorProfile を変更することが可
  # 能であるが、接続関係の不整合を招かないよう、ConnectorProfile の
  # 変更には注意を要する。
  #
  # @param on_publish ConnectionCallback のサブクラスオブジェクトのポインタ
  #
  # @else
  #
  # @brief Setting callback called on publish interfaces
  #
  # This operation sets a functor that is called after publishing
  # interfaces process when connecting between ports.
  #
  # Since the ownership of the callback functor object is owned by
  # the caller, it has the responsibility of object destruction.
  # 
  # The callback functor is called after calling
  # publishInterfaces() that is virtual member function of the
  # PortBase class with an argument of ConnectorProfile type that
  # is same as the argument of publishInterfaces() function.
  # Although by using this functor, you can modify the ConnectorProfile
  # published by publishInterfaces() function, the modification
  # should be done carefully for fear of causing connection
  # inconsistency.
  #
  # @param on_publish a pointer to ConnectionCallback's subclasses
  #
  # @endif
  #
  # void setOnPublishInterfaces(ConnectionCallback* on_publish);
  def setOnPublishInterfaces(self, on_publish):
    self._onPublishInterfaces = on_publish
    return

  ##
  # @if jp
  #
  # @brief インターフェースを取得する際に呼ばれるコールバックをセットする
  #
  # このオペレーションは、このポートが接続時に、相手のポートが持つサー
  # ビスインターフェース情報を取得するタイミングで呼ばれるコールバッ
  # クファンクタをセットする。
  #
  # コールバックファンクタの所有権は、呼び出し側にあり、オブジェクト
  # が必要なくなった時に解体するのは呼び出し側の責任である。
  #
  # このコールバックファンクタは、PortBaseクラスの仮想関数である
  # subscribeInterfaces() が呼ばれる前に、同じ引数 ConnectorProfile と
  # ともに呼び出される。このコールバックを利用して、
  # subscribeInterfaces() に与える ConnectorProfile を変更することが可
  # 能であるが、接続関係の不整合を招かないよう、ConnectorProfile の
  # 変更には注意を要する。
  #
  # @param on_subscribe ConnectionCallback のサブクラスオブジェクトのポインタ
  #
  # @else
  #
  # @brief Setting callback called on publish interfaces
  #
  # This operation sets a functor that is called before subscribing
  # interfaces process when connecting between ports.
  #
  # Since the ownership of the callback functor object is owned by
  # the caller, it has the responsibility of object destruction.
  # 
  # The callback functor is called before calling
  # subscribeInterfaces() that is virtual member function of the
  # PortBase class with an argument of ConnectorProfile type that
  # is same as the argument of subscribeInterfaces() function.
  # Although by using this functor, you can modify ConnectorProfile
  # argument for subscribeInterfaces() function, the modification
  # should be done carefully for fear of causing connection
  # inconsistency.
  #
  # @param on_subscribe a pointer to ConnectionCallback's subclasses
  #
  # @endif
  #
  #void setOnSubscribeInterfaces(ConnectionCallback* on_subscribe);
  def setOnSubscribeInterfaces(self, on_subscribe):
    self._onSubscribeInterfaces = on_subscribe
    return


  ##
  # @if jp
  #
  # @brief 接続完了時に呼ばれるコールバックをセットする
  #
  # このオペレーションは、このポートが接続完了時に呼ばれる、コールバッ
  # クファンクタをセットする。
  #
  # コールバックファンクタの所有権は、呼び出し側にあり、オブジェクト
  # が必要なくなった時に解体するのは呼び出し側の責任である。
  #
  # このコールバックファンクタは、ポートの接続実行関数である
  # notify_connect() の終了直前に、接続処理が正常終了する際に限って
  # 呼び出されるコールバックである。接続処理の過程でエラーが発生した
  # 場合には呼び出されない。
  # 
  # このコールバックファンクタは notify_connect() が out パラメータ
  # として返すのと同じ引数 ConnectorProfile とともに呼び出されるので、
  # この接続において公開されたすべてのインターフェース情報を得ること
  # ができる。このコールバックを利用して、notify_connect() が返す
  # ConnectorProfile を変更することが可能であるが、接続関係の不整合
  # を招かないよう、ConnectorProfile の変更には注意を要する。
  #
  # @param on_subscribe ConnectionCallback のサブクラスオブジェクトのポインタ
  #
  # @else
  #
  # @brief Setting callback called on connection established
  #
  # This operation sets a functor that is called when connection
  # between ports established.
  #
  # Since the ownership of the callback functor object is owned by
  # the caller, it has the responsibility of object destruction.
  # 
  # The callback functor is called only when notify_connect()
  # function successfully returns. In case of error, the functor
  # will not be called.
  #
  # Since this functor is called with ConnectorProfile argument
  # that is same as out-parameter of notify_connect() function, you
  # can get all the information of published interfaces of related
  # ports in the connection.  Although by using this functor, you
  # can modify ConnectorProfile argument for out-paramter of
  # notify_connect(), the modification should be done carefully for
  # fear of causing connection inconsistency.
  #
  # @param on_subscribe a pointer to ConnectionCallback's subclasses
  #
  # @endif
  #
  # void setOnConnected(ConnectionCallback* on_connected);
  def setOnConnected(self, on_connected):
    self._onConnected = on_connected
    return


  ##
  # @if jp
  #
  # @brief インターフェースを解放する際に呼ばれるコールバックをセットする
  #
  # このオペレーションは、このポートが接続時に、相手のポートが持つサー
  # ビスインターフェース情報を解放するタイミングで呼ばれるコールバッ
  # クファンクタをセットする。
  #
  # コールバックファンクタの所有権は、呼び出し側にあり、オブジェクト
  # が必要なくなった時に解体するのは呼び出し側の責任である。
  #
  # このコールバックファンクタは、PortBaseクラスの仮想関数である
  # unsubscribeInterfaces() が呼ばれる前に、同じ引数 ConnectorProfile と
  # ともに呼び出される。このコールバックを利用して、
  # unsubscribeInterfaces() に与える ConnectorProfile を変更することが可
  # 能であるが、接続関係の不整合を招かないよう、ConnectorProfile の
  # 変更には注意を要する。
  #
  # @param on_unsubscribe ConnectionCallback のサブクラスオブジェク
  # トのポインタ
  #
  # @else
  #
  # @brief Setting callback called on unsubscribe interfaces
  #
  # This operation sets a functor that is called before unsubscribing
  # interfaces process when disconnecting between ports.
  #
  # Since the ownership of the callback functor object is owned by
  # the caller, it has the responsibility of object destruction.
  # 
  # The callback functor is called before calling
  # unsubscribeInterfaces() that is virtual member function of the
  # PortBase class with an argument of ConnectorProfile type that
  # is same as the argument of unsubscribeInterfaces() function.
  # Although by using this functor, you can modify ConnectorProfile
  # argument for unsubscribeInterfaces() function, the modification
  # should be done carefully for fear of causing connection
  # inconsistency.
  #
  # @param on_unsubscribe a pointer to ConnectionCallback's subclasses
  #
  # @endif
  #
  # void setOnUnsubscribeInterfaces(ConnectionCallback* on_subscribe);
  def setOnUnsubscribeInterfaces(self, on_subscribe):
    self._onUnsubscribeInterfaces = on_unsubscribe
    return


  ##
  # @if jp
  #
  # @brief 接続解除に呼ばれるコールバックをセットする
  #
  # このオペレーションは、このポートの接続解除時に呼ばれる、コールバッ
  # クファンクタをセットする。
  #
  # コールバックファンクタの所有権は、呼び出し側にあり、オブジェクト
  # が必要なくなった時に解体するのは呼び出し側の責任である。
  #
  # このコールバックファンクタは、ポートの接続解除実行関数である
  # notify_disconnect() の終了直前に、呼び出されるコールバックである。
  # 
  # このコールバックファンクタは接続に対応する ConnectorProfile とと
  # もに呼び出される。この ConnectorProfile はこのファンクタ呼出し後
  # に破棄されるので、変更がほかに影響を与えることはない。
  #
  # @param on_disconnected ConnectionCallback のサブクラスオブジェク
  # トのポインタ
  #
  # @else
  #
  # @brief Setting callback called on disconnected
  #
  # This operation sets a functor that is called when connection
  # between ports is destructed.
  #
  # Since the ownership of the callback functor object is owned by
  # the caller, it has the responsibility of object destruction.
  # 
  # The callback functor is called just before notify_disconnect()
  # that is disconnection execution function returns.
  #
  # This functor is called with argument of corresponding
  # ConnectorProfile.  Since this ConnectorProfile will be
  # destructed after calling this functor, modifications never
  # affect others.
  #
  # @param on_disconnected a pointer to ConnectionCallback's subclasses
  #
  # @endif
  #
  # void setOnDisconnected(ConnectionCallback* on_disconnected);
  def setOnDisconnected(self, on_disconnected):
    self._onDisconnected = on_disconnected
    return

  # void setOnConnectionLost(ConnectionCallback* on_connection_lost);
  def setOnConnectionLost(self, on_connection_lost):
    self._onConnectionLost = on_connection_lost
    return

  ##
  # @if jp
  #
  # @brief Interface 情報を公開する(サブクラス実装用)
  #
  # このオペレーションは、notify_connect() 処理シーケンスの始めにコール
  # される関数である。
  # notify_connect() では、
  #
  # - publishInterfaces()
  # - connectNext()
  # - subscribeInterfaces()
  # - updateConnectorProfile()
  #
  # の順に protected 関数がコールされ接続処理が行われる。
  # <br>
  # 具象 Port ではこのオペレーションをオーバーライドし、引数として
  # 与えられた ConnectorProfile に従い処理を行い、パラメータが不適切
  # であれば、RteurnCode_t 型のエラーコードを返す。
  # 通常 publishInterafaces() 内においては、この Port に属する
  # インターフェースに関する情報を ConnectorProfile に対して適切に設定し
  # 他の Port に通知しなければならない。
  # <br>
  # また、この関数がコールされる段階では、他の Port の Interface に関する
  # 情報はすべて含まれていないので、他の Port の Interface を取得する処理
  # は subscribeInterfaces() 内で行われるべきである。
  # <br>
  # このオペレーションは、新規の connector_id に対しては接続の生成、
  # 既存の connector_id に対しては更新が適切に行われる必要がある。<BR>
  # ※サブクラスでの実装参照用
  #
  # @param self
  # @param connector_profile 接続に関するプロファイル情報
  #
  # @return ReturnCode_t 型のリターンコード
  #
  # @else
  #
  # @brief Publish interface information
  #
  # This operation is pure virutal method that would be called at the
  # beginning of the notify_connect() process sequence.
  # In the notify_connect(), the following methods would be called in order.
  #
  # - publishInterfaces()
  # - connectNext()
  # - subscribeInterfaces()
  # - updateConnectorProfile() 
  #
  # In the concrete Port, this method should be overridden. This method
  # processes the given ConnectorProfile argument and if the given parameter
  # is invalid, it would return error code of ReturnCode_t.
  # Usually, publishInterfaces() method should set interfaces information
  # owned by this Port, and publish it to the other Ports.
  # <br>
  # When this method is called, other Ports' interfaces information may not
  # be completed. Therefore, the process to obtain other Port's interfaces
  # information should be done in the subscribeInterfaces() method.
  # <br>
  # This operation should create the new connection for the new
  # connector_id, and should update the connection for the existing
  # connection_id.
  #
  # @param connector_profile The connection profile information
  # @return The return code of ReturnCode_t type.
  #
  #@endif
  def publishInterfaces(self, connector_profile):
    pass


  ##
  # @if jp
  #
  # @brief 次の Port に対して notify_connect() をコールする
  #
  # ConnectorProfile の port_ref 内に格納されている Port のオブジェクト
  # リファレンスのシーケンスの中から、自身の Port の次の Port に対して
  # notify_connect() をコールする。
  #
  # @param self
  # @param connector_profile 接続に関するプロファイル情報
  #
  # @return ReturnCode_t 型のリターンコード
  #
  # @else
  #
  # @brief Call notify_connect() of the next Port
  #
  # This operation calls the notify_connect() of the next Port's 
  # that stored in ConnectorProfile's port_ref sequence.
  #
  # @param connector_profile The connection profile information
  #
  # @return The return code of ReturnCode_t type.
  #
  # @endif
  # virtual ReturnCode_t connectNext(ConnectorProfile& connector_profile);
  def connectNext(self, connector_profile):
    index = OpenRTM_aist.CORBA_SeqUtil.find(connector_profile.ports,
                                            self.find_port_ref(self._profile.port_ref))
    if index < 0:
      return RTC.BAD_PARAMETER, connector_profile

    index += 1
    if index < len(connector_profile.ports):
      p = connector_profile.ports[index]
      return p.notify_connect(connector_profile)

    return (RTC.RTC_OK, connector_profile)


  ##
  # @if jp
  #
  # @brief 次の Port に対して notify_disconnect() をコールする
  #
  # ConnectorProfile の port_ref 内に格納されている Port のオブジェクト
  # リファレンスのシーケンスの中から、自身の Port の次の Port に対して
  # notify_disconnect() をコールする。
  #
  # @param self
  # @param connector_profile 接続に関するプロファイル情報
  #
  # @return ReturnCode_t 型のリターンコード
  #
  # @else
  #
  # @brief Call notify_disconnect() of the next Port
  #
  # This operation calls the notify_disconnect() of the next Port's 
  # that stored in ConnectorProfile's port_ref sequence.
  #
  # @param connector_profile The connection profile information
  #
  # @return The return code of ReturnCode_t type.
  #
  # @endif
  # virtual ReturnCode_t disconnectNext(ConnectorProfile& connector_profile);
  def disconnectNext(self, connector_profile):
    index = OpenRTM_aist.CORBA_SeqUtil.find(connector_profile.ports,
                                            self.find_port_ref(self._profile.port_ref))
    if index < 0:
      return RTC.BAD_PARAMETER

    index += 1

    while index < len(connector_profile.ports):
      p = connector_profile.ports[index]
      index += 1
      try:
        return p.notify_disconnect(connector_profile.connector_id)
      except:
        self._rtcout.RTC_WARN("Unknown exception caught.")
        continue

    return RTC.RTC_OK


  ##
  # @if jp
  #
  # @brief Interface 情報を取得する(サブクラス実装用)
  #
  # このオペレーションは、notify_connect() 処理シーケンスの中間にコール
  # される関数である。
  # notify_connect() では、
  #
  #  - publishInterfaces()
  #  - connectNext()
  #  - subscribeInterfaces()
  #  - updateConnectorProfile()
  #
  # の順に protected 関数がコールされ接続処理が行われる。
  # <br>
  # 具象 Port ではこのオペレーションをオーバーライドし、引数として
  # 与えられた ConnectorProfile に従い処理を行い、パラメータが不適切
  # であれば、RteurnCode_t 型のエラーコードを返す。
  # 引数 ConnectorProfile には他の Port の Interface に関する情報が
  # 全て含まれている。
  # 通常 subscribeInterafaces() 内においては、この Port が使用する
  # Interface に関する情報を取得し、要求側のインターフェースに対して
  # 情報を設定しなければならない。
  # <br>
  # このオペレーションは、新規の connector_id に対しては接続の生成、
  # 既存の connector_id に対しては更新が適切に行われる必要がある。<BR>
  # ※サブクラスでの実装参照用
  #
  # @param self
  # @param connector_profile 接続に関するプロファイル情報
  #
  # @return ReturnCode_t 型のリターンコード
  #
  # @else
  #
  # @brief Publish interface information
  #
  # This operation is pure virutal method that would be called at the
  # mid-flow of the notify_connect() process sequence.
  # In the notify_connect(), the following methods would be called in order.
  #
  #  - publishInterfaces()
  #  - connectNext()
  #  - subscribeInterfaces()
  #  - updateConnectorProfile()
  #
  # In the concrete Port, this method should be overridden. This method
  # processes the given ConnectorProfile argument and if the given parameter
  # is invalid, it would return error code of ReturnCode_t.
  # The given argument ConnectorProfile includes all the interfaces
  # information in it.
  # Usually, subscribeInterafaces() method obtains information of interfaces
  # from ConnectorProfile, and should set it to the interfaces that require
  # them.
  # <br>
  # This operation should create the new connection for the new
  # connector_id, and should update the connection for the existing
  # connection_id.
  #
  # @param connector_profile The connection profile information
  #
  # @return The return code of ReturnCode_t type.
  #
  #@endif
  def subscribeInterfaces(self, connector_profile):
    pass


  ##
  # @if jp
  #
  # @brief Interface の接続を解除する(サブクラス実装用)
  #
  # このオペレーションは、notify_disconnect() 処理シーケンスの終わりにコール
  # される関数である。
  # notify_disconnect() では、
  #  - disconnectNext()
  #  - unsubscribeInterfaces()
  #  - eraseConnectorProfile()
  # の順に protected 関数がコールされ接続解除処理が行われる。
  # <br>
  # 具象 Port ではこのオペレーションをオーバーライドし、引数として
  # 与えられた ConnectorProfile に従い接続解除処理を行う。<BR>
  # ※サブクラスでの実装参照用
  #
  # @param self
  # @param connector_profile 接続に関するプロファイル情報
  #
  # @else
  #
  # @brief Disconnect interface connection
  #
  # This operation is pure virutal method that would be called at the
  # end of the notify_disconnect() process sequence.
  # In the notify_disconnect(), the following methods would be called.
  #  - disconnectNext()
  #  - unsubscribeInterfaces()
  #  - eraseConnectorProfile() 
  # <br>
  # In the concrete Port, this method should be overridden. This method
  # processes the given ConnectorProfile argument and disconnect interface
  # connection.
  #
  # @param connector_profile The connection profile information
  #
  # @endif
  def unsubscribeInterfaces(self, connector_profile):
    pass


  ##
  # @if jp
  #
  # @brief ConnectorProfile の connector_id フィールドが空かどうか判定
  #
  # 指定された ConnectorProfile の connector_id が空であるかどうかの判定を
  # 行う。
  #
  # @param self
  # @param connector_profile 判定対象コネクタプロファイル
  #
  # @return 引数で与えられた ConnectorProfile の connector_id が空であれば、
  #         true、そうでなければ false を返す。
  #
  # @else
  #
  # @brief Whether connector_id of ConnectorProfile is empty
  #
  # @return If the given ConnectorProfile's connector_id is empty string,
  #         it returns true.
  #
  # @endif
  # bool isEmptyId(const ConnectorProfile& connector_profile) const;
  def isEmptyId(self, connector_profile):
    return connector_profile.connector_id == ""


  ##
  # @if jp
  #
  # @brief UUIDを生成する
  #
  # このオペレーションは UUID を生成する。
  #
  # @param self
  #
  # @return uuid
  #
  # @else
  #
  # @brief Get the UUID
  #
  # This operation generates UUID.
  #
  # @return uuid
  #
  # @endif
  # const std::string getUUID() const;
  def getUUID(self):
    return str(OpenRTM_aist.uuid1())


  ##
  # @if jp
  #
  # @brief UUIDを生成し ConnectorProfile にセットする
  #
  # このオペレーションは UUID を生成し、ConnectorProfile にセットする。
  #
  # @param self
  # @param connector_profile connector_id をセットする ConnectorProfile
  #
  # @else
  #
  # @brief Create and set the UUID to the ConnectorProfile
  #
  # This operation generates and set UUID to the ConnectorProfile.
  #
  # @param connector_profile ConnectorProfile to be set connector_id
  #
  # @endif
  # void setUUID(ConnectorProfile& connector_profile) const;
  def setUUID(self, connector_profile):
    connector_profile.connector_id = self.getUUID()
    assert(connector_profile.connector_id != "")


  ##
  # @if jp
  #
  # @brief id が既存の ConnectorProfile のものかどうか判定する
  #
  # このオペレーションは与えられた ID が既存の ConnectorProfile のリスト中に
  # 存在するかどうか判定する。
  #
  # @param self
  # @param id_ 判定する connector_id
  #
  # @return id の存在判定結果
  #
  # @else
  #
  # @brief Whether the given id exists in stored ConnectorProfiles
  #
  # This operation returns boolean whether the given id exists in 
  # the Port's ConnectorProfiles.
  #
  # @param id connector_id to be find in Port's ConnectorProfiles
  #
  # @endif
  # bool isExistingConnId(const char* id);
  def isExistingConnId(self, id_):
    return OpenRTM_aist.CORBA_SeqUtil.find(self._profile.connector_profiles,
                                           self.find_conn_id(id_)) >= 0


  ##
  # @if jp
  #
  # @brief id を持つ ConnectorProfile を探す
  #
  # このオペレーションは与えられた ID を持つ ConnectorProfile を Port が
  # もつ ConnectorProfile のリスト中から探す。
  # もし、同一の id を持つ ConnectorProfile がなければ、空の ConnectorProfile
  # が返される。
  #
  # @param self
  # @param id_ 検索する connector_id
  #
  # @return connector_id を持つ ConnectorProfile
  #
  # @else
  #
  # @brief Find ConnectorProfile with id
  #
  # This operation returns ConnectorProfile with the given id from Port's
  # ConnectorProfiles' list.
  # If the ConnectorProfile with connector id that is identical with the
  # given id does not exist, empty ConnectorProfile is returned.
  #
  # @param id the connector_id to be searched in Port's ConnectorProfiles
  #
  # @return CoonectorProfile with connector_id
  #
  # @endif
  # ConnectorProfile findConnProfile(const char* id);
  def findConnProfile(self, id_):
    index = OpenRTM_aist.CORBA_SeqUtil.find(self._profile.connector_profiles,
                                            self.find_conn_id(id_))
    if index < 0 or index >= len(self._profile.connector_profiles):
      return RTC.ConnectorProfile("","",[],[])

    return self._profile.connector_profiles[index]


  ##
  # @if jp
  #
  # @brief id を持つ ConnectorProfile を探す
  #
  # このオペレーションは与えられた ID を持つ ConnectorProfile を Port が
  # もつ ConnectorProfile のリスト中から探しインデックスを返す。
  # もし、同一の id を持つ ConnectorProfile がなければ、-1 を返す。
  #
  # @param self
  # @param id_ 検索する connector_id
  #
  # @return Port の ConnectorProfile リストのインデックス
  #
  # @else
  #
  # @brief Find ConnectorProfile with id
  #
  # This operation returns ConnectorProfile with the given id from Port's
  # ConnectorProfiles' list.
  # If the ConnectorProfile with connector id that is identical with the
  # given id does not exist, empty ConnectorProfile is returned.
  #
  # @param id the connector_id to be searched in Port's ConnectorProfiles
  #
  # @return The index of ConnectorProfile of the Port
  #
  # @endif
  # CORBA::Long findConnProfileIndex(const char* id);
  def findConnProfileIndex(self, id_):
    return OpenRTM_aist.CORBA_SeqUtil.find(self._profile.connector_profiles,
                                           self.find_conn_id(id_))


  ##
  # @if jp
  #
  # @brief ConnectorProfile の追加もしくは更新
  #
  # このオペレーションは与えられた与えられた ConnectorProfile を
  # Port に追加もしくは更新保存する。
  # 与えられた ConnectorProfile の connector_id と同じ ID を持つ
  # ConnectorProfile がリストになければ、リストに追加し、
  # 同じ ID が存在すれば ConnectorProfile を上書き保存する。
  #
  # @param self
  # @param connector_profile 追加もしくは更新する ConnectorProfile
  #
  # @else
  #
  # @brief Append or update the ConnectorProfile list
  #
  # This operation appends or updates ConnectorProfile of the Port
  # by the given ConnectorProfile.
  # If the connector_id of the given ConnectorProfile does not exist
  # in the Port's ConnectorProfile list, the given ConnectorProfile would be
  # append to the list. If the same id exists, the list would be updated.
  #
  # @param connector_profile the ConnectorProfile to be appended or updated
  #
  # @endif
  # void updateConnectorProfile(const ConnectorProfile& connector_profile);
  def updateConnectorProfile(self, connector_profile):
    index = OpenRTM_aist.CORBA_SeqUtil.find(self._profile.connector_profiles,
                                            self.find_conn_id(connector_profile.connector_id))

    if index < 0:
      OpenRTM_aist.CORBA_SeqUtil.push_back(self._profile.connector_profiles,
                                           connector_profile)
    else:
      self._profile.connector_profiles[index] = connector_profile


  ##
  # @if jp
  #
  # @brief ConnectorProfile を削除する
  #
  # このオペレーションは Port の PortProfile が保持している
  # ConnectorProfileList のうち与えられた id を持つ ConnectorProfile
  # を削除する。
  #
  # @param self
  # @param id_ 削除する ConnectorProfile の id
  #
  # @return 正常に削除できた場合は true、
  #         指定した ConnectorProfile が見つからない場合は false を返す
  #
  # @else
  #
  # @brief Delete the ConnectorProfile
  #
  # This operation deletes a ConnectorProfile specified by id from
  # ConnectorProfileList owned by PortProfile of this Port.
  #
  # @param id The id of the ConnectorProfile to be deleted.
  #
  # @endif
  # bool eraseConnectorProfile(const char* id);
  def eraseConnectorProfile(self, id_):
    guard = OpenRTM_aist.ScopedLock(self._profile_mutex)

    index = OpenRTM_aist.CORBA_SeqUtil.find(self._profile.connector_profiles,
                                            self.find_conn_id(id_))

    if index < 0:
      return False

    OpenRTM_aist.CORBA_SeqUtil.erase(self._profile.connector_profiles, index)

    return True


  ##
  # @if jp
  #
  # @brief PortInterfaceProfile に インターフェースを登録する
  #
  # このオペレーションは Port が持つ PortProfile の、PortInterfaceProfile
  # にインターフェースの情報を追加する。
  # この情報は、get_port_profile() 似よって得られる PortProfile のうち
  # PortInterfaceProfile の値を変更するのみであり、実際にインターフェースを
  # 提供したり要求したりする場合には、サブクラスで、 publishInterface() ,
  #  subscribeInterface() 等の関数を適切にオーバーライドしインターフェースの
  # 提供、要求処理を行わなければならない。
  #
  # インターフェース(のインスタンス)名は Port 内で一意でなければならない。
  # 同名のインターフェースがすでに登録されている場合、この関数は false を
  # 返す。
  #
  # @param self
  # @param instance_name インターフェースのインスタンスの名前
  # @param type_name インターフェースの型の名前
  # @param pol インターフェースの属性 (RTC::PROVIDED もしくは RTC:REQUIRED)
  #
  # @return インターフェース登録処理結果。
  #         同名のインターフェースが既に登録されていれば false を返す。
  #
  # @else
  #
  # @brief Append an interface to the PortInterfaceProfile
  #
  # This operation appends interface information to the PortInterfaceProfile
  # that is owned by the Port.
  # The given interfaces information only updates PortInterfaceProfile of
  # PortProfile that is obtained through get_port_profile().
  # In order to provide and require interfaces, proper functions (for
  # example publishInterface(), subscribeInterface() and so on) should be
  # overridden in subclasses, and these functions provide concrete interface
  # connection and disconnection functionality.
  #
  # The interface (instance) name have to be unique in the Port.
  # If the given interface name is identical with stored interface name,
  # this function returns false.
  #
  # @param name The instance name of the interface.
  # @param type_name The type name of the interface.
  # @param pol The interface's polarity (RTC::PROVIDED or RTC:REQUIRED)
  #
  # @return false would be returned if the same name is already registered.
  #
  # @endif
  # bool appendInterface(const char* name, const char* type_name,
  #			 PortInterfacePolarity pol);
  def appendInterface(self, instance_name, type_name, pol):
    index = OpenRTM_aist.CORBA_SeqUtil.find(self._profile.interfaces,
                                            self.find_interface(instance_name, pol))

    if index >= 0:
      return False

    # setup PortInterfaceProfile
    prof = RTC.PortInterfaceProfile(instance_name, type_name, pol)
    OpenRTM_aist.CORBA_SeqUtil.push_back(self._profile.interfaces, prof)

    return True


  ##
  # @if jp
  #
  # @brief PortInterfaceProfile からインターフェース登録を削除する
  #
  # このオペレーションは Port が持つ PortProfile の、PortInterfaceProfile
  # からインターフェースの情報を削除する。
  #
  # @param self
  # @param name インターフェースのインスタンスの名前
  # @param pol インターフェースの属性 (RTC::PROVIDED もしくは RTC:REQUIRED)
  #
  # @return インターフェース削除処理結果。
  #         インターフェースが登録されていなければ false を返す。
  #
  # @else
  #
  # @brief Delete an interface from the PortInterfaceProfile
  #
  # This operation deletes interface information from the
  # PortInterfaceProfile that is owned by the Port.
  #
  # @param name The instance name of the interface.
  # @param pol The interface's polarity (RTC::PROVIDED or RTC:REQUIRED)
  #
  # @return false would be returned if the given name is not registered.
  #
  # @endif
  # bool deleteInterface(const char* name, PortInterfacePolarity pol);
  def deleteInterface(self, name, pol):
    index = OpenRTM_aist.CORBA_SeqUtil.find(self._profile.interfaces,
                                            self.find_interface(name, pol))

    if index < 0:
      return False

    OpenRTM_aist.CORBA_SeqUtil.erase(self._profile.interfaces, index)
    return True


  ##
  # @if jp
  #
  # @brief PortProfile の properties に NameValue 値を追加する
  #
  # PortProfile の properties に NameValue 値を追加する。
  # 追加するデータの型をValueTypeで指定する。
  #
  # @param self
  # @param key properties の name
  # @param value properties の value
  #
  # @else
  #
  # @brief Add NameValue data to PortProfile's properties
  #
  # @param key The name of properties
  # @param value The value of properties
  #
  # @endif
  #  template <class ValueType>
  #  void addProperty(const char* key, ValueType value)
  def addProperty(self, key, value):
    OpenRTM_aist.CORBA_SeqUtil.push_back(self._profile.properties,
                                         OpenRTM_aist.NVUtil.newNV(key, value))

  # void appendProperty(const char* key, const char* value)
  def appendProperty(self, key, value):
    OpenRTM_aist.NVUtil.appendStringValue(self._profile.properties, key, value)


  #============================================================
  # Functor
  #============================================================

  ##
  # @if jp
  # @class if_name
  # @brief instance_name を持つ PortInterfaceProfile を探す Functor
  # @else
  # @brief A functor to find a PortInterfaceProfile named instance_name
  # @endif
  class if_name:
    def __init__(self, name):
      self._name = name

    def __call__(self, prof):
      return str(self._name) == str(prof.instance_name)
    

  ##
  # @if jp
  # @class find_conn_id
  # @brief id を持つ ConnectorProfile を探す Functor
  # @else
  # @brief A functor to find a ConnectorProfile named id
  # @endif
  class find_conn_id:
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

  ##
  # @if jp
  # @class find_port_ref
  # @brief コンストラクタ引数 port_ref と同じオブジェクト参照を探す Functor
  # @else
  # @brief A functor to find the object reference that is identical port_ref
  # @endif
  class find_port_ref:
    def __init__(self, port_ref):
      """
       \param port_ref(RTC.PortService)
      """
      self._port_ref = port_ref

    def __call__(self, port_ref):
      """
       \param port_ref(RTC.PortService)
      """
      return self._port_ref._is_equivalent(port_ref)

  ##
  # @if jp
  # @class connect_func
  # @brief Port の接続を行う Functor
  # @else
  # @brief A functor to connect Ports
  # @endif
  class connect_func:
    def __init__(self, p, prof):
      """
       \param p(RTC.PortService)
       \param prof(RTC.ConnectorProfile)
      """
      self._port_ref = p
      self._connector_profile = prof
      self.return_code = RTC.RTC_OK

    def __call__(self, p):
      """
       \param p(RTC.PortService)
      """
      if not self._port_ref._is_equivalent(p):
        retval = p.notify_connect(self._connector_profile)
        if retval != RTC.RTC_OK:
          self.return_code = retval

  ##
  # @if jp
  # @class disconnect_func
  # @brief Port の接続解除を行う Functor
  # @else
  # @brief A functor to disconnect Ports
  # @endif
  class disconnect_func:
    def __init__(self, p, prof):
      """
       \param p(RTC.PortService)
       \param prof(RTC.ConnectorProfile)
      """
      self._port_ref = p
      self._connector_profile = prof
      self.return_code = RTC.RTC_OK
      
    def __call__(self, p):
      """
       \param p(RTC.PortService)
      """
      if not self._port_ref._is_equivalent(p):
        retval = p.disconnect(self._connector_profile.connector_id)
        if retval != RTC.RTC_OK:
          self.return_code = retval

  ##
  # @if jp
  # @class disconnect_all_func
  # @brief Port の全接続解除を行う Functor
  # @else
  # @brief A functor to disconnect all Ports
  # @endif
  class disconnect_all_func:
    def __init__(self, p):
      """
       \param p(OpenRTM_aist.PortBase)
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

  ##
  # @if jp
  # @class find_interface
  # @brief name と polarity から interface を探す Functor
  # @else
  # @brief A functor to find interface from name and polarity
  # @endif
  class find_interface:
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
