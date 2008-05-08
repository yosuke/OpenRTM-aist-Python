#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file SystemLogger.py
# @brief RT component logger class
# @date $Date$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2003-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.


import time
import threading
import logging
import logging.handlers

logger = None

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
  def __init__(self, mutex):
    self.mutex = mutex
    self.mutex.acquire()

  def __del__(self):
    self.mutex.release()


##
# @if jp
#
# @class Logbuf
#
# @brief ロガーバッファダミークラス
#
# ログバッファのダミークラス。
#
# @else
#
# @class Logbuf
#
# @brief Logger buffer dummy class
#
# @endif
class Logbuf:



  ##
  # @if jp
  #
  # @brief コンストラクタ
  #
  # ファイル名およびオープンモードを指定してコンストラクトするコンストラクタ
  #
  # @param self
  # @param fileName ログファイル名(デフォルト値:None)
  # @param mode オープンモード(デフォルト値:None)
  # @param protection 保護モード(デフォルト値:a+)本実装では未使用
  #
  # @else
  #
  # @brief constructor.
  #
  # @endif
  def __init__(self, fileName=None, mode=None, protection='a+'):
    global logger
    self._mutex = threading.RLock()

    logger = logging.getLogger('rtclog')

    if fileName:
      self._fhdlr = logging.FileHandler(fileName)
    else:
      self._fhdlr = logging.FileHandler('rtcsystem.log')


  ##
  # @if jp
  #
  # @brief デストラクタ
  #
  # デストラクタ。ファイルをクローズする。
  #
  # @param self
  #
  # @else
  #
  # @brief destractor.
  #
  # @endif
  def __del__(self):
    self._fhdlr.close()



