#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file OutPortBase.py
# @brief OutPortBase base class
# @date $Date: 2007/09/19 $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
# 
# Copyright (C) 2003-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.



##
# @if jp
#
# @class OutPortBase
# @brief OutPort 基底クラス
# 
# OutPort の実装である OutPort<T> の基底クラス。
#
# OutPortBase と PublisherBase は一種の Observer パターンを形成している。
# OutPortBase の attach(), detach(), notify() および
# PublisherBase の push() は Observer パターンに関連したメソッドである。
#
# @since 0.2.0
#
# @else
#
# @class OutPortBase
# @brief Output port base class.
#
# The base class of OutPort<T> s which are implementations of OutPort  
#
# @endif
class OutPortBase:
  """
  """



  ##
  # @if jp
  # @brief コンストラクタ
  #
  # コンストラクタ。
  #
  # @param self
  # @param name ポート名
  #
  # @else
  #
  # @brief A constructor of OutPortBase class.
  #
  # Constructor of OutPortBase.
  #
  # @endif
  def __init__(self, name):
    self._name = name
    self._publishers = []


  ##
  # @if jp
  # @brief デストラクタ
  #
  # デストラクタ。
  # 登録された全ての Publisher を削除する。
  #
  # @param self
  #
  # @else
  #
  # @brief destructor
  #
  # Destructor
  #
  # @endif
  def __del__(self):
    for pub in self._publishers:
      del(pub)


  ##
  # @if jp
  # @brief OutPort名称の取得
  #
  # OutPortの名称を取得する。
  #
  # @param self
  #
  # @return ポート名称
  #
  # @else
  #
  # @brief OutPort's name
  #
  # This operation returns OutPort's name
  #
  # @endif
  def name(self):
    return self._name


  ##
  # @if jp
  # @brief Publisherの追加
  #
  # 指定したPublisherをデータ更新通知先としてリストの最後尾に追加する。
  # attach_back() と同様な機能。
  #
  # @param self
  # @param id_ 指定されたPublisherに割り当てるID
  # @param publisher 登録対象Publisherオブジェクト
  #
  # @else
  #
  # @brief Attach a publisher
  #
  # Attach a publisher to observe OutPort.
  #
  # @endif
  def attach(self, id_, publisher):
    self.attach_back(id_, publisher)


  ##
  # @if jp
  # @brief リスト先頭へのPublisherの追加
  #
  # Publisherをリストの先頭に追加する。
  #
  # @param self
  # @param id_ 指定されたPublisherに割り当てるID
  # @param publisher 登録対象Publisherオブジェクト
  #
  # @else
  #
  # @brief Attach a publisher
  #
  # Attach a publisher to the head of the Publisher list.
  #
  # @endif
  def attach_front(self, id_, publisher):
    self._publishers.insert(0, self.Publisher(id_, publisher))


  ##
  # @if jp
  # @brief リスト最後尾へのPublisherの追加
  #
  # Publisherをリストの最後尾に追加する。
  #
  # @param self
  # @param id_ 指定されたPublisherに割り当てるID
  # @param publisher 登録対象Publisherオブジェクト
  #
  # @else
  #
  # @brief Attach a publisher
  #
  # Attach a publisher to the taile of the Publisher list.
  #
  # @endif
  def attach_back(self, id_, publisher):
    self._publishers.append(self.Publisher(id_, publisher))


  ##
  # @if jp
  # @brief Publisherの削除
  #
  # 指定された Publisher をデータ更新通知先リストから削除する。
  #
  # @param self
  # @param id_削除対象 Publisher のID
  #
  # @return 削除に成功した場合は、削除した Publisher オブジェクト
  #         指定した Publisher が存在しない場合は null
  #
  # @else
  #
  # @brief Detach a publisher
  #
  # Detach a publisher to observe OutPort.
  #
  # @endif
  def detach(self, id_):
    index = -1

    for i in range(len(self._publishers)):
      if id_ == self._publishers[i].id:
        index = i
        break
    if index < 0:
      return None

    pub = self._publishers[index].publisher
    del self._publishers[index]
    return pub


  ##
  # @if jp
  # @brief 更新の通知
  #
  # 登録されている全ての Publisher にデータ更新を通知する。
  #
  # @param self
  #
  # @else
  #
  # @brief Notify data update
  #
  # This operation notify data update to Publishers
  #
  # @endif
  def notify(self):
    for pub in self._publishers:
      pub.publisher.update()


  ##
  # @if jp
  # @brief Publisher 管理用内部クラス
  # @else
  #
  # @endif
  class Publisher:
    def __init__(self, id_, publisher_):
      self.id = id_
      self.publisher = publisher_


