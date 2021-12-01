from math import cos, sin, pi
import matplotlib.pyplot as plt
import numpy as np

radius = 70
center = (-30, 0, 160)
offset_angle=0.6
stride=1
num_frames = 15 # Must be multiple of 5
frames_on_circle = int(num_frames * 0.6 + 1)

def smart_add(num1, num2):
    sum = num1 + num2
    while sum >= num_frames:
        sum -= num_frames
    return sum


def vect_add(a, b):
    '''add two 3D vectors'''
    return (a[0]+b[0], a[1]+b[1], a[2]+b[2])


for frame in range(15):
    xyz = [(0,0,0)] * 5
    for finger in range(5):
        frame_offset = smart_add(frame, int(num_frames*0.4*finger))
        if frame_offset < frames_on_circle:
            fingerStartAngle = offset_angle + finger*2*pi/5 # Where each finger starts at its frame 0
            angle = fingerStartAngle + frame_offset*stride/frames_on_circle
            x = cos(angle) * radius
            y = sin(angle) * radius
            xyz[finger] = (vect_add(center, (x, y, 0)))

    for finger_coords in xyz:
        print(finger_coords)
        

    xpoints = np.array([xyz[0][0], xyz[1][0], xyz[2][0], xyz[3][0], xyz[4][0]])
    ypoints = np.array([xyz[0][1], xyz[1][1], xyz[2][1], xyz[3][1], xyz[4][1]])
    plt.xlim(-100, 100)
    plt.ylim(-100, 100)
    plt.plot(xpoints, ypoints, 'o')
    plt.show()