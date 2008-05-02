#!/usr/bin/env python
# -#- coding: euc-jp -#-


##
# @file TimeValue.py
# @brief TimeValue class
# @date $Date: 2007/08/23$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2007-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.


import OpenRTM

##
# @if jp
# @class TimeValue
# @brief 時間計算用クラス
# 
# 指定した時間値を保持するためのクラス。
# 時間値に対する各種計算用オペレーションを提供する。
#
# @since 0.4.0
#
# @else
#
# @endif
class TimeValue:
  """
  """



  ##
  # @if jp
  #
  # @brief コンストラクタ
  # 
  # コンストラクタ
  # 指定された秒，マイクロ秒で初期化する。
  #
  # @param self
  # @param sec 秒(デフォルト値:None)
  # @param usec マイクロ秒(デフォルト値:None)
  # 
  # @else
  #
  # @endif
  def __init__(self, sec=None, usec=None):
    if sec is None:
      self.tv_sec = 0
    else:
      self.tv_sec = float(sec)

    if usec is None:
      self.tv_usec = 0
    else:
      self.tv_usec = float(usec)


  ##
  # @if jp
  #
  # @brief 時間減算
  # 
  # 設定された時間から引数で与えられた時間を減算する。
  #
  # @param self
  # @param tm 減算時間
  # 
  # @return 減算結果
  # 
  # @else
  #
  # @endif
  def __sub__(self, tm):
    try:
      res = TimeValue()
    except:
      res = OpenRTM.TimeValue()
    
    if self.tv_sec >= tm.tv_sec:
      if self.tv_usec >= tm.tv_usec:
        res.tv_sec  = self.tv_sec  - tm.tv_sec
        res.tv_usec = self.tv_usec - tm.tv_usec
      else:
        res.tv_sec  = self.tv_sec  - tm.tv_sec - 1
        res.tv_usec = (self.tv_usec + 1000000) - tm.tv_usec
    else:
      if tm.tv_usec >= self.tv_usec:
        res.tv_sec  = -(tm.tv_sec  - self.tv_sec)
        res.tv_usec = -(tm.tv_usec - self.tv_usec)
      else:
        res.tv_sec  = -(tm.tv_sec - self.tv_sec - 1)
        res.tv_usec = -(tm.tv_usec + 1000000) + self.tv_usec
    return res


  ##
  # @if jp
  #
  # @brief 時間加算
  # 
  # 設定された時間に引数で与えられた時間を加算する。
  #
  # @param self
  # @param tm 加算時間
  # 
  # @return 加算結果
  # 
  # @else
  #
  # @endif
  def __add__(self, tm):
    res = TimeValue()
    res.tv_sec  = self.tv_sec  + tm.tv_sec
    res.tv_usec = self.tv_usec + tm.tv_usec
    if res.tv_usec > 1000000:
      res.tv_sec += 1
      res.tv_usec -= 1000000
    return res

  ##
  # @if jp
  #
  # @brief double型→時間型変換
  # 
  # 引数で与えられたdouble型を時間型に変換する。
  #
  # @param self
  # @param time 変換元値
  # 
  # @return 変換結果
  # 
  # @else
  #
  # @endif
  def set_time(self, time):
    self.tv_sec  = long(time)
    self.tv_usec = long((time - float(self.tv_sec))*1000000)
    return self

  ##
  # @if jp
  #
  # @brief 時間型→double型変換
  # 
  # 保持している内容をdouble型に変換する。
  #
  # @param self
  # @return double型変換結果
  # 
  # @else
  #
  # @endif
  def toDouble(self):
    return float(self.tv_sec) + float(self.tv_usec/1000000.0)


  ##
  # @if jp
  # @brief 設定時間を出力する
  #
  # 設定時間を文字列出力する。<br>
  #
  # @param self
  #
  # @return 設定時間文字列表示
  #
  # @else
  #
  # @endif
  def __str__(self):
    return str(self.tv_sec + self.tv_usec/1000000.0)

  ##
  # @if jp
  # @brief 符号判定
  #
  # 保持している内容の符号を判定する。<br>
  #
  # @param self
  #
  # @return 正ならば1を、負ならば-1を、0ならば0
  #
  # @else
  #
  # @endif
  def sign(self):
    if self.tv_sec > 0:
      return 1
    if self.tv_sec < 0:
      return -1
    if self.tv_usec > 0:
      return 1
    if self.tv_usec < 0:
      return -1
    return 0
