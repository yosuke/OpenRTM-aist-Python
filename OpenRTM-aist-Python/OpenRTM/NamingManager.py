#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file NamingManager.py
# @brief naming Service helper class
# @date $Date: 2007/08/27$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.


import threading
import traceback
import sys

import OpenRTM_aist



##
# @if jp
# @class ScopedLock
# @brief ScopedLock クラス
#
# 排他処理用ロッククラス。
#
# @since 0.4.0
#
# @else
#
# @endif
class ScopedLock:



  ##
  # @if jp
  # @brief コンストラクタ
  #
  # コンストラクタ
  #
  # @param self
  # @param mutex ロック用ミューテックス
  #
  # @else
  #
  # @endif
  def __init__(self, mutex):
    self.mutex = mutex
    self.mutex.acquire()


  ##
  # @if jp
  # @brief デストラクタ
  #
  # デストラクタ
  #
  # @param self
  #
  # @else
  #
  # @endif
  def __del__(self):
    self.mutex.release()



##
# @if jp
#
# @class NamingBase
# @brief NamingService 管理用抽象クラス
#
# NamingServer 管理用抽象インターフェースクラス。
# 具象管理クラスは、以下の関数の実装を提供しなければならない。
# - bindObject() : 指定したオブジェクトのNamingServiceへのバインド
# - unbindObject() : 指定したオブジェクトのNamingServiceからのアンバインド
#
# @since 0.4.0
#
# @else
#
# @endif
class NamingBase:



  ##
  # @if jp
  #
  # @brief NamingServiceへバインドする関数(サブクラス実装用)
  #
  # 指定したオブジェクトをNamingServiceへバインドする<BR>
  # ※サブクラスでの実装参照用
  #
  # @param self
  # @param name バインド時の名称
  # @param rtobj バインド対象オブジェクト
  #
  # @else
  #
  # @endif
  def bindObject(self, name, rtobj):
    pass


  ##
  # @if jp
  #
  # @brief NamingServiceからアンバインドする関数(サブクラス実装用)
  #
  # 指定したオブジェクトをNamingServiceからアンバインドする<BR>
  # ※サブクラスでの実装参照用
  #
  # @param self
  # @param name アンバインド対象オブジェクト
  #
  # @else
  #
  # @endif
  def unbindObject(self, name):
    pass



##
# @if jp
#
# @class NamingOnCorba
# @brief CORBA 用 NamingServer 管理クラス
#
# CORBA 用 NamingServer 管理用クラス。
# CORBA コンポーネントのNamingServiceへの登録、解除などを管理する。
#
# @since 0.4.0
#
# @else
#
# @biref ModuleManager class
#
# @endif
class NamingOnCorba(NamingBase):



  ##
  # @if jp
  #
  # @brief コンストラクタ
  #
  # コンストラクタ
  #
  # @param self
  # @param orb ORB
  # @param names NamingServer 名称
  #
  # @else
  #
  # @endif
  def __init__(self, orb, names):
    self._cosnaming = OpenRTM_aist.CorbaNaming(orb,names)


  ##
  # @if jp
  #
  # @brief 指定した CORBA オブジェクトのNamingServiceへバインド
  # 
  # 指定した CORBA オブジェクトを指定した名称で CORBA NamingService へ
  # バインドする。
  # 
  # @param self
  # @param name バインド時の名称
  # @param rtobj バインド対象オブジェクト
  #
  # @else
  #
  # @endif
  def bindObject(self, name, rtobj):
    try:
      self._cosnaming.rebindByString(name, rtobj.getObjRef(), True)
    except:
      pass


  ##
  # @if jp
  #
  # @brief 指定した CORBA オブジェクトをNamingServiceからアンバインド
  # 
  # 指定した CORBA オブジェクトを CORBA NamingService からアンバインドする。
  # 
  # @param self
  # @param name アンバインド対象オブジェクト
  #
  # @else
  #
  # @endif
  def unbindObject(self, name):
    try:
      self._cosnaming.unbind(name)
    except:
      traceback.print_exception(*sys.exc_info())



