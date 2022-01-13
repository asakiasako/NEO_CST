from .resources import load_resources, release_resources, RESOURCES
from libs import algorithm
from .inputs import get_input_param, set_input_param, check_input_param
from .outputs import get_output_param
from .hooks import *
from . import test_options
from .errorlog import loopTestLogger
from collections import OrderedDict
import time
import operator
import csv
import os
from paths import get_sub_dir
import threading
import ctypes
from libs import utils
import json
from libs import config
import random

# TODO: for debug use
class DebugMsgQueue:
    def info(self, msg):
        print(msg)

flag_in_test = False
flag_resources_load = False
thread_test_loop = None
progress_corners = [0, 0]
progress_in_corner = [0, 0]

def wait_for_dut_ready(dut, timeout):
    algorithm.management.wait_for_module_state(dut, 'ModuleReady', timeout)

def wait_for_data_path_activated(dut, timeout):
    algorithm.management.wait_for_data_path_state(dut, 'DataPathActivated', timeout)

def multi_test_loop():
    try:
        # set-up
        set_up()
        # load file paths
        multi_files = RESOURCES.multi_files
        msg_queue = RESOURCES.msg_queue
        for file_path in multi_files:
            try:
                msg_queue.info('Start Test File: {file}'.format(file=file_path))
                print('Test: %s' % file_path)
                # load params
                with open(file_path, 'r') as fp:
                    conf = json.load(fp)
                RESOURCES.loop_config = conf['input']
                RESOURCES.output_params = conf['output']
                # test
                test_loop_main()
            except Exception as e:
                msg_queue = RESOURCES.msg_queue
                err_str = 'Test loop aborted for single file: [{errtype}]: {errmsg}'.format(errtype=e.__class__.__name__, errmsg=e.args[0])
                msg_queue.error(err_str)
                loopTestLogger.exception('Test loop aborted')
            finally:
                msg_queue.info('Finished test for this file.')
    except KeyboardInterrupt:
        msg_queue = RESOURCES.msg_queue
        msg_queue.error('Test is aborted by user')
    except Exception as e:
        msg_queue = RESOURCES.msg_queue
        err_str = 'Test loop aborted: [{errtype}]: {errmsg}'.format(errtype=e.__class__.__name__, errmsg=e.args[0])
        msg_queue.error(err_str)
        loopTestLogger.exception('Test loop aborted')
    finally:
        msg_queue = RESOURCES.msg_queue
        msg_queue.info('All Test Finished')
        clean_up()

def test_loop():
    try:
        set_up()
        test_loop_main()
    except KeyboardInterrupt:
        msg_queue = RESOURCES.msg_queue
        msg_queue.error('Test is aborted by user')
    except Exception as e:
        msg_queue = RESOURCES.msg_queue
        err_str = 'Test loop aborted: [{errtype}]: {errmsg}'.format(errtype=e.__class__.__name__, errmsg=e.args[0])
        msg_queue.error(err_str)
        loopTestLogger.exception('Test loop aborted')
    finally:
        msg_queue = RESOURCES.msg_queue
        msg_queue.info('Test Finished')
        clean_up()

def clean_up():
    # execute after all tests are finished
    # or test loop aborted
    release_resources()

