#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file BufferBase.py
# @brief Buffer abstract class
# @date $Date: 2007/09/12 $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
# 
# Copyright (C) 2006
# Noriaki Ando
#    Task-intelligence Research Group,
#    Intelligent Systems Research Institute,
#    National Institute of
#    Advanced Industrial Science and Technology (AIST), Japan
#    All rights reserved.


##
# @if jp
# @class BufferBase
# 
# 種々のバッファのための抽象インターフェースクラス。
# 具象バッファクラスは、以下の純粋仮想関数の実装を提供しなければならない。
# 
# publicインターフェースとして以下のものを提供する。
# - write(): バッファに書き込む
# - read(): バッファから読み出す
# - length(): バッファ長を返す
# - isFull(): バッファが満杯である
# - isEmpty(): バッファが空である
# 
# protectedインターフェースとして以下のものを提供する。
# - put(): バッファにデータを書き込む
# - get(): バッファからデータを読み出す
# 
# @param DataType バッファに格納するデータ型
# 
# @else
# @class BufferBase
# @brief BufferBase abstract class
# 
# This is the abstract interface class for various Buffer.
# 
# @param DataType Data type to be stored to the buffer.
# 
# @endif

class BufferBase:
	
	def __init__(self):
		pass


	##
	# @if jp
	# バッファの長さを取得する
	# @else
	# Get the buffer length
	# @endif

	def length(self):
		pass


	##
	# @if jp
	# バッファにデータを書き込む
	# @else 
	# Write data into the buffer
	# @endif

	# write(value:RTC.BasicDataType)
	def write(self, value):
		pass


	##
	# @if jp
	# バッファからデータを読み込む
	# @else
	# Read data from the buffer
	# @endif
	
	# read(value:RTC.BasicDataType)
	def read(self, value):
		pass


	##
	# @if jp
	# バッファがfullである
	# @else
	# True if the buffer is full, else false.
	# @endif
	
	def isFull(self):
		pass


	##
	# @if jpwork/OpenRTM-aist-0.2.0-Python/OpenRTM/
	# バッファがemptyである
	# @else
	# True if the buffer is empty, else false.
	# @endif
	
	def isEmpty(self):
		pass


	##
	# @if jp
	# バッファにデータを書き込む
	# @else
	# Write data into the buffer
	# @endif
	
	# put(data:RTC.BasicDataType)
	def put(self, data):
		pass


	##
	# @if jp
	# バッファからデータを取得する
	# @else
	# Get data from the buffer
	# @endif
	
	def get(self):
		pass


	##
	# @if jp
	# 次に書き込むバッファの参照を取得する
	# @else
	# Get the buffer's reference to be written the next
	# @endif
	
	def getRef(self):
		pass



class NullBuffer(BufferBase):
	
	def __init__(self, size=None):
		if size == None:
			size=1
		self._length = 1
		self._data = None
		self._is_new = False
		self._inited = False


	# init(data:RTC.BasicDataType)
	def init(self, data):
		self.put(data)


	def clear(self):
		self._inited = False


	def length(self):
		return 1


	# write(value:RTC.BasicDataType)
	def write(self, value):
		self.put(value)
		return True


	# read(value:RTC.BasicDataType)
	def read(self, value):
		if not self._inited:
			return False
		value[0] = self.get()
		return True


	def isFull(self):
		return False


	def isEmpty(self):
		return not self._inited


	def isNew(self):
		return self._is_new


	# put(data:RTC.BasicDataType)
	def put(self, data):
		self._data = data
		self._is_new = True
		self._inited = True


	def get(self):
		self._is_new = False
		return self._data


	def getRef(self):
		return self._data
