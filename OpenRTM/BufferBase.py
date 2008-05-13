#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file BufferBase.py
# @brief Buffer abstract class
# @date $Date: 2007/09/12 $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
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
# @class BufferBase
# @brief BufferBase 抽象クラス
# 
# 種々のバッファのための抽象インターフェースクラス。
# 具象バッファクラスは、以下の関数の実装を提供しなければならない。
# 
# publicインターフェースとして以下のものを提供する。
#  - write(): バッファに書き込む
#  - read(): バッファから読み出す
#  - length(): バッファ長を返す
#  - isFull(): バッファが満杯である
#  - isEmpty(): バッファが空である
# 
# protectedインターフェースとして以下のものを提供する。
#  - put(): バッファにデータを書き込む
#  - get(): バッファからデータを読み出す
# 
# @since 0.4.0
# 
# @else
# 
# @class BufferBase
# @brief BufferBase abstract class
# 
# This is the abstract interface class for various Buffer.
# 
# @since 0.4.0
# 
# @endif
class BufferBase:
  """
  """


  ##
  # @if jp
  # 
  # @brief バッファの長さを取得する(サブクラス実装用)
  # 
  # バッファ長を取得する<BR>
  # ※サブクラスでの実装参照用
  # 
  # @param self 
  # 
  # @return バッファ長
  # 
  # @else
  # 
  # @brief Get the buffer length
  # 
  # @return buffer length
  # 
  # @endif
  def length(self):
    pass


  ##
  # @if jp
  # 
  # @brief バッファにデータを書き込む(サブクラス実装用)
  # 
  # バッファにデータを書き込む<BR>
  # ※サブクラスでの実装参照用
  # 
  # @param self 
  # @param value 書き込み対象データ
  # 
  # @return データ書き込み結果(true:書き込み成功，false:書き込み失敗)
  # 
  # @else
  # 
  # @brief Write data into the buffer
  # 
  # @endif
  def write(self, value):
    pass


  ##
  # @if jp
  # 
  # @brief バッファからデータを読み出す(サブクラス実装用)
  # 
  # バッファからデータを読み出す<BR>
  # ※サブクラスでの実装参照用
  # 
  # @param self 
  # @param value 読み出しデータ
  # 
  # @return データ読み出し結果(true:読み出し成功，false:読み出し失敗)
  # 
  # @else
  # 
  # @brief Read data from the buffer
  # 
  # @endif
  def read(self, value):
    pass


  ##
  # @if jp
  # 
  # @brief バッファfullチェック(サブクラス実装用)
  # 
  # バッファfullチェック用関数<BR>
  # ※サブクラスでの実装参照用
  # 
  # @param self 
  # 
  # @return fullチェック結果(true:バッファfull，false:バッファ空きあり)
  # 
  # @else
  # 
  # @brief True if the buffer is full, else false.
  # 
  # @endif
  def isFull(self):
    pass


  ##
  # @if jp
  # 
  # @brief バッファemptyチェック(サブクラス実装用)
  # 
  # バッファemptyチェック用関数<BR>
  # ※サブクラスでの実装参照用
  # 
  # @param self 
  # 
  # @return emptyチェック結果(true:バッファempty，false:バッファデータあり)
  # 
  # @else
  # 
  # @brief True if the buffer is empty, else false.
  # 
  # @endif
  def isEmpty(self):
    pass


  ##
  # @if jp
  # 
  # @brief バッファにデータを格納する(サブクラス実装用)
  # 
  # バッファへのデータ格納用関数<BR>
  # ※サブクラスでの実装参照用
  # 
  # @param self 
  # @param data 対象データ
  # 
  # @else
  # 
  # @brief Write data into the buffer
  # 
  # @endif
  def put(self, data):
    pass


  ##
  # @if jp
  # 
  # @brief バッファからデータを取得する(サブクラス実装用)
  # 
  # バッファに格納されたデータ取得用関数<BR>
  # ※サブクラスでの実装参照用
  # 
  # @param self 
  # 
  # @return 取得データ
  # 
  # @else
  # 
  # @brief Get data from the buffer
  # 
  # @endif
  def get(self):
    pass


  ##
  # @if jp
  # 
  # @brief 次に書き込むバッファへの参照を取得する(サブクラス実装用)
  # 
  # 書き込みバッファへの参照取得用関数<BR>
  # ※サブクラスでの実装参照用
  # 
  # @param self 
  # 
  # @return 次の書き込み対象バッファへの参照
  # 
  # @else
  # 
  # @brief Get the buffer's reference to be written the next
  # 
  # @endif
  def getRef(self):
    pass


