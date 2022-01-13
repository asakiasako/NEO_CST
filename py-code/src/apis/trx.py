import time
from libs import config
from libs.trx_modules import TRX_MAP
import math
import struct
from libs.utils import to_signed, parse_dsp_api_data
from contextlib import contextmanager

from .ApiRouter import ApiRouter

@contextmanager
def transceiverGenerator(trx_idx):
    if not isinstance(trx_idx, int):
        if not trx_idx:
            raise ValueError('Please select transceiver.')
    trx_info = config.get_config(':transceiver:list')[trx_idx-1]
    trx_type = config.get_config(':setting:TRX__Type')
    with TRX_MAP[trx_type](trx_info['address']) as trx:
        yield trx

def check_connection(trx_idx):
    if not isinstance(trx_idx, int):
        if not trx_idx:
            raise ValueError('Please select transceiver.')
    trx_info = config.get_config(':transceiver:list')[trx_idx-1]
    trx_type = config.get_config(':setting:TRX__Type')
    available = True
    trx = None
    try:
        trx = TRX_MAP[trx_type](trx_info['address'])
        trx.connect()
        trx.disconnect()
    except Exception:
        available = False
    return available

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

def read_twi_register(trx_idx, addr):
    with transceiverGenerator(trx_idx) as trx:
        return trx[addr]

def write_twi_register(trx_idx, addr, val):
    with transceiverGenerator(trx_idx) as trx:
        trx[addr] = val

def read_twi_register_bit(trx_idx, addr, bit):
    with transceiverGenerator(trx_idx) as trx:
        return trx[addr][bit]

def write_twi_register_bit(trx_idx, addr, bit, state):
    with transceiverGenerator(trx_idx) as trx:
        trx[addr][bit] = state

def read_twi_register_bits(trx_idx, addr, start_bit, stop_bit):
    with transceiverGenerator(trx_idx) as trx:
        return trx[addr][start_bit:stop_bit]

def write_twi_register_bits(trx_idx, addr, start_bit, stop_bit, val): 
    trx_info = config.get_config(':transceiver:list')[trx_idx-1]
    trx_type = config.get_config(':setting:TRX__Type')
    with TRX_MAP[trx_type](trx_info['address']) as trx:
        trx[addr][start_bit:stop_bit] = val

def get_pin_state(trx_idx, pin_name):
    with transceiverGenerator(trx_idx) as trx:
        return trx[pin_name]

def set_pin_state(trx_idx, pin_name, state):
    with transceiverGenerator(trx_idx) as trx:
        trx[pin_name] = state

def sequential_read_registers(trx_idx, start_addr, stop_addr, mode='array'):
    with transceiverGenerator(trx_idx) as trx:
        raw = trx[start_addr:stop_addr]
        if mode == 'array':
            return list(raw)
        elif mode == 'signed':
            return raw.to_signed()
        elif mode == 'unsigned':
            return raw.to_unsigned()

def select_page(trx_idx, page):
    with transceiverGenerator(trx_idx) as trx:
        trx.page = page

def select_bank_page(trx_idx, bank, page):
    with transceiverGenerator(trx_idx) as trx:
        trx.select_bank_page(bank, page)

def write_cdb_password(trx_idx):
    with transceiverGenerator(trx_idx) as trx:
        trx.write_cdb_password()

def get_module_state(trx_idx):
    with transceiverGenerator(trx_idx) as trx:
        return trx.get_module_state()

def get_data_path_state(trx_idx):
    with transceiverGenerator(trx_idx) as trx:
        return trx.get_data_path_state(1)


def call_trx_method(trx_idx, method_name, args=[], kwargs={}):
    with transceiverGenerator(trx_idx) as trx:
        return getattr(trx, method_name)(*args, **kwargs)

def list_adc_keys():
    trx_type = config.get_config(':setting:TRX__Type')
    if not trx_type:
        raise ValueError('Can not get ADC keys. Please select TRX Type in settings.')
    return TRX_MAP[trx_type].adc_keys

def get_adc(trx_idx, key, mode='a'):
    with transceiverGenerator(trx_idx) as trx:
        return trx.get_adc(key, mode)

def list_dac_keys():
    trx_type = config.get_config(':setting:TRX__Type')
    if not trx_type:
        raise ValueError('Can not get DAC keys. Please select TRX Type in settings.')
    return TRX_MAP[trx_type].dac_keys

def get_dac(trx_idx, key, mode='a'):
    with transceiverGenerator(trx_idx) as trx:
        return trx.get_dac(key, mode)

