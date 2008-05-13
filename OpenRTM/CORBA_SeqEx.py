#!/usr/bin/env python
# -*- coding: euc-jp -*-


##
#  @file CORBA_SeqEx.py
#  @brief CORBA utility template classes
#  @date $Date: 2007/09/12 $
#  @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
# 
#  Copyright (C) 2006
#      Task-intelligence Research Group,
#      Intelligent Systems Research Institute,
#      National Institute of
#          Advanced Industrial Science and Technology (AIST), Japan
#      All rights reserved.

import threading
import OpenRTM


class ScopedLock:
	
	def __init__(self, mutex):
		self.mutex = mutex
		self.mutex.acquire()

	def __del__(self):
		self.mutex.release()


##
# @if jp
#  CORBA sequence に対して functor を適用する
# 
# CORBA sequence 全ての要素に対して、与えられた functor を適用する。
# functor は void functor(CORBA sequence の要素) の形式をとる必要がある。
# 
# @return 全ての要素を処理した Functor
# @param seq Functor を適用する CORBA sequence
# @param functor CORBA sequence の要素を処理する Functor
# 
# @else
#  Apply the functor to all CORBA sequence elements
# 
# Apply the given functor to the given CORBA sequence.
# functor should be void functor(CORBA sequence element).
# 
# @return Functor that processed all CORBA sequence elements
# @param seq CORBA sequence to be applied the functor
# @param functor A functor to process CORBA sequence elements
# @endif

def for_each(seq, f):
	len_ = len(seq)

	for i in range(len_):
		f(seq[i])

	return f


##
# @if jp
#  CORBA sequence の中から functor に適合する要素のインデックスを返す
# 	
#  CORBA sequence 全ての要素に対して、与えられた functor を適用し、
#  functor が true を返すようそのインデックスを返す。
#  functor は bool functor(const CORBA sequence の要素) の形式をとり、
#  適合する要素に対して true を返す必要がある。
#  
# @return Functor に適合する要素のインデックス。
# 見つからないときは -1 を返す。
# @param seq Functor を適用する CORBA sequence
# @param functor CORBA sequence から要素を見つける Functor
# 
# @else
# Return the index of CORBA sequence element that functor matches 
# 
# This operation applies the given functor to the given CORBA sequence,
# and returns the index of the sequence element that the functor matches.
# The functor should be bool functor(const CORBA sequence element) type,
# and it would return true, if the element matched the functor.
# 
# @return The index of the element that functor matches.
# If no element found, it would return -1.
# @param seq CORBA sequence to be applied the functor
# @param functor A functor to process CORBA sequence elements
# @endif

def find(seq, f):
	len_ = len(seq)

	for i in range(len_):
		if f(seq[i]):
			return i
	return -1


##
# @if jp
# CORBA sequence の最後に要素を追加する
# 
# CORBA sequence の最後に与えられた要素を追加する。
# CORBA sequence の長さは自動的に拡張される。
# 
# @param seq 要素を追加する CORBA sequence
# @param elem 追加する要素
# 
# @else
# Push the new element back to the CORBA sequence
# 
# Add the given element to the last of CORBA sequence.
# The length of the CORBA sequence will be expanded automatically.
# 
# @param seq CORBA sequence to be added a new element
# @param elem The new element to be added to the CORBA sequence
# @endif

def push_back(seq, elem):
	seq.append(elem)

##
# @if jp
# CORBA sequence に要素を挿入する
# 
# CORBA sequence の index の位置に要素を加える。
# index が 与えられた　CORBA sequence の最大の index より大きい場合
# 最後の要素として加えられる。
# CORBA sequence の長さは自動的に拡張される。
# 
# @param seq 要素を追加する CORBA sequence
# @param elem 追加する要素
# @param index 要素を追加する位置
# 
# @else
# Insert the element to the CORBA sequence
# 
# Insert a new element in the given position to the CORBA sequence.
# If the given index is greater than the length of the sequence,
# the given element is pushed back to the last of the sequence.
# The length of the CORBA sequence will be expanded automatically.
# 
# @param seq The CORBA sequence to be inserted a new element
# @param elem The new element to be inserted the sequence
# @param index The inserting position
# @endif

def insert(seq, elem, index):
	len_ = len(seq)
	if index > len:
		seq.append(elem)
		return
	seq.insert(index, elem)


