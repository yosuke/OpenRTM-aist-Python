#!/usr/bin/env python

import os,os.path
import sys
import string
import commands
import glob
from distutils import core
from distutils import cmd
from distutils import log
from distutils import util
from distutils import dir_util
from distutils import errors
from distutils import version
from distutils.command.build import build
from distutils.command.sdist import sdist


core.DEBUG = False

g_os = None
g_qkc_option = "-u"

if os.sep == '/':
  g_os = "unix"
  if sys.version_info[0:3] >= (2, 6, 0):
    #sitedir = os.path.join("lib", "python" + sys.version[:3], "dist-packages")
    sitedir = os.path.join("lib", "python" + sys.version[:3], "site-packages")
  elif sys.version_info[0:3] >= (2, 2, 0):
    sitedir = os.path.join("lib", "python" + sys.version[:3], "site-packages")
elif os.sep == ':':
  sitedir = os.path.join("lib", "site-packages")
elif os.sep == '\\':
  print "os: win32"
  g_os = "win32"
  sitedir = os.path.join("lib", "site-packages")
else:
  if sys.version_info[0:3] >= (2, 2, 0):
    sitedir = os.path.join("lib", "site-packages")
  else:
    sitedir = "."


def compile_idl(cmd, pars, files):
  """
  Put together command line for python stubs generation.
  """
  global g_os
  cmdline = cmd +' '+ string.join(pars) +' '+string.join(files)
  if g_os == "win32":
    os.system(cmdline)
    return

  log.info(cmdline)
  status, output = commands.getstatusoutput(cmdline)
  log.info(output)
  if status != 0:
    raise errors.DistutilsExecError("Return status of %s is %d" %
            (cmd, status))


def gen_idl_name(dir, name):
  """
  Generate name of idl file from directory prefix and IDL module name.
  """
  full_name = '"'+os.path.join(dir, name + ".idl")+'"'
  return full_name


class Build_idl (cmd.Command):
  """
  This class realizes a subcommand of build command and is used for building
  IDL stubs.
  """

  description = "Generate python stubs from IDL files"

  user_options = [("omniidl=", "i", "omniidl program used to build stubs"),
                  ("idldir=",  "d", "directory where IDL files reside")]

  def initialize_options(self):
    self.idldir  = None
    self.omniidl = None
    self.omniidl_params = ["-bpython"]

  def finalize_options(self):
    if not self.omniidl:
      self.omniidl = "omniidl"
    if not self.idldir:
      self.idldir = os.path.join(os.getcwd(),"OpenRTM_aist","RTM_IDL")

  def run(self):
    #self.omniidl_params.append("-Wbpackage=OpenRTM_aist.RTM_IDL")
    self.omniidl_params.append("-COpenRTM_aist/RTM_IDL")
    self.omniidl_params.append("-IOpenRTM_aist/RTM_IDL")
    modules = ["BasicDataType", "DataPort", "ExtendedDataTypes",
               "InterfaceDataTypes", "Manager", "OpenRTM", "RTC",
               "SDOPackage"]
    util.execute(compile_idl,
                 (self.omniidl, self.omniidl_params,
                  [ gen_idl_name(self.idldir, module) for module in modules ]),
                 "Generating python stubs from IDL files")

    # for SimpleService
    self.idldir = os.path.join(os.getcwd(),"OpenRTM_aist","examples","SimpleService")
    self.omniidl_params[-2]=("-COpenRTM_aist/examples/SimpleService")
    self.omniidl_params[-1]=("-IOpenRTM_aist/examples/SimpleService")
    modules = ["MyService"]
    util.execute(compile_idl,
                 (self.omniidl, self.omniidl_params,
                  [ gen_idl_name(self.idldir, module) for module in modules ]),
                 "Generating python sample stubs from IDL files")

    # for AutoTest
    self.idldir = os.path.join(os.getcwd(),"OpenRTM_aist","examples","AutoTest")
    self.omniidl_params[-2]=("-COpenRTM_aist/examples/AutoTest")
    self.omniidl_params[-1]=("-IOpenRTM_aist/examples/AutoTest")
    modules = ["AutoTestService"]
    util.execute(compile_idl,
                 (self.omniidl, self.omniidl_params,
                  [ gen_idl_name(self.idldir, module) for module in modules ]),
                 "Generating python sample stubs from IDL files")


