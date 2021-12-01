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
        """dir_com: pin for changing direction of communication"""
        self.motor = lx16.lx16(dir_com)


    def query_motors(self):
        info = {id: {} for id in range(15)}

        def smart_round(val):
            if val is None:
                return None
            return round(val)

        for id in info:
            info[id]['temp\t'] = self.motor.read_temp(id)
            info[id]['temp_max_limit'] = self.motor.read_temp_max_limit(id)
            info[id]['angle\t'] = smart_round(self.motor.read_pos(id))
            min, max = self.motor.read_angle_limit(id)
            info[id]['angle_min'], info[id]['angle_max'] = smart_round(min), smart_round(max)
            info[id]['angle_offset'] = smart_round(self.motor.read_angle_offset(id))
            info[id]['vin\t'] = self.motor.read_vin(id)
            min, max = self.motor.read_vin_limit(id)
            info[id]['vin_min\t'], info[id]['vin_max\t'] = min, max
            info[id]['mode\t'] = self.motor.read_servo_mode(id)
            info[id]['load_status'] = self.motor.read_load_status(id)
            info[id]['led_ctrl'] = self.motor.read_led_ctrl(id)
            info[id]['led_error'] = self.motor.read_led_error(id)
        
        # header
        print('motor\t\t', end='')
        for id in info:
            print(id, end='\t')
            if (id+1)%3 == 0:
                print('\t', end='')
        print('\n---------------------------------------------------------------------------------', end='')
        print('-----------------------------------------------------------------------------------')

        # body
        for key in info[0]:
            print(key, end='\t')
            for id in info:
                print(info[id][key], end='\t')
                if (id+1)%3 == 0:
                    print('\t', end='')
            print('\n', end='')

        return None


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


    def move_finger_to_coords(self, finger, xyz, move_time):
        knuckleAngle, fingerAngle, tipAngle = self.calc_angles(finger, xyz)
        self.motor.goal_position(MOTOR_ID[finger][0], knuckleAngle, move_time, timeout=0)
        self.motor.goal_position(MOTOR_ID[finger][1], fingerAngle,  move_time, timeout=0)
        self.motor.goal_position(MOTOR_ID[finger][2], tipAngle,     move_time, timeout=0)
        time.sleep(move_time/1000)
    

    def move_finger(self, finger, angles, move_time):
        """
        Move all motors in finger to given angles
        finger: which finger to move?
        angles: (knuckleAngle, fingerAngle, tipAngle)
        """
        for servo in range(3):
            self.motor.goal_position(MOTOR_ID[finger][servo], angles[servo], move_time, timeout=0)


    def hor_circle(self, finger, xyz, radius, steps, stepTime):
        angle = 0
        zpos = xyz[2]
        while True:
            xpos = xyz[0] + radius*cos(angle)
            ypos = xyz[1] + radius*sin(angle)
            self.move_finger_to_coords(finger, (xpos, ypos, zpos), stepTime)
            angle += 2*pi/steps
            if angle > 2*pi - 0.01:
                angle = 0


    def spin(self, radius=60, stride=1.15, center=(-30, 0, 160), offset_angle=0.8, num_frames=15, frameTime=100):
        """
        --spin ball--
        stride: in radians, must be less than 2*pi/5
        offset_angle: in radians
        num_frames: must be a multiple of 5
        frameTime: time between frames in ms
        """

        # Num of frames where the finger is touching the globe
        frames_on_circle = int(num_frames * 0.6 + 1)
        frames_off_circle = num_frames - frames_on_circle

        def smart_add(num1, num2):
            sum = num1 + num2
            while sum >= num_frames:
                sum -= num_frames
            return sum

        frame = 0 # Starting frame of finger 0, frames of other finger are offset
        while True:
            # Calculation start time
            calcStartTime = time.ticks_ms()
            
            # Calculate coordinates of all finger tips
            xyz = [(0,0,0)] * 5
            for finger in range(5):
                frame_offset = smart_add(frame, int(num_frames*0.4*finger))
                fingerStartAngle = offset_angle + finger*2*pi/5 # Where each finger starts at its frame 0
                
                # if the finger is touching the globe in this frame
                if frame_offset < frames_on_circle:
                    angle = fingerStartAngle + frame_offset*stride/frames_on_circle
                    x = cos(angle) * radius
                    y = sin(angle) * radius
                    xyz[finger] = vect_add(center, (x, y, 0))
                else:
                    increment = stride/(frames_off_circle+1)
                    angle = fingerStartAngle + stride - (1 + frame_offset - frames_on_circle) * increment
                    x = cos(angle) * radius
                    y = sin(angle) * radius
                    z = -20
                    xyz[finger] = vect_add(center, (x, y, z))
                    
            # Calculate motor angles for all fingers
            angles = [(0,0,0)] * 5
            for finger in range(5):
                angles[finger] = self.calc_angles(finger, xyz[finger])

            # Calculation end time
            calcEndTime = time.ticks_ms()
            calcTime = time.ticks_diff(calcEndTime, calcStartTime)
            print('Frame', frame, 'calculations took', calcTime, 'ms.')

            # Wait
            while time.ticks_diff(time.ticks_ms(), calcStartTime) < frameTime:
                pass

            # Move all fingers to frame
            for finger in range(5):
                self.move_finger(finger, angles[finger], frameTime+30)
            print('frame', frame)
            print('moved finger0 to', angles[0])

            # Increment frame counter
            frame = smart_add(frame, 1)
        


    def calc_angles(self, finger, xyz):
        """
        xyz: tuple of position you want finger tip to be
        finger: which finger? 0-4
        returns angle of each motor to get the tip to that position (degrees)
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