##
# @if jp
# @class NullBuffer
# @brief ダミーバッファ実装クラス
# 
# バッファ長が１固定のダミーバッファ実装クラス。
# 
# @param DataType バッファに格納するデータ型
# 
# @since 0.4.0
# 
# @else
# 
# @endif
class NullBuffer(BufferBase):
  """
  """



  ##
  # @if jp
  # 
  # @brief コンストラクタ
  # 
  # コンストラクタ
  # バッファ長を１(固定)で初期化する。
  # 
  # @param self 
  # @param size バッファ長(デフォルト値:None，ただし無効)
  # 
  # @else
  # 
  # @endif
  def __init__(self, size=None):
    if size is None:
      size=1
    self._length = 1
    self._data = None
    self._is_new = False
    self._inited = False


  ##
  # @if jp
  # 
  # @brief コンストラクタ
  # 
  # コンストラクタ
  # 
  # @param self 
  # @param data 格納データ
  # 
  # @else
  # 
  # @endif
  def init(self, data):
    self.put(data)


  ##
  # @if jp
  # 
  # @brief バッファの初期化
  # 
  # バッファの初期化を実行する。
  # 
  # @param self 
  # 
  # @else
  # 
  # @endif
  def clear(self):
    self._inited = False


  ##
  # @if jp
  # 
  # @brief バッファ長(１固定)を取得する
  # 
  # バッファ長を取得する。(常に１を返す。)
  # 
  # @param self 
  # 
  # @return バッファ長(１固定)
  # 
  # @else
  # 
  # @brief Get the buffer length
  # 
  # @return buffer length(always 1)
  # 
  # @endif
  def length(self):
    return 1


  ##
  # @if jp
  # 
  # @brief バッファにデータを書き込む
  # 
  # 引数で与えられたデータをバッファに書き込む。
  # 
  # @param self 
  # @param value 書き込み対象データ
  # 
  # @return データ書き込み結果(true:書き込み成功，false:書き込み失敗)
  # 
  # @else
  # 
  # @brief Write data into the buffer
  # 
  # @endif
  def write(self, value):
    self.put(value)
    return True


  ##
  # @if jp
  # 
  # @brief バッファからデータを読み出す
  # 
  # バッファに格納されたデータを読み出す。
  # 
  # @param self 
  # @param value 読み出したデータ
  # 
  # @return データ読み出し結果(true:読み出し成功，false:読み出し失敗)
  # 
  # @else
  # 
  # @brief Read data from the buffer
  # 
  # @endif
  def read(self, value):
    if not self._inited:
      return False
    value[0] = self.get()
    return True


  ##
  # @if jp
  # 
  # @brief バッファfullチェック
  # 
  # バッファfullをチェックする。(常にfalseを返す。)
  # 
  # @param self 
  # 
  # @return fullチェック結果(常にfalse)
  # 
  # @else
  # 
  # @brief Always false.
  # 
  # @endif
  def isFull(self):
    return False


  ##
  # @if jp
  # 
  # @brief バッファemptyチェック
  # 
  # バッファemptyをチェックする。(常にfalseを返す。)
  # ※要確認
  # 
  # @param self 
  # 
  # @return emptyチェック結果(常にfalse)
  # 
  # @else
  # 
  # @brief Always false.
  # 
  # @endif
  def isEmpty(self):
    return not self._inited


  ##
  # @if jp
  # 
  # @brief 最新データか確認する
  # 
  # 現在のバッファ位置に格納されているデータが最新データか確認する。
  # 
  # @param self 
  # 
  # @return 最新データ確認結果
  #            ( true:最新データ．データはまだ読み出されていない
  #             false:過去のデータ．データは既に読み出されている)
  # 
  # @else
  # 
  # @endif
  def isNew(self):
    return self._is_new


  ##
  # @if jp
  # 
  # @brief バッファにデータを格納
  # 
  # 引数で与えられたデータをバッファに格納する。
  # 
  # @param self 
  # @param data 対象データ
  # 
  # @else
  # 
  # @brief Write data into the buffer
  # 
  # @endif
  def put(self, data):
    self._data = data
    self._is_new = True
    self._inited = True


  ##
  # @if jp
  # 
  # @brief バッファからデータを取得する
  # 
  # バッファに格納されたデータを取得する。
  # 
  # @param self 
  # 
  # @return 取得データ
  # 
  # @else
  # 
  # @brief Get data from the buffer
  # 
  # @endif
  def get(self):
    self._is_new = False
    return self._data


  ##
  # @if jp
  # 
  # @brief 次に書き込むバッファへの参照を取得する
  # 
  # 書き込みバッファへの参照を取得する。
  # 本バッファ実装ではバッファ長は固定で１であるため，
  # 常に同じ位置への参照を返す。
  # 
  # @param self 
  # 
  # @return 次の書き込み対象バッファへの参照(固定)
  # 
  # @else
  # 
  # @brief Get the buffer's reference to be written the next
  # 
  # @endif
  def getRef(self):
    return self._data
