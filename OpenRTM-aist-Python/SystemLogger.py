#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
 \file SystemLogger.py
 \brief RT component logger class
 \date $Date$
 \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara

 Copyright (C) 2003-2005
     Task-intelligence Research Group,
     Intelligent Systems Research Institute,
     National Institute of
         Advanced Industrial Science and Technology (AIST), Japan
     All rights reserved.
"""


import time
import threading
import logging
import logging.handlers

logger = None

class ScopedLock:
	def __init__(self, mutex):
		self.mutex = mutex
		self.mutex.acquire()

	def __del__(self):
		self.mutex.release()

class Logbuf:
	def __init__(self, fileName=None, mode=None, protection='a+'):
		global logger
		self._mutex = threading.RLock()

		logger = logging.getLogger('rtclog')

		if fileName != None:
			self._fhdlr = logging.FileHandler(fileName)
		else:
			self._fhdlr = logging.FileHandler('rtcsystem.log')


	def __del__(self):
		self._fhdlr.close()


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


	def __del__(self):
		pass

	def printf(self, fmt):
		return fmt


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

	def setLogLock(self, lock):
		if lock == 1:
			self._LogLock = True
		elif lock == 0:
			self._LogLock = False


	def enableLogLock(self):
		self._LogLock = True


	def disableLogLock(self):
		self._LogLock = False


	def acquire(self):
		if self._LogLock:
			self.guard = ScopedLock(self._mutex)


	def release(self):
		if self._LogLock:
			del self.guard


	def RTC_LOG(self, LV, msg, opt=None):
		global logger

		if self._log_enable:
			self.acquire()

			if opt != None:
				try:
					messages = msg%(opt)
				except:
					print "RTC_LOG : argument error"
					return
			else:
				messages = msg

			logger.log(LV,messages)

			self.release()


	def RTC_ERROR(self, msg, opt=None):
		global logger

		if self._log_enable:
			self.acquire()

			if opt != None:
				try:
					messages = msg%(opt)
				except:
					print "RTC_ERROR : argument error"
					return
			else:
				messages = msg

			logger.error(messages)

			self.release()


	def RTC_WARN(self, msg, opt=None):
		global logger

		if self._log_enable:
			self.acquire()

			if opt != None:
				try:
					messages = msg%(opt)
				except:
					print "RTC_WARN : argument error"
					return
			else:
				messages = msg

			logger.warning(messages)

			self.release()


	def RTC_INFO(self, msg, opt=None):
		global logger

		if self._log_enable:
			self.acquire()

			if opt != None:
				try:
					messages = msg%(opt)
				except:
					print "RTC_INFO : argument error"
					return
			else:
				messages = msg

			logger.info(messages)
		
			self.release()


	def RTC_NORMAL(self, msg, opt=None):
		return

		global logger

		if self._log_enable:
			self.acquire()

			if opt != None:
				try:
					messages = msg%(opt)
				except:
					print "RTC_NORMAL : argument error"
					return
			else:
				messages = msg
				
			self.release()


	def RTC_DEBUG(self, msg, opt=None):
		global logger

		if self._log_enable:
			self.acquire()

			if opt != None:
				try:
					messages = msg%(opt)
				except:
					print "RTC_DEBUG : argument error"
					return
			else:
				messages = msg
				
			logger.debug(messages)
			
			self.release()


	def RTC_TRACE(self, msg, opt=None):
		global logger

		if self._log_enable:
			self.acquire()

			if opt != None:
				try:
					messages = msg%(opt)
				except:
					print "RTC_TRACE : argument error"
					return
			else:
				messages = msg
				
			logger.debug(messages)
			
			self.release()



	def RTC_VERBOSE(self, msg, opt=None):
		pass


	def RTC_PARANOID(self, msg, opt=None):
		pass
