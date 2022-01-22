# This single-file library was originally made by sasilva1998 under the MIT license and then modified by Nick Wallick
# Original library https://github.com/FunPythonEC/uPy_Lewansoul_LX-16
# Used to send and recieve commands to and from the LewanSoul LX-16A servos


# MIT License

# Copyright (c) 2019 FunPython

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import machine as m    # needed so that uart can be used
from micropython import const
import utime

# every command available for the servo
SERVO_ID_ALL = const(0xFE)
SERVO_MOVE_TIME_WRITE = const(1)
SERVO_MOVE_TIME_READ = const(2)
SERVO_MOVE_TIME_WAIT_WRITE = const(7)
SERVO_MOVE_TIME_WAIT_READ = const(8)
SERVO_MOVE_START = const(11)
SERVO_MOVE_STOP = const(12)
SERVO_ID_WRITE = const(13)
SERVO_ID_READ = const(14)
SERVO_ANGLE_OFFSET_ADJUST = const(17)
SERVO_ANGLE_OFFSET_WRITE = const(18)
SERVO_ANGLE_OFFSET_READ = const(19)
SERVO_ANGLE_LIMIT_WRITE = const(20)
SERVO_ANGLE_LIMIT_READ = const(21)
SERVO_VIN_LIMIT_WRITE = const(22)
SERVO_VIN_LIMIT_READ = const(23)
SERVO_TEMP_MAX_LIMIT_WRITE = const(24)
SERVO_TEMP_MAX_LIMIT_READ = const(25)
SERVO_TEMP_READ = const(26)
SERVO_VIN_READ = const(27)
SERVO_POS_READ = const(28)
SERVO_OR_MOTOR_MODE_WRITE = const(29)
SERVO_OR_MOTOR_MODE_READ = const(30)
SERVO_LOAD_OR_UNLOAD_WRITE = const(31)
SERVO_LOAD_OR_UNLOAD_READ = const(32)
SERVO_LED_CTRL_WRITE = const(33)
SERVO_LED_CTRL_READ = const(34)
SERVO_LED_ERROR_WRITE = const(35)
SERVO_LED_ERROR_READ = const(36)

SERVO_ERROR_OVER_TEMPERATURE = const(1)
SERVO_ERROR_OVER_VOLTAGE = const(2)
SERVO_ERROR_LOCKED_ROTOR = const(4)


header = [0x55, 0x55]  # defined to be used later (initials of the packet)


