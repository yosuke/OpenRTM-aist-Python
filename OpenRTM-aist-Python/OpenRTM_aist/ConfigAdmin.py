#!/usr/bin/env python
# -*- coding: euc-jp -*- 

##
# @file ConfigAdmin.py
# @brief Configuration Administration classes
# @date $Date: 2007/09/04$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
# 
# Copyright (C) 2007-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.



import copy
import OpenRTM_aist


class OnUpdateCallback:
  def __init__(self):
    pass


  def __call__(self, config_set):
    pass



class OnUpdateParamCallback:
  def __init__(self):
    pass


  def __call__(self, config_set, config_param):
    pass



class OnSetConfigurationSetCallback:
  def __init__(self):
    pass


  def __call__(self, config_set):
    pass



class OnAddConfigurationAddCallback:
  def __init__(self):
    pass


  def __call__(self, config_set):
    pass



class OnRemoveConfigurationSetCallback:
  def __init__(self):
    pass


  def __call__(self, config_set):
    pass



class OnActivateSetCallback:
  def __init__(self):
    pass


  def __call__(self, config_id):
    pass



##
# @if jp
# @class Config
# @brief Config クラス
# 
# コンフィギュレーションパラメータの情報を保持するクラス。
# コンフィギュレーションのデータ型と設定されたデータ型を文字列に変換する
# 変換関数を指定する。
# 
# @since 0.4.0
# 
# @else
# 
# @endif
class Config:
  """
  """

  ##
  # @if jp
  # 
  # @brief コンストラクタ
  # 
  # コンストラクタ
  # 
  # @param self 
  # @param name コンフィギュレーションパラメータ名
  # @param var コンフィギュレーションパラメータ格納用変数
  # @param def_val 文字列形式のデフォルト値
  # @param trans 文字列形式変換関数(デフォルト値:None)
  # 
  # @else
  # 
  # @endif
  def __init__(self, name, var, def_val, trans=None):
    self.name = name
    self.default_value = def_val
    self._var = var
    if trans:
      self._trans = trans
    else:
      self._trans = OpenRTM_aist.stringTo


  ##
  # @if jp
  # 
  # @brief バインドパラメータ値を更新
  # 
  # コンフィギュレーション設定値でコンフィギュレーションパラメータを更新する
  # 
  # @param self 
  # @param val パラメータ値の文字列表現
  # 
  # @return 更新処理結果(更新成功:true，更新失敗:false)
  # 
  # @else
  # 
  # @endif
  # virtual bool update(const char* val)
  def update(self, val):
    if self._trans(self._var, val):
      return True
    self._trans(self._var, self._default_value)
    return False



