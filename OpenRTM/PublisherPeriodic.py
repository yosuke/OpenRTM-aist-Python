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

import OpenRTM


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
class PublisherPeriodic(OpenRTM.PublisherBase):
  """
  """



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
  def __init__(self, consumer, property):
    self._consumer = consumer
    self._running = True
    rate = property.getProperty("dataport.push_rate")

    if type(rate) == str or type(rate) == float or type(rate) == long :
      rate = float(rate)
    else:
      rate = float(any.from_any(rate,keep_structs=True))

    if rate:
      hz = rate
      if (hz == 0):
        hz = 1000.0
    else:
      hz = 1000.0

    self._usec = int(1000000.0/hz)

    self._running = True
    self._thread = threading.Thread(target=self.run)
    self._thread.start()


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
    self._running = False
    del self._consumer


  ##
  # @if jp
  # @brief Observer関数(未実装)
  #
  # 本 Publisher では何も実行しない。
  #
  # @param self
  #
  # @else
  # @brief Observer function
  # @endif
  def update(self):
    pass


  ##
  # @if jp
  # @brief タスク開始関数
  #
  # 本Publisher駆動制御用スレッドの実行を開始する。
  #
  # @param self
  #
  # @else
  # @brief Thread execution function
  # @endif
  def run(self):
    import time
    while self._running:
      self._consumer.push()
      time.sleep(self._usec/1000000.0)

    return 0


  ##
  # @if jp
  # @brief タスク終了関数
  #
  # ACE_Task::release() のオーバーライド
  # 駆動フラグをfalseに設定し、本 Publisher の駆動を停止する。
  # ただし、最大１回コンシューマの送出処理が呼び出される場合がある。
  #
  # @param self
  #
  # @else
  # @brief Task terminate function
  #
  # ACE_Task::release() override function
  #
  # @endif
  def release(self):
    self._running = False
