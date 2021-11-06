from vpython import *
import particle

animation = canvas(width=800, height=400, align='left')
gray = color.gray(0.7)

animation.title = "COVID-19 Particles Simulation"
animation.caption = """
Right button or ctrl-drag to rotate camera
Shift-drag to pan left or right
Middle button or alt/option and drag to zoom
"""

# size of the box
d = 6
# radius of the container
r = 0.05

# box sized vectors
boxbottom = curve(color=gray, radius=r)
boxbottom.append([vector(-d, -d, -d), vector(-d, -d, d), vector(d, -d, d), vector(d, -d, -d), vector(-d, -d, -d)])
boxtop = curve(color=gray, radius=r)
boxtop.append([vector(-d, d, -d), vector(-d, d, d), vector(d, d, d), vector(d, d, -d), vector(-d, d, -d)])

# vertices of the boxes
vert1 = curve(color=gray, radius=r)
vert2 = curve(color=gray, radius=r)
vert3 = curve(color=gray, radius=r)
vert4 = curve(color=gray, radius=r)

vert1.append([vector(-d, -d, -d), vector(-d, d, -d)])
vert2.append([vector(-d, -d, d), vector(-d, d, d)])
vert3.append([vector(d, -d, d), vector(d, d, d)])
vert4.append([vector(d, -d, -d), vector(d, d, -d)])


# =================================== 3D person model =========================================

def person(a, b, c):
    """
    vector(a, b, c)
    model of a person
    """
    head = sphere(pos=vector(a, b, c), color=color.gray(.6), radius=0.6)
    body = box(pos=vector(1, b - 1.5, c), size=vector(2, 1, 1), color=vector(0.72, 0.42, 0), axis=vector(0, 1, 0))
    compound([body, head])


a = 1
b = 2
c = 1
person(a, b, c)

#
# ================= Ball Example =================
#


L = 6
mass = 4E-3 / 6E23  # helium mass
Ratom = 0.03  # wildly exaggerated size of helium atom
k = 1.4E-23  # Boltzmann constant
T = 300  # around room temperature
dt = 1E-5
Natoms = 200  # change this to have more or fewer atoms

Atoms = []
p = []
apos = []
pavg = sqrt(2 * mass * 1.5 * k * T)  # average kinetic energy p**2/(2mass) = (3/2)kT

for i in range(Natoms):
    x = L * random() - L / 2
    y = L * random() - L / 2
    z = L * random() - L / 2
    if i == 0:
        Atoms.append(sphere(pos=vector(x, y, z), radius=Ratom, color=color.cyan, make_trail=True, retain=100,
                            trail_radius=0.3 * Ratom))
    else:
        Atoms.append(sphere(pos=vector(x, y, z), radius=Ratom, color=gray))
    apos.append(vec(x, y, z))
    theta = pi * random()
    phi = 2 * pi * random()
    px = pavg * sin(theta) * cos(phi)
    py = pavg * sin(theta) * sin(phi)
    pz = pavg * cos(theta)
    p.append(vector(px, py, pz))


def checkCollisions():
    hitlist = []
    r2 = 2 * Ratom
    r2 *= r2
    for i in range(Natoms):
        ai = apos[i]
        for j in range(i):
            aj = apos[j]
            dr = ai - aj
            if mag2(dr) < r2: hitlist.append([i, j])
    return hitlist


while True:
    rate(300)

    # Update all positions
    for i in range(Natoms): Atoms[i].pos = apos[i] = apos[i] + (p[i] / mass) * dt

    # Check for collisions
    hitlist = checkCollisions()

    # If any collisions took place, update momenta of the two atoms
    for ij in hitlist:
        i = ij[0]
        j = ij[1]
        ptot = p[i] + p[j]
        posi = apos[i]
        posj = apos[j]
        vi = p[i] / mass
        vj = p[j] / mass
        vrel = vj - vi
        a = vrel.mag2
        if a == 0: continue;  # exactly same velocities
        rrel = posi - posj
        if rrel.mag > Ratom: continue  # one atom went all the way through another

        # theta is the angle between vrel and rrel:
        dx = dot(rrel, vrel.hat)  # rrel.mag*cos(theta)
        dy = cross(rrel, vrel.hat).mag  # rrel.mag*sin(theta)
        # alpha is the angle of the triangle composed of rrel, path of atom j, and a line
        #   from the center of atom i to the center of atom j where atome j hits atom i:
        alpha = asin(dy / (2 * Ratom))
        d = (2 * Ratom) * cos(alpha) - dx  # distance traveled into the atom from first contact
        deltat = d / vrel.mag  # time spent moving from first contact to position inside atom

        posi = posi - vi * deltat  # back up to contact configuration
        posj = posj - vj * deltat
        mtot = 2 * mass
        pcmi = p[i] - ptot * mass / mtot  # transform momenta to cm frame
        pcmj = p[j] - ptot * mass / mtot
        rrel = norm(rrel)
        pcmi = pcmi - 2 * pcmi.dot(rrel) * rrel  # bounce in cm frame
        pcmj = pcmj - 2 * pcmj.dot(rrel) * rrel
        p[i] = pcmi + ptot * mass / mtot  # transform momenta back to lab frame
        p[j] = pcmj + ptot * mass / mtot
        apos[i] = posi + (p[i] / mass) * deltat  # move forward deltat in time
        apos[j] = posj + (p[j] / mass) * deltat

    for i in range(Natoms):
        loc = apos[i]
        if abs(loc.x) > L / 2:
            if loc.x < 0:
                p[i].x = abs(p[i].x)
            else:
                p[i].x = -abs(p[i].x)

        if abs(loc.y) > L / 2:
            if loc.y < 0:
                p[i].y = abs(p[i].y)
            else:
                p[i].y = -abs(p[i].y)

        if abs(loc.z) > L / 2:
            if loc.z < 0:
                p[i].z = abs(p[i].z)
            else:
                p[i].z = -abs(p[i].z)