def set_up():
    # Excecuted before test run
    load_resources()
    global flag_resources_load
    flag_resources_load = True

    duts = [RESOURCES.trx['A'], RESOURCES.trx['B']]
    msg_queue = RESOURCES.msg_queue
    instr_res = RESOURCES.instr_res

    if test_options.get_test_option('Initial Configuration'):
        # --- Initialize dut ---
        # Dut signal pins
        msg_queue.info('[Init Transceivers]')
        msg_queue.info('Set pins: LPWn->H, RSTn->H')
        for dut in duts:
            dut['LPWn'] = True
            dut['RSTn'] = True
        # Wait for ModuleReady
        ready_timeout = 120
        msg_queue.info('Wait for ModuleReady, timeout={timeout}, started: {started}'.format(timeout=ready_timeout, started=time.strftime('%H:%M:%S', time.localtime())))
        for dut in duts:
            wait_for_dut_ready(dut, ready_timeout)
        msg_queue.info('Success')
        # Disable fw trigger
        msg_queue.info('Disable FW TriggerMonitor')
        for dut in duts:
            dut[127] = 0xFF
            dut[163] = 1
        # Write CDB Password
        msg_queue.info('Write CDB PSW')
        for dut in duts:
            dut.write_cdb_password()
        # Set dsp c-fec generator checker
        # msg_queue.info('Set DSP C-FEC Generator & Checker')
        # for dut in duts:
        #     dut.dsp.SetCoreCfecTestPatternGeneratorConfig(signalType=6, enable=1)
        #     dut.dsp.SetCoreCfecTestPatternCheckerConfig(signalType=6, enable=1)
        # Set dsp pcs generator checker
        msg_queue.info('Set DSP PCS Generator & Checker')
        pcs_direction = test_options.get_test_option('PcsDirection')
        idx_pcs_dir = 1 if pcs_direction == 'Ingress' else 2
        for dut in duts:
            dut.dsp.SetPcsTestPatternGeneratorConfig(4,idx_pcs_dir,1,1)
            dut.dsp.SetPcsTestPatternCheckerConfig(4,idx_pcs_dir,1,1)
        # Clear DataPathDeinit flags
        msg_queue.info('Clear DataPathDeinit')
        for dut in duts:
            dut[0, 0x10, 128] = 0x00
        # Wait for DataPathActivated
        data_path_activate_timeout = 240
        msg_queue.info('Wait for DataPathActivated, timeout={timeout}, started: {started}'.format(timeout=data_path_activate_timeout, started=time.strftime('%H:%M:%S', time.localtime())))
        for dut in duts:
            wait_for_data_path_activated(dut, data_path_activate_timeout)
        msg_queue.info('Success')

        # --- Initialize Instruments ---
        SR = 59.837  # GHz
        msg_queue.info('[Init Instruments]')
        for (key, instr) in instr_res.items():
            msg_queue.info('Init {key}'.format(key=key))
            if key in ['OPM1', 'OPM5']:
                if instr:
                    min_avg_time = instr.min_avg_time
                    instr.set_avg_time(min_avg_time)
            elif key in ['ATT1', 'ATT2', 'ATT3']:
                if instr:
                    instr.enable()
            elif key in ['OSA']:
                if instr:
                    rbw = 0.5 if SR < 43 else 1
                    narea = 2
                    marea = 1
                    osa = instr
                    osa.sweep("STOP")
                    osa.set_auto_zero(False)
                    osa.analysis_setting("WDM", 'TH', '20.00db')
                    osa.analysis_setting("WDM", 'MDIFF', '3.00DB')
                    osa.analysis_setting("WDM", 'DMASK', '-999')
                    osa.analysis_setting("WDM", 'NALGO', 'MFIX')
                    osa.analysis_setting("WDM", 'NAREA', '{:.2f}NM'.format(narea))
                    osa.analysis_setting("WDM", 'MAREA', '{:.2f}NM'.format(marea))
                    osa.analysis_setting("WDM", 'FALGO', '5TH')
                    osa.analysis_setting("WDM", 'NBW', '0.10NM')
                    osa.set_analysis_cat("WDM")
                    osa.setup("BWIDTH:RES", "%.2fNM" % rbw)
                    osa.set_span(10)
                    osa.sweep('SINGLE')
                    osa.auto_analysis(True)
                    osa.set_auto_ref_level(True)
                    msg_queue.info('Zeroing OSA...(wait 30 sec). Perform every 30 minutes')
                    osa.last_zeroed_time = time.time()
                    osa.zero_once()
                    time.sleep(30)
    else:
        osa = instr_res['OSA']
        if osa:
            osa.set_auto_zero(False)
            osa.last_zeroed_time = time.time()


