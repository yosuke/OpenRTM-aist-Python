#!/usr/bin/env python
# -*- Python -*-

#
# \file test_Manager.py
# \brief test for RTComponent manager class
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

#from Manager import *
import OpenRTM
import RTC, RTC__POA

configsample_spec = ["implementation_id", "TestComp",
					 "type_name",         "TestComp",
					 "description",       "Test example component",
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

com = None

class TestComp(OpenRTM.DataFlowComponentBase):
	def __init_(self, manager):
		OpenRTM.DataFlowComponentBase.__init__(self, manager)

		
def TestCompInit(manager):
	global com
	profile = OpenRTM.Properties(defaults_str=configsample_spec)
	manager.registerFactory(profile,
							TestComp,
							OpenRTM.Delete)
	com = manager.createComponent("TestComp")

def TestEcInit(manager):
	profile = OpenRTM.Properties(defaults_str=configsample_spec)
	print manager.registerECFactory("Art",
									TestComp,
									OpenRTM.Delete)
	manager.createComponent("TestEc")


class TestManager(unittest.TestCase):

	def setUp(self):
		self.manager = OpenRTM.Manager.init(sys.argv)

	"""
	def test_instance(self):
		self.assertEqual(self.manager.instance(), self.manager)

	def test_terminate(self):
		self.manager.terminate()

	def test_shutdown(self):
		self.manager.runManager(True)
		import time
		time.sleep(0.1)
		self.manager.shutdown()
		#self.manager.runManager()
	"""

	def test_createComponent(self):
		global com
		self.manager.setModuleInitProc(TestCompInit)
		self.manager.activateManager()
		print self.manager.getComponent("TestComp0")
		print self.manager.getComponents()
		self.manager.cleanupComponent(com)


	def test_load(self):
		self.manager.load("hoge", "echo")
		self.manager.unload("hoge")
		self.manager.unloadAll()
		self.manager.load("hoge", "echo")
		self.assertEqual(len(self.manager.getLoadedModules()), 1)
		self.assertEqual(len(self.manager.getLoadableModules()), 0)


	def test_registerECFactory(self):
		self.manager.setModuleInitProc(TestCompInit)
		self.manager.activateManager()


	def test_getModulesFactories(self):
		self.manager.getModulesFactories()

	def test_getORB(self):
		self.manager.getORB()
		
	def test_getPOA(self):
		self.manager.getPOA()


	def test_initNaming(self):
		self.manager.initNaming()


############### test #################
if __name__ == '__main__':
        unittest.main()
