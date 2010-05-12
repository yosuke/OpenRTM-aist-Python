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
# @class ConnectCallback
# @brief connect/notify_connect() 時のコールバック抽象クラス
#
# Portに対してconnect/notify_connect() 等が呼び出される時に呼び出される
# コールバックファンクタ。引数に RTC::ConnectorProfile を取る。
#
# @param profile ConnectorProfile
#
# @since 1.0.0
#
# @else
# @class ConnectCallback
# @brief Callback functor abstract for connect/notify_connect() funcs
#
# This is the interface for callback functor for connect/notify_connect()
# invocation in Port. Argument is RTC::ConnectorProfile that is given
# these functions.
#
# @param profile ConnectorProfile
#
# @since 1.0.0
#
# @endif
#
class ConnectionCallback:
  def __del__(self):
    pass

  # virtual void operator()(RTC::ConnectorProfile& profile) = 0;
  def __call__(self, profile):
    pass


##
# @if jp
# @class DisconnectCallback
# @brief disconnect/notify_disconnect() 時のコールバック抽象クラス
#
# Portに対してdisconnect/notify_disconnect() 等が呼び出される時に呼び出される
# コールバックファンクタ。引数に接続IDを取る。
#
# @param connector_id Connector ID
#
# @since 1.0.0
#
# @else
# @class DisconnectCallback
# @brief Callback functor abstract for disconnect/notify_disconnect() funcs
#
# This is the interface for callback functor for 
# disconnect/notify_disconnect() invocation in Port.
# Argument is connector ID is given these functions.
#
# @param connector_id Connector ID
#
# @since 1.0.0
#
# @endif
#
class DisconnectCallback:
  def __del__(self):
    pass


  # virtual void operator()(const char* connector_id) = 0;
  def __call__(self, connector_id):
    pass


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
