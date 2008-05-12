#!/usr/bin/env python 
# -*- coding: euc-jp -*-

"""
 \file PublisherBase.py
 \brief Publisher base class
 \date $Date: 2007/09/05$
 \author Noriaki Ando <n-ando@aist.go.jp>

 Copyright (C) 2006
     Noriaki Ando
     Task-intelligence Research Group,
     Intelligent Systems Research Institute,
     National Institute of
         Advanced Industrial Science and Technology (AIST), Japan
     All rights reserved.
"""


class PublisherBase:
	"""
	\if jp

	\class PublisherBase

	\brief Publisher 基底クラス

	Publisher の基底クラス PublisherBase.
	各種 Publisher はこのクラスを継承して詳細を実装する。

	\else

	\class PublisherBase

	\brief Base class of Publisher.

	A base class of Publisher.
	Variation of Publisher which implements details of Publisher
	inherits this PublisherBase class.

	\endif
	"""
	def __init__(self):
		pass

	def update(self):
		pass

	def release(self):
		pass
