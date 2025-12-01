from fltk import *
import shapefile
import csv

largeur = 900
hauteur = 800
cree_fenetre(largeur, hauteur)

sf = shapefile.Reader("departements-20180101.shp")
departements = sf.shapes()

base_de_donnee =  []

with open("temperature-quotidienne-departementale.csv",encoding="utf-8-sig") as f:
    bd = csv.DictReader(f,delimiter=";")
    for data in bd:
        base_de_donnee.append(data)
      




# Conversion géographique en pixel
def geo_vers_pixel(lon, lat, xmin, ymin, xmax, ymax, largeur, hauteur):
    x = (lon - xmin) / (xmax - xmin) * largeur
    y = hauteur - (lat - ymin) / (ymax - ymin) * hauteur
    return x, y

# On récupère d'abord la bbox TOTALE du shapefile
xmin, ymin, xmax, ymax = sf.bbox

def affichage_carte():
    for departement in departements:
        parties = departement.parts
        parties = list(parties) + [len(departement.points)]
        
        for i in range(len(parties)-1):
        
            point_debut_ile = parties[i]
            point_fin_ile = parties[i+1]
            points_ile = departement.points[point_debut_ile:point_fin_ile]
            
            points_pixels = []
            for lon, lat in points_ile:
                x, y = geo_vers_pixel(lon, lat, xmin, ymin, xmax, ymax, 5000, 5000)
                x -= 2280
                points_pixels.append((x, y))
            
            liste_points = [coord for point in points_pixels for coord in point]
            for data in base_de_donnee:
                for cle,valeur in data.items():
                    if cle == "TMax (°C)":
                        print(valeur)
                        if  0<=valeur<=5: couleur_temperature = "midnightblue"
                        elif 5<=valeur<=10: couleur_temperature = "slateblue"
                        elif 10<=valeur<=15: couleur_temperature = "darkmagenta"
                        elif 15<=valeur<=20: couleur_temperature= "mediumvioletred"
                        elif 20<=valeur<=25: couleur_temperature= "distorched"
                        elif 25<=valeur<=30: couleur_temperature= "darkorange"
                        elif 30<=valeur<=35: couleur_temperature= "orange"
                        else:couleur_temperature= "yellow"
                        

            polygone(liste_points, remplissage="white", couleur=couleur_temperature)
            cercle(x,y, r=5, couleur="black", remplissage="blue")


affichage_carte()
while True:
    ev = donne_ev()
    tev = type_ev(ev)

    if tev == "ClicGauche":
        print(abscisse(ev),ordonnee(ev))

            
       
    
    elif tev == "Quitte":
        break
    mise_a_jour()



ferme_fenetre()
