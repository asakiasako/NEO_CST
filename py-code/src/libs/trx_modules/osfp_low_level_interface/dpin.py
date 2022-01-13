from .broker import Broker

class DPin:
    IDS = '''
        MCU1_DSP_SPI_CS
        MCU1_FLASH_SPI_CS
        MCU1_ADC3_SPI_CS
        ADC4_SPI_CS
        DSP_LINE_LOS
        DSP_INTN_0
        CLK_SEC
        DSP_INTN_1
        M_LPWN
        M_INT
        MCU2_MCU1_INTN_I
        MCU1_FLASH_RSTN
        MCU1_OUT_RST_N
        MCU1_DSP_RSTN
        P0V55_DSP_EN
        P1V8_DSP_EN
        P1V2_DSP_EN
        PS_EN
        COSA_VOFE_EN
        TX_DRIVER_VCC_EN
        P0V94_DSP_EN
        P0V75_DSP_EN

        MCU2_MCU1_INTN_O
        M_LPWN_ABC
        MCU2_ADC12_SPI_CS1
        MCU2_ADC12_SPI_CS2
        RX_TIA_BWH
        RX_TIA_BWL
        RX_TIA_SD
        RX_TIA_MC
        ITLA_OIF_MS_N
        ITLA_OIF_SRQ_N
        ITLA_OIF_DIS_N
        ITLA_OIF_RST_N
        RX_TIA_VCC_XY_EN
        COSA_VPD_EN
        P6V_EN
        COSA_PH_BIAS_EN
    '''.split()

    def __init__(self, broker, id):
        self._b = broker
        self._id = self.IDS.index(id)
        self._valid = False
        self._state = False

    def __str__(self):
        return str( {self.IDS[self._id]:self.state})

    @property
    def valid(self):
        return self._valid

    @property
    def state(self):
        while not self._b.cdb1_idle():
            pass
        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x03\x00\x00\x00\x0f\x02\x00')
        cmd[-1] = self._id
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
                self._valid = True
                self._state = rlp[0]
            else:
                self._valid = False
        else:
            self._valid = False
        return self._state

    @state.setter
    def state(self, val):
        while not self._b.cdb1_idle():
            pass
        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x04\x00\x00\x00\x0f\x03\x00\x00')
        cmd[-2] = self._id
        cmd[-1] = val
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        while self._b.cdb1_cip():
            pass
