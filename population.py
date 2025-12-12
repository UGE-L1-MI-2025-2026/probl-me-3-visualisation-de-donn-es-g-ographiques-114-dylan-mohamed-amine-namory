import csv

def normaliser(code):
    code = code.strip()
    if code.isdigit():
        return code.zfill(2)
    return code


def trouver_colonne(possibles, colonnes):
    """Trouve une colonne en testant plusieurs variantes (accents, BOM, etc.)."""
    possibles = [p.lower() for p in possibles]
    for col in colonnes:
        col_clean = col.lower().lstrip("\ufeff")
        if any(p in col_clean for p in possibles):
            return col


def construire_dictionnaire_population(fichier_csv):
    dico = {}

    with open(fichier_csv, "r", encoding="utf-8") as fichier:
        première_ligne = fichier.readline().lstrip("\ufeff")
        contenu_nettoye = première_ligne + fichier.read()

    lignes = contenu_nettoye.splitlines()
    lecteur = csv.DictReader(lignes)

    colonnes = lecteur.fieldnames

    col_entity = trouver_colonne(["entity", "pays", "nom"], colonnes)
    col_code   = trouver_colonne(["code"], colonnes)
    col_year   = trouver_colonne(["year", "annee"], colonnes)
    col_density = trouver_colonne(["population density", "density"], colonnes)

    for ligne in lecteur:
        code = ligne[col_code].strip()
        anne = ligne[col_year].strip()
        density = ligne[col_density].replace(",", ".").strip()

        if code not in dico:
            dico[code] = {}

        if anne not in dico[code]:
            dico[code][anne] = density

    return dico


def densite_annee(dico, annee):
    """Retourne {code: densité} pour une année donnée."""
    d = {}
    for code, valeurs in dico.items():
        if annee in valeurs:
            d[code] = valeurs[annee]
    return d
import time

def dates_depuis_1980(dico):
    """Récupère toutes les dates distinctes ≥ 1980 et les renvoie une par une chaque seconde."""
    toutes_annees = set()
    for code, valeurs in dico.items():
        for annee in valeurs.keys():
            if annee.isdigit() and int(annee) >= 1980:
                toutes_annees.add(int(annee))
    annees_triees = sorted(toutes_annees)
    # Générateur : yield une année chaque seconde
    for annee in annees_triees:
        yield annee
        time.sleep(1)


# Exemple d’utilisation :
fichier_csv = "population-density.csv"
dico_population = construire_dictionnaire_population(fichier_csv)
print(densite_annee(dico_population,"2010"))
