#!/usr/bin/env python
# -*- coding: euc-jp -*-


##
# @file OutPort.py
# @brief OutPort class
# @date $Date: 2007/09/19$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
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
# @brief 時間単位変換用定数
# @else
# @endif
usec_per_sec = 1000000


import time



##
# @if jp
# @class Time
# @brief 時間管理用クラス
# 
# 指定した時間値を保持するためのクラス。
# 
# @since 0.4.1
# 
# @else
# 
# @endif
class Time:



  ##
  # @if jp
  # @brief コンストラクタ
  #
  # コンストラクタ。
  #
  # @param self
  #
  # @else
  # @brief Constructor.
  #
  # Constructor.
  #
  # @param self
  #
  # @endif
  def __init__(self):
    global usec_per_sec
    tm = time.time()
    tm_f       = tm - int(tm)     # 小数部の取り出し
    self.sec   = int(tm - tm_f)   # 整数部の取り出し
    self.usec  = int(tm_f * usec_per_sec) # sec -> usec (micro second)



##
# @if jp
#
# @class OutPort
#
# @brief OutPort クラス
# 
# OutPort 用クラス
#
# @since 0.2.0
#
# @else
# 
# @endif
class OutPort(OpenRTM.OutPortBase):
  """
  """



  ##
  # @if jp
  #
  # @brief コンストラクタ
  #
  # コンストラクタ
  #
  # @param self
  # @param name ポート名
  # @param value このポートにバインドされるデータ変数
  # @param buffer_ バッファ
  #
  # @else
  #
  # @brief Constructor
  #
  # @endif
  def __init__(self, name, value, buffer_):
    OpenRTM.OutPortBase.__init__(self, name)
    self._buffer         = buffer_
    self._value          = value
    self._timeoutTick    = 1000 # timeout tick: 1ms
    self._readBlock      = False
    self._readTimeout    = 0
    self._writeBlock     = False
    self._writeTimeout   = 0
    self._OnWrite        = None
    self._OnWriteConvert = None
    self._OnRead         = None
    self._OnReadConvert  = None
    self._OnOverflow     = None
    self._OnUnderflow    = None


  ##
  # @if jp
  # @brief 最新データか確認
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
    return self._buffer.isNew()


  ##
  # @if jp
  #
  # @brief データ書き込み
  #
  # ポートへデータを書き込む。
  #
  # - コールバックファンクタ OnWrite がセットされている場合、
  #   OutPort が保持するバッファに書き込む前に OnWrite が呼ばれる。
  # - OutPort が保持するバッファがオーバーフローを検出できるバッファであり、
  #   かつ、書き込む際にバッファがオーバーフローを検出した場合、
  #   コールバックファンクタ OnOverflow が呼ばれる。
  # - コールバックファンクタ OnWriteConvert がセットされている場合、
  #   バッファ書き込み時に、 OnWriteConvert の operator() の戻り値が
  #   バッファに書き込まれる。
  #
  # @param self
  # @param value 書き込み対象データ
  #
  # @return 書き込み処理結果(書き込み成功:true、書き込み失敗:false)
  #
  # @else
  #
  # @brief Write data
  #
  # @endif
  # virtual bool write(const DataType& value)
  ##
  # @if jp
  #
  # @brief データ書き込み
  #
  # ポートへデータを書き込む。
  # 設定された値をポートに書き込む。
  #
  # @param self
  # @param value 書き込み対象データ
  #
  # @return 書き込み処理結果(書き込み成功:true、書き込み失敗:false)
  #
  # @else
  #
  # @endif
  # bool operator<<(DataType& value)
  def write(self, value=None):
    if not value:
      value=self._value

    global usec_per_sec
    
    if self._OnWrite:
      self._OnWrite(value)

    timeout = self._writeTimeout

    tm_pre = Time()

    # blocking and timeout wait
    count = 0
    while self._writeBlock and self._buffer.isFull():
      if self._writeTimeout < 0:
        time.sleep(self._timeoutTick/usec_per_sec)
        continue
      
        
      # timeout wait
      tm_cur = Time()

      sec  = tm_cur.sec - tm_pre.sec
      usec = tm_cur.usec - tm_pre.usec

      timeout -= (sec * usec_per_sec + usec)

      if timeout < 0:
        break
      tm_pre = tm_cur
      time.sleep(self._timeoutTick/usec_per_sec)
      count += 1
      
    if self._buffer.isFull():
      if self._OnOverflow:
        self._OnOverflow(value)
      return False
      
    if not self._OnWriteConvert:
      self._buffer.put(value)
    else:
      self._buffer.put(self._OnWriteConvert(value))

    self.notify()
    return True


  ##
  # @if jp
  #
  # @brief データ読み出し
  #
  # DataPort から値を読み出す
  #
  # - コールバックファンクタ OnRead がセットされている場合、
  #   DataPort が保持するバッファから読み出す前に OnRead が呼ばれる。
  # - DataPort が保持するバッファがアンダーフローを検出できるバッファで、
  #   かつ、読み出す際にバッファがアンダーフローを検出した場合、
  #   コールバックファンクタ OnUnderflow が呼ばれる。
  # - コールバックファンクタ OnReadConvert がセットされている場合、
  #   バッファ書き込み時に、 OnReadConvert の operator() の戻り値が
  #   read()の戻り値となる。
  # - setReadTimeout() により読み出し時のタイムアウトが設定されている場合、
  #   バッファアンダーフロー状態が解除されるまでタイムアウト時間だけ待ち、
  #   OnUnderflow がセットされていればこれを呼び出して戻る
  #
  # @param self
  # @param value 読み出したデータ
  #
  # @return 読み出し処理実行結果(読み出し成功:true、読み出し失敗:false)
  #
  # @else
  #
  # @brief Read data
  #
  # @endif
  def read(self, value):
    if self._OnRead:
      self._OnRead()

    timeout = self._readTimeout
    tm_pre = Time()

    # blocking and timeout wait
    while self._readBlock and self._buffer.isEmpty():
      if self._readTimeout < 0:
        time.sleep(self._timeoutTick/usec_per_sec)
        continue

      # timeout wait
      tm_cur = Time()
      sec  = tm_cur.sec - tm_pre.sec
      usec = tm_cur.usec - tm_pre.usec
      
      timeout -= (sec * usec_per_sec + usec)
      if timeout < 0:
        break
      tm_pre = tm_cur
      time.sleep(self._timeoutTick/usec_per_sec)

    if self._buffer.isEmpty():
      if self._OnUnderflow:
        value[0] = self._OnUnderflow()
        return False
      else:
        return False

    if not self._OnReadConvert:
      value[0] = self._buffer.get()
      return True
    else:
      value[0] = self._OnReadConvert(self._buffer.get())
      return true

    # never comes here
    return False


  ##
  # @if jp
  #
  # @brief データ読み出し処理のブロックモードの設定
  #
  # 読み出し処理に対してブロックモードを設定する。
  # ブロックモードを指定した場合、読み出せるデータを受信するかタイムアウト
  # が発生するまで、 read() メソッドの呼びだしがブロックされる。
  #
  # @param self
  # @param block ブロックモードフラグ
  #
  # @else
  #
  # @brief Set read() block mode
  #
  # @endif
  def setReadBlock(self, block):
    self._readBlock = block


  ##
  # @if jp
  #
  # @brief データ書き込み処理のブロックモードの設定
  #
  # 書き込み処理に対してブロックモードを設定する。
  # ブロックモードを指定した場合、バッファに書き込む領域ができるか
  # タイムアウトが発生するまで write() メソッドの呼びだしがブロックされる。
  #
  # @param self
  # @param block ブロックモードフラグ
  #
  # @else
  #
  # @brief Set read() block mode
  #
  # @endif
  def setWriteBlock(self, block):
    self._writeBlock = block


  ##
  # @if jp
  #
  # @brief 読み出し処理のタイムアウト時間の設定
  # 
  # read() のタイムアウト時間を usec で設定する。
  # read() はブロックモードでなければならない。
  #
  # @param self
  # @param timeout タイムアウト時間 [usec]
  #
  # @else
  #
  # @brief Set read() timeout
  #
  # @endif
  def setReadTimeout(self, timeout):
    self._readTimeout = timeout


  ##
  # @if jp
  #
  # @brief 書き込み処理のタイムアウト時間の設定
  # 
  # write() のタイムアウト時間を usec で設定する。
  # write() はブロックモードでなければならない。
  #
  # @param self
  # @param timeout タイムアウト時間 [usec]
  #
  # @else
  #
  # @brief Set write() timeout
  #
  # @endif
  def setWriteTimeout(self, timeout):
    self._writeTimeout = timeout


  ##
  # @if jp
  #
  # @brief OnWrite コールバックの設定
  #
  # データ書き込み直前に呼ばれる OnWrite コールバックファンクタを設定する。
  #
  # @param self
  # @param on_write OnWrite コールバックファンクタ
  #
  # @else
  #
  # @brief Set OnWrite callback
  #
  # @endif
  def setOnWrite(self, on_write):
    self._OnWrite = on_write


  ##
  # @if jp
  #
  # @brief OnWriteConvert コールバックの設定
  #
  # データ書き込み時に呼ばれる OnWriteConvert コールバックファンクタを設定
  # する。
  # このコールバック関数の処理結果が書き込まれる。
  # このため書き込みデータのフィルタリングが可能となる。
  #
  # @param self
  # @param on_wconvert OnWriteConvert コールバックファンクタ
  #
  # @else
  #
  # @brief Set OnWriteConvert callback
  #
  # @endif
  def setOnWriteConvert(self, on_wconvert):
    self._OnWriteConvert = on_wconvert


  ##
  # @if jp
  #
  # @brief OnOverflow コールバックの設定
  #
  # バッファフルによりデータ書き込みができない場合に呼び出される OnOverflow
  # コールバックファンクタを設定する。
  #
  # @param self
  # @param on_overflow OnOverflow コールバックファンクタ
  #
  # @else
  #
  # @brief Set OnOverflow callback
  #
  # @endif
  def setOnOverflow(self, on_overflow):
    self._OnOverflow = on_overflow


  ##
  # @if jp
  #
  # @brief OnRead コールバックの設定
  #
  # データ読み出し直前に呼び出される OnRead コールバックファンクタを設定
  # する。
  #
  # @param self
  # @param on_read OnRead コールバックファンクタ
  #
  # @else
  #
  # @brief Set OnRead callback
  #
  # @endif
  def setOnRead(self, on_read):
    self._OnRead = on_read


  ##
  # @if jp
  #
  # @brief OnReadConvert コールバックの設定
  #
  # データ読み出し時に呼ばれる OnReadConvert コールバックファンクタを設定
  # する。
  # このコールバック関数の処理結果が読み込まれる。
  # このため読み込みデータのフィルタリングが可能となる。
  #
  # @param self
  # @param on_rconvert OnReadConvert コールバックファンクタ
  #
  # @else
  #
  # @brief Set OnReadConvert callback
  #
  # @endif
  def setOnReadConvert(self, on_rconvert):
    self._OnReadConvert = on_rconvert


  ##
  # @if jp
  #
  # @brief OnUnderflow コールバックの設定
  #
  # バッファエンプティにより読み出せるデータがない場合に呼び出される
  # コールバックファンクタ OnUnderflow を設定する。
  #
  # @param self
  # @param on_underflow OnUnderflow コールバックファンクタ
  #
  # @else
  #
  # @brief Set OnUnderflow callback
  #
  # @endif
  def setOnUnderflow(self, on_underflow):
    self._OnUnderflow = on_underflow


  ##
  # @if jp
  #
  # @brief データ型名取得用メソッド
  #
  # データの型名を取得するため、InPortCorbaProviderから呼ばれる。
  # 
  # @param self
  #
  # @return バッファに設定されているデータの型名
  #
  # @else
  #
  # @endif
  def getPortDataType(self):
    val = any.to_any(self._value)
    return str(val.typecode().name())
