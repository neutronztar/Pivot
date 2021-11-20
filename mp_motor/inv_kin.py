import lx16
from math import *
from constants import *
import time
import utime


def timeit(func):
    def new_func(*args, **kwargs):
        old = utime.ticks_us()
        val = func(*args, **kwargs)
        new = utime.ticks_us()
        print(utime.ticks_diff(new, old))
        return val
    return new_func


def dot3d(a, b):
    # Dot product of two 3D vectors
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]


def dot2d(a, b):
    # Dot product of two 2D vectors
    return a[0]*b[0] + a[1]*b[1]


def cross(a, b):
    # Cross product of two 3D vectors
    return (a[1]*b[2]-a[2]*b[1],  a[2]*b[0]-a[0]*b[2],  a[0]*b[1]-a[1]*b[0])


def mag3d(a):
    # Magnitude of 3D vector
    return sqrt(a[0]**2 + a[1]**2 + a[2]**2)


def mag2d(a):
    # Magnitude of 2D vector
    return sqrt(a[0]**2 + a[1]**2)


def vect_sub(a, b):
    # Subtract b from a (3D vectors)
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2])


def sss(closeSide1, closeSide2, farSide):
    # Calculate an angle of a Side-Side-Side triangle in radians
    return acos( (closeSide1**2+closeSide2**2-farSide**2) / (2*closeSide1*closeSide2) )


@timeit
def calc_angles(x, y, z, finger):
    # x, y, z: position you want finger tip to be
    # finger: which finger? 0-4
    # returns angle of each motor to get the tip to that position

    # CALCULATE KNUCKLE ANGLE
    nor_fing = (0, 0, 1) # normal of finger plane if knuckleAngle was 0 deg
    nor_new = cross(D_VECT[finger], (x,y,z)) # normal of new finger plane
    # calc angle between the two vectors
    knuckleAngle = degrees(acos(  dot3d(nor_fing, nor_new) / (mag3d(nor_fing)*mag3d(nor_new))  ))

    # define new 2D coordinate system with dims u, v (then this is now a 2D problem)
    # scalar projection
    u = -dot3d(D_VECT[finger],(x,y,z)) / D[finger]
    # vector projection
    multiplier = dot3d(D_VECT[finger],(x,y,z)) / dot3d(D_VECT[finger],D_VECT[finger])
    proj = tuple(multiplier*i for i in D_VECT[finger])
    v = mag3d(vect_sub(proj, (x,y,z)))

    # CALCULATE FINGER ANGLE
    l3_vect = (u+D[finger], v)
    l3_mag = mag2d(l3_vect)
    alpha1 = acos( dot2d(l3_vect, (D[finger],0)) / (l3_mag*D[finger]) ) # angle b/t vectors
    alpha2 = sss(FINGER_LEN, l3_mag, TIP_LEN)
    fingerAngle = degrees(pi - alpha1 - alpha2)

    # CALCULATE TIP ANGLE
    alpha3 = sss(FINGER_LEN, TIP_LEN, l3_mag)
    tipAngle = degrees(pi - alpha3)

    return knuckleAngle, fingerAngle, tipAngle



def move_arm(x, y, z, finger, move_time):
    knuckleAngle, fingerAngle, tipAngle = calc_angles(x, y, z, finger)
    motor.goal_position(MOTOR_ID[finger][0], knuckleAngle, move_time, timeout=0)
    motor.goal_position(MOTOR_ID[finger][1], fingerAngle,  move_time, timeout=0)
    motor.goal_position(MOTOR_ID[finger][2], tipAngle,     move_time, timeout=0)
    time.sleep(move_time/1000)


def hor_circle(center, radius, steps, stepTime, finger):
    angle = 0
    zpos = center[2]
    while True:
        xpos = center[0] + radius*cos(angle)
        ypos = center[1] + radius*sin(angle)
        move_arm(xpos, ypos, zpos, finger, stepTime)
        angle += 2*pi/steps
        if angle > 2*pi - 0.01:
            angle = 0



motor = lx16.lx16(22)

hor_circle((-34, 55.4, 150), 40, 16, 200, 0)