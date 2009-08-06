#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file  PublisherFlush.py
# @brief PublisherFlush class
# @date  $Date: 2007/09/06$
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


##
# @if jp
# @class PublisherFlush
# @brief PublisherFlush クラス
#
# Flush 型 Publisher クラス
# バッファ内に格納されている未送信データを送信する。
# データ送出を待つコンシューマを、送出する側と同じスレッドで動作させる。
#
# @else
# @class PublisherFlush
# @brief PublisherFlush class
# @endif
class PublisherFlush(OpenRTM_aist.PublisherBase):
  """
  """



  ##
  # @if jp
  # @brief コンストラクタ
  #
  # コンストラクタ
  #
  # @param self
  # @param consumer データ送出を待つコンシューマ
  # @param property 本Publisherの駆動制御情報を設定したPropertyオブジェクト
  #
  # @else
  # @brief Constructor
  # @endif
  def __init__(self):
    self._consumer = None
    self._active   = False


  ##
  # @if jp
  # @brief デストラクタ
  #
  # デストラクタ
  # 当該Publisherを破棄する際に、PublisherFactoryにより呼び出される。
  #
  # @param self
  #
  # @else
  # @brief Destructor
  # @endif
  def __del__(self):
    # "consumer" should be deleted in the Connector
    self._consumer = None


  ##
  # @if jp
  # @brief 初期化
  # @else
  # @brief initialization
  # @endif
  # PublisherBase::ReturnCode PublisherFlush::init(coil::Properties& prop)
  def init(self, prop):
    return OpenRTM_aist.DataPortStatus.PORT_OK;


  ##
  # @if jp
  # @brief InPortコンシューマのセット
  # @else
  # @brief Store InPort consumer
  # @endif
  # PublisherBase::ReturnCode
  # PublisherFlush::setConsumer(InPortConsumer* consumer)
  def setConsumer(self, consumer):
    if not consumer:
      return OpenRTM_aist.DataPortStatus.INVALID_ARGS

    self._consumer = consumer

    return OpenRTM_aist.DataPortStatus.PORT_OK


  ##
  # @if jp
  # @brief バッファのセット
  # @else
  # @brief Setting buffer pointer
  # @endif
  # PublisherBase::ReturnCode PublisherFlush::setBuffer(CdrBufferBase* buffer)
  def setBuffer(self, buffer):
    return OpenRTM_aist.DataPortStatus.PORT_ERROR


  ## PublisherBase::ReturnCode PublisherFlush::write(const cdrMemoryStream& data,
  ##                                                 unsigned long sec,
  ##                                                 unsigned long usec)
  def write(self, data, sec, usec):
    if not self._consumer:
      return OpenRTM_aist.DataPortStatus.PRECONDITION_NOT_MET
    return self._consumer.put(data)


  ## bool PublisherFlush::isActive()
  def isActive(self):
    return self._active


  ## PublisherBase::ReturnCode PublisherFlush::activate()
  def activate(self):
    if self._active:
      return OpenRTM_aist.DataPortStatus.PRECONDITION_NOT_MET

    self._active = True

    return OpenRTM_aist.DataPortStatus.PORT_OK


  ## PublisherBase::ReturnCode PublisherFlush::deactivate()
  def deactivate(self):
    if not self._active:
      return OpenRTM_aist.DataPortStatus.PRECONDITION_NOT_MET

    self._active = False

    return OpenRTM_aist.DataPortStatus.PORT_OK

  

def PublisherFlushInit():
  OpenRTM_aist.PublisherFactory.instance().addFactory("flush",
                                                      OpenRTM_aist.PublisherFlush,
                                                      OpenRTM_aist.Delete)
