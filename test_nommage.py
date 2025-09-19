#!/usr/bin/env python3
"""
Script de test pour vérifier la fonction de nettoyage des titres
"""

import sys
import os

# Ajoute le répertoire courant au path pour importer le module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tri_wordpress import nettoyer_titre_pour_fichier

def test_nommage():
    """Teste la conversion de titres en noms de fichiers"""
    
    # Exemples de titres du fichier CSV
    exemples_titres = [
        "Architecture de microservices",
        "Comment faire pour créer un routeur en ligne de commande ?",
        "Création et utilisation des machines virtuelles, des volumes et des snapshots",
        "Comment devenir souscripteur pour un agent du ministère de l'Intérieur ?​",
        "Quelle est la différence entre Cloud π, Cloud π Gen2 et Cloud π Native ?",
        "Est-il possible de créer des gabarits personnalisés sur la plateforme Cloud π ?",
        "Console Cloud &pi; : ajouter et supprimer des souscripteurs délégués",
        'Comment faire pour créer, pour lister, pour supprimer un conteneur en ligne de commande ?'
    ]
    
    print("🧪 TEST DE NETTOYAGE DES TITRES")
    print("=" * 80)
    print()
    
    for i, titre in enumerate(exemples_titres, 1):
        nom_fichier = nettoyer_titre_pour_fichier(titre)
        print(f"{i:2d}. Titre original :")
        print(f"    {titre}")
        print(f"    Nom de fichier :")
        print(f"    {nom_fichier}")
        print(f"    Longueur : {len(nom_fichier)} caractères")
        print()
    
    print("=" * 80)
    print("✅ Test terminé")

if __name__ == "__main__":
    test_nommage()


