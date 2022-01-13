from .resources import RESOURCES
import time
import math
from libs.utils import to_signed
from . import test_options
from libs import algorithm
from libs import config


def cal(val,signed,total_bits,fractional_bits):
    if 's' == signed:
        if val & (1 << (total_bits-1)): #negative
            decode_val = (val - 2**total_bits) / (2**fractional_bits)
        else: #positve
            decode_val = val / (2**fractional_bits)
    elif 'u' == signed:
        decode_val = val / (2**fractional_bits)
    print(decode_val)
    return decode_val


def get_module_sn_generator(trx_role):
    def get_module_sn():
        return RESOURCES.trx[trx_role].get_sn()
    return get_module_sn

def get_module_fw_version_generator(trx_role):
    def get_module_fw_version():
        return RESOURCES.trx[trx_role].get_fw_version()
    return get_module_fw_version

def get_power_consumption_generator(trx_role):
    def get_power_consumption():
        dut = RESOURCES.trx[trx_role]
        return dut.get_power_consumption()
    return get_power_consumption

def get_module_vcc_monitor_generator(trx_role):
    def get_module_vcc_monitor():
        dut = RESOURCES.trx[trx_role]
        return dut[16:17].to_unsigned() * 100 * 10**(-6)
    return get_module_vcc_monitor

def get_module_temperature_monitor_generator(trx_role):
    def get_module_temperature_monitor():
        dut = RESOURCES.trx[trx_role]
        return dut[14:15].to_signed()/256
    return get_module_temperature_monitor

def get_module_tx_power_monitor_generator(trx_role):
    def get_module_tx_power_monitor():
        dut = RESOURCES.trx[trx_role]
        power_in_mw = dut[0, 0x11, 154:155].to_unsigned() * 0.1 * 10**(-3)
        if power_in_mw == 0:
            raise ValueError('Power in mw = 0')
        power_in_dbm = 10 * math.log10(power_in_mw)
        return power_in_dbm
    return get_module_tx_power_monitor

def get_module_rx_power_monitor_generator(trx_role):
    def get_module_rx_power_monitor():
        dut = RESOURCES.trx[trx_role]
        power_in_mw = dut[0, 0x11, 186:187].to_unsigned() * 0.1 * 10**(-3)
        if power_in_mw == 0:
            raise ValueError('Power in mw = 0')
        power_in_dbm = 10 * math.log10(power_in_mw)
        return power_in_dbm
    return get_module_rx_power_monitor

def get_vdm_signal_power_generator(trx_role):
    def get_vdm_signal_power():
        dut = RESOURCES.trx[trx_role]
        return dut.vdm['Rx Sig Power']
    return get_vdm_signal_power

def get_vdm_total_power_generator(trx_role):
    def get_vdm_total_power():
        dut = RESOURCES.trx[trx_role]
        return dut.vdm['Rx Total Power']
    return get_vdm_total_power

def get_vdm_osnr_monitor_generator(trx_role):
    def get_vdm_osnr_monitor():
        dut = RESOURCES.trx[trx_role]
        return dut.vdm['OSNR']
    return get_vdm_osnr_monitor

def get_tx_output_power():
    tx_opm = RESOURCES.instr_res['OPM1']
    return tx_opm.get_dbm_value()

# TX_DRV_VOCM
def get_tx_driver_vocm_generator(trx_role):
    def get_tx_driver_vocm():
        """
        return:
            * vocm: <float>
        """
        dut = RESOURCES.trx[trx_role]
        return dut.get_adc('TX_DRV_VOCM')
    return get_tx_driver_vocm

# TX_DRIVER_PI_XI
# TX_DRIVER_PI_XQ
# TX_DRIVER_PI_YI
# TX_DRIVER_PI_YQ
def get_driver_pi_generator(trx_role, phase):
    def get_driver_pi():
        dut = RESOURCES.trx[trx_role]
        key = 'TX_DRIVER_PI_{phase}'.format(phase=phase)
        return dut.get_adc(key)
    return get_driver_pi

# RX_TIA_PI_XI
# RX_TIA_PI_XQ
# RX_TIA_PI_YI
# RX_TIA_PI_YQ
def get_rx_tia_pi_generator(trx_role, phase):
    def get_rx_tia_pi():
        dut = RESOURCES.trx[trx_role]
        key = 'RX_TIA_PI_{phase}'.format(phase=phase)
        return dut.get_adc(key)
    return get_rx_tia_pi

