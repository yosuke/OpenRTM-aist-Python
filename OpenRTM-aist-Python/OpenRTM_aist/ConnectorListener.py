#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file  ConnectorListener.py
# @brief connector listener class
# @date  $Date$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2009
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

from omniORB import *
from omniORB import any

import OpenRTM_aist


##
# @if jp
# @brief ConnectorDataListener のタイプ
#
# - ON_BUFFER_WRITE:          バッファ書き込み時
# - ON_BUFFER_FULL:           バッファフル時
# - ON_BUFFER_WRITE_TIMEOUT:  バッファ書き込みタイムアウト時
# - ON_BUFFER_OVERWRITE:      バッファ上書き時
# - ON_BUFFER_READ:           バッファ読み出し時
# - ON_SEND:                  InProtへの送信時
# - ON_RECEIVED:              InProtへの送信完了時
# - ON_RECEIVER_FULL:         InProt側バッファフル時
# - ON_RECEIVER_TIMEOUT:      InProt側バッファタイムアウト時
# - ON_RECEIVER_ERROR:        InProt側エラー時
#
# @else
# @brief The types of ConnectorDataListener
# 
# - ON_BUFFER_WRITE:          At the time of buffer write
# - ON_BUFFER_FULL:           At the time of buffer full
# - ON_BUFFER_WRITE_TIMEOUT:  At the time of buffer write timeout
# - ON_BUFFER_OVERWRITE:      At the time of buffer overwrite
# - ON_BUFFER_READ:           At the time of buffer read
# - ON_SEND:                  At the time of sending to InPort
# - ON_RECEIVED:              At the time of finishing sending to InPort
# - ON_RECEIVER_FULL:         At the time of bufferfull of InPort
# - ON_RECEIVER_TIMEOUT:      At the time of timeout of InPort
# - ON_RECEIVER_ERROR:        At the time of error of InPort
#
# @endif
#
class ConnectorDataListenerType:
    def __init__(self):
        pass

    ON_BUFFER_WRITE              = 0
    ON_BUFFER_FULL               = 1
    ON_BUFFER_WRITE_TIMEOUT      = 2
    ON_BUFFER_OVERWRITE          = 3
    ON_BUFFER_READ               = 4
    ON_SEND                      = 5
    ON_RECEIVED                  = 6
    ON_RECEIVER_FULL             = 7
    ON_RECEIVER_TIMEOUT          = 8
    ON_RECEIVER_ERROR            = 9
    CONNECTOR_DATA_LISTENER_NUM  = 10



##
# @if jp
# @class ConnectorDataListener クラス
#
# データポートの Connector において発生する各種イベントに対するコー
# ルバックを実現するリスナクラスの基底クラス。
#
# @else
# @class ConnectorDataListener class
#
# This class is abstract base class for listener classes that
# provides callbacks for various events in the data port's
# connectors.
#
# @endif
#
class ConnectorDataListener:
    def __del__(self):
        pass

    # virtual void operator()(const ConnectorInfo& info,
    #                         const cdrMemoryStream& data) = 0;
    def __call__(self, info, data):
        pass



##
# @if jp
# @class ConnectorDataListenerT クラス
#
# データポートの Connector において発生する各種イベントに対するコー
# ルバックを実現するリスナクラスの基底クラス。
# 
# このクラスは、operator()() の第2引数に cdrMemoryStream 型ではなく、
# 実際にデータポートで使用される変数型をテンプレート引数として
# 渡すことができる。
#
# @else
# @class ConnectorDataListenerT class
#
# This class is abstract base class for listener classes that
# provides callbacks for various events in the data port's
# connectors.
#
# This class template can have practical data types that are used
# as typed variable for DataPort as an argument of template instead
# of cdrMemoryStream.
#
# @endif
#
class ConnectorDataListenerT(ConnectorDataListener):
    def __del__(self):
        pass


    # virtual void operator()(const ConnectorInfo& info,
    #                         const cdrMemoryStream& cdrdata)
    def __call__(self, info, cdrdata, data):
        endian = info.properties.getProperty("serializer.cdr.endian","little")
        if endian is not "little" and endian is not None:
            endian = OpenRTM_aist.split(endian, ",") # Maybe endian is ["little","big"]
            endian = OpenRTM_aist.normalize(endian) # Maybe self._endian is "little" or "big"

        if endian == "little":
            endian = True
        elif endian == "big":
            endian = False
        else:
            endian = True

        _data = cdrUnmarshal(any.to_any(data).typecode(), cdrdata, endian)
        return _data



