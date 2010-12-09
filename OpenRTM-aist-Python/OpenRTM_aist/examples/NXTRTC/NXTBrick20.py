#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

import nxt.locator
from nxt.sensor import *
from nxt.motor import *
import time

class NXTBrick:
  def __init__(self, bsock=None):
    """
    Ctor
    Connecting to NXT brick and creating motor object, sensor object
    and so on. Motor encoders will be reset.
    """
    if bsock:
      self.sock = bsock
    else:
      #self.sock = nxt.locator.find_one_brick().connect()
      print "connect 0"
      self.sock = nxt.locator.find_one_brick()
      print "connect 1"

    print "deb0"
    self.motors = [Motor(self.sock, PORT_A),
                   Motor(self.sock, PORT_B),
                   Motor(self.sock, PORT_C)]
            
    print "deb1"
    self.sensors = [Touch(self.sock, PORT_1),
                    Sound(self.sock, PORT_2),
                    Light(self.sock, PORT_3),
                    Ultrasonic(self.sock, PORT_4)]
    print "deb2"
    self.resetPosition()
    print "deb3"

  def close(self):
    """
    Finalizing connection with NXT brick.
    """
    self.sock.close()

  def resetPosition(self, relative = 0):
    """
    Resetting encoders of NXT motors
    """
    for m in self.motors:
      m.reset_position(relative)

  def setMotors(self, vels):
    """
    This operation receives array and set them as motor power.  If the
    number of vels items does not match with the number of motors,
    smaller number of them will be taken and set respectively.
    """
    for i, v in enumerate(vels[:min(len(vels),len(self.motors))]):
      print "setMotors0"
      self.motors[i].sync = 1
      print "setMotors1"
      self.motors[i].weak_turn(max(min(v,127),-127),0)
      print "setMotors2"
      """
      self.motors[i].power = max(min(v,127),-127)
      print "setMotors1"
      self.motors[i].mode = MODE_MOTOR_ON | MODE_REGULATED
      print "setMotors2"
      self.motors[i].regulation = REGULATION_MOTOR_SYNC
      print "setMotors3"
      self.motors[i].run_state = RUN_STATE_RUNNING
      print "setMotors4"
      self.motors[i].tacho_limit = 0
      print "setMotors5"
      self.motors[i].set_output_state()
      """

  def getMotors(self):
    """
    Getting motors' angle (degrees)
    """
    state = []
    for m in self.motors:
      stat = None
      for i in range(3):
        try:
          #stat = m.get_output_state()
          stat = m.get_tacho().tacho_count
          break
        except:
          time.sleep(0.01)
          continue

      if stat == None:
        import sys
        print "Unknown motor encoder error"
        print sys.exc_info()[1]
      state.append(stat)

    return state


  def getSensors(self):
    """
    Getting sensors' values. Data will be returned as array.
    """
    state = []
    for s in self.sensors:
      stat = None
      for i in range(3):
        try:
          stat = s.get_sample()
          break
        except:
          time.sleep(0.01)
          continue
      if stat == None:
        import sys
        print "Unknown sensor error"
        print sys.exc_info()[1]
      state.append(stat)

    return state


"""
Test program
It gives appropriate values to motors, and angles of motors are
obtained and shown.  Sensor data are also obtained and shown.
"""
if __name__ == "__main__":
  import time
  nxt = NXTBrick()
  print "connected"
    
  # Testing motors
  for i in range(0):
    nxt.setMotors([80,-80,80])
    print "Motor: "
    mstat = nxt.getMotors()
    for i, m in enumerate(mstat):
      print "(" , i, "): ", m
    time.sleep(0.1)
  nxt.setMotors([0,0,0])

  # Testing sensors
  for i in range(100):
    sensors = ["Touch", "Sound", "Light", "USonic"]
    sval = nxt.getSensors()
    print sval
    time.sleep(0.1)