# ADC_TIA_VGC_YQ
# ADC_TIA_VGC_YI
# ADC_TIA_VGC_XQ
# ADC_TIA_VGC_XI
def get_rx_tia_vgc_generator(trx_role, phase):
    def get_rx_tia_vgc():
        dut = RESOURCES.trx[trx_role]
        key = 'ADC_TIA_VGC_{phase}'.format(phase=phase)
        return dut.get_adc(key)
    return get_rx_tia_vgc


# POST_MPDX_DC_MCU2ADC
# POST_MPDY_DC_MCU2ADC
def get_post_mpd_generator(trx_role, phase):
    def get_post_mpd():
        dut = RESOURCES.trx[trx_role]
        key = 'POST_MPD{phase}_DC_MCU2ADC'.format(phase=phase)
        return dut.get_adc(key)
    return get_post_mpd

# RX_MPD_X_MCU2
# RX_MPD_Y_MCU2
def get_rx_mpd_generator(trx_role, phase):
    def get_rx_mpd():
        dut = RESOURCES.trx[trx_role]
        key = 'RX_MPD_{phase}_MCU2'.format(phase=phase)
        return dut.get_adc(key)
    return get_rx_mpd

# BER
def get_faw_ber_generator(trx_role):
    duration = test_options.get_test_option('FawBER Duration')
    def get_faw_ber():
        dut = RESOURCES.trx[trx_role]
        return dut.get_faw_ber(period=duration)
    return get_faw_ber

def get_cfec_ber_generator(trx_role):
    duration = test_options.get_test_option('C-Fec Duration')
    check_converge = test_options.get_test_option('Check Converge')
    def get_cfec_ber():
        dut = RESOURCES.trx[trx_role]
        if check_converge:
            if dut.ca.GetIngressSmInformation()['state'] != 255:
                dut.ca.ReStartLineIngressDsp(0)
                time.sleep(1)
        return dut.get_cfec_ber(period=duration)
    return get_cfec_ber

# PreAGC ampl
def __get_dsp_rx_pre_agc_amplitude(trx_role):
    storage_key = '{trx_role}_RxPreAgcAmp'.format(trx_role=trx_role)
    if storage_key in RESOURCES.local_storage:
        status = RESOURCES.local_storage[storage_key]
    else:
        dut = RESOURCES.trx[trx_role]
        dsp = dut.dsp
        try:
            dsp.WriteRegister(0x888000b0,0x40100401)
            status = dsp.get_line_ingress_status()
            RESOURCES.local_storage[storage_key] = status
        finally:
            dsp.WriteRegister(0x888000b0,0x40100400)
    return status

def get_dsp_rx_pre_agc_amplitude_generator(trx_role, phase):
    def get_dsp_rx_pre_agc_amplitude():
        status = __get_dsp_rx_pre_agc_amplitude(trx_role)
        key = 'amplitude_{phase}'.format(phase=phase.lower())
        return status[key]
    return get_dsp_rx_pre_agc_amplitude

# MSE
def __get_dsp_mse(trx_role):
    storage_key = '{trx_role}_DspMse'.format(trx_role=trx_role)
    if storage_key in RESOURCES.local_storage:
        status = RESOURCES.local_storage[storage_key]
    else:
        dut = RESOURCES.trx[trx_role]
        dsp = dut.dsp
        status = dsp.get_line_ingress_status()
        RESOURCES.local_storage[storage_key] = status
    return status

def get_dsp_mse_generator(trx_role, phase):
    def get_dsp_mse():
        status = __get_dsp_mse(trx_role)
        if phase == 'AVG':
            mse_vals = (status['mse_hi'], status['mse_hq'], status['mse_vi'], status['mse_vq'])
            return sum(mse_vals)/len(mse_vals)
        else:
            key = 'mse_{phase}'.format(phase=phase.lower())
            return status[key]
    return get_dsp_mse

def __get_rx_angle_average(trx_role):
    storage_key = '{trx_role}_RxAngleAvg'.format(trx_role=trx_role)
    if storage_key in RESOURCES.local_storage:
        status = RESOURCES.local_storage[storage_key]
    else:
        dut = RESOURCES.trx[trx_role]
        ca = dut.ca
        ca.TriggerMonitors()
        ca.TriggerMonitors()
        status = ca.GetLineOpticalChannelMonitorsAll()
        RESOURCES.local_storage[storage_key] = status
    return status

