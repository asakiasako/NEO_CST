from .broker import Broker

class SPI:
    def __init__(self, broker, port, cs):
        self._b = broker
        self._port = port
        self._cs = cs

    def tx(self, data):
        while not self._b.cdb1_idle():
            pass
        # self._cs.state = 0
        self._b.mdio_write(0x9c02, 0x01)
        self._b.mdio_write(0x9c03, self._port)
        for i in range(len(data)):
            self._b.mdio_write(0x9c04 + i, data[i])
        self._b.mdio_write(0x9c01, len(data) + 2)
        self._b.mdio_write(0x9c00, 0x0e02)
        while self._b.cdb1_cip():
            pass
        # self._cs.state = 1

    def rx(self, len):
        while not self._b.cdb1_idle():
            pass
        # self._cs.state = 0
        self._b.mdio_write(0x9c02, 0x02)
        self._b.mdio_write(0x9c03, self._port)
        self._b.mdio_write(0x9c04, len)
        self._b.mdio_write(0x9c01, 3)
        self._b.mdio_write(0x9c00, 0x0e02)
        while self._b.cdb1_cip():
            pass
        # self._cs.state = 1
        data = bytearray()
        len = self._b.mdio_read(0x9c01)
        for i in range(len):
            data.append(self._b.mdio_read(0x9c02 + i))
        return data

    def trx(self, data):
        while not self._b.cdb1_idle():
            pass
        # self._cs.state = 0
        self._b.mdio_write(0x9c02, 0x03)
        self._b.mdio_write(0x9c03, self._port)
        for i in range(len(data)):
            self._b.mdio_write(0x9c04 + i, data[i])
        self._b.mdio_write(0x9c01,len(data) + 2)
        self._b.mdio_write(0x9c00, 0x0e02)
        while self._b.cdb1_cip():
            pass
        # self._cs.state = 1
        data = bytearray()
        rxlen = self._b.mdio_read(0x9c01)
        for i in range(rxlen):
            data.append(self._b.mdio_read(0x9c02 + i))
        return data

    def configs(self, config):
        while not self._b.cdb1_idle():
            pass
        self._b.mdio_write(0x9c02, 0x04)
        self._b.mdio_write(0x9c03, self._port)
        self._b.mdio_write(0x9c04, config)
        self._b.mdio_write(0x9c01, 3)
        self._b.mdio_write(0x9c00, 0x0e02)
        while self._b.cdb1_cip():
            pass
    
    def configg(self):
        while not self._b.cdb1_idle():
            pass
        self._b.mdio_write(0x9c02, 0x04)
        self._b.mdio_write(0x9c03, self._port)
        self._b.mdio_write(0x9c01, 2)
        self._b.mdio_write(0x9c00, 0x0e02)
        while self._b.cdb1_cip():
            pass
        return self._b.mdio_read(0x9c02)

    def status(self):
        while not self._b.cdb1_idle():
            pass
        self._b.mdio_write(0x9c02, 0x05)
        self._b.mdio_write(0x9c03, self._port)
        self._b.mdio_write(0x9c01, 2)
        self._b.mdio_write(0x9c00, 0x0e02)
        while self._b.cdb1_cip():
            pass
        return self._b.mdio_read(0x9c02)