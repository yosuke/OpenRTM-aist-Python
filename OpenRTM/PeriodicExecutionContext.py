#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
 \file PeriodicExecutionContext.py
 \brief PeriodicExecutionContext class
 \date $Date: 2007/08/29$
 \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara

 Copyright (C) 2006
     Task-intelligence Research Group,
     Intelligent Systems Research Institute,
     National Institute of
         Advanced Industrial Science and Technology (AIST), Japan
     All rights reserved.
"""


import copy
import threading
import time
from omniORB import CORBA, PortableServer

import OpenRTM
import RTC, RTC__POA

class PeriodicExecutionContext(OpenRTM.ExecutionContextBase):

	class DFP:
		def __init__(self, obj, id_):
			"""
			 \param obj(Object)
			 \param id_(long)
			"""
			self._obj = obj
			self._active = True
			self.ec_id = id_
			self._sm = OpenRTM.StateMachine(3)
			self._sm.setListener(self)
			self._sm.setEntryAction (RTC.ACTIVE_STATE,
									 self.on_activated)
			self._sm.setDoAction    (RTC.ACTIVE_STATE,
									 self.on_execute)
			self._sm.setPostDoAction(RTC.ACTIVE_STATE,
									 self.on_state_update)
			self._sm.setExitAction  (RTC.ACTIVE_STATE,
									 self.on_deactivated)
			self._sm.setEntryAction (RTC.ERROR_STATE,
									 self.on_aborting)
			self._sm.setDoAction    (RTC.ERROR_STATE,
									 self.on_error)
			self._sm.setExitAction  (RTC.ERROR_STATE,
									 self.on_reset)
			st = OpenRTM.StateHolder()
			st.prev = RTC.INACTIVE_STATE
			st.curr = RTC.INACTIVE_STATE
			st.next = RTC.INACTIVE_STATE
			self._sm.setStartState(st)
			self._sm.goTo(RTC.INACTIVE_STATE)


		def __del__(self):
			pass

		def on_startup(self):
			return self._obj.on_startup(self.ec_id)

		def on_shutdown(self):
			return self._obj.on_shutdown(self.ec_id)

		def on_activated(self, st):
			"""
			 \param st(list of OpenRTM.StateMachine.Stateholder)
			"""
			if self._obj.on_activated(self.ec_id) != RTC.RTC_OK:
				self._sm.goTo(RTC.ERROR_STATE)
				return
			return

		def on_deactivated(self, st):
			"""
			 \param st(list of OpenRTM.StateMachine.Stateholder)
			"""
			self._obj.on_deactivated(self.ec_id)

		def on_aborting(self, st):
			"""
			 \param st(list of OpenRTM.StateMachine.Stateholder)
			"""
			self._obj.on_aborting(self.ec_id)

		def on_error(self, st):
			"""
			 \param st(list of OpenRTM.StateMachine.Stateholder)
			"""
			self._obj.on_error(self.ec_id)

		def on_reset(self, st):
			"""
			 \param st(list of OpenRTM.StateMachine.Stateholder)
			"""
			if self._obj.on_reset(self.ec_id) != RTC.RTC_OK:
				self._sm.goTo(RTC.ERROR_STATE)
				return
			return

		def on_execute(self, st):
			"""
			 \param st(list of OpenRTM.StateMachine.Stateholder)
			"""
			if self._obj.on_execute(self.ec_id) != RTC.RTC_OK:
				self._sm.goTo(RTC.ERROR_STATE)
				return
			return

		def on_state_update(self, st):
			"""
			 \param st(list of OpenRTM.StateMachine.Stateholder)
			"""
			if self._obj.on_state_update(self.ec_id) != RTC.RTC_OK:
				self._sm.goTo(RTC.ERROR_STATE)
				return
			return

		def on_rate_changed(self):
			self._obj.on_rate_changed(self.ec_id)

		def worker(self):
			return self._sm.worker()

		def get_state(self):
			return self._sm.getState()



	def __init__(self, owner=None, rate=None):
		"""
		 \param owner(RTC.DataFlowComponent)
		 \param rate(float)
		"""
		self._nowait = False
		self._running = False

		if rate == None:
			self._rate = 1000.0
			rate_ = 0.0
			self._usec = long(0)
		else:
			self._rate = rate
			rate_ = rate
			if rate == 0:
				rate_ = 0.0000001
			self._usec = long(1000000/rate_)
			if self._usec == 0:
				self._nowait = True
		self._comps = []
		self._profile = RTC.ExecutionContextProfile(RTC.PERIODIC, rate_, None, [], [])
		self._ref = self._this()
		self._thread = threading.Thread(target=self.run)

	def __del__(self):
		pass
    
	def getRef(self):
		return self._ref


	def run(self):
		"""
		\if jp
		\brief コンポーネントのアクティビティスレッド関数

		コンポーネントの内部アクティビティスレッドの実行関数。
		これは ACE_Task サービスクラスメソッドのオーバーライド。

		\else

		\brief Create internal activity thread

		Run by a daemon thread to handle deferred processing.
		ACE_Task class method override.

		\endif
		"""
		flag = True

		worker = self.invoke_worker()

		while flag:
			sec_ = float(self._usec)/1000000.0
			for comp in self._comps:
				worker(comp)

			#while not self._running:
				#time.sleep(sec_)
			if not self._nowait:
				time.sleep(sec_)

			flag = self._running

		return 0


	def close(self, flags):
		"""
		\if jp
		\brief コンポーネントのアクティビティスレッド終了関数
		   コンポーネントの内部アクティビティスレッド終了時に呼ばれる。
		   コンポーネントオブジェクトの非アクティブ化、マネージャへの通知を行う。
		   これは ACE_Task サービスクラスメソッドのオーバーライド。
		\param flags(long)
		\else
		\brief Close activity thread
		   close() method is called when activity thread svc() is returned.
		   This method deactivate this object and notify it to manager.
		   ACE_Task class method override.
		\endif
		"""
		return 0


	def is_running(self):
		"""
		\if jp
		\brief ExecutionContext が実行中かどうかのテスト
		\else
		\brief Test for ExecutionContext running state
		\endif
		"""
		return self._running


	def start(self):
		"""
		\if jp
		\brief ExecutionContext をスタートさせる
		\else
		\brief Start the ExecutionContext
		\endif
		"""
		if self._running:
			return RTC.PRECONDITION_NOT_MET

		startup = self.invoke_on_startup()
		for comp in self._comps:
			startup(comp)

		self._running = True
		self._thread.start()

		return RTC.RTC_OK


	def stop(self):
		"""
		\if jp
		\brief ExecutionContext をストップさせる
		\else
		\brief Stop the ExecutionContext
		\endif
		"""
		if not self._running:
			return RTC.PRECONDITION_NOT_MET

		shutdown = self.invoke_on_shutdown()
		for comp in self._comps:
			shutdown(comp)

		self._running = False

		return RTC.RTC_OK

	def get_rate(self):
		"""
		\if jp
		\brief 実行周期(Hz)を取得する
		\else
		\brief Get executionrate(Hz)
		\endif
		"""
		return self._profile.rate


	def set_rate(self, rate):
		"""
		\if jp
		\brief 実行周期(Hz)を与える 
		\param rate(float)
		\else
		\brief Set rate (Hz)
		\param rate(float)
		\endif
		"""
		if rate > 0.0:
			self._profile.rate = rate
			self._usec = long(1000000/rate)
			rate_changed = self.invoke_on_rate_changed()
			for comp in self._comps:
				rate_changed(comp)
			return RTC.RTC_OK
		return RTC.BAD_PARAMETER


	def activate_component(self, comp):
		"""
		\if jp
		\brief コンポーネントをアクティブ化する
		\param comp(RTC.LightweightRTObject)
		\else
		\brief Activate a component
		\param comp(RTC.LightweightRTObject)
		\endif
		"""
		predi = self.find_comp(comp)

		for comp in self._comps:
			if predi(comp):
				if not comp._sm._sm.isIn(RTC.INACTIVE_STATE):
					return RTC.PRECONDITION_NOT_MET
				comp._sm._sm.goTo(RTC.ACTIVE_STATE)
				return RTC.RTC_OK

		return RTC.BAD_PARAMETER


	def deactivate_component(self, comp):
		"""
		\if jp
		\brief コンポーネントを非アクティブ化する
		\param comp(RTC.LightweightRTObject)
		\else
		\brief Deactivate a component
		\param comp(RTC.LightweightRTObject)
		\endif
		"""
		predi = self.find_comp(comp)

		for comp in self._comps:
			if predi(comp):
				if not comp._sm._sm.isIn(RTC.ACTIVE_STATE):
					return RTC.PRECONDITION_NOT_MET
				comp._sm._sm.goTo(RTC.INACTIVE_STATE)
				return RTC.RTC_OK

		return RTC.BAD_PARAMETER


	def reset_component(self, comp):
		"""
		\if jp
		\brief コンポーネントをリセットする。
		\param comp(RTC.LightweightRTObject)
		\else
		\brief reset a component
		\param comp(RTC.LightweightRTObject)
		\endif
		"""
		predi = self.find_comp(comp)

		for comp in self._comps:
			if predi(comp):
				if not comp._sm._sm.isIn(RTC.ERROR_STATE):
					return RTC.PRECONDITION_NOT_MET
				comp._sm._sm.goTo(RTC.INACTIVE_STATE)
				return RTC.RTC_OK

		return RTC.BAD_PARAMETER


	def get_component_state(self, comp):
		"""
		\if jp
		\brief コンポーネントの状態を取得する
		\param comp(RTC.LightweightRTObject)
		\else
		\brief Get component's state
		\param comp(RTC.LightweightRTObject)
		\endif
		"""
		predi = self.find_comp(comp)
		for comp in self._comps:
			if predi(comp):
				return comp._sm._sm.getState()

		return RTC.UNKNOWN_STATE


	def get_kind(self):
		"""
		\if jp
		\brief ExecutionKind を取得する
		\else
		\brief Get the ExecutionKind
		\endif
		"""
		return self._profile.kind


	def add(self, comp):
		"""
		\if jp
		\brief コンポーネントを追加する
		\param comp(RTC.LightweightRTObject)
		\else
		\brief Add a component
		\param comp(RTC.LightweightRTObject)
		\endif
		"""
		if CORBA.is_nil(comp):
			return RTC.BAD_PARAMETER
		try:
			dfp_  = comp._narrow(RTC.DataFlowComponent)
			id_   = dfp_.attach_executioncontext(self._ref)
			comp_ = self.Comp(ref=comp, dfp=dfp_, id=id_)
			self._comps.append(comp_)
			return RTC.RTC_OK
		except CORBA.Exception:
			return RTC.BAD_PARAMETER

		return RTC.RTC_OK


	def remove(self, comp):
		"""
		\if jp
		\brief コンポーネントをコンポーネントリストから削除する
		\param comp(RTC.LightweightRTObject)
		\else
		\brief Remove the component from component list
		\param comp(RTC.LightweightRTObject)
		\endif
		"""
		predi = self.find_comp(comp)
		len_ = len(self._comps)
		for i in range(len_):
			idx = (len_ - 1) - i
			if predi(self._comps[idx]):
				self._comps[idx]._ref.detach_executioncontext(self._comps[idx]._sm.ec_id)
				del self._comps[idx]
				return RTC.RTC_OK

		return RTC.BAD_PARAMETER


	def get_profile(self):
		"""
		\if jp
		\brief ExecutionContextProfile を取得する
		\else
		\brief Get the ExecutionContextProfile
		\endif
		"""
		p = RTC.ExecutionContextProfile(self._profile.kind,
										self._profile.rate,
										self._profile.owner,
										self._profile.participants,
										self._profile.properties)
		return p
	

	class Comp:
		def __init__(self, ref=None, dfp=None, id=None, comp=None):
			if comp == None:
				self._ref = ref
				self._sm = PeriodicExecutionContext.DFP(dfp,id)
			else:
				self._ref = comp._ref
				self._sm  = PeriodicExecutionContext.DFP(comp._sm._obj,comp._sm.ec_id)



	class find_comp:
		def __init__(self, comp):
			self._comp = comp
		
		def __call__(self, comp):
			retval = comp._ref._is_equivalent(self._comp)
			return retval

	class invoke_on_startup:
		def __init__(self):
			pass

		def __call__(self, comp):
			comp._sm.on_startup()

	class invoke_on_shutdown:
		def __init__(self):
			pass
		
		def __call__(self, comp):
			comp._sm.on_shutdown()

	class invoke_on_rate_changed:
		def __init__(self):
			pass

		def __call__(self, comp):
			comp._sm.on_rate_changed()

	class invoke_worker:
		def __init__(self):
			pass

		def __call__(self, comp):
			comp._sm.worker()



def PeriodicExecutionContextInit(manager):
	manager.registerECFactory("PeriodicExecutionContext",
							  OpenRTM.PeriodicExecutionContext,
							  OpenRTM.ECDelete)
