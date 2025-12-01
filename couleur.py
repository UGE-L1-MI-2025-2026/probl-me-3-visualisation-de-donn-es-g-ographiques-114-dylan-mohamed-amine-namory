import csv
import re


liste = []

with open("temperature.csv", "r") as fichier:
    lecteur_csv = csv.DictReader(fichier)
    for dict in lecteur_csv:
        for departement,temp in dict.items():
            liste.append(temp)



    def dico_corp(liste_depart):
        dico = {}
        for i in liste_depart:
            cle = i[11:13]
            donne = []
            for a in liste_depart:
                if  cle == a[11:13]:
                    donne.append(a[:11])
                    donne.append(a[13:])
            dico[cle] = donne
        print(dico)
    dico = dico_corp(liste)
    print(dico)
