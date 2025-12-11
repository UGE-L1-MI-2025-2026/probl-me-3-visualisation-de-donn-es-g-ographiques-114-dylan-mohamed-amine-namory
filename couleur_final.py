import csv

def normaliser(dep):
    dep = dep.strip()
    if dep.isdigit():
        return dep.zfill(2)
    return dep


def trouver_colonne(possibles, colonnes):
    """Trouve une colonne en testant plusieurs variantes (accents cassés, BOM, etc.)."""
    possibles = [p.lower() for p in possibles]
    for col in colonnes:
        col_clean = col.lower().lstrip("\ufeff")
        if any(p in col_clean for p in possibles):
            return col
    raise KeyError(f"Impossible de trouver une colonne parmi : {possibles}")


def construire_dictionnaire(fichier_csv):
    dico = {}
    with open(fichier_csv, "r", encoding="utf-8") as fichier:
        première_ligne = fichier.readline().lstrip("\ufeff")
        contenu_nettoye = première_ligne + fichier.read()
    lignes = contenu_nettoye.splitlines()
    lecteur = csv.DictReader(lignes, delimiter=";")

    colonnes = lecteur.fieldnames

    col_date = trouver_colonne(["date"], colonnes)
    col_insee = trouver_colonne(["code insee", "depart"], colonnes)
    col_tmin = trouver_colonne(["tmin"], colonnes)
    col_tmax = trouver_colonne(["tmax"], colonnes)
    col_tmoy = trouver_colonne(["tmoy"], colonnes)
    for ligne in lecteur:
        date = ligne[col_date].strip()
        dep = normaliser(ligne[col_insee])
        tmin = ligne[col_tmin].replace(",", ".").strip()
        tmax = ligne[col_tmax].replace(",", ".").strip()
        tmoy = ligne[col_tmoy].replace(",", ".").strip()
        if dep not in dico:
            dico[dep] = {}
        if date not in dico[dep]:
            dico[dep][date] = {}
        dico[dep][date]["tmin"] = tmin
        dico[dep][date]["tmax"] = tmax
        dico[dep][date]["tmoy"] = tmoy

    return dico




def tempmax(dico, annee):
    resultat = {}

    for dep, dates in dico.items():

        max_dep = None 

        for date, temperatures in dates.items():

            
            if date.startswith(annee):

                
                tmax_str = temperatures["tmax"].replace(",", ".").strip()

                

                tmax = float(tmax_str)

                if max_dep == None:
                    max_dep = tmax
          
                else:
                    if tmax > max_dep:
                        max_dep = tmax


        resultat[dep] = max_dep

    return resultat



