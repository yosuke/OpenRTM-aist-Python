#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file OutPortBase.py
# @brief OutPortBase base class
# @date $Date: 2007/09/19 $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
# 
# Copyright (C) 2003-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

import threading
import OpenRTM_aist
import RTC

##
# @if jp
#
# @class OutPortBase
#
# @brief OutPort 基底クラス
# 
# OutPort の基底クラス。
#
#
#
# Properties: port.outport
# プロパティは
#
# - port.outport
# - port.outport.[name]
# ConnectorProfile.properties の場合は
# - dataport.outport
#
# 以下に指定したものが渡される。
# (port.outport.[name]が優先される)
# さらに、一部のプロパティは接続時に ConnectorProfile により
# 渡される場合があり、その場合は ConnectorProfile が優先される。
#
# - input.throughput.profile: enable
# - input.throughput.update_rate: count [n/count]
# - input.throughput.total_bytes: [bytes]
# - input.throughput.total_count: [n]
# - input.throughput.max_size: [bytes]
# - input.throughput.min_size: [bytes]
# - input.throughput.avg_size: [bytes]
# - input.throughput.byte_sec: [bytes/sec]
#
# - output.throughput.profile: enable
# - output.throughput.update_rate: count [n/count]
# - output.throughput.total_bytes: [bytes]
# - output.throughput.total_count:[n]
# - output.throughput.max_size: [bytes]
# - output.throughput.min_size: [bytes]
# - output.throughput.avg_size: [bytes]
# - output.throughput.max_sendtime: [sec]
# - output.throughput.min_sendtime: [sec]
# - output.throughput.avg_sendtime: [sec]
# - output.throughput.byte_sec: [bytes/sec]
#
# dataport.dataflow_type
# dataport.interface_type
# dataport.subscription_type
#
# [buffer]
#
# - buffer.type:
#     利用可能なバッファのタイプ
#     ConnectorProfile の場合は利用するバッファのタイプ
#     無指定の場合はデフォルトの ringbuffer が使用される。
#     ex. ringbuffer, shmbuffer, doublebuffer, etc.
#     正し、Consumer, Publisher のタイプによっては特定のバッファ型を
#     要求するがあるための、その場合は指定は無効となる。
#
# - buffer.length:
#     バッファの長さ
#
# - buffer.write.full_policy:
#     上書きするかどうかのポリシー
#     overwrite (上書き), do_nothing (何もしない), block (ブロックする)
#     block を指定した場合、次の timeout 値を指定すれば、指定時間後
#     書き込み不可能であればタイムアウトする。
#
# - buffer.write.timeout:
#     タイムアウト時間を [sec] で指定する。
#     1 sec -> 1.0, 1 ms -> 0.001, タイムアウトしない -> 0.0
#
# - buffer.read.empty_policy:
#     バッファが空のときの読み出しポリシー
#     last (最後の要素), do_nothing (何もしない), block (ブロックする)
#     block を指定した場合、次の timeout 値を指定すれば、指定時間後
#     読み出し不可能であればタイムアウトする。
#
# - buffer.read.timeout:
#     タイムアウト時間 [sec] で指定する。
#     1sec -> 1.0, 1ms -> 0.001, タイムアウトしない -> 0.0
#
# - その他バッファ毎に固有なオプション
#
#
# [publihser]
#
# - publisher.types:
#      利用可能な Publisher のタイプ
#      new, periodic, flush, etc..
#
# - publisher.push.policy:
#      InPortへデータを送信するポリシー
#      all: バッファにたまっているすべて送信
#      fifo: バッファをFIFOとみなして送信
#      skip: 古いデータから一定数を間引いて送信
#      new: 常に新しいデータのみを送信
#
# - publisher.push.skip_rate:
#      push.policy=skip のときのスキップ率
#      n: n要素毎にひとつ送信
#
# - publisher.periodic.rate:
#
# - publisher.thread.type:
#       Publisher のスレッドのタイプ
# - publisher.thread.measurement.exec_time: yes/no
# - publisher.thread.measurement.exec_count: number
# - publisher.thread.measurement.period_time: yes/no
# - publisher.thread.measurement.period_count: number
#
# [interface]
#
# - interface.types:
#     OutPort interfaceのタイプ
#     ex. corba_cdr, corba_any, raw_tcp などカンマ区切りで指定。何も
#     指定しなければ利用可能なすべてのプロバイダが使用される
#
#
#
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
# 3. PortBase::connect() をコール
#    Portの接続の基本処理が行われる。
# 4. 上記2.でInPortのリファレンスが取得できなければ、再度InPortに
#    関連する connector 情報を取得する。
#
# 5. ConnectorProfile::properties で与えられた情報から、
#    OutPort側の初期化処理を行う。
#
# - [dataport.interface_type]
# -- CORBA_Any の場合: 
#    InPortAny を通してデータ交換される。
#    ConnectorProfile::properties["dataport.corba_any.inport_ref"]に
#    InPortAny のオブジェクトリファレンスをセットする。
# -- RawTCP の場合: Raw TCP socket を通してデータ交換される。
#    ConnectorProfile::properties["dataport.raw_tcp.server_addr"]
#    にInPort側のサーバアドレスをセットする。
#
# - [dataport.dataflow_type]
# -- Pushの場合: Subscriberを生成する。Subscriberのタイプは、
#    dataport.subscription_type に設定されている。
# -- Pullの場合: InPort側がデータをPull型で取得するため、
#    特に何もする必要が無い。
#
# - [dataport.subscription_type]
# -- Onceの場合: SubscriberOnceを生成する。
# -- Newの場合: SubscriberNewを生成する。
# -- Periodicの場合: SubscriberPeriodicを生成する。
#
# - [dataport.push_interval]
# -- dataport.subscription_type=Periodicの場合周期を設定する。
#
# 6. 上記の処理のうち一つでもエラーであれば、エラーリターンする。
#    正常に処理が行われた場合はRTC::RTC_OKでリターンする。
#
# @since 0.2.0
#
# @else
#
# @class OutPortBase
#
# @brief Output base class.
#
# The base class of OutPort<T> which are implementations of OutPort
#
# Form a kind of Observer pattern with OutPortBase and PublisherBase.
# attach(), detach(), notify() of OutPortBase and
# push() of PublisherBase are methods associated with the Observer pattern.
#
# @since 0.2.0
#
# @endif
#
class OutPortBase(OpenRTM_aist.PortBase,OpenRTM_aist.DataPortStatus):
  """
  """

  ##
  # @if jp
  # @brief Provider を削除するための Functor
  # @else
  # @brief Functor to delete Providers
  # @endif
  #
  class provider_cleanup:
    def __init__(self):
      self._factory = OpenRTM_aist.OutPortProviderFactory.instance()

    def __call__(self, p):
      self._factory.deleteObject(p)

  ##
  # @if jp
  # @brief Connector を削除するための Functor
  # @else
  # @brief Functor to delete Connectors
  # @endif
  #
  class connector_cleanup:
    def __init__(self):
      pass

    def __call__(self, c):
      del c


  ##
  # @if jp
  # @brief コンストラクタ
  #
  # コンストラクタ。
  #
  # @param self
  # @param name ポート名
  #
  # @else
  #
  # @brief A constructor of OutPortBase class.
  #
  # Constructor of OutPortBase.
  #
  # @endif
  # OutPortBase::OutPortBase(const char* name, const char* data_type)
  def __init__(self, name, data_type):
    OpenRTM_aist.PortBase.__init__(self,name)
    self._rtcout.RTC_PARANOID("Port name: %s", name)

    self._rtcout.RTC_PARANOID("setting port.port_type: DataOutPort")
    self.addProperty("port.port_type", "DataOutPort")

    self._rtcout.RTC_PARANOID("setting dataport.data_type: %s", data_type)
    self.addProperty("dataport.data_type", data_type)

    # publisher list
    factory = OpenRTM_aist.PublisherFactory.instance()
    pubs = OpenRTM_aist.flatten(factory.getIdentifiers())

    # blank characters are deleted for RTSE's bug
    pubs = pubs.lstrip()

    self._rtcout.RTC_PARANOID("available subscription_type: %s",  pubs)
    self.addProperty("dataport.subscription_type", pubs)

    self._properties    = OpenRTM_aist.Properties()
    self._name          = name
    self._connectors    = []
    self._consumers     = []
    self._providerTypes = ""
    self._consumerTypes = ""
    self._providers     = []
    self._connector_mutex = threading.RLock()

    self.initConsumers()
    self.initProviders()


  ##
  # @if jp
  # @brief デストラクタ
  #
  # デストラクタ。
  # 登録された全ての Publisher を削除する。
  #
  # @param self
  #
  # @else
  #
  # @brief destructor
  #
  # Destructor
  #
  # @endif
  def __del__(self):
    self._rtcout.RTC_TRACE("~OutPortBase()")
    # provider のクリーンナップ
    OpenRTM_aist.CORBA_SeqUtil.for_each(self._providers,
                                        self.provider_cleanup())
    guard = OpenRTM_aist.ScopedLock(self._connector_mutex)
    # connector のクリーンナップ
    OpenRTM_aist.CORBA_SeqUtil.for_each(self._connectors,
                                        self.connector_cleanup())


  ##
  # @if jp
  # @brief プロパティの初期化
  #
  # OutPortのプロパティを初期化する
  #
  # @else
  #
  # @brief Initializing properties
  #
  # This operation initializes outport's properties
  #
  # @endif
  #
  # void init(coil::Properties& prop);
  def init(self, prop):
    self._rtcout.RTC_TRACE("init()")

    self._rtcout.RTC_PARANOID("given properties:")
    self._properties.mergeProperties(prop)

    self._rtcout.RTC_PARANOID("updated properties:")

    self.configure()


  ##
  # @if jp
  # @brief OutPort名称の取得
  #
  # OutPortの名称を取得する。
  #
  # @param self
  #
  # @return ポート名称
  #
  # @else
  #
  # @brief OutPort's name
  #
  # This operation returns OutPort's name
  #
  # @endif
  def name(self):
    return self._name


  ##
  # @if jp
  # @brief プロパティを取得する
  # @else
  # @brief Get properties
  # @endif
  #
  # coil::Properties& OutPortBase::properties()
  def properties(self):
    self._rtcout.RTC_TRACE("properties()")
    return self._properties


  ##
  # @if jp
  # @brief Connector を取得
  # @else
  # @brief Connector list
  # @endif
  #
  # const std::vector<OutPortConnector*>& OutPortBase::connectors()
  def connectors(self):
    self._rtcout.RTC_TRACE("connectors(): size = %d", len(self._connectors))
    guard = OpenRTM_aist.ScopedLock(self._connector_mutex)
    return self._connectors


  ##
  # @if jp
  # @brief ConnectorProfile を取得
  # @else
  # @brief ConnectorProfile list
  # @endif
  #
  # ConnectorBase::ProfileList OutPortBase::getConnectorProfiles()
  def getConnectorProfiles(self):
    self._rtcout.RTC_TRACE("getConnectorProfiles(): size = %d", len(self._connectors))
    profs = []
    guard = OpenRTM_aist.ScopedLock(self._connector_mutex)
    for con in self._connectors:
      profs.append(con.profile())

    return profs


  ##
  # @if jp
  # @brief ConnectorId を取得
  # @else
  # @brief ConnectorId list
  # @endif
  #
  # coil::vstring OutPortBase::getConnectorIds()
  def getConnectorIds(self):
    ids = []

    guard = OpenRTM_aist.ScopedLock(self._connector_mutex)
    for con in self._connectors:
      ids.append(con.id())

    self._rtcout.RTC_TRACE("getConnectorIds(): %s", OpenRTM_aist.flatten(ids))
    return ids


  ##
  # @if jp
  # @brief Connectorの名前を取得
  # @else
  # @brief Connector name list
  # @endif
  #
  # coil::vstring OutPortBase::getConnectorNames()
  def getConnectorNames(self):
    names = []
    guard = OpenRTM_aist.ScopedLock(self._connector_mutex)
    for con in self._connectors:
      names.append(con.name())

    self._rtcout.RTC_TRACE("getConnectorNames(): %s", OpenRTM_aist.flatten(names))
    return names


  ##
  # @if jp
  # @brief ConnectorProfileをIDで取得
  # @else
  # @brief Getting ConnectorProfile by name
  # @endif
  #
  # bool OutPortBase::getConnectorProfileById(const char* id,
  #                              ConnectorBase::Profile& prof)
  def getConnectorProfileById(self, id, prof):
    self._rtcout.RTC_TRACE("getConnectorProfileById(id = %s)", id)

    sid = id
    guard = OpenRTM_aist.ScopedLock(self._connector_mutex)
    for con in self._connectors:
      if sid  == con.id():
        prof[0] = con.profile()
        return True

    return False


  ##
  # @if jp
  # @brief ConnectorProfileを名前で取得
  # @else
  # @brief Getting ConnectorProfile by name
  # @endif
  #
  # bool OutPortBase::getConnectorProfileByName(const char* name,
  #                                ConnectorBase::Profile& prof)
  def getConnectorProfileByName(self, name, prof):
    self._rtcout.RTC_TRACE("getConnectorProfileById(id = %s)", name)

    sname = name
    guard = OpenRTM_aist.ScopedLock(self._connector_mutex)
    for con in self._connectors:
      if sname == con.name():
        prof[0] = con.profile()
        return True

    return False


  ##
  # @if jp
  # @brief インターフェースプロファイルを公開する
  # @else
  # @brief Publish interface profile
  # @endif
  #
  # bool OutPortBase::publishInterfaceProfiles(SDOPackage::NVList& properties)
  def publishInterfaceProfiles(self, properties):
    self._rtcout.RTC_TRACE("publishInterfaceProfiles()")

    OpenRTM_aist.CORBA_SeqUtil.for_each(self._providers,
                                        OpenRTM_aist.OutPortProvider.publishInterfaceProfileFunc(properties))
    return True


  ##
  # @if jp
  # @brief OutPortを activates する
  # @else
  # @brief Activate all Port interfaces
  # @endif
  #
  # void OutPortBase::activateInterfaces()
  def activateInterfaces(self):
    guard = OpenRTM_aist.ScopedLock(self._connector_mutex)
    for con in self._connectors:
      con.activate()

  
  ##
  # @if jp
  # @brief 全ての Port のインターフェースを deactivates する
  # @else
  # @brief Deactivate all Port interfaces
  # @endif
  #
  # void OutPortBase::deactivateInterfaces()
  def deactivateInterfaces(self):
    guard = OpenRTM_aist.ScopedLock(self._connector_mutex)
    for con in self._connectors:
      con.deactivate()
  
  ##
  # @if jp
  # @brief OutPortの設定を行う
  # @else
  # @brief Configureing outport
  # @endif
  #
  #void OutPortBase::configure()
  def configure(self):
    pass


  ##
  # @if jp
  # @brief Interface情報を公開する
  # @else
  # @brief Publish interface information
  # @endif
  #
  # ReturnCode_t OutPortBase::publishInterfaces(ConnectorProfile& cprof)
  def publishInterfaces(self, cprof):
    self._rtcout.RTC_TRACE("publishInterfaces()")

    # prop: [port.outport].
    prop = self._properties

    conn_prop = OpenRTM_aist.Properties()

    OpenRTM_aist.NVUtil.copyToProperties(conn_prop, cprof.properties)
    prop.mergeProperties(conn_prop.getNode("dataport")) # marge ConnectorProfile


    #
    # ここで, ConnectorProfile からの properties がマージされたため、
    # prop["dataflow_type"]: データフロータイプ
    # prop["interface_type"]: インターフェースタイプ
    # などがアクセス可能になる。
    dflow_type = OpenRTM_aist.normalize([prop.getProperty("dataflow_type")])

    if dflow_type == "push":
      self._rtcout.RTC_PARANOID("dataflow_type = push .... do nothing")
      return RTC.RTC_OK

    elif dflow_type == "pull":
      self._rtcout.RTC_PARANOID("dataflow_type = pull .... create PullConnector")

      provider = self.createProvider(cprof, prop)
      if provider == 0:
        return RTC.BAD_PARAMETER
        
      # create InPortPushConnector
      connector = self.createConnector(cprof, prop, provider_ = provider)
      if connector == 0:
        return RTC.RTC_ERROR

      self._rtcout.RTC_DEBUG("publishInterface() successfully finished.")
      return RTC.RTC_OK

    self._rtcout.RTC_ERROR("unsupported dataflow_type")

    return RTC.BAD_PARAMETER


  ##
  # @if jp
  # @brief Interface情報を取得する
  # @else
  # @brief Subscribe interface
  # @endif
  #
  # ReturnCode_t OutPortBase::subscribeInterfaces(const ConnectorProfile& cprof)
  def subscribeInterfaces(self, cprof):
    self._rtcout.RTC_TRACE("subscribeInterfaces()")

    # prop: [port.outport].
    prop = self._properties

    conn_prop = OpenRTM_aist.Properties()
    OpenRTM_aist.NVUtil.copyToProperties(conn_prop, cprof.properties)
    prop.mergeProperties(conn_prop.getNode("dataport")) # marge ConnectorProfile

    #
    # ここで, ConnectorProfile からの properties がマージされたため、
    # prop["dataflow_type"]: データフロータイプ
    # prop["interface_type"]: インターフェースタイプ
    # などがアクセス可能になる。
    #
    dflow_type = OpenRTM_aist.normalize([prop.getProperty("dataflow_type")])
    
    if dflow_type == "push":
      self._rtcout.RTC_PARANOID("dataflow_type = push .... create PushConnector")

      # interface
      consumer = self.createConsumer(cprof, prop)
      if consumer == 0:
        return RTC.BAD_PARAMETER

      # create OutPortPushConnector
      connector = self.createConnector(cprof, prop, consumer_ = consumer)
      if connector == 0:
        return RTC.RTC_ERROR

      self._rtcout.RTC_DEBUG("publishInterface() successfully finished.")
      return RTC.RTC_OK

    elif dflow_type == "pull":
      self._rtcout.RTC_PARANOID("dataflow_type = pull .... do nothing")
      return RTC.RTC_OK

    self._rtcout.RTC_ERROR("unsupported dataflow_type")
    return RTC.BAD_PARAMETER


  ##
  # @if jp
  # @brief 登録されているInterface情報を解除する
  # @else
  # @brief Unsubscribe interface
  # @endif
  #
  # void
  # OutPortBase::unsubscribeInterfaces(const ConnectorProfile& connector_profile)
  def unsubscribeInterfaces(self, connector_profile):
    self._rtcout.RTC_TRACE("unsubscribeInterfaces()")

    id = connector_profile.connector_id
    self._rtcout.RTC_PARANOID("connector_id: %s", id)

    for (i,con) in enumerate(self._connectors):
      if id == con.id():
        guard = OpenRTM_aist.ScopedLock(self._connector_mutex)
        # Connector's dtor must call disconnect()
        self._connectors[i].deactivate()
        del self._connectors[i]
        self._rtcout.RTC_TRACE("delete connector: %s", id)
        return

    self._rtcout.RTC_ERROR("specified connector not found: %s", id)
    return


  ##
  # @if jp
  # @brief OutPort provider の初期化
  # @else
  # @brief OutPort provider initialization
  # @endif
  #
  # void OutPortBase::initProviders()
  def initProviders(self):
    self._rtcout.RTC_TRACE("initProviders()")

    # create OutPort providers
    factory = OpenRTM_aist.OutPortProviderFactory.instance()
    provider_types = factory.getIdentifiers()
    self._rtcout.RTC_PARANOID("available OutPortProviders: %s",
                              OpenRTM_aist.flatten(provider_types))

    if self._properties.hasKey("provider_types") and \
          OpenRTM_aist.normalize(self._properties.getProperty("provider_types")) != "all":
      self._rtcout.RTC_DEBUG("allowed providers: %s",
                             self._properties.getProperty("provider_types"))

      temp_types = provider_types
      provider_types = []
      active_types = OpenRTM_aist.split(self._properties.getProperty("provider_types"), ",")

      temp_types.sort()
      active_types.sort()
      set_intersection = lambda a, b: [x for x in a if x in b]
      provider_types = provider_types + set_intersection(temp_types, active_types)

    # OutPortProvider supports "pull" dataflow type
    if len(provider_types) > 0:
      self._rtcout.RTC_DEBUG("dataflow_type pull is supported")
      self.appendProperty("dataport.dataflow_type", "push")
      self.appendProperty("dataport.interface_type",
                          OpenRTM_aist.flatten(provider_types))

    self._providerTypes = provider_types


  ##
  # @if jp
  # @brief InPort consumer の初期化
  # @else
  # @brief InPort consumer initialization
  # @endif
  #
  # void OutPortBase::initConsumers()
  def initConsumers(self):
    self._rtcout.RTC_TRACE("initConsumers()")

    # create InPort consumers
    factory = OpenRTM_aist.InPortConsumerFactory.instance()
    consumer_types = factory.getIdentifiers()
    self._rtcout.RTC_PARANOID("available InPortConsumer: %s",
                              OpenRTM_aist.flatten(consumer_types))

    if self._properties.hasKey("consumer_types") and \
          OpenRTM_aist.normalize(self._properties.getProperty("consumer_types")) != "all":
      self._rtcout.RTC_DEBUG("allowed consumers: %s",
                             self._properties.getProperty("consumer_types"))

      temp_types = consumer_types
      consumer_types = []
      active_types = OpenRTM_aist.split(self._properties.getProperty("consumer_types"), ",")

      temp_types.sort()
      active_types.sort()
      set_intersection = lambda a, b: [x for x in a if x in b]
      consumer_types = consumer_types + set_intersection(temp_types, active_types)

    # InPortConsumer supports "push" dataflow type
    if len(consumer_types) > 0:
      self._rtcout.RTC_PARANOID("dataflow_type push is supported")
      self.appendProperty("dataport.dataflow_type", "push")
      self.appendProperty("dataport.interface_type",
                          OpenRTM_aist.flatten(consumer_types))
    
    self._consumerTypes = consumer_types


  ##
  # @if jp
  # @brief OutPort provider の生成
  # @else
  # @brief OutPort provider creation
  # @endif
  #
  # OutPortProvider*
  # OutPortBase::createProvider(ConnectorProfile& cprof, coil::Properties& prop)
  def createProvider(self, cprof, prop):
    if prop.getProperty("interface_type") and \
          not OpenRTM_aist.includes(self._providerTypes, prop.getProperty("interface_type")):
      self._rtcout.RTC_ERROR("no provider found")
      self._rtcout.RTC_DEBUG("interface_type:  %s", prop.getProperty("interface_type"))
      self._rtcout.RTC_DEBUG("interface_types: %s",
                             OpenRTM_aist.flatten(self._providerTypes))
      return 0

    self._rtcout.RTC_DEBUG("interface_type: %s", prop.getProperty("interface_type"))
    provider = OpenRTM_aist.OutPortProviderFactory.instance().createObject(prop.getProperty("interface_type"))
    
    if provider != 0:
      self._rtcout.RTC_DEBUG("provider created")
      provider.init(prop.getNode("provider"))

      if not provider.publishInterface(cprof.properties):
        self._rtcout.RTC_ERROR("publishing interface information error")
        OpenRTM_aist.OutPortProviderFactory.instance().deleteObject(provider)
        return 0

      return provider

    self._rtcout.RTC_ERROR("provider creation failed")
    return 0


  ##
  # @if jp
  # @brief InPort consumer の生成
  # @else
  # @brief InPort consumer creation
  # @endif
  #
  # InPortConsumer* OutPortBase::createConsumer(const ConnectorProfile& cprof,
  #                                             coil::Properties& prop)
  def createConsumer(self, cprof, prop):
    if prop.getProperty("interface_type") and \
          not self._consumerTypes.count(prop.getProperty("interface_type")):
      self._rtcout.RTC_ERROR("no consumer found")
      self._rtcout.RTC_DEBUG("interface_type:  %s", prop.getProperty("interface_type"))
      self._rtcout.RTC_DEBUG("interface_types: %s",
                             OpenRTM_aist.flatten(self._consumerTypes))
      return 0
    
    self._rtcout.RTC_DEBUG("interface_type: %s", prop.getProperty("interface_type"))
    consumer = OpenRTM_aist.InPortConsumerFactory.instance().createObject(prop.getProperty("interface_type"))
    
    if consumer != 0:
      self._rtcout.RTC_DEBUG("consumer created")
      consumer.init(prop.getNode("consumer"))

      if not consumer.subscribeInterface(cprof.properties):
        self._rtcout.RTC_ERROR("interface subscription failed.")
        OpenRTM_aist.InPortConsumerFactory.instance().deleteObject(consumer)
        return 0

      return consumer

    self._rtcout.RTC_ERROR("consumer creation failed")
    return 0


  ##
  # @if jp
  # @brief OutPortPushConnector の生成
  # @else
  # @brief OutPortPushConnector creation
  # @endif
  #
  # OutPortConnector*
  # OutPortBase::createConnector(const ConnectorProfile& cprof,
  #                              coil::Properties& prop,
  #                              InPortConsumer* consumer)
  def createConnector(self, cprof, prop, provider_ = None, consumer_ = None):
    profile = OpenRTM_aist.ConnectorBase.Profile(cprof.name,
                                                 cprof.connector_id,
                                                 OpenRTM_aist.CORBA_SeqUtil.refToVstring(cprof.ports),
                                                 prop)

    connector = None
    try:

      if consumer_ is not None:
        connector = OpenRTM_aist.OutPortPushConnector(profile, consumer_)
      elif provider_ is not None:
        connector = OpenRTM_aist.OutPortPullConnector(profile, provider_)

      else:
        self._rtcout.RTC_ERROR("provider or consumer is not passed. returned 0;")
        return 0

      if connector is None:
        self._rtcout.RTC_ERROR("old compiler? new returned 0;")
        return 0

      self._rtcout.RTC_TRACE("OutPortPushConnector created")

      guard = OpenRTM_aist.ScopedLock(self._connector_mutex)
      self._connectors.append(connector)
      self._rtcout.RTC_PARANOID("connector push backed: %d", len(self._connectors))
      return connector

    except:
      self._rtcout.RTC_ERROR("OutPortPushConnector creation failed")
      return 0


    self._rtcout.RTC_FATAL("never comes here: createConnector()")
    return 0
