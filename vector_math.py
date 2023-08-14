import math

def add_vector2(vec1, vec2):
    return [vec1[0] + vec2[0], vec1[1] + vec2[1]]

def get_endpos(point, radian_angle, length, height):
    x_offset = (length * math.cos(radian_angle)) + (height * math.cos(radian_angle - math.pi / 2))
    y_offset = (length * math.sin(radian_angle)) + (height * math.sin(radian_angle - math.pi / 2))

    return [point[0] + x_offset, point[1] + y_offset]

def normalize_radian_angle(angle):
    full_circle = (math.pi * 2)
    if (angle > full_circle):
        angle = angle % full_circle

    while (angle < 0):
        angle += full_circle
    
    return angle
        