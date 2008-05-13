#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
 \file Factory.py
 \brief RTComponent factory class
 \date $Date: 2006/11/06 01:28:36 $
 \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara

 Copyright (C) 2003-2005
     Task-intelligence Research Group,
     Intelligent Systems Research Institute,
     National Institute of
         Advanced Industrial Science and Technology (AIST), Japan
     All rights reserved.
"""

import OpenRTM


def Delete(rtc):
    del rtc


class FactoryBase:
	
	"""
	\if jp
	\class FactoryBase
	\brief FactoryBase 基底クラス
	
	コンポーネントファクトリの基底クラス。
	\else
	\class FactoryBase
	\brief FactoryBase base class
	
	RTComponent factory base class.
	\endif
	"""


	def __init__(self, profile):
		"""
		\if jp
		\brief FactoryBase クラスコンストラクタ
	
		FactoryBase クラスのコンストラクタ。
		\param profile(OpenRTM.Properties) コンポーネントのプロファイル
		\else
		\brief FactoryBase class constructor.
		
		FactoryBase class constructor.
		\param profile(OpenRTM.Properties) component profile
		\endif
		"""

		## \var self._Profile Component profile
		self._Profile = profile

		## \var self._Number Number of current component instances.
		self._Number = -1
		
		pass


	def __del__(self):
		pass


	def create(self, mgr):
		"""
		\if jp
		\brief コンポーネントの生成
		
		Python で実装された RTComponent のインスタンスを生成する。
		仮想関数。
		\param mgr(OpenRTM.Manager) Managerオブジェクト
		\else
		\brief Create component
		
		Create component implemented in Python.
		virtual method.
		\param mgr(OpenRTM.Manager) Manager object
		\endif
		"""
		pass


	def destroy(self, comp):
		"""
		\if jp
		\brief コンポーネントの破棄
		
		RTComponent のインスタンスを破棄する。
		仮想関数。
		\param comp(OpenRTM.RTObject_impl) RtcBaseオブジェクト
		\else
		\brief Destroy component
		
		Destroy component instance)
		virtual method.
		\param comp(OpenRTM.RTObject_impl) RtcBase object
		\endif
		"""
		pass


	def profile(self):
		"""
		\if jp
		\brief コンポーネントプロファイルの取得
		
		コンポーネントのプロファイルを取得する
		\else
		\brief Get component profile
	
		Get component profile.
		\endif
		"""
		return self._Profile


	def number(self):
		"""
		\if jp
		\brief 現在のインスタンス数
		
		コンポーネントの現在のインスタンス数を取得する。
		\else
		\brief Get number of component instances
		
		Get number of current component instances.
		\endif
		"""
		return self._Number



class FactoryPython(FactoryBase):
	
	"""
	\if jp
	\class FactoryPython
	\brief FactoryPython クラス
	
	Python用コンポーネントファクトリクラス。
	\else
	\class FactoryPython
	\brief FactoryPython class
	
	RTComponent factory class for Python.
	\endif
	"""


	def __init__(self, profile, new_func, delete_func, policy=None):
		"""
		\if jp
		\brief FactoryPython クラスコンストラクタ
		
		FactoryPython クラスのコンストラクタ。
		プロファイル、クラス名、破棄関数オブジェクトを引数に取り、
		コンポーネントのファクトリクラスを生成する。
		\param profile(OpenRTM.Properties) コンポーネントのプロファイル
		\param new_func(create function object) コンポーネントオブジェクト(クラス名)
		\param delete_func(delete function object) コンポーネントの破棄関数オブジェクト
		\else
		\brief FactoryPython class constructor.
		
		FactoryPython class constructor.
		Create component factory class with three arguments:
		component profile, component class name and
		delete function object.
		\param profile(OpenRTM.Properties) Component profile
		\param new_func(create function object) Component name
		\param delete_func(delete function object) Delete function object
		\endif
		"""

		FactoryBase.__init__(self, profile)
		
		if policy == None:
			self._policy = OpenRTM.DefaultNumberingPolicy()
		else:
			self._policy = policy

		self._New = new_func
    
		self._Delete = delete_func


	def create(self, mgr):
		"""
		\if jp
		\brief コンポーネントの生成
	
		Python で実装された RTComponent のインスタンスを生成する。
		\param mgr(OpenRTM.Manager) Managerオブジェクト
		\else
		\brief Create component
		
		Create component implemented in Python.
		\param mgr(OpenRTM.Manager) Manager object
		\endif
		"""
		try:
			rtobj = self._New(mgr)
			if rtobj == 0:
				return None

			self._Number += 1
			
			rtobj.setProperties(self.profile())
			
			instance_name = rtobj.getTypeName()
			instance_name += self._policy.onCreate(rtobj)
			rtobj.setInstanceName(instance_name)

			return rtobj
		except:
			return None


	def destroy(self, comp):
		"""
		\if jp
		\brief コンポーネントの破棄
	
		RTComponent のインスタンスを破棄する。
		\param comp(OpenRTM.RTObject_impl) RtcBaseオブジェクト
		\else
		\brief Destroy component
		
		Destroy component instance
		\param comp(OpenRTM.RTObject_impl) RtcBase object
		\endif
		"""
		self._Number -= 1
		self._policy.onDelete(comp)
		self._Delete(comp)
