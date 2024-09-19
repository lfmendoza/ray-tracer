import numpy as np
from MathLib import reflectVector

class Light(object):
    def __init__(self, color = [1,1,1], intesity = 1.0, lightType = "None"):
        self.color = color
        self.intesity = intesity
        self.lightType = lightType
    
    def GetLightColor(self, intercept= None):
        return [(i * self.intesity) for i in self.color]
    
    def GetSpecularColor(self, intercept, viewPos):
        return [0,0,0]
    
class AmbientLight(Light):
    def __init__(self, color=[1, 1, 1], intesity=1.0):
        super().__init__(color, intesity, "Ambient")

class DirectionalLight(Light):
    def __init__(self, color=[1, 1, 1], intesity=1, direction=[0,-1,0]):
        super().__init__(color, intesity, "Directional")
        self.direction = direction / np.linalg.norm(direction)

    def GetLightColor(self, intercept = None):
        lightColor = super().GetLightColor()
        if intercept:
            dir = [(i * -1) for i in self.direction]
            intensity = np.dot(intercept.normal, dir)
            intensity = max(0, min(1, intensity))
            intensity *= (1 - intercept.obj.material.ks)
            lightColor = [(i * intensity) for i in lightColor]
        return lightColor
    
    def GetSpecularColor(self, intercept, viewPos):
        specColor = super().GetSpecularColor(intercept, viewPos)

        if intercept:
            dir = [(i * -1) for i in self.direction]
            reflect = reflectVector(intercept.normal, dir)

            viewDir = np.subtract(viewPos, intercept.point)
            viewDir /= np.linalg.norm(viewDir)

            # Specular ((V * R)^ks) 
            specularity = max(0, np.dot(viewDir, reflect)) ** intercept.obj.material.spec
            specularity *= intercept.obj.material.ks
            specularity *= self.intesity
            specColor = [(i * specularity) for i in specColor]

        return specColor