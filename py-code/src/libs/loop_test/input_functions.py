from .resources import RESOURCES
import time
from libs import algorithm
from libs import config
from . import test_options
import json
import subprocess

def set_fan_speed_generator(trx_role):
    def set_fan_speed(value):
        dut = RESOURCES.trx[trx_role]
        dut.broker.set_fan_speed(value)
    return set_fan_speed

def get_vcc_generator(trx_role):
    def get_vcc():
        """
        Get Vcc monitor value.
        """
        return RESOURCES.trx[trx_role].get_vcc_monitor()
    return get_vcc

def set_vcc_generator(trx_role):
    def set_vcc(target):
        """
        Adjust Vcc setting value until Vcc monitor value equals target under a defined accuracy.
        """
        dut = RESOURCES.trx[trx_role]
        accuracy = 0.01
        dut.set_vcc(target)
        max_attempts = 3
        for _ in range(max_attempts):
            time.sleep(0.5)
            monitored = dut.get_vcc_monitor()
            if abs(monitored-target) <= accuracy:
                break
            else:
                gap = target - monitored
                dut.set_vcc(dut.get_vcc_setting()+gap)
    return set_vcc

def get_frequency_channel():
    """
    Get frequency channel number of lane 1.
    """
    ch_a = RESOURCES.trx['A'].get_frequency_channel(1)
    ch_b = RESOURCES.trx['B'].get_frequency_channel(1)
    if ch_a == ch_b:
        return ch_a
    else:
        raise ValueError('Channel number for module A and B are not same.')

def set_frequency_channel(ch_num):
    """
    Set frequency channel of lane 1 and wait until DataPathActivated state.
    Then set all instruments to the target channel.
    """
    ch_num = int(ch_num)
    duts = set([RESOURCES.trx['A'], RESOURCES.trx['B']])
    instr_res = RESOURCES.instr_res
    # DataPathDeinit
    for dut in duts:
        dut[0, 0x10, 128] = 0xFF
    # Wait until DataPathDeactivated
    for dut in duts:
        algorithm.management.wait_for_data_path_state(dut, state='DataPathDeactivated', timeout=10)
    # set channel
    for dut in duts:
        dut.set_frequency_channel(1, ch_num)
        # Cancel DataPathDeinit
        dut[0, 0x10, 128] = 0x00
    # Wait until DataPathActivated
    for dut in duts:
        algorithm.management.wait_for_data_path_state(dut, state='DataPathActivated', timeout=300)
    # Get current frequency from dut
    freq = duts.pop().get_current_frequency(1)

    # Set all instrument channel
    for (key, instr) in instr_res.items():
        try:
            if instr:
                instr.set_frequency(freq)
                if key == 'OTF':
                    filter_bw = test_options.get_test_option('Filter Bandwidth (GHz)')
                    C = 299792.458   # km/s
                    bw_in_nm = C/(freq-filter_bw/2000) - C/(freq+filter_bw/2000)
                    try:
                        instr.set_bandwidth_in_ghz(filter_bw)
                    except NotImplementedError:
                        instr.set_bandwidth(bw_in_nm)
        except Exception:
            raise RuntimeError('Unable to set frequency for instrument: {key}'.format(key=key))

def set_pin(target):
    """
    * target: <int|float> input power value in dBm
    """
    instr_res = RESOURCES.instr_res
    opm_rx = instr_res['OPM2']
    att_rx = instr_res['ATT3']
    algorithm.receiver.adjust_att_to_target_rx_input(att_rx, opm_rx, target)

def get_pin():
    """
    return:
        * pin: <float> input power value in dBm
    """
    time.sleep(0.2)
    instr_res = RESOURCES.instr_res
    opm_rx = instr_res['OPM2']
    return opm_rx.get_dbm_value()

def check_pin(target):
    precision = 0.1  # dBm
    pin = get_pin()
    return abs(pin-target) <= precision


def set_rosnr(target):
    """
    target: <int|float> osnr target in dB
    """
    instr_res = RESOURCES.instr_res
    att_ase = instr_res['ATT2']
    att_signal = instr_res['ATT1']
    osa = instr_res['OSA']
    att_rx = instr_res['ATT3']
    opm_rx = instr_res['OPM2']

    osnr_setup = config.get_config(':setting:OSNR__Set-up')
    if osnr_setup == 'ATT1 and ATT2':
        method = 'DualAtt'
    elif osnr_setup == 'ATT1 Only':
        method = 'SignalAtt'
    elif osnr_setup == 'ATT2 Only':
        method = 'AseAtt'

    algorithm.receiver.set_osnr(target, osa, att_ase, att_signal, att_rx, opm_rx, method=method)

