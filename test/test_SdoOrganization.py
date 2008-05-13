#!/usr/bin/env python
# -*- Python -*-

#
#  \file test_SdoOrganization.py
#  \brief test for SDO Organization implementation class
#  \date $Date: 2007/09/12 $
#  \author Shinji Kurihara
# 
#  Copyright (C) 2006
#      Task-intelligence Research Group,
#      Intelligent Systems Research Institute,
#      National Institute of
#          Advanced Industrial Science and Technology (AIST), Japan
#      All rights reserved.
# 

import omniORB.any
import CORBA
import threading

import sys
sys.path.insert(1,"../")

import unittest
import OpenRTM
import SDOPackage, SDOPackage__POA

from SdoOrganization import *



class TestOrganization_impl(unittest.TestCase):
	def setUp(self):
		self.org = Organization_impl()

	def test_get_organization_id(self):
		print self.org.get_organization_id()
	
	def test_get_organization_property(self):
		nv_list = [SDOPackage.NameValue("test", 100)]
		self.org.set_organization_property(SDOPackage.OrganizationProperty(nv_list))
		self.assertEqual(self.org.get_organization_property().properties[0].name, "test")
		self.org.remove_organization_property("test")
		ret_val = self.org.get_organization_property()
		self.assertEqual(len(ret_val.properties), 0)
			
		self.assertRaises(SDOPackage.InvalidParameter, self.org.remove_organization_property, None )

	def test_get_organization_property_value(self):
		self.org.set_organization_property_value("test", 100)
		self.assertRaises(SDOPackage.InvalidParameter, self.org.set_organization_property_value, None, None )

		val = omniORB.any.from_any(self.org.get_organization_property_value("test"))
		self.assertEqual(val, 100)
		# Failure pattern
		# because get_organization_property_value() returns value of CORBA.Any type.
		# self.assertEqual(self.org.get_organization_property_value("test"), 100)
		self.assertRaises(SDOPackage.InvalidParameter, self.org.get_organization_property_value, "aaa" )
		self.assertRaises(SDOPackage.InvalidParameter, self.org.get_organization_property_value, None )

		self.assertRaises(SDOPackage.InvalidParameter, self.org.set_organization_property_value, None, "aaa" )
		

	def test_get_owner(self):
		# Failure pattern
		#self.org.set_owner(None)
		self.assertEqual(self.org.get_owner(),None)
		self.assertRaises(SDOPackage.InvalidParameter, self.org.set_owner, None )

	class sdo_test(OpenRTM.RTObject_impl):
		def __init__(self):
			self._orb = CORBA.ORB_init()
			self._poa = self._orb.resolve_initial_references("RootPOA")
			OpenRTM.RTObject_impl.__init__(self, orb=self._orb, poa=self._poa)


	def test_get_members(self):
		# Failure pattern
		#self.org.set_members([])
		self.assertEqual(self.org.get_members(),[])
		member = self.sdo_test()
		member.setInstanceName("test0")
		self.org.set_members([member])
		member = self.sdo_test()
		member.setInstanceName("test1")
		self.org.add_members([member])
		self.assertEqual(len(self.org.get_members()),2)
		self.org.remove_member("test1")
		self.assertEqual(len(self.org.get_members()),1)

		self.assertRaises(SDOPackage.InvalidParameter, self.org.set_members, None )
		self.assertRaises(SDOPackage.InvalidParameter, self.org.add_members, None )
		self.assertRaises(SDOPackage.InvalidParameter, self.org.remove_member, None )


	def test_get_dependency(self):
		self.org.set_dependency(SDOPackage.OWN)
		self.assertEqual(self.org.get_dependency(), SDOPackage.OWN)

		self.assertRaises(SDOPackage.InvalidParameter, self.org.set_dependency, None )


############### test #################
if __name__ == '__main__':
        unittest.main()