##
# @if jp
# @brief ConnectorListener のタイプ
#  
# - ON_BUFFER_EMPTY:       バッファが空の場合
# - ON_BUFFER_READTIMEOUT: バッファが空でタイムアウトした場合
# - ON_SENDER_EMPTY:       OutPort側バッファが空
# - ON_SENDER_TIMEOUT:     OutPort側タイムアウト時
# - ON_SENDER_ERROR:       OutPort側エラー時
# - ON_CONNECT:            接続確立時
# - ON_DISCONNECT:         接続切断時
#
# @else
# @brief The types of ConnectorListener
# 
# - ON_BUFFER_EMPTY:       At the time of buffer empty
# - ON_BUFFER_READTIMEOUT: At the time of buffer read timeout
# - ON_BUFFER_EMPTY:       At the time of empty of OutPort
# - ON_SENDER_TIMEOUT:     At the time of timeout of OutPort
# - ON_SENDER_ERROR:       At the time of error of OutPort
# - ON_CONNECT:            At the time of connection
# - ON_DISCONNECT:         At the time of disconnection
#
# @endif
#
# enum ConnectorListenerType
class ConnectorListenerType:

    def __init__(self):
        pass

    ON_BUFFER_EMPTY        = 0
    ON_BUFFER_READ_TIMEOUT = 1
    ON_SENDER_EMPTY        = 2
    ON_SENDER_TIMEOUT      = 3
    ON_SENDER_ERROR        = 4
    ON_CONNECT             = 5
    ON_DISCONNECT          = 6
    CONNECTOR_LISTENER_NUM = 7



##
# @if jp
# @class ConnectorListener クラス
#
# データポートの Connector において発生する各種イベントに対するコー
# ルバックを実現するリスナクラスの基底クラス。
#
# @else
# @class ConnectorListener class
#
# This class is abstract base class for listener classes that
# provides callbacks for various events in the data port's
# connectors.
#
# @endif
#
class ConnectorListener:
    def __del__(self):
        pass

    # virtual void operator()(const ConnectorInfo& info) = 0;
    def __call__(self,  info):
        pass



##
# @if jp
# @class ConnectorDataListener ホルダクラス
#
# 複数の ConnectorDataListener を保持し管理するクラス。
#
# @else
# @class ConnectorDataListener holder class
#
# This class manages one ore more instances of ConnectorDataListener class.
#
# @endif
#
class ConnectorDataListenerHolder:
    def __init__(self):
        self._listeners = []
        return


    def __del__(self):
        for listener in self._listeners:
            for (k,v) in listener.iteritems():
                if v:
                    del k
        return

    
    # void addListener(ConnectorDataListener* listener, bool autoclean);
    def addListener(self, listener, autoclean):
        self._listeners.append({listener:autoclean})
        return

    
    # void removeListener(ConnectorDataListener* listener);
    def removeListener(self, listener):
        for (i, _listener) in enumerate(self._listeners):
            if listener in _listener:
                del self._listeners[i][listener]
                return

    
    # void notify(const ConnectorInfo& info,
    #             const cdrMemoryStream& cdrdata);
    def notify(self, info, cdrdata):
        for listener in self._listeners:
            for (k,v) in listener.iteritems():
                k(info, cdrdata)
        return


##
# @if jp
# @class ConnectorListener ホルダクラス
#
# 複数の ConnectorListener を保持し管理するクラス。
#
# @else
# @class ConnectorListener holder class
#
# This class manages one ore more instances of ConnectorListener class.
#
# @endif
#
class ConnectorListenerHolder:

    def __init__(self):
        self._listeners = []
        return

    
    def __del__(self):
        for listener in self._listeners:
            for (k,v) in listener.iteritems():
                if v:
                    del k
        return
        
    
    # void addListener(ConnectorListener* listener, bool autoclean);
    def addListener(self, listener, autoclean):
        self._listeners.append({listener:autoclean})
        return


    # void removeListener(ConnectorListener* listener);
    def removeListener(self, listener):
        for (i, _listener) in enumerate(self._listeners):
            if listener in _listener:
                del self._listeners[i][listener]
                return


    # void notify(const ConnectorInfo& info);
    def notify(self, info):
        for listener in self._listeners:
            for (k,v) in listener.iteritems():
                k(info)
        return


  
class ConnectorListeners:
    def __init__(self):
        self.connectorData_ = [ OpenRTM_aist.ConnectorDataListenerHolder() for i in range(OpenRTM_aist.ConnectorDataListenerType.CONNECTOR_DATA_LISTENER_NUM) ]
        self.connector_     = [ OpenRTM_aist.ConnectorListenerHolder() for i in range(OpenRTM_aist.ConnectorListenerType.CONNECTOR_LISTENER_NUM) ]
        return
