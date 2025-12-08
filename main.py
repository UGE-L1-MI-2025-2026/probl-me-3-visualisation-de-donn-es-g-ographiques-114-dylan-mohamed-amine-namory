from fltk import *
import shapefile
from couleur_final import *

import matplotlib.pyplot as plt
import numpy as np



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



liste_polygone = []
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
                id_dep = polygone(liste_points, remplissage=couleur_temperature, couleur="black")
                liste_polygone.append(id_dep)
               


affichage_carte()

cmaps = [('Perceptually Uniform Sequential', [
            'viridis', 'plasma', 'inferno', 'magma', 'cividis']),
]

gradient = np.linspace(0, 1, 256)
gradient = np.vstack((gradient, gradient))


def plot_color_gradients(cmap_category, cmap_list):
    # Create figure and adjust figure height to number of colormaps
    nrows = len(cmap_list)
    figh = 0.35 + 0.15 + (nrows + (nrows-1)*0.1)*0.22
    fig, axs = plt.subplots(nrows=nrows, figsize=(6.4, figh))
    fig.subplots_adjust(top=1-.35/figh, bottom=.15/figh, left=0.2, right=0.99)

    axs[0].set_title(f"{cmap_category} colormaps", fontsize=14)

    for ax, cmap_name in zip(axs, cmap_list):
        ax.imshow(gradient, aspect='auto', cmap=cmap_name)
        ax.text(-.01, .5, cmap_name, va='center', ha='right', fontsize=10,
                transform=ax.transAxes)

    # Turn off *all* ticks & spines, not just the ones with colormaps.
    for ax in axs:
        ax.set_axis_off()


for cmap_category, cmap_list in cmaps:
    plot_color_gradients(cmap_category, cmap_list)

plt.show()


while True:
    ev = donne_ev()
    tev = type_ev(ev)


    for dep in liste_polygone:
        objet = objet_survole()
        if objet == dep:
            modifie(dep,couleur="white")



    if tev == "Quitte":
        break
    mise_a_jour()



ferme_fenetre()
