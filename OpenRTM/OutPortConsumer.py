#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file  OutPortConsumer.py
# @brief OutPortConsumer class
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

import OpenRTM


##
# @if jp
#
# @class OutPortConsumer
#
# @brief OutPortConsumer クラス
#
# 出力ポートコンシューマのためのクラス
# 各具象クラスは、以下の関数の実装を提供しなければならない。
# - pull(): データ受信
# - subscribeInterface(): データ受信通知への登録
# - unsubscribeInterface(): データ受信通知の登録解除
#
# @since 0.4.0
#
# @else
# @class OutPortConsumer
# @brief OutPortConsumer class
# @endif
class OutPortConsumer:
  """
  """



  ##
  # @if jp
  #
  # @brief データを受信する(サブクラス実装用)
  #
  # データ受信を実行するための関数。<BR>
  # ※サブクラスでの実装参照用
  #
  # @param self
  #
  # @else
  #
  # @endif
  def pull(self):
    pass


  ##
  # @if jp
  #
  # @brief データ受信通知への登録(サブクラス実装用)
  #
  # 指定されたプロパティ情報に基づいて、データ受信通知に登録する関数。<BR>
  # ※サブクラスでの実装参照用
  #
  # @param self
  # @param properties 登録用プロパティ
  #
  # @return 登録処理結果(登録成功:true、登録失敗:false)
  #
  # @else
  #
  # @endif
  def subscribeInterface(self, properties):
    pass


  ##
  # @if jp
  #
  # @brief データ受信通知からの登録解除(サブクラス実装用)
  #
  # データ受信通知からの登録を解除するための関数。<BR>
  # ※サブクラスでの実装参照用
  #
  # @param self
  # @param properties 登録解除用プロパティ
  #
  # @return 登録解除処理結果(登録解除成功:true、登録解除失敗:false)
  #
  # @else
  #
  # @endif
  def unsubscribeInterface(self, properties):
    pass
