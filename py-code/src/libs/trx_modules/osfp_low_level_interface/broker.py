from socket import *
import time
import ctypes

class Broker():

    def __init__(self, ip="192.168.1.212", long_term_connection=False, timeout=5):
        # self._socket = socket(AF_INET, SOCK_STREAM)
        # self._ip = "192.168.1.1"
        self._ip = ip
        self._long_term_connection = long_term_connection
        self._socket = None
        self._timeout = timeout

    def open(self):
        self._socket = socket(AF_INET, SOCK_STREAM)
        self._socket.settimeout(self._timeout)
        self._socket.connect((self._ip, 1000))
        prompt = self._socket.recv(1024)
        # print(prompt.decode('gbk'))

    def close(self):
        self._socket.close()
        self._socket = None

    @property
    def IP(self):
        return self._ip

    @IP.setter
    def IP(self, val):
        self._ip = val

    @property
    def TWI_SPEED(self):
        if not self._long_term_connection:
            self.open()
        self._socket.send("*twir".encode())
        rx = self._socket.recv(1024)
        if not self._long_term_connection:
            self.close()
        # print(rx.decode('gbk'))
        return int(str(rx.decode('gbk')).split('>')[1].split('\\')[0], 10)

    @TWI_SPEED.setter
    def TWI_SPEED(self, val):
        if not self._long_term_connection:
            self.open()
        tx = ("*twir %d" % val).encode()
        self._socket.send(tx)
        rx = self._socket.recv(1024)
        if not self._long_term_connection:
            self.close()
        # print(rx.decode('gbk'))

    def parse_cmdstr(self, buffer_string):
        s1 = str(buffer_string)
        s2 = s1.split(";")
        s3 = s2[0].split("'")
        buffer_string = s3[1]
        return buffer_string

    def dcpy(self, addr, len):
        if not self._long_term_connection:
            self.open()
        tx = ("*dcpy %d %d" % (addr, len)).encode()
        self._socket.send(tx)
        rx = self._socket.recv(1024)
        if not self._long_term_connection:
            self.close()        
        if self.parse_cmdstr(rx) == '$0000':
            return 1
        else:
            return 0

    def twi_car(self):  # Current Address Read Operation
        if not self._long_term_connection:
            self.open()
        self._socket.send("*twi 1".encode())
        rx = self._socket.recv(1024)
        if not self._long_term_connection:
            self.close()
        return int(str(rx.decode('gbk')).split('>')[1].split(',')[0], 16)
    
    def twi_scar(self, len):  # Sequential Current Address Read Operation
        if not self._long_term_connection:
            self.open()
        self._socket.send(("*twi %d" % len).encode())
        rx = self._socket.recv(1024)
        if not self._long_term_connection:
            self.close()
        vals = str(rx.decode('gbk')).split('>')[1].split(',')
        # print(vals)
        r = bytearray()
        for i in range(len):
            r.append(int(vals[i], 16))
        return r
    
    def twi_rr(self, addr):  # Random Read Operation
        if not self._long_term_connection:
            self.open()
        self._socket.send(("*twi 1 %d" % addr).encode())
        rx = self._socket.recv(1024)
        # print(rx)
        if not self._long_term_connection:
            self.close()
        # print(rx.decode('gbk'))
        return int(str(rx.decode('gbk')).split('>')[1].split(',')[0], 16)

    def twi_srr(self, addr, len):  # Sequential Random Read Operation
        if not self._long_term_connection:
            self.open()
        self._socket.send(("*twi %d %d" % (len, addr)).encode())
        rx = self._socket.recv(1024)
        if not self._long_term_connection:
            self.close()
        # print(rx)
        vals = str(rx.decode('gbk')).split('>')[1].split(',')
        # print(vals)
        r = bytearray()
        for i in range(len):
            r.append(int(vals[i], 16))
        return r

    def twi_bw(self, addr, val): # Byte Write Operation
        tx = "*twi 1 %d %d" % (addr, val)
        # print(tx)
        if not self._long_term_connection:
            self.open()
        self._socket.send(tx.encode())
        rx = self._socket.recv(1024)
        if not self._long_term_connection:
            self.close()
        # print(rx.decode('gbk'))

    def twi_sbw(self, addr, vals): # Sequential Byte Write Operation
        length = len(vals)
        # print(length)
        tx = '*twi %d %d' % (length, addr)
        for b in vals:
            tx += ' %d' % b
        # print(tx)
        if not self._long_term_connection:
            self.open()
        self._socket.send(tx.encode())
        rx = self._socket.recv(1024)
        if not self._long_term_connection:
            self.close()
    
    def cdb_pswdw(self): # Write CDB password: 0xa5, 0x5a, 0x5a, 0xa5 to lower memory byte 122~125
        self.twi_sbw(122, b'\xa5\x5a\x5a\xa5')

    def ain(self, id): 
        tx = '*ain %d' % id
        if not self._long_term_connection:
            self.open()
        self._socket.send(tx.encode())
        rx = self._socket.recv(1024)
        if not self._long_term_connection:
            self.close()
        # print(rx.decode('gbk'))
        vals = str(rx.decode('gbk')).split('>')[1].split(',')
        d = int(vals[0], 10)
        a = float(vals[1])
        return d, a

    def aout(self, id): 
        tx = '*aout %d' % id
        if not self._long_term_connection:
            self.open()
        self._socket.send(tx.encode())
        rx = self._socket.recv(1024)
        if not self._long_term_connection:
            self.close()
        # print(rx.decode('gbk'))
        vals = str(rx.decode('gbk')).split('>')[1].split(',')
        s = float(vals[0])
        r = float(vals[1])
        return s, r

    def aout_set(self, id, val): 
        tx = '*aout %d %f' % (id, val)
        if not self._long_term_connection:
            self.open()
        self._socket.send(tx.encode())
        rx = self._socket.recv(1024)
        if not self._long_term_connection:
            self.close()
        # print(rx.decode('gbk'))

    def din(self, id):
        tx = '*din %d' % id
        if not self._long_term_connection:
            self.open()
        self._socket.send(tx.encode())
        rx = self._socket.recv(1024)
        if not self._long_term_connection:
            self.close()
        # print(rx.decode('gbk'))
        return int(str(rx.decode('gbk')).split('>')[1].strip(), 10)

    def dout(self, id):
        tx = '*dout %d' % id
        if not self._long_term_connection:
            self.open()
        self._socket.send(tx.encode())
        rx = self._socket.recv(1024)
        if not self._long_term_connection:
            self.close()
        # print(rx.decode('gbk'))
        return int(str(rx.decode('gbk')).split('>')[1].strip(), 10)

    def dout_set(self, id, state):
        tx = '*dout %d %d' % (id, state)
        if not self._long_term_connection:
            self.open()
        self._socket.send(tx.encode())
        rx = self._socket.recv(1024)
        if not self._long_term_connection:
            self.close()
        # print(rx.decode('gbk'))

    @property
    def MOD_VOLTAGE(self):
        return self.ain(102)[1] # P3V3_OSFP_CON = 102

    @MOD_VOLTAGE.setter
    def MOD_VOLTAGE(self, val):
        self.aout_set(101, val)

    @property
    def MOD_CURRENT(self):
        return self.ain(100)[1] # P3V3_OSFP_CURR_CHECK = 100

    @property
    def MOD_INT(self):
        return not self.din(1) # MOD_INTN = 1

    @property
    def MOD_PRSn(self):
        return not self.din(2) # MOD_PRSN = 2

    @property
    def MOD_LPWn(self):
        return bool(self.dout(23)) # MOD_LPWN = 21

    @MOD_LPWn.setter
    def MOD_LPWn(self, state):
        self.dout_set(23, state) # H_LPWN_OE_N = 21
        # self.dout_set(21, state) # MCU_MOD_LPWN = 21

    @property
    def MOD_RSTn(self):
        return not self.dout(22) # MOD_RSTN = 3

    @MOD_RSTn.setter
    def MOD_RSTn(self, state):
        self.dout_set(22, not state) # H_RSTN_OE_N = 22
        # self.dout_set(20, state) # MCU_MOD_RSTN = 20

    def reset_module(self):
        self.MOD_RSTn = True
        self.MOD_RSTn = False
        time.sleep(5)

    def cdb1_idle(self):
        status = self.twi_rr(37)
        return not (status & 0x80)

    def cdb1_cip(self):
        time.sleep(0.1)
        status = self.twi_rr(37)
        # print("cip 0x%4x.\n" % status)
        # return bool(status & 0x80)
        return bool((status & 0x80) or (status == 0))

    def cdb1_success(self):
        status = self.twi_rr(37)
        # print('cdb reg37 status %d.\n' % status)
        return not (status & 0xC0)

    def cdb_chkcode(self, vals):
        chkcode = ctypes.c_ubyte(0)
        for b in vals:
            chkcode.value += b
        chkcode.value = - chkcode.value - 1
        return chkcode.value

    def cdb_psw(self): # Vendor password Write CDB password: 0xa5, 0x5a, 0x5a, 0xa5 to lower memory byte 122~125
        self.twi_sbw(122, b'\xa5\x5a\x5a\xa5')

    def cdb_user_psw(self):
        self.twi_sbw(122, b'\x00\x00\x10\x11')

    def set_fan_speed(self, value):
        if not 0 <= value <= 100:
            raise ValueError('Invalid value for fan duty percent: %r' % value)
        self._socket.send('*FAN {percent:d}'.format(percent=round(value)).encode())
        self._socket.recv(1024)
