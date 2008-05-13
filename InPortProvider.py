#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file  InPortProvider.py
# @brief InPortProvider class
# @date  $Date: 2007/09/20 $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006-2008
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.


import OpenRTM
import SDOPackage, SDOPackage__POA


##
# @if jp
# @class InPortProvider
# @brief InPortProvider クラス
#
# InPortの情報を保持するためのクラス。
#
# @since 0.4.0
#
# @else
# @class InPortProvider
# @brief InPortProvider class
# @endif
class InPortProvider:
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
    self._dataType = ""
    self._interfaceType = ""
    self._dataflowType = ""
    self._subscriptionType = ""


  ##
  # @if jp
  # @brief InterfaceProfile情報を公開する
  #
  # InterfaceProfile情報を公開する。
  #
  # @param self
  # @param prop InterfaceProfile情報を受け取るプロパティ
  #
  # @else
  #
  # @endif
  def publishInterfaceProfile(self, prop):
    OpenRTM.NVUtil.appendStringValue(prop, "dataport.data_type",
             self._dataType)
    OpenRTM.NVUtil.appendStringValue(prop, "dataport.interface_type",
             self._interfaceType)
    OpenRTM.NVUtil.appendStringValue(prop, "dataport.dataflow_type",
             self._dataflowType)
    OpenRTM.NVUtil.appendStringValue(prop, "dataport.subscription_type",
             self._subscriptionType)


  ##
  # @if jp
  # @brief Interface情報を公開する
  #
  # Interface情報を公開する。
  #
  # @param self
  # @param prop Interface情報を受け取るプロパティ
  #
  # @else
  #
  # @endif
  def publishInterface(self, prop):
    if not OpenRTM.NVUtil.isStringValue(prop,
                "dataport.interface_type",
                self._interfaceType):
      return

    OpenRTM.NVUtil.append(prop, self._properties)


  ##
  # @if jp
  # @brief データタイプを設定する
  #
  # データタイプを設定する。
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
  # @brief インタフェースタイプを設定する
  #
  # インタフェースタイプを設定する。
  #
  # @param self
  # @param interface_type 設定対象インタフェースタイプ
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
  # データフロータイプを設定する。
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
  # サブスクリプションタイプを設定する。
  #
  # @param self
  # @param subs_type 設定対象サブスクリプションタイプ
  #
  # @else
  #
  # @endif
  def setSubscriptionType(self, subs_type):
    self._subscriptionType = subs_type
