#!/usr/bin/env python
# -*- coding: euc-jp -*-


"""
  \file PortCallBack.py
  \brief PortCallBack class
  \date $Date: 2007/09/20 $
  \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
 
  Copyright (C) 2006
      Noriaki Ando
      Task-intelligence Research Group,
      Intelligent Systems Research Institute,
      National Institute of
          Advanced Industrial Science and Technology (AIST), Japan
      All rights reserved.
"""
 

#============================================================
# callback functor base classes
#

class OnWrite:
	"""
	\if jp
	\class OnWrite
	\brief write() 時のコールバック抽象クラス

	DataPortのバッファにデータがwrite()される時に
	このコールバックが呼ばれる。

	\else
	\class OnPut
	\brief OnPut abstract class

	\endif
	"""
	def __init__(self):
		pass

	def __call__(self, value):
		pass


class OnWriteConvert:
	"""
	\if jp
	\class OnWriteConvert
	\brief write() 時のデータ変換コールバック抽象クラス
	
	InPortのバッファにデータが write()される時にこのコールバックが呼ばれ、
	このコールバックの戻り値がバッファに格納される。
	
	\else
	\class OnWriteConvert
	\brief OnWriteConvert abstract class
	
	\endif
	"""
	def __init__(self):
		pass


	def __call__(self,value):
		pass


class OnRead:
	"""
	\if jp
	\class OnRead
	\brief read() 時のコールバック抽象クラス
	
	DataPortのバッファからデータがread()される時に
	このコールバックが呼ばれる。
	
	\else
	\class OnRead
	\brief OnRead abstract class
	
	\endif
	"""
	def __init__(self):
		pass


	def __call__(self):
		pass


class OnReadConvert:
	"""
	\if jp
	\class OnReadConvert
	\brief read() 時のデータ変換コールバック抽象クラス
	
	InPortのバッファからデータが read()される時にこのコールバックが呼ばれ、
	このコールバックの戻り値がread()の戻り値となる。
	
	\else
	\class OnReadConvert
	\brief OnReadConvert abstract class
	
	\endif
	"""
	def __init__(self):
		pass


	def __call__(self,value):
		pass
  

class OnOverflow:
	"""
	\if jp
	\class OnOverflow
	\brief バッファオーバーフロー時のコールバック抽象クラス
	
	バッファにデータがput()される時、バッファオーバーフローが
	生じた場合にこのコールバックが呼ばれる。
	
	\else
	\class OnOverflow
	\brief OnOverflow abstract class
	
	\endif
	"""
	def __init__(self):
		pass


	def __call__(self,value):
		pass


class OnUnderflow:
	"""
	\if jp
	\class OnUnderflow
	\brief Underflow 時のコールバック抽象クラス
	
	InPortのバッファにデータがput()される時にこのコールバックが呼ばれる。
	
	\else
	\class OnUnderflow
	\brief OnUnderflow abstract class
    
	\endif
	"""
	def __init__(self):
		pass


	def __call__(self,value):
		pass
