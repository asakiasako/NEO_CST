from libs import config
from libs import trx_modules
from types import MappingProxyType
from .ApiRouter import ApiRouter

SETTINGS_LIST = {
    'TRX__Type': {
        'type': 'select',
        'default': list(trx_modules.TRX_MAP.keys())[0],
        'options': list(trx_modules.TRX_MAP.keys())
    },
    'OSNR__Set-up': {
        'type': 'select',
        'default': 'ATT1 and ATT2',
        'options': ['ATT1 Only', 'ATT2 Only', 'ATT1 and ATT2']
    }
}

def init_settings():
    for key, value in SETTINGS_LIST.items():
        if get_setting_value(key) is None:
            if 'default' in value:
                set_setting_value(key, value['default'])

def list_settings():
    return SETTINGS_LIST

def get_setting_value(key):
    key = key.strip()
    return config.get_config(':setting:{key}'.format(key=key))

def set_setting_value(key, value):
    key = key.strip()
    config.set_config(':setting:{key}'.format(key=key), value)

init_settings()

# :setting
ApiRouter().register_from_map({
    ':setting:get': get_setting_value,
    ':setting:set': set_setting_value,
    ':setting:list': list_settings,
})