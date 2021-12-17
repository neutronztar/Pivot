from math import radians, sin, cos
from micropython import const


# Distance from center of palm to axis 1 for each finger
D = (91, 91, 91, 91, 91)

# Angle from X-axis for each finger
THETA_DEG = (0, 72, 144, 216, 288)
THETA = tuple(map(radians, THETA_DEG))

# Vector for each of the finger start positions
D_VECT = (
    (D[0]*cos(THETA[0]), D[0]*sin(THETA[0]), 0),
    (D[1]*cos(THETA[1]), D[1]*sin(THETA[1]), 0),
    (D[2]*cos(THETA[2]), D[2]*sin(THETA[2]), 0),
    (D[3]*cos(THETA[3]), D[3]*sin(THETA[3]), 0),
    (D[4]*cos(THETA[4]), D[4]*sin(THETA[4]), 0)
)

# Lengths (mm)
FINGER_LEN = const(85) # exact: 85.38
TIP_LEN = const(118)   # exact: 118.04

# Motor IDs (knuckle,finger,tip) for each finger
MOTOR_ID = ((0,1,2), (3,4,5), (6,7,8), (9,10,11), (12,13,14))

# Offest Angles (knuckle,finger,tip) for each finger
OFFSET_ANGLE = ((-1,-2,9), (1,-2,9), (-1,-6,9), (1,-4,6), (-1,-6,10))

# Motor angle limits - limits move with the offsets!
KNUCKLE_LIMIT = (45, 135)
FINGER_LIMIT = (0, 114)
TIP_LIMIT = (0, 133)

# Potentiometer middle positions
X_AVG = 1690
Y_AVG = 1678
Z_AVG = 1720
SLOP = 200 # Distance from middle position before something starts happening