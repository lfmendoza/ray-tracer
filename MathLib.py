import math

def dot(v0, v1):
    return sum([a * b for a, b in zip(v0, v1)])

def length(v):
    return sum([a * a for a in v]) ** 0.5

def sub(v0, v1):
    return [a - b for a, b in zip(v0, v1)]

def add(v0, v1):
    return [a + b for a, b in zip(v0, v1)]

def mul(v0, k):
    return [a * k for a in v0]

def div(v0, k):
    if k == 0:
        return [0 for a in v0]
    return [a / k for a in v0]

def norm(v):
    l = length(v)
    if l == 0:
        return [0 for a in v]
    return [a / l for a in v]

def cross(v0, v1):
    return [v0[1] * v1[2] - v0[2] * v1[1],
            v0[2] * v1[0] - v0[0] * v1[2],
            v0[0] * v1[1] - v0[1] * v1[0]]

def reflectVector(N, I):
    # R = I - 2(N · I)N
    dot_NI = dot(N, I)
    N_times_2_dot_NI = mul(N, 2 * dot_NI)
    R = sub(I, N_times_2_dot_NI)
    R = norm(R)
    return R
