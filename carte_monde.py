from fltk import *
import shapefile
import math

'''Mathématiquement, la projection de Mercator est défini de la façon suivante :
 si un point de la sphère a pour latitude φ et pour longitude λ 
 (avec λ0 placé au centre de la carte, alors son projeté sur la carte de Mercator aura pour coordonnées {x=λ−λ0y=ln(tan(π4+φ2)). { x = λ − λ 0 y = ln 
largeur = 1920-10  
hauteur = 1080-100
cree_fenetre(largeur, hauteur)

sf = shapefile.Reader("country_shapes.shp")
shapes = sf.shapes()



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
ferme_fenetre()'''
from fltk import *
import shapefile


largeur = 1920-10
hauteur = 1080-100
cree_fenetre(largeur, hauteur)

sf = shapefile.Reader("country_shapes.shp")
shapes = sf.shapes()



# Conversion géographique en pixel
def geo_vers_pixel(lon, lat, xmin, ymin, xmax, ymax, largeur, hauteur):
    x = (lon - xmin) / (xmax - xmin) * largeur
    y = hauteur - (lat - ymin) / (ymax - ymin) * hauteur
    return x, y

# On récupère d'abord la bbox TOTALE du shapefile
xmin, ymin, xmax, ymax = sf.bbox

def affichage_carte():
    for shp in shapes:
        parts = shp.parts
        parts = list(parts) + [len(shp.points)]
        
        for i in range(len(parts)-1):
            point_debut_ile = parts[i]
            point_fin_ile = parts[i+1]
            points_ile = shp.points[point_debut_ile:point_fin_ile]
            
            points_pixels = []
            for lon, lat in points_ile:
                x, y = geo_vers_pixel(lon, lat, xmin, ymin, xmax, ymax, 1920-100, 1080-100)
                points_pixels.append((x, y))
            
            liste_points = [coord for point in points_pixels for coord in point]
            polygone(liste_points, remplissage="white", couleur="black")
            cercle(x,y, r=3, couleur="black", remplissage="blue")



affichage_carte()
while True:
    ev = donne_ev()
    tev = type_ev(ev)

    if tev == "Touche":
        pass

            
       
    
    elif tev == "Quitte":
        break
    mise_a_jour()



ferme_fenetre()
