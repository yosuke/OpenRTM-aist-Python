#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
 \file RingBuffer.py
 \brief Defautl Buffer class
 \date $Date: 2007/09/12 $
 \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara

 Copyright (C) 2006
     Noriaki Ando
     Task-intelligence Research Group,
     Intelligent Systems Research Institute,
     National Institute of
         Advanced Industrial Science and Technology (AIST), Japan
     All rights reserved.
"""

import RTC
import OpenRTM

class RingBuffer(OpenRTM.BufferBase):

	def __init__(self, length):
		"""
		 \param length(int)
		"""
		self._oldPtr = 0
		if length < 2:
			self._length = 2
			self._newPtr = 1
		else:
			self._length = length
			self._newPtr = length - 1

		self._inited = False
		self._buffer = [self.Data() for i in range(self._length)]

	def __del__(self):
		"""
		\if jp
		\brief 仮想デストラクタ
		\else
		\brief virtual destractor
		\endif
		"""
		pass
    

	def init(self, data):
		"""
		 \param data(any data)
		"""
		for i in range(self._length):
			self.put(data)


	def clear(self):
		self._inited = False


	def length(self):
		"""
		\if jp
		\brief バッファの長さを取得する
		\else
		\brief Get the buffer length
		\endif
		"""
		return self._length


	def write(self, value):
		"""
		\if jp
		\brief バッファにデータを書き込む
		\param value(any data)
		\else
		\brief Write data into the buffer
		\param value(any data)
		\endif
		"""
		self.put(value)
		return True


	def read(self, value):
		"""
		\if jp
		\brief バッファからデータを読み込む
		\param value(list)
		\else
		\brief Read data from the buffer
		\param value(list)
		\endif
		"""
		if not self._inited:
			return False
		value[0] = self.get()
		return True


	def isFull(self):
		"""
		\if jp
		\brief バッファがfullである
		\else
		\brief True if the buffer is full, else false.
		\endif
		"""
		return False


	def isEmpty(self):
		"""
		\if jp
		\brief バッファがemptyである
		\else
		\brief True if the buffer is empty, else false.
		\endif
		"""
		return not self._inited


	def isNew(self):
		return self._buffer[self._newPtr].isNew()


	def put(self, data):
		"""
		\if jp
		\brief バッファにデータを書き込む
		\param data(any data)
		\else
		\brief Write data into the buffer
		\param data(any data)
		\endif
		"""
		self._buffer[self._oldPtr].write(data)
		self._newPtr = self._oldPtr
		ptr = self._oldPtr + 1
		self._oldPtr = ptr % self._length
		self._inited = True


	def get(self):
		"""
		\if jp
		\brief バッファからデータを取得する
		\else
		\brief Get data from the buffer
		\endif
		"""
		return self._buffer[self._newPtr].read()


	def getRef(self):
		"""
		\if jp
		\brief 次に書き込むバッファの参照を取得する
		\else
		\brief Get the buffer's reference to be written the next
		\endif
		"""
		return self._buffer[self._newPtr].data


	class Data:
		"""
		\if jp
		\brief バッファ配列
		\else
		\brief Buffer sequence
		\endif
		"""
		def __init__(self):
			self.data = None
			self.is_new = False


		def write(self, other):
			self.is_new = True
			self.data = other


		def read(self):
			self.is_new = False
			return self.data


		def isNew(self):
			return self.is_new
