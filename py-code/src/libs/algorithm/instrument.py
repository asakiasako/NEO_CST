import time

def safe_set_att(voa_obj, target):
    BASE_DELAY = 0.2    # second
    DELAY_COEF = 0.1    # second/dB
    old_att = voa_obj.get_att()
    att_gap = target - old_att
    additional_delay = abs(att_gap) * DELAY_COEF
    total_delay = BASE_DELAY + additional_delay
    voa_obj.set_att(target)
    time.sleep(total_delay)
