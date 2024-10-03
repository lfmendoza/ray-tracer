from intercept import Intercept
from math import atan2, acos, pi, isclose
from MathLib import dot, sub, add, mul, norm, length

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
