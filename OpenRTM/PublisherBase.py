#!/usr/bin/env python 
# -*- coding: euc-jp -*-

##
# @file PublisherBase.py
# @brief Publisher base class
# @date $Date: 2007/09/05$
# @author Noriaki Ando <n-ando@aist.go.jp>
#
# Copyright (C) 2006-2008
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.


##
# @if jp
#
# @class PublisherBase
#
# @brief Publisher 基底クラス
# 
# データ送出タイミングを管理して送出を駆動するPublisher* の基底クラス。
# 各種 Publisher はこのクラスを継承して詳細を実装する。
#
# @since 0.4.0
#
# @else
#
# @class PublisherBase
#
# @brief Base class of Publisher.
#
# A base class of Publisher*.
# Variation of Publisher* which implements details of Publisher
# inherits this PublisherBase class.
#
# @endif
class PublisherBase:
  """
  """



  ##
  # @if jp
  #
  # @brief 送出タイミングを通知する。(サブクラス実装用)
  #
  # 送出を待つオブジェクトに、送出タイミングを通知するための関数。<BR>
  # ※サブクラスでの実装参照用
  # 
  # @param self
  # 
  # @else
  #
  # @endif
  def update(self):
    pass


  ##
  # @if jp
  #
  # @brief Publisher を破棄する。(サブクラス実装用)
  #
  # 当該 Publisher を破棄する。
  # 当該 Publisher が不要になった場合に PublisherFactory から呼び出される。<BR>
  # ※サブクラスでの実装参照用
  # 
  # @param self
  #
  # @else
  #
  # @endif
  def release(self):
    pass