def get_dsp_rx_angle_average_generator(trx_role, phase):
    def get_dsp_rx_angle_average():
        status = __get_rx_angle_average(trx_role)
        key = 'rx_angle_average_{phase}'.format(phase=phase.lower())
        return to_signed(status[key], 2)/(2**8)
    return get_dsp_rx_angle_average

def get_abc_demod_generator(trx_role, phase):
    mapping = {
        'XP': 0,
        'XI': 1,
        'XQ': 2,
        'YP': 3,
        'YI': 4,
        'YQ': 5
    }
    def get_abc_demod():
        idx = mapping[phase]
        dut = RESOURCES.trx[trx_role]
        return dut.abc.curr_demod(idx)
    return get_abc_demod

def __get_corr_and_un_corr(trx_role):
    check_converge = test_options.get_test_option('Check Converge')
    storage_key = '{trx_role}_CorrAndUnCorr'.format(trx_role=trx_role)
    if storage_key in RESOURCES.local_storage:
        status = RESOURCES.local_storage[storage_key]
    else:
        duration = test_options.get_test_option('ErrorCorrDuration')
        dut = RESOURCES.trx[trx_role]
        if check_converge:
            if dut.ca.GetIngressSmInformation()['state'] != 255:
                dut.ca.ReStartLineIngressDsp(0)
                time.sleep(1)
        status = dut.get_corr_and_un_corr(duration)
        RESOURCES.local_storage[storage_key] = status
    return status

def get_uncorrected_codeword_generator(trx_role):
    def get_uncorrected_codeword():
        status = __get_corr_and_un_corr(trx_role)
        return status[1]
    return get_uncorrected_codeword

def get_corrected_ber_generator(trx_role):
    def get_corrected_ber():
        status = __get_corr_and_un_corr(trx_role)
        return status[0]
    return get_corrected_ber

def __get_estimated_ber(trx_role):
    storage_key = '{trx_role}_PreFec'
    if storage_key in RESOURCES.local_storage:
        status = RESOURCES.local_storage[storage_key]
    else:
        duration = test_options.get_test_option('EstimatedDuration')
        ca = RESOURCES.trx[trx_role].ca
        ca.TriggerMonitors()
        time.sleep(duration)
        ca.TriggerMonitors()
        time.sleep(0.15)
        rsp = ca.GetEstimatedPreCfecBer()
        res = {}

        res['staircaise_estimated_ber'] = rsp['staircaise_estimated_ber_mantissa']/(2**12) * 10 ** to_signed(rsp['staircaise_estimated_ber_order_of_magnitude'], 2)
        res['hamming_estimated_ber'] = rsp['hamming_estimated_ber_mantissa']/(2**12) * 10 ** to_signed(rsp['hamming_estimated_ber_order_of_magnitude'], 2)
        status = res
        RESOURCES.local_storage[storage_key] = status
    return status

def get_staircaise_estimated_ber_generator(trx_role):
    def get_staircaise_estimated_ber():
        status = __get_estimated_ber(trx_role)
        if not status:
            raise ValueError('Get PreFec data error')
        return status['staircaise_estimated_ber']
    return get_staircaise_estimated_ber

def get_hamming_estimated_ber_generator(trx_role):
    def get_hamming_estimated_ber():
        status = __get_estimated_ber(trx_role)
        if not status:
            raise ValueError('Get PreFec data error')
        return status['hamming_estimated_ber']
    return get_hamming_estimated_ber

def get_total_estimated_ber_generator(trx_role):
    def get_total_estimated_ber():
        status = __get_estimated_ber(trx_role)
        if not status:
            raise ValueError('Get Estimated BER data error')
        return status['hamming_estimated_ber'] + status['staircaise_estimated_ber']
    return get_total_estimated_ber

def get_pcs_ber_generator(trx_role):
    def get_pcs_ber():
        duration = test_options.get_test_option('PcsBerDuration')
        trx = RESOURCES.trx[trx_role]
        trx.ca.TriggerMonitors()
        time.sleep(duration)
        trx.ca.TriggerMonitors()
        res = trx.ca.GetPcsTestPmatternCheckerStatistics(4,1)
        bit_count = res['accum_bit_count']
        err_count = res['accum_error_count']
        if bit_count <= 0:
            ber = 1
        else:
            ber = err_count/bit_count
        return ber
    return get_pcs_ber

