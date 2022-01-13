import struct
import time
from .broker import Broker

class Flash:
    PAGE_SIZE = 256
    PAGE_COUNT = 4 * 4 * 2 * 1024
    SECTOR_SIZE = 4 * 1024
    SECTOR_COUNT = 2 * 1024
    SIZE = SECTOR_SIZE * SECTOR_COUNT

    def __init__(self, broker):
        self._b = broker


    @property
    def id(self):
        while not self._b.cdb1_idle():
            pass
        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x03\x00\x00\x00\x0f\x06\x00')
        cmd[-1] = 1
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
                data = bytearray()
                for i in range(rlplen):
                    data.append(rlp[i])
                return ''.join(format(b, '02x') for b in data)

    def erase_sector(self, sec):
        while not self._b.cdb1_idle():
            time.sleep(0.1)
            pass
        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x05\x00\x00\x00\x0f\x06\x02\x00\x00')
        cmd[-2] = (sec & 0xff00) >> 8
        cmd[-1] = sec & 0xff
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        time.sleep(0.05)
        while self._b.cdb1_cip():
            time.sleep(0.1)
            pass


    def read(self, addr, len):
        while not self._b.cdb1_idle():
            time.sleep(0.1)
            pass
        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x0b\x00\x00\x00\x0f\x06\x03\x00\x00\x00\x00\x00\x00\x00\x00')
        cmd[-8] = (addr >> 24) & 0xff
        cmd[-7] = (addr >> 16) & 0xff
        cmd[-6] = (addr >> 8) & 0xff
        cmd[-5] = addr & 0xff
        cmd[-4] = (len >> 24) & 0xff
        cmd[-3] = (len >> 16) & 0xff
        cmd[-2] = (len >> 8) & 0xff
        cmd[-1] = len & 0xff
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        time.sleep(0.1)
        while self._b.cdb1_cip():
            time.sleep(0.1)
            pass
        if self._b.cdb1_success():
            data = bytearray()
            pages = len // 128
            if len % 128:
                pages += 1
            for i in range(pages):
                change_page_cmd = bytearray(b'\x00\xa0')
                change_page_cmd[-1] = 0xa0 + i
                self._b.twi_sbw(126, change_page_cmd)
                time.sleep(0.1)
                if len >= 128:
                    data += self._b.twi_srr(128, 128)
                    len -= 128
                else:
                    data += self._b.twi_srr(128, len)
                time.sleep(0.1)
            return data
            # return struct.unpack('>1H', data)


    def program(self, addr, data, bw = False):
        while not self._b.cdb1_idle():
            time.sleep(0.1)
            pass
        # self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x07\x00\x00\x00\x0f\x06\x04\x00\x00\x00\x00')
        cmd[-4] = (addr >> 24) & 0xff
        cmd[-3] = (addr >> 16) & 0xff
        cmd[-2] = (addr >> 8) & 0xff
        cmd[-1] = addr & 0xff
        length = int(len(data))
        if length > 2048:
            return
        cmd[2] = (length >> 8) & 0xff #EPL MSB
        cmd[3] = length & 0xff #EPL LSB
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        print(cmd)
        # pages = length // 128
        # if length % 128:
        #     pages += 1
        # for i in range(pages):
        #     change_page_cmd = bytearray(b'\x00\xa0')
        #     change_page_cmd[-1] = 0xa0 + i
        #     self._b.twi_sbw(126, change_page_cmd)
        #     time.sleep(0.1)
        #     if length >= 128:
        #         self._b.twi_sbw(128, data[i*128 : (i+1)*128])
        #         length -= 128
        #     else:
        #         self._b.twi_sbw(128, data)
        #     time.sleep(0.1)

        change_page_cmd = bytearray(b'\x00\xa0')
        self._b.twi_sbw(126, change_page_cmd)
        time.sleep(0.1)
        self._b.twi_sbw(128, data[0:length+1])
        time.sleep(0.1)


        self._b.twi_sbw(126, b'\x00\x9f')
        time.sleep(0.1)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        time.sleep(0.1)
        while self._b.cdb1_cip():
            time.sleep(0.1)
            pass

    def cfg_verify(self):
        while not self._b.cdb1_idle():
            time.sleep(0.1)
            pass
        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x03\x00\x00\x00\x0f\x06\x05')
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        time.sleep(0.05)
        while self._b.cdb1_cip():
            time.sleep(0.1)
            pass
        if self._b.cdb1_success():
            rlplen = self._b.twi_rr(134)
            rlp_chkcode = self._b.twi_rr(135)
            rlp = self._b.twi_srr(136, rlplen)
            if self._b.cdb_chkcode(rlp) == rlp_chkcode:
                return rlp[0]
    # @property
    # def status(self):
    #     while not self._b.cdb1_idle():
    #         pass
    #     self._b.mdio_write(0x9c02, 0x05)
    #     self._b.mdio_write(0x9c01, 1)
    #     self._b.mdio_write(0x9c00, 0x0f06)
    #     while self._b.cdb1_cip():
    #         pass
    #     data = bytearray()
    #     len = self._b.mdio_read(0x9c01)
    #     for i in range(len):
    #         data.append(self._b.mdio_read(0x9c02 + i))
    #     return ''.join(format(b, '02x') for b in data)


    def main_mem_erase(self, addr):#8k bytes per time
        while not self._b.cdb1_idle():
            time.sleep(0.1)
            pass
        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x07\x00\x00\x00\x0f\x06\x10\x00\x00\x00\x00')
        cmd[-4] = (addr >> 24) & 0xff
        cmd[-3] = (addr >> 16) & 0xff
        cmd[-2] = (addr >> 8) & 0xff
        cmd[-1] = (addr >> 0) & 0xff        
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        time.sleep(0.05)
        while self._b.cdb1_cip():
            time.sleep(0.1)
            pass

    def main_mem_write(self, addr, data):#8bytes per time
        while not self._b.cdb1_idle():
            time.sleep(0.1)
            pass
        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x0f\x00\x00\x00\x0f\x06\x11') + \
              struct.pack('>I', addr) + \
              struct.pack('>Q', data)       
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        time.sleep(0.05)
        while self._b.cdb1_cip():
            time.sleep(0.1)
            pass

    def main_mem_read(self, addr):#8bytes per time
        while not self._b.cdb1_idle():
            time.sleep(0.1)
            pass
        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x07\x00\x00\x00\x0f\x06\x12\x00\x00\x00\x00')
        cmd[-4] = (addr >> 24) & 0xff
        cmd[-3] = (addr >> 16) & 0xff
        cmd[-2] = (addr >> 8) & 0xff
        cmd[-1] = (addr >> 0) & 0xff        
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        time.sleep(0.05)
        while self._b.cdb1_cip():
            time.sleep(0.1)
            pass

        if self._b.cdb1_success():
            rlplen = self._b.twi_rr(134)
            rlp_chkcode = self._b.twi_rr(135)
            rlp = self._b.twi_srr(136, rlplen)
            if self._b.cdb_chkcode(rlp) == rlp_chkcode:
                data = struct.unpack('>Q', rlp)[0]
                return data

    def abc_mem_erase(self, addr):#8k bytes per time
        while not self._b.cdb1_idle():
            time.sleep(0.1)
            pass
        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x07\x00\x00\x00\x0f\x06\x20\x00\x00\x00\x00')
        cmd[-4] = (addr >> 24) & 0xff
        cmd[-3] = (addr >> 16) & 0xff
        cmd[-2] = (addr >> 8) & 0xff
        cmd[-1] = (addr >> 0) & 0xff        
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        time.sleep(0.05)
        while self._b.cdb1_cip():
            time.sleep(0.1)
            pass

    def abc_mem_write(self, addr, data):#8bytes per time
        while not self._b.cdb1_idle():
            time.sleep(0.1)
            pass
        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x0f\x00\x00\x00\x0f\x06\x21') + \
              struct.pack('>I', addr) + \
              struct.pack('>Q', data)       
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        time.sleep(0.05)
        while self._b.cdb1_cip():
            time.sleep(0.1)
            pass

    def abc_mem_read(self, addr):#8bytes per time
        while not self._b.cdb1_idle():
            time.sleep(0.1)
            pass
        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x07\x00\x00\x00\x0f\x06\x22\x00\x00\x00\x00')
        cmd[-4] = (addr >> 24) & 0xff
        cmd[-3] = (addr >> 16) & 0xff
        cmd[-2] = (addr >> 8) & 0xff
        cmd[-1] = (addr >> 0) & 0xff        
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        time.sleep(0.05)
        while self._b.cdb1_cip():
            time.sleep(0.1)
            pass

        if self._b.cdb1_success():
            rlplen = self._b.twi_rr(134)
            rlp_chkcode = self._b.twi_rr(135)
            rlp = self._b.twi_srr(136, rlplen)
            if self._b.cdb_chkcode(rlp) == rlp_chkcode:
                data = struct.unpack('>Q', rlp)[0]
                return data