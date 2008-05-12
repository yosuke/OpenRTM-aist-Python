#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
  \file  PublisherNew.py
  \brief PublisherNew class
  \date  $Date: 2007/09/27 $
  \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
 
  Copyright (C) 2006
      Noriaki Ando
      Task-intelligence Research Group,
      Intelligent Systems Research Institute,
      National Institute of
          Advanced Industrial Science and Technology (AIST), Japan
      All rights reserved.
"""
 
import threading

import OpenRTM


class PublisherNew(OpenRTM.PublisherBase):
	"""
	\if jp
	\class PublisherNew
	\brief PublisherNew クラス
	\else
	\class PublisherNew
	\brief PublisherNew class
	\endif
	"""	

	def __init__(self, consumer, property):
		"""
		\if jp
		\brief コンストラクタ
		\param consumer(OpenRTM.InPortConsumer)
		\param property(OpenRTM.Properties)
		\else
		\brief Constructor
		\param consumer(OpenRTM.InPortConsumer)
		\param property(OpenRTM.Properties)
		\endif
		"""
		OpenRTM.PublisherBase.__init__(self)
		self._data = self.NewData()
		self._consumer = consumer
		self._running = True
		self._thread = threading.Thread(target=self.run)
		self._thread.start()


	def __del__(self):
		"""
		\if jp
		\brief デストラクタ
		\else
		\brief Destructor
		\endif
		"""
		del self._consumer


	def update(self):
		"""
		\if jp
		\brief Observer関数
		\else
		\brief Observer function
		\endif
		"""
		if not self._data._cond.acquire(0):
			return

		self._data._updated = True
		self._data._cond.notify()
		self._data._cond.release()
		return


	def run(self):
		"""
		\if jp
		\brief スレッド実行関数
		\else
		\brief Thread execution function
		\endif
		"""
		while self._running:
			self._data._cond.acquire()
			# Waiting for new data updated
			while not self._data._updated and self._running:
				self._data._cond.wait()

			if self._data._updated:
				self._consumer.push()
				self._data._updated = False

			self._data._cond.release()


	def release(self):
		if not self._data._cond.acquire(0):
			return

		self._running = False
		self._data._cond.notify()
		self._data._cond.release()
		#self.wait()

    
    # NewData condition struct
	class NewData:
		def __init__(self):
			self._mutex = threading.RLock()
			self._cond = threading.Condition(self._mutex)
			self._updated = False
