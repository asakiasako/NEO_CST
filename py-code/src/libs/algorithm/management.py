import time

def wait_for_module_state(dut, state, timeout):
    start = time.time()
    while True:
        time.sleep(1)
        c_state = dut.get_module_state()
        if c_state == state:
            break
        else:
            if time.time() - start > timeout:
                raise TimeoutError('Wait for {state} timeout: {timeout:d}s'.format(state=state, timeout=timeout))

def wait_for_data_path_state(dut, state, timeout):
    start = time.time()
    while True:
        time.sleep(1)
        c_state = dut.get_data_path_state(1)
        if c_state == state:
            break
        else:
            if time.time() - start > timeout:
                raise TimeoutError('Wait for {state} timeout: {timeout:d}s'.format(state=state, timeout=timeout))
