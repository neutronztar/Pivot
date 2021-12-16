import time
from math import isinf
from micropython import const
from machine import ADC, Pin
from claw import Claw, time_it
from constants import *


def main():
    claw = Claw(22)

    # Left and right joystick potentiometer
    potX = ADC(Pin(33))
    potX.atten(ADC.ATTN_11DB)

    # Front and back joystick potentiometer
    potY = ADC(Pin(32))
    potY.atten(ADC.ATTN_11DB)

    # Up and Down joystick potentiometer
    potZ = ADC(Pin(35))
    potZ.atten(ADC.ATTN_11DB)

    speedTable = {
    #speedKnob: numFrames
        0:     float('inf'), # stopped
        1:         80,       # slowest
        2:         75,
        3:         70,
        4:         65,
        5:         60,
        6:         55,
        7:         50,       # default
        8:         45,
        9:         40,
        10:        35, 
        11:        30,
        12:        25,
        13:        20        # fastest
    }  
    
    
    STRIDE = 1.15               # radians, must be less than 2*pi/5
    OFFSET_ANGLE = -STRIDE / 2  # radians
    FRAME_TIME = const(60)      # ms
    
    center = [0, 0, 150]        # center of the circle that the finger tips move along
    radius = 50
    numFrames = -60
    phase = 0                   # sweeps 0-359
    frameStartTime = time.ticks_ms()
    firstLoop = True


    ### MAIN LOOP ###
    while True:
        # Update values based on user input
        center = update_values(potX, potY, potZ, center)
        
        # If not stopped
        if not isinf(numFrames):
            # Calculate angles of all 15 servos for next frame
            angles = claw.calc_frame_angles(phase, STRIDE, OFFSET_ANGLE, radius, center)

            # ------Wait------
            while time.ticks_diff(time.ticks_ms(), frameStartTime) < FRAME_TIME:
                pass
            frameStartTime = time.ticks_ms() # reset timer
            
            # Move all fingers to frame
            claw.move_to_frame(angles, FRAME_TIME, firstLoop)
            firstLoop = False

            # Increment phase
            phase = (phase + 360 / numFrames) % 360



def update_values(potX, potY, potZ, center):
    """Update values based on user input"""
    
    def bound(val, low, high):
        return max(low, min(high, val))
    
    joyX = potX.read() - X_AVG
    joyY = potY.read() - Y_AVG
    joyZ = potZ.read() - Z_AVG

    if joyX > SLOP:
        targetX = int(min(joyX - SLOP, 1200) * 50/1200)
    elif joyX < -SLOP:
        targetX = int(max(joyX + SLOP, -1200) * 50/1200)
    else:
        targetX = 0

    if joyY > SLOP:
        targetY = int(min(joyY - SLOP, 1200) * 50/1200)
    elif joyY < -SLOP:
        targetY = int(max(joyY + SLOP, -1200) * 50/1200)
    else:
        targetY = 0

    if joyZ > SLOP:
        zStep = int(min(joyZ - SLOP, 1200) * 6/1200)
    elif joyZ < -SLOP:
        zStep = int(max(joyZ + SLOP, -1200) * 6/1200)
    else:
        zStep = 0




    xStep = int((targetX - center[0]) / 4)
    yStep = int((targetY - center[1]) / 4)

    center[0] += xStep
    center[1] += yStep
    center[2] = bound(center[2] + zStep, 100, 180)


    return center


if __name__ == "__main__":
    main()