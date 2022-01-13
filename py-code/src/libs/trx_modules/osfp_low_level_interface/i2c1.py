from .broker import Broker

class I2C1:
    def __init__(self, broker):
        self._b = broker

    def tx(self, addr, data):
        while not self._b.cdb1_idle():
            pass
        self._b.mdio_write(0x9c02, 0x01)
        self._b.mdio_write(0x9c03, addr)
        for i in range(len(data)):
            self._b.mdio_write(0x9c04 + i, data[i])
        self._b.mdio_write(0x9c01, len(data) + 2)
        self._b.mdio_write(0x9c00, 0x0e01)
        while self._b.cdb1_cip():
            pass

    def rx(self, addr, len):
        while not self._b.cdb1_idle():
            pass
        self._b.mdio_write(0x9c02, 0x02)
        self._b.mdio_write(0x9c03, addr)
        self._b.mdio_write(0x9c04, len)
        self._b.mdio_write(0x9c01, 3)
        self._b.mdio_write(0x9c00, 0x0e01)
        while self._b.cdb1_cip():
            pass
        data = bytearray()
        len = self._b.mdio_read(0x9c01)
        for i in range(len):
            data.append(self._b.mdio_read(0x9c02 + i))
        return data

    def rrx(self, addr, reg, len):
        while not self._b.cdb1_idle():
            pass
        self._b.mdio_write(0x9c02, 0x03)
        self._b.mdio_write(0x9c03, addr)
        self._b.mdio_write(0x9c04, reg)
        self._b.mdio_write(0x9c05, len)
        self._b.mdio_write(0x9c01, 4)
        self._b.mdio_write(0x9c00, 0x0e01)
        while self._b.cdb1_cip():
            pass
        data = bytearray()
        len = self._b.mdio_read(0x9c01)
        for i in range(len):
            data.append(self._b.mdio_read(0x9c02 + i))
        return data