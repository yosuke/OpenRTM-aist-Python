#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file  InPortProvider.py
# @brief InPortProvider class
# @date  $Date: 2007/09/20 $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006-2008
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.


import OpenRTM
import SDOPackage, SDOPackage__POA


##
# @if jp
# @class InPortProvider
# @brief InPortProvider ���饹
#
# InPort�ξ�����ݻ����뤿��Υ��饹��
#
# @since 0.4.0
#
# @else
# @class InPortProvider
# @brief InPortProvider class
# @endif
class InPortProvider:
  """
  """



  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  #
  # @param self
  #
  # @else
  # @brief Constructor
  # @endif
  def __init__(self):
    self._properties = []
    self._dataType = ""
    self._interfaceType = ""
    self._dataflowType = ""
    self._subscriptionType = ""


  ##
  # @if jp
  # @brief InterfaceProfile������������
  #
  # InterfaceProfile�����������롣
  #
  # @param self
  # @param prop InterfaceProfile�����������ץ��ѥƥ�
  #
  # @else
  #
  # @endif
  def publishInterfaceProfile(self, prop):
    OpenRTM.NVUtil.appendStringValue(prop, "dataport.data_type",
             self._dataType)
    OpenRTM.NVUtil.appendStringValue(prop, "dataport.interface_type",
             self._interfaceType)
    OpenRTM.NVUtil.appendStringValue(prop, "dataport.dataflow_type",
             self._dataflowType)
    OpenRTM.NVUtil.appendStringValue(prop, "dataport.subscription_type",
             self._subscriptionType)


  ##
  # @if jp
  # @brief Interface������������
  #
  # Interface�����������롣
  #
  # @param self
  # @param prop Interface�����������ץ��ѥƥ�
  #
  # @else
  #
  # @endif
  def publishInterface(self, prop):
    if not OpenRTM.NVUtil.isStringValue(prop,
                "dataport.interface_type",
                self._interfaceType):
      return

    OpenRTM.NVUtil.append(prop, self._properties)


  ##
  # @if jp
  # @brief �ǡ��������פ����ꤹ��
  #
  # �ǡ��������פ����ꤹ�롣
  #
  # @param self
  # @param data_type �����оݥǡ���������
  #
  # @else
  #
  # @endif
  def setDataType(self, data_type):
    self._dataType = data_type


  ##
  # @if jp
  # @brief ���󥿥ե����������פ����ꤹ��
  #
  # ���󥿥ե����������פ����ꤹ�롣
  #
  # @param self
  # @param interface_type �����оݥ��󥿥ե�����������
  #
  # @else
  #
  # @endif
  def setInterfaceType(self, interface_type):
    self._interfaceType = interface_type


  ##
  # @if jp
  # @brief �ǡ����ե��������פ����ꤹ��
  #
  # �ǡ����ե��������פ����ꤹ�롣
  #
  # @param self
  # @param dataflow_type �����оݥǡ����ե���������
  #
  # @else
  #
  # @endif
  def setDataFlowType(self, dataflow_type):
    self._dataflowType = dataflow_type


  ##
  # @if jp
  # @brief ���֥�����ץ���󥿥��פ����ꤹ��
  #
  # ���֥�����ץ���󥿥��פ����ꤹ�롣
  #
  # @param self
  # @param subs_type �����оݥ��֥�����ץ���󥿥���
  #
  # @else
  #
  # @endif
  def setSubscriptionType(self, subs_type):
    self._subscriptionType = subs_type