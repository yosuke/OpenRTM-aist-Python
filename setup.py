#!/usr/bin/env python

import os,os.path,sys

if os.sep == '/':
	sitedir = os.path.join("lib", "python" + sys.version[:3], "site-packages")
elif os.sep == ':':
	sitedir = os.path.join("lib", "site-packages")
else:
	if sys.version_info[0:3] >= (2, 2, 0):
		sitedir = os.path.join("lib", "site-packages")
	else:
		sitedir = "."


from distutils.core import setup
from distutils.sysconfig import get_python_lib
setup(name = "OpenRTM-aist-Python",
      version = "0.4.1",
      description = "Python modules for OpenRTM-aist-0.4.1",
      author = "Shinji Kurihara",
      author_email = "shinji.kurihara@aist.go.jp",
      url = "http://www.is.aist.go.jp/rt/OpenRTM-aist/html/",
      long_description = "OpenRTM-aist is a reference implementation of RT-Middleware,\
which is now under standardization process in OMG (Object Management Group).\
OpenRTM-aist is being developed and distributed by\
Task Intelligence Research Group,\
Intelligent Systems Research Institute,\
National Institute of Advanced Industrial Science and Technology (AIST), Japan.\
Please see http://www.is.aist.go.jp/rt/OpenRTM-aist/html/ for more detail.",
      licence = "LGPL",
      packages = ["OpenRTM",
                  "OpenRTM.RTM_IDL",
		  "OpenRTM.RTM_IDL.RTC",
		  "OpenRTM.RTM_IDL.RTC__POA",
		  "OpenRTM.RTM_IDL.SDOPackage",
		  "OpenRTM.RTM_IDL.SDOPackage__POA",
		  "OpenRTM.examples.ConfigSample",
		  "OpenRTM.examples.ExtTrigger",
		  "OpenRTM.examples.SeqIO",
		  "OpenRTM.examples.SimpleIO",
		  "OpenRTM.examples.SimpleService._GlobalIDL",
		  "OpenRTM.examples.SimpleService._GlobalIDL__POA",
		  "OpenRTM.examples.SimpleService",
		  "OpenRTM.examples.Slider_and_Motor",
		  "OpenRTM.examples.MobileRobotCanvas",
		  "OpenRTM.examples.TkJoyStick",
		  "OpenRTM.rtc-template",
		  "OpenRTM.rtm-naming"],
      data_files = [(sitedir,['OpenRTM.pth']),
                    (os.path.join(sitedir,'OpenRTM/examples/ConfigSample'),['OpenRTM/examples/ConfigSample/rtc.conf']),
                    (os.path.join(sitedir,'OpenRTM/examples/ConfigSample'),['OpenRTM/examples/ConfigSample/configsample.conf']),
                    (os.path.join(sitedir,'OpenRTM/examples/ExtTrigger'),['OpenRTM/examples/ExtTrigger/rtc.conf']),
                    (os.path.join(sitedir,'OpenRTM/examples/SimpleIO'),['OpenRTM/examples/SimpleIO/rtc.conf']),
                    (os.path.join(sitedir,'OpenRTM/examples/SeqIO'),['OpenRTM/examples/SeqIO/rtc.conf']),
                    (os.path.join(sitedir,'OpenRTM/examples/SimpleService'),['OpenRTM/examples/SimpleService/rtc.conf']),
                    (os.path.join(sitedir,'OpenRTM/examples/Slider_and_Motor'),['OpenRTM/examples/Slider_and_Motor/rtc.conf']),
                    (os.path.join(sitedir,'OpenRTM/examples/MobileRobotCanvas'),['OpenRTM/examples/MobileRobotCanvas/rtc.conf']),
                    (os.path.join(sitedir,'OpenRTM/examples/TkJoyStick'),['OpenRTM/examples/TkJoyStick/rtc.conf']),
                    (os.path.join(sitedir,'OpenRTM/RTM_IDL'),['OpenRTM/RTM_IDL/OpenRTM.pth']),
                    (os.path.join(sitedir,'OpenRTM/RTM_IDL'),['OpenRTM/RTM_IDL/BasicDataType.idl']),
                    (os.path.join(sitedir,'OpenRTM/RTM_IDL'),['OpenRTM/RTM_IDL/DataPort.idl']),
                    (os.path.join(sitedir,'OpenRTM/RTM_IDL'),['OpenRTM/RTM_IDL/OpenRTM.idl']),
                    (os.path.join(sitedir,'OpenRTM/RTM_IDL'),['OpenRTM/RTM_IDL/RTC.idl']),
                    (os.path.join(sitedir,'OpenRTM/RTM_IDL'),['OpenRTM/RTM_IDL/SDOPackage.idl'])])
