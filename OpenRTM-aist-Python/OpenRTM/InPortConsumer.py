#!/usr/bin/env python
# -*- coding: euc-jp -*-


##
# @file  InPortConsumer.py
# @brief InPortConsumer class
# @date  $Date: 2007/09/04$
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
#
# @class InPortConsumer
#
# @brief InPortConsumer 基底クラス
#
# 入力ポートコンシューマのための抽象インターフェースクラス
# 各具象クラスは、以下の関数の実装を提供しなければならない。
# - push(): データ送信
# - clone(): ポートのコピー
# - subscribeInterface(): データ送出通知への登録
# - unsubscribeInterface(): データ送出通知の登録解除
#
# @since 0.4.0
#
# @else
# @class InPortConsumer
# @brief InPortConsumer class
# @endif
class InPortConsumer:
  """
  """



  ##
  # @if jp
  # @brief 接続先へのデータ送信(サブクラス実装用)
  #
  # 接続先のポートへデータを送信するための関数。<BR>
  # ※サブクラスでの実装参照用
  #
  # @param self
  #
  # @else
  #
  # @endif
  def push(self):
    pass

  ##
  # @if jp
  # @brief 当該ポートのコピー(サブクラス実装用)
  #
  # 当該ポートのコピーを生成するための関数。
  # ※サブクラスでの実装参照用
  #
  # @param self
  #
  # @return 複製された InPortConsumer オブジェクト
  #
  # @else
  #
  # @endif
  def clone(self):
    pass


  ##
  # @if jp
  # @brief データ送出通知受け取りへの登録(サブクラス実装用)
  #
  # 指定されたプロパティの内容に基づいて、データ送出通知の受け取りに登録する
  # ための関数。
  # ※サブクラスでの実装参照用
  #
  # @param self
  # @param properties 登録時に参照するプロパティ
  #
  # @return 登録処理結果
  #
  # @else
  #
  # @endif
  def subscribeInterface(self, properties):
    pass


  ##
  # @if jp
  # @brief データ送出通知受け取りからの登録解除(サブクラス実装用)
  #
  # データ送出通知の受け取りから登録解除するための関数。
  # ※サブクラスでの実装参照用
  #
  # @param self
  # @param properties 登録解除時に参照するプロパティ
  #
  # @else
  #
  # @endif
  def unsubscribeInterface(self, properties):
    pass
