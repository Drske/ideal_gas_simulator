import math


def starting_coords(N, radius, width, height):
    coords = set()

    x = y = radius

    while x <= width - radius:
        while y <= height - radius:
            coords.add((x, y))
            y += 2 * radius
        x += 2 * radius
        y = radius

    return coords


def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def bounce(atom1, atom2):
    h = abs(atom1.pos_y - atom2.pos_y)
    w = abs(atom1.pos_x - atom2.pos_x)

    if w == 0:
        atom1.vel_y, atom2.vel_y = atom2.vel_y, atom1.vel_y
        return
    else:
        slope = math.atan(float(h) / w)

    if atom1.pos_x > atom2.pos_x:
        atom1, atom2 = atom2, atom1

    if atom1.pos_y > atom2.pos_y:
        pass
    else:
        slope = -slope

    cos_slope = math.cos(slope)
    sin_slope = math.sin(slope)

    vx1 = atom1.vel_x * cos_slope - atom1.vel_y * sin_slope
    vy1 = atom1.vel_x * sin_slope + atom1.vel_y * cos_slope

    vx2 = atom2.vel_x * cos_slope - atom2.vel_y * sin_slope
    vy2 = atom2.vel_x * sin_slope + atom2.vel_y * cos_slope

    vx1, vx2 = vx2, vx1

    slope = -slope

    cos_slope = math.cos(slope)
    sin_slope = math.sin(slope)

    atom1.vel_x = vx1 * cos_slope - vy1 * sin_slope
    atom1.vel_y = vx1 * sin_slope + vy1 * cos_slope

    atom2.vel_x = vx2 * cos_slope - vy2 * sin_slope
    atom2.vel_y = vx2 * sin_slope + vy2 * cos_slope
