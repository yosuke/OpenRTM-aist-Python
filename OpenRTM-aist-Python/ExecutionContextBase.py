#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
 \file ExecutionContextBase.py
 \brief ExecutionContext base class
 \date $Date: 2007/08/31$
 \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara

 Copyright (C) 2007
     Task-intelligence Research Group,
     Intelligent Systems Research Institute,
     National Institute of
        Advanced Industrial Science and Technology (AIST), Japan
     All rights reserved.
"""


import RTC__POA
import OpenRTM

class ExecutionContextBase(RTC__POA.ExtTrigExecutionContextService):
	
	def __init__(self):
		pass
	
	def tick(self):
		pass
