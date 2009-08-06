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


from omniORB import *
from omniORB import CORBA
from omniORB import any
import sys
import traceback

import RTC, RTC__POA
import OpenRTM_aist
import OpenRTM, OpenRTM__POA


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
class InPortCorbaConsumer(OpenRTM_aist.InPortConsumer,OpenRTM_aist.CorbaConsumer):
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
    self._rtcout = OpenRTM_aist.Manager.instance().getLogbuf("InPortCorbaConsumer")

    if consumer:
      OpenRTM_aist.CorbaConsumer.__init__(self, consumer=consumer)
      self._buffer = consumer._buffer
      return
    
    OpenRTM_aist.CorbaConsumer.__init__(self)
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
    self._rtcout.RTC_PARANOID("put()")
    obj = self._ptr()._narrow(OpenRTM.InPortCdr)
    obj.put(data)


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
    self._rtcout.RTC_PARANOID("push()")
    data = [None]
    self._buffer.read(data)

    if not self._ptr():
      return

    obj = self._ptr()._narrow(OpenRTM.InPortCdr)

    # 本当はエラー処理をすべき
    if CORBA.is_nil(obj):
      return
    try:
      obj.put(data[0])
    except:
      self._rtcout.RTC_INFO("exception while invoking _ptr().put()")
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
    self._rtcout.RTC_TRACE("clone()")
    return OpenRTM_aist.InPortCorbaConsumer(self, consumer=self)


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
    self._rtcout.RTC_TRACE("subscribeInterface()")

    if self.subscribeFromIor(properties):
      return True

    if self.subscribeFromRef(properties):
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
    self._rtcout.RTC_TRACE("unsubscribeInterface()")

    if self.unsubscribeFromIor(properties):
      return

    self.unsubscribeFromRef(properties)



  ##
  # @if jp
  # @brief IOR文字列からオブジェクト参照を取得する
  #
  # @return true: 正常取得, false: 取得失敗
  #
  # @else
  # @brief Getting object reference fromn IOR string
  #
  # @return true: succeeded, false: failed
  #
  # @endif
  #
  # bool subscribeFromIor(const SDOPackage::NVList& properties)
  def subscribeFromIor(self, properties):
    self.RTC_TRACE("subscribeFromIor()")
    
    index = OpenRTM_aist.NVUtil.find_index(properties,
                                           "dataport.corba_any.inport_ior")
    if index < 0:
      self._rtcout.RTC_ERROR("inport_ior not found")
      return False

    ior = any.from_any(properties[index].value, keep_structs=True)
    if not ior:
      self._rtcout.RTC_ERROR("inport_ior has no string")
      return False


    orb = OpenRTM_aist.Manager.instance().getORB()
    obj = orb.string_to_object(ior)
      
    if CORBA.is_nil(obj):
      self._rtcout.RTC_ERROR("invalid IOR string has been passed")
      return False

    if not self.setObject(obj):
      self._rtcout.RTC_WARN("Setting object to consumer failed.")
      return False

    return True


  ##
  # @if jp
  # @brief Anyから直接オブジェクト参照を取得する
  #
  # @return true: 正常取得, false: 取得失敗
  #
  # @else
  # @brief Getting object reference fromn Any directry
  #
  # @return true: succeeded, false: failed
  #
  # @endif
  #
  #bool subscribeFromRef(const SDOPackage::NVList& properties)
  def subscribeFromRef(self, properties):
    self._rtcout.RTC_TRACE("subscribeFromRef()")
    index = OpenRTM_aist.NVUtil.find_index(properties,
                                           "dataport.corba_any.inport_ref")
    if index < 0:
      self._rtcout.RTC_ERROR("inport_ref not found")
      return False


    obj = any.from_any(properties[index].value, keep_structs=True)
    if not obj:
      self._rtcout.RTC_ERROR("prop[inport_ref] is not objref")
      return True

    if CORBA.is_nil(obj):
      self._rtcout.RTC_ERROR("prop[inport_ref] is not objref")
      return False
      
    if not self.setObject(obj):
      self._rtcout.RTC_ERROR("Setting object to consumer failed.")
      return False

    return True


  ##
  # @if jp
  # @brief 接続解除(IOR版)
  #
  # @return true: 正常取得, false: 取得失敗
  #
  # @else
  # @brief ubsubscribing (IOR version)
  #
  # @return true: succeeded, false: failed
  #
  # @endif
  #
  # bool unsubscribeFromIor(const SDOPackage::NVList& properties)
  def unsubscribeFromIor(self, properties):
    self._rtcout.RTC_TRACE("unsubscribeFromIor()")
    index = OpenRTM_aist.NVUtil.find_index(properties,
                                           "dataport.corba_any.inport_ior")
    if index < 0:
      self._rtcout.RTC_ERROR("inport_ior not found")
      return False

    ior = any.from_any(properties[index].value, keep_structs=True)
    if not ior:
      self._rtcout.RTC_ERROR("prop[inport_ior] is not string")
      return False


    orb = OpenRTM_aist.Manager.instance().getORB()
    var = orb.string_to_object(ior)
    
    if not self._ptr()._is_equivalent(var):
      self._rtcout.RTC_ERROR("connector property inconsistency")
      return False

    self.releaseObject()
    return True


  ##
  # @if jp
  # @brief 接続解除(Object reference版)
  #
  # @return true: 正常取得, false: 取得失敗
  #
  # @else
  # @brief ubsubscribing (Object reference version)
  #
  # @return true: succeeded, false: failed
  #
  # @endif
  #
  # bool unsubscribeFromRef(const SDOPackage::NVList& properties)
  def unsubscribeFromRef(self, properties):
    self._rtcout.RTC_TRACE("unsubscribeFromRef()")
    index = OpenRTM_aist.NVUtil.find_index(properties,
                                           "dataport.corba_any.inport_ref")
    if index < 0:
      return False

    obj = any.from_any(properties[index].value, keep_structs=True)
    if not obj:
      return False

    if not self._ptr()._is_equivalent(obj):
      return False

    self.releaseObject()
    return True
