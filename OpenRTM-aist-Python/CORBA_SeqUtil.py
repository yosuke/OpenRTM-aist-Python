#!/usr/bin/env python
# -*- coding: euc-jp -*-


##
# @file CORBA_SeqUtil.py
#  CORBA sequence utility template functions
# @date $Date: 2007/09/03 $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.
#


##
# @if jp
#  
# CORBA sequence ヘルパーテンプレート関数
# 
# CORBA sequence に対して以下のユーティリティテンプレート関数を提供する。
# 操作はスレッドセーフではないので、スレッドセーフに操作したい場合は、
# 対象となるシーケンス値を適切にmutex等で保護する必要がある。
# 
# - for_each()
# - find()
# - push_back()
# - insert()
# - front()
# - back()
# - erase()
# - clear()
# 
# @else
#  
# CORBA sequence helper template functions
# 
# This group provides the following utility function to CORBA sequence.
# Since these functions are not thread-safe operations,
# if the sequence would be operated in thread-safe,
# the value should be protected by mutex properly.
# 
# - for_each()
# - find()
# - push_back()
# - insert()
# - front()
# - back()
# - erase()
# - clear()
# 
# @endif



##
# @if jp
#  
# CORBA sequence に対して functor を適用する
# 
# CORBA sequence 全ての要素に対して、与えられた functor を適用する。
# functor は void functor(CORBA sequence の要素) の形式をとる必要がある。
# 
# @return 全ての要素を処理した Functor
# @param seq Functor を適用する CORBA sequence
# @param functor CORBA sequence の要素を処理する Functor
#   
# @else
# 
# Apply the functor to all CORBA sequence elements
# 
# Apply the given functor to the given CORBA sequence.
# functor should be void functor(CORBA sequence element).
# 
# @return Functor that processed all CORBA sequence elements
# @param seq CORBA sequence to be applied the functor
# @param functor A functor to process CORBA sequence elements
# 
# @endif
def for_each(seq, f):
	len_ = len(seq)
	for i in range(len_):
		f(seq[i])
	return f



##
# @if jp
# CORBA sequence の中から functor に適合する要素のインデックスを返す
# 
# CORBA sequence 全ての要素に対して、与えられた functor を適用し、
# functor が true を返すようそのインデックスを返す。
# functor は bool functor(const CORBA sequence の要素) の形式をとり、
# 適合する要素に対して true を返す必要がある。
# 
# @return Functor に適合する要素のインデックス。
# 見つからないときは -1 を返す。
# @param seq Functor を適用する CORBA sequence
# @param functor CORBA sequence から要素を見つける Functor
# 
# @else
# 
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
# 
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
# 
# Push the new element back to the CORBA sequence
# 
# Add the given element to the last of CORBA sequence.
# The length of the CORBA sequence will be expanded automatically.
# 
# @param seq CORBA sequence to be added a new element
# @param elem The new element to be added to the CORBA sequence
# 
# @endif
def push_back(seq, elem):
	seq.append(elem)


def push_back_list(seq1, seq2):
	for elem in seq2:
		seq1.append(elem)


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
# 
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
# 
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
# 
# Get the front element of the CORBA sequence
# 
# This operation returns seq[0].
# 
# @param seq The CORBA sequence to be get the element
# 
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
# 
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
# 
# @endif
def erase(seq, index):
	if index > len(seq):
		return

	del seq[index]


def erase_if(seq, f):
	index = find(seq, f)
	if index < 0:
		return
	del seq[index]


##
# @if jp
# CORBA sequence の全要素を削除
# 
# seq.length(0) と同じ。
# 
# @else
# 
# Erase all the elements of the CORBA sequence
# 
# same as seq.length(0).
# 
# @endif
def clear(seq):
	del seq[0:]