def set_dac(trx_idx, key, value, mode='a'):
    with transceiverGenerator(trx_idx) as trx:
        return trx.set_dac(key, value, mode)

def get_vdm(trx_idx, key):
    with transceiverGenerator(trx_idx) as trx:
        return trx.vdm[key]

def get_ddm_temperature(trx_idx):
    with transceiverGenerator(trx_idx) as trx:
        return trx[14:15].to_signed()/256

def get_ddm_vcc(trx_idx):
    with transceiverGenerator(trx_idx) as trx:
        return trx[16:17].to_unsigned() * 100 * 10**(-6)

def get_ddm_laser_temperature(trx_idx):
    with transceiverGenerator(trx_idx) as trx:
        return trx[20:21].to_signed()/256.0

def get_ddm_tx1_power(trx_idx):
    with transceiverGenerator(trx_idx) as trx:
        power_in_mw = trx[0, 0x11, 154:155].to_unsigned() * 0.1 * 10**(-3)
        if power_in_mw == 0:
            raise ValueError('Power in mw = 0')
        power_in_dbm = 10 * math.log10(power_in_mw)
        return power_in_dbm

def get_ddm_rx1_power(trx_idx):
    with transceiverGenerator(trx_idx) as trx:
        power_in_mw = trx[0, 0x11, 186:187].to_unsigned() * 0.1 * 10**(-3)
        if power_in_mw == 0:
            raise ValueError('Power in mw = 0')
        power_in_dbm = 10 * math.log10(power_in_mw)
        return power_in_dbm

def get_faw_ber(trx_idx, period):
    with transceiverGenerator(trx_idx) as trx:
        if period is None:
            raise TypeError('Please input period (seconds)')
        return trx.get_faw_ber(period)

def get_post_fec_ber(trx_idx, period):
    with transceiverGenerator(trx_idx) as trx:
        if period is None:
            raise TypeError('Please input period (seconds)')
        return trx.get_cfec_ber(period)

def get_rx_signal_power(trx_idx):
    with transceiverGenerator(trx_idx) as trx:
        return trx[0, 0x24, 158:159].to_signed()/100

def get_rx_total_power(trx_idx):
    with transceiverGenerator(trx_idx) as trx:
        return trx[0, 0x24, 160:161].to_signed()/100

def get_vdm_rx_osnr(trx_idx):
    with transceiverGenerator(trx_idx) as trx:
        return trx[0, 0x24, 190:191].to_unsigned()/10

def get_module_active_firmware_version(trx_idx):
    with transceiverGenerator(trx_idx) as trx:
        major = trx[39]
        minor = trx[40]
        return '{major}.{minor}'.format(major=major, minor=minor)

def get_dsp_firmware_version(trx_idx):
    with transceiverGenerator(trx_idx) as trx:
        if not trx.get_module_state() == 'ModuleReady':
            raise ValueError('DSP FW Ver. is only available in ModuleReady state.')
        n_dsp_ver = trx.low_level_cmis.dsp_ver
        dsp_bytes = n_dsp_ver.to_bytes(4, 'big')
        version_str = '.'.join([str(i) for i in dsp_bytes])
        return version_str

def get_module_information(trx_idx):
    with transceiverGenerator(trx_idx) as trx:
        if not trx.get_module_state() == 'ModuleReady':
            raise ValueError('DSP FW Ver. is only available in ModuleReady state.')
        rlplen, rlp_chkcode, rlp = trx.cdb.CMD0100h()
    fwStaus = rlp[0]#136
    result = {}
    result['ImgA Running'] = fwStaus & 0x01  # bit0
    result['ImgA Committed'] = (fwStaus >> 1) & 0x01  # bit1
    result['ImgA Empty'] = (fwStaus >> 2) & 0x01  # bit2
    result['ImgB Running'] = (fwStaus >> 4) & 0x01  # bit4
    result['ImgB Committed'] = (fwStaus >> 5) & 0x01  # bit5
    result['ImgB Empty'] = (fwStaus >> 6) & 0x01  # bit6
    result['ImgA Ver.'] = '{major}.{minor}'.format(major=rlp[2], minor=rlp[3])  # 138, 139
    result['ImgA Build No.'] = '%d' % ((rlp[4]<<8) | rlp[5])
    sub_mcu_imageA_ver = struct.unpack('>I', rlp[6:10])[0]  # 142-145
    result['Sub MCU ImgA Ver.'] = '0x%08X' % sub_mcu_imageA_ver
    result['Sub MCU Running Img'] = '%d' % rlp[10]
    dsp_imageA_ver = struct.unpack('>I', rlp[11:15])[0]  #147-150
    result['DSP ImgA Ver.'] = '0x%08X' % dsp_imageA_ver
    result['ImgB Ver.'] = '{major}.{minor}'.format(major=rlp[174-136], minor=rlp[175-136]) #174,175
    result['ImgB Build No.'] = '%d' % ((rlp[176-136]<<8) | rlp[177-136])  #176,177
    sub_mcu_imageB_ver = struct.unpack('>I', rlp[(178-136):(182-136)])[0]#178-181
    result['Sub MCU ImgB Ver.'] = '0x%08X' % sub_mcu_imageB_ver  #178-181  
    dsp_imageB_ver = struct.unpack('>I', rlp[(182-136):(186-136)])[0]#182-185
    result['DSP ImgB Ver.'] = '0x%08X' % dsp_imageB_ver  #182-185 
    return result