##
# @if jp
# CORBA sequence の先頭要素を取得する
# 
# seq[0] と同じ。
# 
# @param seq 要素を取得する CORBA sequence
# 
# @else
# Get the front element of the CORBA sequence
# 
# This operation returns seq[0].
# 
# @param seq The CORBA sequence to be get the element
# @endif

def front(seq):
	return seq[0]


##
# @if jp
# CORBA sequence の末尾要素を取得する
# 
# seq[seq.length() - 1] と同じ。
# 
# @param seq 要素を取得する CORBA sequence
# 
# @else
# 
# Get the last element of the CORBA sequence
# 
# This operation returns seq[seq.length() - 1].
# 
# @param seq The CORBA sequence to be get the element
# @endif

def back(seq):
	return seq[-1]


##
# @if jp
# CORBA sequence の指定された位置の要素を削除する
# 
# 指定されたインデックスの要素を削除する。
# 削除された要素は詰められ、sequence の長さは1減る。
# 
# @param seq 要素を削除する CORBA sequence
# @param index 削除する要素のインデックス
# 
# @else
# 
# Erase the element of the specified index
# 
# This operation removes the element of the given index.
# The other elements are closed up around the hole.
# 
# @param seq The CORBA sequence to be get the element
# @param index The index of the element to be removed
# @endif

def erase(seq, index):
	if index > len(seq):
		return

	del seq[index]


##
# @if jp
# CORBA sequence の全要素を削除
# 
# seq.length(0) と同じ。
# 
# @else
# Erase all the elements of the CORBA sequence
# 
# same as seq.length(0).
# @endif

def clear(seq):
	del seq[0:]



""" CORBA sequence extention class """

class LockedStruct:
	
	def __init__(self):
		self.lock = threading.RLock()
		self.data = None

##
# @if jp
# @class SequenceEx
# CORBA::sequence 拡張クラス
# 
# このクラスは CORBA の sequence 型を拡張し std::vector のインターフェースを
# 提供する (例えば size(), max_size(), empty(), resize(), insert(),
# 	  erase(), erase_if(), push_back(), pop_back(), find()).
# CORBA の sequence 型を継承しているため、CORBA の sequence 型の
# オペレーション(like operator=(), maximum(), length(), operator[])も
# 使用可能である。
# 
# @else
# CORBA::sequence extention class
# 
# This class extends CORBA sequence type, and provides std::vector like
# interfaces (like size(), max_size(), empty(), resize(), insert(),
# 	    erase(), erase_if(), push_back(), pop_back(), find()).
# Since this class inherits CORBA sequence class, user can also use CORBA
# sequence interfaces (like operator=(), maximum(), length(), operator[]).
# @endif

