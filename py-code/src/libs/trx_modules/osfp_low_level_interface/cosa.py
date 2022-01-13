from .broker import Broker
from .dpin import DPin
from .ain import Ain
from .aout import Aout

import time
import struct




class COSA:
    def __init__(self, broker):
        self._b = broker
        self._xpdc = Aout(broker, 'MCU2_TXPH1_DC')
        self._xidc = Aout(broker, 'MCU2_TXIH1_DC')
        self._xqdc = Aout(broker, 'MCU2_TXQH1_DC')
        self._ypdc = Aout(broker, 'MCU2_TYPH1_DC')
        self._yidc = Aout(broker, 'MCU2_TYIH1_DC')
        self._yqdc = Aout(broker, 'MCU2_TYQH1_DC')
        self._vofe_i = Ain(broker, 'VOFE_CURRENT_SEN')
        self._vofe_v = Ain(broker, 'P5V8_DRIVER_VOFE')
        self._xpac = Aout(broker, 'MCU2_TXPH1_AC')
        self._xiac = Aout(broker, 'MCU2_TXIH1_AC')
        self._xqac = Aout(broker, 'MCU2_TXQH1_AC')
        self._ypac = Aout(broker, 'MCU2_TYPH1_AC')
        self._yiac = Aout(broker, 'MCU2_TYIH1_AC')
        self._yqac = Aout(broker, 'MCU2_TYQH1_AC')        
        self._tx_voa_x = Aout(broker, 'MCU1_TX_VOA_X')   
        self._tx_voa_y = Aout(broker, 'MCU1_TX_VOA_Y')
        self._mpdx_dc = Ain(broker, 'POST_MPDX_DC_MCU2ADC')
        self._mpdy_dc = Ain(broker, 'POST_MPDY_DC_MCU2ADC')
        self._mpd_ac = Ain(broker, 'POST_MPDXY_AC_MCU2ADC')
        self._en_phbias = DPin(broker, 'COSA_PH_BIAS_EN')
        self._phbias = Ain(broker, 'COSA_PH_BIAS')

    @property
    def power(self):
        return 0

    @power.setter
    def power(self, val):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x04\x00\x00\x00\x0f\x0a\x01\x00')
        if val:  # power on
            cmd[-1] = 1
        else:
            cmd[-1] = 0
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        while self._b.cdb1_cip():
            pass

        if val:
            # self._phxpp.aval = 1.75
            # self._phxip.aval = 2.25
            # self._phxqp.aval = 2.25
            # self._phypp.aval = 1.75
            # self._phyip.aval = 2.25
            # self._phyqp.aval = 2.25
            # self._phxpn.aval = 0.7
            # self._phxin.aval = 0.7
            # self._phxqn.aval = 0.7
            # self._phypn.aval = 0.7
            # self._phyin.aval = 0.7
            # self._phyqn.aval = 0.7
            self._xpdc.aval = 1.35
            self._xidc.aval = 1.35
            self._xqdc.aval = 1.35
            self._ypdc.aval = 1.35
            self._yidc.aval = 1.35
            self._yqdc.aval = 1.35
 
            pass            


    @property
    def power1(self):
        return 0
    @power1.setter
    def power1(self, val):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x04\x00\x00\x00\x0f\x0a\x03\x00')
        if val:  # power on
            cmd[-1] = 1
        else:
            cmd[-1] = 0
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        while self._b.cdb1_cip():
            pass

        if val:
            self._xpdc.aval = 1.35
            self._xidc.aval = 1.35
            self._xqdc.aval = 1.35
            self._ypdc.aval = 1.35
            self._yidc.aval = 1.35
            self._yqdc.aval = 1.35
 
            pass    