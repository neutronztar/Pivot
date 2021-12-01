from math import sqrt, acos


def dot3d(a, b):
    '''Dot product of two 3D vectors'''
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]


def dot2d(a, b):
    '''Dot product of two 2D vectors'''
    return a[0]*b[0] + a[1]*b[1]


def cross(a, b):
    '''Cross product of two 3D vectors'''
    return (a[1]*b[2]-a[2]*b[1],  a[2]*b[0]-a[0]*b[2],  a[0]*b[1]-a[1]*b[0])


def mag3d(a):
    '''Magnitude of 3D vector'''
    return sqrt(a[0]**2 + a[1]**2 + a[2]**2)


def mag2d(a):
    '''Magnitude of 2D vector'''
    return sqrt(a[0]**2 + a[1]**2)


def vect_sub(a, b):
    '''Subtract b from a (3D vectors)'''
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2])


def vect_add(a, b):
    '''add two 3D vectors'''
    return (a[0]+b[0], a[1]+b[1], a[2]+b[2])


def sss(closeSide1, closeSide2, farSide):
    '''Calculate an angle of a Side-Side-Side triangle in radians'''
    return acos( (closeSide1**2+closeSide2**2-farSide**2) / (2*closeSide1*closeSide2) )

