#!/usr/bin/env python
# -*- coding: euc-jp -*-

#
#  \file SdoService.py
#  \brief SDO Service administration class
#  \date $Date: 2007/09/12 $
#  \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
# 
#  Copyright (C) 2006
#      Task-intelligence Research Group,
#      Intelligent Systems Research Institute,
#      National Institute of
#          Advanced Industrial Science and Technology (AIST), Japan
#      All rights reserved.
# 


import SDOPackage, SDOPackage__POA

class SDOServiceProfile:
	def __init__(self, id_=None, type_=None):
		"""
		 \param id_(string)
		 \param type_(string)
		"""
		if id_ == None:
			self.id = ""
		else:
			self.id = id_

		if type_ == None:
			self.type = ""
		else:
			self.type = type_
			
		self.interfaceType = ""
		self.idlDefinition = ""
		self.properties = []
		self.serviceRef = None
		

	def getProfile(self):
		return self
    
	def setName(self, id_):
		"""
		 \if jp
		 \brief ServiceProfile.id をセットする
		 \param id_(string)
		 \else
		 \brief Setting ServiceProfile.id
		 \param id_(string)
		 \endif
		"""
		self.id = id_


	def getName(self):
		"""
		 \if jp
		 \brief ServiceProfile.id を取得
		 \else
		 \brief Getting ServiceProfile.id
		 \endif
		"""
		return self.id

	def setInterfaceType(self, interfaceType):
		"""
		 \if jp
		 \brief RTCServiceProfile.interfaceType をセットする
		 \param interfaceType(string)
		 \else
		 \brief Setting RTCServiceProfile.interfaceType
		 \param interfaceType(string)
		 \endif
		"""
		self.interfaceType = interfaceType
    

	def getInterfaceType(self):
		"""
		 \if jp
		 \brief RTCServiceProfile.interfaceType を取得する
		 \else
		 \brief Getting RTCServiceProfile.interfaceType
		 \endif
		"""
		return self.interfaceType


	def setIdlDefinition(self, idlDefinition):
		"""
		 \if jp
		 \brief RTCServiceProfile.idlDefinition をセットする
		 \param idlDefinition(string)
		 \else
		 \brief Setting RTCServiceProfile.idlDefnition
		 \param idlDefinition(string)
		 \endif
		"""
		self.idlDefinition = idlDefinition

    
	def getIdlDefinition(self):
		"""
		 \if jp
		 \brief RTCServiceProfile.idlDefinition を取得する
		 \else
		 \brief Getting RTCServiceProfile.idlDefnition
		 \endif
		"""
		return self.idlDefinition
    

	def setProperties(self, properties):
		"""
		 \if jp
		 \brief RTCServiceProfile.properties をセットする
		 \else
		 \brief Setting RTCServiceProfile.properties
		 \endif
		"""
		self.properties = properties

    
	def getProperties(self):
		"""
		 \if jp
		 \brief RTCServiceProfile.properties を取得する
		 \else
		 \brief Getting RTCServiceProfile.properties
		 \endif
		"""
		return self.properties

    
	# bool addProperty(char name, CORBA::Any data);
    
	def setServiceRef(self, serviceRef):
		"""
		 \if jp
		 \brief RTCServiceProfile.serviceRef をセットする
		 \else
		 \brief Setting RTCServiceProfile.serviceRef
		 \endif
		"""
		self.serviceRef = serviceRef

    
	def getServiceRef(self):
		"""
		 \if jp
		 \brief RTCServiceProfile.serviceRef を取得する
		 \else
		 \brief Getting RTCServiceProfile.serviceRef
		 \endif
		"""
		return self.serviceRef
  
