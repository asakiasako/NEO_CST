from .broker import Broker
import struct
import time

class Ain:
    IDS = '''
        TX_DRIVER_PI_XI
        TX_DRIVER_PI_XQ
        TX_DRIVER_PI_YI
        TX_DRIVER_PI_YQ
        COSA_TEMP_OUT
        TX_DRV_VOCM
        RX_TIA_PI_XI
        VOFE_CURRENT_SEN
        MCU1_RX_TIA_PI_YI
        TX_VOA_X
        TX_VOA_Y
        REF2V5_MCU_ABC
        TX_VOA_X_I
        TX_VOA_Y_I
        MCU1INTERNAL_TEMP_SNS
        MCU1INTERNAL_AVDD
        MCU1INTERNAL_IOVDD0
        MCU1INTERNAL_IOVDD1

        P0V55_DSP_VDDC
        P0V75_DSP_VDDM
        P0V94_DSP_VDDA
        P1V8_DSP_VDDA18
        P1V2_DSP_VDDA12
        P3V_ABC_TXMPD
        PCB_TEMP_ADC
        DSP_TEMP

        POST_MPDX_DC_MCU2ADC
        POST_MPDY_DC_MCU2ADC
        POST_MPDXY_AC_MCU2ADC
        RX_VOA_X
        TIA_PD_BIAS
        TIA_VCC
        RX_VOA_Y
        RX_MPD_X_MCU2
        RX_TIA_PI_XQ
        RX_TIA_PI_YI
        RX_TIA_PI_YQ
        RX_VOA_X_I
        RX_MPD_Y_MCU2
        RX_VOA_Y_I
        MCU2INTERNAL_TEMP_SNS
        MCU2INTERNAL_AVDD
        MCU2INTERNAL_IOVDD0
        MCU2INTERNAL_IOVDD1
        
        ADC_TIA_VGC_YQ
        ADC_TIA_VGC_YI
        ADC_TIA_VGC_XQ
        ADC_TIA_VGC_XI
        TX_DRV_VCC
        P5V8_DRIVER_VOFE
        P6V_VOA
        COSA_PH_BIAS
    '''.split()

    def __init__(self, broker, id):
        self._b = broker
        self._id = self.IDS.index(id)
        
    def __str__(self):
        return str({self.IDS[self._id]: self.val})

    @property
    def dval(self):
        dval, aval, rawAval = self.val
        return dval

    @property
    def name(self):
        return self.IDS[self._id]

    @property
    def aval(self):
        dval, aval, rawAval = self.val
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
        cmd = bytearray(b'\x80\x00\x00\x00\x03\x00\x00\x00\x0f\x04\x00')
        cmd[-1] = self._id
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        while self._b.cdb1_cip():
            pass

        if self._b.cdb1_success():
            # print('cdb suc.\n')
            rlplen = self._b.twi_rr(134)
            rlp_chkcode = self._b.twi_rr(135)
            rlp = self._b.twi_srr(136, rlplen)
            # print(rlp)
            if self._b.cdb_chkcode(rlp) == rlp_chkcode:
                _dval = struct.unpack('>1H', rlp[0:2])[0]       
                _aval = struct.unpack('<1f', rlp[2:6])[0]
                _raw_aval = struct.unpack('<1f', rlp[6:])[0]
                return (_dval, _aval, _raw_aval)

        print('cdb failed.\n')
        return (0, 0.0, 0.0)

    # adc averaged value
    @property
    def dval_a(self):
        dval, aval, rawAval = self.val_a
        return dval


    @property
    def aval_a(self):
        dval, aval, rawAval = self.val_a
        return aval

    @property
    def raw_aval_a(self):
        dval, aval, rawAval = self.val_a
        return rawAval

    @property
    def val_a(self):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x03\x00\x00\x00\x0f\x84\x00')
        cmd[-1] = self._id
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])

        time.sleep(0.1)
        while self._b.cdb1_cip():
            
            pass

        if self._b.cdb1_success():
            # print('cdb suc.\n')
            rlplen = self._b.twi_rr(134)
            rlp_chkcode = self._b.twi_rr(135)
            rlp = self._b.twi_srr(136, rlplen)
            # print(rlp)
            if self._b.cdb_chkcode(rlp) == rlp_chkcode:
                _dval = struct.unpack('>1H', rlp[0:2])[0]       
                _aval = struct.unpack('<1f', rlp[2:6])[0]
                _raw_aval = struct.unpack('<1f', rlp[6:])[0]
                return (_dval, _aval, _raw_aval)

        print('cdb failed.\n')
        return (0, 0.0, 0.0)
