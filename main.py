from fltk import *
import shapefile


largeur = 2000
hauteur = 1000
cree_fenetre(largeur, hauteur)

sf = shapefile.Reader("departements-20180101.shp")
shapes = sf.shapes()

zoom = 2
largeur_zoom = 3

# Conversion géographique en pixel
def geo_vers_pixel(lon, lat, xmin, ymin, xmax, ymax, largeur, hauteur):
    x = (lon - xmin) / (xmax - xmin) * largeur
    y = hauteur - (lat - ymin) / (ymax - ymin) * hauteur
    return x, y

# On récupère d'abord la bbox TOTALE du shapefile
xmin, ymin, xmax, ymax = sf.bbox

def affichage_carte(zoom,largeur_zoom ):
    for shp in shapes:
        # Liste de points convertis pour ce département
        points_pixels = []
        for lon, lat in shp.points:
            x, y = geo_vers_pixel(lon, lat, xmin, ymin, xmax, ymax, (9000*zoom)//3.1,(6500*zoom)//3)
            x,y = x//largeur_zoom,y+zoom
            points_pixels.append((x,y))
        liste_points = [coord for point in points_pixels for coord in point]
        # Dessin du polygone du département
        polygone(liste_points, remplissage="white", couleur="black")
        cercle(x,y,r=5,couleur="black",remplissage="blue")


affichage_carte(zoom,largeur_zoom)
while True:
    ev = donne_ev()
    tev = type_ev(ev)

    if tev == "Touche":
        print(touche(ev))
        if touche(ev) == "z":
            largeur_zoom +=0.5
            zoom += 0.5
            efface_tout()
            affichage_carte(zoom,largeur_zoom)
            

            
       
    
    elif tev == "Quitte":
        break
    mise_a_jour()



ferme_fenetre()
