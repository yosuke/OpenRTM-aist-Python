#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
 \file StateMachine.py
 \brief State machine template class
 \date $Date: 2007/08/30$
 \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara

 Copyright (C) 2006
     Task-intelligence Research Group,
     Intelligent Systems Research Institute,
     National Institute of
         Advanced Industrial Science and Technology (AIST), Japan
     All rights reserved.
"""


import threading

import OpenRTM
import RTC, RTC__POA

class ScopedLock:
	def __init__(self, mutex):
		self.mutex = mutex
		self.mutex.acquire()

	def __del__(self):
		self.mutex.release()
		

class StateHolder:
	def __init__(self):
		self.curr = None
		self.prev = None
		self.next = None



class StateMachine:
	"""
	\if jp
	\class StateMachine
	\brief 状態マシンクラス
	StateMachine クラスは状態マシンを実現するクラスである。
	例: ActiveObjectは状態マシンを持つアクティブオブジェクトであるとする。
	状態は3状態 INACTIVE, ACTIVE, ERROR あり、各状態でのEntryやExit動作を
	定義したいとすると、以下のように実現される。
	<pre>
	class ActiveObject 
	{  
	public: 
	  enum MyState { INACTIVE, ACTIVE, ERROR }; 
	  typedef States<MyState> MyStates; 

	  ActiveObject() 
		: m_sm(3) 
	  { 
		m_sm.setNOP(&ActiveObject::nullAction); 
		m_sm.setListener(this); 

		m_sm.setExitAction(NACTIVE, &ActiveObject::inactiveExit); 
		  : 
		m_sm.setPostDoAction(ERROR, &ActiveObject::errorPostDo); 
		m_sm.setTransitionAction(&ActiveObject:tratransitionnsition); 
	  }; 

	  bool nullAction(MyStates st) {}; 
	  bool inactiveExit(MyStates st) {}; 
		: 
	  bool errorPostDo(MyStates st) {}; 
	  bool transition(MyStates st) {}; 

	private: 
	  StateMachine<MyState, bool, ActiveObject> m_sm; 
	}; 
	</pre>
	状態を持たせたいクラスは以下の条件を満たすように実装しなければならない。
	<ol>
	<li> enum で状態を定義
	<li> StateMachine のテンプレート引数は、<br>
		<状態の型(MyState), アクション関数の戻り値(bool), 当該オブジェクトの型>
	<li> StateMachine のコンストラクタ引数は状態の数
	<li> 以下のアクション関数を(Return _function_name_(States)) の関数として設定
	<ol>
		<li> 何もしない関数を必ず定義し、setNOP で与えなければならない
		<li> 各状態毎に, set(Entry|PreDo|Do|PostDo|Exit)Action でアクションを設定
		<li> 状態遷移時のアクションを setTransitionAction() で設定。
	</ol>
	<li> 遷移時のアクションは、与えられた現在状態、次状態、前状態を元に、
		ユーザが実装しなければならない。
	<li> 状態の変更は goTo() で、状態のチェックは isIn(state) で行う。
	<li> goTo()は次状態を強制的にセットする関数であり、遷移の可否は、
		ユーザが現在状態を取得し判断するロジックを実装しなければならない。
	</ol>

	このクラスは、一つの状態に対して、
	<ul>
	<li> Entry action
	<li> PreDo action
	<li> Do action2
	<li> PostDo action
	<li> Exit action
	</ul>
	5つのアクションが定義することができる。
	Transition action はあらゆる状態間遷移で呼び出されるアクションで、
	その振る舞いはユーザが定義しなければならない。

	このクラスは以下のようなタイミングで各アクションが実行される。

	<ul>
	<li> 状態が変更され(A->B)状態が遷移する場合 <br>
	(A:Exit)->|(状態更新:A->B)->(B:Entry)->(B:PreDo)->(B:Do)->(B:PostDo)

	<li> 状態が変更されず、B状態を維持する場合 (|はステップの区切りを表す)<br>
	(B(n-1):PostDo)->|(B(n):PreDo)->(B(n):Do)->(B(n):PostDo)->|(B(n+1):PreDo)<br>
	PreDo, Do, PostDo が繰り返し実行される。

	<li> 自己遷移する場合 <br>
	(B(n-1):PostDo)->(B(n-1):Exit)->|(B(n):Entry)->(B(n):PreDo) <br>
	一旦 Exit が呼ばれた後、Entry が実行され、以降は前項と同じ動作をする。
	</ul>2
		\else

	\brief

	\endif

	"""

	state_array = (RTC.INACTIVE_STATE,
				   RTC.ACTIVE_STATE,
				   RTC.ERROR_STATE,
				   RTC.UNKNOWN_STATE)

	def __init__(self, num_of_state):
		"""
		\if jp
		\brief コンストラクタ
		\param num_of_state(int)
		\else
		\brief Constructor
		\param num_of_state(int)
		\endif
		"""
		self._num = num_of_state
		self._entry  = {}
		self._predo  = {}
		self._do     = {}
		self._postdo = {}
		self._exit   = {}

		self.setNullFunc(self._entry,  None)
		self.setNullFunc(self._do,     None)
		self.setNullFunc(self._exit,   None)
		self.setNullFunc(self._predo,  None)
		self.setNullFunc(self._postdo, None)
		self._transit = None
		self._mutex = threading.RLock()
		self._selftrans = False


	def setNOP(self, call_back):
		"""
		\if jp
		\brief NOP関数を登録する
		\param call_back(function object)
		\else
		\brief Set NOP function
		\param call_back(function object)
		\endif
		"""
		self.setNullFunc(self._entry,  call_back)
		self.setNullFunc(self._do,     call_back)
		self.setNullFunc(self._exit,   call_back)
		self.setNullFunc(self._predo,  call_back)
		self.setNullFunc(self._postdo, call_back)
		self._transit = call_back


	def setListener(self, listener):
		"""
		\if jp
		\brief Listener オブジェクトを登録する
		\param listener(class of function object)
		\else
		\brief Set Listener Object
		\param listener(class of function object)
		\endif
		"""
		self._listener = listener


	def setEntryAction(self, state, call_back):
		"""
		\if jp
		\brief Entry action 関数を登録する
		\param state(RTC.LifeCycleState)
		\param call_back(function object)
		\else
		\brief Set Entry action function
		\param state(RTC.LifeCycleState)
		\param call_back(function object)
		\endif
		"""
		if self._entry.has_key(state):
			self._entry[state] = call_back
		else:
			self._entry.setdefault(state, call_back)
		return True


	def setPreDoAction(self, state, call_back):
		"""
		\if jp
		\brief PreDo action 関数を登録する
		\param state(RTC.LifeCycleState)
		\param call_back(function object)
		\else
		\brief Set PreDo action function
		\param state(RTC.LifeCycleState)
		\param call_back(function object)
		\endif
		"""
		if self._predo.has_key(state):
			self._predo[state] = call_back
		else:
			self._predo.setdefault(state, call_back)
		return True


	def setDoAction(self, state, call_back):
		"""
		\if jp
		\brief Do action 関数を登録する
		\param state(RTC.LifeCycleState)
		\param call_back(function object)
		\else
		\brief Set Do action function
		\param state(RTC.LifeCycleState)
		\param call_back(function object)
		\endif
		"""
		if self._do.has_key(state):
			self._do[state] = call_back
		else:
			self._do.setdefault(state, call_back)
		return True



	def setPostDoAction(self, state, call_back):
		"""
		\if jp
		\brief Post action 関数を登録する
		\param state(RTC.LifeCycleState)
		\param call_back(function object)
		\else
		\brief Set Post action function
		\param state(RTC.LifeCycleState)
		\param call_back(function object)
		\endif
		"""
		if self._postdo.has_key(state):
			self._postdo[state] = call_back
		else:
			self._postdo.setdefault(state, call_back)
		return True


	def setExitAction(self, state, call_back):
		"""
		\if jp
		\brief Exit action 関数を登録する
		\param state(RTC.LifeCycleState)
		\param call_back(function object)
		\else
		\brief Set Exit action function
		\param state(RTC.LifeCycleState)
		\param call_back(function object)
		\endif
		"""
		if self._exit.has_key(state):
			self._exit[state] = call_back
		else:
			self._exit.setdefault(state, call_back)
		return True


	def setTransitionAction(self, call_back):
		"""
		\if jp
		\brief State transition action 関数を登録する
		\param call_back(function object)
		\else
		\brief Set state transition action function
		\param call_back(function object)
		\endif
		"""
		self._transit = call_back
		return True


	def setStartState(self, states):
		"""
		\if jp
		\brief 初期状態をセットする
		\param state(RTC.LifeCycleState)
		\else
		\brief Set Exit action function
		\param state(RTC.LifeCycleState)
		\endif
		"""
		self._states = StateHolder()
		self._states.curr = states.curr
		self._states.prev = states.prev
		self._states.next = states.next


	def getStates(self):
		"""
		\if jp
		\brief 状態を取得する
		\else
		\brief Get state machine's status
		\endif
		"""
		guard = ScopedLock(self._mutex)
		return self._states


	def getState(self):
		guard = ScopedLock(self._mutex)
		return self._states.curr


	def isIn(self, state):
		"""
		\if jp
		\brief 現在状態を確認
		\param state(RTC.LifeCycleState)
		\else
		\brief Evaluate current status
		\param state(RTC.LifeCycleState)
		\endif
		"""
		guard = ScopedLock(self._mutex)
		if self._states.curr == state:
			return True
		else:
			return False


	def goTo(self, state):
		"""
		\if jp
		\brief 状態を変更
		\param state(RTC.LifeCycleState)
		\else
		\brief Change status
		\param state(RTC.LifeCycleState)
		\endif
		"""
		guard = ScopedLock(self._mutex)
		self._states.next = state
		if self._states.curr == state:
			self._selftrans  = True


	def worker(self):
		"""
		\if jp
		\brief 駆動関数
		\else
		\brief Worker function
		\endif
		"""
		states = StateHolder()
		self.sync(states)

		# If no state transition required, execute set of do-actions
		if states.curr == states.next:
			# pre-do
			if self._predo[states.curr] != None:
				self._predo[states.curr](states)
			if self.need_trans():
				return

			# do
			if self._do[states.curr] != None:
				self._do[states.curr](states)
			if self.need_trans():
				return

			# post-do
			if self._postdo[states.curr] != None:
				self._postdo[states.curr](states)
		# If state transition required, exit current state and enter next state
		else:
			if self._exit[states.curr] != None:
				self._exit[states.curr](states)
			self.sync(states)

			# If state transition still required, move to the next state
			if states.curr != states.next:
				states.curr = states.next
				if self._entry[states.curr] != None:
					self._entry[states.curr](states)
				self.update_curr(states.curr)


	def setNullFunc(self, s, nullfunc):
		"""
		 \param s(map of callback function object)
		 \param nullfunc(callback function object)
		"""
		for i in range(self._num):
			if s.has_key(StateMachine.state_array[i]):
				s[StateMachine.state_array[i]] = nullfunc
			else:
				s.setdefault(StateMachine.state_array[i], nullfunc)


	def sync(self, states):
		"""
		 \param state(OpenRTM.StateHolder<RTC.LifeCycleState>)
		"""
		guard = ScopedLock(self._mutex)
		states.prev = self._states.prev
		states.curr = self._states.curr
		states.next = self._states.next
		

	def need_trans(self):
		guard = ScopedLock(self._mutex)
		return (self._states.curr != self._states.next)


	def update_curr(self, curr):
		"""
		 \param curr(RTC.LifeCycleState)
		""" 
		guard = ScopedLock(self._mutex)
		self._states.curr = curr
