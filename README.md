# RoboClaw
open source robotic art piece


## MicroPython Commands for Controlling ESP32 on Linux ##

# list files on board
ampy -p /dev/ttyUSB0 ls

# control board with REPL
picocom /dev/ttyUSB0 -b115200
then push 'en' button on board

# Connect with rshell (broken)
rshell -p /dev/ttyUSB0)



# MicroPython Tools
ampy rshell mpfshell