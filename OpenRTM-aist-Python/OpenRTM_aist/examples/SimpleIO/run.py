#!/usr/bin/env python
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
    os.system("start python ..\\..\\..\\bin\\rtm-naming.py")
    os.system("start python ConsoleIn.py")
    os.system("start python Consoleout.py")
    time.sleep(3)
    os.system("python Connector.py")

else:
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
            path = os.path.join(p,"OpenRTM_aist","rtm-naming")
            break
    if path is None:
        print "rtm-naming directory not exist."
        sys.exit(0)

    os.system('python %s/rtm-naming.py'%path)
    os.system('%s -e python ConsoleIn.py &'%term)
    os.system('%s -e python ConsoleOut.py &'%term)
    time.sleep(3)
    os.system("python Connector.py")
