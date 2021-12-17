import lx16
import time

# motor IDs
KNUCKLE = 0
FINGER = 1
TIP = 2

motor = lx16.lx16(22)


while True:
    # set all to pos 0
    motor.goal_position(KNUCKLE, 45, 2000, timeout=0)
    motor.goal_position(FINGER, 0, 2000, timeout=0)
    motor.goal_position(TIP, 0, 2000, timeout=0)
    time.sleep(2)

    # set all to max pos
    motor.goal_position(KNUCKLE, 135, 2000, timeout=0)
    motor.goal_position(FINGER, 114, 2000, timeout=0)
    motor.goal_position(TIP, 135, 2000, timeout=0)
    time.sleep(2)