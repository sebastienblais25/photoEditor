#classe permettant d'entrer un pixel d'interet avec sa position
class pixelInteret:

    pointx = 0
    pointy = 0
    pixel = []

    # constructeur permettant de construire l'objet avec la position du pixel
    def __init__(self, x, y):
        self.pointx = x
        self.pointy = y
        self.pixel = [0 for i in range(4)]

    # Setteur permettant de placer une position et unpixel
    def setpoint(self, x, y, pixel):
        self.pointx = x
        self.pointy = y
        self.pixel = pixel