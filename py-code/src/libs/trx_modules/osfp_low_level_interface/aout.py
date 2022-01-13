from .broker import Broker
import struct

class Aout:
    IDS = '''
        DRIVER_VGC_XI
        DRIVER_VGC_YI
        DRIVER_VGC_XQ
        DRIVER_VGC_YQ
        MCU1_TX_VOA_X
        MCU1_TX_VOA_Y
        DRIVER_VT
        MCU1_DAC_TX_PN_BIAS
        COSA_VOFE_FB
        P0V55_DSP_FB

        MCU2_TXIH1_AC
        MCU2_TXIH1_DC
        MCU2_TXQH1_DC
        MCU2_TYIH1_DC
        MCU2_TYQH1_DC
        MCU2_TXQH1_AC
        MCU2_TYIH1_AC
        MCU2_TYQH1_AC
        MCU2_TXPH1_DC
        MCU2_TYPH1_DC
        MCU2_TXPH1_AC
        MCU2_TYPH1_AC

        DAC_TIA_VOA_YI
        DAC_TIA_VOA_XI
        DAC_TIA_VOA_YQ
        DAC_TIA_VOA_XQ

        DAC_RX_VOA_X
        DAC_RX_VOA_Y

        DAC_RX_IQ_PH_X
        DAC_RX_IQ_PH_Y

        ABC_VGA_R
    '''.split()

    def __init__(self, broker, id):
        self._b = broker
        self._id = self.IDS.index(id)

        
    def __str__(self):
        return str({self.IDS[self._id]: self.val})

    @property
    def name(self):
        return self.IDS[self._id]

    @property
    def dval(self):
        dval, aval, raw_aval = self.val
        return dval

    @property
    def aval(self):
        dval, aval, raw_aval = self.val
        return aval

    @property
    def raw_aval(self):
        dval, aval, rawAval = self.val
        return rawAval

    @property
    def val(self):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x04\x00\x00\x00\x0f\x05\x00\x01')
        cmd[-2] = self._id
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        while self._b.cdb1_cip():
            pass

        if self._b.cdb1_success():
            rlplen = self._b.twi_rr(134)
            rlp_chkcode = self._b.twi_rr(135)
            rlp = self._b.twi_srr(136, rlplen)
            if self._b.cdb_chkcode(rlp) == rlp_chkcode:
                _dval = struct.unpack('>1H', rlp[0:2])[0]       
                _aval = struct.unpack('<1f', rlp[2:6])[0]
                _raw_aval = struct.unpack('<1f', rlp[6:])[0]
                return (_dval, _aval, _raw_aval)

        return (0, 0.0, 0.0)

    @aval.setter
    def aval(self, v):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x08\x00\x00\x00\x0f\x05\x00\x03\x00\x00\x00\x00')
        cmd[-6] = self._id
        # print(v)
        vs = struct.pack('<1f', v)
        # print(vs)
        cmd[-4] = vs[0]
        cmd[-3] = vs[1]
        cmd[-2] = vs[2]
        cmd[-1] = vs[3]
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        while self._b.cdb1_cip():
            pass

    @dval.setter
    def dval(self, v):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x06\x00\x00\x00\x0f\x05\x00\x02\x00\x00')
        cmd[-4] = self._id
        cmd[-2] = v >> 8
        cmd[-1] = v & 0xff
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        while self._b.cdb1_cip():
            pass
