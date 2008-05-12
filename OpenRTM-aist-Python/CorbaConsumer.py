#!/usr/bin/env python
# -*- coding: euc-jp -*-


##
#  @file CorbaConsumer.py
#   CORBA Consumer class
#  @date $Date: 2007/09/20 $
#  @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
# 
#  Copyright (C) 2006
#      Noriaki Ando
#      Task-intelligence Research Group,
#      Intelligent Systems Research Institute,
#      National Institute of
#          Advanced Industrial Science and Technology (AIST), Japan
#      All rights reserved.

from omniORB import CORBA

##
# @if jp
# @class ConsumerBase
#  オブジェクトリファレンスを保持するプレースホルダ基底クラス
# @else
# @class ConsumerBase
#  Placeholder base class to hold remote object reference.
# @endif

class CorbaConsumerBase:
	

	##
	# @if jp
	#  コンストラクタ
	# @param consumer(CorbaConsumerBase&) CorbaConsumerBaseオブジェクト
	# @else
	#  Consructor
	# @param consumer(CorbaConsumerBase&) CorbaConsumerBase object
	# @endif
	def __init__(self, consumer=None):
		if consumer:
			self._objref = consumer._objref
		else:
			self._objref = None


	def equal(self, consumer):
		self._objref = consumer._objref
		return self

	##
	# @if jp
	#  デストラクタ
	# @else
	#  Destructor
	# @endif
	def __del__(self):
		pass


	##
	# @if jp
	#  CORBAオブジェクトをセットする
	# 
	# 与えられたオブジェクトリファレンスは、ConsumerBase オブジェクト内に
	# 保持される。 
	# 
	# @param obj CORBA オブジェクトのリファレンス
	# @return obj が nil リファレンスの場合 false を返す。
	# @else
	#  Set CORBA Object
	# 
	# The given CORBA Object is held.
	# @param obj Object reference of CORBA object
	# @return If obj is nil reference, it returns false.
	# @endif
	def setObject(self, obj):
		if CORBA.is_nil(obj):
			return False

		self._objref = obj
		return True


	##
	# @if jp
	#  CORBAオブジェクトを取得する
	# 
	# setObject(obj)にて与えられたオブジェクトリファレンスを返す。
	# @return obj CORBA オブジェクトのリファレンス
	# @else
	#  Set CORBA Object
	# 
	# The CORBA Object reference that given by setObject(obj)
	# @return obj Object reference of CORBA object
	# @endif
	def getObject(self):
		return self._objref


	def releaseObject(self):
		self._objref = CORBA.Object._nil


##
# @if jp
# @class Consumer
#  オブジェクトリファレンスを保持するプレースホルダテンプレートクラス
# 
# interfaceType引数で与えられた型のオブジェクトを保持する。
# オブジェクトがセットされたときに、与えられた型で narrow されるので、
# _ptr() で取得するリファレンスは、narrow 済みのリファレンスである。
# @param interfaceType このホルダが保持するオブジェクトの型
# @param consumer このクラス型のオブジェクト
# @else
# @class Consumer
#  Placeholder template class to hold remote object reference.
# 
# This class holds a type of object that given by interfaceType parameter.
# @endif

class CorbaConsumer(CorbaConsumerBase):
	
	##
	# @if jp
	#  コンストラクタ
	# @param interfaceType idlファイルで定義されているインターフェース
	# @param consumer(CorbaConsumer&) CorbaConsumerオブジェクト
	# @else
	#  Consructor
	# @param interfaceType Type of interface defined in your xxx.idl
	# @param consumer(CorbaConsumer&) CorbaConsumer object
	# @endif
	def __init__(self, interfaceType=None, consumer=None):
		if interfaceType:
			self._interfaceType = interfaceType
		else:
			self._interfaceType = None

		if consumer:
			CorbaConsumerBase.__init__(self, consumer)
			self._var = consumer._var
		else:
			CorbaConsumerBase.__init__(self)
			self._var = None


	def equal(self, consumer):
		self._var = consumer._var


	##
	# @if jp
	#  デストラクタ
	# @else
	#  Destructor
	# @endif
	def __del__(self):
		pass


	##
	# @if jp
	#  オブジェクトをセットする
	# ConsumerBase のオーバーライド。 CorbaConsumerBase._objrefにオブジェクト
	# をセットするとともに、interfaceType型で narrow したオブジェクトを
	# メンバ変数に保持する。
	# @param obj CORBA Objecct
	# @return True or False
	# @else
	#  Set Object
	# Override function of ConsumerBase. This operation set an Object to 
	# self._objref in the CorbaConsumerBase class, and this object is narrowed to
	# given interfaceType parameter and stored in the member variable.
	# @param obj CORBA Objecct
	# @return True or False
	# @endif
	def setObject(self, obj):
		if CorbaConsumerBase.setObject(self, obj):
			if self._interfaceType:
				self._var = obj._narrow(self._interfaceType)
			else:
				self._var = self._objref
			if not CORBA.is_nil(self._var):
				return True
		return False


	##
	# @if jp
	#  オブジェクトへnarrow済みのオブジェクトリファレンスを取得
	# 	
	# オブジェクトのリファレンスを取得する。
	# オブジェクトリファレンスを使用するには、setObject() でセット済みで
	# なければならない。
	# オブジェクトがセットされていなければ　nil オブジェクトリファレンスが、
	# 返される。
	# @return interfaceTypeにnarrow済みのオブジェクトのリファレンス
	# @else
	#  Get Object reference narrowed as interfaceType
	# 
	# This operation returns object reference narrowed as interfaceType.
	# To use the returned object reference, reference have to be set by
	# setObject().
	# If object is not set, this operation returns nil object reference.
	# @return The object reference narrowed as interfaceType
	# @endif
	def _ptr(self):
		return self._var


	def releaseObject(self):
		CorbaConsumerBase.releaseObject(self)
		self._var = CORBA.Object._nil
