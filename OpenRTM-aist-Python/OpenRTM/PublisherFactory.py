#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file  PublisherFactory.py
# @brief PublisherFactory class
# @date  $Date: 2007/09/05$
# @author Noriaki Ando <n-ando@aist.go.jp>
#
# Copyright (C) 2006-2008
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

from omniORB import any

import OpenRTM


##
# @if jp
# @class PublisherFactory
# @brief PublisherFactory クラス
#
# 各種Publisherオブジェクトの生成・破棄を管理するファクトリクラス
# ※テンポラリな実装
#   将来的には任意のPublisherを生成できるようにする。
#
# @else
# @class PublisherFactory
# @brief PublisherFactory class
# @endif
class PublisherFactory:
  """
  """


  ##
  # @if jp
  # @brief Publisherの生成
  #
  # Publisherオブジェクトを生成する。
  # 指定された引数に応じた適切なPublisher実装のオブジェクトが生成される。
  # 生成するPublisherの種別を、指定されたPropertyオブジェクトの
  # dataport.subscription_typeメンバに設定しておく必要がある。
  # また、種別によっては、Publisherの駆動を制御する情報をさらに設定する必要が
  # ある。
  # これらの具体的な内容は、それぞれのPublisher実装を参照のこと。
  #
  # @param self
  # @param consumer Publisherによってデータ送出を駆動されるコンシューマ
  # @param property 生成すべきPublisherを特定するための情報や、Publisherの
  #                 駆動を制御するための情報が設定されているPropertyオブジェ
  #                 クト
  #
  # @return 生成したPublisherオブジェクト。生成に失敗した場合はNullを返す。
  #
  # @else
  # @brief Create Publisher
  # @endif
  def create(self, consumer, property):
    pub_type = property.getProperty("dataport.subscription_type", "New")

    if type(pub_type) != str :
      pub_type = str(any.from_any(pub_type,keep_structs=True))
    if pub_type == "New":
      return OpenRTM.PublisherNew(consumer, property)
    elif pub_type == "Periodic":
      return OpenRTM.PublisherPeriodic(consumer, property)
    elif pub_type == "Flush":
      return OpenRTM.PublisherFlush(consumer, property)

    return None


  ##
  # @if jp
  # @brief Publisherの破棄
  #
  # 設定されたPublisherオブジェクトを破棄する。
  #
  # @param self
  # @param publisher 破棄対象Publisherオブジェクト
  #
  # @else
  # @brief Destroy Publisher
  # @endif
  def destroy(self, publisher):
    if publisher:
      publisher.release()
    del publisher
