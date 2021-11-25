import time
from math import pi, degrees
import lx16
from constants import *
from lin_alg import *


def time_it(func):
    def new_func(*args, **kwargs):
        old = time.ticks_us()
        val = func(*args, **kwargs)
        new = time.ticks_us()
        print("time of", func.__name__, time.ticks_diff(new, old), "us")
        return val
    return new_func


class Claw:
    """da claw"""

    def __init__(self, dir_com):
        self.motor = lx16.lx16(dir_com)


    def set_offsets(self):
        for finger in range(5):
            for servo in range(3):
                self.motor.set_temp_offset_angle(MOTOR_ID[finger][servo], OFFSET_ANGLE[finger][servo])
                self.motor.set_offset_angle(     MOTOR_ID[finger][servo], OFFSET_ANGLE[finger][servo])
        print('offsets set')
        return None


    def set_limits(self):
        for finger in range(5):
            self.motor.set_angle_limit(MOTOR_ID[finger][1], FINGER_LIMIT[0],  FINGER_LIMIT[1])
            self.motor.set_angle_limit(MOTOR_ID[finger][0], KNUCKLE_LIMIT[0], KNUCKLE_LIMIT[1])
            self.motor.set_angle_limit(MOTOR_ID[finger][2], TIP_LIMIT[0],     TIP_LIMIT[1])
        print('limits set')
        return None


    def move_arm(self, finger, xyz, move_time):
        knuckleAngle, fingerAngle, tipAngle = self.calc_angles(finger, xyz)
        self.motor.goal_position(MOTOR_ID[finger][0], knuckleAngle, move_time, timeout=0)
        self.motor.goal_position(MOTOR_ID[finger][1], fingerAngle,  move_time, timeout=0)
        self.motor.goal_position(MOTOR_ID[finger][2], tipAngle,     move_time, timeout=0)
        time.sleep(move_time/1000)


    def hor_circle(self, finger, xyz, radius, steps, stepTime):
        angle = 0
        zpos = xyz[2]
        while True:
            xpos = xyz[0] + radius*cos(angle)
            ypos = xyz[1] + radius*sin(angle)
            self.move_arm(finger, (xpos, ypos, zpos), stepTime)
            angle += 2*pi/steps
            if angle > 2*pi - 0.01:
                angle = 0


    @time_it
    def calc_angles(self, finger, xyz):
        """
        xyz: tuple of position you want finger tip to be
        finger: which finger? 0-4
        returns angle of each motor to get the tip to that position
        """

        # CALCULATE KNUCKLE ANGLE
        nor_fing = (0, 0, 1) # normal of finger plane if knuckleAngle was 0 deg
        nor_new = cross(D_VECT[finger], xyz) # normal of new finger plane
        # calc angle between the two vectors
        knuckleAngle = degrees(acos(  dot3d(nor_fing, nor_new) / (mag3d(nor_fing)*mag3d(nor_new))  ))

        # define new 2D coordinate system with dims u, v (then this is now a 2D problem)
        # scalar projection
        u = -dot3d(D_VECT[finger],xyz) / D[finger]
        # vector projection
        multiplier = dot3d(D_VECT[finger],xyz) / dot3d(D_VECT[finger],D_VECT[finger])
        proj = tuple(multiplier*i for i in D_VECT[finger])
        v = mag3d(vect_sub(proj, xyz))

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


