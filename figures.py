from intercept import Intercept
from math import atan2, acos, pi, isclose, sin, cos, sqrt
from MathLib import cross, dot, sub, add, mul, norm, length

class Shape(object):
    def __init__(self, position, material):
        self.position = position
        self.material = material
        self.type = "None"

    def ray_intersect(self, orig, dir):
        return None

class Sphere(Shape):
    def __init__(self, position, radius, material):
        super().__init__(position, material)
        self.radius = radius
        self.type = "Sphere"

    def ray_intersect(self, orig, dir):
        L = sub(self.position, orig)
        tca = dot(L, dir)
        d2 = dot(L, L) - tca * tca

        if d2 > self.radius * self.radius:
            return None

        thc = (self.radius * self.radius - d2) ** 0.5
        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1

        if t0 < 0:
            return None

        P = add(orig, mul(dir, t0))
        normal = sub(P, self.position)
        normal = norm(normal)

        u = (atan2(normal[2], normal[0])) / (2 * pi) + 0.5
        v = acos(normal[1]) / pi

        return Intercept(point=P, normal=normal, distance=t0, texCoords=[u, v], rayDirection=dir, obj=self)

class Plane(Shape):
    def __init__(self, position, normal, material):
        super().__init__(position=position, material=material)
        self.normal = norm(normal)
        self.type = "Plane"

    def ray_intersect(self, orig, dir):
        denom = dot(dir, self.normal)

        if isclose(0, denom):
            return None

        num = dot(sub(self.position, orig), self.normal)
        t = num / denom

        if t < 0:
            return None

        P = add(orig, mul(dir, t))
        return Intercept(point=P,
                         normal=self.normal,
                         distance=t,
                         texCoords=None,
                         rayDirection=dir,
                         obj=self)

class Disc(Plane):
    def __init__(self, position, normal, radio, material):
        super().__init__(position=position, normal=normal, material=material)
        self.radio = radio
        self.type = "Disc"

    def ray_intersect(self, orig, dir):
        planeIntercept = super().ray_intersect(orig, dir)

        if planeIntercept is None:
            return None

        contact = sub(planeIntercept.point, self.position)
        contact_length = length(contact)

        if contact_length > self.radio:
            return None

        return planeIntercept

class AABB(Shape):
    # Axis-Aligned Bounding Box

    def __init__(self, position, sizes, material):
        super().__init__(position, material)
        self.sizes = sizes
        self.type = "AABB"

        # Planes
        self.planes = []

        rightPlane = Plane(position=[position[0] + sizes[0] / 2, position[1], position[2]], normal=[1, 0, 0], material=material)
        leftPlane = Plane(position=[position[0] - sizes[0] / 2, position[1], position[2]], normal=[-1, 0, 0], material=material)

        upPlane = Plane(position=[position[0], position[1] + sizes[1] / 2, position[2]], normal=[0, 1, 0], material=material)
        downPlane = Plane(position=[position[0], position[1] - sizes[1] / 2, position[2]], normal=[0, -1, 0], material=material)

        frontPlane = Plane([position[0], position[1], position[2] + sizes[2] / 2], [0, 0, 1], material=material)
        backPlane = Plane([position[0], position[1], position[2] - sizes[2] / 2], [0, 0, -1], material=material)

        self.planes.append(rightPlane)
        self.planes.append(leftPlane)
        self.planes.append(upPlane)
        self.planes.append(downPlane)
        self.planes.append(frontPlane)
        self.planes.append(backPlane)

        # Bounds
        self.boundsMin = [0, 0, 0]
        self.boundsMax = [0, 0, 0]

        epsilon = 0.001

        for i in range(3):
            self.boundsMin[i] = position[i] - (epsilon + sizes[i] / 2)
            self.boundsMax[i] = position[i] + (epsilon + sizes[i] / 2)

    def ray_intersect(self, orig, dir):
        intercept = None
        t = float("inf")
        for plane in self.planes:
            planeIntercept = plane.ray_intersect(orig, dir)

            if planeIntercept is not None:
                planePoint = planeIntercept.point

                if self.boundsMin[0] <= planePoint[0] <= self.boundsMax[0]:
                    if self.boundsMin[1] <= planePoint[1] <= self.boundsMax[1]:
                        if self.boundsMin[2] <= planePoint[2] <= self.boundsMax[2]:
                            if planeIntercept.distance < t:
                                t = planeIntercept.distance
                                intercept = planeIntercept
        if intercept is None:
            return None

        u, v = 0, 0
        if abs(intercept.normal[0]) > 0:
            u = (intercept.point[1] - self.boundsMin[1]) / self.sizes[1]
            v = (intercept.point[2] - self.boundsMin[2]) / self.sizes[2]
        elif abs(intercept.normal[1]) > 0:
            u = (intercept.point[0] - self.boundsMin[0]) / self.sizes[0]
            v = (intercept.point[2] - self.boundsMin[2]) / self.sizes[2]
        elif abs(intercept.normal[2]) > 0:
            u = (intercept.point[0] - self.boundsMin[0]) / self.sizes[0]
            v = (intercept.point[1] - self.boundsMin[1]) / self.sizes[1]

        u = min(0.999, max(0, u))
        v = min(0.999, max(0, v))

        return Intercept(point=intercept.point,
                         normal=intercept.normal,
                         distance=t,
                         texCoords=[u, v],
                         rayDirection=dir,
                         obj=self)

