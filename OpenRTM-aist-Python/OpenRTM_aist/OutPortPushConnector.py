#!/usr/bin/env python
# -*- coding: euc-jp -*-


##
# @file OutPortPushConnector.py
# @brief Push type connector class
# @date $Date$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2009
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.
#

from omniORB import *
from omniORB import any

import OpenRTM_aist

class OutPortPushConnector(OpenRTM_aist.OutPortConnector):

    ##
    # @if jp
    # @brief コンストラクタ
    #
    # OutPortPushConnector は InPortConsumer の所有権を持つ。
    # したがって、OutPortPushConnector 削除時には、InPortConsumerも同時に
    # 解体・削除される。
    #
    # @param profile ConnectorProfile
    # @param consumer InPortConsumer
    #
    # @elsek
    # @brief Constructor
    #
    # OutPortPushConnector assume ownership of InPortConsumer.
    # Therefore, InPortConsumer will be deleted when OutPortPushConnector
    # is destructed.
    #
    # @param profile ConnectorProfile
    # @param consumer InPortConsumer
    #
    # @endif
    #
    # OutPortPushConnector(Profile profile,
    #                      InPortConsumer* consumer,
    #                      CdrBufferBase* buffer = 0);
    def __init__(self, profile, consumer, buffer = 0):
        OpenRTM_aist.OutPortConnector.__init__(self, profile)

        self._buffer = buffer
        self._consumer = consumer

        # publisher/buffer creation. This may throw std::bad_alloc;
        self._publisher = self.createPublisher(profile)
        if not self._buffer:
            self._buffer = self.createBuffer(profile)


        if not self._publisher or not self._buffer:
            raise

        if self._publisher.init(profile.properties) != OpenRTM_aist.DataPortStatus.PORT_OK:
            raise
        
        if self._profile.properties.hasKey("serializer"):
            endian = self._profile.properties.getProperty("serializer.cdr.endian")
            if not endian:
                self._rtcout.RTC_ERROR("write(): endian is not set.")
                raise
        
            endian = OpenRTM_aist.split(endian, ",") # Maybe endian is ["little","big"]
            self._endian = OpenRTM_aist.normalize(endian) # Maybe self._endian is "little" or "big"
        else:
            self._endian = "little"

        self._consumer.init(profile.properties)
        self._publisher.setConsumer(self._consumer)
        self._publisher.setBuffer(self._buffer)

        return


    ##
    # @if jp
    # @brief デストラクタ
    #
    # disconnect() が呼ばれ、consumer, publisher, buffer が解体・削除される。
    #
    # @else
    #
    # @brief Destructor
    #
    # This operation calls disconnect(), which destructs and deletes
    # the consumer, the publisher and the buffer.
    #
    # @endif
    #
    def __del__(self):
        self.disconnect()
        return

    ##
    # @if jp
    # @brief データの書き込み
    #
    # Publisherに対してデータを書き込み、これにより対応するInPortへ
    # データが転送される。
    #
    # @else
    #
    # @brief Writing data
    #
    # This operation writes data into publisher and then the data
    # will be transferred to correspondent InPort.
    #
    # @endif
    # template<class DataType>
    # virtual ReturnCode write(const DataType& data);
    def write(self, data):
        self._rtcout.RTC_TRACE("write()")

        # data -> (conversion) -> CDR stream
        cdr_data = None    
        if self._endian == "little":
            cdr_data = cdrMarshal(any.to_any(data).typecode(), data, 1)
        elif self._endian == "big":
            cdr_data = cdrMarshal(any.to_any(data).typecode(), data, 0)
        else:
            self._rtcout.RTC_ERROR("write(): endian %s is not support.",self._endian)
            return OpenRTM_aist.DataPortStatus.UNKNOWN_ERROR

        return self._publisher.write(cdr_data, 0, 0)


    ##
    # @if jp
    # @brief 接続解除
    #
    # consumer, publisher, buffer が解体・削除される。
    #
    # @else
    #
    # @brief disconnect
    #
    # This operation destruct and delete the consumer, the publisher
    # and the buffer.
    #
    # @endif
    #
    # virtual ReturnCode disconnect();
    def disconnect(self):
        self._rtcout.RTC_TRACE("disconnect()")
        # delete publisher
        if self._publisher:
            self._rtcout.RTC_DEBUG("delete publisher")
            pfactory = OpenRTM_aist.PublisherFactory.instance()
            pfactory.deleteObject(self._publisher)

        self._publisher = 0
    
        # delete consumer
        if self._consumer:
            self._rtcout.RTC_DEBUG("delete consumer")
            cfactory = OpenRTM_aist.InPortConsumerFactory.instance()
            cfactory.deleteObject(self._consumer)

        self._consumer = 0

        # delete buffer
        if self._buffer:
            self._rtcout.RTC_DEBUG("delete buffer")
            bfactory = OpenRTM_aist.CdrBufferFactory.instance()
            bfactory.deleteObject(self._buffer)

        self._buffer = 0
        self._rtcout.RTC_TRACE("disconnect() done")

        return OpenRTM_aist.DataPortStatus.PORT_OK


    ##
    # @if jp
    # @brief アクティブ化
    #
    # このコネクタをアクティブ化する
    #
    # @else
    #
    # @brief Connector activation
    #
    # This operation activates this connector
    #
    # @endif
    #
    # virtual void activate();
    def activate(self):
        self._publisher.activate()
        return


    ##
    # @if jp
    # @brief 非アクティブ化
    #
    # このコネクタを非アクティブ化する
    #
    # @else
    #
    # @brief Connector deactivation
    #
    # This operation deactivates this connector
    #
    # @endif
    #
    # virtual void deactivate();
    def deactivate(self):
        self._publisher.deactivate()
        return

    
    ##
    # @if jp
    # @brief Buffer を取得する
    #
    # Connector が保持している Buffer を返す
    #
    # @else
    # @brief Getting Buffer
    #
    # This operation returns this connector's buffer
    #
    # @endif
    #
    # virtual CdrBufferBase* getBuffer();
    def getBuffer(self):
        return self._buffer


    ##
    # @if jp
    # @brief Publisherの生成
    # @else
    # @brief create publisher
    # @endif
    #
    # virtual PublisherBase* createPublisher(Profile& profile);
    def createPublisher(self, profile):
        pub_type = profile.properties.getProperty("subscription_type","flush")
        pub_type = OpenRTM_aist.normalize([pub_type])
        return OpenRTM_aist.PublisherFactory.instance().createObject(pub_type)


    ##
    # @if jp
    # @brief Bufferの生成
    # @else
    # @brief create buffer
    # @endif
    #
    # virtual CdrBufferBase* createBuffer(Profile& profile);
    def createBuffer(self, profile):
        buf_type = profile.properties.getProperty("buffer_type",
                                                  "ring_buffer")

        return OpenRTM_aist.CdrBufferFactory.instance().createObject(buf_type)

