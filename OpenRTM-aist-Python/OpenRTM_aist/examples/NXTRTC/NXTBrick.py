#!/usr/bin/env python
# -*- coding:shift_jis -*-

import nxt.locator
from nxt.sensor import *
from nxt.motor import *
import time

class NXTBrick:
    def __init__(self, bsock=None):
        """
        コンストラクタ
        NXTブロックへのコネクションを行い、モータや、センサオブジェクトを
        作成する。モータのエンコーダのリセットを行う。
        """
        if bsock:
            self.sock = bsock
        else:
            self.sock = nxt.locator.find_one_brick().connect()

        self.motors = [Motor(self.sock, PORT_A),
                       Motor(self.sock, PORT_B),
                       Motor(self.sock, PORT_C)]
            
        self.sensors = [TouchSensor(self.sock, PORT_1),
                        SoundSensor(self.sock, PORT_2),
                        LightSensor(self.sock, PORT_3),
                        UltrasonicSensor(self.sock, PORT_4)]
        self.resetPosition()

    def close(self):
        """
        NXTブロックとの接続を終了する
        """
        self.sock.close()

    def resetPosition(self, relative = 0):
        """
        NXTのモータのエンコーダをリセットする
        """
        for m in self.motors:
            m.reset_position(relative)

    def setMotors(self, vels):
        """
        配列を受け取り、モータのパワーとしてセットする。
        velsの数とモータの数が一致しない場合、両者の要素数のうち
        小さい方でループを回す。
        """
        for i, v in enumerate(vels[:min(len(vels),len(self.motors))]):
            self.motors[i].power = max(min(v,127),-127)
            self.motors[i].mode = MODE_MOTOR_ON | MODE_REGULATED
            self.motors[i].regulation_mode = REGULATION_MOTOR_SYNC
            self.motors[i].run_state = RUN_STATE_RUNNING
            self.motors[i].tacho_limit = 0
            self.motors[i].set_output_state()

    def getMotors(self):
        """
        モータの位置(角度)を取得する
        
        """
        state = []
        for m in self.motors:
            stat = None
            for i in range(3):
                try:
                    stat = m.get_output_state()
                    break
                except:
                    time.sleep(0.01)
                    self.getMotors()
                    continue

            if stat == None:
                import sys
                print "Unknown motor encoder error"
                print sys.exc_info()[1]
            state.append(stat)

        return state

    def getSensors(self):
        """
        センサの値を取得する。得られたデータは配列で返される。
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
                    self.getSensors()
                    continue
            if stat == None:
                import sys
                print "Unknown sensor error"
                print sys.exc_info()[1]
            state.append(stat)

        return state


"""
テストプログラム
モータに適当な出力を与え、角度を読み表示する。
センサから値を読み込み表示する。
"""
if __name__ == "__main__":
    import time
    nxt = NXTBrick()
    print "connected"
    
    # モータのテスト
    for i in range(0):
        nxt.setMotors([80,-80,80])
        print "Motor: "
        mstat = nxt.getMotors()
        for i, m in enumerate(mstat):
            print "(" , i, "): ", m
        time.sleep(0.1)
    nxt.setMotors([0,0,0])

    # センサのテスト
    for i in range(100):
        sensors = ["Touch", "Sound", "Light", "USonic"]
        sval = nxt.getSensors()
        print sval
        time.sleep(0.1)