class Build_doc(cmd.Command):
  """
  This class realizes a subcommand of build command and is used for building
  document by doxygen.
  """

  description = "Generate document by doxygen"

  def initialize_options(self):
    pass

  def finalize_options(self):
    pass

  def run(self):
    global g_os

    if g_os == "unix":
      curr_dir = os.getcwd()
      docs_dir = os.path.join(os.getcwd(), 'OpenRTM_aist', 'docs')
      os.chdir(docs_dir)
      os.system("make")
      os.chdir(curr_dir)


class Build (build):
  """
  This is here just to override default sub_commands list of build class.
  We added 'build_idl' item.
  """
  def has_pure_modules (self):
    return self.distribution.has_pure_modules()

  def has_c_libraries (self):
    return self.distribution.has_c_libraries()

  def has_ext_modules (self):
    return self.distribution.has_ext_modules()

  def has_scripts (self):
    return self.distribution.has_scripts()

  def has_idl_files (self):
    return True

  def has_doc_files (self):
    return True

  sub_commands = [('build_doc',     has_doc_files),
                  ('build_idl',     has_idl_files),
                  ('build_py',      has_pure_modules),
                  ('build_clib',    has_c_libraries),
                  ('build_ext',     has_ext_modules),
                  ('build_scripts', has_scripts)]

class OtherSetupForSdist(sdist):

  def make_distribution (self):
    """Create the source distribution(s).  First, we create the release
    tree with 'make_release_tree()'; then, we create all required
    archive files (according to 'self.formats') from the release tree.
    Finally, we clean up by blowing away the release tree (unless
    'self.keep_temp' is true).  The list of archive files created is
    stored so it can be retrieved later by 'get_archive_files()'.
    """
    global g_os
    global g_qkc_option
    print "make_distribution"
    # Don't warn about missing meta-data here -- should be (and is!)
    # done elsewhere.
    base_dir = self.distribution.get_fullname()
    base_name = os.path.join(self.dist_dir, base_dir)

    self.make_release_tree(base_dir, self.filelist.files)
    archive_files = []              # remember names of files we create

    if g_os == "unix":
      curr_dir = os.getcwd()
      cmd_dir = os.path.join(os.getcwd(), pkg_name+'-'+pkg_version)
      os.chdir(cmd_dir)
      cmd_ = "find . -name \"*\" | xargs qkc %s" % g_qkc_option
      os.system(cmd_)
      os.chdir(curr_dir)
          
    for fmt in self.formats:
      file = self.make_archive(base_name, fmt, base_dir=base_dir)
      archive_files.append(file)
      self.distribution.dist_files.append(('sdist', '', file))

    self.archive_files = archive_files

    if not self.keep_temp:
      dir_util.remove_tree(base_dir, dry_run=self.dry_run)


############################### data for setup() ###########################################
unix_packages = ["OpenRTM_aist",
                 "OpenRTM_aist.RTM_IDL",
                 "OpenRTM_aist.RTM_IDL.device_interfaces",
                 "OpenRTM_aist.utils",
                 "OpenRTM_aist.utils.rtcd",
                 "OpenRTM_aist.utils.rtcprof",
                 "OpenRTM_aist.utils.rtc-template",
                 "OpenRTM_aist.utils.rtm-naming"]

win32_packages = ["OpenRTM_aist",
                  "OpenRTM_aist.RTM_IDL",
                  "OpenRTM_aist.examples.AutoControl",
                  "OpenRTM_aist.examples.Composite",
                  "OpenRTM_aist.examples.ConfigSample",
                  "OpenRTM_aist.examples.ExtTrigger",
                  "OpenRTM_aist.examples.MobileRobotCanvas",
                  "OpenRTM_aist.examples.NXTRTC",
                  "OpenRTM_aist.examples.SeqIO",
                  "OpenRTM_aist.examples.SimpleIO",
                  "OpenRTM_aist.examples.SimpleService",
                  "OpenRTM_aist.examples.Slider_and_Motor",
                  "OpenRTM_aist.examples.Templates",
                  "OpenRTM_aist.examples.TkJoyStick",
                  "OpenRTM_aist.examples.TkLRFViewer",
                  "OpenRTM_aist.utils",
                  "OpenRTM_aist.utils.rtcd",
                  "OpenRTM_aist.utils.rtcprof",
                  "OpenRTM_aist.utils.rtc-template",
                  "OpenRTM_aist.utils.rtm-naming"]

