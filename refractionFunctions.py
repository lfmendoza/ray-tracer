from MathLib import dot, mul, sub, norm
from math import acos, asin, pi

def refractVector(normal, incident, iorFrom, iorTo):
    # Snell's Law
    n = iorFrom / iorTo
    c1 = -dot(normal, incident)
    under_sqrt = 1 - n**2 * (1 - c1**2)
    if under_sqrt < 0:
        # Ocurre Reflexión Interna Total
        return None
    sqrt_term = under_sqrt ** 0.5

    temp = sub(incident, mul(normal, c1))
    T = mul(temp, n)
    T = sub(T, mul(normal, sqrt_term))
    T = norm(T)
    return T


def totalInternalReflection(normal, incident, n1, n2):
    c1 = dot(normal, incident)
    if c1 < 0:
        c1 = -c1
    else:
        n1, n2 = n2, n1

    if n1 < n2:
        return False

    theta1 = acos(c1)
    thetaC = asin(n2/n1)

    return theta1 >= thetaC


def fresnel(normal, incident, iorFrom, iorTo):
    cosi = max(-1, min(1, dot(incident, normal)))
    etai = iorFrom
    etat = iorTo
    if cosi > 0:
        etai, etat = etat, etai
    sint = etai / etat * (max(0, 1 - cosi ** 2)) ** 0.5
    if sint >= 1:
        # Reflexión Interna Total
        kr = 1
    else:
        cost = (max(0, 1 - sint ** 2)) ** 0.5
        cosi = abs(cosi)
        Rs = ((etat * cosi) - (etai * cost)) / ((etat * cosi) + (etai * cost))
        Rp = ((etai * cosi) - (etat * cost)) / ((etai * cosi) + (etat * cost))
        kr = (Rs ** 2 + Rp ** 2) / 2
    kt = 1 - kr
    return kr, kt