#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file InPort.py
# @brief InPort template class
# @date $Date: 2007/09/20 $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
# 
# Copyright (C) 2003-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

from omniORB import any
import sys
import traceback

import OpenRTM

TIMEOUT_TICK_USEC = 10.0
USEC_PER_SEC      = 1000000.0
TIMEOUT_TICK_SEC = TIMEOUT_TICK_USEC/USEC_PER_SEC


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
    tm = time.time()
    tm_f       = tm - int(tm)     # 小数部の取り出し
    self.sec   = int(tm - tm_f)   # 整数部の取り出し
    self.usec  = int(tm_f * USEC_PER_SEC) # sec -> usec (micro second)



##
# @if jp
#
# @class InPort
#
# @brief InPort クラス
# 
# InPort の実装クラス。
# InPort は内部にリングバッファを持ち、外部から送信されたデータを順次
# このリングバッファに格納する。リングバッファのサイズはデフォルトで64と
# なっているが、コンストラクタ引数によりサイズを指定することができる。
# データはフラグによって未読、既読状態が管理され、isNew(), getNewDataLen()
# getNewList(), getNewListReverse() 等のメソッドによりハンドリングすることが
# できる。
#
# @since 0.2.0
#
# @else
#
# @class InPort
#
# @brief InPort template class
#
# This class template provides interfaces to input port.
# Component developer can define input value, which act as input
# port from other components, using this template.
# This is class template. This class have to be incarnated class as port
# value types. This value types are previously define RtComponent IDL.
# ex. type T: TimedFload, TimedLong etc... 
#
# @since 0.2.0
#
# @endif
class InPort:
  """
  """



  ##
  # @if jp
  #
  # @brief コンストラクタ
  #
  # コンストラクタ。
  #
  # @param self
  # @param name InPort 名。InPortBase:name() により参照される。
  # @param value この InPort にバインドされる変数
  # @param buffer_ InPort が内部に保持するバッファ
  # @param read_block 読込ブロックフラグ。
  #        データ読込時に未読データがない場合、次のデータ受信までブロックする
  #        かどうかを設定(デフォルト値:False)
  # @param write_block 書込ブロックフラグ。
  #        データ書込時にバッファがフルであった場合、バッファに空きができる
  #        までブロックするかどうかを設定(デフォルト値:False)
  # @param read_timeout 読込ブロックを指定していない場合の、データ読取タイム
  #        アウト時間(ミリ秒)(デフォルト値:0)
  # @param write_timeout 書込ブロックを指定していない場合の、データ書込タイム
  #        アウト時間(ミリ秒)(デフォルト値:0)
  #
  # @else
  #
  # @brief A constructor.
  #
  # Setting channel name and registering channel value.
  #
  # @param self
  # @param name A name of the InPort. This name is referred by
  #             InPortBase::name().
  # @param value A channel value related with the channel.
  # @param buffer_ Buffer length of internal ring buffer of InPort 
  # @param read_block
  # @param write_block
  # @param read_timeout
  # @param write_timeout
  #
  # @endif
  def __init__(self, name, value, buffer_,
         read_block=False, write_block=False,
         read_timeout=0, write_timeout = 0):
    self._buffer         = buffer_
    self._name           = name
    self._value          = value
    self._readBlock      = read_block
    self._readTimeout    = read_timeout
    self._writeBlock     = write_block
    self._writeTimeout   = write_timeout
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
  # @brief ポート名称を取得する。
  #
  # ポート名称を取得する。
  #
  # @param self
  #
  # @return ポート名称
  #
  # @else
  #
  # @endif
  def name(self):
    return self._name


  ##
  # @if jp
  #
  # @brief DataPort に値を書き込む
  #
  # DataPort に値を書き込む。
  #
  # - コールバックファンクタ OnWrite がセットされている場合、
  #   InPort が保持するバッファに書き込む前に OnWrite が呼ばれる。
  # - InPort が保持するバッファがオーバーフローを検出できるバッファであり、
  #   かつ、書き込む際にバッファがオーバーフローを検出した場合、
  #   コールバックファンクタ OnOverflow が呼ばれる。
  # - コールバックファンクタ OnWriteConvert がセットされている場合、
  #   バッファ書き込み時に、OnWriteConvert の operator()() の戻り値が
  #   バッファに書き込まれる。
  # - setWriteTimeout() により書き込み時のタイムアウトが設定されている場合、
  #   タイムアウト時間だけバッファフル状態が解除するのを待ち、
  #   OnOverflowがセットされていればこれを呼び出して戻る。
  #
  # @param self
  # @param value 書込対象データ
  #
  # @return 書込処理結果(書込成功:true、書込失敗:false)
  #
  # @else
  #
  # @brief 
  #
  # @endif
  def write(self, value):
    if self._OnWrite:
      self._OnWrite(value)

    timeout = self._writeTimeout

    tm_pre = Time()

    # blocking and timeout wait
    while self._writeBlock and self._buffer.isFull():
      if self._writeTimeout < 0:
        time.sleep(TIMEOUT_TICK_SEC)
        continue

      # timeout wait
      tm_cur = Time()

      sec  = tm_cur.sec - tm_pre.sec
      usec = tm_cur.usec - tm_pre.usec

      timeout -= (sec * USEC_PER_SEC + usec)

      if timeout < 0:
        break

      tm_pre = tm_cur
      time.sleep(TIMEOUT_TICK_USEC)

    if self._buffer.isFull() and self._OnOverflow:
      self._OnOverflow(value)
      return False

    if not self._OnWriteConvert:
      self._buffer.put(value)
    else:
      self._buffer.put(self._OnWriteConvert(value))

    return True


  ##
  # @if jp
  #
  # @brief DataPort から値を読み出す
  #
  # DataPort から値を読み出す
  #
  # - コールバックファンクタ OnRead がセットされている場合、
  #   DataPort が保持するバッファから読み出す前に OnRead が呼ばれる。
  # - DataPort が保持するバッファがアンダーフローを検出できるバッファで、
  #   かつ、読み出す際にバッファがアンダーフローを検出した場合、
  #   コールバックファンクタ OnUnderflow が呼ばれる。
  # - コールバックファンクタ OnReadConvert がセットされている場合、
  #   バッファ書き込み時に、OnReadConvert の operator()() の戻り値が
  #   read()の戻り値となる。
  # - setReadTimeout() により読み出し時のタイムアウトが設定されている場合、
  #   バッファアンダーフロー状態が解除されるまでタイムアウト時間だけ待ち、
  #   OnUnderflowがセットされていればこれを呼び出して戻る
  #
  # @param self
  #
  # @return 読み出したデータ
  #
  # @else
  #
  # @brief [CORBA interface] Put data on InPort
  #
  # @endif
  def read(self):
    if self._OnRead:
      self._OnRead()

    timeout = self._readTimeout

    tm_pre = Time()

    # blocking and timeout wait
    while self._readBlock and self._buffer.isEmpty():
      if self._readTimeout < 0:
        time.sleep(TIMEOUT_TICK_SEC)
        continue

      # timeout wait
      tm_cur = Time()

      sec  = tm_cur.sec - tm_pre.sec
      usec = tm_cur.usec - tm_pre.usec
      
      timeout -= (sec * USEC_PER_SEC + usec)

      if timeout < 0:
        break

      tm_pre = tm_cur
      time.sleep(TIMEOUT_TICK_SEC)

    if self._buffer.isEmpty():
      if self._OnUnderflow:
        self._value = self._OnUnderflow()
      return self._value

    if not self._OnReadConvert:
      self._value = self._buffer.get()
      return self._value
    else:
      self._value = self._OnReadConvert(self._buffer.get())
      return self._value

    # never comes here
    return self._value


  ##
  # @if jp
  #
  # @brief InPort 内のリングバッファの値を初期化(サブクラス実装用)
  #
  # InPort 内のリングバッファの値を指定した値で初期化する。<BR>
  # ※サブクラスでの実装時参照用
  #
  # @param self
  # @param value 初期化対象データ
  #
  # @else
  #
  # @brief Initialize ring buffer value of InPort
  #
  # @endif
  def init(self, value):
    pass


  ##
  # @if jp
  #
  # @brief バインドされた変数に InPort バッファの最新値を読み込む
  #
  # バインドされたデータに InPort の最新値を読み込む。
  # コンストラクタで変数と InPort がバインドされていなければならない。
  # このメソッドはポリモーフィックに使用される事を前提としているため、
  # 型に依存しない引数、戻り値となっている。
  #
  # @param self
  #
  # @else
  #
  # @brief Read into bound T-type data from current InPort
  #
  # @endif
  def update(self):
    try:
      self._value = self._buffer.get()
    except:
      if self._OnUnderflow:
        self._OnUnderflow()
      else:
        traceback.print_exception(*sys.exc_info())
        
    return


  ##
  # @if jp
  #
  # @brief 未読の新しいデータ数を取得する
  #
  # バッファ内の未読データ数を取得する。
  #
  # @param self
  #
  # @return 未読データ数
  #
  # @else
  #
  # @brief Get number of new data to be read.
  #
  # @endif
  def getNewDataLen(self):
    return self._buffer.new_data_len()


  ##
  # @if jp
  #
  # @brief 未読の新しいデータを取得する
  #
  # バッファ内の未読データリストを取得する。
  #
  # @param self
  #
  # @return 未読データリスト
  #
  # @else
  #
  # \brief Get new data to be read.
  #
  # @endif
  def getNewList(self):
    return self._buffer.get_new_list()


  ##
  # @if jp
  #
  # @brief 未読の新しいデータを逆順(新->古)で取得する
  #
  # バッファ内の未読データを逆順(新->古)でリスト化し、取得する。
  #
  # @param self
  #
  # @return 未読データリスト
  #
  # @else
  #
  # \brief Get new data to be read.
  #
  # @endif
  def getNewListReverse(self):
    return self._buffer.get_new_rlist()


  ##
  # @if jp
  #
  # @brief InPort バッファへデータ入力時のコールバックの設定
  #
  # InPort が持つバッファにデータがputされたときに呼ばれるコールバック
  # オブジェクトを設定する。設定されるコールバックオブジェクトは
  # 引数に value を持ち、戻り値 void の __call__ 関数を実装している必要がある。
  #
  # <pre>
  # class MyOnWrite:
  #     def __call__(self, value):
  #       処理<br>
  # </pre>
  # のようにコールバックオブジェクトを実装し、<br> 
  # m_inport.setOnWrite(new MyOnWrite());<br>
  # のようにコールバックオブジェクトをセットする。
  #
  # @param self
  # @param on_write 設定対象コールバックオブジェクト
  #
  # @else
  #
  # @brief Get new data to be read.
  #
  # @endif
  def setOnWrite(self, on_write):
    self._OnWrite = on_write


  ##
  # @if jp
  #
  # @brief InPort バッファへデータ書き込み時のコールバックの設定
  #
  # InPort が持つバッファにデータ書き込まれる時に呼ばれるコールバック
  # オブジェクトを設定する。バッファにはコールバックオブジェクトの
  # 戻り値が設定される。
  # 
  # @param self
  # @param on_wconvert 設定対象コールバックオブジェクト
  #
  # @else
  #
  # @endif
  def setOnWriteConvert(self, on_wconvert):
    self._OnWriteConvert = on_wconvert


  ##
  # @if jp
  #
  # @brief InPort バッファへデータ読み込み時のコールバックの設定
  #
  # InPort が持つバッファからデータが読み込まれる直前に呼ばれるコールバック
  # オブジェクトを設定する。
  # 
  # @param self
  # @param on_read 設定対象コールバックオブジェクト
  #
  # @else
  #
  # @endif
  def setOnRead(self, on_read):
    self._OnRead = on_read


  ##
  # @if jp
  #
  # @brief InPort バッファへデータ読み出し時のコールバックの設定
  #
  # InPort が持つバッファからデータが読み出される際に呼ばれるコールバック
  # オブジェクトを設定する。コールバックオブジェクトの戻り値がread()メソッド
  # の呼出結果となる。
  # 
  # @param self
  # @param on_rconvert 設定対象コールバックオブジェクト
  #
  # @else
  #
  # @endif
  def setOnReadConvert(self, on_rconvert):
    self._OnReadConvert = on_rconvert


  ##
  # @if jp
  #
  # @brief InPort バッファへバッファオーバーフロー時のコールバックの設定
  #
  # InPort が持つバッファでバッファオーバーフローが検出された際に呼び出される
  # コールバックオブジェクトを設定する。
  # 
  # @param self
  # @param on_overflow 設定対象コールバックオブジェクト
  #
  # @else
  #
  # @endif
  def setOnOverflow(self, on_overflow):
    self._OnOverflow = on_overflow


  ##
  # @if jp
  #
  # @brief InPort バッファへバッファアンダーフロー時のコールバックの設定
  #
  # InPort が持つバッファでバッファアンダーフローが検出された際に呼び出される
  # コールバックオブジェクトを設定する。
  # 
  # @param self
  # @param on_underflow 設定対象コールバックオブジェクト
  #
  # @else
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
