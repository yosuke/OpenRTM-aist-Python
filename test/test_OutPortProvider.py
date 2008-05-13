#!/usr/bin/env python
# -*- Python -*-

#
# \file  test_OutPortProvider.py
# \brief test for OutPortProvider class
# \date  $Date: 2007/09/05$
# \author Shinji Kurihara
#
# Copyright (C) 2006
#     Noriaki Ando
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

from OutPortProvider import *


class TestOutPortProvider(unittest.TestCase):
	def setUp(self):
		self._opp = OutPortProvider()
		self._opp.setPortType("data")
		self._opp.setDataType("int")
		self._opp.setInterfaceType("Service")
		self._opp.setDataFlowType("flow")
		self._opp.setSubscriptionType("new")

	def test_publishInterface(self):
		pass
	
############### test #################
if __name__ == '__main__':
        unittest.main()
