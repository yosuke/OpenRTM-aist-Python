#!/usr/bin/env python
# -*- Python -*-

#
#  \file  test_PublisherNew.py
#  \brief test for PublisherNew class
#  \date  $Date: 2007/09/27 $
#  \author Shinji Kurihara
# 
#  Copyright (C) 2006
#      Noriaki Ando
#      Task-intelligence Research Group,
#      Intelligent Systems Research Institute,
#      National Institute of
#          Advanced Industrial Science and Technology (AIST), Japan
#      All rights reserved.
 
import OpenRTM

import sys
sys.path.insert(1,"../")

import unittest

from PublisherNew import *

class Consumer:
	def push(self):
		print "push"

class TestPublisherNew(unittest.TestCase):

	def setUp(self):
		self._pn = PublisherNew(Consumer(),None)

	def test_update(self):
		self._pn.update()
		self._pn.release()


############### test #################
if __name__ == '__main__':
        unittest.main()
