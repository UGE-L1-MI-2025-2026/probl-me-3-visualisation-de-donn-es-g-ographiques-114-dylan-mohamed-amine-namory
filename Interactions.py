import fltk as f 
import shapefile
import time 





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






def triller_dates():
    


    da = f"{annee}-{mois}-{jour}" 

    while annee <= 2025 and mois <= 10 and jour <= 31:
        
    







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

        


        f.mise_a_jour()



    
    

    
