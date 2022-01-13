from libs.config import get_config, set_config
from libs.loop_test.resources import TRX_CONFIG_FIELDS
from libs.loop_test import functions as loop_test_functions
from libs.loop_test import runner
from libs.loop_test import test_options
import json
from .ApiRouter import ApiRouter

def get_loop_list():
    return loop_test_functions.get_loop_list()

def get_loop_config():
    return get_config(':loop-test:loop-config')

def save_loop_config(config):
    set_config(':loop-test:loop-config', config)

def get_output_list():
    return loop_test_functions.get_output_list()

def get_output_params():
    return get_config(':loop-test:output-params')

def save_output_params(params):
    set_config(':loop-test:output-params', params)

def load_params_from_file(file_path):
    with open(file_path, 'r') as fp:
        conf = json.load(fp)
    set_config(':loop-test:loop-config', conf['input'])
    set_config(':loop-test:output-params', conf['output'])

def save_params_to_file(file_path):
    input_params = get_config(':loop-test:loop-config')
    output_params = get_config(':loop-test:output-params')
    with open(file_path, 'w') as fp:
        json.dump({
            'input': input_params,
            'output': output_params
        }, fp)

def select_multiple_param_files(filepaths):
    set_config(':loop-test:multiple-param-files', filepaths)

def get_multiple_param_files():
    return get_config(':loop-test:multiple-param-files')

def get_options_info():
    return test_options.get_test_options_info()

def get_option(key):
    return test_options.get_test_option(key)

def set_option(key, value):
    return test_options.set_test_option(key, value)

def get_trx_config_fields():
    return TRX_CONFIG_FIELDS

def start_test():
    runner.run_test()

def start_multi_test():
    runner.run_multi_files_test()

def get_msg():
    return loop_test_functions.get_from_msg_queue()

def is_running():
    return runner.is_in_test()

def stop_test():
    runner.stop_test()

def get_progress_info():
    return runner.get_progress_info()

# :loop-test
ApiRouter().register_from_map({
    ':loop-test:get-loop-list': get_loop_list,
    ':loop-test:get-loop-config': get_loop_config,
    ':loop-test:save-loop-config': save_loop_config,
    ':loop-test:get-output-list': get_output_list,
    ':loop-test:get-output-params': get_output_params,
    ':loop-test:save-output-params': save_output_params,
    ':loop-test:load-params-from-file': load_params_from_file,
    ':loop-test:save-params-to-file': save_params_to_file,
    ':loop-test:select-multiple-param-files': select_multiple_param_files,
    ':loop-test:get-multiple-param-files': get_multiple_param_files,
    ':loop-test:get-options-info': get_options_info,
    ':loop-test:get-option': get_option,
    ':loop-test:set-option': set_option,
    ':loop-test:get-trx-config-fields': get_trx_config_fields,
    ':loop-test:start-test': start_test,
    ':loop-test:start-multi-test': start_multi_test,
    ':loop-test:get-msg': get_msg,
    ':loop-test:is-running': is_running,
    ':loop-test:stop-test': stop_test,
    ':loop-test:progress': get_progress_info,
})
