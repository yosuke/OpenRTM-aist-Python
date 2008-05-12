#/usr/bin/env python
# -*- Python -*-

import sys
import string

import OpenRTM
import RTC
import _GlobalIDL

myserviceconsumer_spec = ["implementation_id", "MyServiceConsumer",
                          "type_name",         "MyServiceConsumer",
                          "description",       "MyService Consumer Sample component",
                          "version",           "1.0",
                          "vendor",            "Shinji Kurihara",
                          "category",          "example",
                          "activity_type",     "DataFlowComponent",
                          "max_instance",      "10",
                          "language",          "Python",
                          "lang_type",         "script",
                          ""]


class MyServiceConsumer(OpenRTM.DataFlowComponentBase):
    # constructor
    def __init__(self, manager):
        OpenRTM.DataFlowComponentBase.__init__(self, manager)

        # initialization of CORBA Port
        self._myServicePort = OpenRTM.CorbaPort("MyService")

        # initialization of Consumer
        self._myservice0 = OpenRTM.CorbaConsumer(interfaceType=_GlobalIDL.MyService)
        
        # Set service consumers to Ports
        self._myServicePort.registerConsumer("myservice0", "MyService", self._myservice0)

        # Set CORBA Service Ports
        self.registerPort(self._myServicePort)
        

    # The execution action that is invoked periodically
    def onExecute(self, ec_id):
        print "\n"
        print "Command list: "
        print " echo [msg]       : echo message."
        print " set_value [value]: set value."
        print " get_value        : get current value."
        print " get_echo_history : get input messsage history."
        print " get_value_history: get input value history."
        print "> ",

        args = str(sys.stdin.readline())
        argv = string.split(args)
        argv[-1] = argv[-1].rstrip("\n")

        if argv[0] == "echo" and len(argv) > 1:
            retmsg = ""
            retmsg = self._myservice0._ptr().echo(argv[1])
            print "echo return: ", retmsg
            return RTC.RTC_OK

        if argv[0] == "set_value" and len(argv) > 1:
            val = float(argv[1])
            self._myservice0._ptr().set_value(val)
            print "Set remote value: ", val
            return RTC.RTC_OK
      
        if argv[0] == "get_value":
            retval = self._myservice0._ptr().get_value()
            print "Current remote value: ", retval
            return RTC.RTC_OK;
      
        if argv[0] == "get_echo_history":
            OpenRTM.CORBA_SeqUtil.for_each(self._myservice0._ptr().get_echo_history(),
                                           self.seq_print())
            return RTC.RTC_OK
      
        if argv[0] == "get_value_history":
            OpenRTM.CORBA_SeqUtil.for_each(self._myservice0._ptr().get_value_history(),
                                           self.seq_print())
            return RTC.RTC_OK
      
        print "Invalid command or argument(s)."

        return RTC.RTC_OK


    # functor class to print sequence data
    class seq_print:
        def __init__(self):
            self._cnt = 0

        def __call__(self, val):
            print self._cnt, ": ", val
            self._cnt += 1


def MyModuleInit(manager):
    profile = OpenRTM.Properties(defaults_str=myserviceconsumer_spec)
    manager.registerFactory(profile,
                            MyServiceConsumer,
                            OpenRTM.Delete)

    # Create a component
    comp = manager.createComponent("MyServiceConsumer")



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
