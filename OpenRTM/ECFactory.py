#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
 \file ECFactory.py
 \brief ExecutionContext Factory class
 \date $Date: 2007/04/13 16:06:22 $
 \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
 
 Copyright (C) 2007
     Task-intelligence Research Group,
     Intelligent Systems Research Institute,
     National Institute of
         Advanced Industrial Science and Technology (AIST), Japan
     All rights reserved.
 
"""


import string

import OpenRTM


def ECDelete(ec):
	del ec

	
class ECFactoryBase :
	
	def __init__(self):
		pass


	# This method should be implemented in subclasses
	def name(self):
		pass


	# This method should be implemented in subclasses
	def create(self):
		pass

	# This method should be implemented in subclasses
	def destroy(self, comp):
		pass


  
class ECFactoryPython(ECFactoryBase):
	
	def __init__(self, name, new_func, delete_func):
		"""
		 \brief constructor
		 \param name(string)
		 \param new_func(create function object)
		 \param delete_func(delete function object)
		"""
		ECFactoryBase.__init__(self)
		self._name   = name
		self._New    = new_func
		self._Delete = delete_func
		
		return


	def __del__(self):
		pass


	def name(self):
		return self._name


	def create(self):
		return self._New()


	def destroy(self, ec):
		self._Delete(ec)
    