def before_each_test():
    instr_res = RESOURCES.instr_res
    msg_queue = RESOURCES.msg_queue
    # Zero OSA every 30 minutes
    osa = instr_res['OSA']
    if osa:
        if time.time() - osa.last_zeroed_time > 30 * 60:
            msg_queue.info('Zeroing OSA...(wait 30 sec) Perform every 30 minutes')
            osa.last_zeroed_time = time.time()
            osa.zero_once()
            time.sleep(30)

def test_loop_main():
    # get resources
    loop_config = RESOURCES.loop_config
    output_params = RESOURCES.output_params
    msg_queue = RESOURCES.msg_queue
    
    # generate loop config
    loop_info = []
    for line in loop_config:
        param_name = line['loopSelect']
        start = line['start']
        stop = line['stop']
        step = line['step']
        additional = [float(i) for i in line['additional'].split(',')] if (line['additional'] and line['additional'].strip()) else []
        mode = line['mode']
        cycles = line['cycles']
        delay = line['delay']
        # generate param list
        range_values = set(utils.float_range(start, stop, step)) if isinstance(start, (float, int)) and isinstance(stop, (float, int)) and isinstance(step, (float, int)) else set()
        additional_values = set(additional)
        raw_param_values = list(range_values | additional_values)
        raw_param_values.sort()
        param_values = []
        for i in range(cycles):
            if mode == 'obverse':
                param_values.extend(raw_param_values)
            elif mode == 'reverse':
                param_values.extend(reversed(raw_param_values))
            elif mode == 'random':
                random.shuffle(raw_param_values)
                param_values.extend(raw_param_values)
            else:
                raise ValueError('Invalid sequence mode: {mode}'.format(mode=mode))
        loop_info.append({
            'param': param_name,
            'values': param_values,
            'delay': delay,
            'last_idx': None,
            'next_idx': 0,  # start from 0
        })

    # generate file and write headers
    filename = test_options.get_test_option('Result Filename').strip()
    if not filename:
        filename = 'LoopTest'
    result_file_path = os.path.join(get_sub_dir('Result'), time.strftime('{filename}.%Y%m%d%H%M%S.csv'.format(filename=filename), time.localtime()))
    headers = []
    headers.extend(['{param}_IT'.format(param=i['param']) for i in loop_info])
    headers.extend(['{param}_IM'.format(param=i['param']) for i in loop_info])
    headers.extend(['{param}_O'.format(param=i) for i in output_params])
    headers.extend(['start', 'end'])
    with open(result_file_path, 'a', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
    
    total_corners = 1
    for i in loop_info:
        total_corners *= len(i['values'])
    progress_corners[1] = total_corners
    msg_queue.info('[Test Start] Total Corners: {total_corners:d}'.format(total_corners=total_corners))
    curr_corner_idx = 0

    end_loop = False    # flag to end the outer loop when all corners are tested
    input_target_values = OrderedDict.fromkeys([i['param'] for i in loop_info], None)
    while True:
        # --- set loop ---
        if end_loop:
            break
        # set param value if they changed, in given sequence, log target and monitored values
        curr_corner_idx += 1
        current_corner = [(i['param'], i['values'][i['next_idx']]) for i in loop_info]
        # clear local storage before new loop
        RESOURCES.local_storage.clear()
        corner_start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        s_current_corner = '[Corner]' + ', '.join(['{param}={value}'.format(param=i[0], value=i[1]) for i in current_corner])
        msg_queue.info(s_current_corner)
        msg_queue.info('Start at: {start}'.format(start=corner_start_time))
        for info in loop_info:
            param, values, delay, last_idx, next_idx = operator.itemgetter('param', 'values', 'delay', 'last_idx', 'next_idx')(info)
            if next_idx != last_idx or (not check_input_param(param, target)):  # check param if target not changed
                target = values[next_idx]
                msg_queue.info('Set input: {param}->{value}'.format(param=param, value=target))
                set_input_param(param, target)
                input_target_values[param] = target
                # delay
                msg_queue.info('Delay: {delay} seconds'.format(delay=delay))
                if delay:
                    start_delay_at = time.time()
                    while True:
                        time.sleep(0.1)
                        if time.time() - start_delay_at >= delay:
                            break
            info['last_idx'] = next_idx
        # change next idx, from inner to outer
        for info in reversed(loop_info):
            param, values, delay, last_idx, next_idx = operator.itemgetter('param', 'values', 'delay', 'last_idx', 'next_idx')(info)
            if next_idx + 1 < len(values):
                next_idx += 1
                info['next_idx'] = next_idx
                break
            else:
                next_idx = 0
                info['next_idx'] = next_idx
        else:
            # if every level has finished iteration, then mark as end
            end_loop = True

        # --- get output param ---
        msg_queue.info('Set input parameters success. Now measuring outputs.')
        msg_queue.info('[Outputs] {outputs}'.format(outputs=', '.join(output_params)))
        result = {}
        total_output_number = len(output_params)
        progress_in_corner[1] = total_output_number
        curr_output_idx = 0
        # Read back input params
        input_monitor_values = OrderedDict.fromkeys([i['param'] for i in loop_info], None)
        for param in input_monitor_values:
            try:
                monitored_input = get_input_param(param)
                msg_queue.info('Read back input: {param}={value}'.format(param=param, value=monitored_input))
                input_monitor_values[param] = monitored_input
            except Exception as e:
                msg_queue.warn('Read back input {param} ERROR: [{errtype}] {errmsg}'.format(param=param, errtype=e.__class__.__name__, errmsg=e.args[0]))
                loopTestLogger.exception('Exception on reading back input param: {param}'.format(param=i))
        for i in output_params:
            curr_output_idx += 1
            # before each test
            before_each_test()
            try:
                result[i] = i_res = get_output_param(param_name=i)
                msg_queue.info('Get: {param}={value}'.format(param=i, value=i_res))
            except Exception as e:
                result[i] = None
                msg_queue.warn('Get {param} ERROR: [{errtype}] {errmsg}'.format(param=i, errtype=e.__class__.__name__, errmsg=e.args[0]))
                loopTestLogger.exception('Exception on output param: {param}'.format(param=i))
            finally:
                # update progress in corner
                progress_in_corner[0] += 1
        corner_end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        # update progress
        progress_corners[0] += 1
        progress_in_corner[0] = 0
        # write to result
        dataline = []
        dataline.extend(input_target_values.values())
        dataline.extend(input_monitor_values.values())
        dataline.extend(result.values())
        dataline.extend([corner_start_time, corner_end_time])
        with open(result_file_path, 'a', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(dataline)


def run_test():
    global flag_in_test, thread_test_loop, progress_corners, progress_in_corner
    progress_corners = [0, 0]
    progress_in_corner = [0, 0]
    flag_in_test = True
    thread_test_loop = threading.Thread(target=test_loop, daemon=True)
    thread_monitor = threading.Thread(target=test_thread_monitor, daemon=True)
    thread_test_loop.start()
    thread_monitor.start()


def run_multi_files_test():
    global flag_in_test, thread_test_loop, progress_corners, progress_in_corner
    progress_corners = [0, 0]
    progress_in_corner = [0, 0]
    flag_in_test = True
    thread_test_loop = threading.Thread(target=multi_test_loop, daemon=True)
    thread_monitor = threading.Thread(target=test_thread_monitor, daemon=True)
    thread_test_loop.start()
    thread_monitor.start()


def test_thread_monitor():
    while True:
        global flag_in_test, thread_test_loop, flag_resources_load
        time.sleep(1)
        if not (thread_test_loop and thread_test_loop.is_alive()):
            flag_in_test = False
            thread_test_loop = None
            flag_resources_load = False
            break


def is_in_test():
    return flag_in_test

def stop_test():
    """
    Raise async KeyboardInterrupt to stop test loop.
    """
    t = thread_test_loop
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_ulong(t.ident),
        ctypes.py_object(KeyboardInterrupt)
    )
    if res > 1:
        raise RuntimeError('Failed terminating thread: %r with return code: %r' % (t, res))

def get_progress_info():
    return progress_corners, progress_in_corner