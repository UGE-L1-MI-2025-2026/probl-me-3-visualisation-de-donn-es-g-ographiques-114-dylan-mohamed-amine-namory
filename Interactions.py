import fltk as f 
import shapefile





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

def changement_date():
    while True:
        ev = f.donne_ev()

        if f.tev == 'Touche':
            t = f.touche(ev)
            print(f"Touche appuyée : {t}")

        if t.lower() == 'd':
            f.efface_tout()

            
            
            
            
        elif t.lower() == 'q': 
            f.efface_tout()
        


        f.mise_a_jour()



    
    

    
