from math import cos, radians
import matplotlib.pyplot as plt
import numpy as np


def finger_path(phase):
    """
    If you plot this function it is a graph of the motion of each finger
    phase: 0-259, phase the finger is in
    returns:
        angle: offset angle from finger's step start position
        z: height offset from globe plane
    """
    stepHeight = 40 # mm
    
    if 0 <= phase <= 215:
        angle = phase/215
        z = 0
    elif 215 < phase < 360:
        angle = -phase/145 + 72/29
        z = stepHeight/2*cos(radians(phase-215)/0.4) - stepHeight/2
    else:
        raise ValueError('Input must be 0-259')

    return angle, z


x = list(range(360))
y1 = []
y2 = []
for val in x:
    angleOffset, zOffset = finger_path(val)
    y1.append(angleOffset)
    y2.append(zOffset)



plt.xlim(0, 360)
plt.ylim(-40, 0)
plt.plot(x, y2, 'bo')
plt.show()