def get_abc_params(trx_idx, pid_idx):
    with transceiverGenerator(trx_idx) as trx:
        abc = trx.abc
        p, i, d, i_min, i_max = abc.pid_get(pid_idx)
        polarity = abc.polarity_get(pid_idx)
        step = abc.step_get(pid_idx)
        method = abc.method_get(pid_idx)
        target = abc.target_get(pid_idx)
        theta = abc.theta_get(pid_idx)
    return p, i, d, i_min, i_max, polarity, step, method, target, theta

def set_abc_params(trx_idx, pid_idx, p, i, d, i_min, i_max, polarity, step, method, target, theta):
    with transceiverGenerator(trx_idx) as trx:
        abc = trx.abc
        abc.pid_set(pid_idx, p, i, d, i_min, i_max)
        abc.polarity_set(pid_idx, polarity)
        abc.step_set(pid_idx, step)
        abc.method_set(pid_idx, method)
        abc.target_set(pid_idx, target)
        abc.theta_set(pid_idx, theta)

def get_abc_service(trx_idx):
    with transceiverGenerator(trx_idx) as trx:
        abc = trx.abc
        return bool(abc.service)

def set_abc_service(trx_idx, is_on):
    with transceiverGenerator(trx_idx) as trx:
        abc = trx.abc
        abc.service = 0x3F if is_on else 0

def get_abc_algo(trx_idx):
    with transceiverGenerator(trx_idx) as trx:
        abc = trx.abc
        return abc.algo  # 0=PID, 1=BUTTERFLY

def set_abc_algo(trx_idx, algo_id):
    with transceiverGenerator(trx_idx) as trx:
        abc = trx.abc
        abc.algo = algo_id  # 0=PID, 1=BUTTERFLY

def get_abc_dither(trx_idx):
    with transceiverGenerator(trx_idx) as trx:
        abc = trx.abc
        return bool(abc.dither)

def set_abc_dither(trx_idx, enable):
    with transceiverGenerator(trx_idx) as trx:
        abc = trx.abc
        abc.dither = int(enable)

def get_abc_settings(trx_idx):
    with transceiverGenerator(trx_idx) as trx:
        abc = trx.abc
        return abc.setting  # freq_idx, ampl, theta, iter

def set_abc_settings(trx_idx, freq_idx, ampl, theta, _iter):
    with transceiverGenerator(trx_idx) as trx:
        abc = trx.abc
        abc.setting = (freq_idx, ampl, theta, _iter)

def get_abc_fine(trx_idx):
    with transceiverGenerator(trx_idx) as trx:
        abc = trx.abc
        raw_fine = abc.fine
        fine = []
        for i in range(6):
            fine.append(bool((raw_fine >> i) & 1))
        return fine

def set_abc_fine(trx_idx, vals):
    with transceiverGenerator(trx_idx) as trx:
        abc = trx.abc
        int_val = 0
        for i in range(6):
            int_val += int(vals[i]) << i
        abc.fine = int_val

def get_abc_target(trx_idx, ph_idx):
    with transceiverGenerator(trx_idx) as trx:
        abc = trx.abc
        return abc.target_get(ph_idx)

def set_abc_target(trx_idx, ph_idx, value):
    with transceiverGenerator(trx_idx) as trx:
        abc = trx.abc
        abc.target_set(ph_idx, value)

