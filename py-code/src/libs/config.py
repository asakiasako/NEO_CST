from libs.models import AppConfig
from paths import get_sub_dir
import os
import json


CONFIGS_DIR = get_sub_dir('Configs')
CONFIG_FILE_EXT = 'cfg'
DEFALT_CONFIG_MAP = {
    'PreEmphasisFilter': [
        '[0,0,-0.1,0.7,-0.1,0,0]',
        '[0,0,-0.1,0.9,-0.1,0,0]',
        '[0,0,-0.15,0.7,-0.15,0,0]',
        '[0,0,-0.05,0.7,-0.05,0,0]',
    ],
    'ExternalExe': [
        '"cmd"',
        '"C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"',
    ]
}

def get_config(key):
    config, created = AppConfig.get_or_create(key=key, defaults={'value': None})
    return config.value


def set_config(key, value):
    config, created = AppConfig.get_or_create(key=key, defaults={'value': None})
    config.value = value
    config.save()


def generate_default_config_files():
    for key, data in DEFALT_CONFIG_MAP.items():
        f_path = os.path.join(CONFIGS_DIR, '{fname}.{ext}'.format(fname=key, ext=CONFIG_FILE_EXT))
        if os.path.exists(f_path):
            continue
        else:
            with open(f_path, 'w') as f:
                for idx in range(len(data)):
                    f.write('{line_no}: {line}\n'.format(line_no=idx+1, line=data[idx]))


def load_config_file(key):
    f_path = os.path.join(CONFIGS_DIR, '{fname}.{ext}'.format(fname=key, ext=CONFIG_FILE_EXT))
    conf_dict = {}
    with open(f_path, 'r') as f:
        lines = f.read().strip().split('\n')
    for line in lines:
        s_idx, s_val = line.split(':', 1)
        idx = int(s_idx)
        val = json.loads(s_val)
        conf_dict[idx] = val
    return conf_dict


generate_default_config_files()