##
# @if jp
#
# @class LogStream
#
# @brief ロガーフォーマットダミークラス
#
# ログフォーマット用ダミークラス。
#
# @else
#
# @endif
class LogStream:



  SILENT    = 0 # ()
  ERROR     = 1 # (ERROR)
  WARN      = 2 # (ERROR, WARN)
  INFO      = 3 # (ERROR, WARN, INFO)
  NORMAL    = 4 # (ERROR, WARN, INFO, NORMAL)
  DEBUG     = 5 # (ERROR, WARN, INFO, NORMAL, DEBUG)
  TRACE     = 6 # (ERROR, WARN, INFO, NORMAL, DEBUG, TRACE)
  VERBOSE   = 7 # (ERROR, WARN, INFO, NORMAL, DEBUG, TRACE, VERBOSE)
  PARANOID  = 8 # (ERROR, WARN, INFO, NORMAL, DEBUG, TRACE, VERBOSE, PARA)
  MANDATORY = 9 #  This level is used for only LogLockLevel


  ##
  # @if jp
  #
  # @brief ログレベル設定
  #
  # 与えられた文字列に対応したログレベルを設定する。
  #
  # @param self
  # @param lv ログレベル文字列
  #
  # @return 設定したログレベル
  #
  # @else
  #
  # @endif
  def strToLogLevel(self, lv):
    if lv == LogStream.SILENT:
      return LogStream.SILENT
    elif lv == LogStream.ERROR:
      return LogStream.ERROR
    elif lv == LogStream.WARN:
      return LogStream.WARN
    elif lv == LogStream.INFO:
      return LogStream.INFO
    elif lv == LogStream.NORNAL:
      return LogStream.NORMAL
    elif lv == LogStream.DEBUG:
      return LogStream.DEBUG
    elif lv == LogStream.TRACE:
      return LogStream.TRACE
    elif lv == LogStream.VERBOSE:
      return LogStream.VERBOSE
    elif lv == LogStream.PARANOID:
      return LogStream.PARANOID
    elif lv == LogStream.MANDATORY:
      return LogStream.MANDATORY
    else:
      return LogStream.NORMAL


  ##
  # @if jp
  #
  # @brief コンストラクタ
  #
  # コンストラクタ
  #
  # @param self
  # @param logbufObj ログバッファオブジェクト(デフォルト値:None)
  #
  # @else
  #
  # @brief constructor.
  #
  # @endif
  def __init__(self, logbufObj=None):
    global logger
    self._mutex = threading.RLock()
    self._LogLock = False
    self._log_enable = False
    if logbufObj:
      formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
      self._pLogbuf = logbufObj
      fh = self._pLogbuf._fhdlr
      self._mhdlr = logging.handlers.MemoryHandler(1024,logging.DEBUG, fh)
      fh.setFormatter(formatter)
      logger.addHandler(self._mhdlr)
      logger.setLevel(logging.DEBUG)
      self._log_enable = True


  ##
  # @if jp
  #
  # @brief printf フォーマット出力
  #
  # printfライクな書式でログ出力する。<br>
  # ※本実装では引数 fmt で与えられた文字をそのまま返す。
  #
  # @param self
  # @param fmt 書式文字列
  #
  # @return 書式付き文字列出力
  #
  # @else
  #
  # @brief Formatted output like printf
  #
  # @endif
  def printf(self, fmt):
    return fmt


  ##
  # @if jp
  #
  # @brief ログレベル設定
  #
  # ログレベルを設定する。
  #
  # @param self
  # @param level ログレベル
  #
  # @else
  #
  # @endif
  def setLogLevel(self, level):
    global logger

    if level == "INFO":
      logger.setLevel(logging.INFO)
    elif level == "ERROR":
      logger.setLevel(logging.ERROR)
    elif level == "WARNING":
      logger.setLevel(logging.WARNING)
    elif level == "DEBUG":
      logger.setLevel(logging.DEBUG)
    elif level == "SILENT":
      logger.setLevel(logging.NOTSET)
    else:
      logger.setLevel(logging.INFO)


  ##
  # @if jp
  #
  # @brief ロックモード設定
  #
  # ログのロックモードを設定する。
  #
  # @param self
  # @param lock ログロックフラグ
  #
  # @else
  #
  # @endif
  def setLogLock(self, lock):
    if lock == 1:
      self._LogLock = True
    elif lock == 0:
      self._LogLock = False


  ##
  # @if jp
  #
  # @brief ロックモード有効化
  #
  # @param self
  #
  # ロックモードを有効にする。
  #
  # @else
  #
  # @endif
  def enableLogLock(self):
    self._LogLock = True


  ##
  # @if jp
  #
  # @brief ロックモード解除
  #
  # @param self
  #
  # ロックモードを無効にする。
  #
  # @else
  #
  # @endif
  def disableLogLock(self):
    self._LogLock = False


  ##
  # @if jp
  #
  # @brief ログロック取得
  # ロックモードが設定されている場合、ログのロックを取得する。
  #
  # @param self
  #
  # @else
  #
  # @endif
  def acquire(self):
    if self._LogLock:
      self.guard = ScopedLock(self._mutex)


  ##
  # @if jp
  #
  # @brief ログロック解放
  # ロックモードが設定されている場合に、ログのロックを解放する。
  #
  # @param self
  #
  # @else
  #
  # @endif
  def release(self):
    if self._LogLock:
      del self.guard


  ##
  # @if jp
  #
  # @brief 汎用ログ出力
  #
  # ログレベルおよび出力フォーマット文字列を引数としてとり，
  # 汎用ログを出力する。
  #
  # @param self
  # @param LV ログレベル
  # @param msg ログメッセージ
  # @param opt オプション(デフォルト値:None)
  #
  # @else
  #
  # @brief Log output macro
  #
  # @endif
  def RTC_LOG(self, LV, msg, opt=None):
    global logger

    if self._log_enable:
      self.acquire()

      if opt:
        try:
          messages = msg%(opt)
        except:
          print "RTC_LOG : argument error"
          return
      else:
        messages = msg

      logger.log(LV,messages)

      self.release()


  ##
  # @if jp
  #
  # @brief エラーログ出力
  #
  # エラーレベルのログを出力する。<BR>ログレベルが
  # ERROR, WARN, INFO, NORMAL, DEBUG, TRACE, VERBOSE, PARANOID
  # の場合にログ出力される。
  #
  # @param self
  # @param msg ログメッセージ
  # @param opt オプション(デフォルト値:None)
  #
  # @else
  #
  # @brief Error log output macro.
  #
  # @endif
  def RTC_ERROR(self, msg, opt=None):
    global logger

    if self._log_enable:
      self.acquire()

      if opt:
        try:
          messages = msg%(opt)
        except:
          print "RTC_ERROR : argument error"
          return
      else:
        messages = msg

      logger.error(messages)

      self.release()


  ##
  # @if jp
  #
  # @brief ワーニングログ出力
  #
  # ワーニングレベルのログを出力する。<BR>ログレベルが
  # ( WARN, INFO, NORMAL, DEBUG, TRACE, VERBOSE, PARANOID )
  # の場合にログ出力される。
  #
  # @param self
  # @param msg ログメッセージ
  # @param opt オプション(デフォルト値:None)
  #
  # @else
  #
  # @brief Warning log output macro.
  #
  # If logging levels are
  # ( WARN, INFO, NORMAL, DEBUG, TRACE, VERBOSE, PARANOID ),
  # message will be output to log.
  #
  # @endif
  def RTC_WARN(self, msg, opt=None):
    global logger

    if self._log_enable:
      self.acquire()

      if opt:
        try:
          messages = msg%(opt)
        except:
          print "RTC_WARN : argument error"
          return
      else:
        messages = msg

      logger.warning(messages)

      self.release()


  ##
  # @if jp
  #
  # @brief インフォログ出力
  #
  # インフォレベルのログを出力する。<BR>ログレベルが
  # ( INFO, NORMAL, DEBUG, TRACE, VERBOSE, PARANOID )
  # の場合にログ出力される。
  #
  # @param self
  # @param msg ログメッセージ
  # @param opt オプション(デフォルト値:None)
  #
  # @else
  #
  # @brief Infomation level log output macro.
  #
  #  If logging levels are
  # ( INFO, NORMAL, DEBUG, TRACE, VERBOSE, PARANOID ),
  # message will be output to log.
  #
  # @endif
  def RTC_INFO(self, msg, opt=None):
    global logger

    if self._log_enable:
      self.acquire()

      if opt:
        try:
          messages = msg%(opt)
        except:
          print "RTC_INFO : argument error"
          return
      else:
        messages = msg

      logger.info(messages)
    
      self.release()


  ##
  # @if jp
  #
  # @brief ノーマルログ出力
  #
  # ノーマルレベルのログを出力する。<BR>ログレベルが
  # ( NORMAL, DEBUG, TRACE, VERBOSE, PARANOID )
  # の場合にログ出力される。
  #
  # @param self
  # @param msg ログメッセージ
  # @param opt オプション(デフォルト値:None)
  #
  # @else
  #
  # @brief Normal level log output macro.
  #
  # If logging levels are
  # ( NORMAL, DEBUG, TRACE, VERBOSE, PARANOID ),
  # message will be output to log.
  #
  # @endif
  def RTC_NORMAL(self, msg, opt=None):
    return

    global logger

    if self._log_enable:
      self.acquire()

      if opt:
        try:
          messages = msg%(opt)
        except:
          print "RTC_NORMAL : argument error"
          return
      else:
        messages = msg
        
      self.release()


  ##
  # @if jp
  #
  # @brief デバッグログ出力
  #
  # デバッグレベルのログを出力する。<BR>ログレベルが
  # ( DEBUG, TRACE, VERBOSE, PARANOID )
  # の場合にログ出力される。
  #
  # @param self
  # @param msg ログメッセージ
  # @param opt オプション(デフォルト値:None)
  #
  # @else
  #
  # @brief Debug level log output macro.
  #
  # If logging levels are
  # ( DEBUG, TRACE, VERBOSE, PARANOID ),
  # message will be output to log.
  #
  # @endif
  def RTC_DEBUG(self, msg, opt=None):
    global logger

    if self._log_enable:
      self.acquire()

      if opt:
        try:
          messages = msg%(opt)
        except:
          print "RTC_DEBUG : argument error"
          return
      else:
        messages = msg
        
      logger.debug(messages)
      
      self.release()


  ##
  # @if jp
  #
  # @brief トレースログ出力
  #
  # トレースレベルのログを出力する。<BR>ログレベルが
  # ( TRACE, VERBOSE, PARANOID )
  # の場合にログ出力される。
  #
  # @param self
  # @param msg ログメッセージ
  # @param opt オプション(デフォルト値:None)
  #
  # @else
  #
  # @brief Trace level log output macro.
  #
  # If logging levels are
  # ( TRACE, VERBOSE, PARANOID ),
  # message will be output to log.
  #
  # @endif
  def RTC_TRACE(self, msg, opt=None):
    global logger

    if self._log_enable:
      self.acquire()

      if opt:
        try:
          messages = msg%(opt)
        except:
          print "RTC_TRACE : argument error"
          return
      else:
        messages = msg
        
      logger.debug(messages)
      
      self.release()


  ##
  # @if jp
  #
  # @brief ベルボーズログ出力
  #
  # ベルボーズレベルのログを出力する。<BR>ログレベルが
  # ( VERBOSE, PARANOID )
  # の場合にログ出力される。<br>
  # ※現状では未実装
  #
  # @param self
  # @param msg ログメッセージ
  # @param opt オプション(デフォルト値:None)
  #
  # @else
  #
  # @brief Verbose level log output macro.
  #
  # If logging levels are
  # ( VERBOSE, PARANOID ),
  # message will be output to log.
  #
  # @endif
  def RTC_VERBOSE(self, msg, opt=None):
    pass


  ##
  # @if jp
  #
  # @brief パラノイドログ出力
  #
  # パラノイドレベルのログを出力する。<BR>ログレベルが
  # ( PARANOID )
  # の場合にログ出力される。<br>
  # ※現状では未実装
  #
  # @param self
  # @param msg ログメッセージ
  # @param opt オプション(デフォルト値:None)
  #
  # @else
  #
  # @brief Paranoid level log output macro.
  #
  # If logging levels are
  # ( PARANOID ),
  # message will be output to log.
  #
  # @endif
  def RTC_PARANOID(self, msg, opt=None):
    pass