def get_abc_demod(trx_idx, ph_idx):
    with transceiverGenerator(trx_idx) as trx:
        abc = trx.abc
        return abc.curr_demod(ph_idx)

def get_abc_theta(trx_idx, ph_idx):
    with transceiverGenerator(trx_idx) as trx:
        abc = trx.abc
        return abc.theta_get(ph_idx)

def set_abc_theta(trx_idx, ph_idx, value):
    with transceiverGenerator(trx_idx) as trx:
        abc = trx.abc
        return abc.theta_set(ph_idx, value)

def set_abc_dither_amplitude(trx_idx, ph_idx, value):
    with transceiverGenerator(trx_idx) as trx:
        abc = trx.abc
        abc.dither_amp_set(ph_idx, value)

def get_abc_dither_amplitude(trx_idx, ph_idx):
    with transceiverGenerator(trx_idx) as trx:
        abc = trx.abc
        return abc.dither_amp_get(ph_idx)

def get_abc_method(trx_idx, ph_idx):
    with transceiverGenerator(trx_idx) as trx:
        abc = trx.abc
        return abc.method_get(ph_idx)

def set_abc_method(trx_idx, ph_idx, value):
    with transceiverGenerator(trx_idx) as trx:
        abc = trx.abc
        return abc.method_set(ph_idx, value)

def set_abc_dither_setting(trx_idx, ch, ph_idx, freq, amplitude):
    with transceiverGenerator(trx_idx) as trx:
        abc = trx.abc
        abc.dither_set(ch, ph_idx, freq, amplitude)

def get_dsp_mse(trx_idx):
    with transceiverGenerator(trx_idx) as trx:
        res = trx.dsp.get_line_ingress_status()
        return {
            'HI': res['mse_hi'],
            'HQ': res['mse_hq'],
            'VI': res['mse_vi'],
            'VQ': res['mse_vq']
        }

def get_pre_agc_amp(trx_idx):
    with transceiverGenerator(trx_idx) as trx:
        dsp = trx.dsp
        dsp.WriteRegister(0x888000b0,0x40100401)
        try:
            res = dsp.get_line_ingress_status()
            return {
                'HI': res['amplitude_hi'],
                'HQ': res['amplitude_hq'],
                'VI': res['amplitude_vi'],
                'VQ': res['amplitude_vq'],
            }
        finally:
            dsp.WriteRegister(0x888000b0,0x40100400)

def get_agc_gain(trx_idx):
    with transceiverGenerator(trx_idx) as trx:
        dsp = trx.ca
        rsp = dsp.GetLineIngressAgcStatus()
    result = {
        'HI': rsp['gain_hi']/2**8,
        'HQ': rsp['gain_hq']/2**8,
        'VI': rsp['gain_vi']/2**8,
        'VQ': rsp['gain_vq']/2**8,
    }
    return result

def get_tx_skew(trx_idx, lane):
    with transceiverGenerator(trx_idx) as trx:
        dsp = trx.dsp
        return dsp.get_line_egress_low_sr_lane_skew(lane)

def set_tx_skew(trx_idx, lane, value):
    with transceiverGenerator(trx_idx) as trx:
        dsp = trx.dsp
        dsp.SetLineEgressLowSrLaneSkew(lane,int(round(value*512))&0xffff)

def get_rx_skew(trx_idx, lane):
    with transceiverGenerator(trx_idx) as trx:
        dsp = trx.dsp
        return dsp.get_line_ingress_skew(lane)

def set_rx_skew(trx_idx, lane, value):
    with transceiverGenerator(trx_idx) as trx:
        dsp = trx.dsp
        value = int(round(value))
        dsp.SetLineIngressSkew(lane, value)

def get_dsp_tx_att(trx_idx, lane):
    with transceiverGenerator(trx_idx) as trx:
        dsp = trx.dsp
        return dsp.get_line_egress_low_sr_lane_attenuation(lane)

def set_dsp_tx_att(trx_idx, lane, value):
    with transceiverGenerator(trx_idx) as trx:
        dsp = trx.dsp
        dsp.SetLineEgressLowSrLaneAttenuation(lane, int(value))

def set_dsp_tx_analog_att(trx_idx, lane, value):
    with transceiverGenerator(trx_idx) as trx:
        ca = trx.ca
        ca.SetLineEgressLaneAnalogAttenuation(lane, value)

def get_cfec_generator(trx_idx):
    with transceiverGenerator(trx_idx) as trx:
        dsp = trx.dsp
        rsp = dsp.GetCoreCfecTestPatternGeneratorConfig()
        pattern_idx = rsp[4]
        enable = bool(rsp[5])
    return pattern_idx, enable

