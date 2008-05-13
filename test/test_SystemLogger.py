#!/usr/bin/env python
# -*- Python -*-

# @file test_SystemLogger.py
# @brief test for RT component logger class
# @date $Date$
# @author Shinji Kurihara
#
# Copyright (C) 2003-2005
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.
#
# $Id$
#

#
# $Log$
#
#

import sys
sys.path.insert(1,"../")

import unittest

from SystemLogger import *
i = 0

class TestLogbuf(unittest.TestCase):
	def setUp(self):

		#import random
		#val = random.uniform(0,100)
		#self.filename = "log" + str(val) + ".log"
		global i
		i+=1
		self.filename = "log" + str(i) + ".log"
		self.logbuf = Logbuf(fileName=self.filename)
		self.logstr = LogStream(self.logbuf)

	def tearDown(self):
		#self.logbuf.__del__()
		del self.logstr
		pass

	def test_strToLogLevel(self):
		ERROR = 1
		WARN  = 2
		self.assertEqual(self.logstr.strToLogLevel(ERROR), ERROR)


	def test_RTC_LOG(self):
		import logging
		self.logstr.RTC_LOG(logging.ERROR,"log %s, %s",("hoge","hogehoge"))


	def test_RTC_ERROR(self):
		self.logstr.RTC_ERROR("error!!!!!")


	def test_RTC_WARN(self):
		self.logstr.RTC_WARN("warn!!!!!")


	def test_RTC_INFO(self):
		self.logstr.RTC_INFO("info!!!!!")


	def test_RTC_NORMAL(self):
		self.logstr.RTC_NORMAL("normal!!!!")


	def test_RTC_DEBUG(self):
		self.logstr.RTC_DEBUG("debug!!!!!")


	def test_RTC_TRACE(self):
		self.logstr.RTC_TRACE("trace!!!!")


if __name__ == "__main__":
	unittest.main()
