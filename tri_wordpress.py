#!/usr/bin/env python3
"""
Script de tri du contenu WordPress

Ce script utilise le fichier tri.csv pour copier les articles WordPress
depuis le répertoire source vers le répertoire de destination approprié.

Colonne C : répertoire de départ (à partir de wordpress-content-to-sort)
Colonne D : répertoire de destination
"""

import csv
import os
import re
import shutil
import sys
import unicodedata
from pathlib import Path


def nettoyer_titre_pour_fichier(titre):
    """
    Convertit un titre d'article en nom de fichier valide
    
    Args:
        titre (str): Titre de l'article
        
    Returns:
        str: Nom de fichier nettoyé et valide
    """
    if not titre:
        return "article_sans_titre"
    
    # Supprime ou remplace les caractères problématiques
    # Normalise les caractères Unicode (supprime les accents)
    titre_normalise = unicodedata.normalize('NFD', titre)
    titre_ascii = ''.join(c for c in titre_normalise if unicodedata.category(c) != 'Mn')
    
    # Remplace les caractères spéciaux par des tirets
    titre_nettoye = re.sub(r'[^\w\s-]', '', titre_ascii)
    
    # Remplace les espaces et multiples tirets par un seul tiret
    titre_nettoye = re.sub(r'[-\s]+', '-', titre_nettoye)
    
    # Supprime les tirets en début et fin
    titre_nettoye = titre_nettoye.strip('-')
    
    # Limite la longueur (max 100 caractères pour éviter les problèmes de système de fichiers)
    if len(titre_nettoye) > 100:
        titre_nettoye = titre_nettoye[:100].rstrip('-')
    
    # Convertit en minuscules
    titre_nettoye = titre_nettoye.lower()
    
    # S'assure qu'on a au moins quelque chose
    if not titre_nettoye:
        return "article_sans_titre"
    
    return titre_nettoye


def lire_fichier_tri(fichier_csv):
    """
    Lit le fichier tri.csv et retourne la liste des opérations de tri
    
    Args:
        fichier_csv (str): Chemin vers le fichier tri.csv
        
    Returns:
        list: Liste de dictionnaires contenant les informations de tri
    """
    operations = []
    
    try:
        with open(fichier_csv, 'r', encoding='utf-8') as f:
            lecteur = csv.DictReader(f)
            for ligne in lecteur:
                # Utilise les noms des colonnes du CSV
                operation = {
                    'titre': ligne.get('Titre', ''),
                    'chemin_actuel': ligne.get('Chemin actuel', ''),
                    'repertoire_export': ligne.get('Répertoire d\'export', ''),
                    'destination': ligne.get('Destination ', '')  # Note l'espace après Destination
                }
                
                # Vérifie que les colonnes importantes ne sont pas vides
                if operation['repertoire_export'] and operation['destination']:
                    operations.append(operation)
                    
    except FileNotFoundError:
        print(f"❌ Erreur : Le fichier {fichier_csv} n'a pas été trouvé.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du fichier CSV : {e}")
        sys.exit(1)
        
    return operations


def creer_repertoires_destination(chemin_destination):
    """
    Crée tous les répertoires nécessaires pour le chemin de destination
    
    Args:
        chemin_destination (str): Chemin vers le répertoire de destination
    """
    try:
        Path(chemin_destination).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la création du répertoire {chemin_destination} : {e}")
        return False


def copier_contenu(source, repertoire_destination, nouveau_nom=None):
    """
    Copie le contenu depuis la source vers la destination avec possibilité de renommage
    
    Args:
        source (str): Chemin source
        repertoire_destination (str): Répertoire de destination
        nouveau_nom (str, optional): Nouveau nom pour le fichier/dossier copié
        
    Returns:
        tuple: (bool, str) - (succès, chemin_destination_final)
    """
    try:
        if not os.path.exists(source):
            print(f"⚠️  Source inexistante : {source}")
            return False, ""
        
        # Détermine le nom final du fichier/dossier
        if nouveau_nom:
            nom_final = nouveau_nom
        else:
            nom_final = os.path.basename(source)
        
        # Construit le chemin de destination complet
        destination_complete = os.path.join(repertoire_destination, nom_final)
        
        if os.path.isfile(source):
            # Si c'est un fichier, on le copie
            shutil.copy2(source, destination_complete)
            return True, destination_complete
            
        elif os.path.isdir(source):
            # Si c'est un répertoire, on copie tout le contenu
            if os.path.exists(destination_complete):
                shutil.rmtree(destination_complete)
            shutil.copytree(source, destination_complete)
            return True, destination_complete
            
        else:
            print(f"⚠️  Type de source non supporté : {source}")
            return False, ""
            
    except Exception as e:
        print(f"❌ Erreur lors de la copie de {source} vers {repertoire_destination} : {e}")
        return False, ""