def __get_oma_ch1_data(trx_role):
    # Trace8 = H
    storage_key = '{trx_role}_OmaCh1'
    if storage_key in RESOURCES.local_storage:
        status = RESOURCES.local_storage[storage_key]
    else:
        oma = RESOURCES.instr_res['OMA']
        status = oma.get_trace_data(8)
        RESOURCES.local_storage[storage_key] = status
    return status

def __get_oma_ch2_data(trx_role):
    # Trace11 = K
    storage_key = '{trx_role}_OmaCh2'
    if storage_key in RESOURCES.local_storage:
        status = RESOURCES.local_storage[storage_key]
    else:
        oma = RESOURCES.instr_res['OMA']
        status = oma.get_trace_data(11)
        RESOURCES.local_storage[storage_key] = status
    return status

def get_oma_ch1_generator(trx_role, key):
    def get_param_value():
        return __get_oma_ch1_data(trx_role)[key][0]
    return get_param_value

def get_oma_ch2_generator(trx_role, key):
    def get_param_value():
        return __get_oma_ch2_data(trx_role)[key][0]
    return get_param_value

def get_mz_dc_generator(trx_role, phase):
    def get_mz_dc():
        key = 'MCU2_T{phase}H1_DC'.format(phase=phase)
        dut = RESOURCES.trx[trx_role]
        return dut.get_dac(key)
    return get_mz_dc

def get_osnr_tolerance():
    opm_rx = RESOURCES.instr_res['OPM2']
    voa_rx = RESOURCES.instr_res['ATT3']
    voa_ase = RESOURCES.instr_res['ATT2']
    voa_signal = RESOURCES.instr_res['ATT1']
    osa = RESOURCES.instr_res['OSA']
    dut = RESOURCES.trx['B']
    
    duration = test_options.get_test_option('C-Fec Duration')

    osnr_setup = config.get_config(':setting:OSNR__Set-up')
    if osnr_setup == 'ATT1 and ATT2':
        method = 'DualAtt'
    elif osnr_setup == 'ATT1 Only':
        method = 'SignalAtt'
    elif osnr_setup == 'ATT2 Only':
        method = 'AseAtt'

    osnr_start = test_options.get_test_option('OSNR Tol. Start')
    osnr_stop = test_options.get_test_option('OSNR Tol. Stop')
    osnr_step = test_options.get_test_option('OSNR Tol. Max Step')

    curr_start_point = osnr_start
    curr_step = osnr_step
    the_last_step = False
    while True:
        if curr_step <= 0.1:
            curr_step = 0.1
            the_last_step = True
        
        curr_osnr = curr_start_point
        while True:
            algorithm.receiver.set_osnr(curr_osnr, osa, voa_ase, voa_signal, voa_rx, opm_rx, method=method)
            time.sleep(1)
            cfec = dut.get_cfec_ber(period=duration)
            if cfec:
                if curr_osnr >= osnr_start:
                    raise ValueError('Get cfec BER even at start point: %f' % curr_osnr)
                curr_start_point = curr_osnr + curr_step
                curr_step /= 2
                break
            else:
                if curr_osnr <= osnr_stop:
                    raise ValueError('No cfec BER even when OSNR = %f' % curr_osnr)
                curr_osnr -= curr_step
        if the_last_step:
            break
    
    osnr_tolerance = curr_start_point
    return osnr_tolerance

def get_vofe_current_sen_generator(trx_role):
    def get_vofe_current_sen():
        dut = RESOURCES.trx[trx_role]
        return dut.get_adc('VOFE_CURRENT_SEN')
    return get_vofe_current_sen

def get_avs_voltage_generator(trx_role):
    def get_avs_voltage():
        dut = RESOURCES.trx[trx_role]
        return dut.get_adc('P0V55_DSP_VDDC')
    return get_avs_voltage

def get_dsp_lrx_temp_generator(trx_role):
    def get_dsp_lrx_temp():
        dut = RESOURCES.trx[trx_role]
        return cal(dut[0, 0xFF, 130:131].to_unsigned(), 's', 11, 2)
    return get_dsp_lrx_temp

def get_laser_temperature_monitor_generator(trx_role):
    def get_laser_temperature_monitor():
        dut = RESOURCES.trx[trx_role]
        return dut[20:21].to_signed()/256.0
    return get_laser_temperature_monitor
