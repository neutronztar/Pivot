# MicroPython Commands for Controlling ESP32 on Linux #

## installing mp
cd /home/nick/.local/lib/python3.8/site-packages
python3 esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
python3 esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 esp32-20210902-v1.17.bin

## list files on board
ampy -p /dev/ttyUSB0 ls

## control board with REPL
picocom /dev/ttyUSB0 -b115200
then push 'en' button on board
exit picocom with Ctrl-a --> Ctrl-x

## Connect with rshell (broken on MicroPython 1.17... or not?)
rshell -p /dev/ttyUSB0
## Then list files on board
ls /pyboard
## Enter REPL
repl
## Run file from REPL
exec(open('file.py').read())



## MicroPython Tools
ampy rshell mpfshell


## All importable modules
help('modules')

## check ram
import micropython as mp
mp.mem_info(True)

## check file-system space
import os
os.statvfs('/')
https://docs.micropython.org/en/latest/library/os.html#:~:text=file%20or%20directory.-,os.statvfs,-(path)