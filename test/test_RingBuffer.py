#!/usr/bin/env python
# -*- Python -*-

# \file test_RingBuffer.py
# \brief test for Defautl Buffer class
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

from RingBuffer import *


class TestRingBuffer(unittest.TestCase):

	def setUp(self):
		self._rb = RingBuffer(5)


	def test_init(self):
		self._rb.init(123)
		data=[0]
		self._rb.read(data)
		self.assertEqual(data[0],123)


	def test_clear(self):
		self._rb.clear()
		data=[0]
		self.assertEqual(self._rb.read(data),False)


	def test_length(self):
		self.assertEqual(self._rb.length(), 5)


	def test_write(self):
		data=[0]

		self.assertEqual(self._rb.write(1),True)
		self._rb.read(data)
		self.assertEqual(data[0],1)

		self.assertEqual(self._rb.write(2),True)
		self._rb.read(data)
		self.assertEqual(data[0],2)

		self.assertEqual(self._rb.write(3),True)
		self._rb.read(data)
		self.assertEqual(data[0],3)

		self.assertEqual(self._rb.write(4),True)
		self._rb.read(data)
		self.assertEqual(data[0],4)

		self.assertEqual(self._rb.write(5),True)
		self._rb.read(data)
		self.assertEqual(data[0],5)

		self.assertEqual(self._rb.write(6),True)
		self._rb.read(data)
		self.assertEqual(data[0],6)

		self.assertEqual(self._rb.write("string"),True)
		self._rb.read(data)
		self.assertEqual(data[0],"string")

		self.assertEqual(self._rb.write([1,2,3]),True)
		self._rb.read(data)
		self.assertEqual(data[0],[1,2,3])

		self.assertEqual(self._rb.write(0.12345),True)
		self._rb.read(data)
		self.assertEqual(data[0],0.12345)


	def test_read(self):
		data=[0]
		self.assertEqual(self._rb.read(data),False)

		self.assertEqual(self._rb.write("string"),True)
		# Failure pattern (parameter must be List object.)
		# data=0
		# self._rb.read(data)


	def test_isFull(self):
		self.assertEqual(self._rb.isFull(),False)


	def test_isEmpty(self):
		self.assertEqual(self._rb.isEmpty(),True)
		self._rb.init(0)
		self.assertEqual(self._rb.isEmpty(),False)


	def test_isNew(self):
		self.assertEqual(self._rb.isNew(),False)
		self._rb.init(0)
		self.assertEqual(self._rb.isNew(),True)
		data=[0]
		self._rb.read(data)
		self.assertEqual(self._rb.isNew(),False)

		self.assertEqual(self._rb.write(0.12345),True)
		self.assertEqual(self._rb.write(0.12345),True)
		self.assertEqual(self._rb.write(0.12345),True)
		self.assertEqual(self._rb.isNew(),True)
		self.assertEqual(self._rb.isNew(),True)
		self.assertEqual(self._rb.isNew(),True)


############### test #################
if __name__ == '__main__':
        unittest.main()
