#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file InPortPullConnector.py
# @brief InPortPull type connector class
# @date $Date$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2009
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.
#

from omniORB import *
from omniORB import any

import OpenRTM_aist


##
# @if jp
# @class InPortPullConnector
# @brief InPortPullConnector 基底クラス
#
# InPort の Push 型データフローのための Connector
#
# @since 1.0.0
#
# @else
# @class InPortPullConnector
# @brief InPortPullConnector base class
#
# A connector class for pull type dataflow of InPort
#
# @since 1.0.0
#
# @endif
class InPortPullConnector(OpenRTM_aist.InPortConnector):
    
  ##
  # @if jp
  # @brief コンストラクタ
  # @else
  # @brief Constructor
  # @endif
  #
  # InPortPullConnector(ConnectorInfo info,
  #                     OutPortConsumer* consumer,
  #                     ConnectorListeners& listeners,
  #                     CdrBufferBase* buffer = 0);
  def __init__(self, info, consumer, listeners, buffer = 0):
    OpenRTM_aist.InPortConnector.__init__(self, info, buffer)
    self._consumer = consumer
    self._listeners = listeners
    if buffer == 0:
      self._buffer = self.createBuffer(self._profile)

    if self._buffer == 0 or not self._consumer:
      raise
        
    self._buffer.init(info.properties.getNode("buffer"))
    self._consumer.setBuffer(self._buffer)
    self._consumer.setListener(info, self._listeners)
    self.onConnect()
    return


  ##
  # @if jp
  # @brief デストラクタ
  # @else
  # @brief Destructor
  # @endif
  #
  def __del__(self):
    self.onDisconnect()
    self.disconnect()
    return


  ##
  # @if jp
  # @brief read 関数
  #
  # Buffer からデータを InPort へ read する関数
  #
  # @else
  # @brief Destructor
  #
  # The read function to read data from buffer to InPort
  #
  # @endif
  #
  # virtual ReturnCode read(cdrMemoryStream& data);
  def read(self, data):
    self._rtcout.RTC_TRACE("InPortPullConnector.read()")
    if not self._consumer:
      return self.PORT_ERROR

    cdr_data = [None]
    ret = self._consumer.get(cdr_data)

    _data = None
    # CDR -> (conversion) -> data
    if self._endian is not None:
      _data = cdrUnmarshal(any.to_any(data[0]).typecode(),cdr_data[0],self._endian)

    else:
      self._rtcout.RTC_ERROR("unknown endian from connector")
      return OpenRTM_aist.BufferStatus.PRECONDITION_NOT_MET
    
    return ret


  ##
  # @if jp
  # @brief 接続解除関数
  #
  # Connector が保持している接続を解除する
  #
  # @else
  # @brief Disconnect connection
  #
  # This operation disconnect this connection
  #
  # @endif
  #
  # virtual ReturnCode disconnect();
  def disconnect(self):
    return self.PORT_OK
        

  ## virtual void activate(){}; // do nothing
  def activate(self): # do nothing
    pass

  ## virtual void deactivate(){}; // do nothing
  def deactivate(self): # do nothing
    pass

  ## CdrBufferBase* createBuffer(Profile& profile);
  def createBuffer(self, profile):
    buf_type = profile.properties.getProperty("buffer_type","ring_buffer")
    return OpenRTM_aist.CdrBufferFactory.instance().createObject(buf_type)
    
  ##
  # @if jp
  # @brief 接続確立時にコールバックを呼ぶ
  # @else
  # @brief Invoke callback when connection is established
  # @endif
  # void onConnect()
  def onConnect(self):
    self._listeners.connector_[OpenRTM_aist.ConnectorListenerType.ON_CONNECT].notify(self._profile)
    return

  ##
  # @if jp
  # @brief 接続切断時にコールバックを呼ぶ
  # @else
  # @brief Invoke callback when connection is destroied
  # @endif
  # void onDisconnect()
  def onDisconnect(self):
    self._listeners.connector_[OpenRTM_aist.ConnectorListenerType.ON_DISCONNECT].notify(self._profile)
    return
