from math import cos, sin, radians, pi
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


def vect_add(a, b):
    '''add two 3D vectors'''
    return (a[0]+b[0], a[1]+b[1], a[2]+b[2])



phase = 0
offsetAngle = 0
radius = 50
stride = 1.15
center = [0, 0, 150]

for i in range(300):
    # Calculate coordinates of all finger tips
    xyz = [(0,0,0)] * 5
    for finger in range(5):
        phaseOffset = (phase + 144 * finger) % 360 # each finger is 144 degrees out of phase from the last
        fingerStartAngle = offsetAngle + finger*2*pi/5 # Where each finger starts at its frame 0 (radians)
        stepPos, z = finger_path(phaseOffset)
        angle = fingerStartAngle + stepPos * stride
        x = cos(angle) * radius
        y = sin(angle) * radius
        xyz[finger] = vect_add(center, (x, y, z))
    
    x = []
    y = []
    z = []
    for entry in xyz:
        x.append(entry[0])
        y.append(entry[1])
        z.append(entry[2])
    
    

    fig = plt.figure(figsize = (8, 8))
    plt.scatter(x, y, c=z, cmap='Greens')
    plt.axis([-60, 60, -60, 60])
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.xscale('linear')
    plt.yscale('linear')
    plt.title('Fingertip Positions')
    plt.savefig('./animation/' + str(i) + '.png')
    #plt.show()


    phase = (phase + 6) % 360