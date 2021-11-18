import time
import machine

pin = machine.Pin(2, machine.Pin.OUT)

while True:
    pin.on()
    time.sleep(0.2)
    pin.off()
    time.sleep(0.2)
    print('test')