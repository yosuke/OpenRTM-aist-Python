#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file Manager.py
# @brief RTComponent manager class
# @date $Date: $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

import threading
import string
import signal, os
import sys
import traceback
import time
from omniORB import CORBA
from types import IntType, ListType

import OpenRTM
import RTC
import SDOPackage



#------------------------------------------------------------
# static var
#------------------------------------------------------------

##
# @if jp
# @brief 唯一の Manager へのポインタ
# @else
# @brief The pointer to the Manager
# @endif
manager = None

##
# @if jp
# @brief 唯一の Manager へのポインタに対する mutex
# @else
# @brief The mutex of the pointer to the Manager 
# @endif
mutex = threading.RLock()


##
# @if jp
# @brief 終了処理
#
# マネージャを終了させる
#
# @param signum シグナル番号
# @param frame 現在のスタックフレーム
#
# @else
#
# @endif
def handler(signum, frame):
  mgr = OpenRTM.Manager.instance()
  mgr.terminate()



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
# @class Manager
# @brief Manager クラス
#
# コンポーネントなど各種の情報管理を行うマネージャクラス。
#
# @since 0.2.0
#
# @else
# @class Manager
# @brief Manager class
# @endif
class Manager:
  """
  """



  ##
  # @if jp
  # @brief コピーコンストラクタ
  #
  # コピーコンストラクタ
  #
  # @param self
  # @param _manager コピー元マネージャオブジェクト(デフォルト値:None)
  #
  # @else
  # @brief Protected Copy Constructor
  #
  # @endif
  def __init__(self, _manager=None):
    self._initProc   = None
    self._runner     = None
    self._terminator = None
    self._compManager = OpenRTM.ObjectManager(self.InstanceName)
    self._factory = OpenRTM.ObjectManager(self.FactoryPredicate)
    self._ecfactory = OpenRTM.ObjectManager(self.ECFactoryPredicate)
    self._terminate = self.Term()
    self._ecs = []
    self._timer = None
    signal.signal(signal.SIGINT, handler)
    
    return


  ##
  # @if jp
  # @brief マネージャの初期化
  #
  # マネージャを初期化する static 関数。
  # マネージャをコマンドライン引数を与えて初期化する。
  # マネージャを使用する場合は、必ずこの初期化メンバ関数 init() を
  # 呼ばなければならない。
  # マネージャのインスタンスを取得する方法として、init(), instance() の
  # 2つの static 関数が用意されているが、初期化はinit()でしか行われないため、
  # Manager の生存期間の一番最初にはinit()を呼ぶ必要がある。
  #
  # ※マネージャの初期化処理
  # - initManager: 引数処理、configファイルの読み込み、サブシステム初期化
  # - initLogger: Logger初期化
  # - initORB: ORB 初期化
  # - initNaming: NamingService 初期化
  # - initExecutionContext: ExecutionContext factory 初期化
  # - initTimer: Timer 初期化
  #
  # @param argv コマンドライン引数
  # 
  # @return Manager の唯一のインスタンスの参照
  #
  # @else
  # @brief Initializa manager
  #
  # This is the static function to tintialize the Manager.
  # The Manager is initialized by given arguments.
  # At the starting the manager, this static function "must" be called from
  # application program. The manager has two static functions to get 
  # the instance, "init()" and "instance()". Since initializing
  # process is only performed by the "init()" function, the "init()" has
  # to be called at the beginning of the lifecycle of the Manager.
  # function.
  #
  # @param argv The array of the command line arguments.
  #
  # @endif
  def init(*arg):
    global manager
    global mutex
    
    if len(arg) == 1:
      argv = arg[0]
    elif len(arg) == 2 and \
             isinstance(arg[0], IntType) and \
             isinstance(arg[1], ListType):
      argv = arg[1]
    else:
      print "Invalid arguments for init()"
      print "init(argc,argv) or init(argv)"
        
    if manager is None:
      guard = ScopedLock(mutex)
      if manager is None:
        manager = Manager()
        manager.initManager(argv)
        manager.initLogger()
        manager.initORB()
        manager.initNaming()
        manager.initExecContext()
        manager.initTimer()

    return manager
  
  init = staticmethod(init)


  ##
  # @if jp
  # @brief マネージャのインスタンスの取得
  #
  # マネージャのインスタンスを取得する static 関数。
  # この関数を呼ぶ前に、必ずこの初期化関数 init() が呼ばれている必要がある。
  #
  # @return Manager の唯一のインスタンスの参照
  # 
  # @else
  #
  # @brief Get instance of the manager
  #
  # This is the static function to get the instance of the Manager.
  # Before calling this function, ensure that the initialization function
  # "init()" is called.
  #
  # @return The only instance reference of the manager
  #
  # @endif
  def instance():
    global manager
    global mutex
    
    if manager is None:
      guard = ScopedLock(mutex)
      if manager is None:
        manager = Manager()
        manager.initManager(None)
        manager.initLogger()
        manager.initORB()
        manager.initNaming()
        manager.initExecContext()
        manager.initTimer()

    return manager

  instance = staticmethod(instance)


  ##
  # @if jp
  # @brief マネージャ終了処理
  #
  # マネージャの終了処理を実行する。
  #
  # @param self
  #
  # @else
  #
  # @endif
  def terminate(self):
    if self._terminator:
      self._terminator.terminate()


  ##
  # @if jp
  # @brief マネージャ・シャットダウン
  #
  # マネージャの終了処理を実行する。
  # ORB終了後、同期を取って終了する。
  #
  # @param self
  #
  # @else
  #
  # @endif
  def shutdown(self):
    self._rtcout.RTC_DEBUG("Manager::shutdown()")
    self.shutdownComponents()
    self.shutdownNaming()
    self.shutdownORB()
    self.shutdownManager()

    if self._runner:
      self._runner.wait()
    else:
      self.join()

    self.shutdownLogger()


  ##
  # @if jp
  # @brief マネージャ終了処理の待ち合わせ
  #
  # 同期を取るため、マネージャ終了処理の待ち合わせを行う。
  #
  # @param self
  #
  # @else
  #
  # @endif
  def join(self):
    self._rtcout.RTC_DEBUG("Manager::wait()")
    guard = ScopedLock(self._terminate.mutex)
    self._terminate.waiting += 1
    del guard
    while 1:
      guard = ScopedLock(self._terminate.mutex)
      #if self._terminate.waiting > 1:
      if self._terminate.waiting > 0:
        break
      del guard
      time.sleep(0.001)


  ##
  # @if jp
  #
  # @brief 初期化プロシージャのセット
  #
  # このオペレーションはユーザが行うモジュール等の初期化プロシージャ
  # を設定する。ここで設定されたプロシージャは、マネージャが初期化され、
  # アクティブ化された後、適切なタイミングで実行される。
  #
  # @param self
  # @param proc 初期化プロシージャの関数ポインタ
  #
  # @else
  #
  # @brief Run the Manager
  #
  # This operation sets the initial procedure call to process module
  # initialization, other user defined initialization and so on.
  # The given procedure will be called at the proper timing after the 
  # manager initialization, activation and run.
  #
  # @param proc A function pointer to the initial procedure call
  #
  # @endif
  def setModuleInitProc(self, proc):
    self._initProc = proc
    return


  ##
  # @if jp
  #
  # @brief Managerのアクティブ化
  #
  # このオペレーションは以下の処理を行う
  # - CORBA POAManager のアクティブ化
  # - マネージャCORBAオブジェクトのアクティブ化
  # - Manager オブジェクトへの初期化プロシージャの実行
  #
  # このオペレーションは、マネージャの初期化後、runManager()
  # の前に呼ぶ必要がある。
  #
  # @param self
  #
  # @return 処理結果(アクティブ化成功:true、失敗:false)
  #
  # @else
  #
  # @brief Activate Manager
  #
  # This operation do the following,
  # - Activate CORBA POAManager
  # - Activate Manager CORBA object
  # - Execute the initial procedure call of the Manager
  #
  # This operationo should be invoked after Manager:init(),
  # and before tunManager().
  #
  # @endif
  def activateManager(self):
    self._rtcout.RTC_DEBUG("Manager::activateManager()")

    try:
      self.getPOAManager().activate()
      if self._initProc:
        self._initProc(self)
    except:
      print "Exception: Manager.activateManager()"
      return False

    return True


  ##
  # @if jp
  #
  # @brief Managerの実行
  #
  # このオペレーションはマネージャのメインループを実行する。
  # このメインループ内では、CORBA ORBのイベントループ等が
  # 処理される。デフォルトでは、このオペレーションはブロックし、
  # Manager::destroy() が呼ばれるまで処理を戻さない。
  # 引数 no_block が true に設定されている場合は、内部でイベントループ
  # を処理するスレッドを起動し、ブロックせずに処理を戻す。
  #
  # @param self
  # @param no_block false: ブロッキングモード, true: ノンブロッキングモード
  #
  # @else
  #
  # @brief Run the Manager
  #
  # This operation processes the main event loop of the Manager.
  # In this main loop, CORBA's ORB event loop or other processes
  # are performed. As the default behavior, this operation is going to
  # blocking mode and never returns until manager::destroy() is called.
  # When the given argument "no_block" is set to "true", this operation
  # creates a thread to process the event loop internally, and it doesn't
  # block and returns.
  #
  # @param no_block false: Blocking mode, true: non-blocking mode.
  #
  # @endif
  def runManager(self, no_block=None):
    if no_block is None:
      no_block = False

    if no_block:
      self._rtcout.RTC_DEBUG("Manager::runManager(): non-blocking mode")
      self._runner = self.OrbRunner(self._orb)
      # self._runnner.open()
    else:
      self._rtcout.RTC_DEBUG("Manager::runManager(): blocking mode")
      self._orb.run()
      self._rtcout.RTC_DEBUG("Manager::runManager(): ORB was terminated")
      self.join()
    return


  ##
  # @if jp
  # @brief [CORBA interface] モジュールのロード
  #
  # 指定したコンポーネントのモジュールをロードするとともに、
  # 指定した初期化関数を実行する。
  #
  # @param self
  # @param fname   モジュールファイル名
  # @param initfunc 初期化関数名
  # 
  # @else
  #
  # @brief [CORBA interface] Load module
  #
  # Load module (shared library, DLL etc..) by file name,
  # and invoke initialize function.
  #
  # @param fname    The module file name
  # @param initfunc The initialize function name
  #
  # @endif
  def load(self, fname, initfunc):
    self._rtcout.RTC_DEBUG("Manager::load()")
    self._module.load(fname, initfunc)
    return


  ##
  # @if jp
  #
  # @brief モジュールのアンロード
  #
  # モジュールをアンロードする
  #
  # @param self
  # @param fname モジュールのファイル名
  # 
  # @else
  #
  # @brief Unload module
  #
  # Unload shared library.
  #
  # @param pathname Module file name
  #
  # @endif
  def unload(self, fname):
    self._rtcout.RTC_DEBUG("Manager::unload()")
    self._module.unload(fname)
    return


  ##
  # @if jp
  #
  # @brief 全モジュールのアンロード
  #
  # モジュールをすべてアンロードする
  #
  # @param self
  #
  # @else
  #
  # @brief Unload module
  #
  # Unload all loaded shared library.
  #
  # @endif
  def unloadAll(self):
    self._rtcout.RTC_DEBUG("Manager::unloadAll()")
    self._module.unloadAll()
    return


  ##
  # @if jp
  # @brief ロード済みのモジュールリストを取得する
  #
  # 現在マネージャにロードされているモジュールのリストを取得する。
  #
  # @param self
  #
  # @return ロード済みモジュールリスト
  #
  # @else
  # @brief Get loaded module names
  # @endif
  def getLoadedModules(self):
    self._rtcout.RTC_DEBUG("Manager::getLoadedModules()")
    return self._module.getLoadedModules()


  ##
  # @if jp
  # @brief ロード可能なモジュールリストを取得する
  #
  # ロード可能モジュールのリストを取得する。
  # (現在はModuleManager側で未実装)
  #
  # @param self
  #
  # @return ロード可能モジュール　リスト
  #
  # @else
  # @brief Get loadable module names
  # @endif
  def getLoadableModules(self):
    self._rtcout.RTC_DEBUG("Manager::getLoadableModules()")
    return self._module.getLoadableModules()


  #============================================================
  # Component Factory Management
  #============================================================

  ##
  # @if jp
  # @brief RTコンポーネント用ファクトリを登録する
  #
  # RTコンポーネントのインスタンスを生成するための
  # Factoryを登録する。
  #
  # @param self
  # @param profile RTコンポーネント プロファイル
  # @param new_func RTコンポーネント生成用関数
  # @param delete_func RTコンポーネント破棄用関数
  #
  # @return 登録処理結果(登録成功:true、失敗:false)
  #
  # @else
  # @brief Register RT-Component Factory
  # @endif
  def registerFactory(self, profile, new_func, delete_func):
    self._rtcout.RTC_DEBUG("Manager::registerFactory(%s)", profile.getProperty("type_name"))
    try:
      factory = OpenRTM.FactoryPython(profile, new_func, delete_func)
      self._factory.registerObject(factory)
      return True
    except:
      return False


  ##
  # @if jp
  # @brief ExecutionContext用ファクトリを登録する
  #
  # ExecutionContextのインスタンスを生成するためのFactoryを登録する。
  #
  # @param self
  # @param name 生成対象ExecutionContext名称
  # @param new_func ExecutionContext生成用関数
  # @param delete_func ExecutionContext破棄用関数
  #
  # @return 登録処理結果(登録成功:true、失敗:false)
  #
  # @else
  # @brief Register ExecutionContext Factory
  # @endif
  def registerECFactory(self, name, new_func, delete_func):
    self._rtcout.RTC_DEBUG("Manager::registerECFactory(%s)", name)
    try:
      self._ecfactory.registerObject(OpenRTM.ECFactoryPython(name, new_func, delete_func))
      return True
    except:
      return False

    return False


  ##
  # @if jp
  # @brief ファクトリ全リストを取得する
  #
  # 登録されているファクトリの全リストを取得する。
  #
  # @param self
  #
  # @return 登録ファクトリ リスト
  #
  # @else
  # @brief Get the list of all RT-Component Factory
  # @endif
  def getModulesFactories(self):
    self._rtcout.RTC_DEBUG("Manager::getModulesFactories()")

    self._modlist = []
    for _obj in self._factory._objects._obj:
      self._modlist.append(_obj.profile().getProperty("implementation_id"))
    return self._modlist


  #============================================================
  # Component management
  #============================================================

  ##
  # @if jp
  # @brief RTコンポーネントを生成する
  #
  # 指定したRTコンポーネントのインスタンスを登録されたFactory経由で生成する。
  # インスタンス生成が成功した場合、併せて以下の処理を実行する。
  #  - 外部ファイルで設定したコンフィギュレーション情報の読み込み，設定
  #  - ExecutionContextのバインド，動作開始
  #  - ネーミングサービスへの登録
  #
  # @param self
  # @param module_name 生成対象RTコンポーネント名称
  #
  # @return 生成したRTコンポーネントのインスタンス
  #
  # @else
  # @brief Create RT-Component
  # @endif
  def createComponent(self, module_name):
    self._rtcout.RTC_DEBUG("Manager::createComponent(%s)", module_name)

    obj = self._factory.find(module_name)
    comp = obj.create(self)
    if comp is None:
      return None
    self._rtcout.RTC_DEBUG("RTC Created: %s", module_name)

    self.configureComponent(comp)

    if comp.initialize() != RTC.RTC_OK:
      self._rtcout.RTC_DEBUG("RTC initialization failed: %s", module_name)
      comp.exit()
      self._rtcout.RTC_DEBUG("%s was finalized", module_name)
      return None

    self._rtcout.RTC_DEBUG("RTC initialization succeeded: %s", module_name)
    self.bindExecutionContext(comp)
    self.registerComponent(comp)
    return comp


  ##
  # @if jp
  # @brief RTコンポーネントを直接 Manager に登録する
  #
  # 指定したRTコンポーネントのインスタンスをファクトリ経由ではなく
  # 直接マネージャに登録する。
  #
  # @param self
  # @param comp 登録対象RTコンポーネントのインスタンス
  #
  # @return 登録処理結果(登録成功:true、失敗:false)
  #
  # @else
  # @brief Register RT-Component directly without Factory
  # @endif
  def registerComponent(self, comp):
    self._rtcout.RTC_DEBUG("Manager::registerComponent(%s)", comp.getInstanceName())

    self._compManager.registerObject(comp)
    names = comp.getNamingNames()

    for name in names:
      self._rtcout.RTC_DEBUG("Bind name: %s", name)
      self._namingManager.bindObject(name, comp)

    return True

  
  ##
  # @if jp
  # @brief RTコンポーネントの登録を解除する
  #
  # 指定したRTコンポーネントの登録を解除する。
  #
  # @param self
  # @param comp 登録解除対象RTコンポーネントのインスタンス
  #
  # @return 登録解除処理結果(解除成功:true、解除失敗:false)
  #
  # @else
  # @brief Register RT-Component directly without Factory
  # @endif
  def unregisterComponent(self, comp):
    self._rtcout.RTC_DEBUG("Manager::unregisterComponent(%s)", comp.getInstanceName())
    self._compManager.unregisterObject(comp.getInstanceName())
    names = comp.getNamingNames()
    
    for name in names:
      self._rtcout.RTC_DEBUG("Unbind name: %s", name)
      self._namingManager.unbindObject(name)

    return True


  ##
  # @if jp
  # @brief RTコンポーネントにExecutionContextをバインドする
  #
  # 指定したRTコンポーネントにExecutionContextをバインドする。
  # バインドするExecutionContextの型はプロパティ・ファイルの
  # "exec_cxt.periodic.type"属性によって指定する。
  #
  # @param self
  # @param comp バインド対象RTコンポーネントのインスタンス
  #
  # @return バインド処理結果(バインド成功:true、失敗:false)
  #
  # @else
  # @brief Register RT-Component directly without Factory
  # @endif
  def bindExecutionContext(self, comp):
    self._rtcout.RTC_DEBUG("Manager::bindExecutionContext()")
    self._rtcout.RTC_DEBUG("ExecutionContext type: %s",
                 self._config.getProperty("exec_cxt.periodic.type"))

    rtobj = comp.getObjRef()

    exec_cxt = None

    if OpenRTM.isDataFlowParticipant(rtobj):
      ectype = self._config.getProperty("exec_cxt.periodic.type")
      exec_cxt = self._ecfactory.find(ectype).create()
      rate = self._config.getProperty("exec_cxt.periodic.rate")
      exec_cxt.set_rate(float(rate))
    else:
      ectype = self._config.getProperty("exec_cxt.evdriven.type")
      exec_cxt = self._ecfactory.find(ectype).create()
    exec_cxt.add(rtobj)
    exec_cxt.start()
    self._ecs.append(exec_cxt)
    return True


  ##
  # @if jp
  # @brief Manager に登録されているRTコンポーネントを削除する(未実装)
  #
  # マネージャに登録されているRTコンポーネントを削除する。
  #
  # @param self
  # @param instance_name 削除対象RTコンポーネントのインスタンス名
  #
  # @else
  # @brief Unregister RT-Component that is registered in the Manager
  # @endif
  def deleteComponent(self, instance_name):
    self._rtcout.RTC_DEBUG("Manager::deleteComponent(%s)", instance_name)


  ##
  # @if jp
  # @brief Manager に登録されているRTコンポーネントを検索する
  #
  # Manager に登録されているRTコンポーネントを指定した名称で検索し、
  # 合致するコンポーネントを取得する。
  #
  # @param self
  # @param instance_name 検索対象RTコンポーネントの名称
  #
  # @return 名称が一致するRTコンポーネントのインスタンス
  #
  # @else
  # @brief Get RT-Component's pointer
  # @endif
  def getComponent(self, instance_name):
    self._rtcout.RTC_DEBUG("Manager::getComponent(%s)", instance_name)
    return self._compManager.find(instance_name)


  ##
  # @if jp
  # @brief Manager に登録されている全RTコンポーネントを取得する
  #
  # Manager に登録されているRTコンポーネントの全インスタンスを取得する。
  #
  # @param self
  #
  # @return 全RTコンポーネントのインスタンスリスト
  #
  # @else
  # @brief Get all RT-Component's pointer
  # @endif
  def getComponents(self):
    self._rtcout.RTC_DEBUG("Manager::getComponents()")
    return self._compManager.getObjects()


  #============================================================
  # CORBA 関連
  #============================================================

  ##
  # @if jp
  # @brief ORB のポインタを取得する
  #
  # Manager に設定された ORB のポインタを取得する。
  #
  # @param self
  #
  # @return ORB オブジェクト
  #
  # @else
  # @brief Get the pointer to the ORB
  # @endif
  def getORB(self):
    self._rtcout.RTC_DEBUG("Manager::getORB()")
    return self._orb


  ##
  # @if jp
  # @brief Manager が持つ RootPOA のポインタを取得する
  #
  # Manager に設定された RootPOA へのポインタを取得する。
  #
  # @param self
  #
  # @return RootPOAオブジェクト
  #
  # @else
  # @brief Get the pointer to the RootPOA 
  # @endif
  def getPOA(self):
    self._rtcout.RTC_DEBUG("Manager::getPOA()")
    return self._poa


  ##
  # @if jp
  # @brief Manager が持つ POAManager を取得する
  #
  # Manager に設定された POAMAnager を取得する。
  #
  # @param self
  #
  # @return POAマネージャ
  #
  # @else
  #
  # @endif
  def getPOAManager(self):
    self._rtcout.RTC_DEBUG("Manager::getPOAManager()")
    return self._poaManager



  #============================================================
  # Manager initialize and finalization
  #============================================================

  ##
  # @if jp
  # @brief Manager の内部初期化処理
  # 
  # Manager の内部初期化処理を実行する。
  #  - Manager コンフィギュレーションの設定
  #  - ログ出力ファイルの設定
  #  - 終了処理用スレッドの生成
  #  - タイマ用スレッドの生成(タイマ使用時)
  #
  # @param self
  # @param argv コマンドライン引数
  # 
  # @else
  # @brief Manager internal initialization
  # @endif
  def initManager(self, argv):
    config = OpenRTM.ManagerConfig(argv)
    self._config = config.configure(OpenRTM.Properties())
    self._config.setProperty("logger.file_name",self.formatString(self._config.getProperty("logger.file_name"), self._config))

    self._module = OpenRTM.ModuleManager(self._config)
    self._terminator = self.Terminator(self)
    guard = ScopedLock(self._terminate.mutex)
    self._terminate.waiting = 0
    del guard

    if OpenRTM.toBool(self._config.getProperty("timer.enable"), "YES", "NO", True):
      tm = OpenRTM.TimeValue(0, 100000)
      tick = self._config.getProperty("timer.tick")
      if tick != "":
        tm = tm.set_time(float(tick))
        self._timer = OpenRTM.Timer(tm)
        self._timer.start()


  ##
  # @if jp
  # @brief Manager の終了処理(未実装)
  #
  # Manager を終了する
  # (ただし，現在は未実装)
  #
  # @param self
  #
  # @else
  #
  # @endif
  def shutdownManager(self):
    self._rtcout.RTC_DEBUG("Manager::shutdownManager()")
    if self._timer:
      self._timer.stop()


  #============================================================
  # Logger initialize and terminator
  #============================================================

  ##
  # @if jp
  # @brief System logger の初期化
  #
  # System logger の初期化を実行する。
  # コンフィギュレーションファイルに設定された情報に基づき、
  # ロガーの初期化，設定を実行する。
  #
  # @param self
  #
  # @return 初期化実行結果(初期化成功:true、初期化失敗:false)
  #
  # @else
  # @brief System logger initialization
  # @endif
  def initLogger(self):
    logfile = self._config.getProperty("logger.file_name")
    if logfile == "":
      logfile = "./rtc.log"

    if OpenRTM.toBool(self._config.getProperty("logger.enable"), "YES", "NO", True):
      self._Logbuf = OpenRTM.Logbuf(fileName = logfile)
      self._rtcout = OpenRTM.LogStream(self._Logbuf)
      self._rtcout.setLogLevel(self._config.getProperty("logger.log_level"))
      self._rtcout.setLogLock(OpenRTM.toBool(self._config.getProperty("logger.stream_lock"),
                          "enable", "disable", False))

      self._rtcout.RTC_INFO("%s", self._config.getProperty("openrtm.version"))
      self._rtcout.RTC_INFO("Copyright (C) 2003-2007")
      self._rtcout.RTC_INFO("  Noriaki Ando")
      self._rtcout.RTC_INFO("  Task-intelligence Research Group,")
      self._rtcout.RTC_INFO("  Intelligent Systems Research Institute, AIST")
      self._rtcout.RTC_INFO("Manager starting.")
      self._rtcout.RTC_INFO("Starting local logging.")
    else:
      self._rtcout = OpenRTM.LogStream()

    return True


  ##
  # @if jp
  # @brief System Logger の終了処理(未実装)
  #
  # System Loggerの終了処理を実行する。
  # (現在は未実装)
  #
  # @param self
  #
  # @else
  # @brief System Logger finalization
  # @endif
  def shutdownLogger(self):
    self._rtcout.RTC_DEBUG("Manager::shutdownLogger()")


  #============================================================
  # ORB initialization and finalization
  #============================================================

  ##
  # @if jp
  # @brief CORBA ORB の初期化処理
  #
  # 設定情報を元にORBを初期化する。
  #
  # @param self
  #
  # @return ORB 初期化処理結果(初期化成功:true、初期化失敗:false)
  #
  # @else
  # @brief CORBA ORB initialization
  # @endif
  def initORB(self):
    self._rtcout.RTC_DEBUG("Manager::initORB()")

    try:
      args = OpenRTM.split(self.createORBOptions(), " ")
      argv = OpenRTM.toArgv(args)
      self._orb = CORBA.ORB_init(argv)

      self._poa = self._orb.resolve_initial_references("RootPOA")

      if CORBA.is_nil(self._poa):
        self._rtcout.RTC_ERROR("Could not resolve RootPOA")
        return False

      self._poaManager = self._poa._get_the_POAManager()
      self._objManager = OpenRTM.CorbaObjectManager(self._orb, self._poa)
    except:
      self._rtcout.RTC_ERROR("Exception: Caught unknown exception in initORB().")
      return False

    return True


  ##
  # @if jp
  # @brief ORB のコマンドラインオプション作成
  #
  # コンフィギュレーション情報に設定された内容から
  # ORB の起動時オプションを作成する。
  #
  # @param self
  #
  # @return ORB 起動時オプション
  #
  # @else
  # @brief ORB command option creation
  # @endif
  def createORBOptions(self):
    opt      = self._config.getProperty("corba.args")
    corba    = self._config.getProperty("corba.id")
    endpoint = self._config.getProperty("corba.endpoint")

    if endpoint != "":
      if opt != "":
        opt += " "
      if corba == "omniORB":
        opt = "-ORBendPoint giop:tcp:" + endpoint
      elif corba == "TAO":
        opt = "-ORBEndPoint iiop://" + endpoint
      elif corba == "MICO":
        opt = "-ORBIIOPAddr inet:" + endpoint
    return opt


  ##
  # @if jp
  # @brief ORB の終了処理
  #
  # ORB の終了処理を実行する。
  # 実行待ちの処理が存在する場合には、その処理が終了するまで待つ。
  # 実際の終了処理では、POA Managerを非活性化し、 ORB のシャットダウンを実行
  # する。
  #
  # @param self
  #
  # @else
  # @brief ORB finalization
  # @endif
  def shutdownORB(self):
    self._rtcout.RTC_DEBUG("Manager::shutdownORB()")
    try:
      while self._orb.work_pending():
        self._rtcout.RTC_PARANOID("Pending work still exists.")
        if self._orb.work_pending():
          self._orb.perform_work()
    except:
      traceback.print_exception(*sys.exc_info())
      pass

    self._rtcout.RTC_DEBUG("No pending works of ORB. Shutting down POA and ORB.")

    if not CORBA.is_nil(self._poa):
      try:
        if not CORBA.is_nil(self._poaManager):
          self._poaManager.deactivate(False, True)
        self._rtcout.RTC_DEBUG("POA Manager was deactivated.")
        self._poa.destroy(False, True)
        self._poa = PortableServer.POA._nil
        self._rtcout.RTC_DEBUG("POA was destroid.")
      except CORBA.SystemException, ex:
        self._rtcout.RTC_ERROR("Caught SystemException during root POA destruction")
      except:
        self._rtcout.RTC_ERROR("Caught unknown exception during destruction")

    if self._orb:
      try:
        self._orb.shutdown(True)
        self._rtcout.RTC_DEBUG("ORB was shutdown.")
        self._orb = CORBA.Object._nil
      except CORBA.SystemException, ex:
        self._rtcout.RTC_ERROR("Caught CORBA::SystemException during ORB shutdown.")
      except:
        self._rtcout.RTC_ERROR("Caught unknown exception during ORB shutdown.")


  #============================================================
  # NamingService initialization and finalization
  #============================================================

  ##
  # @if jp
  # @brief NamingManager の初期化
  #
  # NamingManager の初期化処理を実行する。
  # ただし、 NamingManager を使用しないようにプロパティ情報に設定されている
  # 場合には何もしない。
  # NamingManager を使用する場合、プロパティ情報に設定されている
  # デフォルト NamingServer を登録する。
  # また、定期的に情報を更新するように設定されている場合には、指定された周期
  # で自動更新を行うためのタイマを起動するとともに、更新用メソッドをタイマに
  # 登録する。
  #
  # @param self
  #
  # @return 初期化処理結果(初期化成功:true、初期化失敗:false)
  #
  # @else
  #
  # @endif
  def initNaming(self):
    self._rtcout.RTC_DEBUG("Manager::initNaming()")
    self._namingManager = OpenRTM.NamingManager(self)

    if not OpenRTM.toBool(self._config.getProperty("naming.enable"), "YES", "NO", True):
      return True

    meths = OpenRTM.split(self._config.getProperty("naming.type"),",")
    
    for meth in meths:
      names = OpenRTM.split(self._config.getProperty(meth+".nameservers"), ",")
      for name in names:
        self._rtcout.RTC_DEBUG("Register Naming Server: %s/%s", (meth, name))
        self._namingManager.registerNameServer(meth,name)

    if OpenRTM.toBool(self._config.getProperty("naming.update.enable"), "YES", "NO", True):
      tm = OpenRTM.TimeValue(10,0)
      intr = self._config.getProperty("naming.update.interval")
      if intr != "":
        tm = OpenRTM.TimeValue(intr)

      if self._timer:
        self._timer.registerListenerObj(self._namingManager,OpenRTM.NamingManager.update,tm)
  
    return True


  ##
  # @if jp
  # @brief NamingManager の終了処理
  #
  # NamingManager を終了する。
  # 登録されている全要素をアンバインドし、終了する。
  #
  # @param self
  #
  # @else
  #
  # @endif
  def shutdownNaming(self):
    self._rtcout.RTC_DEBUG("Manager::shutdownNaming()")
    self._namingManager.unbindAll()


  ##
  # @if jp
  # @brief ExecutionContextManager の初期化
  #
  # 使用する各 ExecutionContext の初期化処理を実行し、各 ExecutionContext 
  # 生成用 Factory を ExecutionContextManager に登録する。
  #
  # @param self
  #
  # @return ExecutionContextManager 初期化処理実行結果
  #         (初期化成功:true、初期化失敗:false)
  #
  # @else
  #
  # @endif
  def initExecContext(self):
    self._rtcout.RTC_DEBUG("Manager::initExecContext()")
    OpenRTM.PeriodicExecutionContextInit(self)
    OpenRTM.ExtTrigExecutionContextInit(self)
    return True


  ##
  # @if jp
  # @brief Timer の初期化
  #
  # 使用する各 Timer の初期化処理を実行する。
  # (現状の実装では何もしない)
  #
  # @param self
  #
  # @return Timer 初期化処理実行結果(初期化成功:true、初期化失敗:false)
  #
  # @else
  #
  # @endif
  def initTimer(self):
    return True


  ##
  # @if jp
  # @brief NamingManager に登録されている全コンポーネントの終了処理
  #
  # NamingManager に登録されているRTコンポーネントおよび ExecutionContext の
  # リストを取得し、全コンポーネントを終了する。
  #
  # @param self
  #
  # @else
  #
  # @endif
  def shutdownComponents(self):
    self._rtcout.RTC_DEBUG("Manager::shutdownComponents()")
    comps = self._namingManager.getObjects()
    for comp in comps:
      try:
        comp.exit()
        p = OpenRTM.Properties(key=comp.getInstanceName())
        p.mergeProperties(comp.getProperties())
      except:
        traceback.print_exception(*sys.exc_info())
        pass

    for ec in self._ecs:
      try:
        self._poa.deactivate_object(self._poa.servant_to_id(ec))
      except:
        traceback.print_exception(*sys.exc_info())
        pass


  ##
  # @if jp
  # @brief RTコンポーネントの登録解除
  #
  # 指定したRTコンポーネントのインスタンスをネーミングサービスから
  # 登録解除する。
  #
  # @param self
  # @param comp 登録解除対象RTコンポーネント
  #
  # @else
  #
  # @endif
  def cleanupComponent(self, comp):
    self._rtcout.RTC_DEBUG("Manager::cleanupComponents")
    self.unregisterComponent(comp)


  ##
  # @if jp
  # @brief RTコンポーネントのコンフィギュレーション処理
  #
  # RTコンポーネントの型およびインスタンス毎に記載されたプロパティファイルの
  # 情報を読み込み、コンポーネントに設定する。
  # また、各コンポーネントの NamingService 登録時の名称を取得し、設定する。
  #
  # @param self
  # @param comp コンフィギュレーション対象RTコンポーネント
  #
  # @else
  #
  # @endif
  def configureComponent(self, comp):
    category  = comp.getCategory()
    type_name = comp.getTypeName()
    inst_name = comp.getInstanceName()

    type_conf = category + "." + type_name + ".config_file"
    name_conf = category + "." + inst_name + ".config_file"

    type_prop = OpenRTM.Properties()

    name_prop = OpenRTM.Properties()

    if self._config.getProperty(name_conf) != "":
      try:
        conff = open(self._config.getProperty(name_conf))
      except:
        print "Not found. : %s" % self._config.getProperty(name_conf)
      else:
        name_prop.load(conff)

    if self._config.getProperty(type_conf) != "":
      try:
        conff = open(self._config.getProperty(type_conf))
      except:
        print "Not found. : %s" % self._config.getProperty(type_conf)
      else:
        type_prop.load(conff)

    type_prop = type_prop.mergeProperties(name_prop)
    comp.getProperties().mergeProperties(type_prop)

    naming_formats = ""
    comp_prop = OpenRTM.Properties(prop=comp.getProperties())

    naming_formats += self._config.getProperty("naming.formats")
    naming_formats += ", " + comp_prop.getProperty("naming.formats")

    naming_formats = OpenRTM.flatten(OpenRTM.unique_sv(OpenRTM.split(naming_formats, ",")))

    naming_names = self.formatString(naming_formats, comp.getProperties())
    comp.getProperties().setProperty("naming.formats",naming_formats)
    comp.getProperties().setProperty("naming.names",naming_names)


  ##
  # @if jp
  # @brief プロパティ情報のマージ
  #
  # 指定されたファイル内に設定されているプロパティ情報をロードし、
  # 既存の設定済みプロパティとマージする。
  #
  # @param self
  # @param prop マージ対象プロパティ
  # @param file_name プロパティ情報が記述されているファイル名
  #
  # @return マージ処理実行結果(マージ成功:true、マージ失敗:false)
  #
  # @else
  #
  # @endif
  def mergeProperty(self, prop, file_name):
    if file_name == "":
      self._rtcout.RTC_ERROR("Invalid configuration file name.")
      return False

    if file_name[0] != '\0':
      
      try:
        conff = open(file_name)
      except:
        print "Not found. : %s" % file_name
      else:
        prop.load(conff)
        conff.close()
        return True

    return False

  ##
  # @if jp
  # @brief NamingServer に登録する際の登録情報を組み立てる
  #
  # 指定された書式とプロパティ情報を基に NameServer に登録する際の情報を
  # 組み立てる。
  # 各書式指定用文字の意味は以下のとおり
  # - % : コンテキストの区切り
  # - n : インスタンス名称
  # - t : 型名
  # - m : 型名
  # - v : バージョン
  # - V : ベンダー
  # - c : カテゴリ
  # - h : ホスト名
  # - M : マネージャ名
  # - p : プロセスID
  #
  # @param self
  # @param naming_format NamingService 登録情報書式指定
  # @param prop 使用するプロパティ情報
  #
  # @return 指定書式変換結果
  #
  # @else
  #
  # @endif
  def formatString(self, naming_format, prop):
    name_ = naming_format
    str_  = ""
    count = 0

    for n in name_:
      if n == '%':
        count+=1
        if not (count % 2):
          str_ += n
      else:
        if  count > 0 and (count % 2):
          count = 0
          if   n == "n": str_ += prop.getProperty("instance_name")
          elif n == "t": str_ += prop.getProperty("type_name")
          elif n == "m": str_ += prop.getProperty("type_name")
          elif n == "v": str_ += prop.getProperty("version")
          elif n == "V": str_ += prop.getProperty("vendor")
          elif n == "c": str_ += prop.getProperty("category")
          elif n == "h": str_ += self._config.getProperty("manager.os.hostname")
          elif n == "M": str_ += self._config.getProperty("manager.name")
          elif n == "p": str_ += str(self._config.getProperty("manager.pid"))
          else: str_ += n
        else:
          count = 0
          str_ += n

    return str_


  ##
  # @if jp
  # @brief ログバッファの取得
  #
  # マネージャに設定したログバッファを取得する。
  #
  # @param self
  #
  # @return マネージャに設定したログバッファ
  #
  # @else
  #
  # @endif
  def getLogbuf(self):
    return self._rtcout


  ##
  # @if jp
  # @brief マネージャコンフィギュレーションの取得
  #
  # マネージャに設定したコンフィギュレーションを取得する。
  #
  # @param self
  #
  # @return マネージャのコンフィギュレーション
  #
  # @else
  #
  # @endif
  def getConfig(self):
    return self._config


  #============================================================
  # コンポーネントマネージャ
  #============================================================
  ##
  # @if jp
  # @class InstanceName
  # @brief ObjectManager 検索用ファンクタ
  #
  # @else
  #
  # @endif
  class InstanceName:



    ##
    # @if jp
    # @brief コンストラクタ
    #
    # コンストラクタ
    #
    # @param self
    # @param name 検索対象コンポーネント名称(デフォルト値:None)
    # @param factory 検索対象ファクトリ名称(デフォルト値:None)
    #
    # @else
    #
    # @endif
    def __init__(self, name=None, factory=None):
      if factory:
        self._name = factory.getInstanceName()
      elif name:
        self._name = name

    def __call__(self, factory):
      return self._name == factory.getInstanceName()



  #============================================================
  # コンポーネントファクトリ
  #============================================================
  ##
  # @if jp
  # @class FactoryPredicate
  # @brief コンポーネントファクトリ検索用ファンクタ
  #
  # @else
  #
  # @endif
  class FactoryPredicate:



    def __init__(self, name=None, factory=None):
      if name:
        self._name = name
      elif factory:
        self._name = factory.profile().getProperty("implementation_id")

    def __call__(self, factory):
      return self._name == factory.profile().getProperty("implementation_id")



  #============================================================
  # ExecutionContextファクトリ
  #============================================================
  ##
  # @if jp
  # @class FactoryPredicate
  # @brief ExecutionContextファクトリ検索用ファンクタ
  #
  # @else
  #
  # @endif
  class ECFactoryPredicate:



    def __init__(self, name=None, factory=None):
      if name:
        self._name = name
      elif factory:
        self._name = factory.name()

    def __call__(self, factory):
      return self._name == factory.name()


  #------------------------------------------------------------
  # ORB runner
  #------------------------------------------------------------
  ##
  # @if jp
  # @class OrbRunner
  # @brief OrbRunner クラス
  #
  # ORB 実行用ヘルパークラス。
  #
  # @since 0.4.0
  #
  # @else
  # @class OrbRunner
  # @brief OrbRunner class
  # @endif
  class OrbRunner:



    ##
    # @if jp
    # @brief コンストラクタ
    #
    # コンストラクタ
    #
    # @param self
    # @param orb ORB
    #
    # @else
    # @brief Constructor
    #
    # @endif
    def __init__(self, orb):
      self._orb = orb
      self._th = threading.Thread(target=self.run)
      self._th.start()
      self._evt = threading.Event()


    ##
    # @if jp
    # @brief ORB 実行処理
    #
    # ORB 実行
    #
    # @param self
    #
    # @else
    #
    # @endif
    def run(self):
      try:
        self._orb.run()
        #Manager.instance().shutdown()
        self._evt.set()
      except:
        traceback.print_exception(*sys.exc_info())
        pass
      self._evt.set()
      return


    ##
    # @if jp
    # @brief ORB wait処理
    #
    # ORB wait
    #
    # @param self
    #
    # @else
    #
    # @endif
    def wait(self):
      self._evt.wait()

    ##
    # @if jp
    # @brief ORB 終了処理(未実装)
    #
    # ORB 終了処理
    #
    # @param self
    # @param flags 終了処理フラグ
    #
    # @return 終了処理結果
    #
    # @else
    #
    # @endif
    def close(self, flags):
      return 0


  #------------------------------------------------------------
  # Manager Terminator
  #------------------------------------------------------------
  ##
  # @if jp
  # @class Terminator
  # @brief Terminator クラス
  #
  # ORB 終了用ヘルパークラス。
  #
  # @since 0.4.0
  #
  # @else
  #
  # @endif
  class Terminator:



    ##
    # @if jp
    # @brief コンストラクタ
    #
    # コンストラクタ
    #
    # @param self
    # @param manager マネージャ・オブジェクト
    #
    # @else
    # @brief Constructor
    #
    # @endif
    def __init__(self, manager):
      self._manager = manager


    ##
    # @if jp
    # @brief 終了処理
    #
    # ORB，マネージャ終了処理を開始する。
    #
    # @param self
    #
    # @else
    #
    # @endif
    def terminate(self):
      self._manager.shutdown()



  ##
  # @if jp
  # @class Term
  # @brief Term クラス
  #
  # 終了用ヘルパークラス。
  #
  # @since 0.4.0
  #
  # @else
  #
  # @endif
  class Term:



    def __init__(self):
      self.waiting = 0
      self.mutex   = threading.RLock()
