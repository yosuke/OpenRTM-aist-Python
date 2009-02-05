#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file  OutPortProvider.py
# @brief OutPortProvider class
# @date  $Date: 2007/09/05$
# @author Noriaki Ando <n-ando@aist.go.jp>
#
# Copyright (C) 2006-2008
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.



import OpenRTM_aist

##
# @if jp
#
# @class OutPortProvider
# @brief OutPortProvider
#
# - Port に対して何を提供しているかを宣言する。
#   PortProfile の properties に Provider に関する情報を追加する。
#
# (例) OutPort を Provide する場合
#
# OutPortCorbaProvider が以下を宣言
#  - dataport.interface_type = CORBA_Any
#  - dataport.dataflow_type = Push, Pull
#  - dataport.subscription_type = Once, New, Periodic
# 
# @since 0.4.0
#
# @else
#
#
# @endif
class OutPortProvider:
  """
  """



  ##
  # @if jp
  # @brief コンストラクタ
  #
  # コンストラクタ
  #
  # @param self
  #
  # @else
  # @brief Constructor
  # @endif
  def __init__(self):
    self._properties = []


  ##
  # @if jp
  # @brief InterfaceProfile情報を公開する
  #
  # InterfaceProfile情報を公開する。
  # 引数で指定するプロパティ情報内の NameValue オブジェクトの
  # dataport.interface_type 値を調べ、当該ポートに設定されている
  # インターフェースタイプと一致する場合のみ情報を取得する。
  #
  # @param self
  # @param prop InterfaceProfile情報を受け取るプロパティ
  #
  # @else
  #
  # @endif
  def publishInterfaceProfile(self, prop):
    OpenRTM_aist.NVUtil.appendStringValue(prop, "dataport.data_type", self._dataType)
    OpenRTM_aist.NVUtil.appendStringValue(prop, "dataport.interface_type", self._interfaceType)
    OpenRTM_aist.NVUtil.appendStringValue(prop, "dataport.dataflow_type", self._dataflowType)
    OpenRTM_aist.NVUtil.appendStringValue(prop, "dataport.subscription_type", self._subscriptionType)


  ##
  # @if jp
  # @brief Interface情報を公開する
  #
  # Interface情報を公開する。
  # 引数で指定するプロパティ情報内の NameValue オブジェクトの
  # dataport.interface_type 値を調べ、当該ポートに設定されていなければ
  # NameValue に情報を追加する。
  # すでに同一インターフェースが登録済みの場合は何も行わない。
  #
  # @param self
  # @param prop InterfaceProfile情報を受け取るプロパティ
  #
  # @else
  #
  # @endif
  def publishInterface(self, prop):
    if not OpenRTM_aist.NVUtil.isStringValue(prop,"dataport.interface_type",self._interfaceType):
      return

    OpenRTM_aist.NVUtil.append(prop,self._properties)


  ##
  # @if jp
  # @brief ポートタイプを設定する
  #
  # 引数で指定したポートタイプを設定する。
  #
  # @param self
  # @param port_type 設定対象ポートタイプ
  #
  # @else
  #
  # @endif
  def setPortType(self, port_type):
    self._portType = port_type


  ##
  # @if jp
  # @brief データタイプを設定する
  #
  # 引数で指定したデータタイプを設定する。
  #
  # @param self
  # @param data_type 設定対象データタイプ
  #
  # @else
  #
  # @endif
  def setDataType(self, data_type):
    self._dataType = data_type


  ##
  # @if jp
  # @brief インターフェースタイプを設定する
  #
  # 引数で指定したインターフェースタイプを設定する。
  #
  # @param self
  # @param interface_type 設定対象インターフェースタイプ
  #
  # @else
  #
  # @endif
  def setInterfaceType(self, interface_type):
    self._interfaceType = interface_type


  ##
  # @if jp
  # @brief データフロータイプを設定する
  #
  # 引数で指定したデータフロータイプを設定する。
  #
  # @param self
  # @param dataflow_type 設定対象データフロータイプ
  #
  # @else
  #
  # @endif
  def setDataFlowType(self, dataflow_type):
    self._dataflowType = dataflow_type


  ##
  # @if jp
  # @brief サブスクリプションタイプを設定する
  #
  # 引数で指定したサブスクリプションタイプを設定する。
  #
  # @param self
  # @param subs_type 設定対象サブスクリプションタイプ
  #
  # @else
  #
  # @endif
  def setSubscriptionType(self, subs_type):
    self._subscriptionType = subs_type