unix_data_files = [(sitedir,['OpenRTM-aist.pth'])]

idl_files= glob.glob(os.path.join('OpenRTM_aist',
                                  'RTM_IDL',
                                  '*.idl'))

device_if_idl_files= glob.glob(os.path.join('OpenRTM_aist',
                                            'RTM_IDL',
                                            'device_interfaces',
                                            '*.idl'))

unix_data_files.append((os.path.join(sitedir,'OpenRTM_aist', 'utils', 'rtcd'),
                        ['OpenRTM_aist/utils/rtcd/rtcd.conf']))
unix_data_files.append((os.path.join(sitedir,'OpenRTM_aist', 'utils', 'rtcd'),
                        ['OpenRTM_aist/utils/rtcd/rtc.conf']))

for idl in idl_files:
  unix_data_files.append((os.path.join(sitedir, 'OpenRTM_aist', 'RTM_IDL'),
                          [idl]))

for device_idl in device_if_idl_files:
  unix_data_files.append((os.path.join(sitedir, 'OpenRTM_aist', 'RTM_IDL',
                                       'device_interfaces'), [device_idl]))


win32_data_files = unix_data_files

win32_data_files.append((os.path.join(sitedir,'OpenRTM_aist', 'examples'),
                         ['OpenRTM_aist/examples/rtc.conf.sample']))
win32_data_files.append((os.path.join(sitedir,'OpenRTM_aist', 'examples'),
                         ['OpenRTM_aist/examples/component.conf']))
win32_data_files.append((os.path.join(sitedir,'OpenRTM_aist', 'utils', 'rtcd'),
                         ['OpenRTM_aist/utils/rtcd/rtcd.conf']))
"""
win32_data_files.append((os.path.join(sitedir,'OpenRTM_aist', 'examples','AutoControl'),
                         ['OpenRTM_aist/examples/AutoControl/rtc.conf']))
win32_data_files.append((os.path.join(sitedir,'OpenRTM_aist', 'examples','Composite'),
                         ['OpenRTM_aist/examples/Composite/rtc.conf']))
win32_data_files.append((os.path.join(sitedir,'OpenRTM_aist', 'examples','Composite'),
                         ['OpenRTM_aist/examples/Composite/composite.conf']))
win32_data_files.append((os.path.join(sitedir,'OpenRTM_aist', 'examples','ConfigSample'),
                         ['OpenRTM_aist/examples/ConfigSample/rtc.conf']))
win32_data_files.append((os.path.join(sitedir,'OpenRTM_aist', 'examples','ConfigSample'),
                         ['OpenRTM_aist/examples/ConfigSample/configsample.conf']))
win32_data_files.append((os.path.join(sitedir,'OpenRTM_aist', 'examples','ExtTrigger'),
                         ['OpenRTM_aist/examples/ExtTrigger/rtc.conf']))
win32_data_files.append((os.path.join(sitedir,'OpenRTM_aist', 'examples','MobileRobotCanvas'),
                         ['OpenRTM_aist/examples/MobileRobotCanvas/rtc.conf']))
win32_data_files.append((os.path.join(sitedir,'OpenRTM_aist', 'examples','NXTRTC'),
                         ['OpenRTM_aist/examples/NXTRTC/rtc.conf']))
win32_data_files.append((os.path.join(sitedir,'OpenRTM_aist', 'examples','SimpleIO'),
                         ['OpenRTM_aist/examples/SimpleIO/rtc.conf']))
win32_data_files.append((os.path.join(sitedir,'OpenRTM_aist', 'examples','SeqIO'),
                         ['OpenRTM_aist/examples/SeqIO/rtc.conf']))
win32_data_files.append((os.path.join(sitedir,'OpenRTM_aist', 'examples','SimpleService'),
                         ['OpenRTM_aist/examples/SimpleService/rtc.conf']))
win32_data_files.append((os.path.join(sitedir,'OpenRTM_aist', 'examples','Slider_and_Motor'),
                         ['OpenRTM_aist/examples/Slider_and_Motor/rtc.conf']))
win32_data_files.append((os.path.join(sitedir,'OpenRTM_aist', 'examples','TkJoyStick'),
                         ['OpenRTM_aist/examples/TkJoyStick/rtc.conf']))
win32_data_files.append((os.path.join(sitedir,'OpenRTM_aist', 'examples','TkLRFViewer'),
                         ['OpenRTM_aist/examples/TkLRFViewer/rtc.conf']))
"""

