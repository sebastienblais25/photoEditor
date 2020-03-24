###### Import #######
from PIL import Image
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
#import pandas as pd
#import xlrd
from pixelInteret import pixelInteret
from mask import mask

############### Function ###################

# fonction qui applique un filtre de la libraire mathplotlib
def applyfilter(photo, namefilter):
    lum_img = photo[:, :, 0]
    # enleve le contour
    plt.xticks([])
    plt.yticks([])
    plt.axis('off')
    plt.tight_layout()

    # Application du filtre
    plt.imshow(lum_img, cmap=namefilter)

# fonction qui enregistre une image
def saveImg(name):
    plt.savefig(name, bbox_inches='tight',pad_inches=0)

#
def pixelMask(mask, width, height):

    for i in range(height):
        for j in range(width):
            # losque la valeur du masque est zero,
            # on place un pixel transparent
            if mask[i][j] == 0:
                mask[i][j] = [0,0,0,0]

            # losque la valeur du masque est zero,
            # on place un pixel opaque
            if mask[i][j] == 1:
                mask[i][j] = [0,0,0,255]

    # retourne le nouveau masque
    return mask

# Analyse d'une photo avec le filtre envoyer en parametre
# afin de realiser une analyse pour chaque photo
def analysisphoto(img, filtre):

    # Les pixels d'interet pour chaque filtre
    if filtre == 0:
        rmin = 150
        rmax = 255
        gmin = 0
        gmax = 207
        bmin = 0
        bmax = 100
        wmin = 150
        wmax = 240
    elif filtre == 1:
        rmin = 230
        rmax = 250
        gmin = 230
        gmax = 255
        bmin = 230
        bmax = 255
        wmin = 0
        wmax = 0
    else:
        rmin = 0
        rmax = 20
        gmin = 0
        gmax = 20
        bmin = 0
        bmax = 20
        wmin = 0
        wmax = 0

    # les dimensions de la matrice
    width, height = img.size
    count = 0
    pix1 = np.asarray(img)

    lel = []
    for i in range(height):

        for j in range(width):
            # Application du filtre hot
            if filtre == 1:
                good = 0
                goodi =0
                gucci = 0
                if pix1[i][j][0] >rmin :

                    goodi = 1
                if pix1[i][j][1] >gmin:

                    gucci = 1
                if pix1[i][j][2] > bmin:

                    good = 1

                if good == 1 and goodi == 1 and gucci ==1:
                    positionpixel = pixelInteret(0, 0)

                    positionpixel.setpoint(i, j, pix1[i][j])

                    lel.append(positionpixel)

                    count += 1
            # Application des deux autres filtre
            else:
                if pix1[i][j][0] > rmin and pix1[i][j][0] < rmax:

                    if pix1[i][j][1] > gmin and pix1[i][j][1] < gmax:

                        if pix1[i][j][2] > bmin and pix1[i][j][2] < bmax:

                            positionpixel = pixelInteret(0, 0)

                            positionpixel.setpoint(i,j,pix1[i][j])

                            lel.append(positionpixel)

                            count += 1
                elif pix1[i][j][0] > wmin and pix1[i][j][0] < wmax and (pix1[i][j][0] == pix1[i][j][1] == pix1[i][j][2]):
                    positionpixel = pixelInteret(0, 0)

                    positionpixel.setpoint(i, j, pix1[i][j])

                    lel.append(positionpixel)

                    count += 1
    print(count)

    # Initialisation du masque
    masque = mask(height, width)

    # realisation du prmeier masque
    mask1 = masque.setMask(lel)

    # realistion du masque avec les pixels
    mask1 = pixelMask(mask1, width, height)
    print('done')

    return mask1


# Tranfomation d'une matrice numpy en image
def transformMatrixToImage(lel, name):
    allo = np.asanyarray(lel)
    allo = np.uint8(allo)
    output = Image.fromarray(allo)
    output.save(name)


# comparaison de trois mask
def compareMask(one, two, three):
    # For pour la longueur du mask
    for i in range(len(one)):
        # For pour la largeur du masque
        for j in range(len(one[0])):
            # enlever une bande de 20 pixel autour de la photo afin de faire la comparaison
            if i > 20 and j > 20:
                if i < (len(one)-20) and j < (len(one[0])-20):
                    count = 0
                    # Les for pour faire une verification de 20 pixel autour du pixel d'interet
                    for k in range(10):
                        for l in range(10):
                            # quadran ++
                            if one[i][j][3] == two[i + k][j + l][3]:
                                count = + 1
                            # quadran --
                            if one[i][j][3] == two[i - k][j - l][3]:
                                count = + 1

                            if k > 1:
                                # quadran -+
                                if one[i][j][3] == two[i + k][j - l][3]:
                                    count = + 1
                                # quadran +-
                                if one[i][j][3] == two[i - k][j + l][3]:
                                    count = + 1

                            # Si plus de la moitie des pixel sont different du pixel
                            # d'interet on change la valeur pour la valeur inverse
                            if count < 200:
                                if one[i][j][3] == 255:
                                    one[i][j][3] = 0
                                else:
                                    one[i][j][3] = 255
                    # On ajoute le mask spectral par-dessus la comparaison des 2 autres
                    if three[i][j][3] == 255:
                        one[i][j][3] = 255
            else:
                # les pixels dans la bande de 20 pixel,
                # on fait un rtion de 1 pour 1
                if one[i][j][3] != two[i][j][3]:
                    one[i][j][3] = 0
                # On ajoute le mask spectral par-dessus la comparaison des 2 autres
                if three[i][j][3] == 255:
                    one[i][j][3] = 1
    return one


###### Main ########



# Demande a l'utilisteur

# Verification que l'utilisateur entre une photo PNG

# lecture de l'image avec mathplotlib
#img = mpimg.imread('feu10.png')

# Application des filtres pour les image et
# ensuite enregistrer chaque photo pour les garder en memoire
#applyfilter(img, 'hot')
#saveImg('img1.png')
#applyfilter(img, 'nipy_spectral')
#saveImg('img2.png')
#applyfilter(img, 'Greys')
#saveImg('img3.png')

# Ouvrir les images a l'aide de la librairie Pillow
#img1 = Image.open('img1.png')
#img2 = Image.open('img2.png')
#img3 = Image.open('img3.png')

# Analyse des images pour chaque filtre
#lel1 = analysisphoto(img2, 0)
#lel2 = analysisphoto(img1, 1)
#lel3 = analysisphoto(img3, 2)

#lel4 = compareMask(lel3, lel2, lel1)

# Transformation pour chaque array en photo afin d'obtenir un masque visible
#transformMatrixToImage(lel3, 'greyOutput.png')
#transformMatrixToImage(lel2, 'hotOutput.png')
#transformMatrixToImage(lel1, 'spectralOutput.png')
#transformMatrixToImage(lel4, 'FinalOutput.png')
