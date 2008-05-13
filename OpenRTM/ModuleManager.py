#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
 \file ModulesManager.py
 \brief Loadable modules manager class
 \date $Date: 2007/08/24$
 \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara

 Copyright (C) 2006
     Task-intelligence Research Group,
     Intelligent Systems Research Institute,
     National Institute of
         Advanced Industrial Science and Technology (AIST), Japan
     All rights reserved.
"""


import string
import os

import OpenRTM


CONFIG_EXT    = "manager.modules.config_ext"
CONFIG_PATH   = "manager.modules.config_path"
DETECT_MOD    = "manager.modules.detect_loadable"
MOD_LOADPTH   = "manager.modules.load_path"
INITFUNC_SFX  = "manager.modules.init_func_suffix"
INITFUNC_PFX  = "manager.modules.init_func_prefix"
ALLOW_ABSPATH = "manager.modules.abs_path_allowed"
ALLOW_URL     = "manager.modules.download_allowed"
MOD_DWNDIR    = "manager.modules.download_dir"
MOD_DELMOD    = "manager.modules.download_cleanup"
MOD_PRELOAD   = "manager.modules.preload"



class ModuleManager:
	"""
	\if jp
	\brief モジュールマネージャクラス
	\else
	\biref ModuleManager class
	\endif
	"""


	def __init__(self, prop):
		"""
		 \brief クラスコンストラクタ
		 \param prop(OpenRTM.Properties)
		"""
		self._properties = prop

		self._configPath = prop.getProperty(CONFIG_PATH).split(",")
		for i in range(len(self._configPath)):
			tmp = [self._configPath[i]]
			OpenRTM.eraseHeadBlank(tmp)
			self._configPath[i] = tmp[0]

		self._loadPath = prop.getProperty(MOD_LOADPTH).split(",")
		for i in range(len(self._loadPath)):
			tmp = [self._loadPath[i]]
			OpenRTM.eraseHeadBlank(tmp)
			self._loadPath[i] = tmp[0]

		self._absoluteAllowed = OpenRTM.toBool(prop.getProperty(ALLOW_ABSPATH),
											   "yes", "no", False)

		self._downloadAllowed = OpenRTM.toBool(prop.getProperty(ALLOW_URL),
											   "yes", "no", False)

		self._initFuncSuffix = prop.getProperty(INITFUNC_SFX)
		self._initFuncPrefix = prop.getProperty(INITFUNC_PFX)
		self._modules = {}

	def __del__(self):
		#self.unloadAll()
		pass
		
		
    
	class Error:
		def __init__(self, reason_):
			self.reason = reason_
    

	class NotFound:
		def __init__(self, name_):
			self.name = name_
    

	class FileNotFound(NotFound):
		def __init__(self, name_):
			ModuleManager.NotFound.__init__(self, name_)

    
	class ModuleNotFound(NotFound):
		def __init__(self, name_):
			ModuleManager.NotFound.__init__(self, name_)

    
	class SymbolNotFound(NotFound):
		def __init__(self, name_):
			ModuleManager.NotFound.__init__(self, name_)

    
	class NotAllowedOperation(Error):
		def __init__(self, reason_):
			ModuleManager.Error.__init__(self, reason_)
			ModuleManager.Error.__init__(self, reason_)

    
	class InvalidArguments(Error):
		def __init__(self, reason_):
			ModuleManager.Error.__init__(self, reason_)

    
	class InvalidOperation(Error):
		def __init__(self, reason_):
			ModuleManager.Error.__init__(self, reason_)


	def load(self, file_name, init_func=None):
		"""
		\if jp
		\brief モジュールのロード
		
		   file_name をDLL もしくは共有ライブラリとしてロードする。
		   file_name は既定のロードパス (manager.modules.load_path) に対する
		   相対パスで指定する。
		   
		   Property manager.modules.abs_path_allowed が yes の場合、
		   ロードするモジュールを絶対パスで指定することができる。
		   Property manager.modules.download_allowed が yes の場合、
		   ロードするモジュールをURLで指定することができる。
		   
		   file_name は絶対パスで指定することができる。
		   manager.modules.allowAbsolutePath が no の場合、
		   既定のモジュールロードパスから、file_name のモジュールを探しロードする。
		\param file_name(string)
		\param init_func(string)
		\else
		\brief Load module
		\param file_name(string)
		\param init_func(string)
		\endif
		"""
		if file_name == "":
			raise ModuleManager.InvalidArguments, "Invalid file name."

		if OpenRTM.isURL(file_name):
			if not self._downloadAllowed:
				raise ModuleManager.NotAllowedOperation, "Downloading module is not allowed."
			else:
				raise ModuleManager.NotFound, "Not implemented."

		if OpenRTM.isAbsolutePath(file_name):
			if not self._absoluteAllowed:
				raise ModuleManager.NotAllowedOperation, "Absolute path is not allowed"
			else:
				file_path = file_name
			
		else:
			file_path = self.findFile(file_name, self._loadPath)

		if file_path == "":
			raise ModuleManager.InvalidArguments, "Invalid file name."

		if not self.fileExist(file_path+".py"):
			raise ModuleManager.FileNotFound, file_path

		mo = __import__(str(file_path))
		self._modules[file_name] = self.DLL(mo)

		if init_func == None:
			return file_path

		if file_path == "":
			raise ModuleManager.InvalidOperation, "Invalid file name"

		try:
			self._modules[file_name].dll.__getattribute__(init_func)()
		except:
			print "Could't call init_func: ", init_func


	def unload(self, file_name):
		"""
		\if jp
		\brief モジュールのアンロード
		\param file_name(string)
		\else
		\brief Unload module
		\param file_name(string)
		\endif
		"""
		if not self._modules.has_key(file_name):
			raise ModuleManager.NotFound, file_name

		# self._modules[file_name].dll.close()
		del self._modules[file_name]


	def unloadAll(self):
		"""
		\if jp
		\brief 全モジュールのアンロード
		\else
		\brief Unload all modules
		\endif
		"""
		keys   = self._modules.keys()
		
		self._modules.clear()


	def symbol(self, file_name, func_name):
		"""
		\if jp
		\brief モジュールのシンボルの参照
		\param file_name(string)
		\param func_name(string)
		\else
		\brief Look up a named symbol in the module
		\param file_name(string)
		\param func_name(string)
		\endif
		"""
		if not self._modules.has_key(file_name):
			raise ModuleManager.ModuleNotFound, file_name

		func = self._modules[file_name].dll.symbol(func_name)

		if not func:
			raise ModuleManager.SymbolNotFound, func_name

		return func


	def setLoadpath(self, load_path_list):
		"""
		\if jp
		\brief モジュールロードパスを指定する
		\param load_path_list(list of string)
		\else
		\brief Set default module load path
		\param load_path_list(list of string)
		\endif
		"""
		self._loadPath = load_path_list
		return

	
	def getLoadPath(self):
		return self._loadPath


	def addLoadpath(self, load_path):
		"""
		\if jp
		\brief モジュールロードパスを追加する
		\param load_path(list of string)
		\else
		\brief Add module load path
		\param load_path(list of string)
		\endif
		"""
		for path in load_path:
			self._loadPath.append(path)
		return


	def getLoadedModules(self):
		"""         
		\if jp
		\brief ロード済みのモジュールリストを取得する
		\else
		\brief Get loaded module names
		\endif
		"""       
		modules = []
		keys = self._modules.keys()
		for mod_name in keys:
			modules.append(mod_name)

		return modules


	def getLoadableModules(self):
		"""              
		\if jp
		\brief ロード可能なモジュールリストを取得する
		\else
		\brief Get loadable module names
		\endif
		"""
		return []


	def allowAbsolutePath(self):
		"""     
		\if jp
		\brief モジュールの絶対パス指定許す
		\else
		\brief Allow absolute load path
		\endif
		"""
		self._absoluteAllowed = True


	def disallowAbsolutePath(self):
		"""     
		\if jp
		\brief モジュールの絶対パス指定禁止する
		\else
		\brief Forbid absolute load path
		\endif
		"""
		self._absoluteAllowed = False


	def allowModuleDownload(self):
		"""     
		\if jp
		\brief モジュールのダウンロードを許す
		\else
		\brief Allow module download
		\endif
		"""
		self._downloadAllowed = True


	def disallowModuleDownload(self):
		"""     
		\if jp
		\brief モジュールのダウンロードを禁止する
		\else
		\brief Forbid module download
		\endif
		"""
		self._downloadAllowed = False


	def findFile(self, fname, load_path):
		"""     
		\if jp
		\brief LoadPath からのファイルの検索
		\param fname(string)
		\param load_path(list of string)
		\else
		\brief Search file from load path
		\param fname(string)
		\param load_path(list of string)
		\endif
		"""
		file_name = fname

		if len(load_path) == 1:
			load_path.append(".")
		for path in load_path:
			f = str(path)+"/"+str(file_name)+".py"
			if self.fileExist(f):
				return fname
		return ""


	def fileExist(self, filename):
		"""     
		\if jp
		\brief ファイルが存在するかどうかのチェック
		\param filename(string)
		\else
		\brief Check file existance
		\param filename(string)
		\endif
		"""
		try:
			infile = open(filename)
		except:
			return False

		infile.close()
		return True


	def getInitFuncName(self, file_path):
		"""     
		\if jp
		\brief 初期化関数シンボルを生成する
		\param file_path(string)
		\else
		\brief Create initialize function symbol
		\param file_path(string)
		\endif
		"""
		base_name = os.path.basename(file_path)
		return str(self._initFuncPrefix)+str(base_name)+str(self._initFuncSuffix)
    
    
	class DLL:
		def __init__(self, dll):
			self.dll = dll