class Triangle(Shape):
    def __init__(self, v0, v1, v2, material):
        super().__init__(position=None, material=material)
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2
        self.normal = norm(cross(sub(v1, v0), sub(v2, v0)))
        self.type = "Triangle"

    def ray_intersect(self, orig, dir):
        # Möller–Trumbore ray-triangle intersection algorithm
        epsilon = 1e-5
        edge1 = sub(self.v1, self.v0)
        edge2 = sub(self.v2, self.v0)
        h = cross(dir, edge2)
        a = dot(edge1, h)

        if -epsilon < a < epsilon:
            return None

        f = 1.0 / a
        s = sub(orig, self.v0)
        u = f * dot(s, h)
        if u < 0.0 or u > 1.0:
            return None

        q = cross(s, edge1)
        v = f * dot(dir, q)
        if v < 0.0 or u + v > 1.0:
            return None

        t = f * dot(edge2, q)
        if t > epsilon:
            P = add(orig, mul(dir, t))
            return Intercept(point=P, normal=self.normal, distance=t, texCoords=None, rayDirection=dir, obj=self)
        else:
            return None

class Pyramid(Shape):
    def __init__(self, base_center, base_size, height, material):
        super().__init__(position=base_center, material=material)
        self.base_center = base_center
        self.base_size = base_size
        self.height = height
        self.type = "Pyramid"

        # Calculamos los vértices
        half_size = base_size / 2
        self.v0 = add(base_center, [-half_size, 0, -half_size])
        self.v1 = add(base_center, [half_size, 0, -half_size])
        self.v2 = add(base_center, [half_size, 0, half_size])
        self.v3 = add(base_center, [-half_size, 0, half_size])
        self.apex = add(base_center, [0, height, 0])

        # Triángulos de la pirámide
        self.faces = [
            Triangle(self.v0, self.v1, self.apex, material),
            Triangle(self.v1, self.v2, self.apex, material),
            Triangle(self.v2, self.v3, self.apex, material),
            Triangle(self.v3, self.v0, self.apex, material),
            Triangle(self.v0, self.v1, self.v2, material),  # Base
            Triangle(self.v2, self.v3, self.v0, material),  # Base
        ]

    def ray_intersect(self, orig, dir):
        intercepts = [face.ray_intersect(orig, dir) for face in self.faces]
        intercepts = [intercept for intercept in intercepts if intercept is not None]
        if not intercepts:
            return None
        intercept = min(intercepts, key=lambda i: i.distance)
        return intercept

