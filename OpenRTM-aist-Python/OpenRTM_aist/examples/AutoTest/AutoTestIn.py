#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
 \file AutoTestIn.py
 \brief ModuleDescription
 \date $Date$


"""
import sys
import string
import time
sys.path.append(".")

# Import RTM module
import OpenRTM_aist
import RTC
import math
import AutoTest, AutoTest__POA
from decimal import *
import os.path

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
AutoTestIn_spec = ["implementation_id", "AutoTestIn", 
		 "type_name",         "AutoTestIn", 
		 "description",       "ModuleDescription", 
		 "version",           "1.0.0", 
		 "vendor",            "HarumiMiyamoto", 
		 "category",          "example", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 "exec_cxt.periodic.rate", "1.0",
		 ""]
# </rtc-template>


# Class implementing IDL interface MyService(MyService.idl)
class MyServiceSVC_impl(AutoTest__POA.MyService):
    def __init__(self):
        self._echoList = []
        self._valueList = []
        self._value = 0
	self.__echo_msg= ""

    def __del__(self):
        pass

    def echo(self, msg):
        OpenRTM_aist.CORBA_SeqUtil.push_back(self._echoList, msg)
	self.__echo_msg = msg
	return msg

    def get_echo(self):
        
        echomsg = self.__echo_msg
        return echomsg

class AutoTestIn(OpenRTM_aist.DataFlowComponentBase):
	
	"""
	\class AutoTestIn
	\brief ModuleDescription
	
	"""
	def __init__(self, manager):
		"""
		\brief constructor
		\param manager Maneger Object
		"""
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		self._d_dp_vIn = RTC.TimedFloat(RTC.Time(0,0),0)
		self._d_dp_vSeqIn = RTC.TimedFloatSeq(RTC.Time(0,0),[])

		self._InIn = OpenRTM_aist.InPort("in", self._d_dp_vIn, OpenRTM_aist.RingBuffer(8))
		self._SeqInIn = OpenRTM_aist.InPort("seqin", self._d_dp_vSeqIn, OpenRTM_aist.RingBuffer(8))
		

		# Set InPort buffers
		self.registerInPort("in",self._InIn)
		self.registerInPort("seqin",self._SeqInIn)
		
		# Set OutPort buffers
		self._MyServicePort = OpenRTM_aist.CorbaPort("MyService")
		#self._myservice0_var = MyService_i()
		
		# initialization of Provider
		self._myservice0_var = MyServiceSVC_impl()

		# Set service provider to Ports
		self._MyServicePort.registerProvider("myservice0", "MyService", self._myservice0_var)
		
		# Set CORBA Service Ports
		self.registerPort(self._MyServicePort)
		self._cnt=0
		self._flag=0

	def onInitialize(self):
		# Bind variables and configuration variable
		return RTC.RTC_OK

	
	def onActivated(self, ec_id):
		self._file=open('received-data','w')
		return RTC.RTC_OK
	
	def onDeactivated(self, ec_id):	
            self._file.close()
            return RTC.RTC_OK
	
	def onExecute(self, ec_id):

		if (self._InIn.isNew() and self._SeqInIn.isNew()):
                    floatdata = self._InIn.read()
                    seqfloatdata = self._SeqInIn.read()
                        
                    fdata = str(float(floatdata.data)) + "\n"

                    self._file.write(fdata)
                    
                    sdata = str(round(seqfloatdata.data[0],2)) + " "+ str(round(seqfloatdata.data[1],2)) + " " + str(round(seqfloatdata.data[2],2)) + " " + str(round(seqfloatdata.data[3],2)) + " " + str(round(seqfloatdata.data[4],2)) + "\n"
                    self._file.write(sdata)


                    edata=self._myservice0_var.get_echo() + "\n"
                    self._file.write(edata)
                    return RTC.RTC_OK
		else:
                    return RTC.RTC_OK
	



def MyModuleInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=AutoTestIn_spec)
    manager.registerFactory(profile,
                            AutoTestIn,
                            OpenRTM_aist.Delete)

    # Create a component
    comp = manager.createComponent("AutoTestIn")



def main():
	mgr = OpenRTM_aist.Manager.init(len(sys.argv), sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

