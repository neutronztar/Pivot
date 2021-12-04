import time
from math import cos, sin, pi
from rotary_irq_esp import RotaryIRQ
from claw import Claw



if __name__ == "__main__":
    claw = Claw(22)

    knob = RotaryIRQ(pin_num_clk=21,
                    pin_num_dt=19,
                    min_val=-20,
                    max_val=20,
                    reverse=True,
                    range_mode=RotaryIRQ.RANGE_BOUNDED)
    knob.set(value=0)
    
    
    STRIDE = 1.15               # radians, must be less than 2*pi/5
    OFFSET_ANGLE = -STRIDE / 2  # radians
    FRAME_TIME = 60             # ms
    
    radius = 60
    center = [0, 0, 150]        # center of the circle that the finger tips move along
    numFrames = -50             # multiple of 5
    phase = 0                   # sweeps 0-359
    frameStartTime = time.ticks_ms()
    firstLoop = True


    ### MAIN LOOP ###
    while True:
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
