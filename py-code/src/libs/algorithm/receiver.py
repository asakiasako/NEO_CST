import time
from .instrument import safe_set_att

def adjust_att_to_target_rx_input(voa_obj, pm_obj, rx_input_target, precision = 0.05):
    """
    * voa_obj: (TypeVOA) VOA to adjust RX input power
    * pm_obj: (TypePM) PM to monitor RX input power
    * rx_input_target: (int|float) RX input power target
    * precision: (float) the precision to adjust att value of voa object
    * voa_set_delay: delay time after adjust att value of voa_obj
    """
    neg_count = 0
    over_count = 0
    while True:
        curr_rx_input = pm_obj.get_dbm_value()
        rx_input_gap = rx_input_target - curr_rx_input

        if abs(rx_input_gap) >= precision/2:
            if neg_count >= 2:
                raise ValueError(
                    'Rx Input Power could not meet requirement even when ATT = 0. target = %.1f; real = %.1f' % (rx_input_target, curr_rx_input),
                    'ATT_OUT_OF_RANGE',
                    curr_rx_input
                )
            if over_count >= 2:
                raise ValueError(
                    'Rx Input Power could not meet requirement even when ATT = %.1f. target = %.1f; real = %.1f' % (voa_obj.max_att, rx_input_target, curr_rx_input),
                    'ATT_OUT_OF_RANGE',
                    curr_rx_input
                )
            curr_att = voa_obj.get_att()
            target_att = curr_att - rx_input_gap
            if target_att < 0:
                neg_count += 1
                print('neg_count = %d, ATT = %.1f' % (neg_count, target_att))
                target_att = 0
            if target_att > voa_obj.max_att:
                over_count += 1
                print('over_count = %d, ATT = %.1f' % (over_count, target_att))
                target_att = voa_obj.max_att
            safe_set_att(voa_obj, target_att)
        else:
            print('RX => %.2f' % rx_input_target)
            break

def adjust_att_to_target_osnr(voa_obj, osa_obj, osnr_target, positive, precision = 0.05):
    """
    * voa_obj: (TypeVOA) Adjust this VOA to change osnr
    * osa_obj: (TypeOSA) OSNR value is get from this OSA
    * osnr_target: (int|float) OSNR target
    * positive: (bool) if osnr and att value of voa_obj is in positive relation
    * precision: (float) the precision to adjust att value of voa object
    * voa_set_delay: delay time after adjust att value of voa_obj
    """
    neg_count = 0
    over_count = 0
    while True:
        # osnr refresh delay
        osa_obj.sweep(mode='SINGLE')
        time.sleep(1)
        osa_obj.opc
        curr_osnr = float(osa_obj.get_analysis_data().split(',')[-1])
        osnr_gap = osnr_target - curr_osnr
        if abs(osnr_gap) >= precision/2:
            if neg_count >= 2:
                raise ValueError(
                    'OSNR could not meet requirement even when ATT = 0. target = %.1f; real = %.1f' % (osnr_target, curr_osnr),
                    'ATT_OUT_OF_RANGE',
                    curr_osnr
                )
            if over_count >= 2:
                raise ValueError(
                    'OSNR could not meet requirement even when ATT = %.1f. target = %.1f; real = %.1f' % (voa_obj.max_att, osnr_target, curr_osnr),
                    'ATT_OUT_OF_RANGE',
                    curr_osnr
                )
            curr_att = voa_obj.get_att()
            target_att = curr_att + osnr_gap*(1 if positive else -1)
            if target_att < 0:
                neg_count += 1
                print('neg_count = %d, ATT = %.1f' % (neg_count, target_att))
                target_att = 0
            if target_att > voa_obj.max_att:
                over_count += 1
                print('over_count = %d, ATT = %.1f' % (over_count, target_att))
                target_att = voa_obj.max_att
            safe_set_att(voa_obj, target_att)
        else:
            print('OSNR => %.2f' % osnr_target)
            break


def set_osnr(target, osa, att_ase, att_signal, att_rx, opm_rx, method='DualAtt'):

    METHODS = ['DualAtt', 'SignalAtt', 'AseAtt']
    if method not in METHODS:
        raise KeyError('Invalid OSNR searching method: %r' % method)

    old_pin = opm_rx.get_dbm_value()

    if method == 'DualAtt':
        if att_ase.get_att() <= att_signal.get_att():
            try:
                safe_set_att(att_ase, 0.2)
                adjust_att_to_target_osnr(att_signal, osa, target, positive=False)
            except ValueError:
                safe_set_att(att_signal, 0.2)
                adjust_att_to_target_osnr(att_ase, osa, target, positive=True)
        else:
            try:
                safe_set_att(att_signal, 0.2)
                adjust_att_to_target_osnr(att_ase, osa, target, positive=True)
            except ValueError:
                safe_set_att(att_ase, 0.2)
                adjust_att_to_target_osnr(att_signal, osa, target, positive=False)

        adjust_att_to_target_rx_input(att_rx, opm_rx, old_pin)

    elif method == 'AseAtt':
        adjust_att_to_target_osnr(att_ase, osa, target, positive=True)
        adjust_att_to_target_rx_input(att_rx, opm_rx, old_pin)

    elif method == 'SignalAtt':
        adjust_att_to_target_osnr(att_signal, osa, target, positive=False)
        adjust_att_to_target_rx_input(att_rx, opm_rx, old_pin)
