#/usr/bin/env python
# -*- Python -*-

import sys

import OpenRTM
import RTC

consolein_spec = ["implementation_id", "ConsoleIn",
                  "type_name",         "ConsoleIn",
                  "description",       "Console input component",
                  "version",           "1.0",
                  "vendor",            "Shinji Kurihara",
                  "category",          "example",
                  "activity_type",     "DataFlowComponent",
                  "max_instance",      "10",
                  "language",          "Python",
                  "lang_type",         "script",
                  ""]


class ConsoleIn(OpenRTM.DataFlowComponentBase):
    def __init__(self, manager):
        OpenRTM.DataFlowComponentBase.__init__(self, manager)
        self._data = RTC.TimedLong(RTC.Time(0,0),0)
        self._outport = OpenRTM.OutPort("out", self._data, OpenRTM.RingBuffer(8))

        # Set OutPort buffer
        self.registerOutPort("out", self._outport)

        
    def onExecute(self, ec_id):
        print "Please input number: ",
        self._data.data = long(sys.stdin.readline())
        print "Sending to subscriber: ", self._data.data
        self._outport.write()
        return RTC.RTC_OK


def MyModuleInit(manager):
    profile = OpenRTM.Properties(defaults_str=consolein_spec)
    manager.registerFactory(profile,
                            ConsoleIn,
                            OpenRTM.Delete)

    # Create a component
    comp = manager.createComponent("ConsoleIn")


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
