import lx16
from math import *
from constants import *

def dot(a, b):
    # Dot product of two 3D vectors
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]


def cross(a, b):
    # Cross product of two 3D vectors
    return (a[1]*b[2]-a[2]*b[1],  a[2]*b[0]-a[0]*b[2],  a[0]*b[1]-a[1]*b[0])


def mag(a):
    # Magnitude of 3D vector
    return sqrt(a[0]**2 + a[1]**2 + a[2]**2)


def vect_sub(a, b):
    # Subtract b from a (3D vectors)
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2])


def calc_angles(x, y, z, finger):
    # x, y, z: position you want finger tip to be
    # finger: which finger? 0-4
    # returns angle of each motor to get the tip to that position

    # CALCULATE KNUCKLE ANGLE
    nor_fing = (0, 0, 1) # normal of finger plane if knuckleAngle was 0 deg
    nor_new = cross(D_VECT[finger], (x,y,z)) # normal of new finger plane
    # calc angle between the two vectors
    knuckleAngle = degrees(acos(  dot(nor_fing, nor_new) / (mag(nor_fing)*mag(nor_new))  ))

    # define new 2D coordinate system with dims u, v (then this is now a 2D problem)
    # scalar projection
    u = -dot(D_VECT[finger],(x,y,z)) / D[finger]
    # vector projection
    multiplier = dot(D_VECT[finger],(x,y,z)) / dot(D_VECT[finger],D_VECT[finger])
    proj = tuple(multiplier*i for i in D_VECT[finger])
    v = mag(vect_sub(proj, (x,y,z)))



    fingerAngle = 0
    tipAngle = 0

    return u, v#knuckleAngle, fingerAngle, tipAngle



motor = lx16.lx16(22)
#knuckleAngle, fingerAngle, tipAngle = calc_angles(0, 0, 100, 0)
#motor.goal_position(MOTOR_ID[0][0], knuckleAngle, 1000, timeout=0)