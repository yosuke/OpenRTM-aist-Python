#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
  \file InPort.py
  \brief InPort template class
  \date $Date: 2007/09/20 $
  \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
 
  Copyright (C) 2003-2005
      Task-intelligence Research Group,
      Intelligent Systems Research Institute,
      National Institute of
          Advanced Industrial Science and Technology (AIST), Japan
      All rights reserved.
"""
 

from omniORB import any
import sys
import traceback

import OpenRTM

TIMEOUT_TICK_USEC = 10.0
USEC_PER_SEC      = 1000000.0
TIMEOUT_TICK_SEC = TIMEOUT_TICK_USEC/USEC_PER_SEC


import time
class Time:
	
	def __init__(self):
		tm = time.time()
		tm_f       = tm - int(tm)     # 小数部の取り出し
		self.sec   = int(tm - tm_f)   # 整数部の取り出し
		self.usec  = int(tm_f * USEC_PER_SEC) # sec -> usec (micro second)


class InPort:
	
	"""
	\if jp
	
	\class InPort
	
	\brief InPort クラス
 
        InPort の実装である
        インスタンス生成時にRingBufferまたは、NullBufferのインスタンスを
		buff_として渡す必要がある。
        データはフラグによって未読、既読状態が管理され、isNew(), getNewDataLen()
        getNewList(), getNewListReverse() 等のメソッドによりハンドリングすることが
        できる。
	\endif
	"""


	def __init__(self, name, value, buffer_,
				 read_block=False, write_block=False,
				 read_timeout=0, write_timeout = 0):
		"""
		\if jp
		\brief InPort クラスコンストラクタ
		
		InPortクラスのコンストラクタ。
		\param name(string) InPort 名。InPortBase:name() により参照される。
		\param value(data) この InPort にバインドされる T 型の変数
		\param buffer_(OpenRTM.BufferBase) InPort で使用するバッファのオブジェクト
		\param read_block(bool)
		\param write_block(bool)
		\param read_timeout(int)
		\param write_timeout(int)
		\else
		\brief A constructor.
		
		Setting channel name and registering channel value.
		\param name(string) A name of the InPort. This name is referred by
		InPortBase::name().
		\param value(data) A channel value related with the channel.
		\param buffer_(OpenRTM.BufferBase) Buffer Object which is used in InPort 
		\param read_block(bool)
		\param write_block(bool)
		\param read_timeout(int)
		\param write_timeout(int)
		\endif
		"""
		self._buffer         = buffer_
		self._name           = name
		self._value          = value
		self._readBlock      = read_block
		self._readTimeout    = read_timeout
		self._writeBlock     = write_block
		self._writeTimeout   = write_timeout
		self._OnWrite        = None
		self._OnWriteConvert = None
		self._OnRead         = None
		self._OnReadConvert  = None
		self._OnOverflow     = None
		self._OnUnderflow    = None


	def __del__(self):
		"""
		\if jp
		\brief InPortクラスデストラクタ
		
		InPortクラスのデストラクタ。
		\else
		\brief A destructor
		\endif
		"""
		pass


	def isNew(self):
		return self._buffer.isNew()
	

	def name(self):
		return self._name


	def write(self, value):
		"""
		\if jp
		\brief DataPort に値を書き込む

		DataPort に値を書き込む。

		- コールバックファンクタ OnWrite がセットされている場合、
			InPort が保持するバッファに書き込む前に OnWrite が呼ばれる。
		- InPort が保持するバッファがオーバーフローを検出できるバッファであり、
			かつ、書き込む際にバッファがオーバーフローを検出した場合、
			コールバックファンクタ OnOverflow が呼ばれる。
		- コールバックファンクタ OnWriteConvert がセットされている場合、
			バッファ書き込み時に、OnWriteConvert の operator()() の戻り値が
			バッファに書き込まれる。
		- setWriteTimeout() により書き込み時のタイムアウトが設定されている場合、
			タイムアウト時間だけバッファフル状態が解除するのを待ち、
			OnOverflowがセットされていればこれを呼び出して戻る。
		\param value(data)
		\else
		\brief 
		\param value(data)
		\endif
		"""
		if self._OnWrite:
			self._OnWrite(value)

		timeout = self._writeTimeout

		tm_pre = Time()

		# blocking and timeout wait
		while self._writeBlock and self._buffer.isFull():
			if self._writeTimeout < 0:
				time.sleep(TIMEOUT_TICK_SEC)
				continue

			# timeout wait
			tm_cur = Time()

			sec  = tm_cur.sec - tm_pre.sec
			usec = tm_cur.usec - tm_pre.usec

			timeout -= (sec * USEC_PER_SEC + usec)

			if timeout < 0:
				break

			tm_pre = tm_cur
			time.sleep(TIMEOUT_TICK_USEC)

		if self._buffer.isFull() and self._OnOverflow:
			self._OnOverflow(value)
			return False

		if not self._OnWriteConvert:
			self._buffer.put(value)
		else:
			self._buffer.put(self._OnWriteConvert(value))

		return True


	def read(self):
		"""
		\if jp
		\brief DataPort から値を読み出す

		DataPort から値を読み出す

		- コールバックファンクタ OnRead がセットされている場合、
			DataPort が保持するバッファから読み出す前に OnRead が呼ばれる。
		- DataPort が保持するバッファがアンダーフローを検出できるバッファで、
			かつ、読み出す際にバッファがアンダーフローを検出した場合、
			コールバックファンクタ OnUnderflow が呼ばれる。
		- コールバックファンクタ OnReadConvert がセットされている場合、
			バッファ書き込み時に、OnReadConvert の operator()() の戻り値が
			read()の戻り値となる。
		- setReadTimeout() により読み出し時のタイムアウトが設定されている場合、
			バッファアンダーフロー状態が解除されるまでタイムアウト時間だけ待ち、
			OnUnderflowがセットされていればこれを呼び出して戻る
		\else
		\brief [CORBA interface] Put data on InPort
		\endif
		"""
		if self._OnRead:
			self._OnRead()

		timeout = self._readTimeout

		tm_pre = Time()

		# blocking and timeout wait
		while self._readBlock and self._buffer.isEmpty():
			if self._readTimeout < 0:
				time.sleep(TIMEOUT_TICK_SEC)
				continue

			# timeout wait
			tm_cur = Time()

			sec  = tm_cur.sec - tm_pre.sec
			usec = tm_cur.usec - tm_pre.usec
			
			timeout -= (sec * USEC_PER_SEC + usec)

			if timeout < 0:
				break

			tm_pre = tm_cur
			time.sleep(TIMEOUT_TICK_SEC)

		if self._buffer.isEmpty():
			if self._OnUnderflow:
				self._value = self._OnUnderflow()
			return self._value

		if not self._OnReadConvert:
			self._value = self._buffer.get()
			return self._value
		else:
			self._value = self._OnReadConvert(self._buffer.get())
			return self._value

		# never comes here
		return self._value


	def init(self, value):
		"""
		\if jp
		\brief InPort 内のリングバッファの値を初期化
		
		InPort 内のリングバッファの値を初期化する。
		\param value(data)
		\else
		\brief Initialize ring buffer value of InPort
		\endif
		"""
		pass
    
    
	def update(self):
		"""
		\if jp
		\brief バインドされた変数self._valueに InPort バッファの最新値を読み込む
		
		バインドされたデータに InPort の最新値を読み込む。
		\else
		\brief Read data from current InPort
		\endif
		"""
		try:
			self._value = self._buffer.get()
		except:
			if self._OnUnderflow:
				self._OnUnderflow()
			else:
				traceback.print_exception(*sys.exc_info())
				
		return
    
    
	"""
      \if jp
     
      \brief 未読の新しいデータ数を取得する
     
      \else
     
      \brief Get number of new data to be read.
     
      \endif

	def getNewDataLen(self):
		return self._buffer.new_data_len()
	"""

    
	"""
      \if jp
     
      \brief 未読の新しいデータを取得する
     
      \else
     
      \brief Get new data to be read.
     
      \endif

	def getNewList(self):
		return self._buffer.get_new_list()

	"""

    
	"""
      \if jp
     
      \brief 未読の新しいデータを逆順(新->古)で取得する
     
      \else
     
      \brief Get new data to be read.
     
      \endif

	def getNewListReverse(self):
		return self._buffer.get_new_rlist()
	"""


	def setOnWrite(self, on_write):
		"""
		\if jp
		\brief InPort バッファにデータ入力時のコールバックの設定
		
		InPort が持つバッファにデータがputされたときに呼ばれるコールバック
		オブジェクトを設定する。設定されるコールバックオブジェクトは
		InPort<DataType>::OnPutクラスを継承し、引数 const DataType& 、
		戻り値 void の operator() 関数が実装されている必要がある。
		
		struct MyOnPutCallback : public InPort<DataType> {<br>
        void operator()(const DataType data) {<br>
		処理<br>
        }<br>
		};<br>
		のようにコールバックオブジェクトを実装し、<br>
		<br> 
		m_inport.setOnPut(new MyOnPutCallback());<br>
		のようにコールバックオブジェクトをセットする。
		\param on_write(function object)
		
		\else
		\brief Get new data to be read.
		\param on_write(function object)
		\endif
		"""
		self._OnWrite = on_write


	def setOnWriteConvert(self, on_wconvert):
		"""
		 \brief InPort バッファにデータ入力時のコールバックの設定
		 \param on_wconvert(function object)
		"""
		self._OnWriteConvert = on_wconvert


	def setOnRead(self, on_read):
		"""
		 \brief InPort バッファからデータ読み込み時のコールバックの設定
		 \param on_read(function object)
		"""
		self._OnRead = on_read


	def setOnReadConvert(self, on_rconvert):
		"""
		 \brief InPort バッファからデータ読み込み時のコールバックの設定
		 \param on_rconvert(function object)
		"""
		self._OnReadConvert = on_rconvert


	def setOnOverflow(self, on_overflow):
		"""
		 \brief InPort バッファに関するコールバックの設定
		 \param on_overflow(function object)
		"""
		self._OnOverflow = on_overflow


	def setOnUnderflow(self, on_underflow):
		"""
		 \brief InPort バッファに関するコールバックの設定
		 \param on_underflow(function object)
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
