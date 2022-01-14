import time
from math import pi, degrees, isclose
from micropython import const
import lx16
from constants import *
from lin_alg import *


def time_it(func):
    """Decorator that times a function and prints how long it took"""
    def new_func(*args, **kwargs):
        startTime = time.ticks_us()
        val = func(*args, **kwargs)
        timeTaken = time.ticks_diff(time.ticks_us(), startTime)
        print("time of", func.__name__, f"{timeTaken:,d}", "us")
        return val
    return new_func


class Claw:
    """Da Claw"""

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
            info[id]['vin_min\t'], info[id]['vin_max\t'] = self.motor.read_vin_limit(id)
            info[id]['mode\t'] = self.motor.read_servo_mode(id)
            info[id]['load_status'] = self.motor.read_load_status(id)
            info[id]['led_ctrl'] = self.motor.read_led_ctrl(id)
            info[id]['led_error'] = self.motor.read_led_error(id)
            goal_angle, goal_time = self.motor.read_goal_position(id)
            info[id]['goal_angle'], info[id]['goal_time'] = smart_round(goal_angle), goal_time
        
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
            #for check in range(3):
                # Send move command
            self.motor.goal_position(MOTOR_ID[finger][servo], angles[servo], move_time, timeout=0)
                
                # Check that it got command
                # angle, time = self.motor.read_goal_position(MOTOR_ID[finger][servo])
                # if isclose(angle, angles[servo], abs_tol=0.9) and move_time == time:
                #     break
                # else:
                #     print('Try', check, 'failed for finger', finger, 'servo', servo)


    def move_in_sync(self, knuckleAngle, fingerAngle, tipAngle, moveTime):
        """Move all fingers at the same time"""
        angles = (knuckleAngle, fingerAngle, tipAngle)
        for finger in range(5):
            self.move_finger(finger, angles, moveTime)


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


    def finger_path(self, phase):
        """
        If you plot this function it is a graph of the motion of each finger
        phase: 0-259, phase the finger is in
        returns:
            stepPos: offset from finger's step start position (0-1)
            z: height offset from globe plane
        """
        stepHeight = 35 # mm
        
        if 0 <= phase <= 215:
            stepPos = phase/215
            z = 0
        elif 215 < phase < 360:
            stepPos = -phase/145 + 72/29
            z = stepHeight/2*cos(radians(phase-215)/0.4) - stepHeight/2
        else:
            raise ValueError('Input must be 0-259')

        return stepPos, z


    def calc_frame_angles(self, phase, stride, offsetAngle, radius, center):
        """Calculate all 15 motor angles for a frame"""

        # Calculate coordinates of all finger tips
        xyz = [(0,0,0)] * 5
        for finger in range(5):
            phaseOffset = (phase + 144 * finger) % 360 # each finger is 144 degrees out of phase from the last
            fingerStartAngle = offsetAngle + finger*2*pi/5 # Where each finger starts at its frame 0 (radians)
            stepPos, z = self.finger_path(phaseOffset)
            angle = fingerStartAngle + stepPos * stride
            x = cos(angle) * radius
            y = sin(angle) * radius
            xyz[finger] = vect_add(center, (x, y, z))

        # Use above coordinates to calculate motor angles for all fingers
        angles = [(0,0,0)] * 5
        for finger in range(5):
            angles[finger] = self.calc_angles(finger, xyz[finger])

        return angles


    def move_to_frame(self, angles, moveTime, firstLoop):
        """Move all 15 motors to given angles in moveTime ms"""

        # Slow for first frame cause we don't know current positions
        if firstLoop:
            for finger in range(5):
                self.move_finger(finger, angles[finger], 800)
            time.sleep_ms(800)
        
        # Regular speed for all other frames
        else:
            for finger in range(5):
                self.move_finger(finger, angles[finger], moveTime)


    def spin_old(self, knob, radius=60, stride=1.15, center=[0, 0, 150], numFrames=-50, frameTime=60):
        """
        ---spin ball---
        stride: in radians, must be less than 2*pi/5
        center: tuple, center of the circle that the finger tips move along
        offsetAngle: in radians
        numFrames: must be a multiple of 5, (max 360)
        frameTime: time between frames in ms
        """
        offsetAngle = -stride / 2

        def smart_add(num1, num2):
            return (num1 + num2) % 360
        
        phase = 0
        moveStartTime = time.ticks_ms()
        firstLoop = True
        while True:
            # Calculation start time
            calcStartTime = time.ticks_ms()

            # map knob value to z
            center[0] = 3 * knob.value()
            
            # Calculate coordinates of all finger tips
            xyz = [(0,0,0)] * 5
            for finger in range(5):
                phaseOffset = smart_add(phase, 144*finger) # each finger is 144 degrees out of phase from the last
                fingerStartAngle = offsetAngle + finger*2*pi/5 # Where each finger starts at its frame 0 (radians)
                stepPos, z = self.finger_path(phaseOffset)
                angle = fingerStartAngle + stepPos * stride
                x = cos(angle) * radius
                y = sin(angle) * radius
                xyz[finger] = vect_add(center, (x, y, z))

            # Calculate motor angles for all fingers
            angles = [(0,0,0)] * 5
            for finger in range(5):
                angles[finger] = self.calc_angles(finger, xyz[finger])

            # Calculation end time
            calcEndTime = time.ticks_ms()
            print('calcs took', time.ticks_diff(calcEndTime, calcStartTime), 'ms')

            # ------Wait------
            while time.ticks_diff(time.ticks_ms(), moveStartTime) < frameTime:
                pass
            
            # Move start time
            moveStartTime = time.ticks_ms()

            # Move all fingers to frame
            if firstLoop: # slow for first frame cause we don't know current positions
                for finger in range(5):
                    self.move_finger(finger, angles[finger], 1200)
                time.sleep_ms(1200)
                firstLoop = False
            else:
                for finger in range(5):
                    self.move_finger(finger, angles[finger], frameTime)

            # Move end time
            moveEndTime = time.ticks_ms()
            print('moving took', time.ticks_diff(moveEndTime, moveStartTime), 'ms')

            # Increment phase
            phase = smart_add(phase, 360/numFrames)
        

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


