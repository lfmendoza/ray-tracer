from intercept import Intercept
from math import atan2, acos, pi, isclose, sin, cos, sqrt
from MathLib import cross, dot, sub, add, mul, norm, length, matrix_multiply

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

        thc = sqrt(self.radius * self.radius - d2)
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
class Tetrahedron(Shape):
    def __init__(self, position, size, material):
        super().__init__(position=position, material=material)
        self.size = size
        self.type = "Tetrahedron"

        h = size * sqrt(2 / 3)
        self.vertices = [
            add(position, [0, h / sqrt(2), 0]),  # Apex
            add(position, [-size / 2, -h / (2 * sqrt(2)), size / (2 * sqrt(3))]),
            add(position, [size / 2, -h / (2 * sqrt(2)), size / (2 * sqrt(3))]),
            add(position, [0, -h / (2 * sqrt(2)), -size / sqrt(3)])
        ]

        # Faces (triangles)
        self.faces = [
            Triangle(self.vertices[0], self.vertices[1], self.vertices[2], material),
            Triangle(self.vertices[0], self.vertices[2], self.vertices[3], material),
            Triangle(self.vertices[0], self.vertices[3], self.vertices[1], material),
            Triangle(self.vertices[1], self.vertices[3], self.vertices[2], material)
        ]

    def ray_intersect(self, orig, dir):
        intercepts = [face.ray_intersect(orig, dir) for face in self.faces]
        intercepts = [intercept for intercept in intercepts if intercept is not None]
        if not intercepts:
            return None
        intercept = min(intercepts, key=lambda i: i.distance)
        return intercept
class Prism(Shape):
    def __init__(self, position, radius, height, sides, rotation, material):
        super().__init__(position=position, material=material)
        self.radius = radius
        self.height = height
        self.sides = sides
        self.rotation = rotation  # En radianes
        self.type = "Prism"

        angle = 2 * pi / sides
        self.vertices_top = []
        self.vertices_bottom = []
        for i in range(sides):
            x = self.radius * cos(i * angle + self.rotation)
            z = self.radius * sin(i * angle + self.rotation)
            self.vertices_top.append([x, self.height / 2, z])
            self.vertices_bottom.append([x, -self.height / 2, z])

        # Transformar vértices a la posición del prisma
        self.vertices_top = [add(self.position, v) for v in self.vertices_top]
        self.vertices_bottom = [add(self.position, v) for v in self.vertices_bottom]

        # Crear las caras
        self.faces = []
        for i in range(sides):
            next_i = (i + 1) % sides
            # Caras laterales
            self.faces.append(Triangle(self.vertices_bottom[i], self.vertices_top[i], self.vertices_top[next_i], self.material))
            self.faces.append(Triangle(self.vertices_bottom[i], self.vertices_top[next_i], self.vertices_bottom[next_i], self.material))
        # Caras superior e inferior
        for i in range(1, sides - 1):
            # Cara superior
            self.faces.append(Triangle(self.vertices_top[0], self.vertices_top[i], self.vertices_top[i + 1], self.material))
            # Cara inferior
            self.faces.append(Triangle(self.vertices_bottom[0], self.vertices_bottom[i + 1], self.vertices_bottom[i], self.material))

    def ray_intersect(self, orig, dir):
        intercepts = [face.ray_intersect(orig, dir) for face in self.faces]
        intercepts = [i for i in intercepts if i is not None]
        if not intercepts:
            return None
        intercept = min(intercepts, key=lambda i: i.distance)
        return intercept
class Disc(Shape):
    def __init__(self, position, normal, radius, material):
        super().__init__(position=position, material=material)
        self.normal = norm(normal)
        self.radius = radius
        self.type = "Disc"

    def ray_intersect(self, orig, dir):
        # Primero, verificamos la intersección con el plano en el que se encuentra el disco
        denom = dot(dir, self.normal)
        if abs(denom) < 1e-6:
            # El rayo es paralelo al plano
            return None

        t = dot(sub(self.position, orig), self.normal) / denom
        if t < 0:
            # La intersección está detrás del origen del rayo
            return None

        P = add(orig, mul(dir, t))
        dist = sqrt(sum([(P[i] - self.position[i]) ** 2 for i in range(3)]))
        if dist > self.radius:
            # El punto de intersección está fuera del disco
            return None

        # Calculamos las coordenadas de textura (u, v) si es necesario
        u = (P[0] - self.position[0]) / (2 * self.radius) + 0.5
        v = (P[2] - self.position[2]) / (2 * self.radius) + 0.5

        return Intercept(point=P, normal=self.normal, distance=t, texCoords=[u, v], rayDirection=dir, obj=self)
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
class Ellipsoid(Shape):
    def __init__(self, position, radii, material):
        super().__init__(position=position, material=material)
        self.radii = radii  # [rx, ry, rz]
        self.type = "Ellipsoid"

    def ray_intersect(self, orig, dir):
        # Ecuación del elipsoide: (x/a)^2 + (y/b)^2 + (z/c)^2 = 1
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
        normal = [2 * (P[i] - self.position[i]) / (self.radii[i] ** 2) for i in range(3)]
        normal = norm(normal)
        return Intercept(point=P, normal=normal, distance=t, texCoords=None, rayDirection=dir, obj=self)

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
