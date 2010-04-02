@echo off
rem Copyright (C) 2010
rem     Shinji Kurihara
rem     Intelligent Systems Research Institute,
rem     National Institute of
rem         Advanced Industrial Science and Technology (AIST), Japan
rem     All rights reserved.
rtcprof.py %* > rtcprof_tmp.bat
rtcprof_tmp
del rtcprof_tmp.bat
