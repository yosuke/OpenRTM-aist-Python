#!/usr/bin/env python
# -*- Python -*-

orb="omniORB"

#
#  @file rtm-naming.py
#  @brief OpenRTM-aist name server launcher
#  @date $Date: 2007/10/25 $
#  @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
# 
#  Copyright (C) 2003-2005
#      Task-intelligence Research Group,
#      Intelligent Systems Research Institute,
#      National Institute of
#          Advanced Industrial Science and Technology (AIST), Japan
#      All rights reserved.
# 

import sys,os,platform

sysinfo = platform.uname()
hostname=sysinfo[1]
currdir=os.getcwd()
port=2809
pla=sys.platform

if pla == "win32":
    rmcmd = "del /F "
else:
    rmcmd = "rm -f "

def usage():
    print "Usage: python rtm-naming.py port_number"


def omniname():
	global hostname, sysinfo, currdir, port, rmcmd
	log_fname = "omninames-"+str(hostname)+".log"
	if os.path.exists(log_fname):
		cmd = rmcmd+log_fname
		os.system(cmd)
	bak_fname = "omninames-"+str(hostname)+".bak"
	if os.path.exists(bak_fname):
		cmd = rmcmd+bak_fname
		os.system(cmd)
	print "Starting omniORB omniNames: ", hostname,":", port
	cmd = "omniNames -start "+str(port)+" -logdir \""+str(currdir)+"\" &"
	print cmd
	os.system(cmd)


if __name__ == "__main__":
    try:
        if len(sys.argv) == 2:
            port = int(sys.argv[1])

            if sys.argv[1] == "-u" or sys.argv[1] == "-h" or sys.argv[1] == "--help":
                usage()
    except:
        usage()
        sys.exit(1)
        
    omniname()
