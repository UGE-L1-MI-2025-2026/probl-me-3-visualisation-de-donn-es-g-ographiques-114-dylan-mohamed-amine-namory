from fltk import *
import shapefile


largeur = 900
hauteur = 800
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
                x, y = geo_vers_pixel(lon, lat, xmin, ymin, xmax, ymax, 5000, 5000)
                x -= 2280
                points_pixels.append((x, y))
            
            liste_points = [coord for point in points_pixels for coord in point]
            polygone(liste_points, remplissage="white", couleur="black")
            cercle(x,y, r=5, couleur="black", remplissage="blue")



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
