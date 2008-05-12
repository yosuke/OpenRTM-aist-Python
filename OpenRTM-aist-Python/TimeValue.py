#!/usr/bin/env python
# -#- coding: euc-jp -#-


"""
 \file TimeValue.py
 \brief TimeValue class
 \date $Date: 2007/08/23$
 \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara

 Copyright (C) 2007
     Task-intelligence Research Group,
     Intelligent Systems Research Institute,
     National Institute of
         Advanced Industrial Science and Technology (AIST), Japan
     All rights reserved.
"""


import OpenRTM

class TimeValue:
	def __init__(self, sec=None, usec=None):
		"""
		 \param sec(long)
		 \param usec(long)
		"""
		if sec == None:
			self.tv_sec = 0
		else:
			self.tv_sec = float(sec)

		if usec == None:
			self.tv_usec = 0
		else:
			self.tv_usec = float(usec)

	def __sub__(self, tm):
		try:
			res = TimeValue()
		except:
			res = OpenRTM.TimeValue()
		
		if self.tv_sec >= tm.tv_sec:
			if self.tv_usec >= tm.tv_usec:
				res.tv_sec  = self.tv_sec  - tm.tv_sec
				res.tv_usec = self.tv_usec - tm.tv_usec
			else:
				res.tv_sec  = self.tv_sec  - tm.tv_sec - 1
				res.tv_usec = (self.tv_usec + 1000000) - tm.tv_usec
		else:
			if tm.tv_usec >= self.tv_usec:
				res.tv_sec  = -(tm.tv_sec  - self.tv_sec)
				res.tv_usec = -(tm.tv_usec - self.tv_usec)
			else:
				res.tv_sec  = -(tm.tv_sec - self.tv_sec - 1)
				res.tv_usec = -(tm.tv_usec + 1000000) + self.tv_usec
		return res

	def __add__(self, tm):
		res = TimeValue()
		res.tv_sec  = self.tv_sec  + tm.tv_sec
		res.tv_usec = self.tv_usec + tm.tv_usec
		if res.tv_usec > 1000000:
			res.tv_sec += 1
			res.tv_usec -= 1000000
		return res

	# operator=(double time) の実装
	def set_time(self, time):
		self.tv_sec  = long(time)
		self.tv_usec = long((time - float(self.tv_sec))*1000000)
		return self

	def toDouble(self):
		return float(self.tv_sec) + float(self.tv_usec/1000000.0)


	def __str__(self):
		return str(self.tv_sec + self.tv_usec/1000000.0)

