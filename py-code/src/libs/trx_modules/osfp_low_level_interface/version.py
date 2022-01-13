from .broker import Broker

class Version:
    def __init__(self, broker):
        self._b = broker

    def refresh(self):
        while not self._b.cdb1_idle():
            pass
        self._b.mdio_write(0x9c00, 0x0f01)
        while True:
            val = self._b.mdio_read(0x9c00)
            if (val & 0xff00 == 0x0100):
                break
        if 6 == self._b.mdio_read(0x9c01):
            self._valid = True
            results = {}
            if (1 == self._b.mdio_read(0x9c02)):
                self._a_image = hex((self._b.mdio_read(0x9c04) << 16) | self._b.mdio_read(0x9c05))
            else:
                self._a_image = 'INVALID'
            if (1 == self._b.mdio_read(0x9c03)):
                self._b_image = hex((self._b.mdio_read(0x9c06) << 16) | self._b.mdio_read(0x9c07))
            else:
                self._b_image = 'INVALID'
        else:
            self._valid = False

    def __str__(self):
        self.refresh()
        if self._valid:
            results = {}
            results['A_image'] = self._a_image
            results['B_image'] = self._b_image
            return results.__str__()
        else:
            return 'ACCESS ERROR'

    @property
    def valid(self):
        return self._valid