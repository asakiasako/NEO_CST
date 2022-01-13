from libs import models
from libs import pyinst
from libs import config
from libs import trx_modules
from libs.message import MsgQueue
from .errorlog import loopTestLogger
import time

TRX_CONFIG_FIELDS = [
    'A',
    'B'
]

class __Resources:
    @property
    def local_storage(self):
        return _local_storage

    @property
    def msg_queue(self):
        return _msg_queue

    @property
    def loop_config(self):
        return _loop_config

    @loop_config.setter
    def loop_config(self, value):
        global _loop_config
        _loop_config = value

    @property
    def output_params(self):
        return _output_params

    @output_params.setter
    def output_params(self, value):
        global _output_params
        _output_params = value

    @property
    def instr_res(self):
        return _instr_res

    @property
    def trx(self):
        return _trx

    @property
    def multi_files(self):
        return _multi_files
    # @property
    # def dut(self):
    #     return _dut


RESOURCES = __Resources()

_local_storage = {}
_msg_queue = None
_loop_config = []
_output_params = []
_instr_res = {}
_trx = {}
_multi_files = []
# TODO: below is for code snippet, remove before running
# dut = trx_modules.TRX_MAP['CFP2 DCO Chameleon']()


def load_resources():
    load_msg_queue()
    load_loop_config()
    load_output_params()
    # TODO
    load_instr_resources()
    load_trx()
    load_multi_files()

def load_multi_files():
    global _multi_files
    _multi_files = config.get_config(':loop-test:multiple-param-files') or []
    return _multi_files

def release_resources():
    release_trx()
    release_instr_resources()

def load_msg_queue():
    time.sleep(5)
    global _msg_queue
    _msg_queue = MsgQueue()
    return _msg_queue

def load_loop_config():
    global _loop_config
    _loop_config = config.get_config(':loop-test:loop-config')
    for line in _loop_config:
        if ('mode' not in line) or (not line['mode']):
            line['mode'] = 'reverse' if line.get('reverse', False) else 'obverse'
        if ('cycles' not in line) or (not line['cycles']):
            line['cycles'] = 1
    return _loop_config

def load_output_params():
    global _output_params
    _output_params = config.get_config(':loop-test:output-params')
    return _output_params

def load_trx(stricked=True):
    global _trx
    trx_list = config.get_config(':transceiver:list')
    trx_type = config.get_config(':setting:TRX__Type')
    if not trx_type:
        raise ValueError('Empty TRX Type. Please select in settings.')
    res = {}
    trx_instances = {}
    for name in TRX_CONFIG_FIELDS:
        idx = config.get_config(':transceiver:{name}'.format(name=name))

        try:
            if idx is None:
                raise ValueError('Empty configuration for TRx %r' % name)
            else:
                addr = trx_list[idx-1]['address'].strip()
                if addr in trx_instances:
                    trx = trx_instances[addr]
                else:
                    TypeTRx = trx_modules.TRX_MAP[trx_type]
                    trx = TypeTRx(ip=addr)
                    trx.connect()
                    trx_instances[addr] = trx
                trx_obj = trx
        except Exception:
            if stricked:
                raise ConnectionError('Check transceiver connection failed: %s' % name)
            else:
                trx_obj = EmptyTRx('DUT')
        res[name] = trx_obj
    _trx = res
    return res

def release_trx():
    global _trx
    
    try:
        released = []
        for key, instance in _trx.items():
            if instance:
                if instance not in released:
                    instance.disconnect()
                    released.append(instance)
    except Exception:
        loopTestLogger.exception('Exception on Release DUT')
    finally:
        _trx = None

def load_instr_resources():
    global _instr_res
    # get instrument config from database
    with models.db_app.atomic():
        config_query = models.InstrMapping.select()
        inst_list = ([i.field, i.instr_resource] for i in config_query)
    # check_connection and initialize instruments
    inst_res_dict = {}
    for i in inst_list:
        inst_field = i[0]
        if check_instr_connection(inst_field):
            inst = pyinst.__dict__[i[1].class_name](i[1].resource_name, **i[1].params)
        else:
            inst = None
        inst_res_dict[inst_field] = inst
    _instr_res = inst_res_dict
    return _instr_res

def release_instr_resources():
    global _instr_res
    for ins in _instr_res.values():
        if ins:
            try:
                ins.close()
            except Exception:
                loopTestLogger.exception('Exception release instr: {ins}'.format(ins=ins))
    else:
        _instr_res = {}

class EmptyInstrument:
    def __init__(self, inst_field):
        self.__inst_field = inst_field
    def __getattr__(self, attr_name):
        raise AttributeError('Instrument [{inst}] is not available.'.format(inst=self.__inst_field))


class EmptyTRx:
    def __init__(self, role):
        self.__role = role
    def __getattr__(self, attr_name):
        raise AttributeError('TRx role [{role}] is not available.'.format(role=self.__role))


def check_instr_connection(field):
    try:
        inst = models.InstrMapping.get(models.InstrMapping.field==field)
        with pyinst.__dict__[inst.instr_resource.class_name](inst.instr_resource.resource_name, **inst.instr_resource.params) as inst_obj:
            return inst_obj.check_connection()
    except Exception:
        return False
