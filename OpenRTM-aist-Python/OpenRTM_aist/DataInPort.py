#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
#  \file DataInPort.py
#  \brief RTC::Port implementation for Data InPort
#  \date $Date: 2007/09/20 $
#  \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
# 
#  Copyright (C) 2006-2008
#      Noriaki Ando
#      Task-intelligence Research Group,
#      Intelligent Systems Research Institute,
#      National Institute of
#          Advanced Industrial Science and Technology (AIST), Japan
#      All rights reserved.


import OpenRTM_aist
import RTC, RTC__POA



##
# @if jp
# @class DataInPort
# @brief InPort 用 Port
#
# データ入力ポートの実装クラス。
#
# @since 0.4.0
#
# @else
# @class DataInPort
# @brief InPort abstruct class
# @endif
class DataInPort(OpenRTM_aist.PortBase):
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
  # @param inport 当該データ入力ポートに関連付けるInPortオブジェクト
  # @param prop   ポート設定用プロパティ
  #
  # @else
  # @brief Constructor
  # @endif
  def __init__(self, name, inport, prop):
    OpenRTM_aist.PortBase.__init__(self, name)

    # PortProfile::properties を設定
    self.addProperty("port.port_type", "DataInPort")
    self._providers = []
    self._providers.append(OpenRTM_aist.InPortCorbaProvider(inport))
    self._providers[-1].publishInterfaceProfile(self._profile.properties)
    self._consumers = []
    self._consumers.append(OpenRTM_aist.OutPortCorbaConsumer(inport))
    # self._dummy = [1]


  ##
  # @if jp
  # @brief Interface情報を公開する
  #
  # Interface情報を公開する。
  # このPortが所有しているプロバイダ(Provider)に関する情報を、
  # ConnectorProfile#propertiesに代入する。
  #
  # @param self
  # @param connector_profile コネクタプロファイル
  #
  # @return ReturnCode_t 型のリターンコード
  #
  # @else
  #
  # @endif
  def publishInterfaces(self, connector_profile):
    #if len(self._dummy) != 1:
    #  print "Memory access violation was detected."
    #  print "dummy.size(): ", len(self._dummy)
    #  print "size() should be 1."

    for provider in self._providers:
      provider.publishInterface(connector_profile.properties)

    return RTC.RTC_OK
      

  ##
  # @if jp
  # @brief Interfaceに接続する
  #
  # Interfaceに接続する。
  # Portが所有するConsumerに適合するProviderに関する情報を 
  # ConnectorProfile#properties から抽出し、
  # ConsumerにCORBAオブジェクト参照を設定する。
  #
  # @param self
  # @param connector_profile コネクタ・プロファイル
  #
  # @return ReturnCode_t 型のリターンコード
  #
  # @else
  #
  # @endif
  def subscribeInterfaces(self, connector_profile):
    for consumer in self._consumers:
      consumer.subscribeInterface(connector_profile.properties)

    return RTC.RTC_OK


  ##
  # @if jp
  # @brief Interfaceへの接続を解除する
  #
  # Interfaceへの接続を解除する。
  # 与えられたConnectorProfileに関連するConsumerに設定された全てのObjectを
  # 解放し接続を解除する。
  #
  # @param self
  # @param connector_profile コネクタ・プロファイル
  #
  # @else
  #
  # @endif
  def unsubscribeInterfaces(self, connector_profile):
    for consumer in self._consumers:
      consumer.unsubscribeInterface(connector_profile.properties)
    
    
