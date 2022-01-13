from .broker import Broker
import time
import struct
from .ddm import DDM
from .fpn import cal as fpnCal
from .cdb import CDB

class CMIS:

    def __init__(self, broker):
        self._b = broker
    @property
    def checksum00h(self):
        self._b.twi_sbw(126, b'\x00\x00')#switch page
        time.sleep(0.05)        
        checksum = 0
        for addr in range( 128, 222 ):
            data = self._b.twi_rr(addr)
            checksum += data
        checksum &= 0xff
        print( "calculated checksum {:#x}".format( checksum ) )
        addr = 222
        data = self._b.twi_rr(addr)
        print( "programmed checksum {:#x}".format( data ) )
        return data

    @property
    def checksum01h(self):
        self._b.twi_sbw(126, b'\x00\x01')#switch page
        time.sleep(0.05)        
        checksum = 0
        for addr in range( 130, 255 ):
            data = self._b.twi_rr(addr)
            checksum += data
        checksum &= 0xff
        print( "calculated checksum {:#x}".format( checksum ) )
        addr = 255
        data = self._b.twi_rr(addr)
        print( "programmed checksum {:#x}".format( data ) )
        return data

    @property
    def checksum02h(self):
        self._b.twi_sbw(126, b'\x00\x02')#switch page
        time.sleep(0.05)        
        checksum = 0
        for addr in range( 128, 255 ):
            data = self._b.twi_rr(addr)
            checksum += data
        checksum &= 0xff
        print( "calculated checksum {:#x}".format( checksum ) )
        addr = 255
        data = self._b.twi_rr(addr)
        print( "programmed checksum {:#x}".format( data ) )
        return data

    @property
    def force_lpwr(self):
        return (self._b.twi_rr(26) >> 4) & 0x01
    @force_lpwr.setter
    def force_lpwr(self, val):
        temp = self._b.twi_rr(26)
        temp &= ~(1 << 4)#clear bit 4
        temp |= 1 << 4
        self._b.twi_bw(26,temp)

    @property
    def mod_ddm(self):
        rsp = self._b.twi_srr(14, 4)
        response = {}
        response['Case Temp'] = struct.unpack('>h', rsp[0:2])[0] / 256.0
        response['Mod Vcc'] = struct.unpack('>H', rsp[2:])[0] / 10000.0
        time.sleep(0.05)
        rsp = self._b.twi_srr(20, 2)
        response['Laser Temp'] = struct.unpack('>h', rsp[0:2])[0] / 256.0

        rsp = self._b.twi_srr(24, 2)
        response['DSP Temp'] = struct.unpack('>h', rsp[0:2])[0] / 256.0
        return response

    @property
    def active_fw_ver(self):
        rsp = self._b.twi_srr(39, 2)
        response = {}
        response['Major Ver'] = rsp[0]
        response['Minor Ver'] = rsp[1]
        return response

    @property
    def low_ch_100(self):
        self._b.twi_sbw(126, b'\x00\x04')#switch page
        time.sleep(0.05)
        return struct.unpack('>h', self._b.twi_srr(150,2))[0]

    @property
    def high_ch_100(self):
        self._b.twi_sbw(126, b'\x00\x04')#switch page
        time.sleep(0.05)
        return struct.unpack('>h', self._b.twi_srr(152,2))[0]

    @property
    def low_ch_75(self):
        self._b.twi_sbw(126, b'\x00\x04')#switch page
        time.sleep(0.05)
        return struct.unpack('>h', self._b.twi_srr(158,2))[0]

    @property
    def high_ch_75(self):
        self._b.twi_sbw(126, b'\x00\x04')#switch page
        time.sleep(0.05)
        return struct.unpack('>h', self._b.twi_srr(160,2))[0]

    @property
    def low_fine_range(self):
        self._b.twi_sbw(126, b'\x00\x04')#switch page
        time.sleep(0.05)
        return struct.unpack('>h', self._b.twi_srr(192,2))[0]

    @property
    def high_fine_range(self):
        self._b.twi_sbw(126, b'\x00\x04')#switch page
        time.sleep(0.05)
        return struct.unpack('>h', self._b.twi_srr(194,2))[0]


    @property
    def grid_sel(self):
        self._b.twi_sbw(126, b'\x00\x12')#switch page
        time.sleep(0.05)
        return self._b.twi_rr(128) >> 4

    @grid_sel.setter
    def grid_sel(self,val):
        self._b.twi_sbw(126, b'\x00\x12')#switch page
        time.sleep(0.05)
        raw = self._b.twi_rr(128)
        self._b.twi_bw(128, (val << 4) | (raw & 0x0f))

    @property
    def fine_tune_en(self):
        self._b.twi_sbw(126, b'\x00\x12')#switch page
        time.sleep(0.05)
        return self._b.twi_rr(128) & 0x01

    @fine_tune_en.setter
    def fine_tune_en(self,val):
        self._b.twi_sbw(126, b'\x00\x12')#switch page
        time.sleep(0.05)
        raw = self._b.twi_rr(128)
        self._b.twi_bw(128, (val & 0x01) | (raw & 0xfe))

    @property
    def fine_offset(self):
        self._b.twi_sbw(126, b'\x00\x12')#switch page
        time.sleep(0.05)
        return struct.unpack('>h', self._b.twi_srr(152,2))[0]

    @fine_offset.setter
    def fine_offset(self,val):
        self._b.twi_sbw(126, b'\x00\x12')#switch page
        time.sleep(0.05)
        self._b.twi_sbw(152, struct.pack('>h',val))

    @property
    def cmis_ch(self):
        self._b.twi_sbw(126, b'\x00\x12')#switch page
        time.sleep(0.05)
        return struct.unpack('>h', self._b.twi_srr(136,2))[0]

    @cmis_ch.setter
    def cmis_ch(self,val):
        self._b.twi_sbw(126, b'\x00\x12')#switch page
        time.sleep(0.05)
        self._b.twi_sbw(136, struct.pack('>h',val))

    @property
    def cur_freq(self):
        self._b.twi_sbw(126, b'\x00\x12')#switch page
        time.sleep(0.05)
        rsp = self._b.twi_srr(168,4)
        THz = struct.unpack('>H', rsp[0:2])[0]
        GHz = struct.unpack('>H', rsp[2:])[0]
        # print('%d.%d\n' % (THz, GHz/20))
        if self._b.twi_rr(1) == 0x40:
            val = THz + (GHz / 20.0) / 1000.0
        else:
            val = struct.unpack('>I', rsp[0:4])[0] / 1000.0 / 1000.0
        return val

    @property
    def tune_sta(self):
        self._b.twi_sbw(126, b'\x00\x12')#switch page
        time.sleep(0.05)
        return self._b.twi_rr(222)

    @property
    def laser_latched_sta(self):
        self._b.twi_sbw(126, b'\x00\x12')#switch page
        time.sleep(0.05)
        return self._b.twi_srr(230,2)

    @property
    def tune_sum(self):
        self._b.twi_sbw(126, b'\x00\x12')#switch page
        time.sleep(0.05)
        return self._b.twi_rr(230)

    @property
    def tune_latch(self):
        self._b.twi_sbw(126, b'\x00\x12')#switch page
        time.sleep(0.05)
        return self._b.twi_rr(231)

    @property
    def media_gen(self):
        self._b.twi_sbw(126, b'\x00\x13')#switch page
        time.sleep(0.05)
        return self._b.twi_rr(152)

    @media_gen.setter
    def media_gen(self,val):
        self._b.twi_sbw(126, b'\x00\x13')#switch page
        time.sleep(0.05)
        self._b.twi_bw(152, val)

    @property
    def media_chk(self):
        self._b.twi_sbw(126, b'\x00\x13')#switch page
        time.sleep(0.05)
        return self._b.twi_rr(168)

    @media_chk.setter
    def media_chk(self,val):
        self._b.twi_sbw(126, b'\x00\x13')#switch page
        time.sleep(0.05)
        self._b.twi_bw(168, val)


    @property
    def host_gen(self):
        self._b.twi_sbw(126, b'\x00\x13')#switch page
        time.sleep(0.05)
        return self._b.twi_rr(144)

    @host_gen.setter
    def host_gen(self,val):
        self._b.twi_sbw(126, b'\x00\x13')#switch page
        time.sleep(0.05)
        self._b.twi_bw(144, val)

    @property
    def host_chk(self):
        self._b.twi_sbw(126, b'\x00\x13')#switch page
        time.sleep(0.05)
        return self._b.twi_rr(160)

    @host_chk.setter
    def host_chk(self,val):
        self._b.twi_sbw(126, b'\x00\x13')#switch page
        time.sleep(0.05)
        self._b.twi_bw(160, val)


    @property
    def media_out(self):
        self._b.twi_sbw(126, b'\x00\x13')#switch page
        time.sleep(0.05)
        return self._b.twi_rr(180)

    @media_out.setter
    def media_out(self,val):
        self._b.twi_sbw(126, b'\x00\x13')#switch page
        time.sleep(0.05)
        self._b.twi_bw(180, val)

    @property
    def media_in(self):
        self._b.twi_sbw(126, b'\x00\x13')#switch page
        time.sleep(0.05)
        return self._b.twi_rr(181)

    @media_in.setter
    def media_in(self,val):
        self._b.twi_sbw(126, b'\x00\x13')#switch page
        time.sleep(0.05)
        self._b.twi_bw(181, val)

    @property
    def host_out(self):
        self._b.twi_sbw(126, b'\x00\x13')#switch page
        time.sleep(0.05)
        return self._b.twi_rr(182)

    @host_out.setter
    def host_out(self,val):
        self._b.twi_sbw(126, b'\x00\x13')#switch page
        time.sleep(0.05)
        self._b.twi_bw(182, val)

    @property
    def host_in(self):
        self._b.twi_sbw(126, b'\x00\x13')#switch page
        time.sleep(0.05)
        return self._b.twi_rr(183)

    @host_in.setter
    def host_in(self,val):
        self._b.twi_sbw(126, b'\x00\x13')#switch page
        time.sleep(0.05)
        self._b.twi_bw(183, val)

    @property
    def dign_sel(self):
        self._b.twi_sbw(126, b'\x00\x14')#switch page
        time.sleep(0.05)
        return self._b.twi_rr(128)

    @dign_sel.setter
    def dign_sel(self,val):
        self._b.twi_sbw(126, b'\x00\x14')#switch page
        time.sleep(0.05)
        self._b.twi_bw(128, val)


    def dign_info(self):
        self._b.twi_sbw(126, b'\x00\x14')#switch page
        time.sleep(0.05)
        response = self._b.twi_srr(192,8)
        rsp = {}
        rsp['error_count'] = struct.unpack('<Q', response)[0]
        response = self._b.twi_srr(200,8)
        rsp['total_bit_count'] = struct.unpack('<Q', response)[0]
        # if(0 != struct.unpack('<Q', response)[0]):
        #     rsp['ber'] = struct.unpack('<Q', response)[0] / struct.unpack('<Q', response)[0]
        return rsp

    @property
    def rx_output_dis(self):
        self._b.twi_sbw(126, b'\x00\x10')#switch page
        time.sleep(0.05)
        return self._b.twi_rr(138) & 0x01

    @rx_output_dis.setter
    def rx_output_dis(self,val):
        self._b.twi_sbw(126, b'\x00\x10')#switch page
        time.sleep(0.05)
        self._b.twi_bw(138, val)

    @property
    def rx_squelch_dis(self):
        self._b.twi_sbw(126, b'\x00\x10')#switch page
        time.sleep(0.05)
        return self._b.twi_rr(139) & 0x01

    @rx_squelch_dis.setter
    def rx_squelch_dis(self,val):
        self._b.twi_sbw(126, b'\x00\x10')#switch page
        time.sleep(0.05)
        self._b.twi_bw(139, val)

    @property
    def dp_deinit(self):
        self._b.twi_sbw(126, b'\x00\x10')#switch page
        time.sleep(0.05)
        return self._b.twi_rr(128)

    @dp_deinit.setter
    def dp_deinit(self,val):
        self._b.twi_sbw(126, b'\x00\x10')#switch page
        time.sleep(0.05)
        self._b.twi_bw(128, val)

    @property
    def tx_dis(self):
        self._b.twi_sbw(126, b'\x00\x10')#switch page
        time.sleep(0.05)
        return self._b.twi_rr(130)

    @tx_dis.setter
    def tx_dis(self,val):
        self._b.twi_sbw(126, b'\x00\x10')#switch page
        time.sleep(0.05)
        self._b.twi_bw(130, val)

    @property
    def m_state(self):
        return self._b.twi_rr(3) & 0xfe

    @property
    def dp_state(self):
        self._b.twi_sbw(126, b'\x00\x11')#switch page
        time.sleep(0.05)
        return self._b.twi_rr(128) & 0x0f#lane 1 state

    @property
    def rxlos(self):
        self._b.twi_sbw(126, b'\x00\x11')#switch page
        time.sleep(0.05)
        return self._b.twi_rr(147)


    @property
    def vdm_latch_req(self):
        self._b.twi_sbw(126, b'\x00\x2F')#switch page
        time.sleep(0.01)
        return self._b.twi_rr(144) >> 7


    @vdm_latch_req.setter
    def vdm_latch_req(self,val):
        self._b.twi_sbw(126, b'\x00\x2F')#switch page
        time.sleep(0.01)
        self._b.twi_bw(144, (val & 0x01) << 7)


    @property
    def vdm_latch_done(self):
        self._b.twi_sbw(126, b'\x00\x2F')#switch page
        time.sleep(0.01)
        val = self._b.twi_rr(145) >> 7
        print('latch %d.\n' % val)
        return val
    

    @property
    def vdm_latch_clear_done(self):
        self._b.twi_sbw(126, b'\x00\x2F')#switch page
        time.sleep(0.01) 
        val = (self._b.twi_rr(145) >> 6) & 0x01
        print('latch clear %d.\n' % val)
        return val


    @property
    def vdm_24h(self):
        self._b.twi_sbw(126, b'\x00\x24')#switch page
        time.sleep(0.05)
        data = self._b.twi_srr(128, 16)
        bers = {}
        for i in range(8):
            val = struct.unpack('>H', data[i*2:i*2 + 2])[0]
            bers[i] = (hex(val), (val & 0x7ff) * 10**((val >> 11) - 24))
        print(bers)

    @property
    def vdm_24h_co(self):
        self._b.twi_sbw(126, b'\x00\x24')#switch page
        time.sleep(0.05)
        data = self._b.twi_srr(144, 10)
        rsp = {}
        rsp['CD ps/nm'] = struct.unpack('>h', data[0:2])[0]
        rsp['DGD 0.01ps'] = struct.unpack('>H', data[2:4])[0]
        rsp['PDL 0.1db'] = struct.unpack('>H', data[4:6])[0]
        rsp['CFO 1MHZ'] = struct.unpack('>h', data[6:8])[0]
        rsp['EVM 100/65535'] = struct.unpack('>H', data[8:10])[0]
        return rsp

    @property
    def vdm_all(self):
        self._b.twi_sbw(126, b'\x00\x24')#switch page
        time.sleep(0.02)
        data = self._b.twi_srr(128, 16)
        response = {}
        bers = []
        for i in range(8):
            val = struct.unpack('>H', data[i*2:i*2 + 2])[0]
            bers.append((val & 0x7ff) * 10**((val >> 11) - 24))

        response['Media Min Pre'] = bers[0]
        response['Media Max Pre'] = bers[1]
        response['Media Avg Pre'] = bers[2]
        response['Media Cur Pre'] = bers[3]
        response['Host Min Pre'] = bers[4]
        response['Host Max Pre'] = bers[5]
        response['Host Avg Pre'] = bers[6]
        response['Host Cur Pre'] = bers[7]

        data = self._b.twi_srr(162, 16)
        bers_post = []
        for i in range(8):
            val = struct.unpack('>H', data[i*2:i*2 + 2])[0]
            bers_post.append((val & 0x7ff) * 10**((val >> 11) - 24))

        response['Media Min Post'] = bers_post[0]
        response['Media Max Post'] = bers_post[1]
        response['Media Avg Post'] = bers_post[2]
        response['Media Cur Post'] = bers_post[3]
        response['Host Min Post'] = bers_post[4]
        response['Host Max Post'] = bers_post[5]
        response['Host Avg Post'] = bers_post[6]
        response['Host Cur Post'] = bers_post[7]

        data = self._b.twi_srr(144, 18)
        response['CD ps/nm'] = struct.unpack('>h', data[0:2])[0]
        response['DGD 0.01ps'] = struct.unpack('>H', data[2:4])[0]
        response['PDL 0.1db'] = struct.unpack('>H', data[4:6])[0]
        response['CFO 1MHZ'] = struct.unpack('>h', data[6:8])[0]
        response['EVM 100/65535'] = struct.unpack('>H', data[8:10])[0]
        response['Laser Temp'] = struct.unpack('>h', data[10:12])[0] / 256.0
        response['Tx Power'] = struct.unpack('>h', data[12:14])[0] / 100.0
        response['Rx Sig Power'] = struct.unpack('>h', data[14:16])[0] / 100.0
        response['Rx Total Power'] = struct.unpack('>h', data[16:18])[0] / 100.0


        data = self._b.twi_srr(178, 14)
        response['Bias XI'] = (struct.unpack('>H', data[0:2])[0] / 65535) * 100
        response['Bias XQ'] = (struct.unpack('>H', data[2:4])[0] / 65535) * 100
        response['Bias XP'] = (struct.unpack('>H', data[4:6])[0] / 65535) * 100
        response['Bias YI'] = (struct.unpack('>H', data[6:8])[0] / 65535) * 100
        response['Bias YQ'] = (struct.unpack('>H', data[8:10])[0] / 65535) * 100
        response['Bias YP'] = (struct.unpack('>H', data[10:12])[0] / 65535) * 100
        response['OSNR'] = (struct.unpack('>H', data[12:14])[0] / 10)

        self._b.twi_sbw(126, b'\x00\x11')#switch page
        time.sleep(0.02)
        if 2 == (self._b.twi_rr(206) >> 4):#4*100ge
            self._b.twi_sbw(126, b'\x00\x25')#switch page
            time.sleep(0.02)
            data = self._b.twi_srr(128, 48)
            bers = []
            for i in range(24):
                val = struct.unpack('>H', data[i*2:i*2 + 2])[0]
                bers.append((val & 0x7ff) * 10**((val >> 11) - 24))
            response['Host Min Pre 3'] = bers[0]
            response['Host Max Pre 3'] = bers[1]
            response['Host Avg Pre 3'] = bers[2]
            response['Host Cur Pre 3'] = bers[3]
            response['Host Min Post 3'] = bers[4]
            response['Host Max Post 3'] = bers[5]
            response['Host Avg Post 3'] = bers[6]
            response['Host Cur Post 3'] = bers[7]

            response['Host Min Pre 5'] = bers[8]
            response['Host Max Pre 5'] = bers[9]
            response['Host Avg Pre 5'] = bers[10]
            response['Host Cur Pre 5'] = bers[11]
            response['Host Min Post 5'] = bers[12]
            response['Host Max Post 5'] = bers[13]
            response['Host Avg Post 5'] = bers[14]
            response['Host Cur Post 5'] = bers[15]

            response['Host Min Pre 7'] = bers[16]
            response['Host Max Pre 7'] = bers[17]
            response['Host Avg Pre 7'] = bers[18]
            response['Host Cur Pre 7'] = bers[19]
            response['Host Min Post 7'] = bers[20]
            response['Host Max Post 7'] = bers[21]
            response['Host Avg Post 7'] = bers[22]
            response['Host Cur Post 7'] = bers[23]

        return response


    @property
    def pm_34h(self):
        self._b.twi_sbw(126, b'\x00\x34')#switch page
        time.sleep(0.05)
        data = self._b.twi_srr(128, 60)
        response = {}
        response['mediaRxBitsPm'] = struct.unpack('>Q', data[0:8])[0]
        response['mediaRxBitsSubIntPm'] = struct.unpack('>Q', data[8:16])[0]
        response['mediaRxCorrBitsPm'] = struct.unpack('>Q', data[16:24])[0]
        response['mediaRxMinCorrBitsSubIntPm'] = struct.unpack('>Q', data[24:32])[0]
        response['mediaRxMaxCorrBitsSubIntPm'] = struct.unpack('>Q', data[32:40])[0]
        response['mediaRxFramesPm'] = struct.unpack('>I', data[40:44])[0]
        response['mediaRxFramesSubIntPm'] = struct.unpack('>I', data[44:48])[0]
        response['mediaRxFramesUncorrErrPm'] = struct.unpack('>I', data[48:52])[0]
        response['mediaRxMinFramesUncorrErrSubintPm'] = struct.unpack('>I', data[52:56])[0]
        response['mediaRxMaxFramesUncorrErrSubintPm'] = struct.unpack('>I', data[56:60])[0]

        return response

    @property
    def pm_35h(self):
        self._b.twi_sbw(126, b'\x00\x35')#switch page
        time.sleep(0.05)
        data = self._b.twi_srr(128, 128)
        response = {}
        response['rxAvgCdPm'] = struct.unpack('>i', data[0:4])[0]
        response['rxMinCdPm'] = struct.unpack('>i', data[4:8])[0]
        response['rxMaxCdPm'] = struct.unpack('>i', data[8:12])[0]
        response['rxAvgDgdPm'] = struct.unpack('>H', data[12:14])[0]
        response['rxMinDgdPm'] = struct.unpack('>H', data[14:16])[0]
        response['rxMaxDgdPm'] = struct.unpack('>H', data[16:18])[0]
        response['rxAvgSopmdPm'] = struct.unpack('>H', data[18:20])[0]
        response['rxMinSopmdPm'] = struct.unpack('>H', data[20:22])[0]
        response['rxMaxSopmdPm'] = struct.unpack('>H', data[22:24])[0]
        response['rxAvgPdlPm'] = struct.unpack('>H', data[24:26])[0]
        response['rxMinPdlPm'] = struct.unpack('>H', data[26:28])[0]
        response['rxMaxPdlPm'] = struct.unpack('>H', data[28:30])[0]
        response['rxAvgOsnrPm'] = struct.unpack('>H', data[30:32])[0]
        response['rxMinOsnrPm'] = struct.unpack('>H', data[32:34])[0]
        response['rxMaxOsnrPm'] = struct.unpack('>H', data[34:36])[0]
        response['rxAvgEsnrPm'] = struct.unpack('>H', data[36:38])[0]
        response['rxMinEsnrPm'] = struct.unpack('>H', data[38:40])[0]
        response['rxMaxEsnrPm'] = struct.unpack('>H', data[40:42])[0]
        response['rxAvgCfoPm'] = struct.unpack('>h', data[42:44])[0]
        response['rxMinCfoPm'] = struct.unpack('>h', data[44:46])[0]
        response['rxMaxCfoPm'] = struct.unpack('>h', data[46:48])[0]
        response['rxAvgEvmPm'] = struct.unpack('>H', data[48:50])[0]
        response['rxMinEvmPm'] = struct.unpack('>H', data[50:52])[0]
        response['rxMaxEvmPm'] = struct.unpack('>H', data[52:54])[0]
        response['txAvgPowerPm'] = struct.unpack('>h', data[54:56])[0] / 100.0
        response['txMinPowerPm'] = struct.unpack('>h', data[56:58])[0] / 100.0
        response['txMaxPowerPm'] = struct.unpack('>h', data[58:60])[0] / 100.0
        response['rxAvgPowerPm'] = struct.unpack('>h', data[60:62])[0] / 100.0
        response['rxMinPowerPm'] = struct.unpack('>h', data[62:64])[0] / 100.0
        response['rxMaxPowerPm'] = struct.unpack('>h', data[64:66])[0] / 100.0
        response['rxAvgSigPowerPm'] = struct.unpack('>h', data[66:68])[0] / 100.0
        response['rxMinSigPowerPm'] = struct.unpack('>h', data[68:70])[0] / 100.0
        response['rxMaxSigPowerPm'] = struct.unpack('>h', data[70:72])[0] / 100.0
        response['rxAvgSopcrPm'] = struct.unpack('>H', data[72:74])[0]
        response['rxMinSopcrPm'] = struct.unpack('>H', data[74:76])[0]
        response['rxMaxSopcrPm'] = struct.unpack('>H', data[76:78])[0]
        response['rxAvgMerPm'] = struct.unpack('>H', data[78:80])[0]
        response['rxMinMerPm'] = struct.unpack('>H', data[80:82])[0]
        response['rxMaxMerPm'] = struct.unpack('>H', data[82:84])[0]
        return response

    @property
    def pm_3Ah(self):
        self._b.twi_sbw(126, b'\x00\x3A')#switch page
        time.sleep(0.05)
        data = self._b.twi_srr(128, 60)
        response = {}
        response['hostRxBitsPm'] = struct.unpack('>Q', data[0:8])[0]
        response['hostRxBitsSubIntPm'] = struct.unpack('>Q', data[8:16])[0]
        response['hostRxCorrBitsPm'] = struct.unpack('>Q', data[16:24])[0]
        response['hostRxMinCorrBitsSubIntPm'] = struct.unpack('>Q', data[24:32])[0]
        response['hostRxMaxCorrBitsSubIntPm'] = struct.unpack('>Q', data[32:40])[0]
        response['hostRxFramesPm'] = struct.unpack('>I', data[40:44])[0]
        response['hostRxFramesSubIntPm'] = struct.unpack('>I', data[44:48])[0]
        response['hostRxFramesUncorrErrPm'] = struct.unpack('>I', data[48:52])[0]
        response['hostRxMinFramesUncorrErrSubintPm'] = struct.unpack('>I', data[52:56])[0]
        response['hostRxMaxFramesUncorrErrSubintPm'] = struct.unpack('>I', data[56:60])[0]

        self._b.twi_sbw(126, b'\x00\x11')#switch page
        time.sleep(0.02)
        if 2 == (self._b.twi_rr(206) >> 4):#4*100ge
            self._b.twi_sbw(126, b'\x02\x3A')#switch page
            time.sleep(0.05)
            data = self._b.twi_srr(128, 60)
            response['hostRxBitsPm3'] = struct.unpack('>Q', data[0:8])[0]
            response['hostRxBitsSubIntPm3'] = struct.unpack('>Q', data[8:16])[0]
            response['hostRxCorrBitsPm3'] = struct.unpack('>Q', data[16:24])[0]
            response['hostRxMinCorrBitsSubIntPm3'] = struct.unpack('>Q', data[24:32])[0]
            response['hostRxMaxCorrBitsSubIntPm3'] = struct.unpack('>Q', data[32:40])[0]
            response['hostRxFramesPm3'] = struct.unpack('>I', data[40:44])[0]
            response['hostRxFramesSubIntPm3'] = struct.unpack('>I', data[44:48])[0]
            response['hostRxFramesUncorrErrPm3'] = struct.unpack('>I', data[48:52])[0]
            response['hostRxMinFramesUncorrErrSubintPm3'] = struct.unpack('>I', data[52:56])[0]
            response['hostRxMaxFramesUncorrErrSubintPm3'] = struct.unpack('>I', data[56:60])[0]

            self._b.twi_sbw(126, b'\x04\x3A')#switch page
            time.sleep(0.05)
            data = self._b.twi_srr(128, 60)
            response['hostRxBitsPm5'] = struct.unpack('>Q', data[0:8])[0]
            response['hostRxBitsSubIntPm5'] = struct.unpack('>Q', data[8:16])[0]
            response['hostRxCorrBitsPm5'] = struct.unpack('>Q', data[16:24])[0]
            response['hostRxMinCorrBitsSubIntPm5'] = struct.unpack('>Q', data[24:32])[0]
            response['hostRxMaxCorrBitsSubIntPm5'] = struct.unpack('>Q', data[32:40])[0]
            response['hostRxFramesPm5'] = struct.unpack('>I', data[40:44])[0]
            response['hostRxFramesSubIntPm5'] = struct.unpack('>I', data[44:48])[0]
            response['hostRxFramesUncorrErrPm5'] = struct.unpack('>I', data[48:52])[0]
            response['hostRxMinFramesUncorrErrSubintPm5'] = struct.unpack('>I', data[52:56])[0]
            response['hostRxMaxFramesUncorrErrSubintPm5'] = struct.unpack('>I', data[56:60])[0]


            self._b.twi_sbw(126, b'\x00\x3A')#switch page
            time.sleep(0.05)
            data = self._b.twi_srr(128, 60)
            response['hostRxBitsPm7'] = struct.unpack('>Q', data[0:8])[0]
            response['hostRxBitsSubIntPm7'] = struct.unpack('>Q', data[8:16])[0]
            response['hostRxCorrBitsPm7'] = struct.unpack('>Q', data[16:24])[0]
            response['hostRxMinCorrBitsSubIntPm7'] = struct.unpack('>Q', data[24:32])[0]
            response['hostRxMaxCorrBitsSubIntPm7'] = struct.unpack('>Q', data[32:40])[0]
            response['hostRxFramesPm7'] = struct.unpack('>I', data[40:44])[0]
            response['hostRxFramesSubIntPm7'] = struct.unpack('>I', data[44:48])[0]
            response['hostRxFramesUncorrErrPm7'] = struct.unpack('>I', data[48:52])[0]
            response['hostRxMinFramesUncorrErrSubintPm7'] = struct.unpack('>I', data[52:56])[0]
            response['hostRxMaxFramesUncorrErrSubintPm7'] = struct.unpack('>I', data[56:60])[0]

        return response

    def f11p5Decode(self, val):
        return (val & 0x7ff) * 10**((val >> 11) - 24)

    def f11p5Code(self, f):
        s = 24
        old_f = f
        if f > 2047:
            while f > 2047:
                s += 1
                if (31 == s):
                    break
                f /= 10.0
        else:
            while f < 2047:
                s -= 1
                if (0 == s):
                    break
                f *= 10.0
            s += 1
        m = (int)(old_f * (10 ** (24 -s)))
        m &= 0xffff #keep lower 16bits
        return (((s & 0x1f) << 11) | (m & 0x7ff))

    @property
    def mFddRaiseTh(self):
        self._b.twi_sbw(126, b'\x00\x30')#switch page
        time.sleep(0.05)
        data = self._b.twi_srr(160, 2)
        return self.f11p5Decode(struct.unpack('>H', data[0:2])[0])

    @mFddRaiseTh.setter
    def mFddRaiseTh(self, f):
        self._b.twi_sbw(126, b'\x00\x30')#switch page
        time.sleep(0.05)
        val = self.f11p5Code(f)
        self._b.twi_sbw(160, struct.pack('>H', val))

    @property
    def mFddClrTh(self):
        self._b.twi_sbw(126, b'\x00\x30')#switch page
        time.sleep(0.05)
        data = self._b.twi_srr(162, 2)
        return self.f11p5Decode(struct.unpack('>H', data[0:2])[0])

    @mFddClrTh.setter
    def mFddClrTh(self, f):
        self._b.twi_sbw(126, b'\x00\x30')#switch page
        time.sleep(0.05)
        val = self.f11p5Code(f)
        self._b.twi_sbw(162, struct.pack('>H', val))

    @property
    def mFedRaiseTh(self):
        self._b.twi_sbw(126, b'\x00\x30')#switch page
        time.sleep(0.05)
        data = self._b.twi_srr(164, 2)
        return self.f11p5Decode(struct.unpack('>H', data[0:2])[0])

    @mFedRaiseTh.setter
    def mFedRaiseTh(self, f):
        self._b.twi_sbw(126, b'\x00\x30')#switch page
        time.sleep(0.05)
        val = self.f11p5Code(f)
        self._b.twi_sbw(164, struct.pack('>H', val))

    @property
    def mFedClrTh(self):
        self._b.twi_sbw(126, b'\x00\x30')#switch page
        time.sleep(0.05)
        data = self._b.twi_srr(166, 2)
        return self.f11p5Decode(struct.unpack('>H', data[0:2])[0])

    @mFedClrTh.setter
    def mFedClrTh(self, f):
        self._b.twi_sbw(126, b'\x00\x30')#switch page
        time.sleep(0.05)
        val = self.f11p5Code(f)
        self._b.twi_sbw(166, struct.pack('>H', val))

    @property
    def mFddEn(self):
        self._b.twi_sbw(126, b'\x00\x30')#switch page
        time.sleep(0.05)
        data = self._b.twi_rr(168)
        return data & 0x01

    @mFddEn.setter
    def mFddEn(self, val):
        self._b.twi_sbw(126, b'\x00\x30')#switch page
        time.sleep(0.05)
        data = self._b.twi_rr(168)
        data &= 0xfe #clear bit0
        data |= val & 0x01
        self._b.twi_bw(168, data)

    @property
    def mFedEn(self):
        self._b.twi_sbw(126, b'\x00\x30')#switch page
        time.sleep(0.05)
        data = self._b.twi_rr(168)
        return (data & 0x02) >> 1

    @mFedEn.setter
    def mFedEn(self, val):
        self._b.twi_sbw(126, b'\x00\x30')#switch page
        time.sleep(0.05)
        data = self._b.twi_rr(168)
        data &= 0xfd #clear bit0
        data |= (val & 0x01) << 1
        self._b.twi_bw(168, data)

    @property
    def mFddMask(self):
        self._b.twi_sbw(126, b'\x00\x32')#switch page
        time.sleep(0.05)
        data = self._b.twi_rr(132)
        return data & 0x01

    @mFddMask.setter
    def mFddMask(self, val):
        self._b.twi_sbw(126, b'\x00\x32')#switch page
        time.sleep(0.05)
        data = self._b.twi_rr(132)
        data &= 0xfe #clear bit0
        data |= val & 0x01
        self._b.twi_bw(132, data)

    @property
    def mFedMask(self):
        self._b.twi_sbw(126, b'\x00\x32')#switch page
        time.sleep(0.05)
        data = self._b.twi_rr(132)
        return (data & 0x02) >> 1

    @mFedMask.setter
    def mFedMask(self, val):
        self._b.twi_sbw(126, b'\x00\x32')#switch page
        time.sleep(0.05)
        data = self._b.twi_rr(132)
        data &= 0xfd #clear bit0
        data |= (val & 0x01) << 1
        self._b.twi_bw(132, data)

    @property
    def mFddFedLatch(self):
        self._b.twi_sbw(126, b'\x00\x33')#switch page
        time.sleep(0.05)
        data = self._b.twi_rr(132)
        response = {}
        response['Fdd latch'] = data & 0x01
        response['Fed latch'] = (data & 0x02) >> 1
        return response



    @property
    def hFddRaiseTh(self):
        self._b.twi_sbw(126, b'\x00\x38')#switch page
        time.sleep(0.05)
        data = self._b.twi_srr(128, 2)
        return self.f11p5Decode(struct.unpack('>H', data[0:2])[0])

    @hFddRaiseTh.setter
    def hFddRaiseTh(self, f):
        self._b.twi_sbw(126, b'\x00\x38')#switch page
        time.sleep(0.05)
        val = self.f11p5Code(f)
        self._b.twi_sbw(128, struct.pack('>H', val))

    @property
    def hFddClrTh(self):
        self._b.twi_sbw(126, b'\x00\x38')#switch page
        time.sleep(0.05)
        data = self._b.twi_srr(130, 2)
        return self.f11p5Decode(struct.unpack('>H', data[0:2])[0])

    @hFddClrTh.setter
    def hFddClrTh(self, f):
        self._b.twi_sbw(126, b'\x00\x38')#switch page
        time.sleep(0.05)
        val = self.f11p5Code(f)
        self._b.twi_sbw(130, struct.pack('>H', val))

    @property
    def hFedRaiseTh(self):
        self._b.twi_sbw(126, b'\x00\x38')#switch page
        time.sleep(0.05)
        data = self._b.twi_srr(132, 2)
        return self.f11p5Decode(struct.unpack('>H', data[0:2])[0])

    @hFedRaiseTh.setter
    def hFedRaiseTh(self, f):
        self._b.twi_sbw(126, b'\x00\x38')#switch page
        time.sleep(0.05)
        val = self.f11p5Code(f)
        self._b.twi_sbw(132, struct.pack('>H', val))

    @property
    def hFedClrTh(self):
        self._b.twi_sbw(126, b'\x00\x38')#switch page
        time.sleep(0.05)
        data = self._b.twi_srr(134, 2)
        return self.f11p5Decode(struct.unpack('>H', data[0:2])[0])

    @hFedClrTh.setter
    def hFedClrTh(self, f):
        self._b.twi_sbw(126, b'\x00\x38')#switch page
        time.sleep(0.05)
        val = self.f11p5Code(f)
        self._b.twi_sbw(134, struct.pack('>H', val))

    @property
    def hFddEn(self):
        self._b.twi_sbw(126, b'\x00\x38')#switch page
        time.sleep(0.05)
        data = self._b.twi_rr(136)
        return data & 0x01

    @hFddEn.setter
    def hFddEn(self, val):
        self._b.twi_sbw(126, b'\x00\x38')#switch page
        time.sleep(0.05)
        data = self._b.twi_rr(136)
        data &= 0xfe #clear bit0
        data |= val & 0x01
        self._b.twi_bw(136, data)

    @property
    def hFedEn(self):
        self._b.twi_sbw(126, b'\x00\x38')#switch page
        time.sleep(0.05)
        data = self._b.twi_rr(136)
        return (data & 0x02) >> 1

    @hFedEn.setter
    def hFedEn(self, val):
        self._b.twi_sbw(126, b'\x00\x38')#switch page
        time.sleep(0.05)
        data = self._b.twi_rr(136)
        data &= 0xfd #clear bit0
        data |= (val & 0x01) << 1
        self._b.twi_bw(136, data)

    @property
    def hFddMask(self):
        self._b.twi_sbw(126, b'\x00\x3B')#switch page
        time.sleep(0.05)
        data = self._b.twi_rr(128)
        return data & 0x01

    @hFddMask.setter
    def hFddMask(self, val):
        self._b.twi_sbw(126, b'\x00\x3B')#switch page
        time.sleep(0.05)
        data = self._b.twi_rr(128)
        data &= 0xfe #clear bit0
        data |= val & 0x01
        self._b.twi_bw(128, data)

    @property
    def hFedMask(self):
        self._b.twi_sbw(126, b'\x00\x3B')#switch page
        time.sleep(0.05)
        data = self._b.twi_rr(128)
        return (data & 0x02) >> 1

    @hFedMask.setter
    def hFedMask(self, val):
        self._b.twi_sbw(126, b'\x00\x3B')#switch page
        time.sleep(0.05)
        data = self._b.twi_rr(128)
        data &= 0xfd #clear bit0
        data |= (val & 0x01) << 1
        self._b.twi_bw(128, data)

    @property
    def hFddFedLatch(self):
        self._b.twi_sbw(126, b'\x00\x3B')#switch page
        time.sleep(0.05)
        data = self._b.twi_rr(192)
        response = {}
        response['Fdd latch'] = data & 0x01
        response['Fed latch'] = (data & 0x02) >> 1
        return response

    @property
    def p_times(self):
        self._b.twi_sbw(126, b'\x00\xff')#switch page
        time.sleep(0.05)
        response = {}
        rsp = self._b.twi_srr(144,2)
        response['polling Times'] = rsp[0]
        response['pm Times'] = rsp[1]
        return response

    @property
    def avs_times(self):
        self._b.twi_sbw(126, b'\x00\xff')#switch page
        time.sleep(0.05)
        response = {}
        rsp = self._b.twi_srr(146,3)
        response['avs Times'] = rsp[0]
        response['decrease Times'] = rsp[1]
        response['increase Times'] = rsp[2]
        return response

    @property
    def dsp_ism(self):
        self._b.twi_sbw(126, b'\x00\xff')#switch page
        time.sleep(0.05)
        rsp = self._b.twi_srr(149,1)
        return struct.unpack('B', rsp)[0]

    @property
    def tx_off(self):
        self._b.twi_sbw(126, b'\x00\xFF')#switch page
        time.sleep(0.05)
        return self._b.twi_rr(150)

    @tx_off.setter
    def tx_off(self,val):
        self._b.twi_sbw(126, b'\x00\xFF')#switch page
        time.sleep(0.05)
        self._b.twi_bw(150,val)

    @property
    def rx_off(self):
        self._b.twi_sbw(126, b'\x00\xFF')#switch page
        time.sleep(0.05)
        return self._b.twi_rr(151)

    @rx_off.setter
    def rx_off(self,val):
        self._b.twi_sbw(126, b'\x00\xFF')#switch page
        time.sleep(0.05)
        self._b.twi_bw(151,val)

    @property
    def abc_conv(self):
        self._b.twi_sbw(126, b'\x00\xFF')#switch page
        time.sleep(0.05)
        return self._b.twi_rr(152)

    @property
    def abc_conv2(self):
        self._b.twi_sbw(126, b'\x00\xFF')#switch page
        time.sleep(0.05)
        return self._b.twi_rr(155)

    @property
    def cfg_ver(self):
        self._b.twi_sbw(126, b'\x00\xFF')#switch page
        time.sleep(0.05)
        response = self._b.twi_srr(153, 2)
        rsp = {}
        rsp['Major'] = struct.unpack('B', response[0:1])[0]
        rsp['Minor'] = struct.unpack('B', response[1:2])[0]
        return rsp

    @property
    def dsp_ver(self):
        self._b.twi_sbw(126, b'\x00\xFF')#switch page
        time.sleep(0.05)
        response = self._b.twi_srr(157, 4)
        return struct.unpack('>I', response[0:4])[0]

    @property
    def trigger_mask(self):
        self._b.twi_sbw(126, b'\x00\xFF')#switch page
        time.sleep(0.05)
        return self._b.twi_rr(163)
    @trigger_mask.setter
    def trigger_mask(self,val):
        self._b.twi_sbw(126, b'\x00\xFF')#switch page
        time.sleep(0.05)
        self._b.twi_bw(163,val)

    @property
    def pm_exe(self):
        self._b.twi_sbw(126, b'\x00\xFF')#switch page
        time.sleep(0.01)
        response = self._b.twi_srr(164, 2)
        return struct.unpack('>H', response[0:2])[0]

    @property
    def polling_off(self):
        self._b.twi_sbw(126, b'\x00\xFF')#switch page
        time.sleep(0.05)
        return self._b.twi_rr(166)
    @polling_off.setter
    def polling_off(self,val):
        self._b.twi_sbw(126, b'\x00\xFF')#switch page
        time.sleep(0.05)
        self._b.twi_bw(166,val)

    @property
    def pm_off(self):
        self._b.twi_sbw(126, b'\x00\xFF')#switch page
        time.sleep(0.05)
        return self._b.twi_rr(167)
    @pm_off.setter
    def pm_off(self,val):
        self._b.twi_sbw(126, b'\x00\xFF')#switch page
        time.sleep(0.05)
        self._b.twi_bw(167,val)

    @property
    def imc_mrst_times(self):
        self._b.twi_sbw(126, b'\x00\xFF')#switch page
        time.sleep(0.05)
        response = self._b.twi_srr(193, 2)
        return struct.unpack('>H', response[0:2])[0]

    @property
    def imc_to_times(self):
        self._b.twi_sbw(126, b'\x00\xFF')#switch page
        time.sleep(0.05)
        response = self._b.twi_srr(170, 2)
        return struct.unpack('>H', response[0:2])[0]

    @property
    def imc_idle_cip_to_times(self):
        self._b.twi_sbw(126, b'\x00\xFF')#switch page
        time.sleep(0.05)
        response = self._b.twi_srr(177, 2)
        return struct.unpack('>H', response[0:2])[0]
        
    @property
    def imc_err_times(self):
        self._b.twi_sbw(126, b'\x00\xFF')#switch page
        time.sleep(0.05)
        response = self._b.twi_srr(179, 2)
        return struct.unpack('>H', response[0:2])[0]
    # @property
    # def oor_id(self):
    #     self._b.twi_sbw(126, b'\x00\xFF')#switch page
    #     time.sleep(0.05)
    #     return self._b.twi_rr(251)

    # @property
    # def oor_val(self):
    #     self._b.twi_sbw(126, b'\x00\xFF')#switch page
    #     time.sleep(0.05)
    #     val = struct.unpack('>f', self._b.twi_srr(252, 4))
    #     return val

    @property
    def ddm_all(self):
        ddm = DDM(self._b)
        rsp = {}
        rsp['case temp'] = ddm.case_temp
        rsp['laser temp'] = ddm.laser_temp
        rsp['dsp temp'] = ddm.dsp_temp
        rsp['vcc'] = ddm.vcc
        rsp['tx power'] = ddm.tx_power
        rsp['rx power'] = ddm.rx_power
        rsp['tx bias'] = ddm.tx_bias
        return rsp

    @property
    def mask_all_en(self):
        self._b.twi_sbw(31, b'\xFF\xFF\xFF\xFF\xFF\xFF')#31-36

        self._b.twi_bw(127, 0x10)
        time.sleep(0.05)
        sendStr = b''
        for i in range(213,232,1):#213-231
            sendStr += b'\xFF'
        self._b.twi_sbw(213, sendStr)

        self._b.twi_bw(127, 0x12)
        time.sleep(0.05)
        sendStr = b''
        for i in range(239,247,1):#239-246
            sendStr += b'\xFF'
        self._b.twi_sbw(239, sendStr)    

        self._b.twi_bw(127, 0x32)
        time.sleep(0.05)
        sendStr = b''
        for i in range(128,134,1):#128-133
            sendStr += b'\xFF'
        self._b.twi_sbw(128, sendStr)   

        self._b.twi_bw(127, 0x3b)
        time.sleep(0.05)
        sendStr = b''
        for i in range(128,130,1):#128-129
            sendStr += b'\xFF'
        self._b.twi_sbw(128, sendStr) 

    @property
    def mask_all_dis(self):
        self._b.twi_sbw(31, b'\x00\x00\x00\x00\x00\x00')#31-36

        self._b.twi_bw(127, 0x10)
        time.sleep(0.05)
        sendStr = b''
        for i in range(213,232,1):#213-231
            sendStr += b'\x00'
        self._b.twi_sbw(213, sendStr)

        self._b.twi_bw(127, 0x12)
        time.sleep(0.05)
        sendStr = b''
        for i in range(239,247,1):#239-246
            sendStr += b'\x00'
        self._b.twi_sbw(239, sendStr)    

        self._b.twi_bw(127, 0x32)
        time.sleep(0.05)
        sendStr = b''
        for i in range(128,134,1):#128-133
            sendStr += b'\x00'
        self._b.twi_sbw(128, sendStr)   

        self._b.twi_bw(127, 0x3b)
        time.sleep(0.05)
        sendStr = b''
        for i in range(128,130,1):#128-129
            sendStr += b'\x00'
        self._b.twi_sbw(128, sendStr) 

    @property
    def flags_all(self):
        rsp = {}
        response = self._b.twi_srr(8, 4)
        rsp['CDB block 1 complete'] = (response[0] & (1 << 6)) >> 6
        rsp['Data Path firmware fault'] = (response[0] & (1 << 2)) >> 2
        rsp['Module firmware fault'] = (response[0] & (1 << 1)) >> 1
        rsp['Module state changed flag'] = (response[0] & (1 << 0)) >> 0

        rsp['Vcc3.3v Low Warning'] = (response[1] & (1 << 7)) >> 7
        rsp['Vcc3.3v High Warning'] = (response[1]  & (1 << 6)) >> 6
        rsp['Vcc3.3v Low Alarm'] = (response[1]  & (1 << 5)) >> 5
        rsp['Vcc3.3v High Alarm'] = (response[1]  & (1 << 4)) >> 4

        rsp['Temp Low Warning'] = (response[1]  & (1 << 3)) >> 3
        rsp['Temp High Warning'] = (response[1]  & (1 << 2)) >> 2
        rsp['Temp Low Alarm'] = (response[1]  & (1 << 1)) >> 1
        rsp['Temp High Alarm'] = (response[1]  & (1 << 0)) >> 0

        rsp['LaserTemp Low Warning'] = (response[2] & (1 << 7)) >> 7
        rsp['LaserTemp High Warning'] = (response[2] & (1 << 6)) >> 6
        rsp['LaserTemp Low Alarm'] = (response[2] & (1 << 5)) >> 5
        rsp['LaserTemp High Alarm'] = (response[2] & (1 << 4)) >> 4

        rsp['Aux1 Low Warning'] = (response[2] & (1 << 3)) >> 3
        rsp['Aux1 High Warning'] = (response[2] & (1 << 2)) >> 2
        rsp['Aux1 Low Alarm'] = (response[2] & (1 << 1)) >> 1
        rsp['Aux1 High Alarm'] = (response[2] & (1 << 0)) >> 0

        rsp['DspTemp Low Warning'] = (response[3] & (1 << 7)) >> 7
        rsp['DspTemp High Warning'] = (response[3] & (1 << 6)) >> 6
        rsp['DspTemp Low Alarm'] = (response[3] & (1 << 5)) >> 5
        rsp['DspTemp High Alarm'] = (response[3] & (1 << 4)) >> 4


        self._b.twi_sbw(126, b'\x00\x11')#switch page
        time.sleep(0.05)
        rsp['rxoutput State Changed'] = self._b.twi_rr(133)
        response = self._b.twi_srr(134, 19)
        rsp['DP State Changed'] = response[0]
        rsp['TxFault'] = response[1]
        rsp['TxLos'] = response[2]
        rsp['TxCdrLol'] = response[3]
        rsp['Tx Adaptive Input Eq Fault'] = response[4]
        rsp['Tx Power High Alarm'] = response[5]
        rsp['Tx Power Low Alarm'] = response[6]
        rsp['Tx Power High Warn'] = response[7]
        rsp['Tx Power Low Warn'] = response[8]
        rsp['Tx Bias High Alarm'] = response[9]
        rsp['Tx Bias Low Alarm'] = response[10]
        rsp['Tx Bias High Warn'] = response[11]
        rsp['Tx Bias Low Warn'] = response[12]
        rsp['Rx LOS'] = response[13]
        rsp['Rx LOL'] = response[14]
        rsp['Rx Power High Alarm'] = response[15]
        rsp['Rx Power Low Alarm'] = response[16]
        rsp['Rx Power High Warn'] = response[17]
        rsp['Rx Power Low Warn'] = response[18]

        self._b.twi_sbw(126, b'\x00\x12')#switch page
        time.sleep(0.05)
        data = self._b.twi_rr(231)
        rsp['Tuning Busy'] = (data >> 3) & 0x01
        rsp['Invalid Channel'] = (data >> 2) & 0x01
        rsp['Wavelength unlocked'] = (data >> 1) & 0x01
        rsp['Tuning complete'] = (data >> 0) & 0x01

        self._b.twi_sbw(126, b'\x00\x33')#switch page
        time.sleep(0.05)
        response = self._b.twi_srr(128, 6)
        rsp['mediaTxLoa'] = (response[0] >> 5) & 0x01
        rsp['mediaTxOoa'] = (response[0] >> 4) & 0x01
        rsp['mediaTxLolCmu'] = (response[0] >> 3) & 0x01
        rsp['mediaTxLolRefClk'] = (response[0] >> 2) & 0x01
        rsp['mediaTxLolDeSkew'] = (response[0] >> 1) & 0x01
        rsp['mediaTxFIFO'] = (response[0] >> 0) & 0x01

        rsp['mediaRxLolDemod'] = (response[2] >> 5) & 0x01
        rsp['mediaRxLolCd'] = (response[2] >> 4) & 0x01
        rsp['mediaRxLoa'] = (response[2] >> 3) & 0x01
        rsp['mediaRxOoa'] = (response[2] >> 2) & 0x01
        rsp['mediaRxLolDeskew'] = (response[2] >> 1) & 0x01
        rsp['mediaRxLolFifo'] = (response[2] >> 0) & 0x01

        rsp['mediaRxFedPm'] = (response[4] >> 1) & 0x01
        rsp['mediaRxFddPm'] = (response[4] >> 0) & 0x01

        rsp['mediaRemoteDegrade'] = (response[5] >> 1) & 0x01
        rsp['mediaLocalDegrade'] = (response[5] >> 0) & 0x01

        self._b.twi_sbw(126, b'\x00\x3B')#switch page
        time.sleep(0.05)
        response = self._b.twi_srr(192, 2)
        rsp['hostRxFedPm'] = (response[0] >> 1) & 0x01
        rsp['hostRxFddPm'] = (response[0] >> 0) & 0x01

        rsp['hostRemoteDegrade'] = (response[1] >> 1) & 0x01
        rsp['hostLocalDegrade'] = (response[1] >> 0) & 0x01

        #vdm reserved
        return rsp
    @property
    def rx_output_sta(self):
        self._b.twi_bw(127,0x11)
        return self._b.twi_rr(132)
        
    def WaitModActivated(self):
        print('power up.\n')
        if 2 == (self._b.twi_rr(3) & 0xfe):
            self._b.twi_bw(26,0)
        time.sleep(1)
        while 6 != (self._b.twi_rr(3) & 0xfe):
            time.sleep(5)
            print('.', sep='', end='', flush=True)
        print('ready.\n')

        while 4 != (self.dp_state):
            time.sleep(5)
            print('.', sep='', end='', flush=True)
        print('DP Activatied.\n')

    def SetRegLpwrAndWaitModLpwr(self):
        print("set low pwr.\n")
        self._b.twi_bw(26,0x10)
        while 2 != self.m_state:
            time.sleep(0.05)
        print("into low pwr.\n")

    def ReleaseRegLpwrAndWaitModActivated(self):
        print("release low pwr.\n")
        self._b.twi_bw(26,0)
        while 6 != self.m_state:
            time.sleep(1)
            print('.', sep='', end='', flush=True)
        print('\n')
        print("module ready, into dp init.\n")
        while 4 != (self.dp_state):
            time.sleep(1)
            print('.', sep='', end='', flush=True)
        print('\n')
        print('DP Activatied.\n')

    def SetForceLpwrAndWaitModLpwr(self):
        print("set force low pwr.\n")
        self._b.twi_bw(26,0x40)
        while 2 != self.m_state:
            time.sleep(0.05)
        print("into low pwr.\n")

    def SetFreqChn(self, chn):
        self.dp_deinit=1
        print('Set DP to Deinit.\n')
        time.sleep(0.5)
        while 1 != self.dp_state:
            time.sleep(0.5)
            print('Wait to DP Deact.\n')

        self.cmis_ch = chn
        print('Switch ch to %d.\n' % chn)
        time.sleep(0.05)

        self.dp_deinit=0
        print('Release DP to Init.\n')
        while 4 != self.dp_state:
            time.sleep(5)

        print('Freq = ', self.cur_freq)

    @property
    def FSM_time(self):
        self._b.twi_sbw(126, b'\x00\xfe')#switch page
        time.sleep(0.05)
        response = {}
        rsp = self._b.twi_srr(128,60)

        response['M-Reset_t'] = struct.unpack('>1f', rsp[0:4])[0]
        response['M-Init_t'] = struct.unpack('>1f', rsp[4:8])[0]
        response['M-Resetting_t'] = struct.unpack('>1f', rsp[8:12])[0]
        response['M-LowPwr_t'] = struct.unpack('>1f', rsp[12:16])[0]
        response['M-PwrUp_t'] = struct.unpack('>1f', rsp[16:20])[0]
        response['M-PwrDn_t'] = struct.unpack('>1f', rsp[20:24])[0]
        response['M-Ready_t'] = struct.unpack('>1f', rsp[24:28])[0]
        response['M-Fault_t'] = struct.unpack('>1f', rsp[28:32])[0]
        response['DP-DeActivated_t'] = struct.unpack('>1f', rsp[32:36])[0]
        response['DP-Init_t'] = struct.unpack('>1f', rsp[36:40])[0]
        response['DP-DeInit_t'] = struct.unpack('>1f', rsp[40:44])[0]
        response['DP-Initialized_t'] = struct.unpack('>1f', rsp[44:48])[0]
        response['DP-TurnOff_t'] = struct.unpack('>1f', rsp[48:52])[0]
        response['DP-TurnOn_t'] = struct.unpack('>1f', rsp[52:56])[0]
        response['DP-Activated_t'] = struct.unpack('>1f', rsp[56:60])[0]

        return response

    @property
    def cosa_state(self):
        # return self._b.twi_rr(67)
        self._b.twi_sbw(126, b'\x00\xFF')#switch page
        time.sleep(0.05)
        return self._b.twi_rr(183) 

    @property
    def dsp_state(self):
        # return self._b.twi_rr(66)
        self._b.twi_sbw(126, b'\x00\xFF')#switch page
        time.sleep(0.05)
        return self._b.twi_rr(184) 

    def SetDpDeinitAndWaitDpDeact(self):
        self.dp_deinit=1
        time.sleep(0.5)
        while 1 != self.dp_state:
            time.sleep(0.5)
            print('.', sep='', end='', flush=True)
        print('\n')
        print('DP Into Deact.\n')

    def ReleaseDpDeinitAndWaitDpAct(self):
        self.dp_deinit=0
        print('Release DP to Init.\n')
        while 4 != self.dp_state:
            time.sleep(5)
            print('.', sep='', end='', flush=True)
        print('\n')
        print('DP Into Act.\n')

    def VdmLatchAndWaitDone(self):
        print('VDM Latch Set.\n')
        self.vdm_latch_req = 1
        while 1 != self.vdm_latch_done:
            time.sleep(0.05)
        print('\n')
        print('VDM Latch Done.\n')

    def VdmLatchClearAndWaitDone(self):
        print('VDM Latch Clear.\n')
        self.vdm_latch_req = 0
        while 1 != self.vdm_latch_clear_done:
            time.sleep(0.05)
        print('\n')
        print('VDM Latch Clear Done.\n')

    @property
    def fw_ver(self):
        cdb = CDB(self._b)
        rlplen,rlp_chkcode,rlp = cdb.CMD0100h()
        if self._b.cdb_chkcode(rlp) == rlp_chkcode:
            fwStaus = rlp[0]#136
            if (fwStaus & 0x01): # running at image A
                return '{}.{}.{}'.format(rlp[2],rlp[3],(rlp[4]<<8) | rlp[5])
            elif ((fwStaus >> 4) & 0x01): # running at image B
                return '{}.{}.{}'.format(rlp[174-136], rlp[175-136],(rlp[176-136]<<8) | rlp[177-136])

    @property
    def mod_sn(self):
        # 166-181 16 Vendor SN Vendor Serial Number (ASCII)
        self._b.twi_bw(127,0)
        sn = self._b.twi_srr(166,16)
        res = ''
        for s in sn:
            res += chr(s)
        return res
		
    def CheckCurFreqMatch100Grid(self):
        if 0x40 == self._b.twi_rr(1):
            freq = self.cur_freq
            if freq == (193.1 + self.cmis_ch * 0.1):
                return True, freq
            else:
                return False, freq
        else:
            freq = self.cur_freq_4p1
            if freq == (193100000 + self.cmis_ch*100000):
                return True, freq
            else:
                return False, freq
    
    @property
    def cur_mode(self):
        self._b.twi_sbw(126, b'\x00\x11')#switch page
        time.sleep(0.01)
        return self._b.twi_rr(206) >> 4

    def switch_mode(self,val):
        self._b.twi_sbw(126, b'\x00\x10')#switch page
        time.sleep(0.01)
        if 1 == val:#stage 0
            self._b.twi_bw(143, 0xff)
        elif 2 == val:#stage 1
            self._b.twi_bw(178, 0xff)
			
    @property
    def tx_voas(self):
        self._b.twi_sbw(126, b'\x00\xFF')#switch page
        time.sleep(0.05)
        rsp = self._b.twi_srr(202,6)
        response = {}

        response['voax_mA'] = struct.unpack('>h', rsp[0:2])[0] / 1000
        response['voay_mA'] = struct.unpack('>h', rsp[2:4])[0] / 1000
        response['voa_dB'] = struct.unpack('>h', rsp[4:6])[0] / 100
        return response

    @property
    def rx_voas(self):
        self._b.twi_sbw(126, b'\x00\xFF')#switch page
        time.sleep(0.05)
        self._b.twi_bw(212,1)
        time.sleep(0.5)
        rsp = self._b.twi_srr(213,11)
        response = {}
       
        response['siop_after_voa'] = struct.unpack('>h', rsp[0:2])[0] / 100
        response['siop_before_voa'] = struct.unpack('>h', rsp[2:4])[0] / 100
        response['voa_dB'] = struct.unpack('>h', rsp[4:6])[0] / 100
        response['voax_mA'] = struct.unpack('>h', rsp[6:8])[0] / 1000
        response['voay_mA'] = struct.unpack('>h', rsp[8:10])[0] / 1000
        response['en'] = struct.unpack('B', rsp[10:11])[0]

        return response



    @property
    def rx_voa_en(self):
        self._b.twi_sbw(126, b'\x00\xFF')#switch page
        time.sleep(0.05)
        return self._b.twi_rr(223)
        
    @rx_voa_en.setter   
    def rx_voa_en(self, en):
        self._b.twi_sbw(126, b'\x00\xFF')#switch page
        time.sleep(0.05)
        self._b.twi_bw(223,en)   

    def b0_pre_emp_set(self, lane, pre, main, post):
        self._b.twi_sbw(126, b'\x00\xb0')#switch page
        time.sleep(0.01)
        self._b.twi_sbw(128+lane*6, struct.pack('>h',pre))
        self._b.twi_sbw(130+lane*6, struct.pack('>h',main))
        self._b.twi_sbw(132+lane*6, struct.pack('>h',post))

    def b0_pre_emp_get(self, lane):
        self._b.twi_sbw(126, b'\x00\xb0')#switch page
        time.sleep(0.01)
        response = {} 
        rsp = self._b.twi_srr(128+lane*6, 6)
        response['pre'] = struct.unpack('>h',rsp[0:2])[0]
        response['main'] = struct.unpack('>h',rsp[2:4])[0]
        response['post'] = struct.unpack('>h',rsp[4:6])[0]
        return response