def set_cfec_generator(trx_idx, pattern_idx, enable):
    """
    Pattern index:
    PRBS7: 0
    PRBS9: 1
    PRBS11: 2
    PRBS13: 3
    PRBS15: 4
    PRBS23: 5
    PRBS31: 6
    """
    with transceiverGenerator(trx_idx) as trx:
        dsp = trx.dsp
        dsp.SetCoreCfecTestPatternGeneratorConfig(signalType=pattern_idx, enable=int(enable))

def get_cfec_checker(trx_idx):
    with transceiverGenerator(trx_idx) as trx:
        dsp = trx.dsp
        rsp = dsp.GetCoreCfecTestPatternCheckerConfig()
        pattern_idx = rsp[4]
        enable = bool(rsp[5])
    return pattern_idx, enable

def set_cfec_checker(trx_idx, pattern_idx, enable):
    """
    Pattern index:
    PRBS7: 0
    PRBS9: 1
    PRBS11: 2
    PRBS13: 3
    PRBS15: 4
    PRBS23: 5
    PRBS31: 6
    """
    with transceiverGenerator(trx_idx) as trx:
        dsp = trx.dsp
        dsp.SetCoreCfecTestPatternCheckerConfig(signalType=pattern_idx, enable=int(enable))

def S92DeCal(val):
    if val >= 512:
        return 0
    if val >= 256:
        return (val - 512) / 128
    else:
        return val / 128

def get_dsp_fir_filter(trx_idx, lane):
    with transceiverGenerator(trx_idx) as trx:
        ca = trx.ca
        res = ca.GetLineEgressLowSrFilterCoefficients(lane)
        return [ S92DeCal(res['coefficients'][i]) for i in range(7)]
    
def set_dsp_fir_filter(trx_idx, lane, values):
    with transceiverGenerator(trx_idx) as trx:
        coefs = [int(i*128)&0x1FF for i in values]
        dsp = trx.dsp
        dsp.SetLineEgressLowSrFilterCoefficients(lane, coefs)

def set_egress_lane_mute(trx_idx, lane, mute):
    with transceiverGenerator(trx_idx) as trx:
        dsp = trx.dsp
        dsp.SetLineEgressLaneMute(lane, mute)

def get_egress_lane_mute(trx_idx, lane):
    with transceiverGenerator(trx_idx) as trx:
        dsp = trx.dsp
        rsp = dsp.GetLineEgressLaneMute(lane)
        state = bool(rsp[4])
        return state

def get_ingress_agc(trx_idx):
    with transceiverGenerator(trx_idx) as trx:
        dsp = trx.dsp
        return sum([dsp.get_line_ingress_agc_config(lane)['signal_reference'] for lane in range(4)])/4

def set_ingress_agc(trx_idx, value):
    # value: 0~1
    with transceiverGenerator(trx_idx) as trx:
        ca = trx.ca
        set_value = round(value*128)
        for lane in range(4):
            ca.SetLineIngressAgcConfig(lane, signal_reference=set_value, signal_gain=256, signal_max=511, signal_min=0, enable=1)

def get_error_correction_statistics(trx_idx, framer, direction):
    # value: 0~1
    with transceiverGenerator(trx_idx) as trx:
        dsp = trx.dsp
        dsp.TriggerMonitors()
        dsp.TriggerMonitors()
        time.sleep(0.15)
        rsp = dsp.get_error_correction_statistics(framer, direction)
        return rsp

def get_pre_fec_ber(trx_idx):
    with transceiverGenerator(trx_idx) as trx:
        ca = trx.ca
        ca.TriggerMonitors()
        ca.TriggerMonitors()
        time.sleep(0.15)
        rsp = ca.GetEstimatedPreCfecBer()
    res = {}
    res['staircaise_estimated_ber'] = rsp['staircaise_estimated_ber_mantissa']/(2**12) * 10 ** to_signed(rsp['staircaise_estimated_ber_order_of_magnitude'],2)
    res['hamming_estimated_ber'] = rsp['hamming_estimated_ber_mantissa']/(2**12) * 10 ** to_signed(rsp['hamming_estimated_ber_order_of_magnitude'], 2)
    return res

