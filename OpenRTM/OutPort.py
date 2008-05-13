#!/usr/bin/env python
# -*- coding: euc-jp -*-


"""
  \file OutPort.py
  \brief OutPort class
  \date $Date: 2007/09/19$
  \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
 
  Copyright (C) 2006
      Noriaki Ando
      Task-intelligence Research Group,
      Intelligent Systems Research Institute,
      National Institute of
          Advanced Industrial Science and Technology (AIST), Japan
      All rights reserved.
"""


from omniORB import any

import OpenRTM

usec_per_sec = 1000000


import time
class Time:
	def __init__(self):
		global usec_per_sec
		tm = time.time()
		tm_f       = tm - int(tm)     # 小数部の取り出し
		self.sec   = int(tm - tm_f)   # 整数部の取り出し
		self.usec  = int(tm_f * usec_per_sec) # sec -> usec (micro second)



class OutPort(OpenRTM.OutPortBase):
	"""
	\if jp
	\class OutPort
	\brief OutPort クラス
	\else
	\endif
	"""


	def __init__(self, name, value, buffer_):
		"""
		\if jp
		\brief OutPortクラスのコンストラクタ
		\else
		\brief Constructor
		\param name(string) Port name.
		\param value(data) DataType.
		\param buffer_(OpenRTM.BufferBase) Buffer object.
		\endif
		"""
		OpenRTM.OutPortBase.__init__(self, name)
		self._buffer         = buffer_
		self._value          = value
		self._timeoutTick    = 1000 # timeout tick: 1ms
		self._readBlock      = False
		self._readTimeout    = 0
		self._writeBlock     = False
		self._writeTimeout   = 0
		self._OnWrite        = None
		self._OnWriteConvert = None
		self._OnRead         = None
		self._OnReadConvert  = None
		self._OnOverflow     = None
		self._OnUnderflow    = None


	def isNew(self):
		return self._buffer.isNew()


	def write(self, value=None):
		"""
		\if jp
		\brief データ書き込み
		\param value(data)
		\else
		\brief Write data
		\param value(data)
		\endif
		"""
		if not value:
			value=self._value

		global usec_per_sec
		
		if self._OnWrite:
			self._OnWrite(value)

		timeout = self._writeTimeout

		tm_pre = Time()

		# blocking and timeout wait
		count = 0
		while self._writeBlock and self._buffer.isFull():
			if self._writeTimeout < 0:
				time.sleep(self._timeoutTick/usec_per_sec)
				continue
			
				
			# timeout wait
			tm_cur = Time()

			sec  = tm_cur.sec - tm_pre.sec
			usec = tm_cur.usec - tm_pre.usec

			timeout -= (sec * usec_per_sec + usec)

			if timeout < 0:
				break
			tm_pre = tm_cur
			time.sleep(self._timeoutTick/usec_per_sec)
			count += 1
      
		if self._buffer.isFull():
			if self._OnOverflow:
				self._OnOverflow(value)
			return False
      
		if not self._OnWriteConvert:
			self._buffer.put(value)
		else:
			self._buffer.put(self._OnWriteConvert(value))

		self.notify()
		return True


	def read(self, value):
		"""
		\if jp
		\brief データ読み出し
		\param value(data)
		\else
		\brief Read data
		\param value(data)
		\endif
		"""
		if self._OnRead:
			self._OnRead()

		timeout = self._readTimeout
		tm_pre = Time()

		# blocking and timeout wait
		while self._readBlock and self._buffer.isEmpty():
			if self._readTimeout < 0:
				time.sleep(self._timeoutTick/usec_per_sec)
				continue

			# timeout wait
			tm_cur = Time()
			sec  = tm_cur.sec - tm_pre.sec
			usec = tm_cur.usec - tm_pre.usec
			
			timeout -= (sec * usec_per_sec + usec)
			if timeout < 0:
				break
			tm_pre = tm_cur
			time.sleep(self._timeoutTick/usec_per_sec)

		if self._buffer.isEmpty():
			if self._OnUnderflow:
				value[0] = self._OnUnderflow()
				return False
			else:
				return False

		if not self._OnReadConvert:
			value[0] = self._buffer.get()
			return True
		else:
			value[0] = self._OnReadConvert(self._buffer.get())
			return true

		# never comes here
		return False


	def setReadBlock(self, block):
		"""
		\if jp
		\brief read() のブロック・非ブロックモードのセット
		\param block(bool)
		\else
		\brief Set read() block mode
		\param block(bool)
		\endif
		"""
		self._readBlock = block


	def setWriteBlock(self, block):
		"""
		\if jp
		\brief write() のブロック・非ブロックモードのセット
		\param block(bool)
		\else
		\brief Set read() block mode
		\param block(bool)
		\endif
		"""
		self._writeBlock = block


	def setReadTimeout(self, timeout):
		"""
		\if jp
		\brief read() のタイムアウト時間の設定
		read() のタイムアウト時間を usec で設定する。
		read() はブロックモードでなければならない。
		\param timeout(int) タイムアウト時間 [usec]
		\else
		\brief Set read() timeout
		\param timeout(int) time of timeout [usec]
		\endif
		"""
		self._readTimeout = timeout


	def setWriteTimeout(self, timeout):
		"""
		\if jp
		\brief write() のタイムアウト時間の設定
		
		write() のタイムアウト時間を usec で設定する。
		write() はブロックモードでなければならない。
		\param timeout(int) タイムアウト時間 [usec]
		\else
		\brief Set write() timeout
		\param timeout(int) time of timeout [usec]
		\endif
		"""
		self._writeTimeout = timeout


	def setOnWrite(self, on_write):
		"""
		\if jp
		\brief OutWrite コールバックの設定
		\param on_write(Function Object)  コールバックファンクタオブジェクト
		\else
		\brief Set OnWrite callback
		\param on_write(Function Object)
		\endif
		"""
		self._OnWrite = on_write


	def setOnWriteConvert(self, on_wconvert):
		"""
		\if jp
		\brief OutWriteConvert コールバックの設定
		\param on_wconvert(Function Object)  コールバックファンクタオブジェクト
		\else
		\brief Set OnWriteConvert callback
		\param on_wconvert(Function Object)
		\endif
		"""
		self._OnWriteConvert = on_wconvert


	def setOnOverflow(self, on_overflow):
		"""
		\if jp
		\brief OutOverflow コールバックの設定
		\param on_overflow(Function Object)  コールバックファンクタオブジェクト
		\else
		\brief Set OnOverflow callback
		\param on_overflow(Function Object)
		\endif
		"""
		self._OnOverflow = on_overflow


	def setOnRead(self, on_read):
		"""
		\if jp
		\brief OutRead コールバックの設定
		\param on_read(Function Object)  コールバックファンクタオブジェクト
		\else
		\brief Set OnRead callback
		\param on_read(Function Object)
		\endif
		"""
		self._OnRead = on_read


	def setOnReadConvert(self, on_rconvert):
		"""
		\if jp
		\brief OutReadConvert コールバックの設定
		\param on_rconvert(Function Object)  コールバックファンクタオブジェクト
		\else
		\brief Set OnReadConvert callback
		\param on_rconvert(Function Object)
		\endif
		"""
		self._OnReadConvert = on_rconvert


	def setOnUnderflow(self, on_underflow):
		"""
		\if jp
		\brief OutUnderflow コールバックの設定
		\param on_underflow(Function Object)  コールバックファンクタオブジェクト
		\else
		\brief Set OnUnderflow callback
		\param on_underflow(Function Object)
		\endif
		"""
		self._OnUnderflow = on_underflow


	def getPortDataType(self):
		"""
		\brief データ取得のためのメソッド
		データの型名を取得するため、InPortCorbaProviderから呼ばれる。
		added by kurihara
		"""
		val = any.to_any(self._value)
		return str(val.typecode().name())
