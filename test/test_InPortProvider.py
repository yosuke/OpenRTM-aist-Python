#!/usr/bin/env python
# -*- Python -*-

#
#  \file  test_InPortProvider.py
#  \brief test for InPortProvider class
#  \date  $Date: 2007/09/20 $
#  \author Shinji Kurihara
# 
#  Copyright (C) 2006
#      Noriaki Ando
#      Task-intelligence Research Group,
#      Intelligent Systems Research Institute,
#      National Institute of
#          Advanced Industrial Science and Technology (AIST), Japan
#      All rights reserved.


import sys
sys.path.insert(1,"../")

import unittest

from InPortProvider import *


class TestInPortProvider(unittest.TestCase):
	def setUp(self):
		self._ipp = InPortProvider()

	def test_publishInterfaceProfile(self):
		self._ipp.setDataType("TimedLong")
		self._ipp.setInterfaceType("CORBA_Any")
		self._ipp.setDataFlowType("Push,Pull")
		self._ipp.setSubscriptionType("Flush,New,Periodic")
		self._ipp.publishInterfaceProfile([])

	def test_publishInterface(self):
		self._ipp.publishInterface([])


############### test #################
if __name__ == '__main__':
        unittest.main()
