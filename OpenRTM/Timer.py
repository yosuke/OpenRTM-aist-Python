#!/usr/bin/env/python
# -*- coding: euc-jp -*-

"""
 \file Timer.py
 \brief Timer class
 \date $Date: $
 \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara

 Copyright (C) 2007
     Task-intelligence Research Group,
     Intelligent Systems Research Institute,
     National Institute of
         Advanced Industrial Science and Technology (AIST), Japan
     All rights reserved.
"""


import time
import threading

import OpenRTM


class ScopedLock:
	def __init__(self, mutex):
		self.mutex = mutex
		self.mutex.acquire()

	def __del__(self):
		self.mutex.release()


class Timer:
	def __init__(self, interval):
		"""
		 \param interval(OpenRTM.TimeValue)
		"""
		self._interval = interval
		self._running  = False
		self._runningMutex = threading.RLock()
		self._tasks = []
		self._taskMutex = threading.RLock()
		self._thread = threading.Thread(target=self.run)


	def __del__(self):
		pass
    

	def run(self):
		while self._running:
			self.invoke()
			if self._interval.tv_sec != 0:
				time.sleep(self._interval.tv_sec)
			time.sleep(self._interval.tv_usec/1000000.0)
		return 0
    

	def start(self):
		guard = ScopedLock(self._runningMutex)
		if not self._running:
			self._running = True
			self._thread.start()
    

	def stop(self):
		guard = ScopedLock(self._runningMutex)
		self._running = False
    

	def invoke(self):
		for i in range(len(self._tasks)):
			self._tasks[i].remains = self._tasks[i].remains - self._interval
			if self._tasks[i].remains.tv_usec < 0:
				self._tasks[i].listener.invoke()
				self._tasks[i].remains = self._tasks[i].period
    

	def registerListener(self, listener, tm):
		"""
		 \param listener(OpenRTM.ListenerBase)
		 \param tm(OpenRTM.TimeValue)
		"""
		guard = ScopedLock(self._taskMutex)
		for i in range(len(self._tasks)):
			if self._tasks[i].listener == listener:
				self._tasks[i].period = tm
				self._tasks[i].remains = tm
				return listener
		self._tasks.append(self.Task(listener, tm))
		return listener
		

	def registerListenerObj(self, obj, cbf, tm):
		"""
		 \param obj(object)
		 \param cbf(callback function)
		 \param tm(OpenRTM.TimeValue)
		"""
		return self.registerListener(OpenRTM.ListenerObject(obj, cbf), tm)
    

	def registerListenerFunc(self, cbf, tm):
		"""
		 \param cbf(callback function)
		 \param tm(OpenRTM.TimeValue)
		"""
		return self.registerListener(OpenRTM.ListenerFunc(cbf), tm)


	def unregisterListener(self, id):
		"""
		 \param id(OpenRTM.ListenerBase)
		"""
		guard = ScopedLock(self._taskMutex)
		len_ = len(self._tasks)
		for i in range(len_):
			idx = (len_ - 1) - i
			if self._tasks[idx].listener == id:
				del self._tasks[idx]
				return True
		return False


	class Task:
		def __init__(self, lb, tm):
			self.listener = lb
			self.period = tm
			self.remains = tm
