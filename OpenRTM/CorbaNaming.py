#!/usr/bin/env python
# -*- coding: euc-jp -*-


##
#  @file CorbaNaming.py
#   CORBA naming service helper class
#  @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
# 
#  Copyright (C) 2006
#      Noriaki Ando
#      Task-intelligence Research Group,
#      Intelligent Systems Research Institute,
#      National Institute of
#          Advanced Industrial Science and Technology (AIST), Japan
#      All rights reserved.

import omniORB.CORBA as CORBA
import CosNaming
import string


##
# @if jp
# @class CorbaNaming
#  CORBA Naming Service ヘルパークラス
# 
# このクラスは、CosNaming.NameComponent に対するラッパークラスである。
# CosNaming.NameComponent が持つオペレーションとほぼ同じ機能の
# オペレーションを提供するとともに、ネームコンポーネント CosNaming.NameComponent
# の代わりに文字列による名前表現を受け付けるオペレーションも提供する。
# 
# オブジェクトは生成時、あるいは生成直後に CORBA ネームサーバに接続し
# 以後、このネームサーバのルートコンテキストに対して種々のオペレーション
# を処理する。
# 深い階層のネーミングコンテキストの作成やオブジェクトのバインドにおいて、
# 途中のコンテキストが存在しない場合でも、強制的にコンテキストをバインド
# し目的のコンテキストやオブジェクトのバインドを行うこともできる。
# 
# @else
# @class CorbaNaming
#  CORBA Naming Service helper class
# 
# This class is a wrapper class of CosNaming.NameComponent.
# Almost the same operations which CosNaming.NameComponent has are
# provided, and some operation allows string naming representation of
# context and object instead of CosNaming.NameComponent.
# 
# The object of the class would connect to a CORBA naming server at
# the instantiation or immediately after instantiation.
# After that the object invokes operations to the root context of it.
# This class realizes forced binding to deep NamingContext, without binding
# intermediate NamingContexts explicitly.
# @endif

