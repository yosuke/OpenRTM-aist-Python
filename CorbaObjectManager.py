#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# \file CorbaObjectManager.py
# \brief CORBA Object manager class
# \date $Date: 2007/08/27$
# \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006-2008
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.


from omniORB import CORBA, PortableServer

import OpenRTM


##
# @if jp
# @class CorbaObjectManager
# @brief CORBA オブジェクトをアクティブ化、非アクティブ化する
#
# RTObjectのアクティブ化，非アクティブ化を行うクラスである。
# 保持しているORB，POAを用いて CORBA オブジェクトのアクティブ化，
# 非アクティブ化を行う。
#
# @since 0.4.0
#
# @else
# @class CorbaObjectManager
# @brief Activate and deactivate CORBA objects
# @endif
class CorbaObjectManager:
  """
  """



  ##
  # @if jp
  #
  # @brief コンストラクタ
  #
  # @param self
  # @param orb ORB
  # @param poa POA
  #
  # @else
  #
  # @brief Consructor
  #
  # @param orb ORB
  #
  # @endif
  def __init__(self, orb, poa):
    self._orb = orb
    self._poa = poa


  ##
  # @if jp
  # @brief CORBA オブジェクトをアクティブ化する
  #
  # 指定されたRTObjectを CORBA オブジェクトとしてアクティブ化し、
  # オブジェクトリファレンスを設定する。
  #
  # @param self
  # @param comp アクティブ化対象RTObject
  #
  # @else
  # @brief Activate CORBA object
  # @endif
  def activate(self, comp):
    id_ = self._poa.activate_object(comp)
    obj = self._poa.id_to_reference(id_)
    comp.setObjRef(obj._narrow(OpenRTM.RTObject_impl))


  ##
  # @if jp
  # @brief CORBA オブジェクトを非アクティブ化する
  #
  # 指定されたRTObjectの非アクティブ化を行う
  #
  # @param self
  # @param comp 非アクティブ化対象RTObject
  #
  # @else
  # @brief Deactivate CORBA object
  # @endif
  def deactivate(self, comp):
    id_ = self._poa.servant_to_id(comp)
    self._poa.deactivate_object(id_)
