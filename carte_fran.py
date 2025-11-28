from fltk import *
import shapefile


largeur = 900
hauteur = 900
cree_fenetre(largeur, hauteur)

sf = shapefile.Reader("departements-20180101.shp")
shapes = sf.shapes()

# Conversion géographique en pixel
def geo_vers_pixel(lon, lat, xmin, ymin, xmax, ymax, largeur, hauteur):
    x = (lon - xmin) / (xmax - xmin) * largeur
    y = hauteur - (lat - ymin) / (ymax - ymin) * hauteur
    return x, y

# On récupère d'abord la bbox TOTALE du shapefile
xmin, ymin, xmax, ymax = sf.bbox

for shp in shapes:
    # Liste de points convertis pour ce département
    points_pixels = []
    for lon, lat in shp.points:
        x, y = geo_vers_pixel(lon, lat, xmin, ymin, xmax, ymax, largeur, hauteur)
        points_pixels.append((x, y))
    liste_points = [coord for point in points_pixels for coord in point]
    # Dessin du polygone du département
    polygone(liste_points, remplissage="white", couleur="black")

mise_a_jour()
attend_ev()
ferme_fenetre()