templates_xml = glob.glob(os.path.join('OpenRTM_aist',
                                       'examples',
                                       'Templates',
                                       '*.xml'))

for tmp_xml in templates_xml:
  win32_data_files.append((os.path.join(sitedir,'OpenRTM_aist', 'examples', 'Templates'),
                           [tmp_xml]))


##############################################################################################

pkg_name      = "OpenRTM-aist-Python"
pkg_version   = "1.0.0"
pkg_desc      = "Python modules for OpenRTM-aist-1.0"
pkg_author    = "Shinji Kurihara and Noriaki Ando"
pkg_email     = "n-ando@aist.go.jp"
pkg_url       = "http://www.openrtm.org/"
pkg_long_desc = """\
OpenRTM-aist is a reference implementation of RT-Middleware,
which is now under standardization process in OMG (Object Management Group).
OpenRTM-aist is being developed and distributed by
Intelligent Systems Research Institute,
National Institute of Advanced Industrial Science and Technology (AIST), Japan.
Please see http://www.openrtm.org/ for more detail.
"""
pkg_license   = "EPL"


try:
  if g_os == "unix":
    g_qkc_option = "-u"
    core.setup(name             = pkg_name,
               version          = pkg_version,
               description      = pkg_desc,
               author           = pkg_author,
               author_email     = pkg_email,
               url              = pkg_url,
               long_description = pkg_long_desc,
               license          = pkg_license,
               cmdclass         = { "build":Build, "build_idl":Build_idl, "build_doc":Build_doc, 'sdist':OtherSetupForSdist },
               packages         = unix_packages,
               scripts= ['OpenRTM_aist/utils/rtcprof/rtcprof_python',
                         'OpenRTM_aist/utils/rtcd/rtcd_python'],
               data_files       = unix_data_files)
    if sys.argv[1] == "sdist":
      g_qkc_option = "-m"
      core.setup(name             = pkg_name,
                 version          = pkg_version,
                 description      = pkg_desc,
                 author           = pkg_author,
                 author_email     = pkg_email,
                 url              = pkg_url,
                 long_description = pkg_long_desc,
                 license          = pkg_license,
                 cmdclass         = { "build":Build, "build_idl":Build_idl, "build_doc":Build_doc, 'sdist':OtherSetupForSdist  },
                 packages         = win32_packages,
                 scripts= ['OpenRTM_aist/utils/rtcprof/rtcprof_python.bat',
                           'OpenRTM_aist/utils/rtcd/rtcd_python.bat'],
                 data_files       = win32_data_files,
                 script_args      = ["sdist", "--format=zip"])
  elif g_os == "win32":
    g_qkc_option = "-m"
    core.setup(name             = pkg_name,
               version          = pkg_version,
               description      = pkg_desc,
               author           = pkg_author,
               author_email     = pkg_email,
               url              = pkg_url,
               long_description = pkg_long_desc,
               license          = pkg_license,
               cmdclass         = { "build":Build, "build_idl":Build_idl, "build_doc":Build_doc  },
               packages         = win32_packages,
               scripts= ['OpenRTM_aist/utils/rtcprof/rtcprof_python.bat',
                         'OpenRTM_aist/utils/rtcd/rtcd_python.bat'],
               data_files       = win32_data_files,
               script_args      = ["sdist", "--format=zip"])

except Exception, e:
  log.error("Error: %s", e)
