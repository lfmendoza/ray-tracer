from MathLib import reflectVector
from refractionFunctions import *

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2

class Material(object):
    def __init__(self, diffuse = [0,0,0], spec = 1.0, ks = 0.0, ior = 1.0, texture = None, matType = OPAQUE):
        self.diffuse = diffuse
        self.spec = spec
        self.ks = ks
        self.ior = ior
        self.texture = texture
        self.matType = matType

    def GetSurfaceColor(self, intercept, renderer, recursion = 0):
        # Phong reflection modle
        # LightColors = LightColor + Specular
        # FinalColor = DiffuseColor * LightColor

        lightColor = [0,0,0]
        reflectColor = [0,0,0]
        refractColor = [0,0,0]
        finalColor = self.diffuse

        if self.texture and intercept.texCoords:
            textureColor = self.texture.getColor(intercept.texCoords[0], intercept.texCoords[1])
            finalColor = [finalColor[i] * textureColor[i] for i in range(3)]

        for light in renderer.lights:
            shadowIntercept = None

            if light.lightType == "Directional":
                lightDir = [-i for i in light.direction]
                shadowIntercept = renderer.glCastRay(intercept.point, lightDir, intercept.obj)

            if shadowIntercept == None:
                lightColor = [(lightColor[i] + light.GetSpecularColor(intercept, renderer.camera.translate)[i]) for i in range(3)]

                if self.matType == OPAQUE:
                    lightColor = [(lightColor[i] + light.GetLightColor(intercept)[i]) for i in range(3)]
        
        if self.matType == REFLECTIVE:
            rayDir = [-i for i in intercept.rayDirection]
            reflect = reflectVector(intercept.normal, rayDir)
            reflectIntercept = renderer.glCastRay(intercept.point, reflect, intercept.obj, recursion + 1)
            if reflectIntercept != None:
                reflectColor = reflectIntercept.obj.material.GetSurfaceColor(reflectIntercept, renderer, recursion + 1)
            else:
                reflectColor = renderer.glEnvMapColor(intercept.point, reflect)

        elif self.matType == TRANSPARENT:
            # Revisamos si estamos afuera
            outside = np.dot(intercept.normal, intercept.rayDirection) < 0

            # Agregar margen de error
            bias = [i * 0.001 for i in intercept.normal]

            # Generamos los rayos de refleccion
            rayDir = [-i for i in intercept.rayDirection]
            reflect = reflectVector(intercept.normal, rayDir)
            reflectOrig = np.add(intercept.point, bias) if outside else np.subtract(intercept.point, bias)
            reflectIntercept = renderer.glCastRay(reflectOrig, reflect, None, recursion + 1)

            if reflectIntercept != None:
                reflectColor = reflectIntercept.obj.material.GetSurfaceColor(reflectIntercept, renderer, recursion + 1)
            else:
                reflectColor = renderer.glEnvMapColor(intercept.point, reflect)

            # Generamos los rayos de refraccion
            if not totalInternalReflection(intercept.normal, intercept.rayDirection, 1.0, self.ior):
                refract = refractVector(intercept.normal, intercept.rayDirection, 1.0, self.ior)
                refractOrig = np.subtract(intercept.point, bias) if outside else np.add(intercept.point, bias)
                refractIntercept = renderer.glCastRay(refractOrig, refract, None, recursion + 1)

                if refractIntercept != None:
                    refractColor = refractIntercept.obj.material.GetSurfaceColor(refractIntercept, renderer, recursion + 1)
                else:
                    refractColor = renderer.glEnvMapColor(intercept.point, reflect)
                
                # Usando las ecuaciones de Fresne, determinamos cuanta refleccion
                # y cuanta refraccion agregar al color final
                kr, kt = fresnel(intercept.normal, intercept.rayDirection, 1.0, self.ior)
                reflectColor = [i * kr for i in reflectColor]
                refractColor = [i * kt for i in refractColor]

        finalColor = [(finalColor[i] * (lightColor[i] + reflectColor[i] + refractColor[i])) for i in range(3)]
        finalColor = [min(1, finalColor[i]) for i in range(3)]
        return finalColor
