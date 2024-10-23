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

# Matrix operations for transformations
def TranslationMatrix(tx, ty, tz):
    return [
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ]

def RotationMatrix(rx, ry, rz):
    rx = math.radians(rx)
    ry = math.radians(ry)
    rz = math.radians(rz)

    cosx = math.cos(rx)
    sinx = math.sin(rx)
    cosy = math.cos(ry)
    siny = math.sin(ry)
    cosz = math.cos(rz)
    sinz = math.sin(rz)

    Rx = [
        [1, 0, 0, 0],
        [0, cosx, -sinx, 0],
        [0, sinx, cosx, 0],
        [0, 0, 0, 1]
    ]

    Ry = [
        [cosy, 0, siny, 0],
        [0, 1, 0, 0],
        [-siny, 0, cosy, 0],
        [0, 0, 0, 1]
    ]

    Rz = [
        [cosz, -sinz, 0, 0],
        [sinz, cosz, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ]

    return matrix_multiply(matrix_multiply(Rz, Ry), Rx)

def ScaleMatrix(sx, sy, sz):
    return [
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ]

def matrix_multiply(A, B):
    result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result

def inverse(M):
    # This function calculates the inverse of a 4x4 matrix
    det = (M[0][0] * (M[1][1] * (M[2][2] * M[3][3] - M[2][3] * M[3][2]) -
                      M[1][2] * (M[2][1] * M[3][3] - M[2][3] * M[3][1]) +
                      M[1][3] * (M[2][1] * M[3][2] - M[2][2] * M[3][1])) -
           M[0][1] * (M[1][0] * (M[2][2] * M[3][3] - M[2][3] * M[3][2]) -
                      M[1][2] * (M[2][0] * M[3][3] - M[2][3] * M[3][0]) +
                      M[1][3] * (M[2][0] * M[3][2] - M[2][2] * M[3][0])) +
           M[0][2] * (M[1][0] * (M[2][1] * M[3][3] - M[2][3] * M[3][1]) -
                      M[1][1] * (M[2][0] * M[3][3] - M[2][3] * M[3][0]) +
                      M[1][3] * (M[2][0] * M[3][1] - M[2][1] * M[3][0])) -
           M[0][3] * (M[1][0] * (M[2][1] * M[3][2] - M[2][2] * M[3][1]) -
                      M[1][1] * (M[2][0] * M[3][2] - M[2][2] * M[3][0]) +
                      M[1][2] * (M[2][0] * M[3][1] - M[2][1] * M[3][0])))
    if det == 0:
        raise ValueError("Matrix is not invertible")

    # This is a placeholder for the actual calculation, which is very complex for a 4x4 matrix.
    # Consider using an external library if needed for efficiency.
    raise NotImplementedError("Inverse calculation for a 4x4 matrix is not implemented here.")

def transform(vector, matrix, is_point=True):
    x, y, z = vector
    w = 1 if is_point else 0
    vec = [x, y, z, w]
    transformed_vec = [
        sum(vec[i] * matrix[0][i] for i in range(4)),
        sum(vec[i] * matrix[1][i] for i in range(4)),
        sum(vec[i] * matrix[2][i] for i in range(4)),
        sum(vec[i] * matrix[3][i] for i in range(4))
    ]
    return transformed_vec[:3]
