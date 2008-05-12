#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
 \file ManagerConfig.py
 \brief RTC manager configuration
 \date $Date: $
 \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara

 Copyright (C) 2003-2005
     Task-intelligence Research Group,
     Intelligent Systems Research Institute,
     National Institute of
         Advanced Industrial Science and Technology (AIST), Japan
     All rights reserved.
"""


import sys
import os
import re
import getopt
import platform

import OpenRTM

  
  
class ManagerConfig :
	"""
	\if jp

	\class ManagerConfig
	\brief Manager configuration クラス

	Manager のコンフィギュレーションを行う、コマンドライン引数を受け取り、
	(あるいは引数なしで)インスタンス化される。、Manager のプロパティの前設定
	を行い

	設定(ファイル)の指定の強さは以下のとおりである。
	上がもっとも強く、下がもっとも弱い。
	<OL>
	<LI>コマンドラインオプション "-f"
	<LI>環境変数 "RTC_MANAGER_CONFIG"
	<LI>デフォルト設定ファイル "./rtc.conf"
	<LI>デフォルト設定ファイル "/etc/rtc.conf"
	<LI>デフォルト設定ファイル "/etc/rtc/rtc.conf"
	<LI>デフォルト設定ファイル "/usr/local/etc/rtc.conf"
	<LI>デフォルト設定ファイル "/usr/local/etc/rtc/rtc.conf"
	<LI>埋め込みコンフィギュレーション値
	</OL>
	ただし、コマンドラインオプション "-d" が指定された場合は、
	(たとえ -f で設定ファイルを指定しても)埋め込みコンフィギュレーション値
	が使用される。

	\else

	\brief

	\endif
	"""
  
	# The list of default configuration file path.
	config_file_path = ["./rtc.conf",
						"/etc/rtc.conf",
						"/etc/rtc/rtc.conf",
						"/usr/local/etc/rtc.conf",
						"/usr/local/etc/rtc/rtc.conf",
						None]

	# Environment value to specify configuration file
	config_file_env = "RTC_MANAGER_CONFIG"


	def __init__(self, argc=None, argv=None):
		"""
        \if jp

        \brief ManagerConfig コンストラクタ

        与えられた引数により初期化も同時にするコンストラクタ。

        \param argc コマンドライン引数の数
        \param argv コマンドライン引数

        \else

        \brief ManagerConfig constructor

        The constructor that performs initialization at the same time with
        given arguments.

        \param argc The number of command line arguments
        \param argv The command line arguments

        \endif
		"""
		self._configFile = ""
		if argc != None and argv != None:
			self.init(argc,argv)


	def __del__(self):
		"""
        \if jp
        \brief ManagerConfig デストラクタ
        \else
        \brief ManagerConfig destructor
        \endif
		"""
		pass


	def init(self, argc, argv):
		"""
        \if jp
        \brief 初期化

        コマンドライン引数を与えて初期化する。コマンドラインオプションは
        以下のものが使用可能である。

        -f file   : コンフィギュレーションファイルを指定する。<br>
        -l module : ロードするモジュールを指定する。<br>
        -o options: その他オプションを指定する。。<br>
        -d        : デフォルトのコンフィギュレーションを使う。<br>
        \else
        \brief Initialization

        Initialize with command line options. The following command options
        are available.

        -f file   : Specify a configuration file. <br>
        -l module : Specify modules to be loaded at the beginning. <br>
        -o options: Other options. <br>
        -d        : Use default static configuration. <br>
        \endif
		"""
		self.parseArgs(argc, argv)


	def configure(self, prop):
		"""
		 \if jp
		 \brief Configuration の結果をPropertyに反映させる
		 \param prop(OpenRTM.Properties)
		 \else
		 \brief Apply configuration results to Property
		 \param prop(OpenRTM.Properties)
		 \endif
		"""
		prop.setDefaults(OpenRTM.default_config)
		if self.findConfigFile():
			try:
				fd = file(self._configFile,"r")
				prop.load(fd)
				fd.close()
			except:
				print "Error: file open."
		return self.setSystemInformation(prop)

	"""
        \if jp

        \brief コンフィギュレーションを取得する

        コンフィギュレーションを取得する。init()呼び出し前に呼ぶと、
        静的に定義されたデフォルトのコンフィギュレーションを返す。
        init() 呼び出し後に呼ぶと、コマンドライン引数、環境変数等に
        基づいた初期化されたコンフィギュレーションを返す。

        \else

        \brief Get configuration value.

        This operation returns default configuration statically defined,
        when before calling init() function. When after calling init() function,
        this operation returns initialized configuration value according to
        command option, environment value and so on.

        \endif
    """
	#def getConfig(self):
	#pass


	def parseArgs(self, argc, argv):
		"""
		 \if jp
		 \brief コマンド引数をパースする
		 
		 -f file   : コンフィギュレーションファイルを指定する。<br>
		 -l module : ロードするモジュールを指定する。。<br>
		 -o options: その他オプションを指定する。。<br>
		 -d        : デフォルトのコンフィギュレーションを使う。<br>
		 \else
		 \brief Parse command arguments
		 
		 -f file   : Specify a configuration file. <br>
		 -l module : Specify modules to be loaded at the beginning. <br>
		 -o options: Other options. <br>
		 -d        : Use default static configuration. <br>
		 \endif
		"""
		try:
			opts, args = getopt.getopt(argv[1:], "f:l:o:d:")
		except getopt.GetoptError:
			print "Error: getopt error!"
			sys.exit(0)

		for opt, arg in opts:
			if opt == "-f":
				self._configFile = arg

			if opt == "-l":
				pass

			if opt == "-o":
				pass

			if opt == "-d":
				pass

		return


	def findConfigFile(self):
		"""
        \if jp
        \brief Configuration file を探す

        Configuration file の優先順位

        コマンドオプション指定＞環境変数＞デフォルトファイル＞デフォルト設定

        デフォルト強制オプション(-d): デフォルトファイルがあっても無視して
            デフォルト設定を使う
        \else
        \brief Find configuration file
        \endif
		"""
		if self._configFile != "":
			if self.fileExist(self._configFile):
				return True

		env = os.getenv(self.config_file_env)
		if env != None:
			if self.fileExist(env):
				self._configFile = env
				return True

		i = 0
		while (self.config_file_path[i] != None):
			if self.fileExist(self.config_file_path[i]):
				self._configFile = self.config_file_path[i]
				return True
			i += 1

		return False


	def setSystemInformation(self, prop):
		"""
		 \if jp

		 \brief システム情報をセットする

		    システム情報を取得しプロパティにセットする。設定されるキーは以下の通り。
		    manager.os.name    : OS名
		    manager.os.release : OSリリース名
		    maanger.os.version : OSバージョン名
		    manager.os.arch    : OSアーキテクチャ
		    manager.os.hostname: ホスト名
		    manager.pid        : プロセスID
		 \param prop(OpenRTM.Properties)
		 \else
		 \brief Set system information
		 
		    Get the following system info and set them to Manager's properties.
		    manager.os.name    : OS name
		    manager.os.release : OS release name
		    maanger.os.version : OS version
		    manager.os.arch    : OS architecture
		    manager.os.hostname: Hostname
		    manager.pid        : process ID
		 \param prop(OpenRTM.Properties)
		 \endif
		"""
		sysinfo = platform.uname()

		prop.setProperty("manager.os.name",     sysinfo[0])
		prop.setProperty("manager.os.hostname", sysinfo[1])
		prop.setProperty("manager.os.release",  sysinfo[2])
		prop.setProperty("manager.os.version",  sysinfo[3])
		prop.setProperty("manager.os.arch",     sysinfo[4])
		prop.setProperty("manager.pid",         os.getpid())
		
		return prop


	def fileExist(self, filename):
		"""
		 \if jp
		 \brief ファイルが存在するかどうか確かめる
		 \param filename(string)
		 \else
		 \brief Check file existance
		 \param filename(string)
		 \endif
		"""
		try:
			fp = open(filename)
		except:
			print "Can't open file:", filename
			return False
		else:
			fp.close()
			return True

		return False


