#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file  PublisherNew.py
# @brief PublisherNew class
# @date  $Date: 2007/09/27 $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006-2008
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.
 
import threading

import OpenRTM_aist


##
# @if jp
# @class PublisherNew
# @brief PublisherNew クラス
#
# バッファ内に新規データが格納されたタイミングで、その新規データを送信する。
# データ送出タイミングを待つコンシューマを、送出する側とは異なるスレッドで
# 動作させる場合に使用。
# Publisherの駆動は、データ送出のタイミングになるまでブロックされ、
# 送出タイミングの通知を受けると、即座にコンシューマの送出処理を呼び出す。
#
# @else
# @class PublisherNew
# @brief PublisherNew class
# @endif
class PublisherNew(OpenRTM_aist.PublisherBase):
  """
  """

  # Policy
  ALL  = 0
  FIFO = 1
  SKIP = 2
  NEW  = 3

  ##
  # @if jp
  # @brief コンストラクタ
  #
  # コンストラクタ
  # 本 Publisher 用新規スレッドを生成する。
  #
  # @param self
  # @param consumer データ送出を待つコンシューマ
  # @param property 本Publisherの駆動制御情報を設定したPropertyオブジェクト
  #                 (本Publisherでは未使用)
  # @else
  # @brief Constructor
  # @endif
  def __init__(self):
    self._rtcout = OpenRTM_aist.Manager.instance().getLogbuf("PublisherNew")
    self._consumer = None
    self._buffer   = None
    self._task     = None
    self._retcode  = self.PORT_OK
    self._retmutex = threading.RLock()
    self._pushPolicy = self.NEW
    self._skipn      = 0
    self._active     = False
    self._leftskip   = 0
    self._profile    = None
    self._listeners  = None


  ##
  # @if jp
  # @brief デストラクタ
  #
  # デストラクタ
  #
  # @param self
  #
  # @else
  # @brief Destructor
  #
  # @endif
  def __del__(self):
    self._rtcout.RTC_TRACE("~PublisherNew()")
    if self._task:
      self._task.resume()
      self._task.finalize()

      OpenRTM_aist.PeriodicTaskFactory.instance().deleteObject(self._task)
      self._rtcout.RTC_PARANOID("task deleted.")

    # "consumer" should be deleted in the Connector
    self._consumer = 0
    # "buffer"   should be deleted in the Connector
    self._buffer = 0
    return


  ##
  # @if jp
  # @brief 初期化
  # @else
  # @brief initialization
  # @endif
  # PublisherBase::ReturnCode PublisherNew::init(coil::Properties& prop)
  def init(self, prop):
    self._rtcout.RTC_TRACE("init()")
    
    push_policy = prop.getProperty("publisher.push_policy","new")
    self._rtcout.RTC_DEBUG("push_policy: %s", push_policy)

    skip_count = prop.getProperty("publisher.skip_count","0")
    self._rtcout.RTC_DEBUG("skip_count: %s", skip_count)

    push_policy = OpenRTM_aist.normalize([push_policy])

    if push_policy == "all":
      self._pushPolicy = self.ALL

    elif push_policy == "fifo":
      self._pushPolicy = self.FIFO
    
    elif push_policy == "skip":
      self._pushPolicy = self.SKIP
    
    elif push_policy == "new":
      self._pushPolicy = self.NEW

    else:
      self._rtcout.RTC_ERROR("invalid push_policy value: %s", push_policy)
      self._pushPolicy = self.NEW
  
    skipn = [self._skipn]
    ret = OpenRTM_aist.stringTo(skipn, skip_count)
    if ret:
      self._skipn = skipn[0]
    else:
      self._rtcout.RTC_ERROR("invalid skip_count value: %s", skip_count)
      self._skipn = 0

    if self._skipn < 0:
      self._rtcout.RTC_ERROR("invalid skip_count value: %d", self._skipn)
      self._skipn = 0

    factory = OpenRTM_aist.PeriodicTaskFactory.instance()

    th = factory.getIdentifiers()
    self._rtcout.RTC_DEBUG("available task types: %s", OpenRTM_aist.flatten(th))

    self._task = factory.createObject(prop.getProperty("thread_type", "default"))

    if not self._task:
      self._rtcout.RTC_ERROR("Task creation failed: %s",
                             prop.getProperty("thread_type", "default"))
      return self.INVALID_ARGS

    self._rtcout.RTC_PARANOID("Task creation succeeded.")

    mprop = prop.getNode("measurement")

    # setting task function
    self._task.setTask(self.svc)
    self._task.setPeriod(0.0)
    self._task.executionMeasure(OpenRTM_aist.toBool(mprop.getProperty("exec_time"),
                                                    "enable", "disable", True))
    ecount = [0]
    if OpenRTM_aist.stringTo(ecount, mprop.getProperty("exec_count")):
      self._task.executionMeasureCount(ecount[0])

    self._task.periodicMeasure(OpenRTM_aist.toBool(mprop.getProperty("period_time"),
                                                   "enable", "disable", True))
    pcount = [0]
    if OpenRTM_aist.stringTo(pcount, mprop.getProperty("period_count")):
      self._task.periodicMeasureCount(pcount[0])

    self._task.suspend()
    self._task.activate()
    self._task.suspend()
    return self.PORT_OK

  ##
  # @if jp
  # @brief InPortコンシューマのセット
  # @else
  # @brief Store InPort consumer
  # @endif
  #
  # PublisherBase::ReturnCode PublisherNew::setConsumer(InPortConsumer* consumer)
  def setConsumer(self, consumer):
    self._rtcout.RTC_TRACE("setConsumer()")
    
    if not consumer:
      self._rtcout.RTC_ERROR("setConsumer(consumer = 0): invalid argument.")
      return self.INVALID_ARGS

    self._consumer = consumer
    return self.PORT_OK


  ##
  # @if jp
  # @brief バッファのセット
  # @else
  # @brief Setting buffer pointer
  # @endif
  #
  # PublisherBase::ReturnCode PublisherNew::setBuffer(CdrBufferBase* buffer)
  def setBuffer(self, buffer):
    self._rtcout.RTC_TRACE("setBuffer()")

    if not buffer:
      self._rtcout.RTC_ERROR("setBuffer(buffer == 0): invalid argument")
      return self.INVALID_ARGS

    self._buffer = buffer
    return self.PORT_OK


  ##
  # @if jp
  # @brief リスナのセット
  # @else
  # @brief Setting buffer pointer
  # @endif
  #
  # virtual ReturnCode setListener(ConnectorInfo& info,
  #                                ConnectorListeners* listeners);
  def setListener(self, info, listeners):
    self._rtcout.RTC_TRACE("setListener()")
    
    if not listeners:
      self._rtcout.RTC_ERROR("setListeners(listeners == 0): invalid argument")
      return self.INVALID_ARGS

    self._profile = info
    self._listeners = listeners

    return self.PORT_OK


  ## PublisherBase::ReturnCode PublisherNew::write(const cdrMemoryStream& data,
  ##                                               unsigned long sec,
  ##                                               unsigned long usec)
  def write(self, data, sec, usec):
    self._rtcout.RTC_PARANOID("write()")
    
    if not self._consumer or not self._buffer or not self._listeners:
      return self.PRECONDITION_NOT_MET

    if self._retcode == self.CONNECTION_LOST:
      self._rtcout.RTC_DEBUG("write(): connection lost.")
      return self._retcode

    if self._retcode == self.BUFFER_FULL:
      self._rtcout.RTC_DEBUG("write(): InPort buffer is full.")
      ret = self._buffer.write(data, sec, usec)
      self._task.signal()
      return self.BUFFER_FULL

    # why?
    assert(self._buffer != 0)

    self.onBufferWrite(data)
    ret = self._buffer.write(data, sec, usec)

    self._task.signal()
    self._rtcout.RTC_DEBUG("%s = write()", OpenRTM_aist.DataPortStatus.toString(ret))

    return self.convertReturn(ret, data)

  ## bool PublisherNew::isActive()
  def isActive(self):
    return self._active


  ## PublisherBase::ReturnCode PublisherNew::activate()
  def activate(self):
    self._active = True
    return self.PORT_OK


  ## PublisherBase::ReturnCode PublisherNew::deactivate()
  def deactivate(self):
    self._active = False;
    return self.PORT_OK

  
  ##
  # @if jp
  # @brief PublisherNew::スレッド実行関数
  # @else
  # @brief Thread execution function
  # @endif
  #
  # int PublisherNew::svc(void)
  def svc(self):
    guard = OpenRTM_aist.ScopedLock(self._retmutex)

    if self._pushPolicy == self.ALL:
      self._retcode = self.pushAll()
      return 0
    elif self._pushPolicy == self.FIFO:
      self._retcode = self.pushFifo()
      return 0
    elif self._pushPolicy == self.SKIP:
      self._retcode = self.pushSkip()
      return 0
    elif self._pushPolicy == self.NEW:
      self._retcode = self.pushNew()
      return 0
    else:
      self._retcode = self.pushNew()

    return 0


  ##
  # @brief push all policy
  #
  # PublisherNew::ReturnCode PublisherNew::pushAll()
  def pushAll(self):
    self._rtcout.RTC_TRACE("pushAll()")
    try:

      while self._buffer.readable() > 0:
        cdr = self._buffer.get()
        self.onBufferRead(cdr)

        self.onSend(cdr)
        ret = self._consumer.put(cdr)
            
        if ret != self.PORT_OK:
          self._rtcout.RTC_DEBUG("%s = consumer.put()", OpenRTM_aist.DataPortStatus.toString(ret))
          return self.invokeListener(ret, cdr)
        self.onReceived(cdr)

        self._buffer.advanceRptr()

      return self.PORT_OK
    except:
      return self.CONNECTION_LOST

    return self.PORT_ERROR


  ##
  # @brief push "fifo" policy
  #
  # PublisherNew::ReturnCode PublisherNew::pushFifo()
  def pushFifo(self):
    self._rtcout.RTC_TRACE("pushFifo()")

    try:
      cdr = self._buffer.get()
      self.onBufferRead(cdr)

      self.onSend(cdr)
      ret = self._consumer.put(cdr)

      if ret != self.PORT_OK:
        self._rtcout.RTC_DEBUG("%s = consumer.put()", OpenRTM_aist.DataPortStatus.toString(ret))
        return self.invokeListener(ret, cdr)
      self.onReceived(cdr)
        
      self._buffer.advanceRptr()
        
      return self.PORT_OK
    except:
      return self.CONNECTION_LOST

    return self.PORT_ERROR


  ##
  # @brief push "skip" policy
  #
  # PublisherNew::ReturnCode PublisherNew::pushSkip()
  def pushSkip(self):
    self._rtcout.RTC_TRACE("pushSkip()")
    try:
      ret = self.PORT_OK
      preskip = self._buffer.readable() + self._leftskip
      loopcnt = preskip/(self._skipn+1)
      postskip = self._skipn - self._leftskip

      for i in range(loopcnt):
        self._buffer.advanceRptr(postskip)
        cdr = self._buffer.get()
        self.onBufferRead(cdr)

        self.onSend(cdr)
        ret = self._consumer.put(cdr)
        if ret != self.PORT_OK:
          self._buffer.advanceRptr(-postskip)
          self._rtcout.RTC_DEBUG("%s = consumer.put()", OpenRTM_aist.DataPortStatus.toString(ret))
          return self.invokeListener(ret, cdr)

        self.onReceived(cdr)
        postskip = self._skipn + 1

      self._buffer.advanceRptr(self._buffer.readable())

      if loopcnt == 0:
        # Not put
        self._leftskip = preskip % (self._skipn + 1)
      else:
        if self._retcode != self.PORT_OK:
          # put Error after
          self._leftskip = 0
        else:
          # put OK after
          self._leftskip = preskip % (self._skipn + 1)

      return ret

    except:
      return self.CONNECTION_LOST

    return self.PORT_ERROR


  ##
  # @brief push "new" policy
  #
  # PublisherNew::ReturnCode PublisherNew::pushNew()
  def pushNew(self):
    self._rtcout.RTC_TRACE("pushNew()")
    try:
      self._buffer.advanceRptr(self._buffer.readable() - 1)
        
      cdr = self._buffer.get()
      self.onBufferRead(cdr)

      self.onSend(cdr)
      ret = self._consumer.put(cdr)

      if ret != self.PORT_OK:
        self._rtcout.RTC_DEBUG("%s = consumer.put()", OpenRTM_aist.DataPortStatus.toString(ret))
        return self.invokeListener(ret, cdr)

      self.onReceived(cdr)
      self._buffer.advanceRptr()

      return self.PORT_OK

    except:
      return self.CONNECTION_LOST

    return self.PORT_ERROR


  ## PublisherBase::ReturnCode
  ## PublisherNew::convertReturn(BufferStatus::Enum status,
  ##                             const cdrMemoryStream& data)
  def convertReturn(self, status, data):

    if status == OpenRTM_aist.BufferStatus.BUFFER_OK:
      return self.PORT_OK
    
    elif status == OpenRTM_aist.BufferStatus.BUFFER_ERROR:
      return self.BUFFER_ERROR

    elif status == OpenRTM_aist.BufferStatus.BUFFER_FULL:
      self.onBufferFull(data)
      return self.BUFFER_FULL

    elif status == OpenRTM_aist.BufferStatus.NOT_SUPPORTED:
      return self.PORT_ERROR

    elif status == OpenRTM_aist.BufferStatus.TIMEOUT:
      self.onBufferWriteTimeout(data)
      return self.BUFFER_TIMEOUT

    elif status == OpenRTM_aist.BufferStatus.PRECONDITION_NOT_MET:
      return self.PRECONDITION_NOT_MET

    else:
      return self.PORT_ERROR


  # PublisherNew::ReturnCode
  # PublisherNew::invokeListener(DataPortStatus::Enum status,
  #                              const cdrMemoryStream& data)
  def invokeListener(self, status, data):
    # ret:
    # PORT_OK, PORT_ERROR, SEND_FULL, SEND_TIMEOUT, CONNECTION_LOST,
    # UNKNOWN_ERROR
    if status == self.PORT_ERROR:
      self.onReceiverError(data)
      return self.PORT_ERROR
        
    elif status == self.SEND_FULL:
      self.onReceiverFull(data)
      return self.SEND_FULL
        
    elif status == self.SEND_TIMEOUT:
      self.onReceiverTimeout(data)
      return self.SEND_TIMEOUT
        
    elif status == self.CONNECTION_LOST:
      self.onReceiverError(data)
      return self.CONNECTION_LOST
        
    elif status == self.UNKNOWN_ERROR:
      self.onReceiverError(data)
      return self.UNKNOWN_ERROR
        
    else:
      self.onReceiverError(data)
      return self.PORT_ERROR


  ##
  # @brief Connector data listener functions
  #
  # inline void onBufferWrite(const cdrMemoryStream& data)
  def onBufferWrite(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_WRITE].notify(self._profile, data)
    return

  ## inline void onBufferFull(const cdrMemoryStream& data)
  def onBufferFull(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_FULL].notify(self._profile, data)
    return


  ## inline void onBufferWriteTimeout(const cdrMemoryStream& data)
  def onBufferWriteTimeout(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_WRITE_TIMEOUT].notify(self._profile, data)
    return

  ## inline void onBufferWriteOverwrite(const cdrMemoryStream& data)
  def onBufferWriteOverwrite(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_OVERWRITE].notify(self._profile, data)
    return

  ## inline void onBufferRead(const cdrMemoryStream& data)
  def onBufferRead(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_READ].notify(self._profile, data)
    return

  ##inline void onSend(const cdrMemoryStream& data)
  def onSend(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_SEND].notify(self._profile, data)
    return

  ## inline void onReceived(const cdrMemoryStream& data)
  def onReceived(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVED].notify(self._profile, data)
    return

  ## inline void onReceiverFull(const cdrMemoryStream& data)
  def onReceiverFull(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVER_FULL].notify(self._profile, data)
    return

  ## inline void onReceiverTimeout(const cdrMemoryStream& data)
  def onReceiverTimeout(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVER_TIMEOUT].notify(self._profile, data)
    return

  ## inline void onReceiverError(const cdrMemoryStream& data)
  def onReceiverError(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVER_ERROR].notify(self._profile, data)
    return

  ## inline void onSenderError()
  def onSenderError(self):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connector_[OpenRTM_aist.ConnectorListenerType.ON_SENDER_ERROR].notify(self._profile)
    return



def PublisherNewInit():
  OpenRTM_aist.PublisherFactory.instance().addFactory("new",
                                                      OpenRTM_aist.PublisherNew,
                                                      OpenRTM_aist.Delete)
