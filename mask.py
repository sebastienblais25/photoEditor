#class permttant de creer un masque pour nos photos
class mask:

    heigth = 0
    width = 0
    tab = [[]]

    # constructeur qui initialise la matrice qui va servir de masque
    def __init__(self, h, w):

        self.heigth = h
        self.width = w
        self.tab = [[0 for x in range(w)] for y in range(h)]

    # set la valeur d'un point du masque dans l'objet
    def setMaskPoint(self, i,j, valeur):

        self.tab[i][j] = valeur

    #set le masque au complet en recevant la liste des points d'interet
    def setMask(self, mat):
        k = 0
        # for pour la premiere dimension de la matrice
        for i in range(self.heigth):

            # for pour la deuxieme dimension de la matrice
            for j in range(self.width):

                #pour ne pas depasser l'index lorsque le pixel d'interet est passer
                if (k < len(mat)):
                    if i == mat[k].pointx and j == mat[k].pointy:

                        self.tab[i][j] = 1
                        k += 1
                    else:

                        self.tab[i][j] = 0

        return self.tab

    # Affichage du masque
    def printMask(self):

        for i in range(self.heigth):
            for j in range(self.width):
                if self.tab[i][j] == 1:
                    print(self.tab[i])
