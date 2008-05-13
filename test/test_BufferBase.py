#!/usr/bin/env python
# -*- Python -*-

# \file test_BufferBase.py
# \brief Buffer abstract class
# \date $Date: 2007/09/12 $
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

from BufferBase import *

class TestNullBuffer(unittest.TestCase):
	def setUp(self):
		self.nb = NullBuffer()
		self.nb.init(100)


	def test_clear(self):
		self.nb.clear()
		self.assertEqual(self.nb.read([]), False)


	def test_length(self):
		self.assertEqual(self.nb.length(),1)


	def test_write(self):
		data=[0]
		# test long
		self.assertEqual(self.nb.write(10000), True)
		self.nb.read(data)
		self.assertEqual(data[0], 10000)

		# test float
		self.assertEqual(self.nb.write(1.2345), True)
		self.nb.read(data)
		self.assertEqual(data[0], 1.2345)

		# test string
		self.assertEqual(self.nb.write("test"), True)
		self.nb.read(data)
		self.assertEqual(data[0], "test")
		
		# test list
		self.assertEqual(self.nb.write([1,2,3]), True)
		self.nb.read(data)
		self.assertEqual(data[0], [1,2,3])


	def test_isEmpty(self):
		self.assertEqual(self.nb.isEmpty(),False)
		self.nb.clear()
		self.assertEqual(self.nb.isEmpty(),True)


	def test_isNew(self):
		data=[0]
		self.assertEqual(self.nb.isNew(),True)
		self.nb.read(data)
		self.assertEqual(self.nb.isNew(),False)
		self.assertEqual(self.nb.write(10000), True)
		self.assertEqual(self.nb.isNew(),True)


############### test #################
if __name__ == '__main__':
        unittest.main()
