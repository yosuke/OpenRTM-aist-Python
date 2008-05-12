#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
  \file  PublisherPeriodic.py
  \brief PublisherPeriodic class
  \date  $Date: 2007/09/28 $
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
from omniORB import any

import OpenRTM


class PublisherPeriodic(OpenRTM.PublisherBase):
	"""
	\if jp
	\class PublisherPeriodic
	\brief PublisherPeriodic クラス
	\else
	\class PublisherPeriodic
	\brief PublisherPeriodic class
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
		self._consumer = consumer
		self._running = True
		rate = property.getProperty("dataport.push_rate")

		if type(rate) == str or type(rate) == float or type(rate) == long :
			rate = float(rate)
		else:
			rate = float(any.from_any(rate,keep_structs=True))

		if rate:
			hz = rate
			if (hz == 0):
				hz = 1000.0
		else:
			hz = 1000.0

		self._usec = int(1000000.0/hz)

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
		self._running = False
		del self._consumer


	def update(self):
		"""
		\if jp
		\brief Observer関数
		\else
		\brief Observer function
		\endif
		"""
		pass


	def run(self):
		"""
		\if jp
		\brief スレッド実行関数
		\else
		\brief Thread execution function
		\endif
		"""
		import time
		while self._running:
			self._consumer.push()
			time.sleep(self._usec/1000000.0)

		return 0


	def release(self):
		"""
		\if jp
		\brief タスク終了関数
		\else
		\brief Task terminate function
		\endif
		"""
		self._running = False
