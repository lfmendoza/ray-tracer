from MathLib import dot, sub, add, mul, norm, length, div, reflectVector
from math import cos, pi

class Light(object):
    def __init__(self, color=[1, 1, 1], intensity=1.0, lightType="None"):
        self.color = color
        self.intensity = intensity
        self.lightType = lightType

    def GetLightColor(self, intercept=None):
        return [i * self.intensity for i in self.color]

    def GetSpecularColor(self, intercept, viewPos):
        return [0, 0, 0]

class AmbientLight(Light):
    def __init__(self, color=[1, 1, 1], intensity=1.0):
        super().__init__(color, intensity, "Ambient")

class DirectionalLight(Light):
    def __init__(self, color=[1, 1, 1], intensity=1, direction=[0, -1, 0]):
        super().__init__(color, intensity, "Directional")
        self.direction = norm(direction)

    def GetLightColor(self, intercept=None):
        lightColor = super().GetLightColor()
        if intercept:
            dir_neg = mul(self.direction, -1)
            intensity = dot(intercept.normal, dir_neg)
            intensity = max(0, min(1, intensity))
            intensity *= (1 - intercept.obj.material.ks)
            lightColor = [i * intensity for i in lightColor]
        return lightColor

    def GetSpecularColor(self, intercept, viewPos):
        specColor = super().GetSpecularColor(intercept, viewPos)

        if intercept:
            dir_neg = mul(self.direction, -1)
            reflect = reflectVector(intercept.normal, dir_neg)

            viewDir = sub(viewPos, intercept.point)
            viewDir = norm(viewDir)

            specularity = max(0, dot(viewDir, reflect)) ** intercept.obj.material.spec
            specularity *= intercept.obj.material.ks
            specularity *= self.intensity
            specColor = [i * specularity for i in self.color]

        return specColor

class PointLight(Light):
    def __init__(self, color=[1, 1, 1], intensity=1, position=[0, 0, 0]):
        super().__init__(color, intensity)
        self.position = position
        self.lightType = "Point"

    def GetLightColor(self, intercept=None):
        lightColor = super().GetLightColor(intercept)

        if intercept:
            dir = sub(self.position, intercept.point)
            R = length(dir)
            dir = div(dir, R)

            intensity = dot(intercept.normal, dir)
            intensity = max(0, min(1, intensity))
            intensity *= (1 - intercept.obj.material.ks)
            intensity *= self.intensity

            if R != 0:
                intensity /= R ** 2

            lightColor = [i * intensity for i in lightColor]

        return lightColor

    def GetSpecularColor(self, intercept, viewPos):
        specColor = super().GetSpecularColor(intercept, viewPos)

        if intercept:
            dir = sub(self.position, intercept.point)
            R = length(dir)
            dir = div(dir, R)

            reflect = reflectVector(intercept.normal, dir)

            viewDir = sub(viewPos, intercept.point)
            viewDir = norm(viewDir)

            specularity = max(0, dot(viewDir, reflect)) ** intercept.obj.material.spec
            specularity *= intercept.obj.material.ks
            specularity *= self.intensity

            if R != 0:
                specularity /= R ** 2

            specColor = [i * specularity for i in self.color]

        return specColor

class SpotLight(PointLight):
    def __init__(self, color=[1, 1, 1], intensity=1, position=[0, 0, 0], direction=[0, -1, 0], innerAngle=50, outerAngle=60):
        super().__init__(color, intensity, position)
        self.direction = norm(direction)
        self.innerAngle = innerAngle
        self.outerAngle = outerAngle
        self.lightType = "Spot"

    def GetLightColor(self, intercept=None):
        lightColor = super().GetLightColor(intercept)

        if intercept:
            attenuation = self.SpotLightAttenuation(intercept)
            lightColor = [i * attenuation for i in lightColor]
        return lightColor

    def GetSpecularColor(self, intercept, viewPos):
        specularColor = super().GetSpecularColor(intercept, viewPos)
        if intercept:
            attenuation = self.SpotLightAttenuation(intercept)
            specularColor = [i * attenuation for i in specularColor]
        return specularColor

    def SpotLightAttenuation(self, intercept):
        if intercept is None:
            return 0

        wi = sub(self.position, intercept.point)
        wi = norm(wi)
        innerAngleRads = self.innerAngle * pi / 180
        outerAngleRads = self.outerAngle * pi / 180

        attenuation = (-dot(self.direction, wi) - cos(outerAngleRads)) / (cos(innerAngleRads) - cos(outerAngleRads))
        attenuation = min(1, max(0, attenuation))
        return attenuation