def get_rosnr():
    instr_res = RESOURCES.instr_res
    osa = instr_res['OSA']
    osa.sweep(mode='SINGLE')
    time.sleep(1)
    osa.opc
    return float(osa.get_analysis_data().split(',')[-1])

def check_rosnr(target):
    precision = 0.1
    rosnr = get_rosnr()
    return abs(rosnr-target) <= precision


def set_tx_voa_generator(trx_role, phase):
    def set_tx_voa(value):
        dut = RESOURCES.trx[trx_role]
        key = 'MCU1_TX_VOA_{phase}'.format(phase=phase)
        dut.set_dac(key, value)
    return set_tx_voa

def get_tx_voa_generator(trx_role, phase):
    def get_tx_voa():
        dut = RESOURCES.trx[trx_role]
        key = 'MCU1_TX_VOA_{phase}'.format(phase=phase)
        return dut.get_dac(key)
    return get_tx_voa

def set_rx_voa_generator(trx_role, phase):
    def set_rx_voa(value):
        dut = RESOURCES.trx[trx_role]
        key = 'DAC_RX_VOA_{phase}'.format(phase=phase)
        dut.set_dac(key, value)
    return set_rx_voa

def get_rx_voa_generator(trx_role, phase):
    def get_rx_voa():
        dut = RESOURCES.trx[trx_role]
        key = 'DAC_RX_VOA_{phase}'.format(phase=phase)
        return dut.get_dac(key)
    return get_rx_voa

def set_driver_vt_generator(trx_role):
    def set_driver_vt(a_val):
        # TODO: setup/teardown
        dut = RESOURCES.trx[trx_role]
        dut.set_dac('DRIVER_VT', a_val)
    return set_driver_vt

def get_driver_vt_generator(trx_role):
    def get_driver_vt():
        # TODO: setup/teardown
        dut = RESOURCES.trx[trx_role]
        return dut.get_dac('DRIVER_VT')
    return get_driver_vt

# COSA_VOFE_FB
def set_driver_vofe_generator(trx_role):
    def set_driver_vofe(val):
        dut = RESOURCES.trx[trx_role]
        dut.set_dac('COSA_VOFE_FB', val)
    return set_driver_vofe

def get_driver_vofe_generator(trx_role):
    def get_driver_vofe():
        dut = RESOURCES.trx[trx_role]
        return dut.get_dac('COSA_VOFE_FB')
    return get_driver_vofe

# DRIVER_VGC
def set_driver_vgc_generator(trx_role, phase):
    def set_driver_vgc(value):
        dut = RESOURCES.trx[trx_role]
        if phase == 'ALL':
            keys = ['DRIVER_VGC_XI', 'DRIVER_VGC_XQ', 'DRIVER_VGC_YI', 'DRIVER_VGC_YQ']
            for key in keys:
                dut.set_dac(key, value)
        else:
            key = 'DRIVER_VGC_{phase}'.format(phase=phase)
            dut.set_dac(key, value)
    return set_driver_vgc

def get_driver_vgc_generator(trx_role, phase):
    def get_driver_vgc():
        dut = RESOURCES.trx[trx_role]
        if phase == 'ALL':
            keys = ['DRIVER_VGC_XI', 'DRIVER_VGC_XQ', 'DRIVER_VGC_YI', 'DRIVER_VGC_YQ']
            res = sum(dut.get_dac(key) for key in keys)/4
        else:
            key = 'DRIVER_VGC_{phase}'.format(phase=phase)
            res = dut.get_dac(key)
        return res
    return get_driver_vgc

