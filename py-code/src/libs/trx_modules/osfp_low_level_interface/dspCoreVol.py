from .broker import Broker

class DspCoreVol:
    def __init__(self, broker):
        self._b = broker
        self.VREF = 1.234
        self.FBDIV = 1.0
        self.BUCK2_FBDIV = 0.6
    def read(self, regAddr):
        while not self._b.cdb1_idle():
            pass
        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x04\x00\x00\x00\x0f\x0b\x01\x00')
        cmd[-1] = regAddr
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
                return rlp[0]
            else:
                return 0

    def write(self, regAddr, val):
        while not self._b.cdb1_idle():
            pass
        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x05\x00\x00\x00\x0f\x0b\x02\x00\x00')
        cmd[-2] = regAddr
        cmd[-1] = val
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        while self._b.cdb1_cip():
            pass
        
    @property
    def buck1_vol(self):
        ldac = ((self.read(0x72) << 2) | (self.read(0x73) >> 6))
        print(ldac)
        voltage = (self.VREF / self.FBDIV) * (ldac / 1023.0)
        return voltage
        
    @buck1_vol.setter
    def buck1_vol(self, voltage):
        ldac = int((voltage * self.FBDIV * 1023.0) / self.VREF)
        print(ldac)
        self.write(0x72, (ldac >> 2) & 0xff)
        self.write(0x73, (ldac & 0x3) << 6)

    @property
    def buck2_vol(self):
        ldac = ((self.read(0x8e) << 2) | (self.read(0x8f) >> 6))
        print(ldac)
        voltage = (self.VREF / self.BUCK2_FBDIV) * (ldac / 1023.0)
        return voltage
        
    @buck2_vol.setter
    def buck2_vol(self, voltage):
        ldac = int((voltage * self.BUCK2_FBDIV * 1023.0) / self.VREF)
        print(ldac)
        self.write(0x8e, (ldac >> 2) & 0xff)
        self.write(0x8f, (ldac & 0x3) << 6)