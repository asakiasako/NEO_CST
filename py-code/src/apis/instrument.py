from libs import models
import time
from libs import pyinst
from libs import algorithm
from logging import getLogger
from libs import config
from .ApiRouter import ApiRouter

INSTR_RES = {}
rpcServerLogger = getLogger('LoopTest')

# ROUTE: resource
def add_instr_res(label, instr_type, model, resource_name, params):
    model_obj = get_model_info(model)
    with models.db_app:
        models.InstrResource.create(
            label=label, instr_type=instr_type, model=model, brand=model_obj[1], class_name=model_obj[2],
            resource_name=resource_name, params=params, details=model_obj[4])

def remove_instr_res(labels):
    """
    Remove instrument resource
    :param labels: <str|list|tuple> label or list|tuple of labels
    """
    if isinstance(labels, str):
        labels = [labels]
    with models.db_app.atomic():
        q = models.InstrMapping.select().join(models.InstrResource).where(models.InstrResource.label << labels)
        # set foreign keys to None before delete resources
        models.InstrMapping.update(instr_resource=None).where(models.InstrMapping.id << q).execute()
        models.InstrResource.delete().where(models.InstrResource.label << labels).execute()

def get_instr_res(labels=None):
    if isinstance(labels, str):
        labels = [labels]
    with models.db_app.atomic():
        instr_query = models.InstrResource.select()
        if labels:
            instr_query = instr_query.where(models.InstrResource.label << labels)
        instr_list = []
        for i in instr_query:
            instr_list = [(i.label, i.instr_type, i.model, i.brand, i.class_name, i.resource_name, i.params, i.details)
                        for i in instr_query]
        return instr_list

def mod_instr_res(label, kwargs):
    if ('model' in kwargs) or ('instr_type' in kwargs):
        raise AttributeError('Model and type should not be changed. Please delete and create a new one')
    with models.db_app:
        query = models.InstrResource.update(**kwargs).where(models.InstrResource.label == label)
        query.execute()

def get_res_by_type(instr_type):
    query = models.InstrResource.select().where(models.InstrResource.instr_type == instr_type)
    return [i.label for i in query]


# ROUTE: lib
def get_model_info(model):
    with models.db_app:
        model_obj = models.InstrLib.get(models.InstrLib.model == model)
    return model_obj.model, model_obj.brand, model_obj.class_name, model_obj.param_list, model_obj.details

def get_type_model_map():
    mod_map = []
    with models.db_app.atomic():
        query = models.InstrType.select()
        for i in query:
            mod_map.append({
                'type': i.name,
                'models': [j.model for j in i.models]
            })
    return mod_map


# ROUTE: mapping
def get_instr_mapping(fields=None):
    if isinstance(fields, str):
        fields = [fields]
    with models.db_app.atomic():
        query = models.InstrMapping.select()
        if fields:
            query = query.where(models.InstrMapping.field << fields)
        instr_mapping = {}
        for i in query:
            instr_mapping[i.field] = {
                'instr_type': i.instr_type,
                'label': i.instr_resource.label if i.instr_resource else '',
                'choices': get_res_by_type(i.instr_type)
            }
    return instr_mapping

def set_instr_mapping(field, label):
    with models.db_app:
        instr, created = models.InstrMapping.get_or_create(field=field)
        instr_res = models.InstrResource.get(models.InstrResource.label == label)
        instr.instr_resource = instr_res
        instr.save()

def check_connection(field):
    try:
        inst = models.InstrMapping.get(models.InstrMapping.field==field)
        with pyinst.__dict__[inst.instr_resource.class_name](inst.instr_resource.resource_name, **inst.instr_resource.params) as inst_obj:
            return inst_obj.check_connection()
    except Exception:
        rpcServerLogger.exception('Connection Failed: %s' % field)
        return False

def connect_instrument(field):
    inst = models.InstrMapping.get(models.InstrMapping.field==field)
    inst_obj = pyinst.__dict__[inst.instr_resource.class_name](inst.instr_resource.resource_name, **inst.instr_resource.params)
    INSTR_RES[field] = inst_obj

def disconnect_instrument(field):
    instr = INSTR_RES.get(field, None)
    if instr:
        instr.close()
        del(INSTR_RES[field])

def call_instr_method(field, method_name, args=[], kwargs={}):
    instr = INSTR_RES.get(field, None)
    if not instr:
        raise ConnectionError('Instr: {instr} is not connected.'.format(instr=field))
    res = getattr(instr, method_name)(*args, **kwargs)
    if isinstance(res, (int, float, bool, str, set, list, tuple, dict)):
        return res

def get_instr_attr(field, attr_name):
    instr = INSTR_RES.get(field, None)
    if not instr:
        raise ConnectionError('Instr: {instr} is not connected.'.format(instr=field))
    return getattr(instr, attr_name)

def set_osnr(target):
    osnr_setup = config.get_config(':setting:OSNR__Set-up')
    if osnr_setup == 'ATT1 and ATT2':
        method = 'DualAtt'
    elif osnr_setup == 'ATT1 Only':
        method = 'SignalAtt'
    elif osnr_setup == 'ATT2 Only':
        method = 'AseAtt'
    algorithm.receiver.set_osnr(target, INSTR_RES['OSA'], INSTR_RES['ATT2'], INSTR_RES.get('ATT1', None), INSTR_RES['ATT3'], INSTR_RES['OPM2'], method=method)

def set_pin(target):
    for key in 'ATT3', 'OPM2':
        if not INSTR_RES.get(key, None):
            raise ConnectionError('Please connect {instr} first.'.format(instr = key))
    algorithm.receiver.adjust_att_to_target_rx_input(INSTR_RES['ATT3'], INSTR_RES['OPM2'], target)

# :instrument
ApiRouter().register_from_map({
    # resource
    ':instrument:resource:add': add_instr_res,
    ':instrument:resource:remove': remove_instr_res,
    ':instrument:resource:get': get_instr_res,
    ':instrument:resource:mod': mod_instr_res,
    ':instrument:resource:get-by-type': get_res_by_type,
    # lib
    ':instrument:lib:get-model-info': get_model_info,
    ':instrument:lib:get-type-model-map': get_type_model_map,
    # mapping
    ':instrument:mapping:get': get_instr_mapping,
    ':instrument:mapping:set': set_instr_mapping,
    # status
    ':instrument:status:check-connection': check_connection,
    # operation
    ':instrument:status:connect': connect_instrument,
    ':instrument:status:disconnect': disconnect_instrument,
    ':instrument:status:call-method': call_instr_method,
    ':instrument:status:get-attr': get_instr_attr,
    # panel
    ':instrument:panel:set-osnr': set_osnr,
    ':instrument:panel:set-pin': set_pin,
})