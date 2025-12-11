import fltk as f 
import shapefile
import time
from datetime import date
import couleur_final as c





'''creer fonctions:
-Une permettant de cliquer sur un bouton pour passer de la map monde a france et inversement (Changement de fichier)
-une pour changer les couleurs de la carte (en fonction des dates)
-un timer pour l'animation (chaque seconde evolutions temperature)


'''
#map_france = "departements-20180101.shp"
#map_monde = "country_shapes.shp"

def changement_map():
    while True:
        ev = f.donne_ev()

        if f.tev == "ClicDroit" and sf == shapefile.Reader("country_shapes.shp"):
            sf = shapefile.Reader("departements-20180101.shp")

        elif f.tev == "ClicDroit" and sf == shapefile.Reader("departements-20180101.shp"):
            sf = shapefile.Reader("country_shapes.shp")
        

        f.mise_a_jour()




fichier_csv = "temperature.csv"
dico = c.construire_dictionnaire(fichier_csv)


def recuperer_liste_date(dico):
    liste_date = []
    for cle, valeurs in dico.items():
        for valeur in valeurs:
            if valeur not in liste_date:
                liste_date.append(valeur)
    return liste_date


def str_vers_int(liste_date):
    liste_trier = []
    for i in liste_date:
        annee = int(i[:4])
        mois = int(i[5:7])
        jour = int(i[8:10])
        liste_trier.append((annee, mois, jour))
    return liste_trier




def ordonner_liste_dates(liste_trier):
    liste_ordonner = []
    for date in liste_trier:
        if date not in liste_ordonner:
            liste_ordonner.append(date)

    liste_ordonner.sort()

    return liste_ordonner


print(ordonner_liste_dates(str_vers_int(recuperer_liste_date(dico))))

def maj_date_chaque_seconde(liste_dates, date_actuelle):
    for y, m, d in liste_dates:
        date_actuelle[0] = date(y, m, d).isoformat()
        print("date_actuelle =", date_actuelle[0])
        time.sleep(1)

date_actuelle = [None]   # variable mutable









'''def changement_date_manuel():
    while True:
        ev = f.donne_ev()

        if f.tev == 'Touche':
            t = f.touche(ev)
            print(f"Touche appuyée : {t}")

        if t.lower() == 'd':
            f.efface_tout()
            print(f"La carte { } à la date {}")


            
            
            
            
        elif t.lower() == 'q': 
            f.efface_tout()
            print(f"La carte { } à la date {}")

        


        f.mise_a_jour()'''



    
    

    
