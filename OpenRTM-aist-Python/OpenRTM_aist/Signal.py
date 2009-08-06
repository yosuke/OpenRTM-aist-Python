#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file  SignalPosix.py
# @brief RT-Middleware Service interface
# @date  $Date$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2008
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.
#

import signal

class SignalAction:
    def __init__(self, handle=None, signum=None):
        if handle and signum:
            self._handle = handle
            self._signum = signum
            signal.signal(self._signum, self._handle)
        else:
            self._handle = None
            self._signum = 0
        return


    def __del__(self):
        signal.signal(signal.SIG_DFL, self._handle)
