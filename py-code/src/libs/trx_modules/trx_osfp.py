from .protocol_layer import TrxProtocol
from .cmis import CMIS, HW_TYPE
from .osfp_low_level_interface.broker import Broker
from .osfp_low_level_interface.canopus import Canopus
from .osfp_low_level_interface.canopus_api import CanopusApi
from .osfp_low_level_interface.ain import Ain
from .osfp_low_level_interface.aout import Aout
from .osfp_low_level_interface.dpin import DPin
from .osfp_low_level_interface.cmis import CMIS as LowLevelCMIS
from .osfp_low_level_interface.cdb import CDB
from .osfp_low_level_interface.abc import ABC
from .osfp_low_level_interface.vdm import VDM
from libs.utils import parse_dsp_api_data
import time


class TrxOSFP(CMIS, TrxProtocol):

    adc_keys = Ain.IDS
    dac_keys = Aout.IDS

    def __init__(self, ip):
        if not isinstance(ip, str):
            raise TypeError('ip should be a str in ip address format')
        CMIS.__init__(self, HW_TYPE.OSFP)
        TrxProtocol.__init__(self)
        self.__broker = Broker(ip=ip, long_term_connection=True)
        self.__dsp = Canopus(self.__broker)
        self.__ca = CanopusApi(self.__dsp)
        self.__cmis = LowLevelCMIS(broker=self.__broker)
        self.__cdb = CDB(self.__broker)
        self.__abc = ABC(self.__broker)
        self.__ip = ip
        self.__cmis_version = None
        self.__vdm = VDM(self.__broker)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def __repr__(self):
        return '<{classname} ip={ip}>'.format(classname=self.__class__.__name__, ip=self.__ip)

    def connect(self):
        self.__broker.open()

    def disconnect(self):
        self.__broker.close()

    @property
    def cmis_version(self):
        return self.__cmis_version or self[1]

    @property
    def broker(self):
        return self.__broker

    @property
    def ca(self):
        return self.__ca

    @property
    def dsp(self):
        return self.__dsp

    @property
    def low_level_cmis(self):
        return self.__cmis

    @property
    def cdb(self):
        return self.__cdb
    
    @property
    def abc(self):
        return self.__abc

    @property
    def vdm(self):
        return self.__vdm

    def set_pin_state(self, pin_name, is_high_level):
        mapping = {
            # pin_name: (d_id, polarization) 
            # polarization True->module pin and source digital value has the same active logic
            'LPWn': (21, False), # "MCU_MOD_LPWN" TODO: this pin is reversed in logic due to issue of current module
            'RSTn': (20, True), # 'MCU_MOD_RSTN'
        }
        pin_id, pol = mapping[pin_name]
        self.__broker.dout_set(pin_id, int(not is_high_level ^ pol))

    def get_pin_state(self, pin_name):
        pin_map = {
            # pin_name: (d_id, category, polarization)
            # polarization True->module pin and source digital value has the same active logic
            'LPWn': (21, 'dout', False),  # 'MCU_MOD_LPWN', pin use confirmed with Ming Su TODO: this pin is reversed in logic due to issue of current module
            'RSTn': (20, 'dout', True),  # 'MCU_MOD_RSTN', pin use confirmed with Ming Su
            'PRSn': (2, 'din', True),  # 'H_PRSN'
            'INT': (1, 'din', False),  # 'H_INTN'
        }
        pin_id, pin_type, pol = pin_map[pin_name]
        if pin_type == 'dout':
            return not bool(self.__broker.dout(pin_id)) ^ pol
        else:
            return not bool(self.__broker.din(pin_id)) ^ pol

    def write_twi_register(self, twi_addr, data, data_len=None):
        """
        random write of twi register.
        twi_addr: a 1-byte bytes. twi register address.
        data: bytes.
        data_len: size of data in bytes. if given, length of param 'data' will be confirmed.
                  otherwise, the length of data is used.
        """
        twi_addr_int = int.from_bytes(twi_addr, 'big')
        if not len(data) == data_len:
            raise ValueError('check data length failed')
        if data_len == 1:
            data = int.from_bytes(data, 'big')
            self.__broker.twi_bw(twi_addr_int, data)
        else:
            data = list(data)
            self.__broker.twi_sbw(twi_addr_int, data)

    def read_twi_register(self, twi_addr, data_len=1):
        """
        random read of twi register
        twi_addr: a 1-byte bytes. twi register address.
        data_len: size of data to read in bytes.
        Returns: bytes
        """
        twi_addr_int = int.from_bytes(twi_addr, 'big')
        if data_len==1:
            return self.__broker.twi_rr(twi_addr_int).to_bytes(data_len, 'big')
        else:
            return self.__broker.twi_srr(twi_addr_int, data_len)

    def get_frequency_channel(self, lane):
        """
        * lane: <int> lane
        return:
            * ch_num: <int> channel number
        """
        return self[0, 0x12, 136+(lane-1)*2:136+(lane-1)*2+1].to_signed()

    def set_frequency_channel(self, lane, ch_num):
        """
        * lane: <int> lane
        * ch_num: <int> channel number
        """
        self[0, 0x12, 136+(lane-1)*2:136+(lane-1)*2+1] = ch_num if ch_num >=0 else ch_num+0x10000

    def get_current_frequency(self, lane):
        """
        * lane: <int> lane
        return:
            * <float> frequency in THz
        """
        if self.cmis_version <= 0x40:
            ms_bytes = (168+4*(lane-1), 169+4*(lane-1))  # THz
            ls_bytes = (170+4*(lane-1), 171+4*(lane-1))  # 0.05GHz
            self.select_bank_page(bank=0, page=0x12)
            freq = self[slice(*ms_bytes)].to_unsigned() + self[slice(*ls_bytes)].to_unsigned()*0.05*10**(-3)
        else:
            self.select_bank_page(bank=0, page=0x12)
            freq = self[168:171].to_unsigned()/1000/1000
        return freq

    def get_pre_fec_ber_and_uncorrected_codeword(self, duration):
        raise NotImplementedError()
    #     """
    #     * duration: <float|int> duration in seconds to get pre-fec ber and uncorrected codeword
    #     return:
    #         * <float> pre-fec ber
    #         * <int> uncorrected codeword
    #         if data count = 0, then pre-fec ber = 1, uncorrected codeword = -1 (indicates infinite)
    #     """
    #     # write cdb psw is required
    #     self.write_cdb_password()

    #     self.dsp.TriggerMonitors()
    #     time.sleep(duration)
    #     self.dsp.TriggerMonitors()
    #     try:
    #         fec_info = self.dsp.ber()
    #         return fec_info['pre-fec-ber'], fec_info['post-fec-cwc']
    #     except ZeroDivisionError:
    #         return 1, -1

    def get_faw_ber(self, period=1):
        self.dsp.TriggerMonitors()
        time.sleep(period)
        self.dsp.TriggerMonitors()
        time.sleep(0.15)
        rsp = self.dsp.get_faw_error_statistics()
        bit_count = rsp['accum_fas_bit_count']
        err_count = rsp['accum_fas_err_count']
        if bit_count:
            return err_count/bit_count
        else:
            return 1

    def get_cfec_ber(self, period=1):
        ca = self.ca
        ca.TriggerMonitors()
        time.sleep(period)
        ca.TriggerMonitors()
        time.sleep(0.15)
        response = ca.GetCoreCfecTestPatternCheckerStatistics()
        bit_count = parse_dsp_api_data(response['accum_bit_count'], 'u', 64, 0)
        error_count = parse_dsp_api_data(response['accum_error_count'], 'u', 64, 0)
        if bit_count:
            return error_count/bit_count
        else:
            return 1

    def get_corr_and_un_corr(self, period=1):
        dsp = self.dsp
        dsp.TriggerMonitors()
        time.sleep(period)
        dsp.TriggerMonitors()
        time.sleep(0.15)
        rsp = dsp.get_error_correction_statistics(4, 1)
        bit_count = rsp['accum_bit_count']
        corr_count = rsp['accum_corrected_error_count']
        uncorr_cw = rsp['accum_uncorrected_codeword_count']
        corr_ber = corr_count/bit_count if bit_count else 1
        return corr_ber, uncorr_cw

    def get_sn(self):
        return self[0, 0x00, 166:181].decode().strip()

    def get_fw_version(self):
        rlplen, rlp_chkcode, rlp = self.cdb.CMD0100h()
        fwStaus = rlp[0]
        img_a_running = fwStaus & 0x01
        if img_a_running:
            ver = '{major}.{minor}'.format(major=rlp[2], minor=rlp[3])
            build = '%d' % ((rlp[4]<<8) | rlp[5])
        else:
            ver = '{major}.{minor}'.format(major=rlp[174-136], minor=rlp[175-136])
            build = '%d' % ((rlp[176-136]<<8) | rlp[177-136])
        return '{ver}.{build}'.format(ver=ver, build=build)

    def get_adc(self, key, mode='a'):
        adc = Ain(self.__broker, key)
        if mode == 'a':
            return adc.aval
        elif mode == 'd':
            return adc.dval
        elif mode == 'r':
            return adc.raw_aval
        elif mode == 'all':
            return adc.aval, adc.dval, adc.raw_aval
        else:
            raise ValueError('Invalid mode.')

    def get_dac(self, key, mode='a'):
        dac = Aout(self.__broker, key)
        if mode == 'a':
            return dac.aval
        elif mode == 'd':
            return dac.dval
        elif mode == 'r':
            return dac.raw_aval
        elif mode == 'all':
            return dac.aval, dac.dval, dac.raw_aval
        else:
            raise ValueError('Invalid mode.')

    def set_dac(self, key, value, mode='a'):
        dac = Aout(self.__broker, key)
        if mode == 'a':
            dac.aval = value
        elif mode == 'd':
            dac.dval = value
        else:
            raise ValueError('Invalid mode.')

    def get_dpin(self, key):
        """
        key: <str> key of digital pin
        return:
            pin_state: <bool> if pin is digital high
        """
        dpin = DPin(self.__broker, key)
        return bool(dpin.state)

    def set_dpin(self, key, is_high):
        """
        key: <str> key of digital pin
        is_high: <bool> if pin is digital high
        """
        dpin = DPin(self.__broker, key)
        dpin.state = int(is_high)

    def get_vcc_setting(self):
        """
        return: <float> Vcc setting value
        """
        return self.__broker.aout(101)[1]  # 'P3V3_OSFP' 

    def get_vcc_monitor(self):
        """
        return: <float> Vcc monitor value
        """
        return self.__broker.ain(102)[1]  # 'P3V3_OSFP_CON'

    def set_vcc(self, value):
        """
        value: <int|float> Vcc setting value
        """
        if not isinstance(value, (int, float)):
            raise TypeError('Vcc value should be a number.')
        if value > 3.8:
            raise ValueError('Vcc setting value over max limit=3.8V')
        self.__broker.aout_set(101, value)  # 'P3V3_OSFP'

    def get_icc(self):
        """
        return: <float> Icc monitor
        """
        return self.__broker.ain(100)[1]  # "P3V3_OSFP_CURR_CHECK"

    def get_power_consumption(self):
        """
        return: <float> power consumption
        """
        return self.get_vcc_monitor() * self.get_icc()

    def write_cdb_password(self):
        self[122:125] = b'\xa5\x5a\x5a\xa5'