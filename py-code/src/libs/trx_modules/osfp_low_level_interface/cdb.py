from .broker import Broker
import time

class CDB:

    def __init__(self, broker):
        self._b = broker

    def CMD0000h(self, ms = 0):
        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00')
        cmd[-1] = ms & 0xff
        cmd[-2] = ms >> 8
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        # print(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        while self._b.cdb1_cip():
            time.sleep(0.1)
        rlplen = self._b.twi_rr(134)
        rlp_chkcode = self._b.twi_rr(135)
        rlp = self._b.twi_srr(136, rlplen)
        return rlplen,rlp_chkcode,rlp

    def CMD0040h(self):
        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x00\x40\x00\x00\x00\xBF\x00\x00')
        # print(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        while self._b.cdb1_cip():
            time.sleep(0.1)
        rlplen = self._b.twi_rr(134)
        rlp_chkcode = self._b.twi_rr(135)
        rlp = self._b.twi_srr(136, rlplen)
        return rlplen,rlp_chkcode,rlp

    def CMD0041h(self):
        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x00\x41\x00\x00\x00\xBE\x00\x00')
        # print(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        while self._b.cdb1_cip():
            time.sleep(0.1)
        rlplen = self._b.twi_rr(134)
        rlp_chkcode = self._b.twi_rr(135)
        rlp = self._b.twi_srr(136, rlplen)
        return rlplen,rlp_chkcode,rlp

    def CMD0042h(self):
        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x00\x42\x00\x00\x00\xBD\x00\x00')
        # print(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        while self._b.cdb1_cip():
            time.sleep(0.1)
        rlplen = self._b.twi_rr(134)
        rlp_chkcode = self._b.twi_rr(135)
        rlp = self._b.twi_srr(136, rlplen)
        return rlplen,rlp_chkcode,rlp

    def CMD0043h(self):
        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x00\x43\x00\x00\x00\xBC\x00\x00')
        # print(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        while self._b.cdb1_cip():
            time.sleep(0.1)
        rlplen = self._b.twi_rr(134)
        rlp_chkcode = self._b.twi_rr(135)
        rlp = self._b.twi_srr(136, rlplen)
        return rlplen,rlp_chkcode,rlp

    def CMD0100h(self):
        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x01\x00\x00\x00\x00\xFE')
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        # self._b.twi_sbw(128, cmd)
        # print(cmd)
        while self._b.cdb1_cip():
            time.sleep(0.1)
        rlplen = self._b.twi_rr(134)
        rlp_chkcode = self._b.twi_rr(135)
        rlp = self._b.twi_srr(136, rlplen)
        return rlplen,rlp_chkcode,rlp

    # def CMD0101h(self, size, abc_len, abc_crc, main_len, main_crc):
    def CMD0101h(self, head):
        self._b.twi_sbw(122, b'\x00\x00\x10\x11')
        self._b.twi_sbw(126, b'\x00\x9f')
        time.sleep(0.3)
        cmd = bytearray(b'\x01\x01\x00\x00\x48\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        # cmd[136-128] = (size >> 24) & 0xff
        # cmd[137-128] = (size >> 16) & 0xff
        # cmd[138-128] = (size >> 8) & 0xff
        # cmd[139-128] = (size >> 0) & 0xff     
        # cmd = cmd + \
        #       struct.pack('>I', abc_len) + \
        #       struct.pack('>I', abc_crc) + \
        #       struct.pack('>I', main_len) + \
        #       struct.pack('>I', main_crc)      
        cmd = cmd + head      
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        # print(cmd)
        time.sleep(1)
        while self._b.cdb1_cip():
            time.sleep(0.1)
        self._b.twi_sbw(122, b'\x00\x00\x00\x00')
        return self._b.twi_rr(37)

    def CMD0102h(self):
        self._b.twi_sbw(122, b'\x00\x00\x10\x11')
        self._b.twi_sbw(126, b'\x00\x9f')
        time.sleep(0.1)
        cmd = bytearray(b'\x01\x02\x00\x00\x00\x00\x00\x00')
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        # print(cmd)
        while self._b.cdb1_cip():
            time.sleep(0.1)
        self._b.twi_sbw(122, b'\x00\x00\x00\x00')
        return self._b.twi_rr(37)

    def CMD0104h_host(self, addr, data):
        epl_len = len(data)
        #switch page to a0
        change_page_cmd = bytearray(b'\x00\xa0')
        self._b.twi_sbw(126, change_page_cmd)
        time.sleep(0.05)
        #tell host download bin to module
        self._b.dcpy(addr+0x290040, epl_len)
        time.sleep(0.2)

        self._b.twi_sbw(122, b'\x00\x00\x10\x11')
        self._b.twi_sbw(126, b'\x00\x9f')
        time.sleep(0.1)
        cmd = bytearray(b'\x01\x04\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00')
        cmd[130-128] = (epl_len >> 8) & 0xff
        cmd[131-128] = (epl_len >> 0) & 0xff
        cmd[136-128] = (addr >> 24) & 0xff
        cmd[137-128] = (addr >> 16) & 0xff
        cmd[138-128] = (addr >> 8) & 0xff
        cmd[139-128] = (addr >> 0) & 0xff
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        # print(cmd)
        while self._b.cdb1_cip():
            time.sleep(0.1)
        self._b.twi_sbw(122, b'\x00\x00\x00\x00')
        return self._b.twi_rr(37)

    def CMD0104h_host_fwdsp(self, addr, data):
        epl_len = len(data)
        #switch page to a0
        change_page_cmd = bytearray(b'\x00\xa0')
        self._b.twi_sbw(126, change_page_cmd)
        time.sleep(0.05)
        #tell host download bin to module
        self._b.dcpy(addr+0x10040, epl_len)
        time.sleep(0.2)

        self._b.twi_sbw(122, b'\x00\x00\x10\x11')
        self._b.twi_sbw(126, b'\x00\x9f')
        time.sleep(0.1)
        cmd = bytearray(b'\x01\x04\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00')
        cmd[130-128] = (epl_len >> 8) & 0xff
        cmd[131-128] = (epl_len >> 0) & 0xff
        cmd[136-128] = (addr >> 24) & 0xff
        cmd[137-128] = (addr >> 16) & 0xff
        cmd[138-128] = (addr >> 8) & 0xff
        cmd[139-128] = (addr >> 0) & 0xff
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        # print(cmd)
        while self._b.cdb1_cip():
            time.sleep(0.1)
        self._b.twi_sbw(122, b'\x00\x00\x00\x00')
        return self._b.twi_rr(37)
    
    def CMD0104h(self, addr, data):
        epl_len = len(data)
        pages = epl_len // 128
        if epl_len % 128:
            pages += 1
        for i in range(pages):
            change_page_cmd = bytearray(b'\x00\xa0')
            change_page_cmd[-1] = 0xa0 + i
            self._b.twi_sbw(126, change_page_cmd)
            time.sleep(0.1)
            self._b.twi_sbw(128, data[128*i:128*(i+1)])
            time.sleep(0.1)


        self._b.twi_sbw(122, b'\x00\x00\x10\x11')
        self._b.twi_sbw(126, b'\x00\x9f')
        time.sleep(0.1)
        cmd = bytearray(b'\x01\x04\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00')
        cmd[130-128] = (epl_len >> 8) & 0xff
        cmd[131-128] = (epl_len >> 0) & 0xff
        cmd[136-128] = (addr >> 24) & 0xff
        cmd[137-128] = (addr >> 16) & 0xff
        cmd[138-128] = (addr >> 8) & 0xff
        cmd[139-128] = (addr >> 0) & 0xff
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        # print(cmd)
        while self._b.cdb1_cip():
            time.sleep(0.1)
        self._b.twi_sbw(122, b'\x00\x00\x00\x00')
        return self._b.twi_rr(37)
    
    def CMD0106h(self, addr, len):
        self._b.twi_sbw(122, b'\x00\x00\x10\x11')
        self._b.twi_sbw(126, b'\x00\x9f')
        time.sleep(0.1)
        cmd = bytearray(b'\x01\x06\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        cmd[130-128] = (len >> 8) & 0xff
        cmd[131-128] = (len >> 0) & 0xff
        cmd[136-128] = (addr >> 24) & 0xff
        cmd[137-128] = (addr >> 16) & 0xff
        cmd[138-128] = (addr >> 8) & 0xff
        cmd[139-128] = (addr >> 0) & 0xff
        cmd[140-128] = (len >> 8) & 0xff
        cmd[141-128] = (len >> 0) & 0xff
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        # print(cmd)
        while self._b.cdb1_cip():
            time.sleep(0.1)
        self._b.twi_sbw(122, b'\x00\x00\x00\x00')
        time.sleep(0.1)
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

    def CMD0107h(self):
        self._b.twi_sbw(122, b'\x00\x00\x10\x11')
        self._b.twi_sbw(126, b'\x00\x9f')
        time.sleep(0.1)
        cmd = bytearray(b'\x01\x07\x00\x00\x00\xf7\x00\x00')
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        # print(cmd)
        time.sleep(0.5)
        while self._b.cdb1_cip():
            time.sleep(0.1)
            pass
        self._b.twi_sbw(122, b'\x00\x00\x00\x00')
        time.sleep(0.1)
        return self._b.twi_rr(37)

    def CMD0108h(self, dir):
        self._b.twi_sbw(122, b'\x00\x00\x10\x11')
        self._b.twi_sbw(126, b'\x00\x9f')
        time.sleep(0.1)
        cmd = bytearray(b'\x01\x08\x00\x00\x01\x00\x00\x00\x00')
        cmd[-1] = dir
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        # print(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        while self._b.cdb1_cip():
            pass
        time.sleep(0.1)
        self._b.twi_sbw(122, b'\x00\x00\x00\x00')
        # return self._b.twi_rr(37)

    def CMD0109h(self, mode=0x01):
        self._b.twi_sbw(122, b'\x00\x00\x10\x11')
        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x01\x09\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00')
        cmd[137-128] = mode
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        # print(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        # while self._b.cdb1_cip():
        #     pass
        time.sleep(0.1)
        # self._b.twi_sbw(122, b'\x00\x00\x00\x00')
        # return self._b.twi_rr(37)

    def CMD010Ah(self):
        self._b.twi_sbw(122, b'\x00\x00\x10\x11')
        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x01\x0A\x00\x00\x00\xf4\x00\x00')
        # print(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        while self._b.cdb1_cip():
            time.sleep(0.1)
        self._b.twi_sbw(122, b'\x00\x00\x00\x00')

    def CMD0380h(self):
        pass

    def CMDA000h(self, flag):
        # self._b.cdb_psw()
        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\xA0\x00\x00\x00\x01\x00\x00\x00\x00')
        cmd[-1] = flag
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        # print(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        while self._b.cdb1_cip():
            time.sleep(0.1)

    def CMD9001h(self, val):#IPHI_SetHostIngressLanePolarity
        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x90\x01\x00\x00\x01\x00\x00\x00\x00')
        cmd[-1] = val
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        print(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        while self._b.cdb1_cip():
            time.sleep(0.1)

    def CMD9003h(self, val):#IPHI_SetHostEgressLanePolarity
        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x90\x03\x00\x00\x01\x00\x00\x00\x00')
        cmd[-1] = val
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        print(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        while self._b.cdb1_cip():
            time.sleep(0.1)