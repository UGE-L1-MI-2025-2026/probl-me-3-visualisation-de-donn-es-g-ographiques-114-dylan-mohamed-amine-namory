from fltk import *
import shapefile
import math
import population as p 


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



largeur = 1920-10
hauteur = 1080-100
cree_fenetre(largeur, hauteur)
anne = input("Entrez une année : ")

sf = shapefile.Reader("country_shapes.shp")
shapes = sf.shapes()



# Conversion géographique en pixel
def geo_vers_pixel(lon, lat, xmin, ymin, xmax, ymax, largeur, hauteur):
    x = (lon - xmin) / (xmax - xmin) * largeur
    y = hauteur - (lat - ymin) / (ymax - ymin) * hauteur
    return x, y

# On récupère d'abord la bbox TOTALE du shapefile
xmin, ymin, xmax, ymax = sf.bbox

def affichage_carte_monde():
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
            



affichage_carte_monde()


def changer_annee_carte(annee):
    efface_tout()
    global  population
    population = p.densite_annee(p.dico_population, anne)
    affichage_carte_monde()
    mise_a_jour()


while True:
    ev = donne_ev()
    tev = type_ev(ev)

    if tev == 'ClicDroit' :
        anne = str(int(anne) + 1)
        if int(anne) <= 2025 :
            print(anne)
            changer_annee_carte(anne)


    elif tev == 'ClicGauche' :
        anne = str(int(anne) - 1) 
        if int(anne) >= 2018:
            print(anne)
            changer_annee_carte(anne)

    mise_a_jour()



ferme_fenetre()