class SequenceEx:
	
	##
	# @if jp
	# 	
	# CorbaSequence からのコピーコンストラクタ
	# 
	# CorbaSequence型からのコピーコンストラクタ。
	# 与えられた CorbaSequence の内容をコピーする。
	# 
	# @param _sq CorbaSequence 形のコピー元
	# 
	# @else
	# Copy constructor from CorbaSequence
	# 
	# This constructor copies sequence contents from given CorbaSequence
	# to this object.
	# 
	# @param _sq Copy source of CorbaSequence type
	# @endif

	def __init__(self, _sq):
		len_ = len(_sq)
		self._seq = []
		for i in range(len_):
			self._seq.append(_sq[i])
		self._mutex = threading.RLock()


	##
	# @if jp
	# デストラクタ
	# @else
	# Destructor
	# @endif

	def __del__(self):
		self._seq = []


	##
	# @if jp
	# 
	# サイズを取得する
	# 
	# このオペレーションはシーケンスのサイズを返す。
	# CorbaSequence::length() と同じ。
	# @return シーケンスのサイズ
	# 
	# @else
	# Get size of this sequence
	# 
	# This operation returns the size of the sequence.
	# This is same as CorbaSequence::length().
	# @return The size of the sequence.
	# @endif

	def size(self):
		return len(self._seq)


	##
	# @if jp
	# 格納可能な最大のサイズを取得する
	# 
	# このオペレーションはシーケンスの現在の格納可能な最大のサイズを返す。
	# CorbaSequence::maximum() と同じ。
	# @return シーケンスに格納可能な最大のサイズ
	# 
	# @else
	# Get current maximum size of this sequence
	# 
	# This operation returns the current maximum size of the sequence.
	# This is same as CorbaSequence::maximum().
	# @return The maximum size of the sequence.
	# @endif

	def max_size(self):
		return len(self._seq)


	##
	# @if jp
	# シーケンスが空かどうか調べる
	# 
	# このオペレーションはシーケンスが空かどうかを bool 値で返す。
	# サイズが 0 なら true、そうでなければ false を返す。
	# @return シーケンスが空かどうかの bool 値
	# 
	# @else
	# Test whether the sequence is empty
	# 
	# This operation returns bool value whether the sequence is empty.
	# If the size of the sequence is 0, this operation returns true,
	# and in other case this operation returns false.
	# @return The bool value whether the sequence is empty.
	# @endif

	def empty(self):
		if not self._seq:
			return False
		else:
			return True


	##
	# @if jp
	# シーケンスをリサイズする
	# 
	# このオペレーションはシーケンスの長さを変更する。
	# 現在の長さより大きなサイズが与えられた場合、引数 x で、
	# 新たにアロケートされた部分が埋められる。
	# 現在の長さより小さいサイズが与えられた場合、CorabSequence と同様に
	# 余分なシーケンスの要素は削除される。
	# @param new_size 新しいシーケンスのサイズ
	# @param item　長くなった分のシーケンスを埋める要素
	# 
	# @else
	# Resize the length of the sequence
	# 
	# This operation resizes the length of the sequence.
	# If longer length than current sequence length is given,
	# newly allocated rooms will be assigned by element given by the argument.
	# If shorter length than current sequence length is given,
	# the excessive element of a sequence is deleted like behavior of
	# CorabSequence
	# @param new_size The new size of the sequence
	# @param item　   Sequence element to be assigned to new rooms.
	# @endif

	def resize(self, new_size, item):
		guard = ScopedLock(self._mutex)
		len_ = len(self._seq)
		if new_size > len_:
			self._seq = []
			for i in range(len_):
				self._seq.append(item)
		elif new_size < len_:
			del self._seq[new_size:]


	##
	# @if jp
	# シーケンスに要素を挿入する
	# 
	# このオペレーションはシーケンスの途中に要素を挿入する。
	# @param position 新しい要素を挿入する場所
	# @param item　挿入するシーケンスの要素
	# 
	# @else
	# Insert a new item to the sequence
	# 
	# This operation inserts a new item to the sequence.
	# @param position The position of new inserted item.
	# @param item　   Sequence element to be inserted.
	# @endif

	def insert(self, position, item):
		guard = ScopedLock(self._mutex)
		len_ = len(self._seq)
		if position > len_:
			raise

		self._seq.insert(position, item)


	##
	# @if jp
	# シーケンスの要素を削除する
	# 
	# このオペレーションはシーケンスの要素を削除する
	# @param position 削除するシーケンス要素の場所
	# 
	# @else
	# Erase an item of the sequence
	# 
	# This operation erases an item from the sequence.
	# @param position The position of erased item.
	# @endif

	def erase(self, position):
		guard = ScopedLock(self._mutex)
		len_ = len(self._seq)
		if position > (len_ - 1):
			raise

		erased = self._seq[position]
		del self._seq[position]
		return erased


	##
	# @if jp
	# シーケンスの要素を述語のしたがって削除する
	# 
	# このオペレーションは述語として与えられた関数オブジェクトの
	# 条件が真のとき、そのシーケンスの要素を削除する。
	# @param f 削除するシーケンスを決定する術語
	# 
	# @else
	# Erase an item according to the given predicate
	# 
	# This operation erases an item according to the given predicate.
	# @param f The predicate functor to decide deletion.
	# @endif

	def erase_if(self, f):
		guard = ScopedLock(self._mutex)
		len_ = len(self._seq)
		for i in range(len_):
			if f(self._seq[i]):
				return self.erase(i)
		raise


	##
	# @if jp
	# 要素を最後尾に追加する
	# 
	# このオペレーションは与えられた要素をシーケンスの最後に追加する。
	# @param item 追加するするオブジェクト
	# 
	# @else
	# Append an item to the end of the sequence.
	# 
	# This operation push back an item to the of the sequence.
	# @param item The object to be added to the end of the sequnce.
	# @endif
	def push_back(self, item):
		guard = ScopedLock(self._mutex)
		self._seq.append(item)


	def pop_back(self):
		guard = ScopedLock(self._mutex)
		del self._seq[-1]


	def find(self, f):
		guard = ScopedLock(self._mutex)
		len_ = len(self._seq)
		for i in range(len_):
			if f(self._seq[i]):
				return self._seq[i]
		raise
