#!/usr/bin/env python
# -*- Python -*-

#
#  \file  test_OutPortCorbaCdrProvider.py
#  \brief test for OutPortCorbaCdrProvider class
#  \date  $Date: 2007/09/26 $
#  \author Shinji Kurihara
# 
#  Copyright (C) 2006
#      Noriaki Ando
#      Task-intelligence Research Group,
#      Intelligent Systems Research Institute,
#      National Institute of
#          Advanced Industrial Science and Technology (AIST), Japan
#      All rights reserved.
 
from omniORB import any
from omniORB import CORBA

import OpenRTM_aist
import RTC, RTC__POA 
import SDOPackage, SDOPackage__POA

import sys
sys.path.insert(1,"../")

import unittest

from OutPortCorbaCdrProvider import *

class DummyBuffer:
	def empty(self):
		return False

	def read(self,cdr):
		cdr[0] = 123
		return 0

class TestOutPortCorbaCdrProvider(unittest.TestCase):

	def setUp(self):
		OpenRTM_aist.Manager.instance()
		OpenRTM_aist.OutPortCorbaCdrProviderInit()
		self._opp = OpenRTM_aist.OutPortCorbaCdrProvider()
		return
    
	def test_setBuffer(self):
		self._opp.setBuffer(DummyBuffer())
		return

	def test_get(self):
		self._opp.setBuffer(DummyBuffer())
		ret,data=self._opp.get()
		self.assertEqual(ret,OpenRTM.PORT_OK)
		self.assertEqual(data,123)
		return


############### test #################
if __name__ == '__main__':
        unittest.main()