class Cone(Shape):
    def __init__(self, position, radius, height, material):
        super().__init__(position=position, material=material)
        self.radius = radius
        self.height = height
        self.type = "Cone"

    def ray_intersect(self, orig, dir):
        # Ecuación del cono: (x^2 + z^2) = (r^2/h^2)(y - h)^2
        # Transformamos el rayo al sistema de coordenadas del cono
        co = sub(orig, self.position)
        k = self.radius / self.height
        k = k * k

        a = dir[0] ** 2 + dir[2] ** 2 - k * dir[1] ** 2
        b = 2 * (co[0] * dir[0] + co[2] * dir[2] - k * co[1] * dir[1])
        c = co[0] ** 2 + co[2] ** 2 - k * co[1] ** 2

        disc = b * b - 4 * a * c
        if disc < 0:
            return None

        sqrt_disc = sqrt(disc)
        t0 = (-b - sqrt_disc) / (2 * a)
        t1 = (-b + sqrt_disc) / (2 * a)

        t = min(t0, t1)
        if t < 0:
            t = max(t0, t1)
            if t < 0:
                return None

        P = add(orig, mul(dir, t))
        y = P[1] - self.position[1]
        if y < 0 or y > self.height:
            return None

        # Calculamos la normal
        normal = [P[0] - self.position[0], k * (P[1] - self.position[1]), P[2] - self.position[2]]
        normal = norm(normal)
        return Intercept(point=P, normal=normal, distance=t, texCoords=None, rayDirection=dir, obj=self)

class OBB(Shape):
    # Oriented Bounding Box
    def __init__(self, position, sizes, rotation, material):
        super().__init__(position=position, material=material)
        self.sizes = sizes
        self.rotation = rotation  # Rotación en radianes [rx, ry, rz]
        self.type = "OBB"

        # Matrices de rotación
        self.rotation_matrix = self.get_rotation_matrix()

        # Inversa de la matriz de rotación
        self.inverse_rotation = self.get_inverse_rotation_matrix()

    def get_rotation_matrix(self):
        rx, ry, rz = self.rotation
        sx, cx = sin(rx), cos(rx)
        sy, cy = sin(ry), cos(ry)
        sz, cz = sin(rz), cos(rz)

        rotation_x = [
            [1, 0, 0],
            [0, cx, -sx],
            [0, sx, cx]
        ]

        rotation_y = [
            [cy, 0, sy],
            [0, 1, 0],
            [-sy, 0, cy]
        ]

        rotation_z = [
            [cz, -sz, 0],
            [sz, cz, 0],
            [0, 0, 1]
        ]

        # Multiplicamos las matrices: R = Rz * Ry * Rx
        rotation_matrix = self.matrix_multiply(rotation_z, self.matrix_multiply(rotation_y, rotation_x))
        return rotation_matrix

    def get_inverse_rotation_matrix(self):
        # La inversa de una matriz de rotación es su transpuesta
        return [list(i) for i in zip(*self.rotation_matrix)]

    def matrix_multiply(self, A, B):
        result = []
        for i in range(len(A)):
            row = []
            for j in range(len(B[0])):
                val = sum(A[i][k] * B[k][j] for k in range(len(B)))
                row.append(val)
            result.append(row)
        return result

    def transform_point(self, point, matrix):
        x, y, z = point
        tx = matrix[0][0]*x + matrix[0][1]*y + matrix[0][2]*z
        ty = matrix[1][0]*x + matrix[1][1]*y + matrix[1][2]*z
        tz = matrix[2][0]*x + matrix[2][1]*y + matrix[2][2]*z
        return [tx, ty, tz]

    def ray_intersect(self, orig, dir):
        # Transformamos el rayo al espacio del OBB
        co = sub(orig, self.position)
        orig_local = self.transform_point(co, self.inverse_rotation)
        dir_local = self.transform_point(dir, self.inverse_rotation)

        # Usamos el método de intersección del AABB en el espacio local
        t_min = [(-self.sizes[i]/2 - orig_local[i]) / dir_local[i] if dir_local[i] != 0 else float('-inf') for i in range(3)]
        t_max = [(self.sizes[i]/2 - orig_local[i]) / dir_local[i] if dir_local[i] != 0 else float('inf') for i in range(3)]

        t1 = [min(t_min[i], t_max[i]) for i in range(3)]
        t2 = [max(t_min[i], t_max[i]) for i in range(3)]

        t_near = max(t1)
        t_far = min(t2)

        if t_near > t_far or t_far < 0:
            return None

        t = t_near if t_near > 0 else t_far

        P_local = add(orig_local, mul(dir_local, t))

        # Calculamos la normal en el espacio local
        normal_local = [0, 0, 0]
        for i in range(3):
            if abs(P_local[i] - (-self.sizes[i]/2)) < 1e-3:
                normal_local[i] = -1
            elif abs(P_local[i] - (self.sizes[i]/2)) < 1e-3:
                normal_local[i] = 1

        # Transformamos el punto y la normal al espacio global
        P_world = add(self.position, self.transform_point(P_local, self.rotation_matrix))
        normal_world = norm(self.transform_point(normal_local, self.rotation_matrix))

        return Intercept(point=P_world, normal=normal_world, distance=t, texCoords=None, rayDirection=dir, obj=self)

