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
  def __init__(self, consumer, property):
    self._data = self.NewData()
    self._consumer = consumer
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
  #
  # @endif
  def __del__(self):
    del self._consumer


  ##
  # @if jp
  # @brief Observer関数
  #
  # 送出タイミング時に呼び出す。
  # ブロックしている当該Publisherの駆動が開始され、コンシューマへの送出処理が
  # 行われる。
  #
  # @param self
  #
  # @else
  # @brief Observer function
  # @endif
  def update(self):
    if not self._data._cond.acquire(0):
      return

    self._data._updated = True
    self._data._cond.notify()
    self._data._cond.release()
    return


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
    while self._running:
      self._data._cond.acquire()
      # Waiting for new data updated
      while not self._data._updated and self._running:
        self._data._cond.wait()

      if self._data._updated:
        self._consumer.push()
        self._data._updated = False

      self._data._cond.release()


  ##
  # @if jp
  # @brief タスク終了関数
  #
  # ACE_Task::release() のオーバーライド
  # 駆動フラグをfalseに設定し、本 Publisher の駆動を停止する。
  # ただし、駆動スレッドがブロックされている場合には、
  # 最大１回コンシューマの送出処理が呼び出される場合がある。
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
    if not self._data._cond.acquire(0):
      return

    self._running = False
    self._data._cond.notify()
    self._data._cond.release()
    #self.wait()


  # NewData condition struct
  ##
  # @if jp
  # @class NewData
  # @brief データ状態管理用内部クラス
  # @else
  # @endif
  class NewData:
    def __init__(self):
      self._mutex = threading.RLock()
      self._cond = threading.Condition(self._mutex)
      self._updated = False
