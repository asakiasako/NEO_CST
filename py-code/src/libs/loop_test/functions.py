from .inputs import INPUT_PARAMETERS
from .outputs import OUTPUT_PARAMETERS
from .resources import RESOURCES


def get_loop_list():
    return [i.paramName for i in INPUT_PARAMETERS]

def get_output_list():
    return [i.paramName for i in OUTPUT_PARAMETERS]

def get_from_msg_queue():
    msg_queue = RESOURCES.msg_queue
    msg_list = []
    if msg_queue:
        while True:
            try:
                msg_list.append(msg_queue.get_nowait())
            except Exception:
                break
    return msg_list
    
