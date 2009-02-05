#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file  PublisherFlush.py
# @brief PublisherFlush class
# @date  $Date: 2007/09/06$
# @author Noriaki Ando <n-ando@aist.go.jp>
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
  def __init__(self, consumer, property):
    self._consumer = consumer


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
    del self._consumer


  ##
  # @if jp
  # @brief Observer関数
  #
  # 送出タイミング時に呼び出す。
  # 即座に同一スレッドにてコンシューマの送出処理が呼び出される。
  #
  # @param self
  #
  # @else
  # @brief Observer function
  # @endif
  def update(self):
    self._consumer.push()
    return
  