def get_dsp_die_temperature(trx_idx):
    with transceiverGenerator(trx_idx) as trx:
        hrx2 = cal(trx[0, 0xFF, 128:129].to_unsigned(), 's', 11, 2)
        lrx = cal(trx[0, 0xFF, 130:131].to_unsigned(), 's', 11, 2)
        ltx_v = cal(trx[0, 0xFF, 132:133].to_unsigned(), 's', 11, 2)
        htx_top0 = cal(trx[0, 0xFF, 134:135].to_unsigned(), 's', 11, 2)
        return hrx2, lrx, ltx_v, htx_top0

def get_core_cfec_test_pattern_checker_statistics(trx_idx):
    with transceiverGenerator(trx_idx) as trx:
        ca = trx.ca
        ca.TriggerMonitors()
        ca.TriggerMonitors()
        time.sleep(0.15)
        response = ca.GetCoreCfecTestPatternCheckerStatistics()
        bit_count = parse_dsp_api_data(response['accum_bit_count'], 'u', 64, 0)
        error_count = parse_dsp_api_data(response['accum_error_count'], 'u', 64, 0)
        return bit_count, error_count

def enable_pcs_generator(trx_idx, direction):
    with transceiverGenerator(trx_idx) as trx:
        trx.ca.SetPcsTestPatternGeneratorConfig(4,direction,1,1)

def enable_pcs_checker(trx_idx, direction):
    with transceiverGenerator(trx_idx) as trx:
        trx.ca.SetPcsTestPatternCheckerConfig(4,direction,1,1)

def get_pcs_checker_statistics(trx_idx):
    with transceiverGenerator(trx_idx) as trx:
        trx.ca.TriggerMonitors()
        trx.ca.TriggerMonitors()
        time.sleep(0.15)
        res = trx.ca.GetPcsTestPatternCheckerStatistics(4,1)
        return res['accum_bit_count'], res['accum_error_count']

def get_data_path_deinit(trx_idx):
    with transceiverGenerator(trx_idx) as trx:
        return bool(trx[0, 0x10, 128][0])

def set_data_path_deinit(trx_idx, state):
    with transceiverGenerator(trx_idx) as trx:
        if state:
            value = 0xFF
        else:
            value = 0x00
        trx[0, 0x10, 128] = value

def get_tx_disable(trx_idx):
    with transceiverGenerator(trx_idx) as trx:
        return bool(trx[0, 0x10, 130][0])

def set_tx_disable(trx_idx, state):
    with transceiverGenerator(trx_idx) as trx:
        if state:
            value = 0xFF
        else:
            value = 0x00
        trx[0, 0x10, 130] = value

def get_channel_number(trx_idx):
    with transceiverGenerator(trx_idx) as trx:
        return trx.get_frequency_channel(1)

def set_channel_number(trx_idx, ch_num):
    with transceiverGenerator(trx_idx) as trx:
        trx.set_frequency_channel(1, ch_num)

def get_grid_spacing(trx_idx):
    with transceiverGenerator(trx_idx) as trx:
        return trx[0, 0x12, 128][7:4]

def set_grid_spacing(trx_idx, value):
    with transceiverGenerator(trx_idx) as trx:
        trx[0, 0x12, 128] = value

def get_fine_tune_enable(trx_idx):
    with transceiverGenerator(trx_idx) as trx:
        return bool(trx[0, 0x12, 128][0])

def set_fine_tune_enable(trx_idx, state):
    with transceiverGenerator(trx_idx) as trx:
        trx[0, 0x12, 128][0] = int(state)

def get_fine_tune_frequency(trx_idx):
    with transceiverGenerator(trx_idx) as trx:
        return trx[0, 0x12, 152:153].to_signed() * 0.001

def set_fine_tune_frequency(trx_idx, value):
    with transceiverGenerator(trx_idx) as trx:
        int_val = round(value * 1000)
        if int_val >= 0:
            comp = int_val
        else:
            comp = int_val + 0xFF
        trx[0, 0x12, 152:153] = comp

def get_current_laser_frequency(trx_idx):
    with transceiverGenerator(trx_idx) as trx:
        return trx.get_current_frequency(1)

def get_setting_voltage(trx_idx):
    with transceiverGenerator(trx_idx) as trx:
        return trx.get_vcc_setting()

def get_monitored_voltage(trx_idx):
    with transceiverGenerator(trx_idx) as trx:
        return trx.get_vcc_monitor()

def set_vcc(trx_idx, value):
    if value is None:
        raise TypeError('Please input voltage value')
    with transceiverGenerator(trx_idx) as trx:
        trx.set_vcc(value)

