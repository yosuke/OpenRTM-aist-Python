#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file DataOutPort.py
# @brief Base class of OutPort
# @date $Date: 2007/09/20 $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
# 
# Copyright (C) 2006-2008
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.


import OpenRTM_aist
import RTC, RTC__POA


##
# @if jp
# @class DataOutPort
# @brief Outort 用 Port
#
# データ出力ポートの実装クラス。
#
# @since 0.4.0
#
# @else
# @class DataOutPort
# @brief OutPort abstruct class
# @endif
class DataOutPort(OpenRTM_aist.PortBase):
  """
  """



  ##
  # @if jp
  # @brief コンストラクタ
  #
  # コンストラクタ
  #
  # @param self
  # @param name ポート名称
  # @param outport 当該データ出力ポートに関連付けるOutPortオブジェクト
  #
  # @else
  # @brief Constructor
  # @endif
  def __init__(self, name, outport, prop):
    OpenRTM_aist.PortBase.__init__(self, name)
    self._outport = outport
    # PortProfile::properties を設定
    self.addProperty("port.port_type", "DataOutPort")
    self._providers = []
    self._providers.append(OpenRTM_aist.OutPortCorbaProvider(outport))
    self._providers[-1].publishInterfaceProfile(self._profile.properties)
    self._consumers = []
    self._consumers.append(OpenRTM_aist.InPortCorbaConsumer(outport))
    self._pf = OpenRTM_aist.PublisherFactory()


  ##
  # @if jp
  #
  # @brief Interface 情報を公開する
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
  # このオペレーションは、新規の connector_id に対しては接続の生成、
  # 既存の connector_id に対しては更新が適切に行われる必要がある。
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
  # This operation should create the new connection for the new
  # connector_id, and should update the connection for the existing
  # connection_id.
  #
  # @param connector_profile The connection profile information
  #
  # @return The return code of ReturnCode_t type.
  #
  # @endif
  def publishInterfaces(self, connector_profile):
    for provider in self._providers:
      provider.publishInterface(connector_profile.properties)
    return RTC.RTC_OK


  ##
  # @if jp
  #
  # @brief Interface に接続する
  #
  # このオペレーションは、notify_connect() 処理シーケンスの中間にコール
  # される関数である。
  # notify_connect() では、
  #
  # - publishInterfaces()
  # - connectNext()
  # - subscribeInterfaces()
  # - updateConnectorProfile()
  #
  # の順に protected 関数がコールされ接続処理が行われる。
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
  # - publishInterfaces()
  # - connectNext()
  # - subscribeInterfaces()
  # - updateConnectorProfile()
  #
  # @param connector_profile The connection profile information
  #
  # @return The return code of ReturnCode_t type.
  #
  # @endif
  def subscribeInterfaces(self, connector_profile):
    subscribe = self.subscribe(prof=connector_profile)
    for consumer in self._consumers:
      subscribe(consumer)

    if not subscribe._consumer:
      return RTC.RTC_OK

    
    # Publisherを生成
    prop = OpenRTM_aist.NVUtil.toProperties(connector_profile.properties)
    publisher = self._pf.create(subscribe._consumer.clone(), prop)

    # PublisherをOutPortにアタッチ
    self._outport.attach(connector_profile.connector_id, publisher)
    # self._outport.onConnect(connector_profile.connector_id, publisher)

    return RTC.RTC_OK


  ##
  # @if jp
  #
  # @brief Interface の接続を解除する
  #
  # このオペレーションは、notify_disconnect() 処理シーケンスの終わりにコール
  # される関数である。
  # notify_disconnect() では、
  # - disconnectNext()
  # - unsubscribeInterfaces()
  # - eraseConnectorProfile()
  # の順に protected 関数がコールされ接続解除処理が行われる。
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
  # - disconnectNext()
  # - unsubscribeInterfaces()
  # - eraseConnectorProfile() 
  #
  # @param connector_profile The connection profile information
  #
  # @endif
  def unsubscribeInterfaces(self, connector_profile):
    publisher = self._outport.detach(connector_profile.connector_id)
    self._pf.destroy(publisher)
    self._outport.onDisconnect(connector_profile.connector_id)
    return



  ##
  # @if jp
  # @brief Interface接続用Functor
  #
  # Interface接続処理を実行するためのFunctor。
  # @else
  #
  # @endif
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
       \param cons(OpenRTM_aist.InPortConsumer)
      """
      if cons.subscribeInterface(self._prof.properties):
        self._consumer = cons
