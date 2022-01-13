from .broker import Broker
import time
import struct
import math
from .fpn import cal


class DDM:
    def __init__(self, broker):
        self._b = broker

    @property
    def tx_bias(self):
        self._b.twi_sbw(126, b'\x00\x11')#switch page
        time.sleep(0.05)
        rsp = self._b.twi_srr(170,2)
        if 0 == struct.unpack('>H', rsp)[0]:
            return 0
        return struct.unpack('>H', rsp)[0] / 125.0 #mA

    @property
    def tx_power(self):
        self._b.twi_sbw(126, b'\x00\x11')#switch page
        time.sleep(0.05)
        rsp = self._b.twi_srr(154,2)
        if 0 == struct.unpack('>H', rsp)[0]:
            return 0
        return 10 * math.log(struct.unpack('>H', rsp)[0] / 10000.0, 10)

    # @tx_power.setter
    # def tx_power(self, val):
    #     val = val * 100
    #     print(val)
    #     self._b.mdio_write(0xb410, int(val))

    @property
    def rx_power(self):
        self._b.twi_sbw(126, b'\x00\x11')#switch page
        time.sleep(0.05)
        rsp = self._b.twi_srr(186,2)
        if 0 == struct.unpack('>H', rsp)[0]:
            return 0
        return 10 * math.log(struct.unpack('>H', rsp)[0] / 10000.0, 10)

    # @property
    # def siop(self):
    #     val = self._b.mdio_read(0xb5ce)
    #     return ctypes.c_int16(val).value / 100.0

    @property
    def vcc(self):
        rsp = self._b.twi_srr(16,2)
        return struct.unpack('>H', rsp)[0] / 10000.0


    @property
    def case_temp(self):
        rsp = self._b.twi_srr(14,2)
        caseTemp = struct.unpack('>h', rsp)[0]
        return caseTemp / 256.0

    @property
    def laser_temp(self):
        rsp = self._b.twi_srr(20,2)
        laserTemp = struct.unpack('>h', rsp)[0]
        return laserTemp / 256.0

    @property
    def dsp_temp(self):
        rsp = self._b.twi_srr(24,2)
        dspTemp = struct.unpack('>h', rsp)[0]
        return dspTemp / 256.0

    @property
    def dsp_die_temp(self):
        self._b.twi_sbw(126, b'\x00\xff')#switch page
        time.sleep(0.05)
        rsp = self._b.twi_srr(128,8)

        hrx2 = cal(struct.unpack('<H', rsp[0:2])[0], 's', 11, 2)
        lrx = cal(struct.unpack('<H', rsp[2:4])[0], 's', 11, 2)
        ltx_v = cal(struct.unpack('<H', rsp[4:6])[0], 's', 11, 2)
        htx_top0 = cal(struct.unpack('<H', rsp[6:8])[0], 's', 11, 2)

        return hrx2,lrx,ltx_v,htx_top0

    # @property
    # def dsp_avg_temp(self):
    #     ret='{:016b}'.format(self._b.mdio_read(0xb5e0))
    #     val_h = ret[0:8]
    #     val_l = ret[8:16]
    #     val_l_sum = 0
    #     idx = [-8, -7, -6, -5, -4, -3, -2, -1]
    #     for i in range(0,8):
    #         val_l_sum += 2 ** idx[i] * int(val_l[i])
        
    #     return round( (int(val_h,2) + val_l_sum), 2)
