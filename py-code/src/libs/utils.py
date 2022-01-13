def float_range(start, stop, step):
    # start & stop will be included
    REL_TOL = 1E-5
    res = []
    if (stop-start) * step < 0:
        return res
    else:
        curr_val = start
        while True:
            min_th = min(start, stop) - REL_TOL*min(abs(curr_val), abs(max(start, stop)))
            max_th = max(start, stop) + REL_TOL*min(abs(curr_val), abs(max(start, stop)))
            print(min_th, max_th, curr_val)
            if min_th <= curr_val <= max_th:
                res.append(curr_val)
                curr_val += step
            else:
                break
        return res

def to_signed(value, byte_length):
    if value >= 256**byte_length/2:
        value = value - 256**byte_length
    return value

def parse_dsp_api_data(val,signed,total_bits,fractional_bits):
    decode_val = 0
    if 's' == signed.lower():
        if val & (1 << (total_bits-1)): #negative
            decode_val = (val - 2**total_bits) / (2**fractional_bits)
        else: #positve
            decode_val = val / (2**fractional_bits)
    elif 'u' == signed.lower():
        decode_val = val / (2**fractional_bits)
    print(decode_val)
    return decode_val