##
# @if jp
#
# @class NamingManager
# @brief NamingServer 管理クラス
#
# NamingServer 管理用クラス。
# コンポーネントのNamingServiceへの登録、解除などを管理する。
#
# @since 0.4.0
#
# @else
#
# @biref ModuleManager class
#
# @endif
class NamingManager:
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
  # @param manager マネージャオブジェクト
  #
  # @else
  #
  # @endif
  def __init__(self, manager):
    self._manager = manager
    self._rtcout = manager.getLogbuf()
    #self._rtcout.setLogLevel(manager.getConfig().getProperty("logger.log_level"))
    #self._rtcout.setLogLock(OpenRTM_aist.toBool(manager.getConfig().getProperty("logger.stream_lock"), "enable", "disable", False))
    self._names = []
    self._namesMutex = threading.RLock()
    self._compNames = []
    self._compNamesMutex = threading.RLock()


  ##
  # @if jp
  #
  # @brief NameServer の登録
  #
  # 指定した形式の NameServer を登録する。
  # 現在指定可能な形式は CORBA のみ。
  #
  # @param self
  # @param method NamingService の形式
  # @param name_server 登録する NameServer の名称
  #
  # @else
  #
  # @endif
  def registerNameServer(self, method, name_server):
    self._rtcout.RTC_TRACE("NamingManager::registerNameServer(%s, %s)",
                           (method, name_server))
    name = self.createNamingObj(method, name_server)
    self._names.append(self.Names(method, name_server, name))


  ##
  # @if jp
  #
  # @brief 指定したオブジェクトのNamingServiceへバインド
  # 
  # 指定したオブジェクトを指定した名称で CORBA NamingService へバインドする。
  # 
  # @param self
  # @param name バインド時の名称
  # @param rtobj バインド対象オブジェクト
  #
  # @else
  #
  # @endif
  def bindObject(self, name, rtobj):
    self._rtcout.RTC_TRACE("NamingManager::bindObject(%s)", name)
    guard = ScopedLock(self._namesMutex)
    for i in range(len(self._names)):
      if self._names[i].ns:
        self._names[i].ns.bindObject(name, rtobj)
    self.registerCompName(name, rtobj)

  def bindManagerObject(self, name, mgr):
    self._rtcout.RTC_TRACE("NamingManager::bindManagerObject(%s)", name)
    guard = ScopedLock(self._namesMutex)
    for i in range(len(self._names)):
      if self._names[i].ns:
        self._names[i].ns.bindObject(name, mgr)


  ##
  # @if jp
  #
  # @brief NamingServer の情報の更新
  # 
  # 設定されている NameServer 内に登録されているオブジェクトの情報を
  # 更新する。
  # 
  # @param self
  # 
  # @else
  #
  # @endif
  def update(self):
    self._rtcout.RTC_TRACE("NamingManager::update()")
    guard = ScopedLock(self._namesMutex)
    for i in range(len(self._names)):
      if self._names[i].ns is None:
        nsobj = self.createNamingObj(self._names[i].method,
                                     self._names[i].nsname)
        if nsobj:
          self._rtcout.RTC_INFO("New name server found: %s/%s",
                                (self._names[i].method,
                                 self._names[i].nsname))
          self._names[i].ns = nsobj
          self.bindCompsTo(nsobj)


  ##
  # @if jp
  #
  # @brief 指定したオブジェクトをNamingServiceからアンバインド
  # 
  # 指定したオブジェクトを NamingService からアンバインドする。
  # 
  # @param self
  # @param name アンバインド対象オブジェクト
  #
  # @else
  #
  # @endif
  def unbindObject(self, name):
    self._rtcout.RTC_TRACE("NamingManager::unbindObject(%s)", name)
    guard = ScopedLock(self._namesMutex)
    for i in range(len(self._names)):
      if self._names[i].ns:
        self._names[i].ns.unbindObject(name)
    self.unregisterCompName(name)


  ##
  # @if jp
  #
  # @brief 全てのオブジェクトをNamingServiceからアンバインド
  # 
  # 全てのオブジェクトを CORBA NamingService からアンバインドする。
  # 
  # @param self
  # 
  # @else
  #
  # @endif
  def unbindAll(self):
    self._rtcout.RTC_TRACE("NamingManager::unbindAll(): %d names.", len(self._compNames))
    guard = ScopedLock(self._compNamesMutex)
    for i in range(len(self._compNames)):
      self.unbindObject(self._compNames[i].name)


  ##
  # @if jp
  #
  # @brief バインドされている全てのオブジェクトを取得
  # 
  # バインドされている全てのオブジェクトを 取得する。
  # 
  # @param self
  #
  # @return バインド済みオブジェクト リスト
  # 
  # @else
  #
  # @endif
  def getObjects(self):
    comps = []
    guard = ScopedLock(self._compNamesMutex)
    for i in range(len(self._compNames)):
      comps.append(self._compNames[i].rtobj)
    return comps


  ##
  # @if jp
  #
  # @brief NameServer 管理用オブジェクトの生成
  # 
  # 指定した型のNameServer 管理用オブジェクトを生成する。
  #
  # @param self
  # @param method NamingService 形式
  # @param name_server NameServer 名称
  # 
  # @return 生成した NameServer オブジェクト
  # 
  # @else
  #
  # @endif
  def createNamingObj(self, method, name_server):
    mth = method
    if mth == "corba":
      try:
        name = OpenRTM_aist.NamingOnCorba(self._manager.getORB(),name_server)
        if name is None:
          return None
        self._rtcout.RTC_INFO("NameServer connection succeeded: %s/%s",
                              (method, name_server))
        return name
      except:
        self._rtcout.RTC_INFO("NameServer connection failed: %s/%s",
                              (method, name_server))
        return None

    return None


  ##
  # @if jp
  #
  # @brief 設定済みコンポーネントを NameServer に登録
  # 
  # 設定済みコンポーネントを指定した NameServer に登録する。
  #
  # @param self
  # @param ns 登録対象 NameServer
  # 
  # @else
  #
  # @endif
  def bindCompsTo(self, ns):
    for i in range(len(self._compNames)):
      ns.bindObject(self._compNames[i].name, self._compNames[i].rtobj)


  ##
  # @if jp
  #
  # @brief NameServer に登録するコンポーネントの設定
  # 
  # NameServer に登録するコンポーネントを設定する。
  #
  # @param self
  # @param name コンポーネントの登録時名称
  # @param rtobj 登録対象オブジェクト
  # 
  # @else
  #
  # @endif
  def registerCompName(self, name, rtobj):
    for i in range(len(self._compNames)):
      if self._compNames[i].name == name:
        self._compNames[i].rtobj = rtobj
        return

    self._compNames.append(self.Comps(name, rtobj))
    return


  ##
  # @if jp
  #
  # @brief NameServer に登録するコンポーネントの設定解除
  # 
  # NameServer に登録するコンポーネントの設定を解除する。
  #
  # @param self
  # @param name 設定解除対象コンポーネントの名称
  # 
  # @else
  #
  # @endif
  def unregisterCompName(self, name):
    len_ = len(self._compNames)
    for i in range(len_):
      idx = (len_-1) - i
      if self._compNames[idx].name == name:
        del self._compNames[idx]
        return
    return
    


  # Name Servers' method/name and object
  ##
  # @if jp
  # @class Names
  # @brief NameServer 管理用クラス
  # @else
  #
  # @endif
  class Names:
    def __init__(self, meth, name, naming):
      self.method = meth
      self.nsname = name
      self.ns     = naming


  # Components' name and object
  ##
  # @if jp
  # @class Comps
  # @brief コンポーネント管理用クラス
  # @else
  #
  # @endif
  class Comps:
    def __init__(self, n, obj):
      self.name = n
      self.rtobj = obj