class lx16:

    # constructor
    # default uart used in serialid, especified for esp32
    def __init__(self, dir_com, serialid=2):

        self.baudrate = 115200  # only baudrate avaiable for the servo
        self.serialid = serialid
        self.dir_com = m.Pin(dir_com, m.Pin.OUT)

        # uart defined
        try:
            self.uart = m.UART(self.serialid, self.baudrate)
            self.uart.init(self.baudrate, bits=8, parity=None, stop=1, txbuf=0)
        except Exception as e:
            print(e)

    # =======================WRITE METHODS===================
    # every writing method is here
    def goal_position(self, ID, angle, time, rxbuf=15, timeout=2500, rtime=850):
        # angle: 0-240 and doesn't have to be an int
        # time: 0-30000 ms
        sendPacket(
            bytearray(
                makePacket(
                    ID,
                    SERVO_MOVE_TIME_WRITE,
                    le(int(angle * 1000 / 240)) + le(int(time)),
                    #le(int(angle)) + le(int(time)),
                )
            ),
            self.uart,
            self.dir_com,
            rtime,
            rxbuf,
            timeout,
        )

    def start_goal_position(self, ID, angle, time, rxbuf=15, timeout=2500, rtime=850):
        sendPacket(
            bytearray(
                makePacket(
                    ID,
                    SERVO_MOVE_TIME_WAIT_WRITE,
                    le(int(angle * 1000 / 240)) + le(int(time)),
                )
            ),
            self.uart,
            self.dir_com,
            rtime,
            rxbuf,
            timeout,
        )

    def start(self, ID, rxbuf=15, timeout=5, rtime=850):
        sendPacket(
            bytearray(makePacket(ID, SERVO_MOVE_START)),
            self.uart,
            self.dir_com,
            rtime,
            rxbuf,
            timeout,
        )

    def stop(self, ID, rxbuf=15, timeout=5, rtime=850):
        sendPacket(
            bytearray(makePacket(ID, SERVO_MOVE_STOP)),
            self.uart,
            self.dir_com,
            rtime,
            rxbuf,
            timeout,
        )

    def set_id(self, ID, NID, rxbuf=15, timeout=5, rtime=850):
        sendPacket(
            bytearray(makePacket(ID, SERVO_ID_WRITE, [NID])),
            self.uart,
            self.dir_com,
            rtime,
            rxbuf,
            timeout,
        )

    def set_temp_offset_angle(self, ID, angle, rxbuf=15, timeout=5, rtime=850):
        sendPacket(
            bytearray(
                makePacket(ID, SERVO_ANGLE_OFFSET_ADJUST, [int(angle / 30 * 125)])
            ),
            self.uart,
            self.dir_com,
            rtime,
            rxbuf,
            timeout,
        )

    def set_offset_angle(self, ID, angle, rxbuf=15, timeout=5, rtime=850):
        # angle doesnt even matter at all in this function!
        sendPacket(
            bytearray(
                makePacket(ID, SERVO_ANGLE_OFFSET_WRITE, [int(angle / 30 * 125)])
            ),
            self.uart,
            self.dir_com,
            rtime,
            rxbuf,
            timeout,
        )

    def set_angle_limit(self, ID, minangle, maxangle, rxbuf=15, timeout=5, rtime=850):
        sendPacket(
            bytearray(
                makePacket(
                    ID,
                    SERVO_ANGLE_LIMIT_WRITE,
                    le(int(minangle / 240 * 1000)) + le(int(maxangle / 240 * 1000)),
                )
            ),
            self.uart,
            self.dir_com,
            rtime,
            rxbuf,
            timeout,
        )

    def set_vin_limit(self, ID, minvin, maxvin, rxbuf=15, timeout=5, rtime=850):
        sendPacket(
            bytearray(makePacket(ID, SERVO_VIN_LIMIT_WRITE, le(minvin) + le(maxvin))),
            self.uart,
            self.dir_com,
            rtime,
            rxbuf,
            timeout,
        )

    def set_max_temp_limit(self, ID, temp, rxbuf=15, timeout=5, rtime=850):
        sendPacket(
            bytearray(makePacket(ID, SERVO_TEMP_MAX_LIMIT_WRITE, [temp])),
            self.uart,
            self.dir_com,
            rtime,
            rxbuf,
            timeout,
        )

    def set_load_status(self, ID, status, rxbuf=15, timeout=5, rtime=850):
        sendPacket(
            bytearray(makePacket(ID, SERVO_LOAD_OR_UNLOAD_WRITE, [status])),
            self.uart,
            self.dir_com,
            rtime,
            rxbuf,
            timeout,
        )

    def set_led_ctrl(self, ID, mode, rxbuf=15, timeout=5, rtime=850):
        sendPacket(
            bytearray(makePacket(ID, SERVO_LED_CTRL_WRITE, [mode])),
            self.uart,
            self.dir_com,
            rtime,
            rxbuf,
            timeout,
        )

    def set_led_error(self, ID, fault, rxbuf=15, timeout=5, rtime=850):
        sendPacket(
            bytearray(makePacket(ID, SERVO_LED_ERROR_WRITE, [fault])),
            self.uart,
            self.dir_com,
            rtime,
            rxbuf,
            timeout,
        )

    def goal_speed(self, ID, speed, rxbuf=15, timeout=5, rtime=850):
        sendPacket(
            bytearray(makePacket(ID, SERVO_OR_MOTOR_MODE_WRITE, le(1) + le(speed))),
            self.uart,
            self.dir_com,
            rtime,
            rxbuf,
            timeout,
        )

    def joint_mode(self, ID, rxbuf=15, timeout=5, rtime=850):
        sendPacket(
            bytearray(makePacket(ID, SERVO_OR_MOTOR_MODE_WRITE, le(0) + le(0))),
            self.uart,
            self.dir_com,
            rtime,
            rxbuf,
            timeout,
        )

    # =======================READ METHODS===================
    # every reading method is here

    def read_goal_position(self, ID, rxbuf=15, timeout=5, rtime=430): #rtime=500 was too slow
        command = SERVO_MOVE_TIME_READ
        for attempt in range(5):
            resp = sendPacket(
                bytearray(makePacket(ID, command)),
                self.uart,
                self.dir_com,
                rtime,
                rxbuf,
                timeout,
            )
            if self.validate(resp, ID, command):
                angle = (resp[5] + (resp[6]<<8)) * 240/1000
                time = resp[7] + (resp[8]<<8)
                return angle, time
            else:
                print('sending', command, 'command again')
            
        # if all 5 attempts failed
        return None, None

    def read_wait_goal_position(self, ID, rxbuf=15, timeout=5, rtime=430): #BROKEN?
        command = SERVO_MOVE_TIME_WAIT_READ
        for attempt in range(5):
            resp = sendPacket(
                bytearray(makePacket(ID, command)),
                self.uart,
                self.dir_com,
                rtime,
                rxbuf,
                timeout,
            )
            if self.validate(resp, ID, command):
                angle = (resp[5] + (resp[6]<<8)) * 240/1000
                time = resp[7] + (resp[8]<<8)
                return angle, time
            else:
                print('sending', command, 'command again')
        
        # if all 5 attempts failed
        return None, None

    def read_id(self, ID, rxbuf=15, timeout=5, rtime=430): #rtime=500 was too slow
        command = SERVO_ID_READ
        for attempt in range(5):
            resp = sendPacket(
                bytearray(makePacket(ID, command)),
                self.uart,
                self.dir_com,
                rtime,
                rxbuf,
                timeout,
            )
            if self.validate(resp, ID, command):
                return resp[5]
            else:
                print('sending', command, 'command again')
        
        # if all 5 attempts failed
        return None

    def read_angle_offset(self, ID, rxbuf=15, timeout=5, rtime=430): #rtime=500 was too slow
        command = SERVO_ANGLE_OFFSET_READ
        for attempt in range(5):
            resp = sendPacket(
                bytearray(makePacket(ID, command)),
                self.uart,
                self.dir_com,
                rtime,
                rxbuf,
                timeout,
            )
            if self.validate(resp, ID, command):
                return twos_comp(resp[5], 1) * 240/1000
            else:
                print('sending', command, 'command again')
        
        # if all 5 attempts failed
        return None

    def read_angle_limit(self, ID, rxbuf=15, timeout=5, rtime=430): #rtime=500 was too slow
        command = SERVO_ANGLE_LIMIT_READ
        for attempt in range(5):
            resp = sendPacket(
                bytearray(makePacket(ID, command)),
                self.uart,
                self.dir_com,
                rtime,
                rxbuf,
                timeout,
            )
            if self.validate(resp, ID, command):
                min = (resp[5] + (resp[6]<<8)) * 240/1000
                max = (resp[7] + (resp[8]<<8)) * 240/1000
                return min, max
            else:
                print('sending', command, 'command again')
        
        # if all 5 attempts failed
        return None, None

    def read_vin_limit(self, ID, rxbuf=15, timeout=5, rtime=430): #rtime=500 was too slow
        command = SERVO_VIN_LIMIT_READ
        for attempt in range(5):
            resp = sendPacket(
                bytearray(makePacket(ID, command)),
                self.uart,
                self.dir_com,
                rtime,
                rxbuf,
                timeout,
            )
            if self.validate(resp, ID, command):
                min = (resp[5] + (resp[6]<<8)) / 1000
                max = (resp[7] + (resp[8]<<8)) / 1000
                return min, max
            else:
                print('sending', command, 'command again')
        
        # if all 5 attempts failed
        return None, None

    def read_temp_max_limit(self, ID, rxbuf=15, timeout=5, rtime=430): #rtime=500 was too slow
        command = SERVO_TEMP_MAX_LIMIT_READ
        for attempt in range(5):
            resp = sendPacket(
                bytearray(makePacket(ID, command)),
                self.uart,
                self.dir_com,
                rtime,
                rxbuf,
                timeout,
            )
            if self.validate(resp, ID, command):
                return resp[5]
            else:
                print('sending', command, 'command again')
        
        # if all 5 attempts failed
        return None

    def read_temp(self, ID, rxbuf=15, timeout=5, rtime=500): #rtime good
        command = SERVO_TEMP_READ
        for attempt in range(5):
            resp = sendPacket(
                bytearray(makePacket(ID, command)),
                self.uart,
                self.dir_com,
                rtime,
                rxbuf,
                timeout,
            )
            if self.validate(resp, ID, command):
                return resp[5]
            else:
                print('sending', command, 'command again')
        
        # if all 5 attempts failed
        return None

    def read_vin(self, ID, rxbuf=15, timeout=5, rtime=500): #rtime good
        command = SERVO_VIN_READ
        for attempt in range(5):
            resp = sendPacket(
                bytearray(makePacket(ID, command)),
                self.uart,
                self.dir_com,
                rtime,
                rxbuf,
                timeout,
            )
            if self.validate(resp, ID, command):
                return (resp[5] + (resp[6]<<8)) / 1000
            else:
                print('sending', command, 'command again')
        
        # if all 5 attempts failed
        return None

    def read_pos(self, ID, rxbuf=15, timeout=5, rtime=500): #rtime good
        command = SERVO_POS_READ
        for attempt in range(5):
            resp = sendPacket(
                bytearray(makePacket(ID, command)),
                self.uart,
                self.dir_com,
                rtime,
                rxbuf,
                timeout,
            )
            if self.validate(resp, ID, command):
                return twos_comp((resp[5] + (resp[6]<<8)), 2) * 240/1000
            else:
                print('sending', command, 'command again')
        
        # if all 5 attempts failed
        return None

    def read_servo_mode(self, ID, rxbuf=15, timeout=5, rtime=430): #rtime=500 was too slow
        command = SERVO_OR_MOTOR_MODE_READ
        for attempt in range(5):
            resp = sendPacket(
                bytearray(makePacket(ID, command)),
                self.uart,
                self.dir_com,
                rtime,
                rxbuf,
                timeout,
            )
            if self.validate(resp, ID, command):
                mode = resp[5]
                # need to add support for motor mode speed
                return mode
            else:
                print('sending', command, 'command again')
        
        # if all 5 attempts failed
        return None

    def read_load_status(self, ID, rxbuf=15, timeout=5, rtime=430): #rtime=500 was too slow
        command = SERVO_LOAD_OR_UNLOAD_READ
        for attempt in range(5):
            resp = sendPacket(
                bytearray(makePacket(ID, command)),
                self.uart,
                self.dir_com,
                rtime,
                rxbuf,
                timeout,
            )
            if self.validate(resp, ID, command):
                return resp[5]
            else:
                print('sending', command, 'command again')
        
        # If all 5 attempts failed
        return None

    def read_led_ctrl(self, ID, rxbuf=15, timeout=5, rtime=430): #rtime=500 was too slow
        command = SERVO_LED_CTRL_READ
        for attempt in range(5):
            resp = sendPacket(
                bytearray(makePacket(ID, command)),
                self.uart,
                self.dir_com,
                rtime,
                rxbuf,
                timeout,
            )
            if self.validate(resp, ID, command):
                return resp[5]
            else:
                print('sending', command, 'command again')
        
        # If all 5 attempts failed
        return None

    def read_led_error(self, ID, rxbuf=15, timeout=5, rtime=430): #rtime=500 was too slow
        command = SERVO_LED_ERROR_READ
        for attempt in range(5):
            resp = sendPacket(
                bytearray(makePacket(ID, command)),
                self.uart,
                self.dir_com,
                rtime,
                rxbuf,
                timeout,
            )
            if self.validate(resp, ID, command):
                return resp[5]
            else:
                print('sending', command, 'command again')
        
        # If all 5 attempts failed
        return None


    def validate(self, resp, ID, command):
        """validate servo responses"""
        if resp == None:
            print('no reply from motor')
            return False

        # check header is there
        if resp[0:2] != bytes(header):
            print('invalid resp header')
            return False

        # check resp is of proper length
        if resp[3] is not len(resp)-3:
            print('invalid resp len')
            return False
        
        # check checksum
        if checksum(resp[2:-1]) != resp[-1]:
            print('invalid resp checksum')
            return False
        
        # check ID
        if resp[2] != ID:
            print('ID mismatch')
            return False
        
        # check for command mismatch
        if resp[4] != command:
            print('got wrong command back')
            return False
        
        # response is valid
        return True
        
        

