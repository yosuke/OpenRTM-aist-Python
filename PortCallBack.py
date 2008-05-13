#!/usr/bin/env python
# -*- coding: euc-jp -*-


##
# @file PortCallBack.py
# @brief PortCallBack class
# @date $Date: 2007/09/20 $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
# 
# Copyright (C) 2006-2008
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.
 

#============================================================
# callback functor base classes
#

##
# @if jp
# @class OnWrite
# @brief write() 時のコールバッククラス(サブクラス実装用)
#
# DataPortのバッファにデータがwrite()される直前に呼び出されるコールバック用<BR>
# ※サブクラスでの実装参照用
#
# @param DataType バッファに書き込むデータ型
#
# @since 0.4.0
#
# @else
# @class OnPut
# @brief OnPut abstract class
#
# @endif
class OnWrite:
  def __call__(self, value):
    pass



##
# @if jp
# @class OnWriteConvert
# @brief write() 時のデータ変換コールバッククラス(サブクラス実装用)
#
# InPort/OutPortのバッファにデータが write()される時に呼び出される<BR>
# ※サブクラスでの実装参照用
# コールバック用インターフェース。
# このコールバックの戻り値がバッファに格納される。
#
# @since 0.4.0
#
# @else
# @class OnWriteConvert
# @brief OnWriteConvert abstract class
#
# @endif
class OnWriteConvert:
  def __call__(self,value):
    pass



##
# @if jp
# @class OnRead
# @brief read() 時のコールバッククラス(サブクラス実装用)
#
# InPort/OutPortのバッファからデータが read()される直線に呼び出される
# コールバック用インターフェース。<BR>
# ※サブクラスでの実装参照用
#
# @since 0.4.0
#
# @else
# @class OnRead
# @brief OnRead abstract class
#
# @endif
class OnRead:
  def __call__(self):
    pass



##
# @if jp
# @class OnReadConvert
# @brief read() 時のデータ変換コールバッククラス(サブクラス実装用)
#
# InPort/OutPortのバッファからデータが read()される際に呼び出される
# コールバック用インターフェース。
# このコールバックの戻り値がread()の戻り値となる。<BR>
# ※サブクラスでの実装参照用
#
# @since 0.4.0
#
# @else
# @class OnReadConvert
# @brief OnReadConvert abstract class
#
# @endif
class OnReadConvert:
  def __call__(self,value):
    pass



##
# @if jp
# @class OnOverflow
# @brief バッファオーバーフロー時のコールバッククラス(サブクラス実装用)
#
# InPort/OutPortのバッファにデータがput()される時、バッファオーバーフローが
# 生じた場合に呼ばれるコールバックメソッド。<BR>
# ※サブクラスでの実装参照用
#
# @since 0.4.0
#
# @else
# @class OnOverflow
# @brief OnOverflow abstract class
#
# @endif
class OnOverflow:
  def __call__(self,value):
    pass


##
# @if jp
# @class OnUnderflow
# @brief Underflow 時のコールバッククラス(サブクラス実装用)
#
# @since 0.4.0
#
# InPort/OutPortのバッファにデータがread()される時に、読み出すべきデータが
# ない場合に呼び出されるコールバックインタフェース。
# このコールバックの戻り値がread()の戻り値となる。<BR>
# ※サブクラスでの実装参照用
#
# @else
# @class OnUnderflow
# @brief OnUnderflow abstract class
#
# @endif
class OnUnderflow:
  def __call__(self,value):
    pass
