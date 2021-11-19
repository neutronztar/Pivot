from math import radians, cos, sin


# Distance from center of palm for each finger
D = (126, 126, 126, 126, 76)

# Angle from X-axis for each finger
THETA_DEG = (121.5, 160.5, 199.5, 238.5, 340.5)
THETA = tuple(map(radians, THETA_DEG))

# Vector for each of the finger start positions
D_VECT = (
    (D[0]*cos(THETA[0]), D[0]*sin(THETA[0]), 0),
    (D[1]*cos(THETA[1]), D[1]*sin(THETA[1]), 0),
    (D[2]*cos(THETA[2]), D[2]*sin(THETA[2]), 0),
    (D[3]*cos(THETA[3]), D[3]*sin(THETA[3]), 0),
    (D[4]*cos(THETA[4]), D[4]*sin(THETA[4]), 0)
)

# Lengths
FINGER_LEN = 85.38
TIP_LEN = 118.04

# Motor IDs (knuckle,finger,tip) for each finger
MOTOR_ID = ((0,1,2), (3,4,5), (6,7,8), (9,10,11), (12,13,14))
