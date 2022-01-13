from libs.config import get_config, set_config

# type - number, input, select, bool
# all: default (optional)
# number: precision, min, max, step (optional)
# select: options

OPTIONS = {
    'Initial Configuration': {
        'type': 'bool',
        'default': False
    },
    'Result Filename': {
        'type': 'input',
        'default': 'LoopTest'
    },
    'Filter Bandwidth (GHz)': {
        'type': 'number',
        'default': 100,
        'min': 0,
        'max': 500
    },
    'Check Converge': {
        'type': 'bool',
        'default': False
    },
    'C-Fec Duration': {
        'type': 'number',
        'default': 0,
        'precision': 1,
        'min': 0,
        'max': 60
    },
    'FawBER Duration': {
        'type': 'number',
        'default': 0,
        'precision': 1,
        'min': 0,
        'max': 60
    },
    'ErrorCorrDuration': {
        'type': 'number',
        'default': 0,
        'precision': 1,
        'min': 0,
        'max': 60
    },
    'EstimatedDuration': {
        'type': 'number',
        'default': 0,
        'precision': 1,
        'min': 0,
        'max': 60
    },
    'PcsBerDuration': {
        'type': 'number',
        'default': 0,
        'precision': 1,
        'min': 0,
        'max': 60
    },
    'PcsDirection': {
        'type': 'select',
        'options': ['Ingress', 'Egress']
    },
    'OSNR Tol. Start': {
        'type': 'number',
        'default': 27,
        'precision': 1,
        'min': 20,
        'max': 30
    },
    'OSNR Tol. Stop': {
        'type': 'number',
        'default': 24,
        'precision': 1,
        'min': 20,
        'max': 30
    },
    'OSNR Tol. Max Step': {
        'type': 'number',
        'default': 0.3,
        'precision': 1,
        'min': 0.1
    },
}

def init_test_options():
    for key, info in OPTIONS.items():
        value = info.get('default', None)
        config_key = ':loop-test-options:{key}'.format(key=key)
        set_config(config_key, value)

def set_test_option(key, value):
    if key not in OPTIONS:
        raise KeyError('Invalid key for loop-test options')
    config_key = ':loop-test-options:{key}'.format(key=key)
    set_config(config_key, value)

def get_test_option(key):
    if key not in OPTIONS:
        raise KeyError('Invalid key for loop-test options')
    config_key = ':loop-test-options:{key}'.format(key=key)
    return get_config(config_key)

def get_test_options_info():
    return OPTIONS

init_test_options()
