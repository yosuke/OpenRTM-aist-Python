#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# \file DefaultConfiguration.py
# \brief RTC manager default configuration
# \date $Date: $
# \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.



import OpenRTM

##
# @if jp
# @brief Manager 用 デフォルト・コンフィギュレーション
#
# Managerクラス用デフォルトコンフィギュレーション。
#
# @since 0.4.0
#
# @else
# @endif
default_config =["config.version",         OpenRTM.openrtm_version,
                 "openrtm.version",        OpenRTM.openrtm_name,
                 "manager.name",           "manager",
                 "manager.pid",            "",
                 "os.name",                "",
                 "os.release",             "",
                 "os.version",             "",
                 "os.arch",                "",
                 "os.hostname",            "",
                 "logger.enable",          "YES",
                 "logger.file_name",       "./rtc%p.log",
                 "logger.date_format",     "%b %d %H:%M:%S",
                 "logger.log_level",       "NORMAL",
                 "logger.stream_lock",     "NO",
                 "logger.master_logger",   "",
                 "module.conf_path",       "",
                 "module.load_path",       "",
                 "naming.enable",          "YES",
                 "naming.type",            "corba",
                 "naming.formats",         "%h.host/%n.rtc",
                 "naming.update.enable",   "YES",
                 "naming.update.interval", "10.0",
                 "timer.enable",           "YES",
                 "timer.tick",             "0.1",
                 "corba.args",             "",
                 "corba.endpoint",         "",
                 "corba.id",               OpenRTM.corba_name,
                 "corba.name_servers",     "",
                 "exec_cxt.periodic.type", "PeriodicExecutionContext",
                 "exec_cxt.periodic.rate", "1000",
                 "exec_cxt.evdriven.type", "EventDrivenExecutionContext",
                 ""]
