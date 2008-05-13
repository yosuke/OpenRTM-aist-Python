#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
 \file ExtTrigExecutionContext.py
 \brief ExtTrigExecutionContext class
 \date $Date: 2007/09/06$
 \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara

 Copyright (C) 2007
    Task-intelligence Research Group,
     Intelligent Systems Research Institute,
     National Institute of
         Advanced Industrial Science and Technology (AIST), Japan
     All rights reserved.
"""


import threading
import time

import OpenRTM
import RTC, RTC__POA

class ExtTrigExecutionContext(OpenRTM.PeriodicExecutionContext):
	
	def __init__(self):
		OpenRTM.PeriodicExecutionContext.__init__(self)
		self._worker = self.Worker()

	def __del__(self):
		pass


	def tick(self):
		if not self._worker._cond.acquire(0):
			return
		self._worker._called = True
		self._worker._cond.notify()
		self._worker._cond.release()
		return


	def run(self):
		flag = True

		while flag:
			flag = self._running
			sec_ = float(self._usec)/1000000.0
			self._worker._cond.acquire()
			while not self._worker._called and self._running:
				self._worker._cond.wait()
			if self._worker._called:
				self._worker._called = False
				for comp in self._comps:
					self.invoke_worker()(comp)
				while not self._running:
					time.sleep(sec_)
				time.sleep(sec_)
			self._worker._cond.release()

		
	class Worker:
		
		def __init__(self):
			self._mutex = threading.RLock()
			self._cond = threading.Condition(self._mutex)
			self._called = False


def ExtTrigExecutionContextInit(manager):
	manager.registerECFactory("ExtTrigExecutionContext",
							  OpenRTM.ExtTrigExecutionContext,
							  OpenRTM.ECDelete)