def trier_contenu_wordpress(repertoire_base="wordpress-content-to-sort", fichier_csv="tri.csv", mode_simulation=False):
    """
    Fonction principale pour trier le contenu WordPress
    
    Args:
        repertoire_base (str): Répertoire de base contenant le contenu WordPress
        fichier_csv (str): Fichier CSV contenant les instructions de tri
        mode_simulation (bool): Si True, affiche seulement ce qui serait fait sans l'exécuter
    """
    print("🚀 Démarrage du script de tri du contenu WordPress")
    print("=" * 60)
    
    # Vérification de l'existence du répertoire de base
    if not os.path.exists(repertoire_base):
        print(f"❌ Erreur : Le répertoire de base '{repertoire_base}' n'existe pas.")
        print(f"   Veuillez créer ce répertoire ou modifier le chemin dans le script.")
        sys.exit(1)
    
    # Lecture du fichier de tri
    print(f"📖 Lecture du fichier de tri : {fichier_csv}")
    operations = lire_fichier_tri(fichier_csv)
    print(f"✅ {len(operations)} opérations de tri trouvées\n")
    
    # Statistiques
    nb_reussites = 0
    nb_echecs = 0
    
    # Traitement de chaque opération
    for i, operation in enumerate(operations, 1):
        titre = operation['titre']
        repertoire_source = operation['repertoire_export']
        repertoire_dest = operation['destination']
        
        # Génère le nom de fichier basé sur le titre
        nom_fichier_final = nettoyer_titre_pour_fichier(titre)
        
        print(f"📁 [{i}/{len(operations)}] Traitement : {titre}")
        print(f"   Source : {repertoire_source}")
        print(f"   Destination : {repertoire_dest}")
        print(f"   Nom final : {nom_fichier_final}")
        
        # Construction des chemins complets
        chemin_source = os.path.join(repertoire_base, repertoire_source)
        
        if mode_simulation:
            chemin_dest_final = os.path.join(repertoire_dest, nom_fichier_final)
            print(f"   🔍 SIMULATION - Copierait depuis {chemin_source} vers {chemin_dest_final}")
            if os.path.exists(chemin_source):
                nb_reussites += 1
                print("   ✅ Source existe - opération serait réussie")
            else:
                nb_echecs += 1
                print("   ❌ Source inexistante - opération échouerait")
        else:
            # Création du répertoire de destination
            if creer_repertoires_destination(repertoire_dest):
                # Copie du contenu avec le nouveau nom
                succes, chemin_dest_final = copier_contenu(chemin_source, repertoire_dest, nom_fichier_final)
                
                if succes:
                    nb_reussites += 1
                    print(f"   ✅ Copie réussie vers {chemin_dest_final}")
                else:
                    nb_echecs += 1
            else:
                nb_echecs += 1
        
        print()  # Ligne vide pour la lisibilité
    
    # Résumé final
    print("=" * 60)
    print("📊 RÉSUMÉ DES OPÉRATIONS")
    print(f"✅ Réussites : {nb_reussites}")
    print(f"❌ Échecs : {nb_echecs}")
    print(f"📈 Total traité : {len(operations)}")
    
    if mode_simulation:
        print("\n🔍 Mode simulation activé - aucune opération réelle effectuée")
        print("   Pour exécuter réellement, relancez le script sans '--simulation'")
    else:
        if nb_echecs == 0:
            print("\n🎉 Toutes les opérations ont été effectuées avec succès !")
        else:
            print(f"\n⚠️  {nb_echecs} opération(s) ont échoué. Vérifiez les messages d'erreur ci-dessus.")


def main():
    """Fonction principale du script"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Script de tri du contenu WordPress")
    parser.add_argument("--repertoire-base", "-r", 
                       default="wordpress-content-to-sort",
                       help="Répertoire de base contenant le contenu WordPress (défaut: wordpress-content-to-sort)")
    parser.add_argument("--fichier-csv", "-f",
                       default="tri.csv", 
                       help="Fichier CSV contenant les instructions de tri (défaut: tri.csv)")
    parser.add_argument("--simulation", "-s",
                       action="store_true",
                       help="Mode simulation : affiche ce qui serait fait sans l'exécuter")
    
    args = parser.parse_args()
    
    trier_contenu_wordpress(
        repertoire_base=args.repertoire_base,
        fichier_csv=args.fichier_csv,
        mode_simulation=args.simulation
    )


if __name__ == "__main__":
    main()