# DAC_TIA_VOA_YI
# DAC_TIA_VOA_XI
# DAC_TIA_VOA_YQ
# DAC_TIA_VOA_XQ
def set_rx_tia_voa_generator(trx_role, phase):
    def set_rx_tia_voa(value):
        dut = RESOURCES.trx[trx_role]
        if phase == 'ALL':
            keys = ['DAC_TIA_VOA_XI', 'DAC_TIA_VOA_XQ', 'DAC_TIA_VOA_YI', 'DAC_TIA_VOA_YQ']
            for key in keys:
                dut.set_dac(key, value)
        else:
            key = 'DAC_TIA_VOA_{phase}'.format(phase=phase)
            dut.set_dac(key, value)
    return set_rx_tia_voa

def get_rx_tia_voa_generator(trx_role, phase):
    def get_rx_tia_voa():
        dut = RESOURCES.trx[trx_role]
        if phase == 'ALL':
            keys = ['DAC_TIA_VOA_XI', 'DAC_TIA_VOA_XQ', 'DAC_TIA_VOA_YI', 'DAC_TIA_VOA_YQ']
            res = sum(dut.get_dac(key) for key in keys)/4
        else:
            key = 'DAC_TIA_VOA_{phase}'.format(phase=phase)
            res = dut.get_dac(key)
        return res
    return get_rx_tia_voa

# RX_TIA_BWH
# RX_TIA_BWL
def set_rx_tia_bw_generator(trx_role, level):
    def set_rx_tia_bw(value):
        dut = RESOURCES.trx[trx_role]
        key = 'RX_TIA_BW{level}'.format(level=level)
        dut.set_dpin(key, value)
    return set_rx_tia_bw

def get_rx_tia_bw_generator(trx_role, level):
    def get_rx_tia_bw():
        dut = RESOURCES.trx[trx_role]
        key = 'RX_TIA_BW{level}'.format(level=level)
        return dut.get_dpin(key)
    return get_rx_tia_bw

# Pre-emphasis filter
def set_pre_emphasis_generator(trx_role):
    def set_pre_emphasis_filter(config_line_idx):
        try:
            config_dict = config.load_config_file('PreEmphasisFilter')
        except Exception:
            raise ValueError('Config file format error.')
        config_val = config_dict[config_line_idx]
        if len(config_val) != 7:
            raise ValueError('Invalid config value in line {lineno}: should contain 7 numbers.'.format(lineno=config_line_idx))
        coefs = [int(i*128)&0x1FF for i in config_val]
        dsp = RESOURCES.trx[trx_role].dsp
        # get dsp tx att before setting
        atts = []
        for i in range(4):
            atts.append(get_dsp_tx_att_generator(trx_role, i)())
        # 
        dsp.SetLineEgressLowSrFilterCoefficients(0,coefs)
        dsp.SetLineEgressLowSrFilterCoefficients(1,coefs)
        dsp.SetLineEgressLowSrFilterCoefficients(2,coefs)
        dsp.SetLineEgressLowSrFilterCoefficients(3,coefs)
        # set back dsp tx att
        for i in range(4):
            set_dsp_tx_att_generator(trx_role, i)(atts[i])
    return set_pre_emphasis_filter

def S92DeCal(val):
    if val >= 512:
        return 0
    if val >= 256:
        return (val - 512) / 128
    else:
        return val / 128

def get_pre_emphasis_generator(trx_role):
    def get_pre_emphasis_filter():
        ca = RESOURCES.trx[trx_role].ca
        rsp = [ca.GetLineEgressLowSrFilterCoefficients(i) for i in range(4)]
        coefs = [
            [ S92DeCal(rsp[0]['coefficients'][i]) for i in range(7)],
            [ S92DeCal(rsp[1]['coefficients'][i]) for i in range(7)],
            [ S92DeCal(rsp[2]['coefficients'][i]) for i in range(7)],
            [ S92DeCal(rsp[3]['coefficients'][i]) for i in range(7)]
        ]
        return json.dumps(coefs)
    return get_pre_emphasis_filter

# Tx Skew
def set_tx_skew_n_generator(trx_role, n):
    def set_tx_skew(val):
        dsp = RESOURCES.trx[trx_role].dsp
        dsp.SetLineEgressLowSrLaneSkew(n, int(round(val*512))&0xffff)
    return set_tx_skew

def get_tx_skew_n_generator(trx_role, n):
    def get_tx_skew():
        dsp = RESOURCES.trx[trx_role].dsp
        return dsp.get_line_egress_low_sr_lane_skew(n)
    return get_tx_skew