def get_current(trx_idx):
    with transceiverGenerator(trx_idx) as trx:
        return trx.get_icc()

def get_consumption(trx_idx):
    with transceiverGenerator(trx_idx) as trx:
        return trx.get_power_consumption()

def set_fan_speed(trx_idx, value):
    with transceiverGenerator(trx_idx) as trx:
        trx.broker.set_fan_speed(value)

def get_avs_enable(trx_idx):
    with transceiverGenerator(trx_idx) as trx:
        dsp = trx.dsp
        return bool(dsp.avs)

def set_avs_enable(trx_idx, value):
    with transceiverGenerator(trx_idx) as trx:
        dsp = trx.dsp
        if not isinstance(value, bool):
            raise ValueError('AVS enable status value should be bool')
        dsp.avs = value

def get_avs_ratio(trx_idx):
    with transceiverGenerator(trx_idx) as trx:
        dsp = trx.dsp
        return dsp.ratio/2

def set_avs_ratio(trx_idx, value):
    with transceiverGenerator(trx_idx) as trx:
        dsp = trx.dsp
        dsp.ratio = round(value * 2)

def get_dpin(trx_idx, key):
    with transceiverGenerator(trx_idx) as trx:
        return trx.get_dpin(key)

def set_dpin(trx_idx, key, value):
    with transceiverGenerator(trx_idx) as trx:
        trx.set_dpin(key, value)