class CorbaNaming:
	

	##
	# @if jp
	#  クラスコンストラクタ
	# @param orb(CORBA.ORB_ptr)
	# @param name_server(string)
	# 
	# @else
	#  constructor.
	# @param orb(CORBA.ORB_ptr)
	# @param name_server(string)
	# @endif
	def __init__(self, orb, name_server=None):
		self._orb = orb
		self._nameServer = ""
		self._rootContext = CosNaming.NamingContext._nil
		self._blLength = 100

		if name_server != None:
			self._nameServer = "corbaloc::" + name_server + "/NameService"
			try:
				obj = orb.string_to_object(self._nameServer)
				self._rootContext = obj._narrow(CosNaming.NamingContext)
				if CORBA.is_nil(self._rootContext):
					print "CorbaNaming: Failed to narrow the root naming context."

			except CORBA.ORB.InvalidName:
				print "Service required is invalid [does not exist]."

		return
	

	def __del__(self):
		return


	##
	# @if jp
	#  初期化用メソッド
	# @param name_server(string)
	# 
	# @else
	#  initialiize method.
	# @param name_server(string)
	# @endif
	def init(self, name_server):
		self._nameServer = "corbaloc::" + name_server + "/NameService"
		obj = self._orb.string_to_object(self._nameServer)
		self._rootContext = obj._narrow(CosNaming.NamingContext)
		if CORBA.is_nil(self._rootContext):
			raise MemoryError

		return


	##
	# @if jp
	# 
	#  Object を bind する
	# 
	# CosNaming::bind() とほぼ同等の働きをするが、常に与えられたネームサーバの
	# ルートコンテキストに対してbind()が呼び出される点が異なる。
	# 
	# Name <name> と Object <obj> を当該 NamingContext 上にバインドする。
	# c_n が n 番目の NameComponent をあらわすとすると、
	# name が n 個の NameComponent から成るとき、以下のように扱われる。
	# 
	# cxt->bind(<c_1, c_2, ... c_n>, obj) は以下の操作と同等である。
	# cxt->resolve(<c_1, ... c_(n-1)>)->bind(<c_n>, obj)
	# 
	# すなわち、1番目からn-1番目のコンテキストを解決し、n-1番目のコンテキスト
	# 上に name <n> として　obj を bind する。
	# 名前解決に参加する <c_1, ... c_(n-1)> の NemingContext は、
	# bindContext() や rebindContext() で既にバインド済みでなければならない。
	# もし <c_1, ... c_(n-1)> の NamingContext が存在しない場合には、
	# NotFound 例外が発生する。
	# 
	# ただし、強制バインドフラグ force が true の時は、<c_1, ... c_(n-1)>
	# が存在しない場合にも、再帰的にコンテキストをバインドしながら、
	# 最終的に obj を名前 name <c_n> にバインドする。
	# 
	# いずれの場合でも、n-1番目のコンテキスト上に name<n> のオブジェクト
	# (Object あるいは コンテキスト) がバインドされていれば
	# AlreadyBound 例外が発生する。
	# 
	# @param name_list(list) オブジェクトに付ける名前の NameComponentリスト
	# @param obj(CORBA::Object) 関連付けられる Object
	# @param force(bool) trueの場合、途中のコンテキストを強制的にバインドする
	# 
	# @exception NotFound 途中の <c_1, c_2, ..., c_(n-1)> が存在しない。
	# @exception CannotProceed 何らかの理由で処理を継続できない。
	# @exception InvalidName 引数 name の名前が不正。
	# @exception AlreadyBound name <c_n> の Object がすでにバインドされている。
	# 
	# @else
	# 
	# 
	# 
	# @endif
	def bind(self, name_list, obj, force=None):
		if force == None :
			force = True

		try:
			self._rootContext.bind(name_list, obj)
		except CosNaming.NamingContext.NotFound:
			if force:
				self.bindRecursive(self._rootContext, name_list, obj)
			else:
				raise
		except CosNaming.NamingContext.CannotProceed, err:
			if force:
				self.bindRecursive(err.cxt, err.rest_of_name, obj)
			else:
				raise
		except CosNaming.NamingContext.AlreadyBound:
			self._rootContext.rebind(name_list, obj)


	##
	# @if jp
	#  Object を bind する
	# 
	# Object を bind する際に与える名前が文字列表現であること以外は、bind()
	# と同じである。bind(toName(string_name), obj) と等価。
	# @param string_name(string) オブジェクトに付ける名前の文字列表現
	# @param obj(CORBA::Object) 関連付けられるオブジェクト
	# @param force(bool) trueの場合、途中のコンテキストを強制的にバインドする
	# @exception NotFound 途中の <c_1, c_2, ..., c_(n-1)> が存在しない。
	# @exception CannotProceed 何らかの理由で処理を継続できない。
	# @exception InvalidName 引数 name の名前が不正。
	# @exception AlreadyBound name <n> の Object がすでにバインドされている。
	# 
	# @else
	# 
	# @endif
	def bindByString(self, string_name, obj, force=True):
		self.bind(self.toName(string_name), obj, force)


	##
	# @if jp
	#  途中のコンテキストを bind しながら Object を bind する
	# 
	# context で与えられた NamingContext に対して、name_list で指定された
	# ネームコンポーネント <c_1, ... c_(n-1)> を NamingContext として
	# 解決しながら、名前 <c_n> に対して obj を bind する。
	# もし、<c_1, ... c_(n-1)> に対応する NamingContext がない場合には
	# 新たな NamingContext をバインドする。
	# 
	# 最終的に <c_1, c_2, ..., c_(n-1)> に対応する NamingContext が生成
	# または解決された上で、CosNaming::bind(<c_n>, object) が呼び出される。
	# このとき、すでにバインディングが存在すれば AlreadyBound例外が発生する。
	# 
	# 途中のコンテキストを解決する過程で、解決しようとするコンテキストと
	# 同じ名前の NamingContext ではない Binding が存在する場合、
	# CannotProceed 例外が発生し処理を中止する。
	# @param(CosNaming.NameComponent) context bind を開始する　NamingContext
	# @param name(CosNaming.NameComponentのリスト) オブジェクトに付ける名前のネームコンポーネント
	# @param obj(CORBA::Object) 関連付けられるオブジェクト
	# @exception CannotProceed <c_1, ..., c_(n-1)> に対応する NamingContext 
	# のうちひとつが、すでに NamingContext 以外の object にバインド
	# されており、処理を継続できない。
	# @exception InvalidName 名前 name_list が不正
	# @exception AlreadyBound name <c_n> にすでに何らかの object がバインド
	# されている。
	# @else
	# 
	# @endif
	def bindRecursive(self, context, name_list, obj):
		length = len(name_list)
		cxt = context
		for i in range(length):
			if i == length -1:
				try:
					cxt.bind(self.subName(name_list, i, i), obj)
				except CosNaming.NamingContext.AlreadyBound:
					cxt.rebind(self.subName(name_list, i, i), obj)
				return
			else:
				if self.objIsNamingContext(cxt):
					cxt = self.bindOrResolveContext(cxt,self.subName(name_list, i, i))
				else:
					raise CosNaming.NamingContext.CannotProceed(cxt, self.subName(name_list, i))
		return


	##
	# @if jp
	#  Object を rebind する
	# 
	# name_list で指定された Binding がすでに存在する場合を除いて bind() と同じ
	# である。バインディングがすでに存在する場合には、新しいバインディングに
	# 置き換えられる。
	# @param name_list(CosNaming.NameComponentのlist) オブジェクトに付ける名前の NameComponent
	# @param obj(CORBA::Object) 関連付けられるオブジェクト
	# @param force(bool) trueの場合、途中のコンテキストを強制的にバインドする
	# @else
	# 
	# @endif
	def rebind(self, name_list, obj, force=True):
		if force == None:
			force = True
			
		try:
			self._rootContext.rebind(name_list, obj)

		except CosNaming.NamingContext.NotFound:
			if force:
				self.rebindRecursive(self._rootContext, name_list, obj)
			else:
				raise

		except CosNaming.NamingContext.CannotProceed, err:
			if force:
				self.rebindRecursive(err.cxt, err,rest_of_name, obj)
			else:
				raise
			
		return


	##
	# @if jp
	#  Object を rebind する
	# 
	# Object を rebind する際に与える名前が文字列表現であること以外は rebind()
	# と同じである。rebind(toName(string_name), obj) と等価。
	# @param string_name(string) オブジェクトに付ける名前の文字列表現
	# @param obj(CORBA::Object) 関連付けられるオブジェクト
	# @param force(bool) trueの場合、途中のコンテキストを強制的にバインドする
	# @exception NotFound 途中の <c_1, c_2, ..., c_(n-1)> が存在しない。
	# @exception CannotProceed 何らかの理由で処理を継続できない。
	# @exception InvalidName 引数 name の名前が不正。
	# @else
	# 
	# @endif
	def rebindByString(self, string_name, obj, force=True):
		self.rebind(self.toName(string_name), obj, force)

		return


	##
	# @if jp
	#  途中のコンテキストを bind しながら Object を rebind する
	# 
	# name <c_n> で指定された NamingContext もしくは Object がすでに存在する
	# 場合を除いて bindRecursive() と同じである。
	# 
	# name <c_n> で指定されたバインディングがすでに存在する場合には、
	# 新しいバインディングに置き換えられる。
	# @param context(CosNaming.NameComponent) オブジェクトに付ける名前の文字列表現
	# @param name_list(CosNaming.NameComponentのリスト) 関連付けられるオブジェクト
	# @param obj(CORBA::Object) trueの場合、途中のコンテキストを強制的にバインドする
	# @exception CannotProceed 途中のコンテキストが解決できない。
	# @exception InvalidName 与えられた name が不正。
	# @else
	# 
	# @endif
	def rebindRecursive(self, context, name_list, obj):
		length = len(name_list)
		for i in range(length):
			if i == length - 1:
				context.rebind(self.subName(name_list, i, i), obj)
				return
			else:
				if self.objIsNamingContext(context):
					try:
						context = context.bind_new_context(self.subName(name_list, i, i))
					except CosNaming.NamingContext.AlreadyBound:
						obj_ = context.resolve(self.subName(name_list, i, i))
						context = obj_._narrow(CosNaming.NamingContext)
				else:
					raise CosNaming.NamingContext.CannotProceed(context, self.subName(name_list, i))
		return


	##
	# @if jp
	#  NamingContext を bind する
	# 
	# bind されるオブジェクトが NamingContext であることを除いて bind() 
	# と同じである。
	# @param name(CosNaming.NameComponentのリスト) オブジェクトに付ける名前の文字列表現または、NameComponentのリスト
	# @param name_cxt(CosNaming.NameComponent) 関連付けられる NamingContext
	# @param force(bool) trueの場合、途中のコンテキストを強制的にバインドする
	# @else
	# 
	# @endif
	def bindContext(self, name, name_cxt, force=True):
		if isinstance(name, basestring):
			self.bind(self.toName(name), name_cxt, force)
		else:
			self.bind(name, name_cxt, force)
		return


	##
	# @if jp
	#  NamingContext を bind する
	# 
	# bind されるオブジェクトが NamingContext であることを除いて
	# bindRecursive() と同じである。
	# @param context(CosNaming.NameComponent) bind を開始する　NamingContext
	# @param name_list(CosNaming.NameComponentのリスト) オブジェクトに付ける名前のネームコンポーネント
	# @param name_cxt(CosNaming.NameComponent) 関連付けられる NamingContext
	# @else
	# 
	# @endif
	def bindContextRecursive(self, context, name_list, name_cxt):
		self.bindRecursive(context, name_list, name_cxt)
		return


	##
	# @if jp
	#  NamingContext を rebind する
	# 
	# name で指定されたコンテキストがすでに存在する場合を除いて bindContext() 
	# と同じである。
	# バインディングがすでに存在する場合には、新しいバインディングに
	# 置き換えられる。
	# @param name(CosNaming.NameComponentのリスト) オブジェクトに付ける名前のネームコンポーネントまたは、文字列
	# @param name_cxt(CosNaming.NameComponent) 関連付けられる NamingContext
	# @param force(bool) trueの場合、途中のコンテキストを強制的にバインドする
	# @else
	# 
	# @endif
	def rebindContext(self, name, name_cxt, force=True):
		if isinstance(name, basestring):
			self.rebind(self.toName(name), name_cxt, force)
		else:
			self.rebind(name, name_cxt, force)
		return


	##
	# @if jp
	#  NamingContext を 再帰的にrebind する
	# @param context(CosNaming.NameComponent) NamingContext
	# @param name_list(CosNaming.NameComponentのlist) NamingContextのリスト
	# @param name_cxt(CosNaming.NameComponent) NamingContext
	# @else
	# 
	# @endif
	def rebindContextRecursive(self, context, name_list, name_cxt):
		self.rebindRecursive(context, name_list, name_cxt)
		return


	##
	# @if jp
	#  Object を name から解決する
	# 
	# name に bind されているオブジェクト参照を返す。
	# ネームコンポーネント <c_1, c_2, ... c_n> は再帰的に解決される。
	# 
	# CosNaming::resolve() とほぼ同等の働きをするが、常に与えられた
	# ネームサーバのルートコンテキストに対して resolve() が呼び出される点が
	# 異なる。
	# @param name(CosNaming.NameComponentのリスト または、 str) 解決すべきオブジェクトの名前のネームコンポーネント
	# 　　　　　　または、解決すべきオブジェクトの名前の文字列表現
	# @return 解決されたオブジェクト参照
	# @else
	# @endif
	def resolve(self, name):
		if isinstance(name, basestring):
			name_ = self.toName(name)
		else:
			name_ = name
			
		try:
			obj = self._rootContext.resolve(name_)
			return obj
		except CosNaming.NamingContext.NotFound, ex:
			return None


	##
	# @if jp
	#  指定された名前のオブジェクトの bind を解除する
	# 
	# name に bind されているオブジェクト参照を返す。
	# ネームコンポーネント <c_1, c_2, ... c_n> は再帰的に解決される。
	# 
	# CosNaming::unbind() とほぼ同等の働きをするが、常に与えられた
	# ネームサーバのルートコンテキストに対して unbind() が呼び出される点が
	# 異なる。
	# @param name(CosNaming.NameComponentのリスト または、str) 解決すべきオブジェクトの名前のネームコンポーネント
	# 　　　　　　または、解決すべきオブジェクトの名前の文字列表現
	# @return 解決されたオブジェクト参照
	# @else
	# @endif
	def unbind(self, name):
		if isinstance(name, basestring):
			name_ = self.toName(name)
		else:
			name_ = name

		self._rootContext.unbind(name_)
		return


	##
	# @if jp
	#  新しいコンテキストを生成する
	# 
	# 与えられたネームサーバ上で生成された NamingContext を返す。
	# 返された NamingContext は bind されていない。
	# @return 生成された新しい NamingContext
	# @else
	# @endif
	def newContext(self):
		return self._rootContext.new_context()


	##
	# @if jp
	#  新しいコンテキストを bind する
	# 
	# 与えられた name に対して新しいコンテキストをバインドする。
	# 生成された　NamingContext はネームサーバ上で生成されたものである。
	# @param name(CosNaming.NameComponentのリスト または、 str) NamingContextに付ける名前のネームコンポーネント
	# 　　　　　　または、解決すべきオブジェクトの名前の文字列表現
	# @return 生成された新しい NamingContext
	# @else
	# @endif
	def bindNewContext(self, name, force=True):
		if force == None:
			force = True
			
		if isinstance(name, basestring):
			name_ = self.toName(name)
		else:
			name_ = name

		try:
			return self._rootContext.bind_new_context(name_)
		except CosNaming.NamingContext.NotFound:
			if force:
				self.bindRecursive(self._rootContext, name_, self.newContext())
			else:
				raise
		except CosNaming.NamingContext.CannotProceed, err:
			if force:
				self.bindRecursive(err.cxt, err.rest_of_name, self.newContext())
			else:
				raise
		return None


	##
	# @if jp
	#  NamingContext を非アクティブ化する
	# 
	# context で指定された NamingContext を非アクティブ化する。
	# context に他のコンテキストがバインドされている場合は NotEmpty 例外が
	# 発生する。
	# @param context(CosNaming.NameComponent) 非アクティブ化する NamingContext
	# @else
	#  Destroy the naming context
	# 
	# Delete the specified naming context.
	# any bindings should be <unbind> in which the given context is bound to
	# some names before invoking <destroy> operation on it. 
	# @param context NamingContext which is destroied.
	# @endif
	def destroy(self, context):
		context.destroy()


	##
	# @if jp
	#  NamingContext を再帰的に下って非アクティブ化する
	# @param context(CosNaming.NameComponent) 
	# @else
	#  Destroy the naming context recursively
	# @param context(CosNaming.NameComponent)
	# @endif
	def destroyRecursive(self, context):
		cont = True
		bl = []
		bi = 0
		bl, bi = context.list(self._blLength)
		while cont:
			for i in range(len(bl)):
				if bl[i].binding_type == CosNaming.ncontext:
					obj = context.resolve(bl[i].binding_name)
					next_context = obj._narrow(CosNaming.NamingContext)

					self.destroyRecursive(next_context)
					context.unbind(bl[i].binding_name)
					next_context.destroy()
				elif bl[i].binding_type == CosNaming.nobject:
					context.unbind(bl[i].binding_name)
				else:
					assert(0)
			if CORBA.is_nil(bi):
				cont = False
			else:
				bi.next_n(self._blLength, bl)

		if not (CORBA.is_nil(bi)):
			bi.destroy()
		return


	##
	# @if jp
	#  すべての Binding を削除する
	# @else
	#  Destroy all binding
	# @endif
	def clearAll(self):
		self.destroyRecursive(self._rootContext)
		return


	##
	# @if jp
	#  与えられた NamingContext の Binding を取得する
	# @param name_cxt(CosNaming.NameComponent)
	# @param how_many(long)
	# @param rbl(list)
	# @param rbi(list)
	# @else
	#  Get Binding on the NamingContextDestroy all binding
	# @param name_cxt(CosNaming.NameComponent)
	# @param how_many(long)
	# @param rbl(list)
	# @param rbi(list)
	# @endif
	def list(self, name_cxt, how_many, rbl, rbi):
		bl, bi = name_cxt.list(how_many)

		for i in bl:
			rbl.append(bl)

		rbi.append(bi)
	

	#============================================================
	# interface of NamingContext
	#============================================================

	##
	# @if jp
	#  与えられた NameComponent の文字列表現を返す
	# @param name_list(CosNaming.NameComponentのリスト)
	# @else
	#  Get string representation of given NameComponent
	# @param name_list(list of CosNaming.NameComponent)
	# @endif
	def toString(self, name_list):
		if len(name_list) == 0:
			raise CosNaming.NamingContext.InvalidName

		slen = self.getNameLength(name_list)
		string_name = [""]
		self.nameToString(name_list, string_name, slen)

		return string_name


	##
	# @if jp
	#  与えられた文字列表現を NameComponent に分解する
	# @param sname(string)
	# @else
	#  Get NameComponent from gien string name representation
	# @param sname(string)
	# @endif
	def toName(self, sname):
		if not sname:
			raise CosNaming.NamingContext.InvalidName

		string_name = sname
		name_comps = []

		nc_length = 0
		nc_length = self.split(string_name, "/", name_comps)
		if not (nc_length > 0):
			raise CosNaming.NamingContext.InvalidName

		name_list = [CosNaming.NameComponent("","") for i in range(nc_length)]

		for i in range(nc_length):
			pos = string.rfind(name_comps[i][0:],".")
			if pos == -1:
				name_list[i].id   = name_comps[i]
				name_list[i].kind = ""
			else:
				name_list[i].id   = name_comps[i][0:pos]
				name_list[i].kind = name_comps[i][(pos+1):]

		return name_list


	##
	# @if jp 
	#  与えられた addre と string_name から URL表現を取得する
	# @param addr(string)
	# @param string_name(string)
	# @else
	#  Get URL representation from given addr and string_name
	# @param addr(string)
	# @param string_name(string)
	# @endif
	def toUrl(self, addr, string_name):
		return self._rootContext.to_url(addr, string_name)


	##
	# @if jp 
	#  与えられた文字列表現を resolve しオブジェクトを返す
	# @param string_name(string)
	# @else
	#  Resolve from name of string representation and get object 
	# @param string_name(string)
	# @endif
	def resolveStr(self, string_name):
		return self.resolve(self.toName(string_name))


	#============================================================
	# Find functions
	#============================================================

	##
	# @if jp
	#  名前をバインドまたは解決する
	# @param context(CosNaming.NameComponent)
	# @param name_list(CosNaming.NameComponentのリスト)
	# @param obj(CORBA::Object)
	# @else
	#  Bind of resolve the given name component
	# @param context(CosNaming.NameComponent)
	# @param name_list(list of CosNaming.NameComponent)
	# @param obj(CORBA::Object)
	# @endif
	def bindOrResolve(self, context, name_list, obj):
		try:
			context.bind_context(name_list, obj)
			return obj
		except CosNaming.NamingContext.AlreadyBound:
			obj = context.resolve(name_list)
			return obj
		return CORBA.Object._nil


	##
	# @if jp
	#  名前をバインドまたは解決する
	# @param context(CosNaming.NameComponent)
	# @param name_list(CosNaming.NameComponentのリスト)
	# @param new_context(CosNaming.NameComponent)
	# @else
	#  Bind of resolve the given name component
	# @endif
	def bindOrResolveContext(self, context, name_list, new_context=None):
		if new_context == None:
			new_cxt = self.newContext()
		else:
			new_cxt = new_context

		obj = self.bindOrResolve(context, name_list, new_cxt)
		return obj._narrow(CosNaming.NamingContext)


	##
	# @if jp
	#  ネームサーバの名前を取得する
	# @return string
	# @else
	#  Get the name of naming server
	# @return string
	# @endif
	def getNameServer(self):
		return self._nameServer


	##
	# @if jp
	#  ルートコンテキストを取得する
	# @return CosNaming.NameComponent
	# @else
	#  Get the root context
	# @return CosNaming.NameComponent
	# @endif
	def getRootContext(self):
		return self._rootContext


	##
	# @if jp 
	#  オブジェクトがネーミングコンテキストか判別する
	# @param obj(CORBA::Object)
	# @else
	#  Whether the object is NamingContext
	# @param obj(CORBA::Object)
	# @endif
	def objIsNamingContext(self, obj):
		nc = obj._narrow(CosNaming.NamingContext)
		if CORBA.is_nil(nc):
			return False
		else:
			return True


	##
	# @if jp
	#  与えられた名前がネーミングコンテキストかどうか
	# @param name_list(CosNaming.NameComponentのリスト)
	# @else
	#  Whether the given name component is NamingContext
	# @param name_list(list of CosNaming.NameComponent)
	# @endif
	def nameIsNamingContext(self, name_list):
		return self.objIsNamingContext(self.resolve(name_list))


	##
	# @if jp
	#  ネームコンポーネントの部分を返す
	# @param name_list(CosNaming.NameComponentのリスト)
	# @param begin(long)
	# @param end(long)
	# @else
	#  Get subset of given name component
	# @param name_list(list of CosNaming.NameComponent)
	# @param begin(long)
	# @param end(long)
	# @endif 
	def subName(self, name_list, begin, end = None):
		if end == None or end < 0:
			end = len(name_list) - 1

		sub_len = end - (begin -1)
		objId = ""
		kind  = ""
		
		sub_name = []
		for i in range(sub_len):
			sub_name.append(name_list[begin + i])

		return sub_name


	##
	# @if jp
	#  ネームコンポーネントの文字列表現を取得する
	# @param name_list(CosNaming.NameComponentのリスト)
	# @param string_name(string)
	# @param slen(long)
	# @else
	#  Get string representation of name component
	# @param name_list(list of CosNaming.NameComponent)
	# @param string_name(string)
	# @param slen(long)
	# @endif 
	def nameToString(self, name_list, string_name, slen):

		for i in range(len(name_list)):
			for id_ in name_list[i].id:
				if id_ == "/" or id_ == "." or id_ == "\\":
					string_name[0] += "\\"
				string_name[0] += id_

			if name_list[i].id == "" or name_list[i].kind != "":
				string_name[0] += "."

			for kind_ in name_list[i].kind:
				if kind_ == "/" or kind_ == "." or kind_ == "\\":
					string_name[0] += "\\"
				string_name[0] += kind_

			string_name[0] += "/"


	##
	# @if jp
	#  ネームコンポーネントの文字列表現時の文字長を取得する
	# @param name_list(CosNaming.NameComponentのリスト)
	# @else
	#  Get string length of the name component's string representation
	# @param name_list(list of CosNaming.NameComponent)
	# @endif
	def getNameLength(self, name_list):
		slen = 0

		for i in range(len(name_list)):
			for id_ in name_list[i].id:
				if id_ == "/" or id_ == "." or id_ == "\\":
					slen += 1
				slen += 1
			if name_list[i].id == "" or name_list[i].kind == "":
				slen += 1

			for kind_ in name_list[i].kind:
				if kind_ == "/" or kind_ == "." or kind_ == "\\":
					slen += 1
				slen += 1

			slen += 1

		return slen


	##
	# @if jp
	#  文字列の分割
	# @param input(string)
	# @param delimiter(string)
	# @param results(list of string)
	# @else
	#  Split of string
	# @param input(string)
	# @param delimiter(string)
	# @param results(list of string)
	# @endif
	def split(self, input, delimiter, results):
		delim_size = len(delimiter)
		found_pos = begin_pos = pre_pos = substr_size = 0

		if input[0:delim_size] == delimiter:
			begin_pos = pre_pos = delim_size

		while 1:
			found_pos = string.find(input[begin_pos:],delimiter)
			
			if found_pos == -1:
				results.append(input[pre_pos:])
				break

			if found_pos > 0 and input[found_pos - 1] == "\\":
				begin_pos += found_pos + delim_size
			else:
				substr_size = found_pos + (begin_pos - pre_pos)
				if substr_size > 0:
					results.append(input[pre_pos:(pre_pos+substr_size)])
				begin_pos += found_pos + delim_size
				pre_pos   = begin_pos

		return len(results)
