#!/usr/bin/env python
# -*- Python -*-

#
# \file test_ExtTrigExecutionContext.py
# \brief ExtTrigExecutionContext class
# \date $Date: 2007/09/06$
# \author Shinji Kurihara
#
# Copyright (C) 2007
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

from ExtTrigExecutionContext import *

import CORBA
from omniORB import CORBA, PortableServer

class DFP(OpenRTM.RTObject_impl):
	def __init__(self):
		self._orb = CORBA.ORB_init()
		self._poa = self._orb.resolve_initial_references("RootPOA")
		OpenRTM.RTObject_impl.__init__(self, orb=self._orb, poa=self._poa)
		self._error = False
		self._ref = self._this()
		self._eclist = []


class TestExtTrigExecutionContext(unittest.TestCase):
	def setUp(self):
		self._dfp = DFP()
		self._dfp._poa._get_the_POAManager().activate()
		self.etec = ExtTrigExecutionContext()
		#self.etec = ExtTrigExecutionContext(self._dfp._ref)

	def test_tick(self):
		pass

	def test_run(self):
		self.etec.start()
		import time
		time.sleep(3)
		self.etec.tick()
		time.sleep(3)

############### test #################
if __name__ == '__main__':
        unittest.main()
