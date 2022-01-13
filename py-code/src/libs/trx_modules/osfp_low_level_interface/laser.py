from .broker import Broker
from .dpin import DPin
import ctypes
from .canopus import Canopus
class Laser:
    def __init__(self, broker):
        self._b = broker
        self.rst_n = DPin(self._b, 'ITLA_OIF_RST_N')
        self.dis_n = DPin(self._b, 'ITLA_OIF_DIS_N')

    def read(self, regAddr):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x05\x00\x00\x00\x0f\x09\x01\x00\x00')
        cmd[-2] = regAddr >> 8
        cmd[-1] = regAddr & 0xff
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
                return (rlp[0] << 8) | rlp[1]

        return 0


    def write(self, regAddr, val):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x07\x00\x00\x00\x0f\x09\x02\x00\x00\x00\x00')
        cmd[-4] = regAddr >> 8
        cmd[-3] = regAddr & 0xff
        cmd[-2] = val >> 8
        cmd[-1] = val & 0xff

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
                return (rlp[0] << 8) | rlp[1]

        return 0

    # @property
    # def dis_n(self):
    #     pin_dis_n = DPin(self._b, 'ITLA_OIF_DIS_N')
    #     return pin_dis_n.state

    # @dis_n.setter
    # def dis_n(self, val):
    #     while not self._b.cdb1_idle():
    #         pass

    #     self._b.twi_sbw(126, b'\x00\x9f')
    #     cmd = bytearray(b'\x80\x00\x00\x00\x04\x00\x00\x00\x0f\x09\x03\x00')
    #     cmd[-1] = val & 0xff

    #     cmd[133-128] = self._b.cdb_chkcode(cmd)
    #     self._b.twi_sbw(130, cmd[2:])
    #     self._b.twi_sbw(128, cmd[:2])
    #     while self._b.cdb1_cip():
    #         pass

    # @property
    # def rst_n(self):
    #     pin_rst_n = DPin(self._b, 'ITLA_OIF_RST_N')
    #     return pin_rst_n.state

    # @rst_n.setter
    # def rst_n(self, val):
    #     while not self._b.cdb1_idle():
    #         pass

    #     self._b.twi_sbw(126, b'\x00\x9f')
    #     cmd = bytearray(b'\x80\x00\x00\x00\x04\x00\x00\x00\x0f\x09\x04\x00')
    #     cmd[-1] = val & 0xff

    #     cmd[133-128] = self._b.cdb_chkcode(cmd)
    #     self._b.twi_sbw(130, cmd[2:])
    #     self._b.twi_sbw(128, cmd[:2])
    #     while self._b.cdb1_cip():
    #         pass

    @property
    def frequency(self):
        freq_T = self.read(0x40)
        freq_10G = self.read(0x41)
        freq_M = self.read(0x68)
        #print((freq, freq_T, freq_G, freq_M))
        freq = freq_T + freq_10G * 0.0001 + freq_M * 0.000001
        # print((freq, freq_T, freq_10G, freq_M))
        return freq

    @property
    def fcf(self):
        freq_T = self.read(0x35)
        freq_10G = self.read(0x36)
        freq_M = self.read(0x67)
        #print((freq, freq_T, freq_G, freq_M))
        freq = freq_T + freq_10G * 0.0001 + freq_M * 0.000001
        # print((freq, freq_T, freq_10G, freq_M))
        return freq

    @fcf.setter
    def fcf(self, freq):
        freq_T = int(freq)
        freq_G = int((freq - freq_T) * 10000)
        freq_M = int(((freq - freq_T) * 10000 - freq_G) * 100)
        # print((freq, freq_T, freq_G, freq_M))
        self.write(0x35, freq_T)
        self.write(0x36, freq_G)
        self.write(0x67, freq_M)

    @property
    def lff(self):
        freq_T = self.read(0x52)
        freq_10G = self.read(0x53)
        freq_M = self.read(0x69)
        #print((freq, freq_T, freq_G, freq_M))
        freq = freq_T + freq_10G * 0.0001 + freq_M * 0.000001
        # print((freq, freq_T, freq_10G, freq_M))
        return freq

    @property
    def llf(self):
        freq_T = self.read(0x54)
        freq_10G = self.read(0x55)
        freq_M = self.read(0x6a)
        #print((freq, freq_T, freq_G, freq_M))
        freq = freq_T + freq_10G * 0.0001 + freq_M * 0.000001
        # print((freq, freq_T, freq_10G, freq_M))
        return freq

    @property
    def ftf(self):
        ftf_m = self.read(0x62)
        return ctypes.c_short(ftf_m).value

    @ftf.setter
    def ftf(self, freq):
        ftf_m = ctypes.c_ushort(freq).value
        self.write(0x62, ftf_m)

    @property
    def grid(self):
        grid1 = self.read(0x34)
        grid2 = self.read(0x66)
        return grid1/10 + grid2/1000

    @grid.setter
    def grid(self, grid):
        grid1 = int(grid*10)
        grid2 = int((grid*10 - grid1) * 100)
        # print((grid, grid1, grid2))
        self.write(0x34, grid1)
        self.write(0x66, grid2)

    @property
    def channel(self):
        channel_h = self.read(0x65)
        channel_l = self.read(0x30)
        # print((channel, channel_h, channel_l))
        return (channel_h << 16) + channel_l 

    @channel.setter
    def channel(self, channel):
        channel_h = channel >> 16
        channel_l = channel & 0xffff
        # print((channel, channel_h, channel_l))

        self.write(0x30, channel_l)
        self.write(0x65, channel_h)

    @property
    def power(self):
        dbm = self.read(0x42)
        dbm = ctypes.c_short(dbm).value
        return dbm / 100

    @power.setter
    def power(self, pwr):
        pwr_100dbm = int(pwr * 100)
        # print((pwr, pwr_100dbm))

        self.write(0x31, pwr_100dbm)

    @property
    def temp(self):
        temp = self.read(0x43)
        temp = ctypes.c_short(temp).value
        return temp / 100

    @property
    def release(self):
        self._b.cdb_psw()
        dsp = Canopus(self._b)
        dsp.polling_suspend_resume(0)
        res = self.read(0x6)
        byteslen = res
        recv = bytearray(byteslen)
        i = 0
        while i < byteslen:
            regval = self.read(0x0B)
            recv[i] = regval >> 8
            if i+1 < byteslen :
                recv[i + 1] = regval & 0xFF
            i += 2
            
        print(recv.decode().strip())    
        dsp.polling_suspend_resume(1)
        return recv

    @property
    def SN(self):
        self._b.cdb_psw()
        dsp = Canopus(self._b)
        dsp.polling_suspend_resume(0)
        res = self.read(0x4)
        byteslen = res
        recv = bytearray(byteslen)
        i = 0
        while i < byteslen:
            regval = self.read(0x0B)
            recv[i] = regval >> 8
            if i+1 < byteslen :
                recv[i + 1] = regval & 0xFF
            i += 2
            
        print(recv.decode().strip())    
        dsp.polling_suspend_resume(1)
        return recv

    @property
    def currents(self):
        self._b.cdb_psw()
        dsp = Canopus(self._b)
        dsp.polling_suspend_resume(0)
        res = self.read(0x57)
        byteslen = res
        recv = bytearray(byteslen)
        i = 0
        while i < byteslen:
            regval = self.read(0x0B)
            recv[i] = regval >> 8
            if i+1 < byteslen :
                recv[i + 1] = regval & 0xFF
            i += 2
            
        # print(recv.decode().strip())    
        dsp.polling_suspend_resume(1)
        return recv