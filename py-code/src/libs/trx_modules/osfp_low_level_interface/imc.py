from .broker import Broker
import struct


class IMC:
    def __init__(self, broker):
        self._b = broker

    def regw(self, addr, data):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(
            b'\x80\x00\x00\x00\x08\x00\x00\x00\x0e\x03\x00\x01\x00\x00\x00\x00')
        cmd[-4] = (addr >> 8) & 0xff
        cmd[-3] = addr & 0xff
        cmd[-2] = (data >> 8) & 0xff
        cmd[-1] = data & 0xff
        cmd[133-128] = self._b.cdb_chkcode(cmd)             
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        while self._b.cdb1_cip():
            pass




    def regr(self, addr):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(
            b'\x80\x00\x00\x00\x06\x00\x00\x00\x0e\x03\x00\x02\x00\x00')
        cmd[-2] = (addr >> 8) & 0xff
        cmd[-1] = addr & 0xff
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        while self._b.cdb1_cip():
            pass

        if self._b.cdb1_success():
            print('cdb suc.\n')
            rlplen = self._b.twi_rr(134)
            rlp_chkcode = self._b.twi_rr(135)
            rlp = self._b.twi_srr(136, rlplen)
            print(rlp)
            if self._b.cdb_chkcode(rlp) == rlp_chkcode:
                val = struct.unpack('>1H', rlp[0:2])[0]
                return val

        print('cdb failed.\n')
        return 0xffff
