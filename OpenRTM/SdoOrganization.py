#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
  \file SdoOrganization.py
  \brief SDO Organization implementation class
  \date $Date: 2007/09/12 $
  \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
 
  Copyright (C) 2006
      Task-intelligence Research Group,
      Intelligent Systems Research Institute,
      National Institute of
          Advanced Industrial Science and Technology (AIST), Japan
      All rights reserved.
"""


import omniORB.any
from omniORB import CORBA
import threading

import OpenRTM
import SDOPackage, SDOPackage__POA


class ScopedLock:
	def __init__(self, mutex):
		self.mutex = mutex
		self.mutex.acquire()

	def __del__(self):
		self.mutex.release()


# SdoOrganization.o 23788
# 41892

class Organization_impl:
	def __init__(self):
		self._pId = OpenRTM.uuid1()
		self._org_mutex = threading.RLock()

		self._orgProperty = SDOPackage.OrganizationProperty([])
		self._varOwner	  = None
		self._memberList  = []


    #============================================================
    #
    # <<< CORBA interfaces >>>
    #
    #============================================================
	def get_organization_id(self):
		"""
		\if jp

		\brief [CORBA interface] Organization ID を取得する

		Organization の ID を返すオペレーション。

		\return Resource Data Model で定義された Organization ID。
		\exception SDONotExists ターゲットのSDOが存在しない。
		\exception NotAvailable SDOは存在するが応答がない。
		\exception InternalError 内部的エラーが発生した。
		\else

		\brief [CORBA interface] Get Organization Id

		This operation returns the 'id' of the Organization.

		\return The id of the Organization defined in the resource data model.
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		return self._pId


	def get_organization_property(self):
		"""
		\if jp

		\brief [CORBA interface] OrganizationProperty の取得

		Organization が所有する OrganizationProperty を返すオペレーション。
		Organization がプロパティを持たなければ空のリストを返す。

		\return Organization のプロパティのリスト。
		\exception SDONotExists ターゲットのSDOが存在しない。
		\exception NotAvailable SDOは存在するが応答がない。
		\exception InternalError 内部的エラーが発生した。
		\else

		\brief [CORBA interface] Get OrganizationProperty

		This operation returns the OrganizationProperty that an Organization
		has. An empty OrganizationProperty is returned if the Organization does
		not have any properties.

		\return The list with properties of the organization.
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		guard = ScopedLock(self._org_mutex)
		prop = SDOPackage.OrganizationProperty(self._orgProperty.properties)
		return prop


	def get_organization_property_value(self, name):
		"""
		\if jp

		\brief [CORBA interface] OrganizationProperty の特定の値の取得

		OrganizationProperty の指定された値を返すオペレーション。
		引数 "name" で指定されたプロパティの値を返す。

		\param name(string) 値を返すプロパティの名前。
		\return 引数 "name" で指定されたプロパティの値。
		\exception SDONotExists ターゲットのSDOが存在しない。
		\exception InvalidParameter 引数 "namne" で指定されたプロパティが
			存在しない。
		\exception NotAvailable SDOは存在するが応答がない。
		\exception InternalError 内部的エラーが発生した。
		\else

		\brief [CORBA interface] Get specified value of OrganizationProperty

		This operation returns a value in the OrganizationProperty.
		The value to be returned is specified by argument "name."

		\param name(string) The name of the value to be returned.
		\return The value of property which is specified by argument "name."
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		if not name:
			raise SDOPackage.InvalidParameter("Empty name.")

		index = OpenRTM.CORBA_SeqUtil.find(self._orgProperty.properties, self.nv_name(name))

		if index < 0:
			raise SDOPackage.InvalidParameter("Not found.")

		try:
			value = omniORB.any.to_any(self._orgProperty.properties[index].value)
			return value
		except:
			raise SDOPackage.InternalError("get_organization_property_value()")

		# never reach here
		return None


	def set_organization_property(self, org_property):
		"""
		\if jp

		\brief [CORBA interface] OrganizationProperty のセット

		※ SDO Specification の PIM 記述とオペレーション名が異なる。
		※ addOrganizationProperty に対応か？
		OrganizationProperty を Organization に追加するオペレーション。
		OrganizationProperty は Organization のプロパティ記述である。

		\param org_property(SDOPackage::OrganizationProperty) セットする OrganizationProperty
		\return オペレーションが成功したかどうかを返す。
		\exception SDONotExists ターゲットのSDOが存在しない。
		\exception InvalidParameter "org_property" が null。
		\exception NotAvailable SDOは存在するが応答がない。
		\exception InternalError 内部的エラーが発生した。
		\else

		\brief [CORBA interface] Set OrganizationProperty

		※ SDO Specification の PIM 記述とオペレーション名が異なる。
		※ addOrganizationProperty に対応か？
		This operation adds the OrganizationProperty to an Organization. The
		OrganizationProperty is the property description of an Organization.

		\param org_property(SDOPackage::OrganizationProperty) The type of organization to be added.
		\return If the operation was successfully completed.
		\exception SDONotExists The target SDO does not exist.
		\exception InvalidParameter The argument "organizationProperty" is null.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		try:
			guard = ScopedLock(self._org_mutex)
			self._orgProperty = org_property
			return True
		except:
			raise SDOPackage.InternalError("set_organization_property()")

		return False


	def set_organization_property_value(self, name, value):
		"""
		\if jp

		\brief [CORBA interface] OrganizationProperty の値のセット

		OrganizationProperty の NVList に name と value のセットを追加もしくは
		更新するオペレーション。name と value は引数 "name" と "value" により
		指定する。

		\param name(string) 追加・更新されるプロパティの名前。
		\param value(CORBA::Any) 追加・更新されるプロパティの値。
		\return オペレーションが成功したかどうかを返す。
		\exception SDONotExists ターゲットのSDOが存在しない。
		\exception InvalidParameter 引数 "name" で指定されたプロパティは
			存在しない。
		\exception NotAvailable SDOは存在するが応答がない。
		\exception InternalError 内部的エラーが発生した。
		\else

		\brief [CORBA interface] Set specified value of OrganizationProperty

		This operation adds or updates a pair of name and value as a property
		of Organization to/in NVList of the OrganizationProperty. The name and
		the value to be added/updated are specified by argument "name" and
		"value."

		\param name(string) The name of the property to be added/updated.
		\param value(CORBA::Any) The value of the property to be added/updated.
		\return If the operation was successfully completed.
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InvalidParameter The property that is specified by argument
			"name" does not exist.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		if not name:
			raise SDOPackage.InvalidParameter("set_organization_property_value(): Enpty name.")

		index = OpenRTM.CORBA_SeqUtil.find(self._orgProperty.properties, self.nv_name(name))

		if index < 0:
			nv = SDOPackage.NameValue(name, value)
			OpenRTM.CORBA_SeqUtil.push_back(self._orgProperty.properties, nv)
		else:
			self._orgProperty.properties[index].value = value

		return True


	def remove_organization_property(self, name):
		"""
		\if jp

		\brief [CORBA interface] OrganizationProperty の削除

		OrganizationProperty の NVList から特定のプロパティを削除する。
		削除されるプロパティの名前は引数 "name" により指定される。

		\param name(string) 削除するプロパティの名前。
		\return オペレーションが成功したかどうかを返す。
		\exception SDONotExists ターゲットのSDOが存在しない。
		\exception InvalidParameter 引数 "name" で指定されたプロパティは
			存在しない。
		\exception NotAvailable SDOは存在するが応答がない。
		\exception InternalError 内部的エラーが発生した。
		\else

		\brief [CORBA interface] Remove specified OrganizationProperty

		This operation removes a property of Organization from NVList of the
		OrganizationProperty. The property to be removed is specified by
		argument "name."

		\param name(string) The name of the property to be removed.
		\return If the operation was successfully completed.
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InvalidParameter The property that is specified by argument
			"name" does not exist.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		if not name:
			raise SDOPackage.InvalidParameter("remove_organization_property_value(): Enpty name.")

		index = OpenRTM.CORBA_SeqUtil.find(self._orgProperty.properties, self.nv_name(name))

		if index < 0:
			raise SDOPackage.InvalidParameter("remove_organization_property_value(): Not found.")

		try:
			OpenRTM.CORBA_SeqUtil.erase(self._orgProperty.properties, index)
			return True
		except:
			raise SDOPackage.InternalError("remove_organization_property_value()")

		return False


	def get_owner(self):
		"""
		\if jp

		\brief [CORBA interface] Organization のオーナーを取得する

		この Organization のオーナーへの参照を返す。

		\return オーナーオブジェクトへの参照。
		\exception SDONotExists ターゲットのSDOが存在しない。
		\exception NotAvailable SDOは存在するが応答がない。
		\exception InternalError 内部的エラーが発生した。
		\else

		\brief [CORBA interface] Get the owner of the SDO

		This operation returns the SDOSystemElement that is owner of
		the Organization.

		\return Reference of owner object.
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		return self._varOwner


	def set_owner(self, sdo):
		"""
		\if jp

		\brief [CORBA interface] Organization にオーナーをセットする

		Organization に対して SDOSystemElement をオーナーとしてセットする。
		引数 "sdo" にセットする SDOSystemElement を指定する。

		\param sdo(SDOPackage::SDOSystemElement) オーナーオブジェクトの参照。
		\return オペレーションが成功したかどうかを返す。
		\exception SDONotExists ターゲットのSDOが存在しない。
		\exception InvalidParameter 引数 "sdo" が nullである、もしくは、
			"sdo" が存在しない。
		\exception NotAvailable SDOは存在するが応答がない。
		\exception InternalError 内部的エラーが発生した。
		\else

		\brief [CORBA interface] Set the orner of the Organization

		This operation sets an SDOSystemElement to the owner of the
		Organization. The SDOSystemElement to be set is specified by argument
		"sdo."

		\param sdo(SDOPackage::SDOSystemElement) Reference of owner object.
		\return If the operation was successfully completed.
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InvalidParameter The argument "sdo" is null, or the object
			that is specified by "sdo" in argument "sdo" does not exist.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		if CORBA.is_nil(sdo):
			raise SDOPackage.InvalidParameter("set_owner()")

		try:
			self._varOwner = sdo
			return True
		except:
			raise SDOPackage.InternalError("set_owner()")

		return True


	def get_members(self):
		"""
		\if jp

		\brief [CORBA interface] Organization のメンバーを取得する

		Organization のメンバーの SDO のリストを返す。
		メンバーが存在しなければ空のリストを返す。

		\return Organization に含まれるメンバー SDO のリスト。
		\exception SDONotExists ターゲットのSDOが存在しない。
		\exception NotAvailable SDOは存在するが応答がない。
		\exception InternalError 内部的エラーが発生した。
		\else

		\brief [CORBA interface] Get a menber list of the Organization

		This operation returns a list of SDOs that are members of an
		Organization. An empty list is returned if the Organization does not
		have any members.

		\return Member SDOs that are contained in the Organization object.
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		try:
			return self._memberList
		except:
			raise SDOPackage.InternalError("get_members()")


	def set_members(self, sdos):
		"""
		\if jp

		\brief [CORBA interface] SDO の ServiceProfile のセット

		SDO のリストを Organization のメンバーとしてセットする。
		Organization がすでにメンバーの SDO を管理している場合は、
		与えられた SDO のリストに置き換える。

		\param sdos(SDOPackage::SDOのリスト) メンバーの SDO。
		\return オペレーションが成功したかどうかを返す。
		\exception SDONotExists ターゲットのSDOが存在しない。
		\exception InvalidParameter 引数 "SDOList" が nullである、もしくは
			引数に指定された "SDOList" が存在しない。
		\exception NotAvailable SDOは存在するが応答がない。
		\exception InternalError 内部的エラーが発生した。
		\else

		\brief [CORBA interface] Set SDO's ServiceProfile

		This operation assigns a list of SDOs to an Organization as its members.
		If the Organization has already maintained a member SDO(s) when it is
		called, the operation replaces the member(s) with specified list of
		SDOs.

		\param sdos(SDOPackage::SDOのリスト) Member SDOs to be assigned.
		\return If the operation was successfully completed.
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InvalidParameter The argument "SDOList" is null, or if the
			object that is specified by the argument "sdos" does not
			exist.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		if not sdos:
			raise SDOPackage.InvalidParameter("set_members(): SDOList is empty.")

		try:
			self._memberList = sdos
			return True
		except:
			raise SDOPackage.InternalError("set_members()")

		return True


	def add_members(self, sdo_list):
		"""
		\if jp

		\brief [CORBA interface] SDO メンバーの追加

		Organization にメンバーとして SDO を追加する。
		引数 "sdo" に追加するメンバー SDO を指定する。

		\param sdo Organization に追加される SDO のリスト。
		\return オペレーションが成功したかどうかを返す。
		\exception SDONotExists ターゲットのSDOが存在しない。
		\exception InvalidParameter 引数 "sdo" が nullである。
		\exception NotAvailable SDOは存在するが応答がない。
		\exception InternalError 内部的エラーが発生した。
		\else

		\brief [CORBA interface] Add the menebr SDOs

		This operation adds a member that is an SDO to the organization.
		The member to be added is specified by argument "sdo."

		\param sdo The member to be added to the organization.
		\return If the operation was successfully completed.
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InvalidParameter The argument "sdo" is null.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		try:
			OpenRTM.CORBA_SeqUtil.push_back_list(self._memberList, sdo_list)
			return True
		except:
			raise SDOPackage.InternalError("add_members()")

		return False


	def remove_member(self, id):
		"""
		\if jp

		\brief [CORBA interface] SDO メンバーの削除

		Organization から引数で指定された "id" の SDO を削除する。

		\param id(string) 削除する SDO の id。
		\return オペレーションが成功したかどうかを返す。
		\exception SDONotExists ターゲットのSDOが存在しない。
		\exception InvalidParameter 引数 "id" が null もしくは存在しない。
		\exception NotAvailable SDOは存在するが応答がない。
		\exception InternalError 内部的エラーが発生した。
		\else

		\brief [CORBA interface] Remove menber SDO from Organization

		This operation removes a member from the organization. The member to be
		removed is specified by argument "id."

		\param id(string) Id of the SDO to be removed from the organization.
		\return If the operation was successfully completed.
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InvalidParameter The argument "id" is null or does not exist.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		if not id:
			raise SDOPackage.InvalidParameter("remove_member(): Empty name.")

		index = OpenRTM.CORBA_SeqUtil.find(self._memberList, self.sdo_id(id))

		if index < 0:
			raise SDOPackage.InvalidParameter("remove_member(): Not found.")

		try:
			OpenRTM.CORBA_SeqUtil.erase(self._memberList, index)
			return True
		except:
			raise SDOPackage.InternalError("remove_member(): Not found.")

		return False


	def get_dependency(self):
		"""
		\if jp

		\brief [CORBA interface] Organization の DependencyType を取得

		Organization の関係を表す "DependencyType" を返す。

		\return Organizaton の依存関係 DependencyType を返す。
			DependencyType は OMG SDO 仕様の Section 2.2.2 2-3 ページの
			"Data Structures Used by Resource Data Model" を参照。
		\exception SDONotExists ターゲットのSDOが存在しない。
		\exception NotAvailable SDOは存在するが応答がない。
		\exception InternalError 内部的エラーが発生した。
		\else

		\brief [CORBA interface] Get the DependencyType of the Organization

		This operation gets the relationship "DependencyType" of the
		Organization.

		\return The relationship of the Organization as DependencyType.
			DependencyType is defined in Section 2.2.2, "Data Structures
			Used by Resource Data Model," on page 2-3
			of OMG SDO Specification.
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		return self._dependency


	def set_dependency(self, dependency):
		"""
		\if jp

		\brief [CORBA interface] Organization の DependencyType をセットする

		Organization の依存関係 "DependencyType" をセットする。
		引数 "dependencty" により依存関係を与える。

		\param dependency(SDOPackage::DependencyType) Organization の依存関係を表す DependencyType。
			DependencyType は OMG SDO 仕様の Section 2.2.2、2-3 ページの
			"Data Structures Used by Resource Data Model" を参照。
		\return オペレーションが成功したかどうかを返す。
		\exception SDONotExists ターゲットのSDOが存在しない。
		\exception InvalidParameter 引数 "sProfile" が nullである。
		\exception NotAvailable SDOは存在するが応答がない。
		\exception InternalError 内部的エラーが発生した。
		\else

		\brief [CORBA interface] Set the DependencyType of the Organization

		This operation sets the relationship "DependencyType" of the
		Organization. The value to be set is specified by argument "dependency."

		\param dependency(SDOPackage::DependencyType) The relationship of the Organization as
			DependencyType. DependencyType is defined in Section
			2.2.2, "Data Structures Used by Resource Data Model,"
			on page 2-3.
		\return If the operation was successfully completed.
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InvalidParameter The argument "dependency" is null.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		try:
			self._dependency = dependency
			return True
		except:
			raise SDOPackage.InternalError("set_dependency(): Unknown.")

		return False
		

	# end of CORBA interface definition
	#============================================================


	class nv_name:
		def __init__(self, name):
			self._name = name

		def __call__(self, nv):
			return str(self._name) == str(nv.name)

	class sdo_id:
		def __init__(self, id_):
			self._id = id_

		def __call__(self, sdo):
			id_ = sdo.get_sdo_id()
			return str(self._id) == str(id_)
		
