import sys
import time
import struct

from .broker import Broker
from .dpin import DPin
from .ain import Ain
from .aout import Aout
from .laser import Laser
from .cdm import CDM
from .abc import ABC
from .dsp import Dsp
from .flash import Flash

CONFIG_SECTOR = Flash.SECTOR_COUNT - 1
CONFIG_ADDRESS = Flash.SECTOR_SIZE * CONFIG_SECTOR

class Mod:
    def __init__(self, b):
        self._b = b
        self.laser = Laser(b)
        self.cdm = CDM(b)
        self.abc = ABC(b)
        self.dsp = Dsp(b)
        # self.startup()

    def startup(self):
        print('*** Start up CFP2-DCO module #{} ***'.format(self.id))
        print('=============================================')

        # power enable #1
        sys.stdout.write('Enable EN_5V_TX and N5V2_EN ... ')
        sys.stdout.flush()
        self.en5vtx = DPin(self._b, 'EN_5V_TX')
        self.enn5v = DPin(self._b, 'N5V2_EN')
        self.en5vtx.state = 1
        self.enn5v.state = 1
        sys.stdout.write('done.\n')
        
        # cdm tec enable
        sys.stdout.write('Enable CDM TEC ... ')
        sys.stdout.flush()
        self.cdm.tec.target = 50.0
        self.cdm.tec.service = True
        sys.stdout.write('done.\n')
        self.temp = Ain(self._b, 'MOD_THERM_ADC')
        # print('Current CDM TEC temperature: {} degree.'.format(self.temp.aval))

        # abc vga = 0
        sys.stdout.write('Set ABC VGA to 1-multiply ... ')
        sys.stdout.flush()
        self.vga = Aout(self._b, 'ABC_VGA_R')
        self.vga.aval = 30000.0
        sys.stdout.write('done.\n')

        # enable laser
        sys.stdout.write('Enable ITLA ... ')
        sys.stdout.flush()
        self.laser.rst_n = 1
        time.sleep(1)
        self.laser.frequency_setting(193.55)
        self.laser.power_setting(15.5)
        time.sleep(1)
        self.laser.dis_n = 1
        sys.stdout.write('done.\n')

        # power up cdm
        sys.stdout.write('Powering up CDM ... ')
        sys.stdout.flush()
        self.cdm.power = True
        sys.stdout.write('done.\n')

        # power up cdm
        sys.stdout.write('Set CDM EQ-X/Y ... ')
        sys.stdout.flush()
        self.cdm._eqx.aval = 8.0
        self.cdm._eqy.aval = 8.0
        sys.stdout.write('done.\n')

        # enable abc
        sys.stdout.write('Running ABC ... ')
        sys.stdout.flush()
        self.mpd = Ain(self._b, 'MZ_MPD1_DC_ADC')
        self.abc.setting = 1, 600, 0, 1024
        for ph in range(6):
            self.abc.theta_set(ph,355)
            self.abc.pid_set(ph, (1e-5, 0, 0, 0, 1))
            # self.abc.theta_set(ph, 160)
            # if ph in [0, 3]:
            #     self.abc.method_set(ph, 2)
            # else:
            #     self.abc.method_set(ph, 1)
        self.abc.service = 0x3f
        # ticks = 0
        # while True:
        #     ticks += 1
        #     if ticks > 20:
        #         break
        #     else:
        #         print(self.mpd.dval)
        #         time.sleep(3)
        # self.abc.service = 0x0
        # self.abc.setting = 1, 400, 0, 1024
        # for ph in [0, 3]:
        #     self.abc.method_set(ph, 2)
        # self.abc.service = 0x3f
        sys.stdout.write('done.\n')

        # power enable #2
        sys.stdout.write('Enable RX powers (ICR related) ... ')
        sys.stdout.flush()
        self.en5vrx = DPin(self._b, 'EN_5V_RX')
        self.en3v3icr = DPin(self._b, 'EN_3V3_ICR')
        self.icr_sd_n = DPin(self._b, 'ICR_SD_N')
        self.mgc_agc_sel = DPin(self._b, 'MGC_AGC_SEL')
        self.en5vrx.state = 1
        self.en3v3icr.state = 1
        self.icr_sd_n.state = 1
        self.mgc_agc_sel.state = 1
        sys.stdout.write('done.\n')

        # power up dsp
        sys.stdout.write('Powering up DSP ... ')
        sys.stdout.flush()
        self.dsp.startup()
        while 9 != self.dsp.state(): pass
        sys.stdout.write('done.\n')

        # driver setting
        sys.stdout.write('Configure RF Driver ... ')
        sys.stdout.flush()
        for ch in range(4):
            if 3 == self.id or 4 == self.id:
                self.cdm.drv.gain_set(ch, 255)
                self.cdm.drv.pkctl_set(ch, 255)
            else:
                self.cdm.drv.gain_set(ch, 500)
                self.cdm.drv.pkctl_set(ch, 63)
        sys.stdout.write('done.\n')

        # icr oa
        sys.stdout.write('Configure ICR OAs ... ')
        sys.stdout.flush()
        self.oa_xi = Aout(self._b, 'OA_XI')
        self.oa_xq = Aout(self._b, 'OA_XQ')
        self.oa_yi = Aout(self._b, 'OA_YI')
        self.oa_yq = Aout(self._b, 'OA_YQ')
        if 3 == self.id:
            self.oa_xi.aval = 0.20
            self.oa_xq.aval = 0.25
            self.oa_yi.aval = 0.25
            self.oa_yq.aval = 0.25
        else:
            self.oa_xi.aval = 0.16
            self.oa_xq.aval = 0.12
            self.oa_yi.aval = 0.16
            self.oa_yq.aval = 0.15
        sys.stdout.write('done.\n')

        # dsp configures
        sys.stdout.write('Configure DSP ... ')
        sys.stdout.flush()
        # Set Line Egress Pre-emphasis: all enable 2.5dB
        self.dsp.api(b'\x6c\x00\x11\x00\x04\x00\x0f\x02' + b'\x00' * 100)
        # Set Line Egress Attenuation: all AnalogSwing <= Medium
        self.dsp.api(b'\x0c\x00\x10\x00\x04\x00\x0f\x00\x00\x01\x00\x00')
        if 3 == self.id:
            # Set Line Egress Lane Skew: HQ <= 35
            # b'\x0c\x00\r\x00\x04\x00\x02\x00\x00\x0c\x00\x00'
            self.dsp.api(b'\x0c\x00\r\x00\x04\x00\x02\x00\x00\x23\x00\x00')
            # Set Line Egress Lane Skew: VI <= 70
            # b'\x0c\x00\r\x00\x04\x00\x04\x00\x007\x00\x00'
            self.dsp.api(b'\x0c\x00\r\x00\x04\x00\x04\x00\x00\x46\x00\x00')
            # Set Rx Skew Calibration Words: H <= 132
            self.dsp.api(b'\x0c\x00\x14\x00\x04\x00\x01\x00\x84\x00\x00\x00')
            # Set Rx Skew Calibration Words: V <= 134
            self.dsp.api(b'\x0c\x00\x14\x00\x04\x00\x04\x00\x86\x00\x00\x00')
        else:
            # Set Line Egress Lane Skew: HQ <= 12
            # b'\x0c\x00\r\x00\x04\x00\x02\x00\x00\x0c\x00\x00'
            self.dsp.api(b'\x0c\x00\r\x00\x04\x00\x02\x00\x00\x0c\x00\x00')
            # Set Line Egress Lane Skew: VI <= 55
            # b'\x0c\x00\r\x00\x04\x00\x04\x00\x007\x00\x00'
            self.dsp.api(b'\x0c\x00\r\x00\x04\x00\x04\x00\x007\x00\x00')
            # Set Rx Skew Calibration Words: H <= 128
            self.dsp.api(b'\x0c\x00\x14\x00\x04\x00\x01\x00\x80\x00\x00\x00')
            # Set Rx Skew Calibration Words: V <= 132
            self.dsp.api(b'\x0c\x00\x14\x00\x04\x00\x04\x00\x84\x00\x00\x00')
        sys.stdout.write('done.\n')

        sys.stdout.write('Set TX VOA ... ')
        sys.stdout.flush()
        self.txvoa = Aout(self._b, 'TX_VOA_DAC')
        self.txvoa.aval = 0.0
        sys.stdout.write('done.\n')

        # self.abc.setting = 1, 600, 0, 1024
        # # for ph in [0, 3]:
        # #     self.abc.method_set(ph, 2)
        # #     self.abc.pid_set(ph, (1e-5,0,0,0,1))
        # self.abc.service = 0x3f

    def get_fec_data(self):
        # Set Traffic Performance Monitoring
        self.dsp.api(b'\x08\x00F\x00\x04\x00\x01\x00')
        # Get Error Correction Statistics
        resp = self.dsp.api(b'\x08\x00\xa8\x00\xac\x00\x81\x00')        
        qAccBitCount = struct.unpack('<Q', bytes(resp[4:12]))[0]
        qAccCorrectedErrorCount = struct.unpack('<Q', bytes(resp[12:20]))[0]
        qAccUncorrectedCodewordCount = struct.unpack('<Q', bytes(resp[0x1c:0x24]))[0]
        return qAccBitCount, qAccCorrectedErrorCount, qAccUncorrectedCodewordCount

    @property
    def id(self):
        flash = Flash(self._b)
        sn = flash.read(CONFIG_ADDRESS, 4)
        return int(sn, 16)

    @id.setter
    def id(self, sn):
        flash = Flash(self._b)
        flash.erase_sector(CONFIG_SECTOR)
        data = struct.pack('>I', sn)
        flash.program(CONFIG_ADDRESS, data)

    @property
    def current(self):
        return self._b.current

    @property
    def voltage(self):
        return self._b.voltage

    @property
    def temperature(self):
        if self.temp_tick == None or time.time() - self.temp_tick > 5:
            case = Ain(self._b, 'CASE_THM_ADC')
            while True:
                aval = case.aval
                if (aval > 0.0):
                    break
            self.temp_val = aval
            self.temp_tick = time.time()
        return self.temp_val
