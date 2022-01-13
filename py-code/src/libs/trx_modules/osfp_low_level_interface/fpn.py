import sys

# def cal(val):
#     # print('val 0x%04x.\n' % val)
#     exponent_temp = 0
#     mantissa_temp = 0
#     exponent = 0
#     mantissa  = 0
#     exponent_temp = val >> 11
#     # print('exponent_temp 0x%04x.\n' % exponent_temp)

#     if(exponent_temp & (1 << 4)): #negative
#         exponent_temp = 0x10 - (exponent_temp & 0x0F)
#         # print('negative exponent_temp 0x%04x.\n' % exponent_temp)
#         exponent =  exponent_temp * -1
#         # print('negative exponent %d.\n' % exponent)
#     else:#if exponent positive, no need to translate
#         exponent = exponent_temp


#     mantissa_temp = val & 0x7FF

#     if(mantissa_temp & (1 << 10)): #negative
#         mantissa_temp = 0x400 - (mantissa_temp & 0x3FF)
#         mantissa =  mantissa_temp * -1
#     else: #if mantissa positive, no need to translate
#         mantissa = mantissa_temp
#     print("mantissa %d.\n" %  mantissa)
#     print("exponent %d.\n" %  exponent)

#     res = mantissa * (2 ** exponent)
#     print(res)
def s16_9(val):
    # if val & (1 << (total_bits-1)): #negative
    #     decode_val = (val - 2**total_bits) / (2**fractional_bits)
    # else: #positve
    #     decode_val = val / (2**fractional_bits)
    if val & (1 << (16-1)): #negative
        decode_val = (val - 2**16) / (2**9)
    else: #positve
        decode_val = val / (2**9)
    print(decode_val)

def cal(val,signed,total_bits,fractional_bits):
    if 's' == signed:
        if val & (1 << (total_bits-1)): #negative
            decode_val = (val - 2**total_bits) / (2**fractional_bits)
        else: #positve
            decode_val = val / (2**fractional_bits)
    elif 'u' == signed:
        decode_val = val / (2**fractional_bits)
    print(decode_val)
    return decode_val

# def main():
#     val = sys.argv[1]
#     # signed = sys.argv[1]
#     # val = sys.argv[1]
#     # val = sys.argv[1]
#     print(val)
#     # print('%d.\n' % int(val, 16))
#     s16_9(eval(val))

def main():
    val = sys.argv[1]
    signed = sys.argv[2]
    tb = sys.argv[3]
    fb = sys.argv[4]
    # print(val)
    # print('%d.\n' % int(val, 16))
    cal(eval(val), signed, eval(tb), eval(fb))

if __name__ == '__main__':
    main()
