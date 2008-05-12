#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
 \file Listener.py
 \brief Listener class
 \date $Date: 2007/08/23$
 \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara

 Copyright (C) 2007
     Task-intelligence Research Group,
     Intelligent Systems Research Institute,
     National Institute of
         Advanced Industrial Science and Technology (AIST), Japan
     All rights reserved.
"""



class ListenerBase:
	def __del__(self):
		pass

	def invoke(self):
		pass


class ListenerObject(ListenerBase):
	def __init__(self,obj,cbf):
		self.obj = obj
		self.cbf = cbf


	def __del(self):
		pass


	def invoke(self):
		self.cbf(self.obj)



class ListenerFunc(ListenerBase):
	def __init__(self,cbf):
		self.cbf = cbf


	def __del__(self):
		pass


	def invoke(self):
		self.cbf()
