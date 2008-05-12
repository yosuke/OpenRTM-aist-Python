#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
 \file ObjectManager.py
 \brief Object management class
 \date $Date: $
 \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara

 Copyright (C) 2003-2007
     Task-intelligence Research Group,
     Intelligent Systems Research Institute,
     National Institute of
         Advanced Industrial Science and Technology (AIST), Japan
     All rights reserved.
"""


import sys
import string
import threading

import OpenRTM


class ScopedLock:
	def __init__(self, mutex):
		self.mutex = mutex
		self.mutex.acquire()

	def __del__(self):
		self.mutex.release()


class ObjectManager:

	def __init__(self, predicate):
		self._objects = self.Objects()
		self._predicate = predicate

	def __del__(self):
		pass


	class Objects:
		def __init__(self):
			self._mutex = threading.RLock()
			self._obj = []
	

	def registerObject(self, obj):
		guard = ScopedLock(self._objects._mutex)
		predi = self._predicate(factory=obj)

		for _obj in self._objects._obj:
			if predi(_obj):
				return False

		self._objects._obj.append(obj)
		return True


	def unregisterObject(self, id):
		guard = ScopedLock(self._objects._mutex)
		predi = self._predicate(name=id)
		i = 0
		for _obj in self._objects._obj:
			if predi(_obj):
				ret = _obj
				del self._objects._obj[i]
				return ret
			i+=1
			
		return None


	def find(self, id):
		guard = ScopedLock(self._objects._mutex)
		predi = self._predicate(name=id)
		for _obj in self._objects._obj:
			if predi(_obj):
				return _obj
			
		return None

	def getObjects(self):
		guard = ScopedLock(self._objects._mutex)
		return self._objects._obj


	def for_each(self,p):
		guard = ScopedLock(self._objects._mutex)
		predi = p()

		for _obj in self._objects._obj:
			predi(_obj)

		return predi