##
# @if jp
# @class ConfigAdmin
# @brief ConfigAdmin クラス
# 
# 各種コンフィギュレーション情報を管理するクラス。
# 
# @since 0.4.0
# 
# @else
# 
# @endif
class ConfigAdmin:
  """
  """



  ##
  # @if jp
  # 
  # @brief コンストラクタ
  # 
  # コンストラクタ
  # 
  # @param self 
  # @param configsets 設定対象プロパティ名
  # 
  # @else
  # 
  # @endif
  # ConfigAdmin(coil::Properties& prop);
  def __init__(self, configsets):
    self._configsets = configsets
    self._activeId   = "default"
    self._active     = True
    self._changed    = False
    self._params     = []
    self._emptyconf  = OpenRTM_aist.Properties()
    self._newConfig  = []

    self._updateCb          = None
    self._updateParamCb     = None
    self._setConfigSetCb    = None
    self._addConfigSetCb    = None
    self._removeConfigSetCb = None
    self._activateSetCb     = None


  ##
  # @if jp
  # 
  # @brief デストラクタ
  # 
  # デストラクタ。
  # 設定されているパラメータを削除する。
  # 
  # @param self 
  # 
  # @else
  # 
  # @endif
  def __del__(self):
    del self._params


  ##
  # @if jp
  # 
  # @brief コンフィギュレーションパラメータの設定
  # 
  # コンフィギュレーションパラメータと変数をバインドする
  # 指定した名称のコンフィギュレーションパラメータが既に存在する場合は
  # falseを返す。
  # 
  # @param self 
  # @param param_name コンフィギュレーションパラメータ名
  # @param var コンフィギュレーションパラメータ格納用変数
  # @param def_val コンフィギュレーションパラメータデフォルト値
  # @param trans コンフィギュレーションパラメータ文字列変換用関数
  #             (デフォルト値:None)
  # 
  # @return 設定結果(設定成功:true，設定失敗:false)
  # 
  # @else
  # 
  # @endif
  #template <typename VarType>
  # bool bindParameter(const char* param_name, VarType& var,
  #                    const char* def_val,
  #                    bool (*trans)(VarType&, const char*) = coil::stringTo)
  def bindParameter(self, param_name, var, def_val, trans=None):
    if trans is None:
      trans = OpenRTM_aist.stringTo
    
    if self.isExist(param_name):
      return False

    if not trans(var, def_val):
      return False
    
    self._params.append(Config(param_name, var, def_val, trans))
    return True


  ##
  # void update(void);
  #
  # @if jp
  #
  # @brief コンフィギュレーションパラメータの更新
  #        (アクティブコンフィギュレーションセット)
  # 
  # コンフィギュレーションセットが更新されている場合に、現在アクティ
  # ブになっているコンフィギュレーションに設定した値で、コンフィギュ
  # レーションパラメータの値を更新する。この処理での更新は、アクティ
  # ブとなっているコンフィギュレーションセットが存在している場合、前
  # 回の更新からコンフィギュレーションセットの内容が更新されている場
  # 合のみ実行される。
  #
  # @else
  #
  # @brief Update the values of configuration parameters
  #        (Active configuration set)
  # 
  # When configuration set is updated, update the configuration
  # parameter value to the value that is set to the current active
  # configuration.  This update will be executed, only when an
  # active configuration set exists and the content of the
  # configuration set has been updated from the last update.
  #
  # @endif
  #
  # void update(const char* config_set);
  #
  # @if jp
  #
  # @brief コンフィギュレーションパラメータの更新(ID指定)
  # 
  # コンフィギュレーション変数の値を、指定したIDを持つコンフィギュレー
  # ションセットの値で更新する。これにより、アクティブなコンフィギュ
  # レーションセットは変更されない。したがって、アクティブコンフィギュ
  # レーションセットとパラメータ変数の間に矛盾が発生する可能性がある
  # ので注意が必要である。
  #
  # 指定したIDのコンフィギュレーションセットが存在しない場合は、何も
  # せずに終了する。
  #
  # @param config_set 設定対象のコンフィギュレーションセットID
  # 
  # @else
  #
  # @brief Update configuration parameter (By ID)
  # 
  # This operation updates configuration variables by the
  # configuration-set with specified ID. This operation does not
  # change current active configuration-set. Since this operation
  # causes inconsistency between current active configuration set
  # and actual values of configuration variables, user should
  # carefully use it.
  #
  # This operation ends without doing anything, if the
  # configuration-set does not exist.
  #
  # @param config_set The target configuration set's ID to setup
  #
  # @endif
  #
  # void update(const char* config_set, const char* config_param);
  #
  # @if jp
  #
  # @brief コンフィギュレーションパラメータの更新(名称指定)
  # 
  # 特定のコンフィギュレーション変数の値を、指定したIDを持つコンフィ
  # ギュレーションセットの値で更新する。これにより、アクティブなコン
  # フィギュレーションセットは変更されない。したがって、アクティブコ
  # ンフィギュレーションセットとパラメータ変数の間に矛盾が発生する可
  # 能性があるので注意が必要である。
  #
  # 指定したIDのコンフィギュレーションセットや、指定した名称のパラメー
  # タが存在しない場合は、何もせずに終了する。
  #
  # @param config_set コンフィギュレーションID
  # @param config_param コンフィギュレーションパラメータ名
  # 
  # @else
  #
  # @brief Update the values of configuration parameters (By name)
  # 
  # This operation updates a configuration variable by the
  # specified configuration parameter in the
  # configuration-set. This operation does not change current
  # active configuration-set. Since this operation causes
  # inconsistency between current active configuration set and
  # actual values of configuration variables, user should carefully
  # use it.
  #
  # This operation ends without doing anything, if the
  # configuration-set or the configuration parameter do not exist.
  #
  # @param config_set configuration-set ID.
  # @param config_param configuration parameter name.
  #
  # @endif
  #
  def update(self, config_set=None, config_param=None):
    # update(const char* config_set)
    if config_set and config_param is None:
      if self._configsets.hasKey(config_set) is None:
        return
      prop = self._configsets.getNode(config_set)
      for i in range(len(self._params)):
        if prop.hasKey(self._params[i].name):
          self._params[i].update(prop.getProperty(self._params[i].name))
          self.onUpdate(config_set)

    # update(const char* config_set, const char* config_param)
    if config_set and config_param:
      key = config_set
      key = key+"."+config_param
      for conf in self._params:
        if conf.name == config_param:
          conf.update(self._configsets.getProperty(key))
          self.onUpdateParam(config_set, config_param)
          return

    # update()
    if config_set is None and config_param is None:
      if self._changed and self._active:
        self.update(self._activeId)
        self._changed = False
      return


  ##
  # @if jp
  # 
  # @brief コンフィギュレーションパラメータの存在確認
  # 
  # 指定した名称を持つコンフィギュレーションパラメータが存在するか確認する。
  # 
  # @param self 
  # @param param_name コンフィギュレーションパラメータ名称。
  # 
  # @return 存在確認結果(パラメータあり:true，パラメータなし:false)
  # 
  # @else
  # 
  # @endif
  # bool isExist(const char* name);
  def isExist(self, param_name):
    if not self._params:
      return False
    
    for conf in self._params:
      if conf.name == param_name:
        return True

    return False


  ##
  # @if jp
  # 
  # @brief コンフィギュレーションパラメータの変更確認
  # 
  # コンフィギュレーションパラメータが変更されたか確認する。
  # 
  # @param self 
  # 
  # @return 変更確認結果(変更あり:true、変更なし:false)
  # 
  # @else
  # 
  # @endif
  # bool isChanged(void) {return m_changed;}
  def isChanged(self):
    return self._changed


  ##
  # @if jp
  # 
  # @brief アクティブ・コンフィギュレーションセットIDの取得
  # 
  # 現在アクティブなコンフィギュレーションセットのIDを取得する。
  # 
  # @param self 
  # 
  # @return アクティブ・コンフィギュレーションセットID
  # 
  # @else
  # 
  # @endif
  # const char* getActiveId(void);
  def getActiveId(self):
    return self._activeId


  ##
  # @if jp
  # 
  # @brief コンフィギュレーションセットの存在確認
  # 
  # 指定したコンフィギュレーションセットが存在するか確認する。
  # 
  # @param self 
  # @param config_id 確認対象コンフィギュレーションセットID
  # 
  # @return 存在確認結果(指定したConfigSetあり:true、なし:false)
  # 
  # @else
  # 
  # @endif
  # bool haveConfig(const char* config_id);
  def haveConfig(self, config_id):
    if self._configsets.hasKey(config_id) is None:
      return False
    else:
      return True


  ##
  # @if jp
  # 
  # @brief コンフィギュレーションセットのアクティブ化確認
  # 
  # コンフィギュレーションセットがアクティブ化されているか確認する。
  # 
  # @param self 
  # 
  # @return 状態確認結果(アクティブ状態:true、非アクティブ状態:false)
  # 
  # @else
  # 
  # @endif
  # bool isActive(void);
  def isActive(self):
    return self._active


  ##
  # @if jp
  # 
  # @brief 全コンフィギュレーションセットの取得
  # 
  # 設定されている全コンフィギュレーションセットを取得する。
  # 
  # @param self 
  # 
  # @return 全コンフィギュレーションセット
  # 
  # @else
  # 
  # @endif
  # const std::vector<coil::Properties*>& getConfigurationSets(void);
  def getConfigurationSets(self):
    return self._configsets.getLeaf()


  ##
  # @if jp
  # 
  # @brief 指定したIDのコンフィギュレーションセットの取得
  # 
  # IDで指定したコンフィギュレーションセットを取得する。
  # 指定したコンフィギュレーションセットが存在しない場合は、
  # 空のコンフィギュレーションセットを返す。
  # 
  # @param self 
  # @param config_id 取得対象コンフィギュレーションセットのID
  # 
  # @return コンフィギュレーションセット
  # 
  # @else
  # 
  # @endif
  # const coil::Properties& getConfigurationSet(const char* config_id);
  def getConfigurationSet(self, config_id):
    prop = self._configsets.getNode(config_id)
    if prop is None:
      return self._emptyconf
    return prop


  ##
  # @if jp
  # 
  # @brief 指定したプロパティのコンフィギュレーションセットへの追加
  # 
  # 指定したプロパティをコンフィギュレーションセットへ追加する。
  # 
  # @param self 
  # @param config_set 追加するプロパティ
  # 
  # @return 追加処理実行結果(追加成功:true、追加失敗:false)
  # 
  # @else
  # 
  # @endif
  # bool setConfigurationSetValues(const coil::Properties& config_set)
  def setConfigurationSetValues(self, config_set):
    if config_set.getName() == "" or config_set.getName() is None:
      return False

    if not self._configsets.hasKey(config_set.getName()):
      return False

    p = self._configsets.getNode(config_set.getName())
    if p is None:
      return False

    p.mergeProperties(config_set)
    self._changed = True
    self._active  = False
    self.onSetConfigurationSet(config_set)
    return True


  ##
  # @if jp
  # 
  # @brief アクティブ・コンフィギュレーションセットを取得
  # 
  # 現在アクティブとなっているコンフィギュレーションセットを取得する。
  # アクティブとなっているコンフィギュレーションセットが存在しない場合は、
  # 空のコンフィギュレーションセット を返す。
  # 
  # @param self 
  # 
  # @return アクティブ・コンフィギュレーションセット
  # 
  # @else
  # 
  # @endif
  # const coil::Properties& getActiveConfigurationSet(void);
  def getActiveConfigurationSet(self):
    p = self._configsets.getNode(self._activeId)
    if p is None:
      return self._emptyconf

    return p


  ##
  # @if jp
  # 
  # @brief コンフィギュレーションセットに設定値を追加
  # 
  # コンフィギュレーションセットに設定値を追加する。
  # 
  # @param self 
  # @param configset 追加するプロパティ
  # 
  # @return 追加処理結果(追加成功:true、追加失敗:false)
  # 
  # @else
  # 
  # @endif
  # bool addConfigurationSet(const coil::Properties& configuration_set);
  def addConfigurationSet(self, configset):
    if self._configsets.hasKey(configset.getName()):
      return False
    node = configset.getName()

    # Create node
    self._configsets.createNode(node)

    p = self._configsets.getNode(node)
    if p is None:
      return False

    p.mergeProperties(configset)
    self._newConfig.append(node)

    self._changed = True
    self._active  = False
    self.onAddConfigurationSet(configset)
    return True


  ##
  # @if jp
  # 
  # @brief コンフィギュレーションセットの削除
  # 
  # 指定したIDのコンフィギュレーションセットを削除する。
  # 指定したIDのコンフィギュレーションセットが存在しない場合は、
  # falseを返す。
  # 
  # @param self 
  # @param config_id 削除対象コンフィギュレーションセットのID
  # 
  # @return 削除処理結果(削除成功:true、削除失敗:false)
  # 
  # @else
  # 
  # @endif
  # bool removeConfigurationSet(const char* config_id);
  def removeConfigurationSet(self, config_id):
    if config_id == "default":
      return False
    if self._activeId == config_id:
      return False

    find_flg = False
    # removeable config-set is only config-sets newly added
    for (idx,conf) in enumerate(self._newConfig):
      if conf == config_id:
        find_flg = True
        break


    if not find_flg:
      return False

    p = self._configsets.getNode(config_id)
    if p:
      p.getRoot().removeNode(config_id)
      del p

    del self._newConfig[idx]

    self._changed = True
    self._active  = False
    self.onRemoveConfigurationSet(config_id)
    return True


  ##
  # @if jp
  # 
  # @brief コンフィギュレーションセットのアクティブ化
  # 
  # 指定したIDのコンフィギュレーションセットをアクティブ化する。
  # 指定したIDのコンフィギュレーションセットが存在しない場合は、
  # falseを返す。
  # 
  # @param self 
  # @param config_id 削除対象コンフィギュレーションセットのID
  # 
  # @return アクティブ処理結果(成功:true、失敗:false)
  # 
  # @else
  # 
  # @endif
  # bool activateConfigurationSet(const char* config_id);
  def activateConfigurationSet(self, config_id):
    if config_id is None:
      return False

    # '_<conf_name>' is special configuration set name
    if config_id[0] == '_':
      return False

    if not self._configsets.hasKey(config_id):
      return False
    self._activeId = config_id
    self._active   = True
    self._changed  = True
    self.onActivateSet(config_id)
    return True


  # void setOnUpdate(OnUpdateCallback* cb);
  def setOnUpdate(self, cb):
    self._updateCb = cb


  # void setOnUpdateParam(OnUpdateParamCallback* cb);
  def setOnUpdateParam(self, cb):
    self._updateParamCb = cb


  # void setOnSetConfigurationSet(OnSetConfigurationSetCallback* cb);
  def setOnSetConfigurationSet(self, cb):
    self._setConfigSetCb = cb


  # void setOnAddConfigurationSet(OnAddConfigurationAddCallback* cb);
  def setOnAddConfigurationSet(self, cb):
    self._addConfigSetCb = cb


  # void setOnRemoveConfigurationSet(OnRemoveConfigurationSetCallback* cb);
  def setOnRemoveConfigurationSet(self, cb):
    self._removeConfigSetCb = cb


  # void setOnActivateSet(OnActivateSetCallback* cb);
  def setOnActivateSet(self, cb):
    self._activateSetCb = cb


  # void onUpdate(const char* config_set);
  def onUpdate(self, config_set):
    if self._updateCb is not None:
      self._updateCb(config_set)


  # void onUpdateParam(const char* config_set, const char* config_param);
  def onUpdateParam(self, config_set, config_param):
    if self._updateParamCb is not None:
      self._updateParamCb(config_set, config_param)


  # void onSetConfigurationSet(const coil::Properties& config_set);
  def onSetConfigurationSet(self, config_set):
    if self._setConfigSetCb is not None:
      self._setConfigSetCb(config_set)


  # void onAddConfigurationSet(const coil::Properties& config_set);
  def onAddConfigurationSet(self, config_set):
    if self._addConfigSetCb is not None:
      self._addConfigSetCb(config_set)


  # void onRemoveConfigurationSet(const char* config_id);
  def onRemoveConfigurationSet(self, config_id):
    if self._removeConfigSetCb is not None:
      self._removeConfigSetCb(config_id)


  # void onActivateSet(const char* config_id);
  def onActivateSet(self, config_id):
    if self._activateSetCb is not None:
      self._activateSetCb(config_id)



  class find_conf:
    def __init__(self, name):
      self._name = name

    def __call__(self, conf):
      if conf is None or conf is 0:
        return False

      return self._name == conf.name
