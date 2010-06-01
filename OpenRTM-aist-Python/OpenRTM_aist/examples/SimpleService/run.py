#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

#
# @file run.py
# @brief ExtTrigger example startup script
# @date $Date: 2007/10/26 $
#
# Copyright (c) 2003-2007 Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#          Task-intelligence Research Group,
#          Intelligent System Research Institute,
#          National Institute of Industrial Science (AIST), Japan
#          All rights reserved.
#

import sys,os,platform
import time
import commands

nsport="2809"
sysinfo = platform.uname()
hostname= sysinfo[1]
plat=sys.platform

if plat == "win32":
    os.system("rd /S /Q SimpleService")
    os.system("rd /S /Q SimpleService__POA")
    os.system("omniidl.exe -bpython MyService.idl")
    os.system("start python ..\\..\\..\\bin\\rtm-naming.py")
    os.system("start python MyServiceConsumer.py")
    os.system("start python MyServiceProvider.py")
    time.sleep(3)
    os.system("python Connector.py")

else:
    os.system('rm -rf SimpleService*')
    os.system('omniidl -bpython MyService.idl')
    status,term=commands.getstatusoutput("which kterm")
    if status != 0:
        status,term=commands.getstatusoutput("which xterm")

    if status != 0:
        status,term=commands.getstatusoutput("which uxterm")

    if status != 0:
        status,term=commands.getstatusoutput("which gnome-terminal")

    if status != 0:
        print "No terminal program (kterm/xterm/gnome-terminal) exists."
        sys.exit(0)

    path = None
    for p in sys.path:
        if os.path.exists(os.path.join(p,"OpenRTM_aist")):
            path = os.path.join(p,"OpenRTM_aist","utils","rtm-naming")
            break
    if path is None:
        print "rtm-naming directory not exist."
        sys.exit(0)

    os.system('python %s/rtm-naming.py &'%path)
    os.system('%s -e python MyServiceConsumer.py &'%term)
    os.system('%s -e python MyServiceProvider.py &'%term)
    time.sleep(3)
    os.system("python Connector.py")
