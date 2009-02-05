#/usr/bin/env python
# -*- Python -*-

import sys

from omniORB import CORBA

import OpenRTM_aist
import RTC


def main():

    # subscription type
    subs_type = "Flush"

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


    # connect ports
    conprof = RTC.ConnectorProfile("connector0", "", [pin[0],pout[0]], [])
    OpenRTM_aist.CORBA_SeqUtil.push_back(conprof.properties,
                                         OpenRTM_aist.NVUtil.newNV("dataport.interface_type",
                                                                   "CORBA_Any"))

    OpenRTM_aist.CORBA_SeqUtil.push_back(conprof.properties,
                                         OpenRTM_aist.NVUtil.newNV("dataport.dataflow_type",
                                                                   "Push"))

    OpenRTM_aist.CORBA_SeqUtil.push_back(conprof.properties,
                                         OpenRTM_aist.NVUtil.newNV("dataport.subscription_type",
                                                                   subs_type))

    ret = pin[0].connect(conprof)
    
    # activate ConsoleIn0
    eclistin = inobj.get_owned_contexts()
    eclistin[0].activate_component(inobj)

    # activate ConsoleOut0
    eclistout = outobj.get_owned_contexts()
    eclistout[0].activate_component(outobj)



if __name__ == "__main__":
	main()
