#!/usr/bin/env python
# -*- Python -*-

#
# \file test_ModulesManager.py
# \brief Loadable modules manager class
# \date $Date: $
# \author Shinji Kurihara
#
# Copyright (C) 2006
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.
#

import sys
sys.path.insert(1,"../")

import unittest

import OpenRTM

from ModuleManager import *

configsample_spec = ["implementation_id", "ConfigSample",
					 "type_name",         "ConfigSample",
					 "description",       "Configuration example component",
					 "version",           "1.0",
					 "vendor",            "Shinji Kurihara, AIST",
					 "category",          "example",
					 "activity_type",     "DataFlowComponent",
					 "max_instance",      "10",
					 "language",          "C++",
					 "lang_type",         "compile",
					 # Configuration variables
					 "conf.default.int_param0", "0",
					 "conf.default.int_param1", "1",
					 "conf.default.double_param0", "0.11",
					 "conf.default.double_param1", "9.9",
					 "conf.default.str_param0", "hoge",
					 "conf.default.str_param1", "dara",
					 "conf.default.vector_param0", "0.0,1.0,2.0,3.0,4.0",
					 ""]

class TestModuleManager(unittest.TestCase):
	def setUp(self):
		self.mm = ModuleManager(OpenRTM.Properties(defaults_str=configsample_spec))

	def tearDown(self):
		del self.mm
		
    
	def test_load(self):
		try:
			self.mm.load("hoge","echo")
			# Failure Pattern
			#self.mm.load("sample")
		except:
			print "exception."
		

	def test_unload(self):
		self.mm.load("sample")
		self.mm.unload("sample")
    

	def test_unloadAll(self):
		self.mm.unloadAll()
		

	def test_setLoadpath(self):
		self.mm.setLoadpath(["/usr/lib/python/site-packages"])
	
	def test_getLoadPath(self):
		self.mm.setLoadpath(["/usr/lib/python/site-packages"])
		self.assertEqual(self.mm.getLoadPath()[0],"/usr/lib/python/site-packages")

    
	def test_addLoadpath(self):
		self.mm.setLoadpath(["/usr/lib/python/site-packages"])
		self.mm.addLoadpath(["/usr/local/lib/python/site-packages"])
		self.assertEqual(self.mm.getLoadPath()[0],"/usr/lib/python/site-packages")
		self.assertEqual(self.mm.getLoadPath()[1],"/usr/local/lib/python/site-packages")

	
	def test_getLoadedModules(self):
		self.mm.load("hoge","echo")
		self.assertEqual(self.mm.getLoadedModules()[0],"hoge")
    

	def test_allowAbsolutePath(self):
		self.mm.allowAbsolutePath()

    
	def test_disallowAbsolutePath(self):
		self.mm.disallowAbsolutePath()

    
	def test_allowModuleDownload(self):
		self.mm.allowModuleDownload()

    
	def test_disallowModuleDownload(self):
		self.mm.disallowModuleDownload()

    
	def test_findFile(self):
		self.assertEqual(self.mm.findFile("hoge",["."]),"hoge")
		# Failure pattern
		# self.assertEqual(self.mm.findFile("hoge.py",["."]),"hoge.py")

    
	def test_fileExist(self):
		self.assertEqual(self.mm.fileExist("hoge.py"),True)

    
	def test_getInitFuncName(self):
		self.mm.getInitFuncName("hoge.py")
    
    
############### test #################
if __name__ == '__main__':
        unittest.main()