# Rx Skew
def set_rx_skew_n_generator(trx_role, n):
    def set_rx_skew(val):
        val = int(round(val))
        dsp = RESOURCES.trx[trx_role].dsp
        dsp.SetLineIngressSkew(n, val)
    return set_rx_skew

def get_rx_skew_n_generator(trx_role, n):
    def get_rx_skew():
        dsp = RESOURCES.trx[trx_role].dsp
        return dsp. get_line_ingress_skew(n)
    return get_rx_skew

# DSP MuteEgress
def set_dsp_egress_mute_generator(trx_role):
    def set_dsp_egress_mute(value):
        dsp = RESOURCES.trx[trx_role].dsp
        for lane in range(4):
            value = int(value)
            dsp.SetLineEgressLaneMute(lane, value)
    return set_dsp_egress_mute

# DSP Tx Att
def set_dsp_tx_att_generator(trx_role, n):
    def set_dsp_tx_att(val):
        val = int(round(val))
        dsp = RESOURCES.trx[trx_role].dsp
        if n == 'ALL':
            for i in range(4):
                dsp.SetLineEgressLowSrLaneAttenuation(i, val)
        else:
            dsp.SetLineEgressLowSrLaneAttenuation(n, val)
    return set_dsp_tx_att

def set_dsp_tx_analog_att_generator(trx_role, n):
    def set_dsp_tx_analog_att(val):
        val = int(round(val))
        ca = RESOURCES.trx[trx_role].ca
        if n == 'ALL':
            for i in range(4):
                ca.SetLineEgressLaneAnalogAttenuation(i, val)
        else:
            ca.SetLineEgressLaneAnalogAttenuation(n, val)
    return set_dsp_tx_analog_att

def get_dsp_tx_att_generator(trx_role, n):
    def get_dsp_tx_att():
        dsp = RESOURCES.trx[trx_role].dsp
        if n == 'ALL':
            res = sum(dsp.get_line_egress_low_sr_lane_attenuation(i) for i in range(4))/4
        else:
            res = dsp.get_line_egress_low_sr_lane_attenuation(n)
        return res
    return get_dsp_tx_att

def set_mz_dc_generator(trx_role, phase):
    def set_mz_dc(value):
        key = 'MCU2_T{phase}H1_DC'.format(phase=phase)
        dut = RESOURCES.trx[trx_role]
        dut.set_dac(key, value)
    return set_mz_dc

def get_mz_dc_generator(trx_role, phase):
    def get_mz_dc():
        key = 'MCU2_T{phase}H1_DC'.format(phase=phase)
        dut = RESOURCES.trx[trx_role]
        return dut.get_dac(key)
    return get_mz_dc

def set_rx_iq_ph_generator(trx_role, phase):
    def set_rx_iq_ph(value):
        key = 'DAC_RX_IQ_PH_{phase}'.format(phase=phase)
        dut = RESOURCES.trx[trx_role]
        dut.set_dac(key, value)
    return set_rx_iq_ph

def get_rx_iq_ph_generator(trx_role, phase):
    def get_rx_iq_ph():
        key = 'DAC_RX_IQ_PH_{phase}'.format(phase=phase)
        dut = RESOURCES.trx[trx_role]
        return dut.get_dac(key)
    return get_rx_iq_ph

ABC_PHASE_MAPPING = {
    'XP': 0,
    'XI': 1,
    'XQ': 2,
    'YP': 3,
    'YI': 4,
    'YQ': 5
}

def set_abc_target_generator(trx_role, phase):
    ph_idx = ABC_PHASE_MAPPING[phase]
    def set_abc_target(value):
        dut = RESOURCES.trx[trx_role]
        dut.abc.target_set(ph_idx, value)
    return set_abc_target

def get_abc_target_generator(trx_role, phase):
    ph_idx = ABC_PHASE_MAPPING[phase]
    def get_abc_target():
        dut = RESOURCES.trx[trx_role]
        return dut.abc.target_get(ph_idx)
    return get_abc_target

def set_call_external_exe(value):
    try:
        config_dict = config.load_config_file('ExternalExe')
    except Exception:
        raise ValueError('Config file format error.')
    config_val = config_dict[value]
    r = subprocess.run(config_val)
    RESOURCES.local_storage['external-exe'] = r.returncode

def get_call_external_exe():
    return RESOURCES.local_storage.get('external-exe', None)