#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
 \file NamingManager.py
 \brief naming Service helper class
 \date $Date: 2007/08/27$
 \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara

 Copyright (C) 2006
     Task-intelligence Research Group,
     Intelligent Systems Research Institute,
     National Institute of
         Advanced Industrial Science and Technology (AIST), Japan
     All rights reserved.
"""


import threading
import traceback
import sys

import OpenRTM


class ScopedLock:
	def __init__(self, mutex):
		self.mutex = mutex
		self.mutex.acquire()

	def __del__(self):
		self.mutex.release()


class NamingBase:
	def __init__(self):
		pass

	def __del__(self):
		pass
	
	def bindObject(self, name, rtobj):
		pass
	
	def unbindObject(self, name):
		pass

 
class NamingOnCorba(NamingBase):
	def __init__(self, orb, names):
		self._cosnaming = OpenRTM.CorbaNaming(orb,names)

	def __del__(self):
		pass

	def bindObject(self, name, rtobj):
		try:
			self._cosnaming.rebindByString(name, rtobj.getObjRef(), True)
		except:
			pass

	def unbindObject(self, name):
		try:
			self._cosnaming.unbind(name)
		except:
			traceback.print_exception(*sys.exc_info())


class NamingManager:
	def __init__(self, manager):
		"""
		 \brief コンストラクタ
		 \param manager(OpenRTM.Manager)
		"""
		self._manager = manager
		self._rtcout = manager.getLogbuf()
		#self._rtcout.setLogLevel(manager.getConfig().getProperty("logger.log_level"))
		#self._rtcout.setLogLock(OpenRTM.toBool(manager.getConfig().getProperty("logger.stream_lock"), "enable", "disable", False))
		self._names = []
		self._namesMutex = threading.RLock()
		self._compNames = []
		self._compNamesMutex = threading.RLock()


	def __del__(self):
		pass


	def registerNameServer(self, method, name_server):
		"""
		 \brief NameServerの登録
		 \param method(string)  naming type
		 \param name_server(string) name of server
		"""
		self._rtcout.RTC_TRACE("NamingManager::registerNameServer(%s, %s)",
							   (method, name_server))
		name = self.createNamingObj(method, name_server)
		self._names.append(self.Names(method, name_server, name))


	def bindObject(self, name, rtobj):
		"""
		 \brief NameServerへRTオブジェクトをバインド
		 \param name(string)
		 \param rtobj(OpenRTM.RTObject_impl)
		"""
		self._rtcout.RTC_TRACE("NamingManager::bindObject(%s)", name)
		guard = ScopedLock(self._namesMutex)
		for i in range(len(self._names)):
			if self._names[i].ns != None:
				self._names[i].ns.bindObject(name, rtobj)
		self.registerCompName(name, rtobj)


	def update(self):
		self._rtcout.RTC_TRACE("NamingManager::update()")
		guard = ScopedLock(self._namesMutex)
		for i in range(len(self._names)):
			if self._names[i].ns == None:
				nsobj = self.createNamingObj(self._names[i].method,
											 self._names[i].nsname)
				if nsobj != None:
					self._rtcout.RTC_INFO("New name server found: %s/%s",
										  (self._names[i].method,
										  self._names[i].nsname))
					self._names[i].ns = nsobj
					self.bindCompsTo(nsobj)


	def unbindObject(self, name):
		"""
		 \brief NameServerからRTオブジェクトをアンバインド
		 \param name(string)
		"""
		self._rtcout.RTC_TRACE("NamingManager::unbindObject(%s)", name)
		guard = ScopedLock(self._namesMutex)
		for i in range(len(self._names)):
			if self._names[i].ns != None:
				self._names[i].ns.unbindObject(name)
		self.unregisterCompName(name)


	def unbindAll(self):
		self._rtcout.RTC_TRACE("NamingManager::unbindAll(): %d names.", len(self._compNames))
		guard = ScopedLock(self._compNamesMutex)
		for i in range(len(self._compNames)):
			self.unbindObject(self._compNames[i].name)


	def getObjects(self):
		comps = []
		guard = ScopedLock(self._compNamesMutex)
		for i in range(len(self._compNames)):
			comps.append(self._compNames[i].rtobj)
		return comps


	def createNamingObj(self, method, name_server):
		"""
		 \brief NamingObjectの生成
		 \param method(string)
		 \param name_server(string)
		 \return OpenRTM.NamingOnCorbaオブジェクト
		"""
		mth = method
		if mth == "corba":
			try:
				name = OpenRTM.NamingOnCorba(self._manager.getORB(),name_server)
				if name == None:
					return None
				self._rtcout.RTC_INFO("NameServer connection succeeded: %s/%s",
									  (method, name_server))
				return name
			except:
				self._rtcout.RTC_INFO("NameServer connection failed: %s/%s",
									  (method, name_server))
				return None

		return None
				

	def bindCompsTo(self, ns):
		"""
		 \brief NameServerへRTコンポーネントをバインド
		 \param ns(OpenRTM.NamingBase)
		"""
		for i in range(len(self._compNames)):
			ns.bindObject(self._compNames[i].name, self._compNames[i].rtobj)


	def registerCompName(self, name, rtobj):
		"""
		 \brief コンポーネント名の登録
		 \param name(string)
		 \param rtobj(OpenRTM.RTObject_impl)
		"""
		for i in range(len(self._compNames)):
			if self._compNames[i].name == name:
				self._compNames[i].rtobj = rtobj
				return

		self._compNames.append(self.Comps(name, rtobj))
		return


	def unregisterCompName(self, name):
		"""
		 \brief コンポーネント名の削除
		 \param name(string)
		"""
		len_ = len(self._compNames)
		for i in range(len_):
			idx = (len_-1) - i
			if self._compNames[idx].name == name:
				del self._compNames[idx]
				return
		return
		


	# Name Servers' method/name and object
	class Names:
		def __init__(self, meth, name, naming):
			self.method = meth
			self.nsname = name
			self.ns     = naming


	# Components' name and object
	class Comps:
		def __init__(self, n, obj):
			self.name = n
			self.rtobj = obj
