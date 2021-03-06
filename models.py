from vpython import *


def person(x, y, z, mask):
    """
    vector(a, b, c)
    model of a person
    """
    head = sphere(pos=vector(x, y, z), color=color.gray(.6), radius=0.6)
    body = box(pos=vector(x, y - 1.5, z), size=vector(2, 1, 1),
               color=vector(0.72, 0.42, 0), axis=vector(0, 1, 0))
    # left legg
    left_leg = cylinder(pos=vector(x, y - 2.5, z - 0.5), radius=0.3,
                        axis=vector(0, -4, 0), color=color.gray(.6))

    # right legg
    right_leg = cylinder(pos=vector(x, y - 2.5, z + 0.5), radius=0.3,
                         axis=vector(0, -4, 0), color=color.gray(.6))

    if mask:
        # mask in front of the head
        mask = box(pos=vector(x+1, z, y), size=vector(0.25, 1, 1),
                   color=vector(0.70, 0.3, 0.5), axis=vector(x+1, y, z))

    compound([body, head])
