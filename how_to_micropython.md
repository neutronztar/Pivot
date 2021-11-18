## MicroPython Commands for Controlling ESP32 on Linux ##

# list files on board
ampy -p /dev/ttyUSB0 ls

# control board with REPL
picocom /dev/ttyUSB0 -b115200
then push 'en' button on board
exit picocom with Ctrl-a --> Ctrl-x

# Connect with rshell (broken on MicroPython 1.17... or not?)
rshell -p /dev/ttyUSB0
# Then list files on board
ls /pyboard
# Enter REPL
repl
# Run file from REPL
exec(open('file.py').read())



# MicroPython Tools
ampy rshell mpfshell
