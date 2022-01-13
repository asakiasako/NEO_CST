from .broker import Broker
import struct
import math 
import time
class ABC:
    def __init__(self, broker):
        self._b = broker

    @property
    def setting(self):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x03\x00\x00\x00\x0f\x08\x02')
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
                freq_idx = rlp[0] << 8 | rlp[1]
                ampl = rlp[2] << 8 | rlp[3]
                theta = rlp[4] << 8 | rlp[5]
                iter = rlp[6] << 8 | rlp[7]
                return (freq_idx, ampl, theta, iter)

        return (0, 0, 0, 0)

    @setting.setter
    def setting(self, vals):
        freq_idx, ampl, theta, iter = vals
        while not self._b.cdb1_idle():
            pass
        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x0b\x00\x00\x00\x0f\x08\x01\x00\x00\x00\x00\x00\x00\x00\x00')
        cmd[-8] = (freq_idx >> 8) & 0xff
        cmd[-7] = freq_idx & 0xff
        cmd[-6] = (ampl >> 8) & 0xff
        cmd[-5] = ampl & 0xff
        cmd[-4] = (theta >> 8) & 0xff
        cmd[-3] = theta & 0xff
        cmd[-2] = (iter >> 8) & 0xff
        cmd[-1] = iter & 0xff
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        while self._b.cdb1_cip():
            pass

    def pid_get(self, ph):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x05\x00\x00\x00\x0f\x08\x04\x00\x00')
        cmd[-2] = (ph >> 8) & 0xff
        cmd[-1] = ph & 0xff        
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
                # b = bytearray()
                # b.append(rlp[0])
                # b.append(rlp[1])
                # b.append(rlp[2])
                # b.append(rlp[3])
                # p = struct.unpack('<1f', b)[0]  
                p = struct.unpack('<1f', rlp[0:4])[0]

                # b = bytearray()
                # b.append(rlp[4])
                # b.append(rlp[5])
                # b.append(rlp[6])
                # b.append(rlp[7])
                # i = struct.unpack('<1f', b)[0] 
                i = struct.unpack('<1f', rlp[4:8])[0]

                # b = bytearray()
                # b.append(rlp[8])
                # b.append(rlp[9])
                # b.append(rlp[10])
                # b.append(rlp[11])
                # d = struct.unpack('<1f', b)[0] 
                d = struct.unpack('<1f', rlp[8:12])[0]

                # b = bytearray()
                # b.append(rlp[12])
                # b.append(rlp[13])
                # b.append(rlp[14])
                # b.append(rlp[15])
                # i_min = struct.unpack('<1f', b)[0] 
                i_min = struct.unpack('<1f', rlp[12:16])[0]

                # b = bytearray()
                # b.append(rlp[16])
                # b.append(rlp[17])
                # b.append(rlp[18])
                # b.append(rlp[19])
                # i_max = struct.unpack('<1f', b)[0]  
                i_max = struct.unpack('<1f', rlp[16:20])[0]           
                return (p, i, d, i_min, i_max)


    def pid_set(self, ph, vals):
        p, i, d, i_min, i_max = vals

        while not self._b.cdb1_idle():
            pass
        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x19\x00\x00\x00\x0f\x08\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        cmd[-22] = (ph >> 8) & 0xff
        cmd[-21] = ph & 0xff

        vs = struct.pack('<1f', p)
        cmd[-20] = vs[0]
        cmd[-19] = vs[1]
        cmd[-18] = vs[2]
        cmd[-17] = vs[3]

        vs = struct.pack('<1f', i)
        cmd[-16] = vs[0]
        cmd[-15] = vs[1]
        cmd[-14] = vs[2]
        cmd[-13] = vs[3]

        vs = struct.pack('<1f', d)
        cmd[-12] = vs[0]
        cmd[-11] = vs[1]
        cmd[-10] = vs[2]
        cmd[-9] = vs[3]

        vs = struct.pack('<1f', i_min)
        cmd[-8] = vs[0]
        cmd[-7] = vs[1]
        cmd[-6] = vs[2]
        cmd[-5] = vs[3]

        vs = struct.pack('<1f', i_max)
        cmd[-4] = vs[0]
        cmd[-3] = vs[1]
        cmd[-2] = vs[2]
        cmd[-1] = vs[3]

        cmd[133-128] = self._b.cdb_chkcode(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        while self._b.cdb1_cip():
            pass

    @property
    def service(self):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x03\x00\x00\x00\x0f\x08\x06')
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

    @service.setter
    def service(self, val):
        while not self._b.cdb1_idle():
            pass
        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x05\x00\x00\x00\x0f\x08\x05\x00\x00')
        cmd[-2] = (val >> 8) & 0xff
        cmd[-1] = val & 0xff
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        while self._b.cdb1_cip():
            pass

    def method_get(self, ph):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x05\x00\x00\x00\x0f\x08\x08\x00\x00')
        cmd[-2] = (ph >> 8) & 0xff
        cmd[-1] = ph & 0xff    
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

    def method_set(self, ph, val):
        while not self._b.cdb1_idle():
            pass
        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x07\x00\x00\x00\x0f\x08\x07\x00\x00\x00\x00')
        cmd[-4] = (ph >> 8) & 0xff
        cmd[-3] = ph & 0xff        
        cmd[-2] = (val >> 8) & 0xff
        cmd[-1] = val & 0xff
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        while self._b.cdb1_cip():
            pass

    def theta_get(self, ph):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x05\x00\x00\x00\x0f\x08\x0a\x00\x00')
        cmd[-2] = (ph >> 8) & 0xff
        cmd[-1] = ph & 0xff    
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

    def theta_set(self, ph, val):
        while not self._b.cdb1_idle():
            pass
        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x07\x00\x00\x00\x0f\x08\x09\x00\x00\x00\x00')
        cmd[-4] = (ph >> 8) & 0xff
        cmd[-3] = ph & 0xff        
        cmd[-2] = (val >> 8) & 0xff
        cmd[-1] = val & 0xff
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        while self._b.cdb1_cip():
            pass

    def iter_get(self, ph):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x05\x00\x00\x00\x0f\x08\x11\x00\x00')
        cmd[-2] = (ph >> 8) & 0xff
        cmd[-1] = ph & 0xff    
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

    def iter_set(self, ph, val):
        while not self._b.cdb1_idle():
            pass
        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x07\x00\x00\x00\x0f\x08\x10\x00\x00\x00\x00')
        cmd[-4] = (ph >> 8) & 0xff
        cmd[-3] = ph & 0xff        
        cmd[-2] = (val >> 8) & 0xff
        cmd[-1] = val & 0xff
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        while self._b.cdb1_cip():
            pass

    def vgar_get(self, ph):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x05\x00\x00\x00\x0f\x08\x0d\x00\x00')
        cmd[-2] = (ph >> 8) & 0xff
        cmd[-1] = ph & 0xff    
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

    def vgar_set(self, ph, val):
        while not self._b.cdb1_idle():
            pass
        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x07\x00\x00\x00\x0f\x08\x0c\x00\x00\x00\x00')
        cmd[-4] = (ph >> 8) & 0xff
        cmd[-3] = ph & 0xff        
        cmd[-2] = (val >> 8) & 0xff
        cmd[-1] = val & 0xff
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        while self._b.cdb1_cip():
            pass


    def polarity_get(self, ph):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x07\x00\x00\x00\x0f\x08\x0b\x00\x04\x00\x00')
        cmd[-2] = (ph >> 8) & 0xff
        cmd[-1] = ph & 0xff    
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
        


    def polarity_set(self, ph, val):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x09\x00\x00\x00\x0f\x08\x0b\x00\x04\x00\x00\x00\x00')
        cmd[-4] = (ph >> 8) & 0xff
        cmd[-3] = ph & 0xff   
        cmd[-2] = (val >> 8) & 0xff
        cmd[-1] = val & 0xff          
        cmd[133-128] = self._b.cdb_chkcode(cmd)             
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        while self._b.cdb1_cip():
            pass



    def range_set(self, ph, vals):
        min, max = vals
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x0f\x00\x00\x00\x0f\x08\x0b\x00\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        cmd[-10] = (ph >> 8) & 0xff
        cmd[-9] = ph & 0xff   

        vs = struct.pack('<1f', min)
        cmd[-8] = vs[1]
        cmd[-7] = vs[0]   
        cmd[-6] = vs[3]
        cmd[-5] = vs[2]      

        vs = struct.pack('<1f', max)
        cmd[-4] = vs[1]
        cmd[-3] = vs[0]   
        cmd[-2] = vs[3]
        cmd[-1] = vs[2]                       
        cmd[133-128] = self._b.cdb_chkcode(cmd)             
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        while self._b.cdb1_cip():
            pass

    def range_get(self, ph):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x07\x00\x00\x00\x0f\x08\x0b\x00\x05\x00\x00')
        cmd[-2] = (ph >> 8) & 0xff
        cmd[-1] = ph & 0xff    
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
                print(bytearray(rlp))
                b = bytearray()
                b.append(rlp[1])
                b.append(rlp[0])
                b.append(rlp[3])
                b.append(rlp[2])
                min = struct.unpack('<1f', b)[0] 
                # min = struct.unpack('<1f', rlp[0:4])[0]
                print(min)

                b = bytearray()
                b.append(rlp[5])
                b.append(rlp[4])
                b.append(rlp[7])
                b.append(rlp[6])
                max = struct.unpack('<1f', b)[0] 
                # max = struct.unpack('<1f', rlp[4:8])[0]
                print(max)
                return (min, max)



    def step_set(self, ph, val):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x0b\x00\x00\x00\x0f\x08\x0b\x00\x06\x00\x00\x00\x00\x00\x00')
        cmd[-6] = (ph >> 8) & 0xff
        cmd[-5] = ph & 0xff   

        vs = struct.pack('<1f', val)
        cmd[-4] = vs[1]
        cmd[-3] = vs[0]   
        cmd[-2] = vs[3]
        cmd[-1] = vs[2]                       
        cmd[133-128] = self._b.cdb_chkcode(cmd)             
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        while self._b.cdb1_cip():
            pass


    def step_get(self, ph):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x07\x00\x00\x00\x0f\x08\x0b\x00\x06\x00\x00')
        cmd[-2] = (ph >> 8) & 0xff
        cmd[-1] = ph & 0xff   
                    
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

                b = bytearray()
                b.append(rlp[1])
                b.append(rlp[0])
                b.append(rlp[3])
                b.append(rlp[2])
                step = struct.unpack('<1f', b)[0] 

                return step

    @property
    def algo(self):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x05\x00\x00\x00\x0f\x08\x0b\x00\x07')
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
                return rlp[0] << 8 | rlp[1]

    @algo.setter
    def algo(self, val):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x07\x00\x00\x00\x0f\x08\x0b\x00\x07\x00\x00')
        cmd[-2] = (val >> 8) & 0xff
        cmd[-1] = val & 0xff
        cmd[133-128] = self._b.cdb_chkcode(cmd)             
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        while self._b.cdb1_cip():
            pass

    def dither_set(self, ch, ph, freq, ampl):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x0d\x00\x00\x00\x0f\x08\x0b\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00')
        cmd[-8] = (ch >> 8) & 0xff
        cmd[-7] = ch & 0xff
        cmd[-6] = (ph >> 8) & 0xff
        cmd[-5] = ph & 0xff
        cmd[-4] = (freq >> 8) & 0xff
        cmd[-3] = freq & 0xff
        cmd[-2] = (ampl >> 8) & 0xff
        cmd[-1] = ampl & 0xff
        cmd[133-128] = self._b.cdb_chkcode(cmd)             
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        while self._b.cdb1_cip():
            pass

    def dither_get(self, ch):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x07\x00\x00\x00\x0f\x08\x0b\x00\x08\x00\x00')
        cmd[-2] = (ch >> 8) & 0xff
        cmd[-1] = ch & 0xff
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
                return rlp[0] << 8 | rlp[1]


    @property
    def dither(self):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x05\x00\x00\x00\x0f\x08\x0b\x00\x09')
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
                return rlp[0] << 8 | rlp[1]


    @dither.setter
    def dither(self, val):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x07\x00\x00\x00\x0f\x08\x0b\x00\x09\x00\x00')
        cmd[-2] = (val >> 8) & 0xff
        cmd[-1] = val & 0xff
        cmd[133-128] = self._b.cdb_chkcode(cmd)             
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        while self._b.cdb1_cip():
            pass


    def demod(self, m):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x07\x00\x00\x00\x0f\x08\x0b\x00\x0a\x00\x00')
        cmd[-2] = (m >> 8) & 0xff
        cmd[-1] = m & 0xff    
        cmd[133-128] = self._b.cdb_chkcode(cmd)             
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        while self._b.cdb1_cip():
            pass

        if self._b.cdb1_success():
            rlplen = self._b.twi_rr(134)
            # print(rlplen)
            rlp_chkcode = self._b.twi_rr(135)
            rlp = self._b.twi_srr(136, rlplen)
            # print('rlplen %d.\n' % rlplen)
            if self._b.cdb_chkcode(rlp) == rlp_chkcode:
                b = bytearray()
                # b.append(rlp[0])
                # b.append(rlp[1])
                # b.append(rlp[2])
                # b.append(rlp[3])
                b.append(rlp[1])
                b.append(rlp[0])
                b.append(rlp[3])
                b.append(rlp[2])                
                sin = struct.unpack('<1f', b)[0] 

                b = bytearray()
                b.append(rlp[5]) 
                b.append(rlp[4])
                b.append(rlp[7])
                b.append(rlp[6])
                cos = struct.unpack('<1f', b)[0] 

                root = math.sqrt(sin**2 + cos**2)
                return sin, cos, root



    def demod_table(self, m):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x07\x00\x00\x00\x0f\x08\x0b\x00\x0f\x00\x00')
        cmd[-2] = (m >> 8) & 0xff
        cmd[-1] = m & 0xff    
        cmd[133-128] = self._b.cdb_chkcode(cmd)             
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])

        time.sleep(1)
        while self._b.cdb1_cip():
            pass

        if self._b.cdb1_success():
            eplLen = (self._b.twi_rr(130) << 8) | self._b.twi_rr(131)
            print(eplLen)
            rlplen = self._b.twi_rr(134)
            if(eplLen > 120) and (0 == rlplen):
                data = []
                pages = eplLen // 128
                for i in range(pages):
                    change_page_cmd = bytearray(b'\x00\xa0')
                    change_page_cmd[-1] = 0xa0 + i
                    self._b.twi_sbw(126, change_page_cmd)
                    time.sleep(0.1)
                    rlp = self._b.twi_srr(128, 128)
                    for i in range(int(128/4)):
                        b = bytearray()
                        b.append(rlp[1+4*i])
                        b.append(rlp[0+4*i])
                        b.append(rlp[3+4*i])
                        b.append(rlp[2+4*i])
                        data.append(struct.unpack('<1f', b)[0])                     
                    time.sleep(0.1)       
                if eplLen % 128:
                    change_page_cmd = bytearray(b'\x00\xa0')
                    change_page_cmd[-1] = 0xa0 + pages
                    self._b.twi_sbw(126, change_page_cmd)
                    time.sleep(0.1)
                    rlp = self._b.twi_srr(128, eplLen % 128)
                    for i in range(int((eplLen % 128)/4)):
                        b = bytearray()
                        b.append(rlp[1+4*i])
                        b.append(rlp[0+4*i])
                        b.append(rlp[3+4*i])
                        b.append(rlp[2+4*i])
                        data.append(struct.unpack('<1f', b)[0]) 
                print(len(data))    
                return data
            else:
                rlp_chkcode = self._b.twi_rr(135)
                rlp = self._b.twi_srr(136, rlplen)
                if self._b.cdb_chkcode(rlp) == rlp_chkcode:
                    data = []
                    for i in range(int(rlplen/4)):
                        b = bytearray()
                        b.append(rlp[1+4*i])
                        b.append(rlp[0+4*i])
                        b.append(rlp[3+4*i])
                        b.append(rlp[2+4*i])
                        data.append(struct.unpack('<1f', b)[0]) 
                    return data


    def curr_demod(self, ph):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x07\x00\x00\x00\x0f\x08\x0b\x00\x0b\x00\x00')
        cmd[-2] = (ph >> 8) & 0xff
        cmd[-1] = ph & 0xff    
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
                b = bytearray()
                b.append(rlp[1])
                b.append(rlp[0])
                b.append(rlp[3])
                b.append(rlp[2])
                return struct.unpack('<1f', b)[0] 

    @property
    def iir(self):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x05\x00\x00\x00\x0f\x08\x0b\x00\x22')
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
                return rlp[0] << 8 | rlp[1] 

    @iir.setter
    def iir(self, val):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x07\x00\x00\x00\x0f\x08\x0b\x00\x22\x00\x00')
        cmd[-2] = (val >> 8) & 0xff
        cmd[-1] = val & 0xff
        cmd[133-128] = self._b.cdb_chkcode(cmd)             
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        while self._b.cdb1_cip():
            pass

    @property
    def iirn(self):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x05\x00\x00\x00\x0f\x08\x0b\x00\x23')
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
                b = bytearray()
                b.append(rlp[1])
                b.append(rlp[0])
                b.append(rlp[3])
                b.append(rlp[2])
                n0 = struct.unpack('<1f', b)[0] 
                b = bytearray()
                b.append(rlp[5])
                b.append(rlp[4])
                b.append(rlp[7])
                b.append(rlp[6])
                n1 = struct.unpack('<1f', b)[0]
                b = bytearray()
                b.append(rlp[9])
                b.append(rlp[8])
                b.append(rlp[11])
                b.append(rlp[10])
                n2 = struct.unpack('<1f', b)[0]
                return n0,n1,n2

    @iirn.setter
    def iirn(self, vals):
        n0, n1, n2 = vals
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x11\x00\x00\x00\x0f\x08\x0b\x00\x23\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        vs = struct.pack('<1f', n0)
        cmd[-12] = vs[1]
        cmd[-11] = vs[0]   
        cmd[-10] = vs[3]
        cmd[-9] = vs[2]
        
        vs = struct.pack('<1f', n1)
        cmd[-8] = vs[1]
        cmd[-7] = vs[0]   
        cmd[-6] = vs[3]
        cmd[-5] = vs[2]      

        vs = struct.pack('<1f', n2)
        cmd[-4] = vs[1]
        cmd[-3] = vs[0]   
        cmd[-2] = vs[3]
        cmd[-1] = vs[2]
        cmd[133-128] = self._b.cdb_chkcode(cmd)             
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        while self._b.cdb1_cip():
            pass

    @property
    def iird(self):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x05\x00\x00\x00\x0f\x08\x0b\x00\x24')
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
                b = bytearray()
                b.append(rlp[1])
                b.append(rlp[0])
                b.append(rlp[3])
                b.append(rlp[2])
                n0 = struct.unpack('<1f', b)[0] 
                b = bytearray()
                b.append(rlp[5])
                b.append(rlp[4])
                b.append(rlp[7])
                b.append(rlp[6])
                n1 = struct.unpack('<1f', b)[0]
                b = bytearray()
                b.append(rlp[9])
                b.append(rlp[8])
                b.append(rlp[11])
                b.append(rlp[10])
                n2 = struct.unpack('<1f', b)[0]
                return n0,n1,n2

    @iird.setter
    def iird(self, vals):
        n0, n1, n2 = vals
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x11\x00\x00\x00\x0f\x08\x0b\x00\x24\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        vs = struct.pack('<1f', n0)
        cmd[-12] = vs[1]
        cmd[-11] = vs[0]   
        cmd[-10] = vs[3]
        cmd[-9] = vs[2]
        
        vs = struct.pack('<1f', n1)
        cmd[-8] = vs[1]
        cmd[-7] = vs[0]   
        cmd[-6] = vs[3]
        cmd[-5] = vs[2]      

        vs = struct.pack('<1f', n2)
        cmd[-4] = vs[1]
        cmd[-3] = vs[0]   
        cmd[-2] = vs[3]
        cmd[-1] = vs[2]
        cmd[133-128] = self._b.cdb_chkcode(cmd)             
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        while self._b.cdb1_cip():
            pass

    @property
    def iirpp(self):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x03\x00\x00\x00\x0f\x08\x0f')
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

    @iirpp.setter
    def iirpp(self, val):
        while not self._b.cdb1_idle():
            pass
        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x05\x00\x00\x00\x0f\x08\x0e\x00\x00')
        cmd[-2] = (val >> 8) & 0xff
        cmd[-1] = val & 0xff
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        while self._b.cdb1_cip():
            pass

    def target_get(self, ph):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x07\x00\x00\x00\x0f\x08\x0b\x00\x0d\x00\x00')
        cmd[-2] = (ph >> 8) & 0xff
        cmd[-1] = ph & 0xff    
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
                b = bytearray()
                b.append(rlp[1])
                b.append(rlp[0])
                b.append(rlp[3])
                b.append(rlp[2])
                return struct.unpack('<1f', b)[0] 


    def target_set(self, ph, val):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x0b\x00\x00\x00\x0f\x08\x0b\x00\x0d\x00\x00\x00\x00\x00\x00')
        cmd[-6] = (ph >> 8) & 0xff
        cmd[-5] = ph & 0xff   

        vs = struct.pack('<1f', val)
        cmd[-4] = vs[1]
        cmd[-3] = vs[0]   
        cmd[-2] = vs[3]
        cmd[-1] = vs[2]                       
        cmd[133-128] = self._b.cdb_chkcode(cmd)             
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        while self._b.cdb1_cip():
            pass

   

    def calc(self,polarity,gain_p,pre_out,demod_res):
        curr_demod = demod_res * polarity
        out = curr_demod * gain_p
        cur_out = math.sqrt(pre_out*pre_out + out)
        return cur_out


    @property
    def fine(self):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x05\x00\x00\x00\x0f\x08\x0b\x00\x10')
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
                return rlp[0] << 8 | rlp[1]

    @fine.setter
    def fine(self, val):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x07\x00\x00\x00\x0f\x08\x0b\x00\x10\x00\x00')
        cmd[-2] = (val >> 8) & 0xff
        cmd[-1] = val & 0xff   
        cmd[133-128] = self._b.cdb_chkcode(cmd)             
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        while self._b.cdb1_cip():
            pass
    
    def reset(self):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x05\x00\x00\x00\x0f\x08\x0b\x00\x12')
                       
        cmd[133-128] = self._b.cdb_chkcode(cmd)             
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        while self._b.cdb1_cip():
            pass
    
    
    def converged_time(self,ph):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x07\x00\x00\x00\x0f\x08\x0b\x00\x13\x00\x00')
        cmd[-2] = (ph >> 8) & 0xff
        cmd[-1] = ph & 0xff 
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
                return rlp[0] << 8 | rlp[1]

    def record_table(self, ph):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x07\x00\x00\x00\x0f\x08\x0b\x00\x14\x00\x00')
        cmd[-2] = (ph >> 8) & 0xff
        cmd[-1] = ph & 0xff    
        cmd[133-128] = self._b.cdb_chkcode(cmd)             
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])

        time.sleep(1)
        while self._b.cdb1_cip():
            pass

        if self._b.cdb1_success():
            eplLen = (self._b.twi_rr(130) << 8) | self._b.twi_rr(131)
            print(eplLen)
            rlplen = self._b.twi_rr(134)
            if(eplLen > 120) and (0 == rlplen):
                data = []
                pages = eplLen // 128
                for i in range(pages):
                    change_page_cmd = bytearray(b'\x00\xa0')
                    change_page_cmd[-1] = 0xa0 + i
                    self._b.twi_sbw(126, change_page_cmd)
                    time.sleep(0.1)
                    rlp = self._b.twi_srr(128, 128)
                    for i in range(int(128/2)):
                        data.append(struct.unpack('>H', rlp[(0+i*2):(2+i*2)])[0])                    
                    time.sleep(0.1)       
                if eplLen % 128:
                    change_page_cmd = bytearray(b'\x00\xa0')
                    change_page_cmd[-1] = 0xa0 + pages
                    self._b.twi_sbw(126, change_page_cmd)
                    time.sleep(0.1)
                    rlp = self._b.twi_srr(128, eplLen % 128)
                    for i in range(int((eplLen % 128)/2)):
                        data.append(struct.unpack('>H', rlp[(0+i*2):(2+i*2)])[0]) 
                print(len(data))    
                return data
            else:
                rlp_chkcode = self._b.twi_rr(135)
                rlp = self._b.twi_srr(136, rlplen)
                if self._b.cdb_chkcode(rlp) == rlp_chkcode:
                    data = []
                    for i in range(int(rlplen/2)):
                        data.append(struct.unpack('>H', rlp[(0+i*2):(2+i*2)])[0]) 
                    return data
    def record_start(self, ph):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x09\x00\x00\x00\x0f\x08\x0b\x00\x14\x00\x00\x00\x00')
        cmd[-4] = (ph >> 8) & 0xff
        cmd[-3] = ph & 0xff    
        cmd[133-128] = self._b.cdb_chkcode(cmd)             
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])

        time.sleep(1)
        while self._b.cdb1_cip():
            pass
   
    def dither_amp_get(self, ph):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x07\x00\x00\x00\x0f\x08\x0b\x00\x15\x00\x00')
        cmd[-2] = (ph >> 8) & 0xff
        cmd[-1] = ph & 0xff    
        cmd[133-128] = self._b.cdb_chkcode(cmd)             
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])

        time.sleep(0.1)
        while self._b.cdb1_cip():
            pass        

        if self._b.cdb1_success():
            rlplen = self._b.twi_rr(134)
            rlp_chkcode = self._b.twi_rr(135)
            rlp = self._b.twi_srr(136, rlplen)
            if self._b.cdb_chkcode(rlp) == rlp_chkcode:
                return rlp[0] << 8 | rlp[1]

    
    def dither_amp_set(self, ph, val):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x09\x00\x00\x00\x0f\x08\x0b\x00\x15\x00\x00\x00\x00')
        cmd[-4] = (ph >> 8) & 0xff
        cmd[-3] = ph & 0xff

        cmd[-2] = (val >> 8) & 0xff
        cmd[-1] = val & 0xff 

        cmd[133-128] = self._b.cdb_chkcode(cmd)             
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])

        time.sleep(0.1)
        while self._b.cdb1_cip():
            pass 


    def adc_table(self,m):
 
        log_file = open("ABC-FEEDBACK-ADC-log-{}.csv".format(time.strftime("%Y%m%d%H%M%S")), 'w')
        
        data_i = self.adc_table_0(m)
        time.sleep(1)

        while data_i != []:
            for data in data_i: 
                log_file.write("{}\n".format(data))

            data_i = self.adc_table_1(m)           
            time.sleep(1)

        

    def adc_table_0(self, m):
       

        data = []

        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')


        cmd = bytearray(b'\x80\x00\x00\x00\x07\x00\x00\x00\x0f\x08\x0b\x00\x16\x00\x00')

        
        
        cmd[-2] = (m >> 8) & 0xff
        cmd[-1] = m & 0xff    
        cmd[133-128] = self._b.cdb_chkcode(cmd)             
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])

        time.sleep(1)
        while self._b.cdb1_cip():
            pass

        if self._b.cdb1_success():
            eplLen = (self._b.twi_rr(130) << 8) | self._b.twi_rr(131)
            # print(eplLen)
            rlplen = self._b.twi_rr(134)
            if(eplLen > 120) and (0 == rlplen):
                pages = eplLen // 128
                for i in range(pages):
                    change_page_cmd = bytearray(b'\x00\xa0')
                    change_page_cmd[-1] = 0xa0 + i
                    self._b.twi_sbw(126, change_page_cmd)
                    time.sleep(0.1)
                    rlp = self._b.twi_srr(128, 128)
                    for i in range(int(128/2)):
                        data.append(struct.unpack('>H', rlp[(0+i*2):(2+i*2)])[0])                    
                    time.sleep(0.1)       
                if eplLen % 128:
                    change_page_cmd = bytearray(b'\x00\xa0')
                    change_page_cmd[-1] = 0xa0 + pages
                    self._b.twi_sbw(126, change_page_cmd)
                    time.sleep(0.1)
                    rlp = self._b.twi_srr(128, eplLen % 128)
                    for i in range(int((eplLen % 128)/2)):
                        data.append(struct.unpack('>H', rlp[(0+i*2):(2+i*2)])[0])
                print(len(data))    
                # return data
            else:              
                rlp_chkcode = self._b.twi_rr(135)
                rlp = self._b.twi_srr(136, rlplen)
                if self._b.cdb_chkcode(rlp) == rlp_chkcode:
                    data = []
                    for i in range(int(rlplen/2)):
                        data.append(struct.unpack('>H', rlp[(0+i*2):(2+i*2)])[0])
                    # return data

                

            
        return data

    def adc_table_1(self, m):
       

        data = []

        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')


        cmd = bytearray(b'\x80\x00\x00\x00\x07\x00\x00\x00\x0f\x08\x0b\x00\x17\x00\x00')

        
        
        cmd[-2] = (m >> 8) & 0xff
        cmd[-1] = m & 0xff    
        cmd[133-128] = self._b.cdb_chkcode(cmd)             
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])

        time.sleep(1)
        while self._b.cdb1_cip():
            pass

        if self._b.cdb1_success():
            eplLen = (self._b.twi_rr(130) << 8) | self._b.twi_rr(131)
            # print(eplLen)
            rlplen = self._b.twi_rr(134)
            if(eplLen > 120) and (0 == rlplen):
                pages = eplLen // 128
                for i in range(pages):
                    change_page_cmd = bytearray(b'\x00\xa0')
                    change_page_cmd[-1] = 0xa0 + i
                    self._b.twi_sbw(126, change_page_cmd)
                    time.sleep(0.1)
                    rlp = self._b.twi_srr(128, 128)
                    for i in range(int(128/2)):
                        data.append(struct.unpack('>H', rlp[(0+i*2):(2+i*2)])[0])                    
                    time.sleep(0.1)       
                if eplLen % 128:
                    change_page_cmd = bytearray(b'\x00\xa0')
                    change_page_cmd[-1] = 0xa0 + pages
                    self._b.twi_sbw(126, change_page_cmd)
                    time.sleep(0.1)
                    rlp = self._b.twi_srr(128, eplLen % 128)
                    for i in range(int((eplLen % 128)/2)):
                        data.append(struct.unpack('>H', rlp[(0+i*2):(2+i*2)])[0])
                print(len(data))    
                # return data
            else:              
                rlp_chkcode = self._b.twi_rr(135)
                rlp = self._b.twi_srr(136, rlplen)
                if self._b.cdb_chkcode(rlp) == rlp_chkcode:
                    data = []
                    for i in range(int(rlplen/2)):
                        data.append(struct.unpack('>H', rlp[(0+i*2):(2+i*2)])[0])
                    # return data

                

            
        return data

    def iir_table(self,m):
 
        log_file = open("ABC-FEEDBACK-IIR-log-{}.csv".format(time.strftime("%Y%m%d%H%M%S")), 'w')
        
        data_i = self.iir_table_0(m)
        time.sleep(1)

        while data_i != []:
            for data in data_i: 
                log_file.write("{}\n".format(data))

            data_i = self.iir_table_1(m)           
            time.sleep(1)

        

    def iir_table_0(self, m):
       

        data = []

        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')


        cmd = bytearray(b'\x80\x00\x00\x00\x07\x00\x00\x00\x0f\x08\x0b\x00\x25\x00\x00')

        
        
        cmd[-2] = (m >> 8) & 0xff
        cmd[-1] = m & 0xff    
        cmd[133-128] = self._b.cdb_chkcode(cmd)             
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])

        time.sleep(1)
        while self._b.cdb1_cip():
            pass

        if self._b.cdb1_success():
            eplLen = (self._b.twi_rr(130) << 8) | self._b.twi_rr(131)
            # print(eplLen)
            rlplen = self._b.twi_rr(134)
            if(eplLen > 120) and (0 == rlplen):
                pages = eplLen // 128
                for i in range(pages):
                    change_page_cmd = bytearray(b'\x00\xa0')
                    change_page_cmd[-1] = 0xa0 + i
                    self._b.twi_sbw(126, change_page_cmd)
                    time.sleep(0.1)
                    rlp = self._b.twi_srr(128, 128)
                    for i in range(int(128/4)):
                        f = bytearray()
                        f.append(rlp[1+i*4])
                        f.append(rlp[0+i*4])
                        f.append(rlp[3+i*4])
                        f.append(rlp[2+i*4])
                        data.append(struct.unpack('<f', f)[0])                    
                    time.sleep(0.1)       
                if eplLen % 128:
                    change_page_cmd = bytearray(b'\x00\xa0')
                    change_page_cmd[-1] = 0xa0 + pages
                    self._b.twi_sbw(126, change_page_cmd)
                    time.sleep(0.1)
                    rlp = self._b.twi_srr(128, eplLen % 128)
                    for i in range(int((eplLen % 128)/4)):
                        f = bytearray()
                        f.append(rlp[1+i*4])
                        f.append(rlp[0+i*4])
                        f.append(rlp[3+i*4])
                        f.append(rlp[2+i*4])
                        data.append(struct.unpack('<f', f)[0])
                print(len(data))    
                # return data
            else:              
                rlp_chkcode = self._b.twi_rr(135)
                rlp = self._b.twi_srr(136, rlplen)
                if self._b.cdb_chkcode(rlp) == rlp_chkcode:
                    data = []
                    for i in range(int(rlplen/4)):
                        f = bytearray()
                        f.append(rlp[1+i*4])
                        f.append(rlp[0+i*4])
                        f.append(rlp[3+i*4])
                        f.append(rlp[2+i*4])
                        data.append(struct.unpack('<f', f)[0])
                    # return data

                

            
        return data

    def iir_table_1(self, m):
       

        data = []

        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')


        cmd = bytearray(b'\x80\x00\x00\x00\x07\x00\x00\x00\x0f\x08\x0b\x00\x26\x00\x00')

        
        
        cmd[-2] = (m >> 8) & 0xff
        cmd[-1] = m & 0xff    
        cmd[133-128] = self._b.cdb_chkcode(cmd)             
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])

        time.sleep(1)
        while self._b.cdb1_cip():
            pass

        if self._b.cdb1_success():
            eplLen = (self._b.twi_rr(130) << 8) | self._b.twi_rr(131)
            # print(eplLen)
            rlplen = self._b.twi_rr(134)
            if(eplLen > 120) and (0 == rlplen):
                pages = eplLen // 128
                for i in range(pages):
                    change_page_cmd = bytearray(b'\x00\xa0')
                    change_page_cmd[-1] = 0xa0 + i
                    self._b.twi_sbw(126, change_page_cmd)
                    time.sleep(0.1)
                    rlp = self._b.twi_srr(128, 128)
                    for i in range(int(128/4)):
                        f = bytearray()
                        f.append(rlp[1+i*4])
                        f.append(rlp[0+i*4])
                        f.append(rlp[3+i*4])
                        f.append(rlp[2+i*4])
                        data.append(struct.unpack('<f', f)[0])                    
                    time.sleep(0.1)       
                if eplLen % 128:
                    change_page_cmd = bytearray(b'\x00\xa0')
                    change_page_cmd[-1] = 0xa0 + pages
                    self._b.twi_sbw(126, change_page_cmd)
                    time.sleep(0.1)
                    rlp = self._b.twi_srr(128, eplLen % 128)
                    for i in range(int((eplLen % 128)/4)):
                        f = bytearray()
                        f.append(rlp[1+i*4])
                        f.append(rlp[0+i*4])
                        f.append(rlp[3+i*4])
                        f.append(rlp[2+i*4])
                        data.append(struct.unpack('<f', f)[0])
                print(len(data))    
                # return data
            else:              
                rlp_chkcode = self._b.twi_rr(135)
                rlp = self._b.twi_srr(136, rlplen)
                if self._b.cdb_chkcode(rlp) == rlp_chkcode:
                    data = []
                    for i in range(int(rlplen/4)):
                        f = bytearray()
                        f.append(rlp[1+i*4])
                        f.append(rlp[0+i*4])
                        f.append(rlp[3+i*4])
                        f.append(rlp[2+i*4])
                        data.append(struct.unpack('<f', f)[0])
                    # return data

                

            
        return data

    @property
    def ctl_interval(self):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x05\x00\x00\x00\x0f\x08\x0b\x00\x18')
  
        cmd[133-128] = self._b.cdb_chkcode(cmd)             
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])

        time.sleep(0.1)
        while self._b.cdb1_cip():
            pass       

        if self._b.cdb1_success():
            rlplen = self._b.twi_rr(134)
            rlp_chkcode = self._b.twi_rr(135)
            rlp = self._b.twi_srr(136, rlplen)
            if self._b.cdb_chkcode(rlp) == rlp_chkcode:
                return rlp[0] << 8 | rlp[1]

    @ctl_interval.setter
    def ctl_interval(self, ms):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x07\x00\x00\x00\x0f\x08\x0b\x00\x18\x00\x00')
        cmd[-2] = (ms >> 8) & 0xff
        cmd[-1] = ms & 0xff    
        cmd[133-128] = self._b.cdb_chkcode(cmd)             
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])

        time.sleep(0.1)
        while self._b.cdb1_cip():
            pass   

    @property
    def log(self):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x05\x00\x00\x00\x0f\x08\x0b\x00\x19')
  
        cmd[133-128] = self._b.cdb_chkcode(cmd)             
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])

        time.sleep(0.1)
        while self._b.cdb1_cip():
            pass       

        if self._b.cdb1_success():
            rlplen = self._b.twi_rr(134)
            rlp_chkcode = self._b.twi_rr(135)
            rlp = self._b.twi_srr(136, rlplen)
            if self._b.cdb_chkcode(rlp) == rlp_chkcode:
                return rlp[0] << 8 | rlp[1]

    @log.setter
    def log(self, en):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x07\x00\x00\x00\x0f\x08\x0b\x00\x19\x00\x00')
        cmd[-2] = (en >> 8) & 0xff
        cmd[-1] = en & 0xff    
        cmd[133-128] = self._b.cdb_chkcode(cmd)             
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])

        time.sleep(0.1)
        while self._b.cdb1_cip():
            pass      

    def log_clear(self):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x05\x00\x00\x00\x0f\x08\x0b\x00\x20')
  
        cmd[133-128] = self._b.cdb_chkcode(cmd)             
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])

        time.sleep(0.1)
        while self._b.cdb1_cip():
            pass   

    def log_table_x(self):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x05\x00\x00\x00\x0f\x08\x0b\x00\x21')
  
        cmd[133-128] = self._b.cdb_chkcode(cmd)             
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])

        time.sleep(1)
        while self._b.cdb1_cip():
            pass

        data = bytearray(b'')
        if self._b.cdb1_success():
            eplLen = (self._b.twi_rr(130) << 8) | self._b.twi_rr(131)
            # print(eplLen)
            rlplen = self._b.twi_rr(134)
            
            if(eplLen > 120) and (0 == rlplen):
                pages = eplLen // 128
                
                for i in range(pages):
                    change_page_cmd = bytearray(b'\x00\xa0')
                    change_page_cmd[-1] = 0xa0 + i
                    self._b.twi_sbw(126, change_page_cmd)
                    time.sleep(0.1)
                    rlp = self._b.twi_srr(128, 128)
                    data = data + rlp
                    # for i in range(int(128/2)):
                    #     data.append(struct.unpack('>H', rlp[(0+i*2):(2+i*2)])[0])                    
                    time.sleep(0.1)       
                if eplLen % 128:
                    change_page_cmd = bytearray(b'\x00\xa0')
                    change_page_cmd[-1] = 0xa0 + pages
                    self._b.twi_sbw(126, change_page_cmd)
                    time.sleep(0.1)
                    rlp = self._b.twi_srr(128, eplLen % 128)
                    data = data + rlp
                    # for i in range(int((eplLen % 128))):
                    #     data.append(struct.unpack('B', rlp[(0+i):(1+i)])[0])
                # print(len(data))    
                # return data
            else:              
                rlp_chkcode = self._b.twi_rr(135)
                rlp = self._b.twi_srr(136, rlplen)
                if self._b.cdb_chkcode(rlp) == rlp_chkcode:
                    data = rlp
        data_res = bytearray(len(data))
        print(len(data))
        # print(data) 

   
        for i in range(int(len(data)/2)):
            data_res[0+2*i] = data[1+2*i]
            data_res[1+2*i] = data[0+2*i]

        # print(data_res) 
        return data_res


    def log_table(self):
        
        data = bytearray(b'')
        data_i = self.log_table_x()
        data = data + data_i
        time.sleep(1)

        while data_i != b'':
            data_i = self.log_table_x()  
            data = data + data_i         
            time.sleep(1)

        log_info = {}
        LOG_SIZE = 32

        log_file = open("ABC-Closed-Loop-CTRL-log-{}.csv".format(time.strftime("%Y%m%d%H%M%S")), 'w')
        log_file.write('{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(
            'Timetick(s)',
            'Loop_id',
            'Phase_id',
            'XP_Bias(v)', 'XI_Bias(v)', 'XQ_Bias(v)', 'YP_Bias(v)', 'YI_Bias(v)', 'YQ_Bias(v)',
            'Vgar',
            'Converged',
            'Sine_Demod',
            'Cosine_Demod',
            'Amplitude_Demod'
        ))
        print(len(data))
        try:
            for i in range(int(len(data)/LOG_SIZE)):
                log_info['TimeTick'] = struct.unpack('<f', data[(0+i*LOG_SIZE):(4+i*LOG_SIZE)])[0]
                log_info['Loop_id'] = struct.unpack('<H', data[(4+i*LOG_SIZE):(6+i*LOG_SIZE)])[0]
                log_info['Phase_id'] = struct.unpack('B', data[(6+i*LOG_SIZE):(7+i*LOG_SIZE)])[0]

                log_info['XP_Bias'] = struct.unpack('<H', data[(8+i*LOG_SIZE):(10+i*LOG_SIZE)])[0]/4096*2.5*219.1/220.1 * 1.1 
                log_info['XI_Bias'] = struct.unpack('<H', data[(10+i*LOG_SIZE):(12+i*LOG_SIZE)])[0]/4096*2.5*219.1/220.1 * 1.1
                log_info['XQ_Bias'] = struct.unpack('<H', data[(12+i*LOG_SIZE):(14+i*LOG_SIZE)])[0]/4096*2.5*219.1/220.1 * 1.1
                log_info['YP_Bias'] = struct.unpack('<H', data[(14+i*LOG_SIZE):(16+i*LOG_SIZE)])[0]/4096*2.5*219.1/220.1 * 1.1
                log_info['YI_Bias'] = struct.unpack('<H', data[(16+i*LOG_SIZE):(18+i*LOG_SIZE)])[0]/4096*2.5*219.1/220.1 * 1.1
                log_info['YQ_Bias'] = struct.unpack('<H', data[(18+i*LOG_SIZE):(20+i*LOG_SIZE)])[0]/4096*2.5*219.1/220.1 * 1.1

                log_info['Vgar'] = struct.unpack('B', data[(20+i*LOG_SIZE):(21+i*LOG_SIZE)])[0]
                log_info['Converged'] = struct.unpack('B', data[(21+i*LOG_SIZE):(22+i*LOG_SIZE)])[0]

                log_info['Sine_Demod'] = struct.unpack('<f', data[(24+i*LOG_SIZE):(28+i*LOG_SIZE)])[0]
                log_info['Cosine_Demod'] = struct.unpack('<f', data[(28+i*LOG_SIZE):(32+i*LOG_SIZE)])[0]
                log_info['Amplitude_Demod'] = math.sqrt(log_info['Sine_Demod']**2 + log_info['Cosine_Demod']**2)
            
                log_file.write('{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(
                    log_info['TimeTick'],
                    log_info['Loop_id'],
                    log_info['Phase_id'],
                    log_info['XP_Bias'], log_info['XI_Bias'], log_info['XQ_Bias'], log_info['YP_Bias'], log_info['YI_Bias'], log_info['YQ_Bias'],
                    log_info['Vgar'],
                    log_info['Converged'],
                    log_info['Sine_Demod'],
                    log_info['Cosine_Demod'],
                    log_info['Amplitude_Demod']
                ))
        except:
            log_file.close()

        log_file.close()
        
        # return data

                