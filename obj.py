class Obj(object):
    def __init__(self, filename):
        with open(filename, "r") as file:
            lines = file.read().splitlines()

        self.vertices = []
        self.texcoords = []
        self.normals = []
        self.faces = []

        for line in lines:
            line = line.strip()
            if line == "" or line.startswith("#"):
                continue

            parts = line.split()
            prefix = parts[0]
            values = parts[1:]

            if prefix == "v":
                self.vertices.append([float(v) for v in values])
            elif prefix == "vt":
                self.texcoords.append([float(v) for v in values])
            elif prefix == "vn":
                self.normals.append([float(v) for v in values])
            elif prefix == "f":
                face = []
                for v in values:
                    w = v.split('/')
                    vertex = [int(w[0])]
                    if len(w) > 1 and w[1] != '':
                        vertex.append(int(w[1]))
                    else:
                        vertex.append(0)
                    if len(w) > 2 and w[2] != '':
                        vertex.append(int(w[2]))
                    else:
                        vertex.append(0)
                    face.append(vertex)
                self.faces.append(face)
