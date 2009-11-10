#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file  PublisherPeriodic.py
# @brief PublisherPeriodic class
# @date  $Date: 2007/09/28 $
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
from omniORB import any

import OpenRTM_aist


##
# @if jp
# @class PublisherPeriodic
# @brief PublisherPeriodic クラス
#
# 一定周期でコンシューマの送出処理を呼び出す Publisher
# 定期的にデータ送信を実行する場合に使用する。
#
# @else
# @class PublisherPeriodic
# @brief PublisherPeriodic class
# @endif
class PublisherPeriodic(OpenRTM_aist.PublisherBase):
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
  # 送出処理の呼び出し間隔を、Propertyオブジェクトのdataport.push_rateメンバ
  # に設定しておく必要がある。送出間隔は、Hz単位の浮動小数文字列で指定。
  # たとえば、1000.0Hzの場合は、「1000.0」を設定。
  # 上記プロパティが未設定の場合は、「1000Hz」を設定。
  #
  # @param self
  # @param consumer データ送出を待つコンシューマ
  # @param property 本Publisherの駆動制御情報を設定したPropertyオブジェクト
  #
  # @else
  # @brief Constructor
  # @endif
  def __init__(self):
    self._rtcout = OpenRTM_aist.Manager.instance().getLogbuf("PublisherPeriodic")
    self._consumer   = None
    self._buffer     = None
    self._task       = None
    self._retcode    = OpenRTM_aist.DataPortStatus.PORT_OK
    self._retmutex   = threading.RLock()
    self._pushPolicy = self.NEW
    self._skipn      = 10
    self._active     = False
    self._readback   = False
    self._leftskip  = 0

    return


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
  # @endif
  def __del__(self):
    self._rtcout.RTC_TRACE("~PublisherPeriodic()")
    if self._task:
      self._task.resume()
      self._task.finalize()
      self._rtcout.RTC_PARANOID("task finalized.")

      OpenRTM_aist.PeriodicTaskFactory.instance().deleteObject(self._task)
      self._rtcout.RTC_PARANOID("task deleted.")

    # "consumer" should be deleted in the Connector
    self._consumer = None
    # "buffer"   should be deleted in the Connector
    self._buffer = None
    return


  ##
  # @if jp
  # @brief 初期化
  # @else
  # @brief initialization
  # @endif
  # PublisherBase::ReturnCode PublisherPeriodic::init(coil::Properties& prop)
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
      return OpenRTM_aist.DataPortStatus.INVALID_ARGS

    self._rtcout.RTC_PARANOID("Task creation succeeded.")

    # setting task function
    self._task.setTask(self.svc)

    # Task execution rate
    rate = prop.getProperty("publisher.push_rate")

    if rate != "":
      hz = float(rate)
      if hz == 0:
        hz = 1000.0
      self._rtcout.RTC_DEBUG("Task period %f [Hz]", hz)
    else:
      hz = 1000.0

    self._task.setPeriod(1.0/hz)
    
    # Measurement setting
    mprop = prop.getNode("measurement")

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

    # Start task in suspended mode
    self._task.suspend()
    self._task.activate()
    self._task.suspend()
    return OpenRTM_aist.DataPortStatus.PORT_OK

  
  ##
  # @if jp
  # @brief InPortコンシューマのセット
  # @else
  # @brief Store InPort consumer
  # @endif
  # PublisherBase::ReturnCode
  # PublisherPeriodic::setConsumer(InPortConsumer* consumer)
  def setConsumer(self, consumer):
    self._rtcout.RTC_TRACE("setConsumer()")

    if not consumer:
      self._rtcout.RTC_ERROR("setConsumer(consumer = 0): invalid argument.")
      return OpenRTM_aist.DataPortStatus.INVALID_ARGS

    self._consumer = consumer
    return OpenRTM_aist.DataPortStatus.PORT_OK

  
  ##
  # @if jp
  # @brief バッファのセット
  # @else
  # @brief Setting buffer pointer
  # @endif
  # PublisherBase::ReturnCode PublisherPeriodic::setBuffer(CdrBufferBase* buffer)
  def setBuffer(self, buffer):
    self._rtcout.RTC_TRACE("setBuffer()")
    
    if not buffer:
      self._rtcout.RTC_ERROR("setBuffer(buffer == 0): invalid argument")
      return OpenRTM_aist.DataPortStatus.INVALID_ARGS

    self._buffer = buffer
    return OpenRTM_aist.DataPortStatus.PORT_OK


  ## PublisherBase::ReturnCode
  ## PublisherPeriodic::write(const cdrMemoryStream& data,
  ##                          unsigned long sec,
  ##                          unsigned long usec)
  def write(self, data, sec, usec):
    self._rtcout.RTC_PARANOID("write()")

    if not self._consumer or not self._buffer:
      return OpenRTM_aist.DataPortStatus.PRECONDITION_NOT_MET

    if self._retcode == OpenRTM_aist.DataPortStatus.CONNECTION_LOST:
      self._rtcout.RTC_DEBUG("write(): connection lost.")
      return self._retcode

    if self._retcode == OpenRTM_aist.DataPortStatus.BUFFER_FULL:
      self._rtcout.RTC_DEBUG("write(): InPort buffer is full.")
      self._buffer.write(data,sec,usec)
      return OpenRTM_aist.DataPortStatus.BUFFER_FULL

    ret = self._buffer.write(data, sec, usec)
    self._rtcout.RTC_DEBUG("%s = write()", OpenRTM_aist.DataPortStatus().toString(ret))
    self._task.resume()
    return self.convertReturn(ret)


  ## bool PublisherPeriodic::isActive()
  def isActive(self):
    return self._active


  ## PublisherBase::ReturnCode PublisherPeriodic::activate()
  def activate(self):
    if not self._task or not self._buffer:
      return OpenRTM_aist.DataPortStatus.PRECONDITION_NOT_MET
    self._active = True
    self._task.resume()
    return OpenRTM_aist.DataPortStatus.PORT_OK


  ## PublisherBase::ReturnCode PublisherPeriodic::deactivate()
  def deactivate(self):
    if not self._task:
      return OpenRTM_aist.DataPortStatus.PRECONDITION_NOT_MET
    self._active = False
    self._task.suspend()
    return OpenRTM_aist.DataPortStatus.PORT_OK


  ##
  # @if jp
  # @brief スレッド実行関数
  # @else
  # @brief Thread execution function
  # @endif
  # int PublisherPeriodic::svc(void)
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
  # PublisherBase::ReturnCode PublisherPeriodic::pushAll()
  def pushAll(self):
    self._rtcout.RTC_TRACE("pushAll()")

    while self._buffer.readable() > 0:
      cdr = self._buffer.get()
      ret = self._consumer.put(cdr)

      if ret != OpenRTM_aist.DataPortStatus.PORT_OK:
        return ret

      self._buffer.advanceRptr()

    return OpenRTM_aist.DataPortStatus.PORT_OK


  ##
  # @brief push "fifo" policy
  #
  # PublisherBase::ReturnCode PublisherPeriodic::pushFifo()
  def pushFifo(self):
    self._rtcout.RTC_TRACE("pushFifo()")
    if self._buffer.empty() and not self._readback:
      self._rtcout.RTC_DEBUG("buffer empty")
      return OpenRTM_aist.DataPortStatus.BUFFER_EMPTY

    cdr = self._buffer.get()
    ret = self._consumer.put(cdr)
    if ret != OpenRTM_aist.DataPortStatus.PORT_OK:
      self._rtcout.RTC_DEBUG("%s = consumer.put()",ret)
      return ret

    self._buffer.advanceRptr()
    
    return ret


  ##
  # @brief push "skip" policy
  #
  # PublisherBase::ReturnCode PublisherPeriodic::pushSkip()
  def pushSkip(self):
    self._rtcout.RTC_TRACE("pushSkip()")

    if self._buffer.empty() and not self._readback:
      self._rtcout.RTC_DEBUG("buffer empty")
      return OpenRTM_aist.DataPortStatus.BUFFER_EMPTY

    ret = OpenRTM_aist.DataPortStatus.PORT_OK
    preskip  = self._buffer.readable() + self._leftskip
    loopcnt  = preskip/(self._skipn +1)
    postskip = self._skipn - self._leftskip
    for i in range(loopcnt):
      self._buffer.advanceRptr(postskip)
      cdr = self._buffer.get()
      ret = self._consumer.put(cdr)
      if ret != OpenRTM_aist.DataPortStatus.PORT_OK:
        self._buffer.advanceRptr(-postskip)
        self._rtcout.RTC_DEBUG("%s = consumer.put()",ret)
        return ret
      postskip = self._skipn +1

    self._buffer.advanceRptr(self._buffer.readable())
    self._leftskip = preskip % (self._skipn +1)
    
    return ret


  ##
  # @brief push "new" policy
  #
  # PublisherBase::ReturnCode PublisherPeriodic::pushNew()
  def pushNew(self):
    self._rtcout.RTC_TRACE("pushNew()")

    if self._buffer.empty() and not self._readback:
      self._rtcout.RTC_DEBUG("buffer empty")
      return OpenRTM_aist.DataPortStatus.BUFFER_EMPTY
    
    self._buffer.advanceRptr(self._buffer.readable() - 1)
    
    cdr = self._buffer.get()
    ret = self._consumer.put(cdr)
    self._rtcout.RTC_DEBUG("%s = consumer.put()", ret)

    self._buffer.advanceRptr()
    return ret


  ## PublisherBase::ReturnCode
  ## PublisherPeriodic::convertReturn(BufferStatus::Enum status)
  def convertReturn(self, status):
    if status == OpenRTM_aist.BufferStatus.BUFFER_OK:
      return OpenRTM_aist.DataPortStatus.PORT_OK

    elif status == OpenRTM_aist.BufferStatus.BUFFER_EMPTY:
      return OpenRTM_aist.DataPortStatus.BUFFER_EMPTY

    elif status == OpenRTM_aist.BufferStatus.TIMEOUT:
      return OpenRTM_aist.DataPortStatus.BUFFER_TIMEOUT

    elif status == OpenRTM_aist.BufferStatus.PRECONDITION_NOT_MET:
      return OpenRTM_aist.DataPortStatus.PRECONDITION_NOT_MET

    else:
      return OpenRTM_aist.DataPortStatus.PORT_ERROR



def PublisherPeriodicInit():
  OpenRTM_aist.PublisherFactory.instance().addFactory("periodic",
                                                      OpenRTM_aist.PublisherPeriodic,
                                                      OpenRTM_aist.Delete)