# :trx
ApiRouter().register_from_map({
    # transceiver
    ':trx:check-connection': check_connection,
    ':trx:read-twi-register': read_twi_register,
    ':trx:write-twi-register': write_twi_register,
    ':trx:read-twi-register-bit': read_twi_register_bit,
    ':trx:write-twi-register-bit': write_twi_register_bit,
    ':trx:read-twi-register-bits': read_twi_register_bits,
    ':trx:write-twi-register-bits': write_twi_register_bits,
    ':trx:get-pin-state': get_pin_state,
    ':trx:set-pin-state': set_pin_state,
    ':trx:sequential-read-registers': sequential_read_registers,
    ':trx:select-page': select_page,
    ':trx:select-bank-page': select_bank_page,
    ':trx:write-cdb-password': write_cdb_password,
    ':trx:get-module-state': get_module_state,
    ':trx:get-data-path-state': get_data_path_state,
    ':trx:call': call_trx_method,
    # transceiver adc
    ':trx:adc:list': list_adc_keys,
    ':trx:adc:get': get_adc,
    # transceiver dac
    ':trx:dac:list': list_dac_keys,
    ':trx:dac:get': get_dac,
    ':trx:dac:set': set_dac,
    # transceiver monitor
    ':trx:monitor:vdm': get_vdm,
    ':trx:monitor:temperature': get_ddm_temperature,
    ':trx:monitor:vcc': get_ddm_vcc,
    ':trx:monitor:laser-temperature': get_ddm_laser_temperature,
    ':trx:monitor:tx1-power': get_ddm_tx1_power,
    ':trx:monitor:rx1-power': get_ddm_rx1_power,
    ':trx:monitor:faw-ber': get_faw_ber,
    ':trx:monitor:post-fec-ber': get_post_fec_ber,
    ':trx:monitor:rx-signal-power': get_rx_signal_power,
    ':trx:monitor:rx-total-power': get_rx_total_power,
    ':trx:monitor:rx-osnr': get_vdm_rx_osnr,
    # transceiver information
    ':trx:information:module-active-firmware-version': get_module_active_firmware_version,
    ':trx:information:module-information': get_module_information,
    ':trx:information:dsp-firmware-version': get_dsp_firmware_version,
    # abc
    ':trx:abc:get-params': get_abc_params,
    ':trx:abc:set-params': set_abc_params,
    ':trx:abc:get-service-state': get_abc_service,
    ':trx:abc:set-service-state': set_abc_service,
    ':trx:abc:get-algo': get_abc_algo,
    ':trx:abc:set-algo': set_abc_algo,
    ':trx:abc:get-dither-state': get_abc_dither,
    ':trx:abc:set-dither-state': set_abc_dither,
    ':trx:abc:get-settings': get_abc_settings,
    ':trx:abc:set-settings': set_abc_settings,
    ':trx:abc:get-fine': get_abc_fine,
    ':trx:abc:set-fine': set_abc_fine,
    ':trx:abc:get-target': get_abc_target,
    ':trx:abc:set-target': set_abc_target,
    ':trx:abc:get-demod': get_abc_demod,
    ':trx:abc:get-theta': get_abc_theta,
    ':trx:abc:set-theta': set_abc_theta,
    ':trx:abc:set-dither-amplitude': set_abc_dither_amplitude,
    ':trx:abc:get-dither-amplitude': get_abc_dither_amplitude,
    ':trx:abc:get-method': get_abc_method,
    ':trx:abc:set-method': set_abc_method,
    ':trx:abc:set-dither-setting': set_abc_dither_setting,
    # dsp
    ':trx:dsp:get-mse': get_dsp_mse,
    ':trx:dsp:get-pre-agc-amp': get_pre_agc_amp,
    ':trx:dsp:get-agc-gain': get_agc_gain,
    ':trx:dsp:get-tx-skew': get_tx_skew,
    ':trx:dsp:set-tx-skew': set_tx_skew,
    ':trx:dsp:get-rx-skew': get_rx_skew,
    ':trx:dsp:set-rx-skew': set_rx_skew,
    ':trx:dsp:get-dsp-tx-att': get_dsp_tx_att,
    ':trx:dsp:set-dsp-tx-att': set_dsp_tx_att,
    ':trx:dsp:set-dsp-tx-analog-att': set_dsp_tx_analog_att,
    ':trx:dsp:get-cfec-checker': get_cfec_checker,
    ':trx:dsp:set-cfec-checker': set_cfec_checker,
    ':trx:dsp:get-cfec-generator': get_cfec_generator,
    ':trx:dsp:set-cfec-generator': set_cfec_generator,
    ':trx:dsp:enable-pcs-pattern-generator': enable_pcs_generator,
    ':trx:dsp:enable-pcs-pattern-checker': enable_pcs_checker,
    ':trx:dsp:get-pcs-test-pattern-checker-statistics': get_pcs_checker_statistics,
    ':trx:dsp:get-dsp-fir-filter': get_dsp_fir_filter,
    ':trx:dsp:set-dsp-fir-filter': set_dsp_fir_filter,
    ':trx:dsp:set-egress-lane-mute': set_egress_lane_mute,
    ':trx:dsp:get-egress-lane-mute': get_egress_lane_mute,
    ':trx:dsp:get-ingress-agc': get_ingress_agc,
    ':trx:dsp:set-ingress-agc': set_ingress_agc,
    ':trx:dsp:get-error-correction-statistics': get_error_correction_statistics,
    ':trx:dsp:get-pre-fec-ber': get_pre_fec_ber,
    ':trx:dsp:get-die-temperature': get_dsp_die_temperature,
    ':trx:dsp:get-core-cfec-test-pattern-checker-statistics': get_core_cfec_test_pattern_checker_statistics,
    # data-path
    ':trx:data-path:get-deinit': get_data_path_deinit,
    ':trx:data-path:set-deinit': set_data_path_deinit,
    ':trx:data-path:get-tx-disable': get_tx_disable,
    ':trx:data-path:set-tx-disable': set_tx_disable,
    # laser-control
    ':trx:laser-control:get-channel-number': get_channel_number,
    ':trx:laser-control:set-channel-number': set_channel_number,
    ':trx:laser-control:get-grid-spacing': get_grid_spacing,
    ':trx:laser-control:set-grid-spacing': set_grid_spacing,
    ':trx:laser-control:get-fine-tune-enable': get_fine_tune_enable,
    ':trx:laser-control:set-fine-tune-enable': set_fine_tune_enable,
    ':trx:laser-control:get-fine-tune-frequency': get_fine_tune_frequency,
    ':trx:laser-control:set-fine-tune-frequency': set_fine_tune_frequency,
    ':trx:laser-control:get-current-laser-frequency': get_current_laser_frequency,
    # host-board
    ':trx:host-board:get-setting-voltage': get_setting_voltage,
    ':trx:host-board:set-voltage': set_vcc,
    ':trx:host-board:get-monitored-voltage': get_monitored_voltage,
    ':trx:host-board:get-current': get_current,
    ':trx:host-board:get-consumption': get_consumption,
    ':trx:host-board:set-fan-speed': set_fan_speed,
    # avs
    ':trx:avs:get-enable': get_avs_enable,
    ':trx:avs:set-enable': set_avs_enable,
    ':trx:avs:get-ratio': get_avs_ratio,
    ':trx:avs:set-ratio': set_avs_ratio,
    # dpin
    ':trx:dpin:get': get_dpin,
    ':trx:dpin:set': set_dpin,
})