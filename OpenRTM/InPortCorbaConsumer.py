#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file  InPortCorbaConsumer.py
# @brief InPortCorbaConsumer class
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


from omniORB import CORBA
from omniORB import any
import sys
import traceback

import RTC, RTC__POA
import OpenRTM


##
# @if jp
#
# @class InPortCorbaConsumer
#
# @brief InPortCorbaConsumer クラス
#
# 通信手段に CORBA を利用した入力ポートコンシューマの実装クラス。
#
# @param DataType 本ポートにて扱うデータ型
#
# @since 0.4.0
#
# @else
# @class InPortCorbaConsumer
# @brief InPortCorbaConsumer class
# @endif
class InPortCorbaConsumer(OpenRTM.InPortConsumer,OpenRTM.CorbaConsumer):
  """
  """



  ##
  # @if jp
  # @brief コンストラクタ
  #
  # コンストラクタ
  #
  # @param self
  # @param buffer_ 当該コンシューマに割り当てるバッファオブジェクト
  # @param consumer Consumer オブジェクト(デフォルト値:None)
  #
  # @else
  # @brief Constructor
  # @endif
  def __init__(self, buffer_, consumer=None):
    if consumer:
      OpenRTM.CorbaConsumer.__init__(self, consumer=consumer)
      self._buffer = consumer._buffer
      return
    
    OpenRTM.CorbaConsumer.__init__(self)
    self._buffer = buffer_


  ##
  # @if jp
  # @brief 代入演算子
  #
  # 代入演算子
  #
  # @param self
  # @param consumer 代入元 InPortCorbaConsumer オブジェクト
  #
  # @return 代入結果
  #
  # @else
  #
  # @endif
  def equal_operator(self, consumer):
    if self == consumer:
      return self

    self._buffer = consumer._buffer


  ##
  # @if jp
  # @brief バッファへのデータ書込
  #
  # バッファにデータを書き込む
  #
  # @param self
  # @param data 書込対象データ
  #
  # @else
  #
  # @endif
  def put(self, data):
    tmp = any.to_any(data)
    obj = self._ptr()._narrow(RTC.InPortAny)
    obj.put(tmp)


  ##
  # @if jp
  # @brief バッファからのデータ取出
  #
  # バッファからデータを取り出して送出する。
  #
  # @param self
  #
  # @else
  #
  # @endif
  def push(self):
    data = [None]
    self._buffer.read(data)
    tmp = any.to_any(data[0])

    if not self._ptr():
      return

    obj = self._ptr()._narrow(RTC.InPortAny)

    # 本当はエラー処理をすべき
    if CORBA.is_nil(obj):
      return
    try:
      obj.put(tmp)
    except:
      # オブジェクトが無効になったらdisconnectすべき
      traceback.print_exception(*sys.exec_info())
      return


  ##
  # @if jp
  # @brief コピーの生成
  #
  # 当該InPortCorbaConsumerオブジェクトの複製を生成する。
  #
  # @param self
  #
  # @return コピーされたInPortCorbaConsumerオブジェクト
  #
  # @else
  #
  # @endif
  def clone(self):
    return OpenRTM.InPortCorbaConsumer(self, consumer=self)


  ##
  # @if jp
  # @brief データ送信通知への登録
  #
  # 指定されたプロパティに基づいて、データ送出通知の受け取りに登録する。
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
    if not OpenRTM.NVUtil.isStringValue(properties,
                      "dataport.dataflow_type",
                      "Push"):
      return False

    index = OpenRTM.NVUtil.find_index(properties,
                      "dataport.corba_any.inport_ref")

    if index < 0:
      return False

    obj = None
    try:
      obj = any.from_any(properties[index].value,keep_structs=True)
    except:
      return False

    if not CORBA.is_nil(obj):
      self.setObject(obj)
      return True

    return False


  ##
  # @if jp
  # @brief データ送信通知からの登録解除(サブクラス実装用)
  #
  # データ送出通知の受け取りから登録を解除する。<BR>
  # ※サブクラスでの実装参照用
  #
  # @param self
  # @param properties 登録解除情報
  #
  # @else
  #
  # @endif
  def unsubscribeInterface(self, properties):
    pass