def sendPacket(packet, uart, dir_com, rtime, rxbuf, timeout):
    _ = uart.read()# clear the RX buffer
    dir_com.on()   # turn on so packet is sent
    uart.write(packet)

    # time is traced in order to know when to listen (0.85 or 0.5 ms. very short!)
    tinit = utime.ticks_us()
    while utime.ticks_diff(utime.ticks_us(), tinit) < rtime:
        pass

    dir_com.off()  # off to receive packet

    tinit = utime.ticks_ms()
    while (utime.ticks_ms() - tinit) < timeout:  # timeout of 1600us
        resp = uart.read(rxbuf)
        if resp is not None:
            return resp
    return None


def makePacket(ID, cmd, params=None):
    if params:
        length = 3 + len(params)
        packet = [ID, length, cmd] + params
    else:
        length = 3
        packet = [ID, length, cmd]
    packet = header + packet + [checksum(packet)]
    return packet


def le(h):
    """
	Little-endian, takes a 16b number and returns an array arrange in little
	endian or [low_byte, high_byte].
	"""
    h &= 0xFFFF  # make sure it is 16 bits
    return [h & 0xFF, h >> 8]


def word(l, h):
    """
	Given a low and high bit, converts the number back into a word.
	"""
    return (h << 8) + l


def checksum(packet):
    return 255 - (sum(packet) % 256)


def twos_comp(val, byte_len):
    if byte_len == 1:
        if val & (1 << 7):    # if most sig bit is 1
            val = val | ~0xff # make all above bits 1
        return val
    if byte_len == 2:
        if val & (1 << 15):      # if most sig bit is 1
            val = val | ~0xffff  # make all above bits 1
        return val
