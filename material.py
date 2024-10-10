from MathLib import reflectVector, dot, sub, add, mul, div, length
from refractionFunctions import *

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2
EMISSIVE = 3

class Material(object):
    def __init__(self, diffuse=[0, 0, 0], spec=1.0, ks=0.0, ior=1.0, texture=None, matType=OPAQUE):
        self.diffuse = diffuse
        self.spec = spec
        self.ks = ks
        self.ior = ior
        self.texture = texture
        self.matType = matType

    def GetSurfaceColor(self, intercept, renderer, recursion=0):
        if self.matType == EMISSIVE:
            # Los materiales emisivos devuelven su color difuso sin afectación de luces
            return self.diffuse

        lightColor = [0, 0, 0]
        reflectColor = [0, 0, 0]
        refractColor = [0, 0, 0]
        finalColor = self.diffuse[:]

        if self.texture and intercept.texCoords:
            textureColor = self.texture.getColor(intercept.texCoords[0], intercept.texCoords[1])
            finalColor = [finalColor[i] * textureColor[i] for i in range(3)]

        for light in renderer.lights:
            shadowIntercept = None
            lightDir = None

            if light.lightType == "Directional":
                lightDir = mul(light.direction, -1)
                shadowIntercept = renderer.glCastRay(intercept.point, lightDir, intercept.obj)
            elif light.lightType == "Point":
                lightDir = sub(light.position, intercept.point)
                R = length(lightDir)
                lightDir = div(lightDir, R)
                shadowIntercept = renderer.glCastRay(intercept.point, lightDir, intercept.obj)
                if shadowIntercept and shadowIntercept.distance >= R:
                    shadowIntercept = None
            elif light.lightType == "Ambient":
                pass  # La luz ambiental no crea sombras
            elif light.lightType == "Spot":
                lightDir = sub(light.position, intercept.point)
                R = length(lightDir)
                lightDir = div(lightDir, R)
                theta = acos(dot(lightDir, mul(light.direction, -1))) * (180 / pi)
                if theta < light.innerAngle:
                    intensity = light.intensity
                elif theta < light.outerAngle:
                    intensity = light.intensity * (1 - (theta - light.innerAngle) / (light.outerAngle - light.innerAngle))
                else:
                    intensity = 0
                if intensity > 0:
                    shadowIntercept = renderer.glCastRay(intercept.point, lightDir, intercept.obj)
                    if shadowIntercept and shadowIntercept.distance >= R:
                        shadowIntercept = None
                else:
                    continue

            if shadowIntercept is None:
                lightColor = [lightColor[i] + light.GetLightColor(intercept)[i] for i in range(3)]

        if self.matType == REFLECTIVE:
            rayDir = mul(intercept.rayDirection, -1)
            reflect = reflectVector(intercept.normal, rayDir)
            reflectIntercept = renderer.glCastRay(intercept.point, reflect, intercept.obj, recursion + 1)
            if reflectIntercept:
                reflectColor = reflectIntercept.obj.material.GetSurfaceColor(reflectIntercept, renderer, recursion + 1)
            else:
                reflectColor = renderer.glEnvMapColor(intercept.point, reflect)
                if reflectColor is None:
                    reflectColor = [0, 0, 0]
            finalColor = [finalColor[i] + reflectColor[i] * self.ks for i in range(3)]

        elif self.matType == TRANSPARENT:
            outside = dot(intercept.normal, intercept.rayDirection) < 0
            bias = mul(intercept.normal, 0.001)
            rayDir = mul(intercept.rayDirection, -1)
            reflect = reflectVector(intercept.normal, rayDir)
            reflectOrig = add(intercept.point, bias) if outside else sub(intercept.point, bias)
            reflectIntercept = renderer.glCastRay(reflectOrig, reflect, None, recursion + 1)

            if reflectIntercept:
                reflectColor = reflectIntercept.obj.material.GetSurfaceColor(reflectIntercept, renderer, recursion + 1)
            else:
                reflectColor = renderer.glEnvMapColor(intercept.point, reflect)
                if reflectColor is None:
                    reflectColor = [0, 0, 0]

            refract = refractVector(intercept.normal, intercept.rayDirection, 1.0, self.ior)

            if refract is None:
                # Ocurre reflexión interna total
                kr = 1.0
                kt = 0.0
                refractColor = [0, 0, 0]
            else:
                refractOrig = sub(intercept.point, bias) if outside else add(intercept.point, bias)
                refractIntercept = renderer.glCastRay(refractOrig, refract, None, recursion + 1)

                if refractIntercept:
                    refractColor = refractIntercept.obj.material.GetSurfaceColor(refractIntercept, renderer, recursion + 1)
                else:
                    refractColor = renderer.glEnvMapColor(intercept.point, refract)
                    if refractColor is None:
                        refractColor = [0, 0, 0]

                kr, kt = fresnel(intercept.normal, intercept.rayDirection, 1.0, self.ior)
                reflectColor = [i * kr for i in reflectColor]
                refractColor = [i * kt for i in refractColor]

            finalColor = [finalColor[i] + reflectColor[i] * self.ks + refractColor[i] * self.ks for i in range(3)]
        else:
            # Material OPAQUE
            finalColor = [finalColor[i] * lightColor[i] for i in range(3)]

        finalColor = [min(1, finalColor[i]) for i in range(3)]
        return finalColor
