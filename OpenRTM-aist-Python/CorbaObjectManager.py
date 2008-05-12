#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file CorbaObjManager.py
# @brief CORBA Object manager class
# @date $Date: 2007/08/27$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.


from omniORB import CORBA, PortableServer

import OpenRTM


class CorbaObjectManager:
	
	"""
	@if jp
	@class CorbaObjectManager
	@brief CORBA オブジェクトをアクティブ化、非アクティブ化する
	@else
	@class CorbaObjectManager
	@brief Activate and deactivate CORBA objects
	@endif
	"""


	def __init__(self, orb, poa):
		"""
		@if jp
		@brief コンストラクタ
		@param orb(CORBA::ORB)
		@param poa(PortableServer::POA)
		@else
		@brief Constructor
		@param orb(CORBA::ORB)
		@param poa(PortableServer::POA)
		@endif
		"""
		self._orb = orb
		self._poa = poa


	def __del__(self):
		"""
		\if jp
		\brief デストラクタ
		\elqse
		\brief Destructor
		\endif
		"""
		pass


	def activate(self, comp):
		"""
		\if jp
		\brief CORBA オブジェクトをアクティブ化する
		\param comp(OpenRTM.RTObject_impl)
		\else
		\brief Activate CORBA object
		\param comp(OpenRTM.RTObject_impl)
		\endif
		"""
		id_ = self._poa.activate_object(comp)
		obj = self._poa.id_to_reference(id_)
		comp.setObjRef(obj._narrow(OpenRTM.RTObject_impl))


	def deactivate(self, comp):
		"""
		\if jp
		\brief CORBA オブジェクトを非アクティブ化する
		\param comp(OpenRTM.RTObject_impl)
		\else
		\brief Deactivate CORBA object
		\param comp(OpenRTM.RTObject_impl)
		\endif
		"""
		id_ = self._poa.servant_to_id(comp)
		self._poa.deactivate_object(id_)
