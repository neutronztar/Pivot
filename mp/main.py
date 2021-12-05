import time
from math import isinf
from micropython import const
from rotary_irq_esp import RotaryIRQ
from claw import Claw, time_it


def main():
    claw = Claw(22)

    speedKnob = RotaryIRQ(pin_num_clk=21,
                        pin_num_dt=19,
                        min_val=-13,
                        max_val=13,
                        reverse=True,
                        range_mode=RotaryIRQ.RANGE_BOUNDED)
    speedKnob.set(value=7)


    radKnob = RotaryIRQ(pin_num_clk=23,
                        pin_num_dt=18,
                        min_val=4, # will be * 5
                        max_val=30,
                        reverse=True,
                        range_mode=RotaryIRQ.RANGE_BOUNDED)
    radKnob.set(value=12) # 60mm radius
    

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
    radius = radKnob.value() * 5
    phase = 0                   # sweeps 0-359
    frameStartTime = time.ticks_ms()
    firstLoop = True


    ### MAIN LOOP ###
    while True:
        # Update values based on user input
        phase, numFrames, radius = update_values(phase, speedKnob, radKnob, speedTable, radius)
        
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


@time_it
def update_values(phase, speedKnob, radKnob, speedTable, radius):
    """Update values based on user input"""

    # speed knob position --> number of frames
    speedKnobVal = speedKnob.value()
    if speedKnobVal >= 0:
        numFrames = -speedTable[speedKnobVal]
    else:
        numFrames = speedTable[-speedKnobVal] # Negative number of frames reverses direction
    
    
    # If not stopped
    if not isinf(numFrames):
        multiple = 360 / (-numFrames)
        phase = multiple * round(phase / multiple) # round phase to nearest multiple

        # radius knob position --> radius
        radius = radKnob.value() * 5
    
    # If stopped
    else:
        # Don't allow changing radius
        radKnob.set(value=int(radius/5))


    return phase, numFrames, radius


if __name__ == "__main__":
    main()