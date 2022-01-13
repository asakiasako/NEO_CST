from .input_functions import *
from collections import namedtuple

InputParameterInfo = namedtuple('InputParameterInfo', 'paramName get set check unit')

INPUT_PARAMETERS = [
    InputParameterInfo(paramName='FreqChannel', get=get_frequency_channel, set=set_frequency_channel, check=None, unit=None),
    InputParameterInfo(paramName='Pin', get=get_pin, set=set_pin, check=check_pin, unit='dBm'),
    InputParameterInfo(paramName='ROSNR', get=get_rosnr, set=set_rosnr, check=check_rosnr, unit='dBm'),
    InputParameterInfo(paramName='ExternalExe', get=get_call_external_exe, set=set_call_external_exe, check=None, unit=None),
    # Module A (Tx)
    InputParameterInfo(paramName='[A]FanSpeed', get=None, set=set_fan_speed_generator('A'), check=None, unit='%'),
    InputParameterInfo(paramName='[A]ModuleVcc', get=get_vcc_generator('A'), set=set_vcc_generator('A'), check=None, unit='V'),
    InputParameterInfo(paramName='[A]TxVoaX', get=get_tx_voa_generator('A', 'X'), set=set_tx_voa_generator('A', 'X'), check=None, unit='V'),
    InputParameterInfo(paramName='[A]TxVoaY', get=get_tx_voa_generator('A', 'Y'), set=set_tx_voa_generator('A', 'Y'), check=None, unit='V'),
    InputParameterInfo(paramName='[A]RxVoaX', get=get_rx_voa_generator('A', 'X'), set=set_rx_voa_generator('A', 'X'), check=None, unit='V'),
    InputParameterInfo(paramName='[A]RxVoaY', get=get_rx_voa_generator('A', 'Y'), set=set_rx_voa_generator('A', 'Y'), check=None, unit='V'),
    InputParameterInfo(paramName='[A]DriverVT', get=get_driver_vt_generator('A'), set=set_driver_vt_generator('A'), check=None, unit='V'),
    InputParameterInfo(paramName='[A]DriverVOFE', get=get_driver_vofe_generator('A'), set=set_driver_vofe_generator('A'), check=None, unit='V'),
    InputParameterInfo(paramName='[A]DriverVGC_ALL', get=get_driver_vgc_generator('A', 'ALL'), set=set_driver_vgc_generator('A', 'ALL'), check=None, unit='V'),
    InputParameterInfo(paramName='[A]DriverVGC_XI', get=get_driver_vgc_generator('A', 'XI'), set=set_driver_vgc_generator('A', 'XI'), check=None, unit='V'),
    InputParameterInfo(paramName='[A]DriverVGC_XQ', get=get_driver_vgc_generator('A', 'XQ'), set=set_driver_vgc_generator('A', 'XQ'), check=None, unit='V'),
    InputParameterInfo(paramName='[A]DriverVGC_YI', get=get_driver_vgc_generator('A', 'YI'), set=set_driver_vgc_generator('A', 'YI'), check=None, unit='V'),
    InputParameterInfo(paramName='[A]DriverVGC_YQ', get=get_driver_vgc_generator('A', 'YQ'), set=set_driver_vgc_generator('A', 'YQ'), check=None, unit='V'),
    InputParameterInfo(paramName='[A]RxTiaVOA_ALL', get=get_rx_tia_voa_generator('A', 'ALL'), set=set_rx_tia_voa_generator('A', 'ALL'), check=None, unit='V'),
    InputParameterInfo(paramName='[A]RxTiaVOA_XI', get=get_rx_tia_voa_generator('A', 'XI'), set=set_rx_tia_voa_generator('A', 'XI'), check=None, unit='V'),
    InputParameterInfo(paramName='[A]RxTiaVOA_XQ', get=get_rx_tia_voa_generator('A', 'XQ'), set=set_rx_tia_voa_generator('A', 'XQ'), check=None, unit='V'),
    InputParameterInfo(paramName='[A]RxTiaVOA_YI', get=get_rx_tia_voa_generator('A', 'YI'), set=set_rx_tia_voa_generator('A', 'YI'), check=None, unit='V'),
    InputParameterInfo(paramName='[A]RxTiaVOA_YQ', get=get_rx_tia_voa_generator('A', 'YQ'), set=set_rx_tia_voa_generator('A', 'YQ'), check=None, unit='V'),
    InputParameterInfo(paramName='[A]RxTiaBWH', get=get_rx_tia_bw_generator('A', 'H'), set=set_rx_tia_bw_generator('A', 'H'), check=None, unit='V'),
    InputParameterInfo(paramName='[A]RxTiaBWL', get=get_rx_tia_bw_generator('A', 'L'), set=set_rx_tia_bw_generator('A', 'L'), check=None, unit='V'),
    InputParameterInfo(paramName='[A]PreEmpFilter', get=get_pre_emphasis_generator('A'), set=set_pre_emphasis_generator('A'), check=None, unit=None),
    InputParameterInfo(paramName='[A]TxSkew_HI', get=get_tx_skew_n_generator('A', 0), set=set_tx_skew_n_generator('A', 0), check=None, unit=None),
    InputParameterInfo(paramName='[A]TxSkew_HQ', get=get_tx_skew_n_generator('A', 1), set=set_tx_skew_n_generator('A', 1), check=None, unit=None),
    InputParameterInfo(paramName='[A]TxSkew_VI', get=get_tx_skew_n_generator('A', 2), set=set_tx_skew_n_generator('A', 2), check=None, unit=None),
    InputParameterInfo(paramName='[A]TxSkew_VQ', get=get_tx_skew_n_generator('A', 3), set=set_tx_skew_n_generator('A', 3), check=None, unit=None),
    InputParameterInfo(paramName='[A]RxSkew_H', get=get_rx_skew_n_generator('A', 0), set=set_rx_skew_n_generator('A', 0), check=None, unit=None),
    InputParameterInfo(paramName='[A]RxSkew_V', get=get_rx_skew_n_generator('A', 1), set=set_rx_skew_n_generator('A', 1), check=None, unit=None),
    InputParameterInfo(paramName='[A]DspTxAtt_ALL', get=get_dsp_tx_att_generator('A', 'ALL'), set=set_dsp_tx_att_generator('A', 'ALL'), check=None, unit=None),
    InputParameterInfo(paramName='[A]DspTxAtt_HI', get=get_dsp_tx_att_generator('A', 0), set=set_dsp_tx_att_generator('A', 0), check=None, unit=None),
    InputParameterInfo(paramName='[A]DspTxAtt_HQ', get=get_dsp_tx_att_generator('A', 1), set=set_dsp_tx_att_generator('A', 1), check=None, unit=None),
    InputParameterInfo(paramName='[A]DspTxAtt_VI', get=get_dsp_tx_att_generator('A', 2), set=set_dsp_tx_att_generator('A', 2), check=None, unit=None),
    InputParameterInfo(paramName='[A]DspTxAtt_VQ', get=get_dsp_tx_att_generator('A', 3), set=set_dsp_tx_att_generator('A', 3), check=None, unit=None),
    InputParameterInfo(paramName='[A]MuteDspLineEgress', get=None, set=set_dsp_egress_mute_generator('A'), check=None, unit=None),
    InputParameterInfo(paramName='[A]DspTxAnlAtt_ALL', get=None, set=set_dsp_tx_analog_att_generator('A', 'ALL'), check=None, unit=None),
    InputParameterInfo(paramName='[A]DspTxAnlAtt_HI', get=None, set=set_dsp_tx_analog_att_generator('A', 0), check=None, unit=None),
    InputParameterInfo(paramName='[A]DspTxAnlAtt_HQ', get=None, set=set_dsp_tx_analog_att_generator('A', 1), check=None, unit=None),
    InputParameterInfo(paramName='[A]DspTxAnlAtt_VI', get=None, set=set_dsp_tx_analog_att_generator('A', 2), check=None, unit=None),
    InputParameterInfo(paramName='[A]DspTxAnlAtt_VQ', get=None, set=set_dsp_tx_analog_att_generator('A', 3), check=None, unit=None),
    InputParameterInfo(paramName='[A]MZ_DC_XP', get=get_mz_dc_generator('A', 'XP'), set=set_mz_dc_generator('A', 'XP'), check=None, unit=None),
    InputParameterInfo(paramName='[A]MZ_DC_XI', get=get_mz_dc_generator('A', 'XI'), set=set_mz_dc_generator('A', 'XI'), check=None, unit=None),
    InputParameterInfo(paramName='[A]MZ_DC_XQ', get=get_mz_dc_generator('A', 'XQ'), set=set_mz_dc_generator('A', 'XQ'), check=None, unit=None),
    InputParameterInfo(paramName='[A]MZ_DC_YP', get=get_mz_dc_generator('A', 'YP'), set=set_mz_dc_generator('A', 'YP'), check=None, unit=None),
    InputParameterInfo(paramName='[A]MZ_DC_YI', get=get_mz_dc_generator('A', 'YI'), set=set_mz_dc_generator('A', 'YI'), check=None, unit=None),
    InputParameterInfo(paramName='[A]MZ_DC_YQ', get=get_mz_dc_generator('A', 'YQ'), set=set_mz_dc_generator('A', 'YQ'), check=None, unit=None),
    InputParameterInfo(paramName='[A]RxIQ_PH_X', get=get_rx_iq_ph_generator('A', 'X'), set=set_rx_iq_ph_generator('A', 'X'), check=None, unit=None),
    InputParameterInfo(paramName='[A]RxIQ_PH_Y', get=get_rx_iq_ph_generator('A', 'Y'), set=set_rx_iq_ph_generator('A', 'Y'), check=None, unit=None),
    InputParameterInfo(paramName='[A]ABC_Target_XP', get=get_abc_target_generator('A', 'XP'), set=set_abc_target_generator('A', 'XP'), check=None, unit=None),
    InputParameterInfo(paramName='[A]ABC_Target_XI', get=get_abc_target_generator('A', 'XI'), set=set_abc_target_generator('A', 'XI'), check=None, unit=None),
    InputParameterInfo(paramName='[A]ABC_Target_XQ', get=get_abc_target_generator('A', 'XQ'), set=set_abc_target_generator('A', 'XQ'), check=None, unit=None),
    InputParameterInfo(paramName='[A]ABC_Target_YP', get=get_abc_target_generator('A', 'YP'), set=set_abc_target_generator('A', 'YP'), check=None, unit=None),
    InputParameterInfo(paramName='[A]ABC_Target_YI', get=get_abc_target_generator('A', 'YI'), set=set_abc_target_generator('A', 'YI'), check=None, unit=None),
    InputParameterInfo(paramName='[A]ABC_Target_YQ', get=get_abc_target_generator('A', 'YQ'), set=set_abc_target_generator('A', 'YQ'), check=None, unit=None),
    # Module B (Tx)
    InputParameterInfo(paramName='[B]FanSpeed', get=None, set=set_fan_speed_generator('B'), check=None, unit='%'),
    InputParameterInfo(paramName='[B]ModuleVcc', get=get_vcc_generator('B'), set=set_vcc_generator('B'), check=None, unit='V'),
    InputParameterInfo(paramName='[B]TxVoaX', get=get_tx_voa_generator('B', 'X'), set=set_tx_voa_generator('B', 'X'), check=None, unit='V'),
    InputParameterInfo(paramName='[B]TxVoaY', get=get_tx_voa_generator('B', 'Y'), set=set_tx_voa_generator('B', 'Y'), check=None, unit='V'),
    InputParameterInfo(paramName='[B]RxVoaX', get=get_rx_voa_generator('B', 'X'), set=set_rx_voa_generator('B', 'X'), check=None, unit='V'),
    InputParameterInfo(paramName='[B]RxVoaY', get=get_rx_voa_generator('B', 'Y'), set=set_rx_voa_generator('B', 'Y'), check=None, unit='V'),
    InputParameterInfo(paramName='[B]DriverVT', get=get_driver_vt_generator('B'), set=set_driver_vt_generator('B'), check=None, unit='V'),
    InputParameterInfo(paramName='[B]DriverVOFE', get=get_driver_vofe_generator('B'), set=set_driver_vofe_generator('B'), check=None, unit='V'),
    InputParameterInfo(paramName='[B]DriverVGC_ALL', get=get_driver_vgc_generator('B', 'ALL'), set=set_driver_vgc_generator('B', 'ALL'), check=None, unit='V'),
    InputParameterInfo(paramName='[B]DriverVGC_XI', get=get_driver_vgc_generator('B', 'XI'), set=set_driver_vgc_generator('B', 'XI'), check=None, unit='V'),
    InputParameterInfo(paramName='[B]DriverVGC_XQ', get=get_driver_vgc_generator('B', 'XQ'), set=set_driver_vgc_generator('B', 'XQ'), check=None, unit='V'),
    InputParameterInfo(paramName='[B]DriverVGC_YI', get=get_driver_vgc_generator('B', 'YI'), set=set_driver_vgc_generator('B', 'YI'), check=None, unit='V'),
    InputParameterInfo(paramName='[B]DriverVGC_YQ', get=get_driver_vgc_generator('B', 'YQ'), set=set_driver_vgc_generator('B', 'YQ'), check=None, unit='V'),
    InputParameterInfo(paramName='[B]RxTiaVOA_ALL', get=get_rx_tia_voa_generator('B', 'ALL'), set=set_rx_tia_voa_generator('B', 'ALL'), check=None, unit='V'),
    InputParameterInfo(paramName='[B]RxTiaVOA_XI', get=get_rx_tia_voa_generator('B', 'XI'), set=set_rx_tia_voa_generator('B', 'XI'), check=None, unit='V'),
    InputParameterInfo(paramName='[B]RxTiaVOA_XQ', get=get_rx_tia_voa_generator('B', 'XQ'), set=set_rx_tia_voa_generator('B', 'XQ'), check=None, unit='V'),
    InputParameterInfo(paramName='[B]RxTiaVOA_YI', get=get_rx_tia_voa_generator('B', 'YI'), set=set_rx_tia_voa_generator('B', 'YI'), check=None, unit='V'),
    InputParameterInfo(paramName='[B]RxTiaVOA_YQ', get=get_rx_tia_voa_generator('B', 'YQ'), set=set_rx_tia_voa_generator('B', 'YQ'), check=None, unit='V'),
    InputParameterInfo(paramName='[B]RxTiaBWH', get=get_rx_tia_bw_generator('B', 'H'), set=set_rx_tia_bw_generator('B', 'H'), check=None, unit='V'),
    InputParameterInfo(paramName='[B]RxTiaBWL', get=get_rx_tia_bw_generator('B', 'L'), set=set_rx_tia_bw_generator('B', 'L'), check=None, unit='V'),
    InputParameterInfo(paramName='[B]PreEmpFilter', get=get_pre_emphasis_generator('B'), set=set_pre_emphasis_generator('B'), check=None, unit=None),
    InputParameterInfo(paramName='[B]TxSkew_HI', get=get_tx_skew_n_generator('B', 0), set=set_tx_skew_n_generator('B', 0), check=None, unit=None),
    InputParameterInfo(paramName='[B]TxSkew_HQ', get=get_tx_skew_n_generator('B', 1), set=set_tx_skew_n_generator('B', 1), check=None, unit=None),
    InputParameterInfo(paramName='[B]TxSkew_VI', get=get_tx_skew_n_generator('B', 2), set=set_tx_skew_n_generator('B', 2), check=None, unit=None),
    InputParameterInfo(paramName='[B]TxSkew_VQ', get=get_tx_skew_n_generator('B', 3), set=set_tx_skew_n_generator('B', 3), check=None, unit=None),
    InputParameterInfo(paramName='[B]RxSkew_H', get=get_rx_skew_n_generator('B', 0), set=set_rx_skew_n_generator('B', 0), check=None, unit=None),
    InputParameterInfo(paramName='[B]RxSkew_V', get=get_rx_skew_n_generator('B', 1), set=set_rx_skew_n_generator('B', 1), check=None, unit=None),
    InputParameterInfo(paramName='[B]DspTxAtt_ALL', get=get_dsp_tx_att_generator('B', 'ALL'), set=set_dsp_tx_att_generator('B', 'ALL'), check=None, unit=None),
    InputParameterInfo(paramName='[B]DspTxAtt_HI', get=get_dsp_tx_att_generator('B', 0), set=set_dsp_tx_att_generator('B', 0), check=None, unit=None),
    InputParameterInfo(paramName='[B]DspTxAtt_HQ', get=get_dsp_tx_att_generator('B', 1), set=set_dsp_tx_att_generator('B', 1), check=None, unit=None),
    InputParameterInfo(paramName='[B]DspTxAtt_VI', get=get_dsp_tx_att_generator('B', 2), set=set_dsp_tx_att_generator('B', 2), check=None, unit=None),
    InputParameterInfo(paramName='[B]DspTxAtt_VQ', get=get_dsp_tx_att_generator('B', 3), set=set_dsp_tx_att_generator('B', 3), check=None, unit=None),
    InputParameterInfo(paramName='[B]MuteDspLineEgress', get=None, set=set_dsp_egress_mute_generator('B'), check=None, unit=None),
    InputParameterInfo(paramName='[B]DspTxAnlAtt_ALL', get=None, set=set_dsp_tx_analog_att_generator('B', 'ALL'), check=None, unit=None),
    InputParameterInfo(paramName='[B]DspTxAnlAtt_HI', get=None, set=set_dsp_tx_analog_att_generator('B', 0), check=None, unit=None),
    InputParameterInfo(paramName='[B]DspTxAnlAtt_HQ', get=None, set=set_dsp_tx_analog_att_generator('B', 1), check=None, unit=None),
    InputParameterInfo(paramName='[B]DspTxAnlAtt_VI', get=None, set=set_dsp_tx_analog_att_generator('B', 2), check=None, unit=None),
    InputParameterInfo(paramName='[B]DspTxAnlAtt_VQ', get=None, set=set_dsp_tx_analog_att_generator('B', 3), check=None, unit=None),
    InputParameterInfo(paramName='[B]MZ_DC_XP', get=get_mz_dc_generator('B', 'XP'), set=set_mz_dc_generator('B', 'XP'), check=None, unit=None),
    InputParameterInfo(paramName='[B]MZ_DC_XI', get=get_mz_dc_generator('B', 'XI'), set=set_mz_dc_generator('B', 'XI'), check=None, unit=None),
    InputParameterInfo(paramName='[B]MZ_DC_XQ', get=get_mz_dc_generator('B', 'XQ'), set=set_mz_dc_generator('B', 'XQ'), check=None, unit=None),
    InputParameterInfo(paramName='[B]MZ_DC_YP', get=get_mz_dc_generator('B', 'YP'), set=set_mz_dc_generator('B', 'YP'), check=None, unit=None),
    InputParameterInfo(paramName='[B]MZ_DC_YI', get=get_mz_dc_generator('B', 'YI'), set=set_mz_dc_generator('B', 'YI'), check=None, unit=None),
    InputParameterInfo(paramName='[B]MZ_DC_YQ', get=get_mz_dc_generator('B', 'YQ'), set=set_mz_dc_generator('B', 'YQ'), check=None, unit=None),
    InputParameterInfo(paramName='[B]RxIQ_PH_X', get=get_rx_iq_ph_generator('B', 'X'), set=set_rx_iq_ph_generator('B', 'X'), check=None, unit=None),
    InputParameterInfo(paramName='[B]RxIQ_PH_Y', get=get_rx_iq_ph_generator('B', 'Y'), set=set_rx_iq_ph_generator('B', 'Y'), check=None, unit=None),
    InputParameterInfo(paramName='[B]ABC_Target_XP', get=get_abc_target_generator('B', 'XP'), set=set_abc_target_generator('B', 'XP'), check=None, unit=None),
    InputParameterInfo(paramName='[B]ABC_Target_XI', get=get_abc_target_generator('B', 'XI'), set=set_abc_target_generator('B', 'XI'), check=None, unit=None),
    InputParameterInfo(paramName='[B]ABC_Target_XQ', get=get_abc_target_generator('B', 'XQ'), set=set_abc_target_generator('B', 'XQ'), check=None, unit=None),
    InputParameterInfo(paramName='[B]ABC_Target_YP', get=get_abc_target_generator('B', 'YP'), set=set_abc_target_generator('B', 'YP'), check=None, unit=None),
    InputParameterInfo(paramName='[B]ABC_Target_YI', get=get_abc_target_generator('B', 'YI'), set=set_abc_target_generator('B', 'YI'), check=None, unit=None),
    InputParameterInfo(paramName='[B]ABC_Target_YQ', get=get_abc_target_generator('B', 'YQ'), set=set_abc_target_generator('B', 'YQ'), check=None, unit=None),
]


def set_input_param(param_name, value):
    for i in INPUT_PARAMETERS:
        if i.paramName == param_name:
            i.set(value)
            break
    else:
        raise ValueError('Invalid input param name')


def get_input_param(param_name):
    for i in INPUT_PARAMETERS:
        if i.paramName == param_name:
            if i.get:
                return i.get()
    else:
        raise ValueError('Invalid input param name')


def check_input_param(param_name, target):
    for i in INPUT_PARAMETERS:
        if i.paramName == param_name:
            if not i.check:
                return True
            else:
                return i.check(target)
    else:
        raise ValueError('Invalid input param name')