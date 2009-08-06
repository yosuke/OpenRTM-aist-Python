#/usr/bin/env python
# -*- Python -*-

import sys

from omniORB import CORBA

import OpenRTM_aist
import RTC

def usage():
    print "usage: ConnectorComp [options]"
    print "  --flush         "
    print ": Set subscription type Flush"
    print "  --new           "
    print ": Set subscription type New"
    print "  --periodic [Hz] "
    print ": Set subscription type Periodic \n"

def main():

    # initialization of ORB
    orb = CORBA.ORB_init(sys.argv)

    # get NamingService
    naming = OpenRTM_aist.CorbaNaming(orb, "localhost")
    
    conin = OpenRTM_aist.CorbaConsumer()
    conout = OpenRTM_aist.CorbaConsumer()

    # find ConsoleIn0 component
    conin.setObject(naming.resolve("ConsoleIn0.rtc"))

    # get ports
    inobj = conin.getObject()._narrow(RTC.RTObject)
    pin = inobj.get_ports()
    pin[0].disconnect_all()


    # find ConsoleOut0 component
    conout.setObject(naming.resolve("ConsoleOut0.rtc"))

    # get ports
    outobj = conout.getObject()._narrow(RTC.RTObject)
    pout = outobj.get_ports()
    pout[0].disconnect_all()


    # subscription type
    subs_type = "flush"
    period = ""

    for arg in sys.argv[1:]:
        if arg == "--flush":
            subs_type = "flush"
            break
        elif arg == "--new":
            subs_type = "new"
            break
        elif arg == "--periodic":
            subs_type = "periodic"
        elif sbus_type == "periodic" and type(arg) == float:
            period = srt(arg)
            break
        else:
            usage()
            
    # connect ports
    conprof = RTC.ConnectorProfile("connector0", "", [pin[0],pout[0]], [])
    OpenRTM_aist.CORBA_SeqUtil.push_back(conprof.properties,
                                         OpenRTM_aist.NVUtil.newNV("dataport.interface_type",
                                                                   "corba_cdr"))

    OpenRTM_aist.CORBA_SeqUtil.push_back(conprof.properties,
                                         OpenRTM_aist.NVUtil.newNV("dataport.dataflow_type",
                                                                   "push"))

    OpenRTM_aist.CORBA_SeqUtil.push_back(conprof.properties,
                                         OpenRTM_aist.NVUtil.newNV("dataport.subscription_type",
                                                                   subs_type))

    if period:
        OpenRTM_aist.CORBA_SeqUtil.push_back(conprof.properties,
                                             OpenRTM_aist.NVUtil.newNV("dataport.push_interval",
                                                                       period))


    ret = pin[0].connect(conprof)
    
    # activate ConsoleIn0
    eclistin = inobj.get_owned_contexts()
    eclistin[0].activate_component(inobj)

    # activate ConsoleOut0
    eclistout = outobj.get_owned_contexts()
    eclistout[0].activate_component(outobj)



if __name__ == "__main__":
	main()
