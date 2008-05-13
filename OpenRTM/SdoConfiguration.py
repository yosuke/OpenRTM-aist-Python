#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
 \file SdoConfiguration.py
 \brief RT component base class
 \date $Date: 2007/09/06$
 \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara

 Copyright (C) 2006
     Task-intelligence Research Group,
     Intelligent Systems Research Institute,
     National Institute of
         Advanced Industrial Science and Technology (AIST), Japan
     All rights reserved.
"""


import copy
import threading

import OpenRTM
import SDOPackage, SDOPackage__POA

class ScopedLock:
	def __init__(self, mutex):
		self.mutex = mutex
		self.mutex.acquire()

	def __del__(self):
		self.mutex.release()


# SdoConfiguration with SeqEx 159120
# SdoConfiguration with SeqUtil 114504 114224

def toProperties(prop, conf):
	OpenRTM.NVUtil.copyToProperties(prop, conf.configuration_data)


def toConfigurationSet(conf, prop):
	conf.description = prop.getProperty("description")
	conf.id = prop.getName()
	OpenRTM.NVUtil.copyFromProperties(conf.configuration_data, prop)


	
class Configuration_impl(SDOPackage__POA.Configuration):
	"""
	\if jp

	\class Configuration_impl
	\brief SDO Configuration 実装クラス

	Configuration interface は Resource Data Model で定義されたデータの
	追加、削除等の操作を行うためのインターフェースである。
	DeviceProfile, ServiceProfile, ConfigurationProfile および Organization
	の変更を行うためのオペレーションを備えている。SDO の仕様ではアクセス制御
	およびセキュリティに関する詳細については規定していない。

	複数の設定 (Configuration) を保持することにより、容易かつ素早くある設定
	を反映させることができる。事前に定義された複数の設定を ConfigurationSets
	および configuration profile として保持することができる。ひとつの
	ConfigurationSet は特定の設定に関連付けられた全プロパティ値のリストを、
	ユニークID、詳細とともに持っている。これにより、各設定項目の詳細を記述し
	区別することができる。Configuration interface のオペレーションはこれら
	ConfiguratioinSets の管理を支援する。


	- ConfigurationSet: id, description, NVList から構成される1セットの設定
	- ConfigurationSetList: ConfigurationSet のリスト
	- Parameter: name, type, allowed_values から構成されるパラメータ定義。
	- ActiveConfigurationSet: 現在有効なコンフィギュレーションの1セット。

	以下、SDO仕様に明記されていないもしくは解釈がわからないため独自解釈

	以下の関数は ParameterList に対して処理を行う。
	- get_configuration_parameters()

	以下の関数はアクティブなConfigurationSetに対する処理を行う
	- get_configuration_parameter_values()
	- get_configuration_parameter_value()
	- set_configuration_parameter()

	以下の関数はConfigurationSetListに対して処理を行う
	- get_configuration_sets()
	- get_configuration_set()
	- set_configuration_set_values()
	- get_active_configuration_set()
	- add_configuration_set()
	- remove_configuration_set()
	- activate_configuration_set()

	\else

	\class Configuration_impl
	\brief Configuration implementation class

	Configuration interface provides operations to add or remove data
	specified in resource data model. These operations provide functions to
	change DeviceProfile, ServiceProfile, ConfigurationProfile, and
	Organization. This specification does not address access control or
	security aspects. Access to operations that modifies or removes profiles
	should be controlled depending upon the application.

	Different configurations can be stored for simple and quick activation.
	Different predefined configurations are stored as different
	ConfigurationSets or configuration profile. A ConfigurationSet stores the
	value of all properties assigned for the particular configuration along
	with its unique id and description to identify and describe the
	configuration respectively. Operations in the configuration interface
	help manage these ConfigurationSets.

	\endif
	"""

	def __init__(self, configsets):
		"""
		 \param configsets(OpenRTM.ConfigAdmin)
		"""

		"""
		 \var self._deviceProfile SDO DeviceProfile with mutex lock
		"""
		self._deviceProfile = None
		self._dprofile_mutex = threading.RLock()

		"""
		 \var self._serviceProfiles SDO ServiceProfileList
		"""
		self._serviceProfiles = []
		self._sprofile_mutex = threading.RLock()

		self._parameters = []
		self._params_mutex = threading.RLock()

		self._configsets = configsets
		self._config_mutex = threading.RLock()

		"""
		 \var self._organizations SDO OrganizationList
		"""
		self._organizations = []
		self._org_mutex = threading.RLock()

		self._objref = self._this()


    #============================================================
    #
    # <<< CORBA interfaces >>>
    #
    #============================================================
	def set_device_profile(self, dProfile):
		"""
		\if jp

		\brief [CORBA interface] SDO の DeviceProfile をセットする

		このオペレーションは SDO の DeviceProfile をセットする。SDO が
		DeviceProfile を保持している場合は新たな DeviceProfile を生成し、
		DeviceProfile をすでに保持している場合は既存のものと置き換える。

		\param dProfile(SDOPackage::DeviceProfile) SDO に関連付けられる DeviceProfile。
		\return オペレーションが成功したかどうかを返す。
		\exception SDONotExists ターゲットのSDOが存在しない。
		\exception NotAvailable SDOは存在するが応答がない。
		\exception InvalidParameter 引数 "dProfile" が null である。
		\exception InternalError 内部的エラーが発生した。

		\else

		\brief [CORBA interface] Set DeviceProfile of SDO

		This operation sets the DeviceProfile of an SDO. If the SDO does not
		have DeviceProfile, the operation will create a new DeviceProfile,
		otherwise it will replace the existing DeviceProfile.

		\param dProfile(SDOPackage::DeviceProfile) The device profile that is to be assigned to this SDO.
		\return If the operation was successfully completed.
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InvalidParameter The argument "dProfile" is null.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		try:
			guard = ScopedLock(self._dprofile_mutex)
			self._deviceProfile = dProfile
		except:
			raise SDOPackage.InternalError("Unknown Error")

		return True


	def set_service_profile(self, sProfile):
		"""
		\if jp

		\brief [CORBA interface] SDO の ServiceProfile のセット

		このオペレーションはこの Configuration interface を所有する対象 SDO の
		ServiceProfile を設定する。もし引数の ServiceProfile の id が空であれば
		新しい ID が生成されその ServiceProfile を格納する。もし id が空で
		なければ、SDO は同じ id を持つ ServiceProfile を検索する。
		同じ id が存在しなければこの ServiceProfile を追加し、id が存在すれば
		上書きをする。

		\param sProfile(SDOPackage::ServiceProfile) 追加する ServiceProfile
		\return オペレーションが成功したかどうかを返す。
		\exception SDONotExists ターゲットのSDOが存在しない。
		\exception InvalidParameter 引数 "sProfile" が nullである。
		\exception NotAvailable SDOは存在するが応答がない。
		\exception InternalError 内部的エラーが発生した。
		\else

		\brief [CORBA interface] Set SDO's ServiceProfile

		This operation adds ServiceProfile to the target SDO that navigates this
		Configuration interface. If the id in argument ServiceProfile is null,
		new id is created and the ServiceProfile is stored. If the id is not
		null, the target SDO searches for ServiceProfile in it with the same id.
		It adds the ServiceProfile if not exist, or overwrites if exist.

		\param sProfile(SDOPackage::ServiceProfile) ServiceProfile to be added.
		\return If the operation was successfully completed.
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InvalidParameter The argument "sProfile" is null.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		try:
			if not sProfile.id:
				prof = sProfile
				prof.id = self.getUUID()
				OpenRTM.CORBA_SeqUtil.push_back(self._serviceProfiles, prof)
				return True

			index = OpenRTM.CORBA_SeqUtil.find(self._serviceProfiles,
											   self.service_id(sProfile.id))
			if index >= 0:
				OpenRTM.CORBA_SeqUtil.erase(self._serviceProfiles, index)

			OpenRTM.CORBA_SeqUtil.push_back(self._serviceProfiles, sProfile)
			return True
		except:
			raise SDOPackage.InternalError("Configuration.set_service_profile")

		return True


	def add_organization(self, org):
		"""
		\if jp

		\brief [CORBA interface] Organization の追加

		このオペレーションは Organization object のリファレンスを追加する。

		\param org(SDOPackage::Organization) 追加する Organization
		\return オペレーションが成功したかどうかを返す。
		\exception SDONotExists ターゲットのSDOが存在しない。
		\exception NotAvailable SDOは存在するが応答がない。
		\exception InvalidParameter 引数 "organization" が null である。
		\exception InternalError 内部的エラーが発生した。
		\else

		\brief [CORBA interface] Add Organization

		This operation adds reference of an Organization object.

		\param org(SDOPackage::Organization) Organization to be added.
		\return If the operation was successfully completed.
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InvalidParameter The argument “organization” is null.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		try:
			OpenRTM.CORBA_SeqUtil.push_back(self._organizations, org)
		except:
			raise SDOPackage.InternalError("Configuration.add_organization")

		return True


	def remove_service_profile(self, id_):
		"""
		\if jp

		\brief [CORBA interface] ServiceProfile の削除

		このオペレーションはこの Configuration interface を持つ SDO の
		Service の ServiceProfile を削除する。削除する ServiceProfile
		は引数により指定される。

		\param id_(string) 削除する ServcieProfile の serviceID。
		\return オペレーションが成功したかどうかを返す。
		\exception SDONotExists ターゲットのSDOが存在しない。
		\exception InvalidParameter 引数 "id" が null である。もしくは "id" に
			関連付けられた ServiceProfile が存在しない。
		\exception NotAvailable SDOは存在するが応答がない。
		\exception InternalError 内部的エラーが発生した。
		\else

		\brief [CORBA interface] Remove ServiceProfile

		This operation removes ServiceProfile object to the SDO that has this
		Configuration interface. The ServiceProfile object to be removed is
		specified by argument.

		\param id_(string) serviceID of a ServiceProfile to be removed.
		\return If the operation was successfully completed.
		\exception SDONotExists The target SDO does not exist.
		\exception InvalidParameter The argument "sProfile" is null, or if the
			object that is specified by argument "sProfile" does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		try:
			OpenRTM.CORBA_SeqUtil.erase_if(self._serviceProfiles, self.service_id(id_))
		except:
			raise SDOPackage.InternalError("Configuration.remove_service_profile")

		return True


	def remove_organization(self, organization_id):
		"""
		\if jp

		\brief [CORBA interface] Organization の参照の削除

		このオペレーションは Organization の参照を削除する。

		\param organization_id(string) 削除する Organization の一意な id。
		\return オペレーションが成功したかどうかを返す。
		\exception SDONotExists ターゲットのSDOが存在しない。
		\exception InvalidParameter 
		\exception NotAvailable SDOは存在するが応答がない。
		\exception InternalError 内部的エラーが発生した。
		\else

		\brief [CORBA interface] Remove the reference of Organization 

		This operation removes the reference of an Organization object.

		\param organization_id(string) Unique id of the organization to be removed.
		\return If the operation was successfully completed.
		\exception SDONotExists The target SDO does not exist.
		\exception InvalidParameter The argument "organizationID" is null,
			or the object which is specified by argument "organizationID"
			does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		try:
			guard = ScopedLock(self._org_mutex)
			OpenRTM.CORBA_SeqUtil.erase_if(self._organizations,
										   self.org_id(organization_id))
		except:
			raise SDOPackage.InternalError("Configuration.remove_organization")

		return True


	def get_configuration_parameters(self):
		"""
		\if jp

		\brief [CORBA interface] 設定パラメータのリストの取得

		このオペレーションは configuration parameter のリストを返す。
		SDO が設定可能なパラメータを持たなければ空のリストを返す。

		\return 設定を特徴付けるパラメータ定義のリスト。
		\exception SDONotExists ターゲットのSDOが存在しない。
		\exception NotAvailable SDOは存在するが応答がない。
		\exception InternalError 内部的エラーが発生した。
		\else

		\brief [CORBA interface] Getting a list of configuration parameter

		This operation returns a list of Parameters. An empty list is returned
		if the SDO does not have any configurable parameter.

		\return The list with definitions of parameters characterizing the
			configuration.
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		try:
			guard = ScopedLock(self._params_mutex)
			param = copy.copy(self._parameters)
			return param
		except:
			raise SDOPackage.InternalError("Configuration.get_configuration_parameters")

		return []


	def get_configuration_parameter_values(self):
		"""
		\if jp

		\brief [CORBA interface] Configuration parameter の値のリストの取得

		このオペレーションは configuration パラメータおよび値を返す。

		\return 全ての configuration パラメータと値のリスト。
		\exception SDONotExists ターゲットのSDOが存在しない。
		\exception NotAvailable SDOは存在するが応答がない。
		\exception InternalError 内部的エラーが発生した。
		\else

		\brief [CORBA interface] Getting value list of configuration parameter

		This operation returns all configuration parameters and their values.

		\return List of all configuration parameters and their values.
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		guard = ScopedLock(self._config_mutex)
		nvlist = []
		return nvlist


	def get_configuration_parameter_value(self, name):
		"""
		\if jp

		\brief [CORBA interface] Configuration parameter の値の取得

		このオペレーションは引数 "name" で指定されたパラメータ値を返す。

		\param name(string) 値を要求するパラメータの名前。
		\return 指定されたパラメータの値。
		\exception SDONotExists ターゲットのSDOが存在しない。
		\exception NotAvailable SDOは存在するが応答がない。
		\exception InternalError 内部的エラーが発生した。
		\else

		\brief [CORBA interface] Getting value of configuration parameter

		This operation returns a value of parameter that is specified by
		argument "name."

		\param name(string) Name of the parameter whose value is requested.
		\return The value of the specified parameter.
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		if not name:
			raise SDOPackage.InvalidParameter("Name is empty.")

		return None


	def set_configuration_parameter(self, name, value):
		"""
		\if jp

		\brief [CORBA interface] Configuration パラメータの変更

		このオペレーションは "name" で指定したパラメータの値を "value" に
		変更する。

		\param name(string) 変更したいパラメータの名前。
		\param value(CORBA.Any) 変更したいパラメータの値。
		\return オペレーションが成功したかどうかを返す。
		\exception SDONotExists ターゲットのSDOが存在しない。
		\exception NotAvailable SDOは存在するが応答がない。
		\exception InternalError 内部的エラーが発生した。
		\else

		\brief [CORBA interface] Modify the parameter value

		This operation sets a parameter to a value that is specified by argument
		"value." The parameter to be modified is specified by argument " name."

		\param name(string) The name of parameter to be modified.
		\param value(CORBA.Any) New value of the specified parameter.
		\return If the operation was successfully completed.
		\exception SDONotExists The target SDO does not exist.
		\exception InvalidParameter if arguments ("name" and/or "value") is
			null, or if the parameter that is specified by the argument
			"name" does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		return True


	def get_configuration_sets(self):
		"""
		\if jp

		\brief [CORBA interface] ConfigurationSet リストの取得 

		このオペレーションは ConfigurationProfile が持つ ConfigurationSet の
		リストを返す。 SDO が ConfigurationSet を持たなければ空のリストを返す。

		\return 保持している ConfigurationSet のリストの現在値。
		\exception SDONotExists ターゲットのSDOが存在しない。
		\exception NotAvailable SDOは存在するが応答がない。
		\exception InternalError 内部的エラーが発生した。
		\else

		\brief [CORBA interface] Getting list of ConfigurationSet

		This operation returns a list of ConfigurationSets that the
		ConfigurationProfile has. An empty list is returned if the SDO does not
		have any ConfigurationSets.
		This operation returns a list of all ConfigurationSets of the SDO.
		If no predefined ConfigurationSets exist, then empty list is returned.

		\return The list of stored configuration with their current values.
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		try:
			guard = ScopedLock(self._config_mutex)

			cf = self._configsets.getConfigurationSets()
			len_ = len(cf)

			config_sets = [SDOPackage.ConfigurationSet("","",[]) for i in range(len_)]
			for i in range(len_):
				toConfigurationSet(config_sets[i], cf[i])

			return config_sets

		except:
			raise SDOPackage.InternalError("Configuration.get_configuration_sets")

		return []


	def get_configuration_set(self, config_id):
		"""
		\if jp

		\brief [CORBA interface] ConfigurationSet の取得

		このオペレーションは引数で指定された ConfigurationSet の ID に関連
		付けられた ConfigurationSet を返す。

		\param config_id(string) ConfigurationSet の識別子。
		\return 引数により指定された ConfigurationSet。
		\exception SDONotExists ターゲットのSDOが存在しない。
		\exception InvalidParameter "config_id" が null か、指定された
			ConfigurationSet が存在しない。
		\exception NotAvailable SDOは存在するが応答がない。
		\exception InternalError 内部的エラーが発生した。
		\else

		\brief [CORBA interface] Getting a ConfigurationSet

		This operation returns the ConfigurationSet specified by the parameter
		configurationSetID.

		\param config_id(string) Identifier of ConfigurationSet requested.
		\return The configuration set specified by the parameter config_id.
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		if not config_id:
			raise SDOPackage.InvalidParameter("ID is empty")

		guard = ScopedLock(self._config_mutex)

		if not self._configsets.haveConfig(config_id):
			raise SDOPackage.InvalidParameter("No such ConfigurationSet")

		configset = self._configsets.getConfigurationSet(config_id)

		try:
			config = SDOPackage.ConfigurationSet("","",[])
			toConfigurationSet(config, configset)
			return config
		except:
			raise SDOPackage.InvalidError("Configuration::get_configuration_set()")

		return SDOPackage.ConfigurationSet("","",[])


	def set_configuration_set_values(self, config_id, configuration_set):
		"""
		\if jp

		\brief [CORBA interface] ConfigurationSet をセットする

		このオペレーションは指定された id の ConfigurationSet を更新する。

		\param configu_id(string) 変更する ConfigurationSet の ID。
		\param configuration_set(SDOPackage::ConfigurationSet) 変更する ConfigurationSet そのもの。
		\return ConfigurationSet が正常に更新できた場合は true。
			そうでなければ false を返す。
		\exception InvalidParameter config_id が null か ConfigurationSet
		\exception SDONotExists ターゲットのSDOが存在しない。
		\exception NotAvailable SDOは存在するが応答がない。
		\exception InternalError 内部的エラーが発生した。
		\else

		\brief [CORBA interface] Set ConfigurationSet

		This operation modifies the specified ConfigurationSet of an SDO.

		※ パラメータの数が spec と IDL で異なる！！！
		\param configu_id(string) The ID of ConfigurationSet to be modified.
		\param configuration_set(SDOPackage::ConfigurationSet) ConfigurationSet to be replaced.
		\return A flag indicating if the ConfigurationSet was modified 
			successfully. "true" - The ConfigurationSet was modified
			successfully. "false" - The ConfigurationSet could not be
			modified successfully.
		\exception InvalidParameter if the parameter 'configurationSetID' is
			null or if there is no ConfigurationSet stored with such id.
			This exception is also raised if one of the attributes
			defining ConfigurationSet is not valid.
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		if not config_id:
			raise SDOPackage.InvalidParameter("ID is empty.")


		try:
			conf = OpenRTM.Properties(key=config_id)
			toProperties(conf, configuration_set)
			return self._configsets.setConfigurationSetValues(config_id, conf)
		except:
			raise SDOPackage.InvalidError("Configuration::set_configuration_set_values()")

		return True


	def get_active_configuration_set(self):
		"""
		\if jp

		\brief [CORBA interface] アクティブな ConfigurationSet を取得する

		このオペレーションは当該SDOの現在アクティブな ConfigurationSet を返す。
		(もしSDOの現在の設定が予め定義された ConfigurationSet により設定されて
		いるならば。)
		ConfigurationSet は以下の場合にはアクティブではないものとみなされる。

		- 現在の設定が予め定義された ConfigurationSet によりセットされていない、
		- SDO の設定がアクティブになった後に変更された、
		- SDO を設定する ConfigurationSet が変更された、

		これらの場合には、空の ConfigurationSet が返される。

		\return 現在アクティブな ConfigurationSet。
		\exception SDONotExists ターゲットのSDOが存在しない。
		\exception NotAvailable SDOは存在するが応答がない。
		\exception InternalError 内部的エラーが発生した。
		\else

		\brief [CORBA interface] Get active ConfigurationSet

		This operation returns the current active ConfigurationSet of an
		SDO (i.e., if the current configuration of the SDO was set using
		predefined configuration set).
		ConfigurationSet cannot be considered active if the:

		- current configuration of the SDO was not set using any predefined
			ConfigurationSet, or
		- configuration of the SDO was changed after it has been active, or
		- ConfigurationSet that was used to configure the SDO was modified.

		Empty ConfigurationSet is returned in these cases.

		\return The active ConfigurationSet.
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		if not self._configsets.isActive():
			raise SDOPackage.NotAvailable()

		try:
			guard = ScopedLock(self._config_mutex)
			config = SDOPackage.ConfigurationSet("","",[])
			toConfigurationSet(config, self._configsets.getActiveConfigurationSet())
			return config
		except:
			raise SDOPackage.InternalError("Configuration.get_active_configuration_set()")

		return SDOPackage.ConfigurationSet("","",[])


	def add_configuration_set(self, configuration_set):
		"""
		\if jp

		\brief [CORBA interface] ConfigurationSet を追加する

		ConfigurationProfile に ConfigurationSet を追加するオペレーション。

		\param configuration_set(SDOPackage::ConfigurationSet) 追加される ConfigurationSet。
		\return オペレーションが成功したかどうか。
		\exception SDONotExists ターゲットのSDOが存在しない。
		\exception NotAvailable SDOは存在するが応答がない。
		\exception InternalError 内部的エラーが発生した。
		\else

		\brief [CORBA interface] Add ConfigurationSet

		This operation adds a ConfigurationSet to the ConfigurationProfile.

		\param configuration_set(SDOPackage::ConfigurationSet) The ConfigurationSet that is added.
		\return If the operation was successfully completed.
		\exception SDONotExists The target SDO does not exist.
		\exception InvalidParameter If the argument "configurationSet" is null,
			or if one of the attributes defining "configurationSet" is
			invalid, or if the specified identifier of the configuration
			set already exists.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		try:
			guard = ScopedLock(self._config_mutex)
			config_id = configuration_set.id
			config = OpenRTM.Properties(key=config_id)
			toProperties(config, configuration_set)
			return self._configsets.addConfigurationSet(config)
		except:
			raise SDOPackage.InternalError("Configuration::add_configuration_set()")

		return True


	def remove_configuration_set(self, config_id):
		"""
		\if jp

		\brief [CORBA interface] ConfigurationSet を削除する

		ConfigurationProfile から ConfigurationSet を削除する。

		\param configu_id(string) 削除する ConfigurationSet の id。
		\return オペレーションが成功したかどうか。
		\exception SDONotExists ターゲットのSDOが存在しない。
		\exception InvalidParameter 引数 "configurationSetID" が null である、
			もしくは、引数で指定された ConfigurationSet が存在しない。
		\exception NotAvailable SDOは存在するが応答がない。
		\exception InternalError 内部的エラーが発生した。
		\else

		\brief [CORBA interface] Remove ConfigurationSet

		This operation removes a ConfigurationSet from the ConfigurationProfile.

		\param config_id(string) The id of ConfigurationSet which is removed.
		\return If the operation was successfully completed.
		\exception SDONotExists The target SDO does not exist.
		\exception InvalidParameter The arguments "configurationSetID" is null,
			or if the object specified by the argument
			"configurationSetID" does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		if not config_id:
			raise SDOPackage.InvalidParameter("ID is empty.")
			
		try:
			guard = ScopedLock(self._config_mutex)
			return self._configsets.removeConfigurationSet(config_id)
		except:
			raise SDOPackage.InvalidError("Configuration.remove_configuration_set()")

		return False


	def activate_configuration_set(self, config_id):
		"""
		\if jp

		\brief [CORBA interface] ConfigurationSet のアクティブ化

		ConfigurationProfile に格納された ConfigurationSet のうち一つを
		アクティブにする。
		このオペレーションは特定の ConfigurationSet をアクティブにする。
		すなわち、SDO のコンフィギュレーション・プロパティがその格納されている
		ConfigurationSet により設定されるプロパティの値に変更される。
		指定された ConfigurationSet の値がアクティブ・コンフィギュレーション
		にコピーされるということを意味する。

		\param config_id(string) アクティブ化する ConfigurationSet の id。
		\return オペレーションが成功したかどうか。
		\exception SDONotExists ターゲットのSDOが存在しない。
		\exception InvalidParameter 引数 "config_id" が null である、もしくは
			引数で指定された ConfigurationSet が存在しない。
		\exception NotAvailable SDOは存在するが応答がない。
		\exception InternalError 内部的エラーが発生した。
		\else

		\brief [CORBA interface] Activate ConfigurationSet

		This operation activates one of the stored ConfigurationSets in the
		ConfigurationProfile.
		This operation activates the specified stored ConfigurationSets.
		This means that the configuration properties of the SDO are changed as
		the values of these properties specified in the stored ConfigurationSet.
		In other words, values of the specified ConfigurationSet are now copied
		to the active configuration.

		\param config_id(string) Identifier of ConfigurationSet to be activated.
		\return If the operation was successfully completed.
		\exception SDONotExists The target SDO does not exist.
		\exception InvalidParameter if the argument ("configID") is null or
			there is no configuration set with identifier specified by
			the argument.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		if not config_id:
			raise SDOPackage.InvalidParameter("ID is empty.")
			
		try:
			return self._configsets.activateConfigurationSet(config_id)
		except:
			raise SDOPackage.InvalidError("Configuration.activate_configuration_set()")

		return False


    # end of CORBA interface definition
    #============================================================


	def getObjRef(self):
		return self._objref


	def getDeviceProfile(self):
		return self._deviceProfile


	def getServiceProfiles(self):
		return self._serviceProfiles


	def getServiceProfile(self, id):
		"""
		 \param id(string)
		"""
		index = OpenRTM.CORBA_SeqUtil.find(self._serviceProfiles,
										   self.service_id(id))

		if index < 0:
			return SDOPackage.ServiceProfile("","",[],None)

		return self._serviceProfiles[index]
	

	def getOrganizations(self):
		return self._organizations


	def getUUID(self):
		return OpenRTM.uuid1()
	


	class nv_name:
		"""
		\if jp
		\brief アクティブな ConfigurationSet
		\else
		\brief Active ConfigurationSet id
		\endif
		"""
		def __init__(self, name):
			self._name = name

		def __call__(self, nv):
			return self._name == nv.name
		

	# functor for ServiceProfile
	class service_id:
		def __init__(self, id_):
			self._id = str(id_)

		def __call__(self, s):
			id_ = str(s.id)
			return self._id == id_


	# functor for Organization
	class org_id:
		def __init__(self, id_):
			self._id = str(id_)

		def __call__(self, o):
			id_ = str(o.get_organization_id())
			return self._id == id_

    
	# functor for ConfigurationSet
	class config_id:
		def __init__(self, id_):
			self._id = str(id_)

		def __call__(self, c):
			id_ = str(c.id)
			return self._id == id_
