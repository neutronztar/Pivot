from math import *
import lx16
import time

KNUCKLE = 0
FINGER = 1
TIP = 2


def calc_angles(x, y, z):
    Dsq = y**2 + (126+x)**2
    D = sqrt(Dsq)

    fingerAngle = 180 - degrees(atan(y/(126+x))) - degrees(acos((7289.7444 + Dsq - 13933.4416) / (170.76*D)))
    tipAngle = 180 - degrees(acos((13933.4416 + 7289.7444 - Dsq) / 20156.5104))
    knuckleAngle = 90

    return knuckleAngle, fingerAngle, tipAngle


def move_arm(x, y, z, move_time):
    knuckleAngle, fingerAngle, tipAngle = calc_angles(x, y, z)
    motor.goal_position(KNUCKLE, knuckleAngle, move_time, timeout=0)
    motor.goal_position(FINGER, fingerAngle, move_time, timeout=0)
    motor.goal_position(TIP, tipAngle, move_time, timeout=0)
    time.sleep(move_time/1000)



motor = lx16.lx16(22)

# move in square... kinda
# while True:
#     move_arm(-120, 80, 0, 1000)
#     move_arm(-120, 150, 0, 1000)
#     move_arm(-50, 150, 0, 1000)
#     move_arm(-50, 80, 0, 1000)


# move in circle
radius = 50
x_offset = -40
y_offset = 120
angle = 0 #in radians
steps = 32

while True:
    x = -cos(angle)*radius + x_offset
    y = sin(angle)*radius + y_offset
    z = 0
    move_arm(x, y, z, 40)
    angle += 2*pi/steps
    if angle > 2*pi - 0.01:
        angle = 0