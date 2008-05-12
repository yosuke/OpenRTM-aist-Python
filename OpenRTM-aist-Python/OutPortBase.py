#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
  \file OutPortBase.py
  \brief OutPortBase base class
  \date $Date: 2007/09/19 $
  \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
 
  Copyright (C) 2003-2006
      Task-intelligence Research Group,
      Intelligent Systems Research Institute,
      National Institute of
          Advanced Industrial Science and Technology (AIST), Japan
      All rights reserved.
"""


class OutPortBase:
	"""
	\if jp
	\class OutPortBase
	\brief OutPort 基底クラス
	
	OutPort の実装である OutPort の基底クラス。
	
	OutPortBase と PublisherBase は一種の Observer パターンを形成している。
	OutPortBase の attach(), detach(), notify() および
	PublisherBase の push() は Observer パターンに関連したメソッドである。
	\else
	\class OutPortBase
	\brief Output port base class.
	The base class of OutPort<T> s which are implementations of OutPort  
	\endif
	"""


	def __init__(self, name):
		"""
		\if jp
		\brief OutPortBase クラスコンストラクタ
		   OutPortBase のクラスコンストラクタ。
		\param name(string)

		\else
		\brief A constructor of OutPortBase class.
		   Constructor of OutPortBase.
		\param name(string)
		\endif
		"""
		self._name = name
		self._publishers = []


	def __del__(self):
		"""
		\if jp
		\brief OutPortBase クラスデストラクタ
		
		OutPortBase のクラスデストラクタ。
		\else
		\brief A destructor of OutPortBase class.
		
		Destructor of OutPortBase.
		\endif
		"""
		pub_del=self.pub_del()
		for pub in self._publishers:
			pub_del(pub)


	# Functor to find Publisher by id
	class find_id:
		def __init__(self, id_):
			self._id = id_

		def __call__(self, pub):
			return self._id == pub.id

  
	# Functor to notify update to Publishers
	class pub_push:
		def __init__(self):
			pass

		def __call__(self, pub):
			pub.publisher.update()

  
	# Functor to delete Publishers
	class pub_del:
		def __init__(self):
			pass

		def __call__(self, pub):
			del pub


	def name(self):
		"""
		\if jp
		\brief OutPortの名前
		
		OutPortの名前を返す。
		\else
		\brief OutPort's name
		
		This operation returns OutPort's name
		\endif
		"""
		return self._name


	def attach(self, id_, publisher):
		"""
		\if jp
		\brief Publisherの追加
		   Publisherを追加する。
		\param id_(string)
		\param publisher(OpenRTM.PublisherBase)
		\else
		\brief Attach a publisher
		   Attach a publisher to observe OutPort.
		\param id_(string)
		\param publisher(OpenRTM.PublisherBase)
		\endif
		"""
		self.attach_back(id_, publisher)


	def attach_front(self, id_, publisher):
		"""
		\if jp
		\brief Publisherの追加
		   Publisherをリストの先頭に追加する。
		\param id_(string)
		\param publisher(OpenRTM.PublisherBase)
		\else
		\brief Attach a publisher
		   Attach a publisher to the head of the Publisher list.
		\param id_(string)
		\param publisher(OpenRTM.PublisherBase)
		\endif
		"""
		self._publishers.insert(0, self.Publisher(id_, publisher))


	def attach_back(self, id_, publisher):
		"""
		\if jp
		\brief Publisherの追加
		   Publisherをリストの最後尾に追加する。
		\param id_(string)
		\param publisher(OpenRTM.PublisherBase)
		\else
		\brief Attach a publisher
		   Attach a publisher to the taile of the Publisher list.
		\param id_(string)
		\param publisher(OpenRTM.PublisherBase)
		\endif
		"""
		self._publishers.append(self.Publisher(id_, publisher))


	def detach(self, id_):
		"""
		\if jp
		\brief Publisherの削除
		   Publisherを削除する。
		\param id_(string)
		\else
		\brief Detach a publisher
		   Detach a publisher to observe OutPort.
		\param id_(string)
		\endif
		"""
		func = self.find_id(id_)
		index = -1

		for i in range(len(self._publishers)):
			if func(self._publishers[i]):
				index = i
				break
		if index < 0:
			return None

		pub = self._publishers[index].publisher
		del self._publishers[index]
		return pub


	def notify(self):
		"""
		\if jp
		\brief 更新の通知
		
		Publisherにデータの更新を通知する。
		\else
		\brief Notify data update
		
		This operation notify data update to Publishers
		\endif
		"""
		func = self.pub_push()
		for pub in self._publishers:
			func(pub)


	class Publisher:
		"""
		\brief Publisher struct
		"""
		def __init__(self, id_, publisher_):
			self.id = id_
			self.publisher = publisher_


