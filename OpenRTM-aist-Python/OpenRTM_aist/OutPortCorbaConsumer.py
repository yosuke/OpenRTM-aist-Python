#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file  OutPortCorbaConsumer.py
# @brief OutPortCorbaConsumer class
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
 
from omniORB import any
from omniORB import CORBA

import OpenRTM_aist
import RTC, RTC__POA 



##
# @if jp
# @class OutPortCorbaConsumer
#
# @brief OutPortCorbaConsumer クラス
#
# 通信手段に CORBA を利用した出力ポートコンシューマの実装クラス。
#
# @since 0.4.0
#
# @else
# @class OutPortCorbaConsumer
# @brief OutPortCorbaConsumer class
# @endif
class OutPortCorbaConsumer(OpenRTM_aist.OutPortConsumer,OpenRTM_aist.CorbaConsumer):
  """
  """



  ##
  # @if jp
  # @brief コンストラクタ
  #
  # コンストラクタ
  #
  # @param self
  # @param buffer_ 本ポートに割り当てるバッファ
  #
  # @else
  # @brief Constructor
  # @endif
  def __init__(self, buffer_):
    self._buffer = buffer_
    OpenRTM_aist.CorbaConsumer.__init__(self)


  ##
  # @if jp
  # @brief データを読み出す
  #
  # 設定されたデータを読み出す。
  #
  # @param self
  # @param data 読み出したデータを受け取るオブジェクト
  #
  # @return データ読み出し処理結果(読み出し成功:true、読み出し失敗:false)
  #
  # @else
  #
  # @endif
  def get(self, data):
    try:
      obj = self._ptr()._narrow(RTC.OutPortAny)
      if CORBA.is_nil(obj):
        return False
      data[0] = any.from_any(obj.get(), keep_structs=True)
      return True
    except:
      return False
    
    return False


  ##
  # @if jp
  # @brief ポートからデータを受信する
  #
  # 接続先のポートからデータを受信する。
  # 受信したデータは内部に設定されたバッファに書き込まれる。
  #
  # @param self
  #
  # @else
  #
  # @endif
  def pull(self):
    data = [None]
    if self.get(data):
      self._buffer.write(data[0])


  ##
  # @if jp
  # @brief データ受信通知への登録
  #
  # 指定されたプロパティに基づいて、データ受信通知の受け取りに登録する。
  #
  # @param self
  # @param properties 登録情報
  #
  # @return 登録処理結果(登録成功:true、登録失敗:false)
  #
  # @else
  #
  # @endif
  def subscribeInterface(self, properties):
    index = OpenRTM_aist.NVUtil.find_index(properties,
                                           "dataport.corba_any.outport_ref")
    if index < 0:
      return False

    if OpenRTM_aist.NVUtil.isString(properties,
                                    "dataport.corba_any.outport_ref"):

      try:
        ior = any.from_any(properties[index].value, keep_structs=True)
        print "OutPort ref: ", ior
        orb = OpenRTM_aist.Manager.instance().getORB()
        obj = orb.string_to_object(ior)
        self.setObject(obj)
        return True
      except:
        return False

    return False


  ##
  # @if jp
  # @brief データ受信通知からの登録解除
  #
  # データ受信通知の受け取りから登録を解除する。
  #
  # @param self
  # @param properties 登録解除情報
  #
  # @else
  #
  # @endif
  def unsubscribeInterface(self, properties):
    index = OpenRTM_aist.NVUtil.find_index(properties,
                                           "dataport.corba_any.outport_ref")
    if index < 0:
      return

    try:
      ior = any.from_any(properties[index].value, keep_structs=True)
      if ior:
        orb = OpenRTM_aist.Manager.instance().getORB()
        obj = orb.string_to_object(ior)
        if self._ptr()._is_equivalent(obj):
          self.releaseObject()

    except:
      return
