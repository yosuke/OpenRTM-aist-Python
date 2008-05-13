#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
 \file NumberingPolicy.py
 \brief Object numbering policy class
 \date $Date: 2007/08/23$
 \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara

 Copyright (C) 2006
     Task-intelligence Research Group,
     Intelligent Systems Research Institute,
     National Institute of
         Advanced Industrial Science and Technology (AIST), Japan
     All rights reserved.
"""


import string
import OpenRTM

class NumberingPolicy:
	class ObjectNotFound:
		pass

	def __del__(self):
		pass

	def onCreate(self, obj):
		pass

	def onDelete(self, obj):
		pass



class DefaultNumberingPolicy(NumberingPolicy):
	def __init__(self):
		self._num = 0
		self._objects = []

	def __del__(self):
		pass


	def onCreate(self, obj):
		self._num += 1

		pos = 0
		try:
			pos = self.find(None)
			self._objects[pos] = obj
			return OpenRTM.otos(pos)
		except NumberingPolicy.ObjectNotFound:
			self._objects.append(obj)
			return OpenRTM.otos(int(len(self._objects) - 1))

	
	def onDelete(self, obj):
		pos = 0
		pos = self.find(obj)
		if (pos < len(self._objects)):
			self._objects[pos] = None
		self._num -= 1


	def find(self, obj):
		i = 0
		for obj_ in self._objects:
			if obj_ == obj:
				return i
			i += 1
		raise NumberingPolicy.ObjectNotFound()
			 

