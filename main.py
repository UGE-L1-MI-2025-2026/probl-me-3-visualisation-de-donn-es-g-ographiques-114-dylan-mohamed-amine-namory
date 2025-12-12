from fltk import *
import shapefile
from couleur_final import *
import time 

largeur = 900
hauteur = 800
cree_fenetre(largeur, hauteur)

sf = shapefile.Reader("departements-20180101.shp")
departements = sf.shapes()
re = sf.records()



fichier_csv = "temperature.csv"
dico = construire_dictionnaire(fichier_csv)

annee = '2018' 
TYPE_TEMPERATURE = 'tmax' 

# Conversion géographique en pixel
def geo_vers_pixel(lon, lat, xmin, ymin, xmax, ymax, largeur, hauteur):
    x = (lon - xmin) / (xmax - xmin) * largeur
    y = hauteur - (lat - ymin) / (ymax - ymin) * hauteur
    return x, y

xmin, ymin, xmax, ymax = sf.bbox


def charger_temperatures(dico_complet, annee, type_temp):
    if type_temp == 'tmin':
        return tempmin(dico_complet, annee)
    elif type_temp == 'tmoy':
        return tempmoy(dico_complet, annee)
    return tempmax(dico_complet, annee)


def obtenir_couleur(temp):
    if temp == None:
        return "white"
    if temp <= 0: return "#0d0887"
    elif temp <= 5: return "#46039f"
    elif temp <= 10: return "#7201a8"
    elif temp <= 15: return "#9c179e"
    elif temp <= 20: return "#bd3786"
    elif temp <= 25: return "#dd513a"
    elif temp <= 30: return "#f37819"
    elif temp <= 35: return "#fca50a"
    else: return "#fcba03"


def dessiner_colorbar():
    x1 = 780
    x2 = 840
    hauteur = 40
    y = 50

    couleurs = [
        ("≤ 0°C", "#0d0887"),
        ("≤ 5°C", "#46039f"),
        ("≤ 10°C", "#7201a8"),
        ("≤ 15°C", "#9c179e"),
        ("≤ 20°C", "#bd3786"),
        ("≤ 25°C", "#dd513a"),
        ("≤ 30°C", "#f37819"),
        ("≤ 35°C", "#fca50a"),
        ("> 35°C", "#fcba03")
    ]

    for temp, col in couleurs:
        rectangle(x1, y, x2, y + hauteur, remplissage=col, couleur="black")
        texte(x2 + 5, y + 10, temp, taille=12, couleur="black")
        y += hauteur

dico_temperatures = charger_temperatures(dico, annee, TYPE_TEMPERATURE)

def affichage_temp(code,dico_temperatures):
    t_max = None
    for code_dep, temp in dico_temperatures.items():
        if code_dep == code:
            t_max = temp
    if t_max == None:
        return t_max

    return float(t_max)


dico_departements = {}

def affichage_carte():
    for i in range(len(departements)):
        departement = departements[i]
        record = sf.record(i)  
        code_insee = record["code_insee"]
       
        parties = list(departement.parts) + [len(departement.points)]
        
        for j in range(len(parties)-1):
            point_debut_ile = parties[j]
            point_fin_ile = parties[j+1]
            points_ile = departement.points[point_debut_ile:point_fin_ile]
            
            points_pixels = []
            for lon, lat in points_ile:
                x, y = geo_vers_pixel(lon, lat, xmin, ymin, xmax, ymax, 5000, 5000)
                x -= 2280
                points_pixels.append((x, y))
            
            liste_points = [coord for point in points_pixels for coord in point]

            t_max = affichage_temp(code_insee, dico_temperatures)
            couleur_temperature = obtenir_couleur(t_max) 

            
            id_dep = polygone(liste_points, remplissage=couleur_temperature, couleur="black")
            dico_departements[id_dep] = {"nom":record["nom"],"t_max":t_max}
            

def dessiner_boutons_temperature(type_temp_actuel):
    
    couleur_tmin = "lightgreen" if type_temp_actuel == 'tmin' else "white"
    rectangle(260, 700, 330, 760, remplissage=couleur_tmin, couleur="black")
    texte(275, 720, "TMin", taille=15)

    couleur_tmax = "lightgreen" if type_temp_actuel == 'tmax' else "white"
    rectangle(340, 700, 410, 760, remplissage=couleur_tmax, couleur="black")
    texte(355, 720, "TMax", taille=15)

    couleur_tmoy = "lightgreen" if type_temp_actuel == 'tmoy' else "white"
    rectangle(420, 700, 490, 760, remplissage=couleur_tmoy, couleur="black")
    texte(435, 720, "TMoy", taille=15)



