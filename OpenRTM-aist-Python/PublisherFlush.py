#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
 \file  PublisherFlush.py
 \brief PublisherFlush class
 \date  $Date: 2007/09/06$
 \author Noriaki Ando <n-ando@aist.go.jp>

 Copyright (C) 2006
     Noriaki Ando
     Task-intelligence Research Group,
     Intelligent Systems Research Institute,
     National Institute of
         Advanced Industrial Science and Technology (AIST), Japan
     All rights reserved.
"""


import OpenRTM


class PublisherFlush(OpenRTM.PublisherBase):
	"""
	\if jp
	\class PublisherFlush
	\brief PublisherFlush クラス
	\else
	\class PublisherFlush
	\brief PublisherFlush class
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
		self._consumer.push()
		return
	
