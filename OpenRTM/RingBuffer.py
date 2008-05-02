#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file RingBuffer.py
# @brief Defautl Buffer class
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

import RTC
import OpenRTM

##
# @if jp
# @class RingBuffer
# @brief リングバッファ実装クラス
# 
# 指定した長さのリング状バッファを持つバッファ実装クラス。
# バッファ全体にデータが格納された場合、以降のデータは古いデータから
# 順次上書きされる。
# 従って、バッファ内には直近のバッファ長分のデータのみ保持される。
#
# 注)現在の実装では、一番最後に格納したデータのみバッファから読み出し可能
#
# @param DataType バッファに格納するデータ型
#
# @since 0.4.0
#
# @else
#
# @endif
class RingBuffer(OpenRTM.BufferBase):
  """
  """



  ##
  # @if jp
  #
  # @brief コンストラクタ
  # 
  # コンストラクタ
  # 指定されたバッファ長でバッファを初期化する。
  # ただし、指定された長さが２未満の場合、長さ２でバッファを初期化する。
  #
  # @param self
  # @param length バッファ長
  # 
  # @else
  #
  # @endif
  def __init__(self, length):
    self._oldPtr = 0
    if length < 2:
      self._length = 2
      self._newPtr = 1
    else:
      self._length = length
      self._newPtr = length - 1

    self._inited = False
    self._buffer = [self.Data() for i in range(self._length)]


  ##
  # @if jp
  #
  # @brief 初期化
  # 
  # バッファの初期化を実行する。
  # 指定された値をバッファ全体に格納する。
  #
  # @param self
  # @param data 初期化用データ
  # 
  # @else
  #
  # @endif
  def init(self, data):
    for i in range(self._length):
      self.put(data)


  ##
  # @if jp
  #
  # @brief クリア
  # 
  # バッファに格納された情報をクリアする。
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
  # @brief バッファ長を取得する
  # 
  # バッファ長を取得する。
  #
  # @param self
  # 
  # @return バッファ長
  # 
  # @else
  #
  # @brief Get the buffer length
  #
  # @endif
  def length(self):
    return self._length


  ##
  # @if jp
  #
  # @brief バッファに書き込む
  # 
  # 引数で与えられたデータをバッファに書き込む。
  # 
  # @param self
  # @param value 書き込み対象データ
  #
  # @return データ書き込み結果(常にtrue:書き込み成功を返す)
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
  # @brief バッファから読み出す
  # 
  # バッファに格納されたデータを読み出す。
  # 
  # @param self
  # @param value 読み出したデータ
  #
  # @return データ読み出し結果
  # 
  # @else
  #
  # @brief Write data into the buffer
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
  # @brief バッファが満杯であるか確認する
  # 
  # バッファ満杯を確認する。(常にfalseを返す。)
  # 
  # @param self
  #
  # @return 満杯確認結果(常にfalse)
  # 
  # @else
  #
  # @brief True if the buffer is full, else false.
  #
  # @endif
  def isFull(self):
    return False


  ##
  # @if jp
  #
  # @brief バッファが空であるか確認する
  # 
  # バッファ空を確認する。
  # 
  # 注)現在の実装では，現在のバッファ位置に格納されたデータが読み出されたか
  # どうかを返す。( true:データ読み出し済，false:データ未読み出し)
  # 
  # @param self
  #
  # @return 空確認結果
  # 
  # @else
  #
  # @brief True if the buffer is empty, else false.
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
  #           ( true:最新データ．データはまだ読み出されていない
  #            false:過去のデータ．データは既に読み出されている)
  # 
  # @else
  #
  # @endif
  def isNew(self):
    return self._buffer[self._newPtr].isNew()


  ##
  # @if jp
  #
  # @brief バッファにデータを格納する
  # 
  # 引数で与えられたデータをバッファに格納する。
  # 
  # 注)現在の実装ではデータを格納すると同時に、データの読み出し位置を
  # 格納したデータ位置に設定している。このため、常に直近に格納したデータを
  # 取得する形となっている。
  # 
  # @param self
  # @param data 格納対象データ
  # 
  # @else
  #
  # @brief Write data into the buffer
  #
  # @endif
  def put(self, data):
    self._buffer[self._oldPtr].write(data)
    self._newPtr = self._oldPtr
    ptr = self._oldPtr + 1
    self._oldPtr = ptr % self._length
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
    return self._buffer[self._newPtr].read()


  ##
  # @if jp
  #
  # @brief 次に書き込むバッファへの参照を取得する
  # 
  # 書き込みバッファへの参照を取得する。
  # 
  # @return 次の書き込み対象バッファへの参照
  # 
  # @param self
  #
  # @else
  #
  # @brief Get the buffer's reference to be written the next
  #
  # @endif
  def getRef(self):
    return self._buffer[self._newPtr].data


  ##
  # @if jp
  # @class Data
  # @brief バッファデータクラス
  # 
  # バッファデータ格納用配列クラス。
  #
  # @since 0.4.0
  #
  # @else
  # @brief Buffer sequence
  # @endif
  class Data:
    def __init__(self):
      self.data = None
      self.is_new = False


    def write(self, other):
      self.is_new = True
      self.data = other


    def read(self):
      self.is_new = False
      return self.data


    def isNew(self):
      return self.is_new
