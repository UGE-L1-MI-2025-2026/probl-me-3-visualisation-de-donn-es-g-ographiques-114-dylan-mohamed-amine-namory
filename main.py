from fltk import *
import shapefile
from couleur_final import *

largeur = 900
hauteur = 800
cree_fenetre(largeur, hauteur)

sf = shapefile.Reader("departements-20180101.shp")
departements = sf.shapes()


fichier_csv ="temperature-quotidienne-departementale.csv"
dico = construire_dictionnaire(fichier_csv)

# Conversion géographique en pixel
def geo_vers_pixel(lon, lat, xmin, ymin, xmax, ymax, largeur, hauteur):
    x = (lon - xmin) / (xmax - xmin) * largeur
    y = hauteur - (lat - ymin) / (ymax - ymin) * hauteur
    return x, y

# On récupère d'abord la bbox TOTALE du shapefile
xmin, ymin, xmax, ymax = sf.bbox


def obtenir_temperature_max(t_max):
    if  0<=t_max<=1: return "midnightblue"
    elif 1<=t_max<=2: return"slateblue"
    elif 2<=t_max<=10: return"slateblue"
    elif 5<=t_max<=10: return"slateblue"
    elif 10<=t_max<=15: return "darkmagenta"
    elif 15<=t_max<=20: return "mediumvioletred"
    elif 20<=t_max<=25: return "pink"
    elif 25<=t_max<=30: return "darkorange"
    elif 30<=t_max<=35: return "orange"
    else: return "yellow"




    

anne = input("Entrez une année : ")
dico_temperatures = tempmax(dico,anne)

def affichage_temp(code,dico_temperatures):
    t_max = 0
    for code_dep, temp in dico_temperatures.items():
        if code_dep == code:
            
            t_max = temp
    return float(t_max)

def affichage_carte():
    for code, departement in enumerate(departements):
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
                code_insee = str(code)
                t_max = affichage_temp(code_insee,dico_temperatures)
        

                couleur_temperature = obtenir_temperature_max(t_max)
                polygone(liste_points, remplissage=couleur_temperature, couleur="black")
               


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