rectangle(0,0,340,40, remplissage="white")
rectangle(0,700,250,760,remplissage="gray")

rectangle(0,700,35,760,remplissage="white")
rectangle(210,700,250,760,remplissage="white")

texte(40,720,f'Année : {annee}',taille=20,police="bold")
texte(10,720,"<",taille=20)
texte(215,720,">",taille=20)

dessiner_boutons_temperature(TYPE_TEMPERATURE)

affichage_carte()
dessiner_colorbar()


def changer_annee_carte(annee):
    efface_tout()
    global dico_temperatures, TYPE_TEMPERATURE, dico 
    dico_temperatures = charger_temperatures(dico, annee, TYPE_TEMPERATURE)
    
    affichage_carte()
    dessiner_colorbar()

    rectangle(0,0,340,40, remplissage="white")
    rectangle(0,700,490,760,remplissage="gray") 

    rectangle(0,700,35,760,remplissage="white")
    rectangle(210,700,250,760,remplissage="white")
    texte(40,720,f'Année : {annee}',taille=20,police="bold")
    texte(10,720,"<",taille=20)
    texte(215,720,">",taille=20)
    
    dessiner_boutons_temperature(TYPE_TEMPERATURE)

    mise_a_jour()


ANNEE_DEBUT = 2018
ANNEE_FIN = 2025 
annee_auto_mode = False
last_update_time = time.time()
UPDATE_INTERVAL = 1.0 

objet_precedent = None

while True:
    
    ev = donne_ev()
    tev = type_ev(ev)

    #événement espace pour basculer le mode auto
    if tev == 'Touche':
        if touche(ev) == 'space':
            annee_auto_mode = not annee_auto_mode 
            
            if annee_auto_mode:
                annee = str(ANNEE_DEBUT)
                changer_annee_carte(annee)
                last_update_time = time.time()
            
            print(f"Mode d'affichage annuel automatique : {annee_auto_mode}")


    #avancement automatique de l'année
    if annee_auto_mode and time.time() - last_update_time >= UPDATE_INTERVAL:
        annee_actuelle = int(annee)
        
        if annee_actuelle < ANNEE_FIN:
            annee = str(annee_actuelle + 1)
            changer_annee_carte(annee)
            last_update_time = time.time()
            print(f"Année auto : {annee}")
        else:
            annee_auto_mode = False
            print("Fin de la séquence annuelle. Mode désactivé.")
            

    if tev == 'ClicDroit' or tev=="ClicGauche" :
        x = abscisse(ev)
        y = ordonnee(ev)
        
        if 700 <= y <= 760:
            
            #changements d'année 
            if 210 <= x <= 250:
                annee = str(int(annee) + 1)
                if int(annee) <= 2025 :
                    print(annee)
                    changer_annee_carte(annee)

            elif 0 <= x <= 35:
                annee = str(int(annee) - 1) 
                if int(annee) >= 2018:
                    print(annee)
                    changer_annee_carte(annee)

            if 260 <= x <= 330:
                if TYPE_TEMPERATURE != 'tmin':
                    TYPE_TEMPERATURE = 'tmin'
                    changer_annee_carte(annee)
            elif 340 <= x <= 410: 
                if TYPE_TEMPERATURE != 'tmax':
                    TYPE_TEMPERATURE = 'tmax'
                    changer_annee_carte(annee)
            elif 420 <= x <= 490: 
                if TYPE_TEMPERATURE != 'tmoy':
                    TYPE_TEMPERATURE = 'tmoy'
                    changer_annee_carte(annee)


    objet = objet_survole()

    if objet !=None and objet != objet_precedent:

        if objet_precedent != None:
            modifie(objet_precedent, couleur="black")

        modifie(objet, couleur="white")

        info = dico_departements.get(objet, None)

        if info !=None:
            t_max = info['t_max']
            type_affichage = TYPE_TEMPERATURE.upper() #TMIN, TMAX ou TMOY

            if t_max == None:
                texte_affiche = f"{info['nom']} ({type_affichage}) : pas de donnée"
            else:
                texte_affiche = f"{info['nom']} ({type_affichage}) : {t_max}°C"

            rectangle(0,0,340,40, remplissage="white",couleur="white")
            
            texte_dep = texte(10,10, texte_affiche, taille=15, couleur="black")

        objet_precedent = objet

    if tev == "Quitte":
        break

    mise_a_jour()



ferme_fenetre()
