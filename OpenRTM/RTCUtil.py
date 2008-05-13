#!/usr/bin/env python
# -*- coding: euc-jp -*-


"""
  \file RTCUtil.py
  \brief RTComponent utils
  \date $Date: 2007/09/11 $
  \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
 
  Copyright (C) 2007
      Task-intelligence Research Group,
      Intelligent Systems Research Institute,
      National Institute of
          Advanced Industrial Science and Technology (AIST), Japan
      All rights reserved.
"""

from omniORB import CORBA

import RTC, RTC__POA

def isDataFlowParticipant(obj):
	"""
	 \param obj(CORBA.Object)
	 \return bool
	"""
	dfp = obj._narrow(RTC.DataFlowParticipant)
	return not CORBA.is_nil(dfp)

def isFsmParticipant(obj):
	"""
	 \param obj(CORBA.Object)
	 \return bool
	"""
	fsmp = obj._narrow(RTC.FsmParticipant)
	return not CORBA.is_nil(fsmp)

def isFsmObject(obj):
	"""
	 \param obj(CORBA.Object)
	 \return bool
	"""
	fsm = obj._narrow(RTC.FsmObject)
	return not CORBA.is_nil(fsm)

def isMultiModeObject(obj):
	"""
	 \param obj(CORBA.Object)
	 \return bool
	"""
	mmc = obj._narrow(RTC.MultiModeObject)
	return not CORBA.is_nil(mmc)