class Cylinder(Shape):
    def __init__(self, position, radius, height, material):
        super().__init__(position=position, material=material)
        self.radius = radius
        self.height = height
        self.type = "Cylinder"

    def ray_intersect(self, orig, dir):
        # Ecuación del cilindro infinito: x^2 + z^2 = r^2
        # Luego verificamos si la intersección está dentro de las tapas superior e inferior

        co = sub(orig, self.position)
        a = dir[0] ** 2 + dir[2] ** 2
        b = 2 * (co[0] * dir[0] + co[2] * dir[2])
        c = co[0] ** 2 + co[2] ** 2 - self.radius ** 2

        disc = b * b - 4 * a * c
        if disc < 0:
            return None

        sqrt_disc = sqrt(disc)
        t0 = (-b - sqrt_disc) / (2 * a)
        t1 = (-b + sqrt_disc) / (2 * a)

        t = t0 if t0 > 0 else t1
        if t < 0:
            return None

        y = co[1] + t * dir[1]
        if y < 0 or y > self.height:
            return None

        P = add(orig, mul(dir, t))
        normal = [P[0] - self.position[0], 0, P[2] - self.position[2]]
        normal = norm(normal)
        return Intercept(point=P, normal=normal, distance=t, texCoords=None, rayDirection=dir, obj=self)

class Torus(Shape):
    def __init__(self, position, major_radius, minor_radius, material):
        super().__init__(position=position, material=material)
        self.major_radius = major_radius  # Radio desde el centro hasta el centro del tubo
        self.minor_radius = minor_radius  # Radio del tubo
        self.type = "Torus"

    def ray_intersect(self, orig, dir):
        # El algoritmo de intersección con un toroide es complejo y requiere resolver una ecuación de cuarto grado.
        # Por simplicidad, usaremos una aproximación numérica o descartaremos su implementación detallada aquí.

        # Placeholder para indicar que no está implementado completamente
        return None

class Ellipsoid(Shape):
    def __init__(self, position, radii, material):
        super().__init__(position=position, material=material)
        self.radii = radii  # [rx, ry, rz]
        self.type = "Ellipsoid"

    def ray_intersect(self, orig, dir):
        # Ecuación del elipsoide: (x/a)^2 + (y/b)^2 + (z/c)^2 = 1
        # Transformamos el rayo al espacio del elipsoide

        co = sub(orig, self.position)
        co = [co[i] / self.radii[i] for i in range(3)]
        dir = [dir[i] / self.radii[i] for i in range(3)]

        a = dot(dir, dir)
        b = 2 * dot(co, dir)
        c = dot(co, co) - 1

        disc = b * b - 4 * a * c
        if disc < 0:
            return None

        sqrt_disc = sqrt(disc)
        t0 = (-b - sqrt_disc) / (2 * a)
        t1 = (-b + sqrt_disc) / (2 * a)

        t = min(t0, t1)
        if t < 0:
            t = max(t0, t1)
            if t < 0:
                return None

        P = add(orig, mul(dir, t))
        normal = [P[i] / (self.radii[i] ** 2) for i in range(3)]
        normal = norm(normal)
        return Intercept(point=P, normal=normal, distance=t, texCoords=None, rayDirection=dir, obj=self)