#!/usr/bin/env python3
import os
import re
import csv
from pathlib import Path

def extract_title_from_markdown(file_path):
    """Extrait le titre depuis l'en-tête YAML d'un fichier markdown"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Rechercher le titre dans l'en-tête YAML
        title_match = re.search(r'^title:\s*["\']?([^"\']*)["\']?$', content, re.MULTILINE)
        if title_match:
            return title_match.group(1).strip()
        
        # Si pas de titre dans l'en-tête, chercher un titre de niveau 1
        h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if h1_match:
            return h1_match.group(1).strip()
            
        return None
    except Exception as e:
        print(f"Erreur lors de la lecture de {file_path}: {e}")
        return None

def main():
    # Répertoire de base contenant les articles WordPress
    base_dir = Path("wordpress-content-to-sort")
    
    # Liste pour stocker les titres
    titles = []
    
    # Parcourir tous les dossiers dans le répertoire de base
    for folder in sorted(base_dir.iterdir()):
        if folder.is_dir():
            index_file = folder / "index.md"
            if index_file.exists():
                title = extract_title_from_markdown(index_file)
                if title:
                    titles.append({
                        'folder': folder.name,
                        'title': title
                    })
                    print(f"Trouvé: {title}")
                else:
                    print(f"Aucun titre trouvé dans: {folder.name}")
    
    # Créer le fichier CSV
    csv_filename = "wordpress_articles_titles.csv"
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['folder', 'title']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Écrire l'en-tête
        writer.writeheader()
        
        # Écrire les données
        for item in titles:
            writer.writerow(item)
    
    print(f"\nFichier CSV créé: {csv_filename}")
    print(f"Nombre d'articles traités: {len(titles)}")

if __name__ == "__main__":
    main() 