from obj import Obj
from MathLib import *
from material import Material
from figures import Triangle


class Model(object):
    def __init__(self, filename):
        objFile = Obj(filename)

        self.vertices = objFile.vertices
        self.texCoords = objFile.texcoords
        self.normals = objFile.normals
        self.faces = objFile.faces

        self.translate = [0, 0, 0]
        self.rotate = [0, 0, 0]
        self.scale = [1, 1, 1]

        self.texture = None
        self.material = Material()

    def GetModelMatrix(self):
        translateMat = TranslationMatrix(self.translate[0],
                                         self.translate[1],
                                         self.translate[2])

        rotateMat = RotationMatrix(self.rotate[0],
                                   self.rotate[1],
                                   self.rotate[2])

        scaleMat = ScaleMatrix(self.scale[0],
                               self.scale[1],
                               self.scale[2])

        return matrix_multiply(matrix_multiply(translateMat, rotateMat), scaleMat)

    def LoadTexture(self, filename):
        self.texture = Texture(filename)

    def get_faces(self):
        model_matrix = self.GetModelMatrix()
        transformed_faces = []
        for face in self.faces:
            v0 = transform(self.vertices[face[0][0] - 1], model_matrix)
            v1 = transform(self.vertices[face[1][0] - 1], model_matrix)
            v2 = transform(self.vertices[face[2][0] - 1], model_matrix)
            triangle = Triangle(v0, v1, v2, self.material)
            transformed_faces.append(triangle)
        return transformed_faces
