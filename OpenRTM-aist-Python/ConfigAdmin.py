#!/usr/bin/env python
# -*- coding: euc-jp -*- 

##
#  @file ConfigAdmin.py
#  @brief Configuration Administration classes
#  @date $Date: 2007/09/04$
#  @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
# 
#  Copyright (C) 2007
#      Task-intelligence Research Group,
#      Intelligent Systems Research Institute,
#      National Institute of
#          Advanced Industrial Science and Technology (AIST), Japan
#      All rights reserved.


import copy
import OpenRTM


class ConfigBase:
	
	""" ConfigBase class """
	# ConfigBase(name:str, def_val:str)
	def __init__(self, name, def_val):
		self.name          = name
		self.default_value = def_val

	def update(self, val):
		pass
	
  
class Config(ConfigBase):
	
	""" Config template class """
	# Config(name:str, var:"configuration variable reference", def_val:str, trans:TransFuncObj)
	def __init__(self, name, var, def_val, trans=None):
		ConfigBase.__init__(self, name, def_val)
		self._var = var
		if trans != None:
			self._trans = trans
		else:
			self._trans = OpenRTM.stringTo

	# update(val:str)
	def update(self, val):
		if self._trans(self._var, val):
			return True
		self._trans(self._var, self._default_value)
		return False


class ConfigAdmin:
	
	""" ConfigAdmin class """
	# ConfigAdmin(configsets:OpenRTM.Properties)
	def __init__(self, configsets):
		self._configsets = configsets
		self._activeId   = "default"
		self._active     = True
		self._changed    = False
		self._params     = []
		self._emptyconf  = OpenRTM.Properties()
		self._newConfig  = []

	def __del__(self):
		del self._params

	##
	# @param param_name(string)  The name of parameter.
	# @param var(data object) binding data
	# @param def_val(string) default value. use string.  like "1.0"
	# @param trans(object) function pointer.
	# By the implementation of the C++,
	# bool (*trans)(VarType&, const char*)
	# @return True of False
	def bindParameter(self, param_name, var, def_val, trans=None):
		if trans == None:
			trans = OpenRTM.stringTo
		
		if self.isExist(param_name):
			return False

		if not OpenRTM.stringTo(var, def_val):
			return False
		
		self._params.append(Config(param_name, var, def_val, trans))
		return True


	##
	# @param config_set(string) Character string of Configuration set.
	# @param config_param(string) Character string of Configuration parameter.
	def update(self, config_set=None, config_param=None):
		# update(const char* config_set)
		if config_set != None and config_param == None:
			if self._configsets.hasKey(config_set) == None:
				return
			prop = self._configsets.getNode(config_set)
			for i in range(len(self._params)):
				if prop.hasKey(self._params[i].name) != None:
					self._params[i].update(prop.getProperty(self._params[i].name))

		# update(const char* config_set, const char* config_param)
		if config_set != None and config_param != None:
			key = config_set
			key = key+"."+config_param
			func = self.find_conf(config_param)
			for conf in self._params:
				if func(conf):
					conf.update(self._configsets.getProperty(key))
					return

		# update()
		if config_set == None and config_param == None:
			if self._changed and self._active:
				self.update(self._activeId)
				self._changed = False
			return


	##
	# @param param_name(string) The name of parameter.
	# 
	# @return True of False
	def isExist(self, param_name):
		if not self._params:
			return False
		
		func = self.find_conf(param_name)
		for conf in self._params:
			if func(conf):
				return True

		return False


	def isChanged(self):
		return self._changed


	def getActiveId(self):
		return self._activeId


	##
	# @param config_id(string) The id of configuration.
	# @return True of False
	def haveConfig(self, config_id):
		if self._configsets.hasKey(config_id) == None:
			return False
		else:
			return True


	##
	# @return True of False
	def isActive(self):
		return self._active


	##
	# @return list of Properties objects.
	def getConfigurationSets(self):
		return self._configsets.getLeaf()


	##
	# @param config_id(string) The id of configuration.
	# @return prop Properties object.
	def getConfigurationSet(self, config_id):
		prop = self._configsets.getNode(config_id)
		if prop == None:
			return self._emptyconf
		return prop


	##
	# @param config_id(string) The id of configuration.
	# @param config_set(Properties&) configuration sets.
	# @return True of False
	def setConfigurationSetValues(self, config_id, config_set):
		if config_set.getName() != config_id:
			return False
		if not self._configsets.hasKey(config_id):
			return False

		p = self._configsets.getNode(config_id)
		if p == None:
			return False
		p.mergeProperties(config_set)

		self._changed = True
		self._active  = False
		return True


	##
	# @return p Properties object.
	def getActiveConfigurationSet(self):
		p = self._configsets.getNode(self._activeId)
		if p == None:
			return self._emptyconf

		return p


	##
	# @param configset(OpenRTM.Properties&) Properties object.
	# @return True of False
	def addConfigurationSet(self, configset):
		if self._configsets.hasKey(configset.getName()):
			return False
		node = configset.getName()

		# Create node
		self._configsets.createNode(node)

		p = self._configsets.getNode(node)
		p.mergeProperties(configset)
		self._newConfig.append(node)

		self._changed = True
		self._active  = False

		return True


	##
	# @param config_id(string) The id of Configuration.
	# @return True of False
	def removeConfigurationSet(self, config_id):
		idx = 0
		for conf in self._newConfig:
			if conf == config_id:
				break
			idx += 1

		if idx == len(self._newConfig):
			return False

		p = self._configsets.getNode(config_id)
		if p:
			p.getRoot().removeNode(config_id)
			del p

		del self._newConfig[idx]

		self._changed = True
		self._active  = False

		return True


	##
	# @param config_id(string) The id of Configuration.
	# @return True or False
	def activateConfigurationSet(self, config_id):
		if not config_id:
			return False
		if not self._configsets.hasKey(config_id):
			return False
		self._activeId = config_id
		self._active   = True
		self._changed  = True
		return True



	class find_conf:
		
		def __init__(self, name):
			self._name = name

		def __call__(self, conf):
			return self._name == conf.name
    
