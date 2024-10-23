from MathLib import TranslationMatrix, RotationMatrix, matrix_multiply

class Camera(object):
    def __init__(self):
        self.translate = [0, 0, 0]
        self.rotate = [0, 0, 0]

    def GetViewMatrix(self):
        # Negative translation and rotation for the view matrix
        translateMat = TranslationMatrix(-self.translate[0],
                                         -self.translate[1],
                                         -self.translate[2])

        rotateMat = RotationMatrix(-self.rotate[0],
                                   -self.rotate[1],
                                   -self.rotate[2])

        camMatrix = matrix_multiply(rotateMat, translateMat)
        return camMatrix
