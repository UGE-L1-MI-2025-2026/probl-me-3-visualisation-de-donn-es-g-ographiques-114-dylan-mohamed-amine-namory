import fltk as f 
import shapefile
import time 
import couleur_final as c







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

def contruire_liste_date(dico):
    liste_date = []
    for cle , valeur in dico.items() :
        for valeur in dico[cle] :
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

def tri_insertion(tab): 
    # Parcour de 1 à la taille du tab
    for i in range(1, len(tab)): 
        k = tab[i] 
        j = i-1
        while j >= 0 and k < tab[j] : 
                tab[j + 1] = tab[j] 
                j -= 1
        tab[j + 1] = k
# Programme principale pour tester le code ci-dessus
tab = str_vers_int(contruire_liste_date(dico))
tri_insertion(tab) 
print ("Le tableau trié est:")
for i in range(len(tab)): 
    print ("% d" % tab[i])












'''__________________Brouillon/Poubelle:_________________________

def changement_date_manuel():
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
                
'''creer fonctions:
-Une permettant de cliquer sur un bouton pour passer de la map monde a france et inversement (Changement de fichier)
-une pour changer les couleurs de la carte (en fonction des dates)
-un timer pour l'animation (chaque seconde evolutions temperature)


'''
#map_france = "departements-20180101.shp"
#map_monde = "country_shapes.shp"

    
    

    
