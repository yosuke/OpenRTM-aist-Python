#!/usr/bin/env python
# -*- coding: euc-jp -*-


##
# @file  InPortCorbaProvider.py
# @brief InPortCorbaProvider class
# @date  $Date: 2007/09/25 $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006-2008
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.
 

from  omniORB import any
import sys
import traceback

import OpenRTM_aist
import RTC,RTC__POA


##
# @if jp
# @class InPortCorbaProvider
# @brief InPortCorbaProvider クラス
#
# 通信手段に CORBA を利用した入力ポートプロバイダーの実装クラス。
#
# @since 0.4.0
#
# @else
# @class InPortCorbaProvider
# @brief InPortCorbaProvider class
# @endif
class InPortCorbaProvider(OpenRTM_aist.InPortProvider, RTC__POA.InPortAny):
  """
  """



  ##
  # @if jp
  # @brief コンストラクタ
  #
  # コンストラクタ
  # ポートプロパティに以下の項目を設定する。
  #  - インターフェースタイプ : CORBA_Any
  #  - データフロータイプ : Push, Pull
  #  - サブスクリプションタイプ : Any
  #
  # @param self
  # @param buffer_ 当該プロバイダに割り当てるバッファオブジェクト
  #
  # @else
  # @brief Constructor
  # @endif
  def __init__(self, buffer_):
    OpenRTM_aist.InPortProvider.__init__(self)
    self._buffer = buffer_

    # PortProfile setting
    self.setDataType(self._buffer.getPortDataType())
    self.setInterfaceType("CORBA_Any")
    self.setDataFlowType("Push, Pull")
    self.setSubscriptionType("Any")

    # ConnectorProfile setting
    self._objref = self._this()


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
    if not OpenRTM_aist.NVUtil.isStringValue(prop,
                                             "dataport.interface_type",
                                             "CORBA_Any"):
      return

    nv = self._properties
    OpenRTM_aist.CORBA_SeqUtil.push_back(nv,
                                         OpenRTM_aist.NVUtil.newNV("dataport.corba_any.inport_ref",
                                                                   self._objref))
    OpenRTM_aist.NVUtil.append(prop, nv)


  ##
  # @if jp
  # @brief バッファにデータを書き込む
  #
  # 設定されたバッファにデータを書き込む。
  #
  # @param self
  # @param data 書込対象データ
  #
  # @else
  #
  # @endif
  def put(self, data):
    try:
      tmp = any.from_any(data, keep_structs=True)
      self._buffer.write(tmp)
    except:
      traceback.print_exception(*sys.exc_info())
      return

    return
