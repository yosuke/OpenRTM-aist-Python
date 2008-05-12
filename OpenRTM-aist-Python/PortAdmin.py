#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
 \file PortAdmin.py
 \brief RTC's Port administration class
 \date $Date: 2007/09/03 $
 \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara

 Copyright (C) 2006
     Task-intelligence Research Group,
     Intelligent Systems Research Institute,
     National Institute of
         Advanced Industrial Science and Technology (AIST), Japan
     All rights reserved.
"""

import traceback
import sys

import RTC, RTC__POA
import OpenRTM


class PortAdmin:
	class comp_op:
		def __init__(self, name=None, factory=None):
			if name != None:
				self._name = name
			if factory != None:
				self._name = factory.getProfile().name

		def __call__(self, obj):
			name_ = obj.getProfile().name
			return self._name == name_
    

	class find_port_name:
		def __init__(self, name):
			self._name = name

		def __call__(self, p):
			prof = p.get_port_profile()
			name_ = prof.name 
			return self._name == name_


	class del_port:
		def __init__(self, pa):
			self._pa = pa

		def __call__(self, p):
			self._pa.deletePort(p)


	def __init__(self, orb, poa):
		# ORB オブジェクト
		self._orb = orb

		# POA オブジェクト
		self._poa = poa

		# Portのオブジェクトリファレンスのリスト. PortList
		self._portRefs = []

		# サーバントを直接格納するオブジェクトマネージャ
		self._portServants = OpenRTM.ObjectManager(self.comp_op)


	def getPortList(self):
		"""
		\if jp
		\brief PortList の取得

		registerPort() により登録された Port の PortList へのポインタを返す。
		\return PortList PortList へのポインタ
		\else
		\brief Get PortList

		This operation returns the pointer to the PortList of Ports regsitered
		by registerPort().
		\return PortList+ The pointer points PortList
		\endif
		"""
		return self._portRefs


	def getPortRef(self, port_name):
		"""
		\if jp
		\brief Port のオブジェクト参照の取得

		port_name で指定した Port のオブジェクト参照を返す。
		port_name で指定する Port はあらかじめ registerPort() で登録されてい
		なければならない。
		\param port_name(string) 参照を返すPortの名前
		\return Port_ptr Portのオブジェクト参照
		\else
		\brief Get PortList

		This operation returns the pointer to the PortList of Ports regsitered
		by registerPort().
		\param port_name(string) The name of Port to be returned the reference.
		\return Port_ptr Port's object reference.
		\endif
		"""
		index = OpenRTM.CORBA_SeqUtil.find(self._portRefs, self.find_port_name(port_name))
		if index >= 0:
			return self._portRefs[index]
		return None


	def getPort(self, port_name):
		"""
		\if jp
		\brief Port のサーバントのポインタの取得

		port_name で指定した Port のサーバントのポインタを返す。
		port_name で指定する Port はあらかじめ registerPort() で登録されてい
		なければならない。
		\param port_name(string) 参照を返すPortの名前
		\return PortBase Portサーバント基底クラスのポインタ
		\else
		\brief Getpointer to the Port's servant

		This operation returns the pointer to the PortBase servant regsitered
		by registerPort().
		\param port_name(string) The name of Port to be returned the servant pointer.
		\return PortBase Port's servant's pointer.
		\endif
		"""
		return self._portServants.find(port_name)


	def registerPort(self, port):
		"""
		\if jp
		\brief Port を登録する

		引数 port で指定された Port のサーバントを登録する。
		登録された Port のサーバントはコンストラクタで与えられたPOA 上で
		activate され、そのオブジェクト参照はPortのProfileにセットされる。
		\param port(OpenRTM.PortBase) Port サーバント
		\else
		\brief Regsiter Port

		This operation registers the Port's servant given by argument.
		The given Port's servant will be activated on the POA that is given
		to the constructor, and the created object reference is set
		to the Port's profile.
		\param port(OpenRTM.PortBase) The Port's servant.
		\endif
		"""
		self._portRefs.append(port.getPortRef())
		self._portServants.registerObject(port)


	def deletePort(self, port):
		"""
		\if jp
		\brief Port の登録を削除する

		引数 port で指定された Port の登録を削除する。
		削除時に Port は deactivate され、PortのProfileのリファレンスには、
		nil値が代入される。
		\param port(OpenRTM.PortBase) Port サーバント
		\else
		\brief Delete the Port's registration

		This operation unregisters the Port's registration.
		When the Port is unregistered, Port is deactivated, and the object
		reference in the Port's profile is set to nil.
		\param port(OpenRTM.PortBase) The Port's servant.
		\endif
		"""
		try:
			port.disconnect_all()

			tmp = port.getProfile().name
			OpenRTM.CORBA_SeqUtil.erase_if(self._portRefs, self.find_port_name(tmp))

			self._poa.deactivate_object(self._poa.servant_to_id(port))
			port.setPortRef(RTC.Port._nil)

			self._portServants.unregisterObject(tmp)
		except:
			traceback.print_exception(*sys.exc_info())


	def deletePortByName(self, port_name):
		"""
		\if jp
		\brief Port の登録を削除する

		引数で指定された名前を持つ Port の登録を削除する。
		削除時に Port は deactivate され、PortのProfileのリファレンスには、
		nil値が代入される。
		\param port_name(string) Port の名前
		\else
		\brief Delete the Port' registration

		This operation delete the Port's registration specified by port_ name.
		When the Port is unregistered, Port is deactivated, and the object
		reference in the Port's profile is set to nil.
		\param port_name(string) The Port's name.
		\endif
		"""
		if not port_name:
			return

		p = self._portServants.find(port_name)
		self.deletePort(p)


	def finalizePorts(self):
		"""
		\if jp
		\brief 全ての Port をdeactivateし登録を削除する

		登録されている全てのPortに対して、サーバントのdeactivateを行い、
		登録リストから削除する。
		\else
		\brief Unregister the Port

		This operation deactivates the all Port and deletes the all Port's
		registrations from the list.
		\endif
		"""
		ports = []
		ports = self._portServants.getObjects()
		len_ = len(ports)
		predi = self.del_port(self)
		for i in range(len_):
			idx = (len_ - 1) - i
			predi(ports[idx])
			


