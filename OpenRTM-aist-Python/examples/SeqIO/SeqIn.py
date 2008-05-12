#!/usr/bin/env python
# -*- Python -*-

import sys
import time

import OpenRTM
import RTC

seqin_spec = ["implementation_id", "SeqIn",
              "type_name",         "SequenceInComponent",
              "description",       "Sequence InPort component",
              "version",           "1.0",
              "vendor",            "Shinji Kurihara",
              "category",          "example",
              "activity_type",     "DataFlowComponent",
              "max_instance",      "10",
              "language",          "Python",
              "lang_type",         "script",
              ""]


class SeqIn(OpenRTM.DataFlowComponentBase):
    def __init__(self, manager):
        OpenRTM.DataFlowComponentBase.__init__(self, manager)
        self._short     = RTC.TimedShort(RTC.Time(0,0),0)
        self._long      = RTC.TimedLong(RTC.Time(0,0),0)
        self._float     = RTC.TimedFloat(RTC.Time(0,0),0)
        self._double    = RTC.TimedDouble(RTC.Time(0,0),0)
        self._shortSeq  = RTC.TimedShortSeq(RTC.Time(0,0),[])
        self._longSeq   = RTC.TimedLongSeq(RTC.Time(0,0),[])
        self._floatSeq  = RTC.TimedFloatSeq(RTC.Time(0,0),[])
        self._doubleSeq = RTC.TimedDoubleSeq(RTC.Time(0,0),[])

        self._shortIn     = OpenRTM.InPort("Short", self._short, OpenRTM.RingBuffer(8))
        self._longIn      = OpenRTM.InPort("Long", self._long, OpenRTM.RingBuffer(8))
        self._floatIn     = OpenRTM.InPort("Float", self._float, OpenRTM.RingBuffer(8))
        self._doubleIn    = OpenRTM.InPort("Double", self._double, OpenRTM.RingBuffer(8))
        self._shortSeqIn  = OpenRTM.InPort("ShortSeq", self._shortSeq, OpenRTM.RingBuffer(8))
        self._longSeqIn   = OpenRTM.InPort("LongSeq", self._longSeq, OpenRTM.RingBuffer(8))
        self._floatSeqIn  = OpenRTM.InPort("FloatSeq", self._floatSeq, OpenRTM.RingBuffer(8))
        self._doubleSeqIn = OpenRTM.InPort("DoubleSeq", self._doubleSeq, OpenRTM.RingBuffer(8))


        # Set InPort buffer
        self.registerInPort("Short", self._shortIn)
        self.registerInPort("Long", self._longIn)
        self.registerInPort("Float", self._floatIn)
        self.registerInPort("Double", self._doubleIn)

        self.registerInPort("ShortSeq", self._shortSeqIn)
        self.registerInPort("LongSeq", self._longSeqIn)
        self.registerInPort("FloatSeq", self._floatSeqIn)
        self.registerInPort("DoubleSeq", self._doubleSeqIn)



    def onExecute(self, ec_id):
        short_  = self._shortIn.read()
        long_   = self._longIn.read()
        float_  = self._floatIn.read()
        double_ = self._doubleIn.read()

        shortSeq_  = self._shortSeqIn.read()
        longSeq_   = self._longSeqIn.read()
        floatSeq_  = self._floatSeqIn.read()
        doubleSeq_ = self._doubleSeqIn.read()

        shortSize_  = len(shortSeq_.data)
        longSize_   = len(longSeq_.data)
        floatSize_  = len(floatSeq_.data)
        doubleSize_ = len(doubleSeq_.data)

        maxsize = max(shortSize_, longSize_, floatSize_, doubleSize_)
        shortSeq_.data  = shortSeq_.data  + ['-'] * (maxsize - shortSize_)
        longSeq_.data   = longSeq_.data   + ['-'] * (maxsize - longSize_)
        floatSeq_.data  = floatSeq_.data  + ['-'] * (maxsize - floatSize_)
        doubleSeq_.data = doubleSeq_.data + ['-'] * (maxsize - doubleSize_)

        print '%3.2s %10.8s %10.8s %10.8s %10.8s' \
            % (' ', 'short', 'long', 'float', 'double')
        print '%3.2s %10.8s %10.8s %10.8s %10.8s' \
            % (' ', short_.data, long_.data, float_.data, double_.data)
        print "---------------------------------------------------"
        print "                 Sequence Data                     "
        print "---------------------------------------------------"
        for i in range(maxsize):
            print '%3.2s %10.8s %10.8s %10.8s %10.8s' \
                % (i, shortSeq_.data[i], longSeq_.data[i], floatSeq_.data[i], doubleSeq_.data[i])

        # カーソルの移動   (^[[nA : n行上へ移動)
        print "\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r"

        time.sleep(0.5)
        return RTC.RTC_OK


def MyModuleInit(manager):
    profile = OpenRTM.Properties(defaults_str=seqin_spec)
    manager.registerFactory(profile,
                            SeqIn,
                            OpenRTM.Delete)

    # Create a component
    comp = manager.createComponent("SeqIn")


def main():
    # Initialize manager
    mgr = OpenRTM.Manager.init(len(sys.argv), sys.argv)

    # Set module initialization proceduer
    # This procedure will be invoked in activateManager() function.
    mgr.setModuleInitProc(MyModuleInit)

    # Activate manager and register to naming service
    mgr.activateManager()

    # run the manager in blocking mode
    # runManager(False) is the default
    mgr.runManager()

    # If you want to run the manager in non-blocking mode, do like this
    # mgr.runManager(True)

if __name__ == "__main__":
	main()

