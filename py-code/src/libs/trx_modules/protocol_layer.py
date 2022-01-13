from abc import ABC, abstractmethod


class TrxProtocol(ABC):

    @property
    @abstractmethod
    def dsp(self):
        """
        dsp object
        """

    @property
    @abstractmethod
    def adc_keys(self):
        """
        list adc keys
        """    
        
    @property
    @abstractmethod
    def dac_keys(self):
        """
        list dac keys
        """

    @abstractmethod
    def get_frequency_channel(self, lane):
        """
        * lane: <int> lane
        return:
            * ch_num: <int> channel number
        """

    @abstractmethod
    def set_frequency_channel(self, lane, ch_num):
        """
        * lane: <int> lane
        * ch_num: <int> channel number
        """

    @abstractmethod
    def get_current_frequency(self, lane):
        """
        * lane: <int> lane
        """

    @abstractmethod
    def get_pre_fec_ber_and_uncorrected_codeword(self, duration):
        """
        * duration: <float|int> duration in seconds to get pre-fec ber and uncorrected codeword
        return:
            * <float> pre-fec ber
            * <int> uncorrected codeword
            if data count = 0, then pre-fec ber = 1, uncorrected codeword = -1 (indicates infinite)
        """

    @abstractmethod
    def get_adc(self, key, mode='a'):
        """
        key: <str> key of ADC.
        mode: <str>, 'a'|'d'. a: analog value, d: digital value.
        return: <float|int> analog or digital value of adc.
        """

    @abstractmethod
    def get_dac(self, key, mode='a'):
        """
        key: <str> key of DAC.
        mode: <str>, 'a'|'d'. a: analog value, d: digital value.
        return: <float|int> analog or digital value of dac.
        """

    @abstractmethod
    def set_dac(self, key, value, mode='a'):
        """
        key: <str> key of DAC.
        value: <float|int> analog or digital value
        mode: <str>, 'a'|'d'. a: analog value, d: digital value.
        """

    @abstractmethod
    def get_dpin(self, key):
        """
        key: <str> key of digital pin
        return:
            pin_state: <bool> if pin is digital high
        """

    @abstractmethod
    def set_dpin(self, key, is_high):
        """
        key: <str> key of digital pin
        is_high: <bool> if pin is digital high
        """

    @abstractmethod
    def get_vcc_setting(self):
        """
        return: <float> Vcc setting value
        """

    @abstractmethod
    def get_vcc_monitor(self):
        """
        return: <float> Vcc monitor value
        """

    @abstractmethod
    def set_vcc(self, value):
        """
        value: <int|float> Vcc setting value
        """
    
    @abstractmethod
    def get_icc(self):
        """
        return: <float> Icc monitor
        """

    @abstractmethod
    def get_power_consumption(self):
        """
        return: <float> power consumption
        """
    
    def write_cdb_password(self):
        """
        write cdb password
        """
        