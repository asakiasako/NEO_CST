import struct
from .broker import Broker

class EEPROM:
    PAGE_SIZE = 32

    def __init__(self, broker):
        self._b = broker

    def read(self, addr, len):
        while not self._b.cdb1_idle():
            pass
        self._b.mdio_write(0x9c02, 0x01)#sub cmd, read
        self._b.mdio_write(0x9c03, len)
        self._b.mdio_write(0x9c04, addr)
        self._b.mdio_write(0x9c01, 3)
        self._b.mdio_write(0x9c00, 0x0f0c)
        while self._b.cdb1_cip():
            pass
        data = []
        if 1 == len:
            r = self._b.mdio_read(0x9c02)
            data.append(r & 0xFF)
        else:
             for i in range(len//2):
                 r = self._b.mdio_read(0x9c02 + i)
                 data.append(r & 0xFF)
                 data.append(r >> 8)
             if len%2:
                 r = self._b.mdio_read(0x9c02 + len//2)
                 data.append(r >> 8)
        return data


    def write(self, addr, len, data):
        while not self._b.cdb1_idle():
            pass
        self._b.mdio_write(0x9c02, 0x02)#sub cmd, write
        self._b.mdio_write(0x9c03, len)#byte length
        self._b.mdio_write(0x9c04, addr)
        if 1 == len:
            self._b.mdio_write(0x9c05, data)
            tlen = 4
        else:
            for i in range(len//2):
                self._b.mdio_write(0x9c05+i, ((data[2*i+1] & 0xFF) << 8) | (data[2*i] & 0xFF))
            if len%2:
                self._b.mdio_write(0x9c05+len//2, (data[len-1] & 0xFF))
            tlen = len//2 + len%2 + 3
        self._b.mdio_write(0x9c01, tlen)
        self._b.mdio_write(0x9c00, 0x0f0c)
        while self._b.cdb1_cip():
            pass
