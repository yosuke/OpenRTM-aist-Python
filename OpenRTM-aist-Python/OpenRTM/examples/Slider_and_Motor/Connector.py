#/usr/bin/env python
# -*- Python -*-

import sys

from omniORB import CORBA

import OpenRTM
import RTC


def main():

    # subscription type
    subs_type = "Flush"

    # initialization of ORB
    orb = CORBA.ORB_init(sys.argv)

    # get NamingService
    naming = OpenRTM.CorbaNaming(orb, "localhost")
    
    sl  = OpenRTM.CorbaConsumer()
    tkm = OpenRTM.CorbaConsumer()

    # find ConsoleIn0 component
    tkm.setObject(naming.resolve("TkMotorComp0.rtc"))

    # get ports
    inobj = tkm.getObject()._narrow(RTC.RTObject)
    pin = inobj.get_ports()
    pin[0].disconnect_all()


    # find ConsoleOut0 component
    sl.setObject(naming.resolve("SliderComp0.rtc"))

    # get ports
    outobj = sl.getObject()._narrow(RTC.RTObject)
    pout = outobj.get_ports()
    pout[0].disconnect_all()


    # connect ports
    conprof = RTC.ConnectorProfile("connector0", "", [pin[0],pout[0]], [])
    OpenRTM.CORBA_SeqUtil.push_back(conprof.properties,
                                    OpenRTM.NVUtil.newNV("dataport.interface_type",
                                                         "CORBA_Any"))

    OpenRTM.CORBA_SeqUtil.push_back(conprof.properties,
                                    OpenRTM.NVUtil.newNV("dataport.dataflow_type",
                                                         "Push"))

    OpenRTM.CORBA_SeqUtil.push_back(conprof.properties,
                                    OpenRTM.NVUtil.newNV("dataport.subscription_type",
                                                         subs_type))

    ret = pin[0].connect(conprof)
    
    # activate ConsoleIn0
    eclistin = inobj.get_execution_context_services()
    eclistin[0].activate_component(inobj)

    # activate ConsoleOut0
    eclistout = outobj.get_execution_context_services()
    eclistout[0].activate_component(outobj)



if __name__ == "__main__":
	main()
