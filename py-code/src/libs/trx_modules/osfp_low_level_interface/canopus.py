from .broker import Broker
from .ain import Ain
from .dpin import DPin
import time
import struct
import math
from .fpn import cal

class Canopus:
    def __init__(self, broker):
        self._b = broker
        # self._vdd18_en = DPin(broker, 'EN_DSP_VDD18')
        # self._vdd18 = Ain(broker, 'DSP_VDDIO18_ADC')
        # self._vdd_en = DPin(broker, 'EN_DSP_VDD')
        # self._vdd = Ain(broker, 'DSP_VDD_ADC')
        # self._vddm_en = DPin(broker, 'EN_DSP_VDDM')
        # self._vddm = Ain(broker, 'DSP_VDDM_ADC')
        # self._vdda_en = DPin(broker, 'EN_DSP_VDDA')
        # self._vdda = Ain(broker, 'DSP_VDDA_ADC')
        # self._vdda12_en = DPin(broker, 'EN_DSP_VDDA12')
        # self._vdda12 = Ain(broker, 'DSP_VDDA12_ADC')
        self._rstn = DPin(broker, 'MCU1_DSP_RSTN')

    def reset(self):
        self._rstn.state = 0
        time.sleep(0.001)
        self._rstn.state = 1

    def get_crc(self):
        while not self._b.cdb1_idle():
            pass
        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x03\x00\x00\x00\x0f\x07\x06')
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        time.sleep(3)
        while self._b.cdb1_cip():
            pass

        if self._b.cdb1_success():
            rlplen = self._b.twi_rr(134)
            print('rlplen %d.\n' % rlplen)
            rlp_chkcode = self._b.twi_rr(135)
            rlp = self._b.twi_srr(136, rlplen)
            if self._b.cdb_chkcode(rlp) == rlp_chkcode:
                print(rlp)
                print('Read Out Flash CRC %08x.\n' % struct.unpack('>I', rlp[0:4])[0])
                print('Read Out DSP CRC %08x.\n' % struct.unpack('>I', rlp[4:8])[0])

    def bin_verify(self):
        while not self._b.cdb1_idle():
            pass
        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x03\x00\x00\x00\x0f\x07\x03')
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        time.sleep(3)
        while self._b.cdb1_cip():
            pass

        if self._b.cdb1_success():
            rlplen = self._b.twi_rr(134)
            print('rlplen %d.\n' % rlplen)
            rlp_chkcode = self._b.twi_rr(135)
            rlp = self._b.twi_srr(136, rlplen)
            if self._b.cdb_chkcode(rlp) == rlp_chkcode:
                return rlp[0]

    def polling_suspend_resume(self, val):
        while not self._b.cdb1_idle():
            pass
        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x04\x00\x00\x00\x0f\x07\x04\x00')
        cmd[-1] = val
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        time.sleep(3)
        while self._b.cdb1_cip():
            pass

    def startup(self):
        while not self._b.cdb1_idle():
            pass
        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x03\x00\x00\x00\x0f\x07\x01')
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        # while self._b.cdb1_cip():
        #     pass

    def power_down(self):
        while not self._b.cdb1_idle():
            pass
        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x03\x00\x00\x00\x0f\x07\x05')
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        # while self._b.cdb1_cip():
        #     pass

    def api_epl(self, byteArray):
        while not self._b.cdb1_idle():
            pass
        txLen = len(byteArray)
        rspLen = struct.unpack('<H',byteArray[4:6])[0]
        #write data to AX Page
        pages = txLen // 128
        for i in range(pages):
            change_page_cmd = bytearray(b'\x00\xa0')
            change_page_cmd[-1] = 0xa0 + i
            self._b.twi_sbw(126, change_page_cmd)
            time.sleep(0.1)
            self._b.twi_sbw(128, byteArray[i*128:(i+1)*128])
            time.sleep(0.1)       
        if txLen % 128:
            change_page_cmd = bytearray(b'\x00\xa0')
            change_page_cmd[-1] = 0xa0 + pages
            self._b.twi_sbw(126, change_page_cmd)
            time.sleep(0.1)
            self._b.twi_sbw(128, byteArray[pages*128:])
            time.sleep(0.1) 


        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x03\x00\x00\x00\x0f\x07\x02')
        cmd[2] = (txLen >> 8) & 0xff # EPL MSB
        cmd[3] = txLen & 0xff # EPL LSB
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        # print(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        time.sleep(0.5)
        while self._b.cdb1_cip():
            pass

        if self._b.cdb1_success():
            pages = rspLen // 128
            rlp = b''
            for i in range(pages):
                change_page_cmd = bytearray(b'\x00\xa0')
                change_page_cmd[-1] = 0xa0 + i
                self._b.twi_sbw(126, change_page_cmd)
                time.sleep(0.1)
                rlp += self._b.twi_srr(128, 128)
                time.sleep(0.1)       

            if rspLen % 128:
                change_page_cmd = bytearray(b'\x00\xa0')
                change_page_cmd[-1] = 0xa0 + pages
                self._b.twi_sbw(126, change_page_cmd)
                time.sleep(0.1)
                rlp += self._b.twi_srr(128, rspLen % 128)
                time.sleep(0.1)      
            
            return struct.pack('%sB'%len(rlp), *rlp)

    
    def api_lpl(self, byteArray):
        while not self._b.cdb1_idle():
            pass
        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x03\x00\x00\x00\x0f\x07\x02')
        txlen = len(byteArray)
        # print(txlen)
        cmd[4] = 3 + txlen #total tx len
        # print(cmd[4])
        i = 0
        while i < txlen:
            cmd.append(byteArray[i])
            i += 1
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        # print(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        time.sleep(0.5)
        while self._b.cdb1_cip():
            pass

        if self._b.cdb1_success():
            rlplen = self._b.twi_rr(134)
            print('rlplen %d.\n' % rlplen)
            rlp_chkcode = self._b.twi_rr(135)
            rlp = self._b.twi_srr(136, rlplen)
            if self._b.cdb_chkcode(rlp) == rlp_chkcode:
                # print(struct.pack('%sB'%len(rlp), *rlp))
                return struct.pack('%sB'%len(rlp), *rlp)

    def api(self, byteArray):
        # if len(byteArray) > 120:
        return self.api_epl(byteArray) 
        # else:
            # return api_lpl(byteArrar)

    def send_command(self, data):#use this command for inphi canopus_api.py
        print(data)
        length = len(data)
        i = 0
        while i < length:
            data[i] = data[i] & 0xff
            i += 1
        print(data)
        rsp = self.api(bytearray(data)) 
        print(rsp)
        return rsp

    def state(self):
        return self._b.twi_rr(63)

    @property
    def avs(self):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x03\x00\x00\x00\x0f\x07\x08')

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
        
    @avs.setter
    def avs(self, val):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x04\x00\x00\x00\x0f\x07\x07\x00')
        if val:  # enable
            cmd[-1] = 1
        else:
            cmd[-1] = 0
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        while self._b.cdb1_cip():
            pass

    @property
    def ratio(self):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x03\x00\x00\x00\x0f\x07\x0A')

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
        
    @ratio.setter
    def ratio(self, val):
        while not self._b.cdb1_idle():
            pass

        self._b.twi_sbw(126, b'\x00\x9f')
        cmd = bytearray(b'\x80\x00\x00\x00\x04\x00\x00\x00\x0f\x07\x09\x00')
        cmd[-1] = val
        cmd[133-128] = self._b.cdb_chkcode(cmd)
        self._b.twi_sbw(130, cmd[2:])
        self._b.twi_sbw(128, cmd[:2])
        while self._b.cdb1_cip():
            pass
        
    def power(self, on):
        while not self._b.ddb_idle():
            pass
        self._b.mdio_write(0x9c02, 0x0E)
        self._b.mdio_write(0x9c03, on)
        self._b.mdio_write(0x9c01, 2)
        self._b.mdio_write(0x9c00, 0x0f07)
        while self._b.ddb_cip():
            pass

    def trw(self, addr, val):
        # while not self._b.ddb_idle():
        #     pass
        # self._b.mdio_write(0x9c02, 0x05)
        # self._b.mdio_write(0x9c03, addr & 0xffff)
        # self._b.mdio_write(0x9c04, addr >> 16)
        # self._b.mdio_write(0x9c05, val & 0xffff)
        # self._b.mdio_write(0x9c06, val >> 16)
        # self._b.mdio_write(0x9c01, 5)
        # self._b.mdio_write(0x9c00, 0x0f07)
        # while self._b.ddb_cip():
            pass

    def rr(self, addr):
        # while not self._b.ddb_idle():
        #     pass
        # self._b.mdio_write(0x9c02, 0x0A)
        # self._b.mdio_write(0x9c03, addr & 0xffff)
        # self._b.mdio_write(0x9c04, addr >> 16)
        # self._b.mdio_write(0x9c01, 3)
        # self._b.mdio_write(0x9c00, 0x0f07)
        # while self._b.ddb_cip():
        #     pass
        # h1 = self._b.mdio_read(0x9c02)
        # h2 = self._b.mdio_read(0x9c03)
        # return h1 << 16 | h2
        pass

    def rw(self, addr, val):
        # while not self._b.ddb_idle():
        #     pass
        # self._b.mdio_write(0x9c02, 0x0B)
        # self._b.mdio_write(0x9c03, addr & 0xffff)
        # self._b.mdio_write(0x9c04, addr >> 16)
        # self._b.mdio_write(0x9c05, val & 0xffff)
        # self._b.mdio_write(0x9c06, val >> 16)
        # self._b.mdio_write(0x9c01, 5)
        # self._b.mdio_write(0x9c00, 0x0f07)
        # while self._b.ddb_cip():
            pass

    def load_firmware(self):
        # while not self._b.ddb_idle():
        #     pass
        # self._b.mdio_write(0x9c02, 0x0f)
        # self._b.mdio_write(0x9c01, 1)
        # self._b.mdio_write(0x9c00, 0x0f07)
        # while self._b.ddb_cip():
            pass

    def ReadRegister(self, regaddr):
        request = b'\x0c\x00\xe4\x01\x08\x00\x00\x00' + struct.pack('<I', regaddr)
        return self.api(request)

    def read_register(self, regaddr):
        response = self.ReadRegister(regaddr)
        return struct.unpack('<I', response[0x04:0x08])[0]

    def WriteRegister(self, regaddr, regval):
        request = b'\x10\x00\xe3\x01\x08\x00\x00\x00' + \
                  struct.pack('<I', regaddr) + \
                  struct.pack('<I', regval)
        return self.api(request)

    def SetOtuClientTestPatternGeneratorConfig(self, channel,
                                                     direction,
                                                     signal_type,
                                                     keep_incoming_fs,
                                                     enable):
        request = b'\x10\x00\x76\x01\x04\x00\x00\x00' + \
                  struct.pack('B', channel) + \
                  struct.pack('B', direction) + \
                  struct.pack('B', signal_type) + \
                  struct.pack('B', keep_incoming_fs) + \
                  struct.pack('B', enable) + b'\x00\x00\x00'
        return self.api(request)

    def GetOtuClientTestPatternGeneratorConfig(self, channel,
                                                     direction):
        request = b'\x0C\x00\x77\x01\x08\x00\x00\x00' + \
                  struct.pack('B', channel) + \
                  struct.pack('B', direction) + b'\x00\x00'
        return self.api(request)

    def SetOtuClientTestPatternCheckerConfig(self, channel,
                                                   direction,
                                                   signal_type,
                                                   enable):
        request = b'\x0c\x00\x78\x01\x04\x00\x00\x00' + \
                  struct.pack('B', channel) + \
                  struct.pack('B', direction) + \
                  struct.pack('B', signal_type) + \
                  struct.pack('B', enable)
        return self.api(request)

    def GetOtuClientTestPatternCheckerConfig(self, channel,
                                                     direction):
        request = b'\x0C\x00\x79\x01\x08\x00\x00\x00' + \
                  struct.pack('B', channel) + \
                  struct.pack('B', direction) + b'\x00\x00'
        return self.api(request)

    def GetOtuTestPatternCheckerStatistics(self, channel, direction):
        request = b'\x0c\x00\x7e\x01\x44\x00\x00\x00' + \
                  struct.pack('B', channel) + \
                  struct.pack('B', direction) + b'\x00\x00'
        return self.api(request)

    def get_OtuTestPatternCheckerStatistics(self, channel, direction):
        response = self.GetOtuTestPatternCheckerStatistics(channel, direction)
        rsp = {}
        rsp['accum_prbs_bit_count'] = struct.unpack('<Q', response[0x4:0xc])[0]
        rsp['accum_prbs_error_count'] = struct.unpack('<Q', response[0xc:0x14])[0]
        rsp['max_prbs_bit_count'] = struct.unpack('<Q', response[0x14:0x1c])[0]
        rsp['max_prbs_error_count'] = struct.unpack('<Q', response[0x1c:0x24])[0]
        rsp['min_prbs_bit_count'] = struct.unpack('<Q', response[0x24:0x2c])[0]
        rsp['min_prbs_error_count'] = struct.unpack('<Q', response[0x2c:0x34])[0]
        rsp['instant_prbs_bit_count'] = struct.unpack('<Q', response[0x34:0x3c])[0]
        rsp['instant_prbs_error_count'] = struct.unpack('<Q', response[0x3c:0x44])[0]
        return rsp


    def GetErrorCorrectionStatistics(self, channel, direction):
        request = b'\x0c\x00\x67\x01\x84\x00\x00\x00' + \
                  struct.pack('B', channel) + \
                  struct.pack('B', direction) + b'\x00\x00'
        return self.api(request)


    def get_error_correction_statistics(self, channel, direction):
        response = self.GetErrorCorrectionStatistics(channel, direction)
        rsp = {}
        rsp['accum_bit_count'] = struct.unpack('<Q', response[4:0xc])[0]
        rsp['accum_corrected_error_count'] = struct.unpack('<Q', response[0xc:0x14])[0]
        rsp['accum_uncorrected_codeword_count'] = struct.unpack('<Q', response[0x14:0x1c])[0]
        rsp['accum_codeword_count'] = struct.unpack('<Q', response[0x1c:0x24])[0]
        rsp['max_corrected_bit_count'] = struct.unpack('<Q', response[0x24:0x2c])[0]
        rsp['max_corrected_error_count'] = struct.unpack('<Q', response[0x2c:0x34])[0]
        rsp['max_uncorrected_codeword_count'] = struct.unpack('<Q', response[0x34:0x3c])[0]
        rsp['max_codeword_count'] = struct.unpack('<Q', response[0x3c:0x44])[0]
        rsp['min_corrected_bit_count'] = struct.unpack('<Q', response[0x44:0x4c])[0]
        rsp['min_corrected_error_count'] = struct.unpack('<Q', response[0x4c:0x54])[0]
        rsp['min_uncorrected_codeword_count'] = struct.unpack('<Q', response[0x54:0x5c])[0]
        rsp['min_codeword_count'] = struct.unpack('<Q', response[0x5c:0x64])[0]
        rsp['instant_corrected_bit_count'] = struct.unpack('<Q', response[0x64:0x6c])[0]
        rsp['instant_corrected_error_count'] = struct.unpack('<Q', response[0x6c:0x74])[0]
        rsp['instant_uncorrected_codeword_count'] = struct.unpack('<Q', response[0x74:0x7c])[0]
        rsp['instant_codeword_count'] = struct.unpack('<Q', response[0x7c:0x84])[0]
        return rsp

    def SetLoopbackMode(self, loopback_mode, channel, enable):
        request = b'\x0c\x00\x05\x01\x04\x00\x00\x00' + \
                  struct.pack('B', loopback_mode) + \
                  struct.pack('B', channel) + \
                  struct.pack('B', enable) + b'\x00'
        return self.api(request)

    def GetLoopbackMode(self, loopback_mode, channel):
        request = b'\x0c\x00\x06\x01\x08\x00\x00\x00' + \
                  struct.pack('B', loopback_mode) + \
                  struct.pack('B', channel) + b'\x00'
        return self.api(request)

    def SetLineEgressLaneMute(self, lane, mute):
        print(lane, mute)
        request = b'\x0c\x00\x2c\x01\x04\x00\x00\x00' + \
                  struct.pack('B', lane) + \
                  struct.pack('B', mute) + b'\x00\x00'
        return self.api(request)

    def GetLineEgressLaneMute(self, lane):
        request = b'\x0c\x00\x2d\x01\x08\x00\x00\x00' + \
                  struct.pack('B', lane) + b'\x00\x00\x00'
        return self.api(request)

    def GetFawErrorStatistics(self):
        request = b'\x08\x00\x65\x01\x44\x00\x00\x00'
        return self.api(request)

    def SetHostBallMap(self, hrx_mapping, htx_mapping):
        request = b'\x10\x00\x03\x01\x04\x00\x00\x00' + \
                  struct.pack('<I', hrx_mapping) + \
                  struct.pack('<I', htx_mapping)
        return self.api(request)

    def GetHostBallMap(self):
        request = b'\x08\x00\x04\x01\x0c\x00\x00\x00'
        return self.api(request)

    def GetTemperature(self, id1, id2, id3, id4):
        request = b'\x0c\x00\xe6\x01\x14\x00\x00\x00' + \
                  struct.pack('B', id1) + \
                  struct.pack('B', id2) + \
                  struct.pack('B', id3) + \
                  struct.pack('B', id4)
        return self.api(request)

    def SetTransceiverMode(self,
                           path, 
                           line_fec, 
                           pilot_symbol_separation, 
                           line_shaping,
                           line_modulation,
                           bcd_mode,
                           ltx_osr,
                           lrx_osr,
                           reference_clock,
                           signal_type,
                           line_mapping,
                           host_modulation):
        request = b'\x20\x00\x00\x01\x04\x00\x00\x00' + \
                  struct.pack('B', path) + \
                  struct.pack('B', line_fec) + \
                  struct.pack('B', pilot_symbol_separation) + \
                  struct.pack('B', line_shaping) + \
                  struct.pack('B', line_modulation) + \
                  struct.pack('<I', bcd_mode) + \
                  struct.pack('B', ltx_osr) + \
                  struct.pack('B', lrx_osr) + \
                  struct.pack('<I', reference_clock) + \
                  struct.pack('<I', signal_type) + \
                  struct.pack('<I', line_mapping) + \
                  struct.pack('B', host_modulation)
        return self.api(request)

    def GetTransceiverMode(self):
        request = b'\x08\x00\x01\x01\x18\x00\x00\x00'
        return self.api(request)

    def get_transceiver_mode(self):
        response = self.GetTransceiverMode()
        rsp = {}
        rsp['line_fec'] = struct.unpack('B', response[0x4:0x5])[0]
        rsp['pilot_symbol_separation'] = struct.unpack('B', response[0x5:0x6])[0]
        rsp['line_shaping'] = struct.unpack('B', response[0x6:0x7])[0]
        rsp['line_modulation'] = struct.unpack('B', response[0x7:0x8])[0]
        rsp['bcd_mode'] = struct.unpack('<I', response[0x8:0xc])[0]
        rsp['ltx_osr'] = struct.unpack('B', response[0xc:0xd])[0]
        rsp['lrx_osr'] = struct.unpack('B', response[0xd:0xe])[0]
        rsp['signal_type'] = struct.unpack('<I', response[0xe:0x12])[0]
        rsp['line_mapping'] = struct.unpack('<I', response[0x12:0x16])[0]
        rsp['host_modulation'] = struct.unpack('B', response[0x16:0x17])[0]
        return rsp

    def SetLineEgressHighSrPulseShaping(self, lane,
                                              roll_off_factor,
                                              pulse_shaping_filter):
        request = b'\x0c\x00\x22\x01\x04\x00\x00\x00' + \
                  struct.pack('B', lane) + \
                  struct.pack('B', roll_off_factor) + \
                  struct.pack('B', pulse_shaping_filter) + b'\x00'
        return self.api(request)

    def GetLineEgressHighSrPulseShaping(self, lane):
        request = b'\x0c\x00\x23\x01\x08\x00\x00\x00' + \
                  struct.pack('B', lane) + b'\x00\x00\x00'
        return self.api(request)

    def get_line_egress_high_sr_pulse_shaping(self, lane):
        response = self.GetLineEgressHighSrPulseShaping(lane)
        rsp = {}
        rsp['roll_off_factor'] = struct.unpack('B', response[0x4:0x5])[0]
        rsp['pulse_shaping_filter'] = struct.unpack('B', response[0x5:0x6])[0]
        return rsp

    def SetLineEgressHighSrLaneAmplitude(self, lane, amplitude):
        request = b'\x0c\x00\x26\x01\x04\x00\x00\x00' + \
                  struct.pack('B', lane) + \
                  struct.pack('<H', amplitude) + b'\x00'
        return self.api(request)

    def GetLineEgressHighSrLaneAmplitude(self, lane):
        request = b'\x0c\x00\x27\x01\x08\x00\x00\x00' + \
                  struct.pack('B', lane) + b'\x00\x00\x00'
        return self.api(request)

    def get_line_egress_high_sr_lane_amplitude(self, lane):
        response = self.GetLineEgressHighSrLaneAmplitude(lane)
        return struct.unpack('<H', response[0x4:0x6])[0] / (2**17)

    def SetLineEgressHighSrLaneSkew(self, lane, skew):
        request = b'\x0c\x00\x1e\x01\x04\x00\x00\x00' + \
                  struct.pack('B', lane) + \
                  struct.pack('<h', skew) + b'\x00'
        return self.api(request)

    def GetLineEgressHighSrLaneSkew(self, lane):
        request = b'\x0c\x00\x1f\x01\x08\x00\x00\x00' + \
                  struct.pack('B', lane) + b'\x00\x00\x00'
        return self.api(request)

    def get_line_egress_high_sr_lane_skew(self, lane):
        response = self.GetLineEgressHighSrLaneSkew(lane)
        return struct.unpack('<h', response[4:6])[0] / (64*3)

    def SetLineEgressLowSrLaneSkew(self, lane, skew):
        request = b'\x10\x00\x20\x01\x04\x00\x00\x00' + \
                  struct.pack('B', lane) + \
                  struct.pack('<H', skew) + b'\x00'*5
        return self.api(request)

    def GetLineEgressLowSrLaneSkew(self, lane):
        request = b'\x0c\x00\x21\x01\x08\x00\x00\x00' + \
                  struct.pack('B', lane) + b'\x00\x00\x00'
        return self.api(request)

    def get_line_egress_low_sr_lane_skew(self, lane):
        response = self.GetLineEgressLowSrLaneSkew(lane)
        return struct.unpack('<h', response[4:6])[0] / (2**9)

    def SetLineEgressLowSrLaneAttenuation(self, lane, attenuation):
        request = b'\x0c\x00\x28\x01\x04\x00\x00\x00' + \
                  struct.pack('B', lane) + \
                  struct.pack('<H', attenuation) + b'\x00'*1
        return self.api(request)

    def GetLineEgressLowSrLaneAttenuation(self, lane):
        request = b'\x0c\x00\x29\x01\x08\x00\x00\x00' + \
                  struct.pack('B', lane) + b'\x00\x00\x00'
        return self.api(request)

    def get_line_egress_low_sr_lane_attenuation(self, lane):
        response = self.GetLineEgressLowSrLaneAttenuation(lane)
        return struct.unpack('<H', response[4:6])[0]

    def SetLineEgressLowSrFilterCoefficients(self, lane, coefs):
        request = b'\x18\x00\x1c\x01\x04\x00\x00\x00' + \
                  struct.pack('B', lane) + \
                  struct.pack('<7h', *coefs) + b'\x00'
        return self.api(request)

    def GetLineEgressLowSrFilterCoefficients(self, lane):
        request = b'\x0c\x00\x1d\x01\x14\x00\x00\x00' + \
                  struct.pack('B', lane) + b'\x00\x00\x00'
        return self.api(request)

    def S92DeCal(self, val):
        if val >= 512:
            return 0
        if val >= 256:
            return (val - 512) / 128
        else:
            return val / 128

    def get_LineEgressLowSrFilterCoefficients(self, lane):
        response = self.GetLineEgressHighSrLaneSkew(lane)
        rsp = {}
        rsp['coef0'] = self.S92DeCal(struct.unpack('<H', response[4:6])[0])
        rsp['coef1'] = self.S92DeCal(struct.unpack('<H', response[6:8])[0])
        rsp['coef2'] = self.S92DeCal(struct.unpack('<H', response[8:10])[0])
        rsp['coef3'] = self.S92DeCal(struct.unpack('<H', response[10:12])[0])
        rsp['coef4'] = self.S92DeCal(struct.unpack('<H', response[12:14])[0])
        rsp['coef5'] = self.S92DeCal(struct.unpack('<H', response[14:16])[0])
        rsp['coef6'] = self.S92DeCal(struct.unpack('<H', response[16:18])[0])
        return rsp

    def SetLineEgressHighSrPreEmphasis(self, lane, coefficients, enable):
        request = b'\x48\x00\x24\x01\x04\x00\x00\x00' + \
                  struct.pack('B', lane) + \
                  struct.pack('%sb'%len(coefficients), *coefficients) + \
                  struct.pack('B', enable) + b'\x00\x00'
        return self.api(request)

    def ControlTask(self, bRoutineSelect, bAction):
            request = b'\x10\x00\x02\x00\x08\x00\x00\x00' + \
                    struct.pack('B', bRoutineSelect) + \
                    struct.pack('B', bAction) + b'\x00\x00\00\00\00\00'
            return self.api(request)

    def GetLineEgressHighSrPreEmphasis(self, lane):
        request = b'\x0c\x00\x25\x01\x44\x00\x00\x00' + \
                  struct.pack('B', lane) + b'\x00\x00\x00'
        return self.api(request)

    def get_line_egress_high_sr_preemphasis(self, lane):
        response = self.GetLineEgressHighSrPreEmphasis(lane)
        rsp = {}
        rsp['coefficients'] = struct.unpack('60b', response[4:64])
        rsp['enable'] = struct.unpack('B', response[64:65])[0]
        return rsp

    def SetLineIngressSkew(self, polarization, skew_phase_i):
        request = b'\x0c\x00\x2e\x01\x04\x00\x00\x00' + \
                  struct.pack('B', polarization) + \
                  struct.pack('<h', skew_phase_i) + b'\x00'
        return self.api(request)

    def GetLineIngressSkew(self, polarization):
        request = b'\x0c\x00\x2f\x01\x08\x00\x00\x00' + \
                  struct.pack('B', polarization) + b'\x00\x00\x00'
        return self.api(request)

    def get_line_ingress_skew(self, polarization):
        response = self.GetLineIngressSkew(polarization)
        return struct.unpack('<h', response[4:6])[0]

    def SetLineIngressAgcConfig(self, lane, signal_reference, signal_gain, signal_max, signal_min, enable):
        request = b'\x14\x00\x3c\x01\x04\x00\x00\x00' + \
                  struct.pack('B', lane) + \
                  struct.pack('B', int(signal_reference*2**7)) + \
                  struct.pack('<H', int(signal_gain*2**8)) + \
                  struct.pack('<H', int(signal_max*2**5)) + \
                  struct.pack('<H', int(signal_min*2**5)) + \
                  struct.pack('B', enable) + b'\x00'*3
        return self.api(request)

    def GetLineIngressAgcConfig(self, lane):
        request = b'\x0c\x00\x3d\x01\x0c\x00\x00\x00' + \
                  struct.pack('B', lane) + b'\x00\x00\x00'
        return self.api(request)

    def get_line_ingress_agc_config(self, lane):
        response = self.GetLineIngressAgcConfig(lane)
        print(response)
        rsp = {}
        rsp['signal_reference'] = struct.unpack('B', response[4:5])[0]/2**7
        rsp['signal_gain'] = struct.unpack('<H', response[5:7])[0]/2**8
        rsp['signal_max'] = struct.unpack('<H', response[7:9])[0]/2**5
        rsp['signal_min'] = struct.unpack('<H', response[9:11])[0]/2**5
        rsp['enable'] = struct.unpack('B', response[11:12])[0]
        return rsp

    def SetHostIngressLanePolarity(self, polarity):
        request = b'\x0c\x00\x10\x01\x04\x00\x00\x00' + \
                  struct.pack('b', polarity) + b'\x00\x00\x00'
        return self.api(request)

    def GetHostIngressLanePolarity(self):
        request = b'\x08\x00\x11\x01\x08\x00\x00\x00'
        return self.api(request)

    def get_HostIngressLanePolarity(self):
        response = self.GetHostIngressLanePolarity()
        return struct.unpack('B', response[0x4:0x5])[0]

    def SetHostEgressLanePolarity(self, polarity):
        request = b'\x0c\x00\x0C\x01\x04\x00\x00\x00' + \
                  struct.pack('B', polarity) + b'\x00\x00\x00'
        return self.api(request)

    def GetHostEgressLanePolarity(self):
        request = b'\x08\x00\x0d\x01\x08\x00\x00\x00'
        return self.api(request)

    def get_HostEgressLanePolarity(self):
        response = self.GetHostEgressLanePolarity()
        return struct.unpack('B', response[0x4:0x5])[0]

    def SetHostIngressLaneMute(self, dual, mute):
        request = b'\x0c\x00\x14\x01\x04\x00\x00\x00' + \
                  struct.pack('B', dual) + \
                  struct.pack('B', mute) + b'\x00\x00'
        return self.api(request)

    def GetHostIngressLaneMute(self, dual):
        request = b'\x0c\x00\x15\x01\x08\x00\x00\x00' + \
                  struct.pack('B', dual) + b'\x00\x00\x00'
        return self.api(request)

    def get_HostIngressLaneMute(self, dual):
        response = self.GetHostIngressLaneMute(dual)
        return struct.unpack('B', response[0x4:0x5])[0]
    
    def SetHostIngressFilterCoefficients(self, lane, coefficients, low_eye, high_eye):
        request = b'\x14\x00\x12\x01\x04\x00\x00\x00' + \
                  struct.pack('B', lane) + \
                  struct.pack('<3h', *coefficients) + \
                  struct.pack('<H', low_eye) + \
                  struct.pack('<H', high_eye) + b'\x00'
        return self.api(request)
    
    def GetHostIngressFilterCoefficients(self, lane):
        request = b'\x0c\x00\x13\x01\x10\x00\x00\x00' + \
                  struct.pack('B', lane) + b'\x00\x00\x00'
        return self.api(request)

    def get_HostIngressFilterCoefficients(self, lane):
        response = self.GetHostIngressFilterCoefficients(lane)
        rsp = {}
        rsp['coefficients'] = struct.unpack('<3h', response[0x4:0xa])
        rsp['low_eye'] = struct.unpack('<H', response[0xa:0xc])[0]
        rsp['high_eye'] = struct.unpack('<H', response[0xc:0xe])[0]
        return rsp

    def Echo(self, data):
        request = struct.pack('<H', len(data) + 8) + \
                  b'\x01\x00' + \
                  struct.pack('<H', len(data) + 4) + \
                  b'\x00\x00' + \
                  data
        return self.api(request)

    def GetChipId(self):
        request = b'\x08\x00\xe5\x01\x08\x00\x00\x00'
        return self.api(request)

    def get_chip_id(self):
        response = self.GetChipId()
        rsp = {}
        rsp['chip_id'] = hex(struct.unpack('B', response[0x4:0x5])[0])
        return rsp

    def ReadFirmwareInformation(self):
        request = b'\x08\x00\xe1\x01\x2c\x00\x00\x00'
        return self.api(request)

    def read_firmware_information(self):
        response = self.ReadFirmwareInformation()
        rsp = {}
        rsp['dFirmwareVersion'] = hex(struct.unpack('<I', response[0x4:0x8])[0])
        rsp['aGitHash'] = response[0x8:0x14]
        rsp['aCpiosGitHash'] = response[0x14:0x20]
        rsp['aRm'] = hex(struct.unpack('<I', response[0x20:0x24])[0])
        return rsp

    def SetHostUnframedTestPatternGeneratorConfig(self, dual, prbs_type_1, prbs_tye_2, enable):
        request = b'\x0c\x00\x6d\x01\x04\x00\x00\x00' + \
                  struct.pack('B', dual) + \
                  struct.pack('B', prbs_type_1) + \
                  struct.pack('B', prbs_tye_2) + \
                  struct.pack('B', enable)
        return self.api(request)
    
    def GetHostUnframedTestPatternGeneratorConfig(self, dual):
        request = b'\x0c\x00\x6e\x01\x08\x00\x00\x00' + \
                  struct.pack('B', dual) + b'\x00\x00\x00'
        return self.api(request)

    def SetHostUnframedTestPatternCheckerConfig(self, dual, prbs_type_1, prbs_tye_2, enable):
        request = b'\x0c\x00\x6f\x01\x04\x00\x00\x00' + \
                  struct.pack('B', dual) + \
                  struct.pack('B', prbs_type_1) + \
                  struct.pack('B', prbs_tye_2) + \
                  struct.pack('B', enable)
        return self.api(request)
    
    def GetHostUnframedTestPatternCheckerConfig(self, dual):
        request = b'\x0c\x00\x70\x01\x08\x00\x00\x00' + \
                  struct.pack('B', dual) + b'\x00\x00\x00'
        return self.api(request)

    def GetHostUnframedTestPatternCheckerStatistics(self, lane):
        request = b'\x0c\x00\x75\x01\x14\x00\x00\x00' + \
                  struct.pack('B', lane) + \
                  b'\x00\x00\00'
        return self.api(request)

    def get_hostunframedtestpatterncheckerstatistics(self, lane):
        response = self.GetHostUnframedTestPatternCheckerStatistics(lane)
        rsp = {}
        rsp['accum_prbs_bit_count'] = struct.unpack('<Q', response[0x4:0xc])[0]
        rsp['accum_prbs_error_count'] = struct.unpack('<I', response[0xc:0x10])[0]
        rsp['sync'] = struct.unpack('B', response[0x10:0x11])[0]
        rsp['saturate'] = struct.unpack('B', response[0x11:0x12])[0]
        return rsp

    def TriggerMonitors(self):
        request = b'\x08\x00\x6c\x01\x04\x00\x00\x00'
        return self.api(request)
    
    def SetPerformanceMonitorTriggerSource(self, trigger_source):
        request = b'\x0c\x00\x6a\x01\x04\x00\x00\x00' + struct.pack('B', trigger_source) + b'\x00\x00\x00'
        return self.api(request)

    def GetPerformanceMonitorTriggerSource(self):
        request = b'\x08\x00\x6b\x01\x08\x00\x00\x00'
        return self.api(request)

    def GetLineIngressDspStatus(self):
        request = b'\x08\x00\x3f\x01\x1c\x00\x00\x00'
        return self.api(request)

    def get_line_ingress_status(self):
        response = self.GetLineIngressDspStatus()
        rsp = {}
        rsp['amplitude_hi'] = struct.unpack('<H', response[4:6])[0] / (2**15)
        rsp['amplitude_hq'] = struct.unpack('<H', response[6:8])[0] / (2**15)
        rsp['amplitude_vi'] = struct.unpack('<H', response[8:10])[0] / (2**15)
        rsp['amplitude_vq'] = struct.unpack('<H', response[10:12])[0] / (2**15)
        rsp['mse_hi'] = 10*math.log10(struct.unpack('<H',
                                             response[12:14])[0] / (2**11))
        rsp['mse_hq'] = 10*math.log10(struct.unpack('<H',
                                             response[14:16])[0] / (2**11))
        rsp['mse_vi'] = 10*math.log10(struct.unpack('<H',
                                             response[16:18])[0] / (2**11))
        rsp['mse_vq'] = 10*math.log10(struct.unpack('<H',
                                             response[18:20])[0] / (2**11))
        rsp['cg_h'] = struct.unpack('b', response[20:21])[0]
        rsp['cg_v'] = struct.unpack('b', response[21:22])[0]
        rsp['evm_h'] = struct.unpack('<H', response[22:24])[0]
        rsp['evm_v'] = struct.unpack('<H', response[24:26])[0]
        return rsp 

    def get_line_ingress_status1(self):
        response = self.GetLineIngressDspStatus()
        rsp = {}
        rsp['amplitude_hi'] = struct.unpack('<H', response[4:6])[0] / (2**15)
        rsp['amplitude_hq'] = struct.unpack('<H', response[6:8])[0] / (2**15)
        rsp['amplitude_vi'] = struct.unpack('<H', response[8:10])[0] / (2**15)
        rsp['amplitude_vq'] = struct.unpack('<H', response[10:12])[0] / (2**15)

        rsp['mse_hi'] = struct.unpack('<H',response[12:14])[0] / (2**11)
        rsp['mse_hq'] = struct.unpack('<H',
                                            response[14:16])[0] / (2**11)
        rsp['mse_vi'] = struct.unpack('<H',
                                            response[16:18])[0] / (2**11)
        rsp['mse_vq'] = struct.unpack('<H',response[18:20])[0] / (2**11)
        # if( (struct.unpack('<H',response[12:14])[0]) != 0)
        #    && (struct.unpack('<H',response[14:16])[0]) != 0)
        #    && (struct.unpack('<H',response[16:18])[0]) != 0)
        #    && (struct.unpack('<H',response[18:20])[0]) != 0)){
        #     rsp['mse_hi'] = 10*math.log10(struct.unpack('<H',
        #                                         response[12:14])[0] / (2**11))
        #     rsp['mse_hq'] = 10*math.log10(struct.unpack('<H',
        #                                         response[14:16])[0] / (2**11))
        #     rsp['mse_vi'] = 10*math.log10(struct.unpack('<H',
        #                                         response[16:18])[0] / (2**11))
        #     rsp['mse_vq'] = 10*math.log10(struct.unpack('<H',
        #                                      response[18:20])[0] / (2**11))

             
        # }
        # else{
        #     rsp['mse_hi'] = 0
        #     rsp['mse_hq'] = 0
        #     rsp['mse_vi'] = 0
        #     rsp['mse_vq'] = 0
        # }

        rsp['cg_h'] = struct.unpack('b', response[20:21])[0]
        rsp['cg_v'] = struct.unpack('b', response[21:22])[0]
        rsp['evm_h'] = struct.unpack('<H', response[22:24])[0]
        rsp['evm_v'] = struct.unpack('<H', response[24:26])[0]
        return rsp

    def get_ism_status(self):
        regv = self.read_register(0x800002d0)
        return self.read_register(regv | 0x10000000)

    def ber(self):
        ch1 = self.get_error_correction_statistics(0, 1)
        ch2 = self.get_error_correction_statistics(2, 1)
        rsp = {}
        rsp['pre-fec-ber'] = (ch1['accum_corrected_error_count'] + 
                ch2['accum_corrected_error_count']) / (ch1['accum_bit_count'] + 
                ch2['accum_bit_count'])
        rsp['post-fec-cwc'] = (ch1['accum_uncorrected_codeword_count'] +
                ch2['accum_uncorrected_codeword_count'])
        return rsp

    def PRBS_ber(self, lane):
        data_lane = self.get_hostunframedtestpatterncheckerstatistics(lane)
        rsp = {}
        rsp['PRBS_bit_error'] = data_lane['accum_prbs_error_count'] / data_lane['accum_prbs_bit_count']
        rsp['PRBS_Sync.'] = data_lane['sync']
        rsp['PRBS_Saturate'] = data_lane['saturate']
        return rsp

    def PreFECber(self, direction):
        self.TriggerMonitors()
        time.sleep(1)
        ch1 = self.get_error_correction_statistics(0, direction)
        ch2 = self.get_error_correction_statistics(2, direction)
        rsp = {}
        rsp['pre-fec-ber'] = (ch1['accum_corrected_error_count'] + 
                ch2['accum_corrected_error_count']) / (ch1['accum_bit_count'] + 
                ch2['accum_bit_count'])
        rsp['post-fec-cwc'] = (ch1['accum_uncorrected_codeword_count'] +
                ch2['accum_uncorrected_codeword_count'])
        return rsp

    def ReStartLineIngressDsp(self, action):
        request = b'\x0c\x00\xf5\x01\x04\x00\x00\x00' + \
                  struct.pack('B', action) + b'\x00'*3
        return self.api(request)

    def SetCoreCfecTestPatternGeneratorConfig(self, signalType, enable):
        request = b'\x0c\x00\x89\x01\x04\x00\x00\x00' + \
                    struct.pack('B', signalType) + \
                    struct.pack('B', enable) + \
                    b'\x00\x00'
        return self.api(request)

    def SetCoreCfecTestPatternCheckerConfig(self, signalType, enable):
        request = b'\x0C\x00\x8b\x01\x04\x00\x00\x00' + \
                    struct.pack('B', signalType) + \
                    struct.pack('B', enable) + \
                    b'\x00\x00'
        return self.api(request)

    def GetCoreCfecTestPatternCheckerConfig(self):
        request = b'\x08\x00\x8c\x01\x08\x00\x00\x00'
        return self.api(request)

    def GetCoreCfecTestPatternGeneratorConfig(self):
        request = b'\x08\x00\x8a\x01\x08\x00\x00\x00'
        return self.api(request)

    def GetCoreCfecTestPatternCheckerCounters(self):
        request = b'\x08\x00\x12\x02\x18\x00\x00\x00'
        return self.api(request)

    def get_core_cfec_test_pattern_checker_counters(self):
        response = self.GetCoreCfecTestPatternCheckerCounters()
        rsp = {}
        rsp['bit_count'] = struct.unpack('<Q', response[4:0xc])[0]
        rsp['err_count'] = struct.unpack('<Q', response[0xc:0x14])[0]
        rsp['resync_count'] = struct.unpack('<I', response[0x14:0x18])[0]
        return rsp

    def TriggerMonitors(self):
        request = b'\x08\x00\x6c\x01\x04\x00\x00\x00'
        return self.api(request)    

    def get_faw_error_statistics(self):
        response = self.GetFawErrorStatistics()
        rsp = {}
        rsp['accum_fas_bit_count'] = struct.unpack('<Q', response[4:0xc])[0]
        rsp['accum_fas_err_count'] = struct.unpack('<Q', response[0xc:0x14])[0]
        rsp['faw_ber'] = struct.unpack('<Q', response[0xc:0x14])[0] / struct.unpack('<Q', response[4:0xc])[0]
        return rsp

    def SetPcsTestPatternGeneratorConfig(self, channel, direction, signalType, en):
        request = b'\x0c\x00\x7f\x01\x04\x00\x00\x00' + \
                  struct.pack('B', channel) + \
                  struct.pack('B', direction) + \
                  struct.pack('B', signalType) + \
                  struct.pack('B', en)
        return self.api(request)
    
    def GetPcsTestPatternGeneratorConfig(self, channel, direction):
        request = b'\x0c\x00\x80\x01\x08\x00\x00\x00' + \
                  struct.pack('B', channel) + \
                  struct.pack('B', direction) + \
                  b'\x00\x00'
        return self.api(request)

    def SetPcsTestPatternCheckerConfig(self, channel, direction, signalType, en):
        request = b'\x0c\x00\x81\x01\x04\x00\x00\x00' + \
                  struct.pack('B', channel) + \
                  struct.pack('B', direction) + \
                  struct.pack('B', signalType) + \
                  struct.pack('B', en)
        return self.api(request)

    def GetPcsTestPatternCheckerConfig(self, channel, direction):
        request = b'\x0c\x00\x82\x01\x08\x00\x00\x00' + \
                  struct.pack('B', channel) + \
                  struct.pack('B', direction) + \
                  b'\x00\x00'
        return self.api(request)

    def GetPcsTestPatternCheckerStatistics(self, channel, direction):
        request = b'\x0c\x00\x83\x01\x44\x00\x00\x00' + \
                  struct.pack('B', channel) + \
                  struct.pack('B', direction) + \
                  b'\x00\x00'
        return self.api(request)

    def get_pcs_test_pattern_checker_statistics(self, channel, direction):
        response = self.GetPcsTestPatternCheckerStatistics(channel, direction)
        rsp = {}
        rsp['accum_bit_count'] = struct.unpack('<Q', response[4:0xc])[0]
        rsp['accum_err_count'] = struct.unpack('<Q', response[0xc:0x14])[0]
        if rsp['accum_bit_count'] > 0:
            rsp['ber'] = struct.unpack('<Q', response[0xc:0x14])[0] / struct.unpack('<Q', response[4:0xc])[0]
        return rsp

    def ReadLinePowerSupply(self, lane):#lane 0,1,2,3 HI HQ VI VQ
        request = b'\x0c\x00\xf9\x00\xbc\x00\x00\x00' + \
                  struct.pack('B', lane) + \
                  b'\x00\x00\x00'
        return self.api(request)    

    def read_line_power_supply(self, lane):
        response = self.ReadLinePowerSupply(lane)
        # rsp = {}
        for i in range(0,6,1):
            print('rx_vdda%d' % i)
            cal(struct.unpack('<H', response[4+2*i:6+2*i])[0], 'u', 16, 16)

        for i in range(0,20,1):
            print('rx_vssa%d' % i)
            cal(struct.unpack('<H', response[0x10+2*i:0x12+2*i])[0], 'u', 16, 16)

        print('tx_vdda_h')
        cal(struct.unpack('<H', response[0x84:0x86])[0], 'u', 16, 16)
      
        print('tx_vddd_h')
        cal(struct.unpack('<H', response[0x86:0x88])[0], 'u', 16, 16)  

        print('tx_vdda_v')
        cal(struct.unpack('<H', response[0x88:0x8a])[0], 'u', 16, 16) 

        print('tx_vddd_v')
        cal(struct.unpack('<H', response[0x8a:0x8c])[0], 'u', 16, 16)
          
        # rsp['rx_vdda0'] = cal(val, 'u', 16, 16)
        # return rsp

    def get_ReadLinePowerSupply(self, lane):#huabin
        response = self.ReadLinePowerSupply(lane)
        rsp = {}
        rsp['rx_vdda'] = struct.unpack('<6H', response[0x4:0x10])
        rsp['rx_vssa'] = struct.unpack('<10H', response[0x10:0x24])
        rsp['rx_net1'] = struct.unpack('<12H', response[0x24:0x3c])       
        rsp['rx_net2'] = struct.unpack('<12H', response[0x3c:0x54])       
        rsp['rx_net3'] = struct.unpack('<12H', response[0x54:0x6c])       
        rsp['rx_net4'] = struct.unpack('<12H', response[0x6c:0x84])                
        rsp['tx_vdda_h'] = struct.unpack('<H', response[0x84:0x86])[0]        
        rsp['tx_vddd_h'] = struct.unpack('<H', response[0x86:0x88])[0]        
        rsp['tx_vdda_v'] = struct.unpack('<H', response[0x88:0x8a])[0]        
        rsp['tx_vddd_v'] = struct.unpack('<H', response[0x8a:0x8c])[0]        
        rsp['tx_net1'] = struct.unpack('<12H', response[0x8c:0xa4])        
        rsp['tx_net2'] = struct.unpack('<12H', response[0xa4:0xbc])        
        return rsp 

    # def get_ReadLinePowerSupply(self, lane):#hao
    #     response = self.ReadLinePowerSupply(lane)
    #     rsp = {}
    #     rsp['rx_vdda'] = struct.unpack('<6H', response[0x4:0x10])[0]  
    #     rsp['rx_vssa'] = struct.unpack('<10H', response[0x10:0x24])[0]  
    #     rsp['rx_net1'] = struct.unpack('<12H', response[0x24:0x3c])[0]       
    #     rsp['rx_net2'] = struct.unpack('<12H', response[0x3c:0x54])[0]         
    #     rsp['rx_net3'] = struct.unpack('<12H', response[0x54:0x6c])[0]         
    #     rsp['rx_net4'] = struct.unpack('<12H', response[0x6c:0x84])[0]                  
    #     rsp['tx_vdda_h'] = struct.unpack('<H', response[0x84:0x86])[0]        
    #     rsp['tx_vddd_h'] = struct.unpack('<H', response[0x86:0x88])[0]        
    #     rsp['tx_vdda_v'] = struct.unpack('<H', response[0x88:0x8a])[0]        
    #     rsp['tx_vddd_v'] = struct.unpack('<H', response[0x8a:0x8c])[0]        
    #     rsp['tx_net1'] = struct.unpack('<12H', response[0x8c:0xa4])        
    #     rsp['tx_net2'] = struct.unpack('<12H', response[0xa4:0xbc])        
    #     return rsp 

    def GetTemperature(self, sensor_id_0, sensor_id_1, sensor_id_2, sensor_id_3):
        request = b'\x0c\x00\xe6\x01\x14\x00\x00\x00' + \
                struct.pack('B', sensor_id_0) + \
                struct.pack('B', sensor_id_1) + \
                struct.pack('B', sensor_id_2) + \
                struct.pack('B', sensor_id_3)
        return self.api(request)

    # def get_GetTemperature(self, sensor_id_0, sensor_id_1, sensor_id_2, sensor_id_3):#huabin
    #     response = self.GetTemperature(sensor_id_0, sensor_id_1, sensor_id_2, sensor_id_3)
    #     rsp = {}
    #     rsp['temperature_id_0'] = struct.unpack('<i', response[0x4:0x8])[0]
    #     rsp['temperature_id_1'] = struct.unpack('<i', response[0x8:0xc])[0]
    #     rsp['temperature_id_2'] = struct.unpack('<i', response[0xc:0x10])[0]
    #     rsp['temperature_id_3'] = struct.unpack('<i', response[0x10:0x14])[0]
    #     return rsp 

    def get_GetTemperature(self, sensor_id_0, sensor_id_1, sensor_id_2, sensor_id_3):#hao
        response = self.GetTemperature(sensor_id_0, sensor_id_1, sensor_id_2, sensor_id_3)
        rsp = {}
        rsp['temperature_id_0'] = struct.unpack('<I', response[0x4:0x8])[0]
        rsp['temperature_id_1'] = struct.unpack('<I', response[0x8:0xc])[0]
        rsp['temperature_id_2'] = struct.unpack('<I', response[0xc:0x10])[0]
        rsp['temperature_id_3'] = struct.unpack('<I', response[0x10:0x14])[0]
        return rsp 
