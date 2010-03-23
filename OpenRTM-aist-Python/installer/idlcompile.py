#!/usr/bin/env python
#
# @brief IDL Compile for OpenRTM-aist-Python
#
# Target Python version 2.4, 2.5, 2.6
#

import os, glob, sys, _winreg

##--------------------------------------------------------------------
## commandline argument
## argvs[1]: Python version (2.4, 2.5, 2.6)
##--------------------------------------------------------------------
argvs = sys.argv
argc = len(argvs)
inst_ver = "all"

if argc > 1:
    inst_ver = str(argvs[1])


##--------------------------------------------------------------------
## Install check and IDL Compile
##--------------------------------------------------------------------
def idl_compile(chk_ver, reg_key):
  reg_root = _winreg.HKEY_LOCAL_MACHINE

  try:
    InstallPath = None
    index = 0

    ## Get InstallPath
    reg_hdl = _winreg.OpenKey(reg_root, reg_key)
    reg_data = _winreg.EnumValue(reg_hdl, index)
    InstallPath = reg_data[1]
    _winreg.CloseKey(reg_hdl)

    if InstallPath.rfind("\\") != (len(InstallPath) -1):
      InstallPath += "\\"

    curr_dir = InstallPath + "Lib\site-packages\OpenRTM_aist\RTM_IDL"
    os.chdir(curr_dir)

    ## make idl list
    idl_cmd = InstallPath + "omniidl.exe -bpython"
    idl_list = glob.glob("*.idl")
    idl_cnt = len(idl_list)
    for i in range(idl_cnt):
      idl_cmd += " " + idl_list[i]

    ## idl compile
    os.system(idl_cmd)
    return True

  except EnvironmentError:
    return False

  return False


##--------------------------------------------------------------------
## Python 2.4
##--------------------------------------------------------------------
if (inst_ver == "all") or (inst_ver == "2.4"):
  py_ver = "2.4"
  py_key = "SOFTWARE\\Python\\PythonCore\\2.4\\InstallPath"
  ret = idl_compile(py_ver, py_key)
  if ret == False:
    print "Python %s Not Installed." % py_ver


##--------------------------------------------------------------------
## Python 2.5
##--------------------------------------------------------------------
if (inst_ver == "all") or (inst_ver == "2.5"):
  py_ver = "2.5"
  py_key = "SOFTWARE\\Python\\PythonCore\\2.5\\InstallPath"
  ret = idl_compile(py_ver, py_key)
  if ret == False:
    print "Python %s Not Installed." % py_ver


##--------------------------------------------------------------------
## Python 2.6
##--------------------------------------------------------------------
if (inst_ver == "all") or (inst_ver == "2.6"):
  py_ver = "2.6"
  py_key = "SOFTWARE\\Python\\PythonCore\\2.6\\InstallPath"
  ret = idl_compile(py_ver, py_key)
  if ret == False:
    print "Python %s Not Installed." % py_ver

