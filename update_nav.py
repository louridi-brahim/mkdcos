#!/usr/bin/env python3
"""
Script pour mettre à jour automatiquement la section 'nav' du fichier mkdocs.yml
en parcourant l'arborescence du dossier 'docs'.
"""

import os
import re
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional


def extract_title_from_markdown(file_path: Path) -> Optional[str]:
    """
    Extrait le titre d'un fichier Markdown depuis la première ligne commençant par #
    ou depuis les métadonnées YAML front matter.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier s'il y a du front matter YAML
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                try:
                    front_matter = yaml.safe_load(parts[1])
                    if isinstance(front_matter, dict) and 'title' in front_matter:
                        return front_matter['title']
                except yaml.YAMLError:
                    pass
        
        # Chercher le premier titre Markdown
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('# '):
                return line[2:].strip()
        
        # Si aucun titre trouvé, utiliser le nom du fichier
        return file_path.stem.replace('-', ' ').replace('_', ' ').title()
    
    except Exception:
        # En cas d'erreur, utiliser le nom du fichier
        return file_path.stem.replace('-', ' ').replace('_', ' ').title()


def create_nav_item(file_path: Path, docs_root: Path) -> Dict[str, str]:
    """
    Crée un élément de navigation pour un fichier Markdown.
    """
    title = extract_title_from_markdown(file_path)
    relative_path = file_path.relative_to(docs_root)
    
    return {title: str(relative_path).replace('\\', '/')}


def scan_directory(directory: Path, docs_root: Path) -> List[Any]:
    """
    Parcourt récursivement un répertoire et génère la structure de navigation.
    """
    nav_items = []
    
    # Traiter d'abord les fichiers dans le répertoire courant
    md_files = []
    subdirs = []
    
    for item in sorted(directory.iterdir()):
        if item.is_file() and item.suffix == '.md':
            md_files.append(item)
        elif item.is_dir() and not item.name.startswith('.'):
            subdirs.append(item)
    
    # Ajouter les fichiers Markdown du répertoire courant
    for md_file in md_files:
        nav_items.append(create_nav_item(md_file, docs_root))
    
    # Traiter les sous-répertoires
    for subdir in subdirs:
        subdir_nav = scan_directory(subdir, docs_root)
        if subdir_nav:
            # Utiliser le nom du répertoire comme titre de section
            section_title = subdir.name.replace('-', ' ').replace('_', ' ').title()
            
            # Mapper certains noms de dossiers vers des titres plus appropriés
            title_mapping = {
                'How-To': 'Guides',
                'how-to': 'Guides',
                'Reference': 'Référence',
                'Explanation': 'Explications',
                'Tutorials': 'Tutoriels',
                'Faq': 'FAQ',
                'Cloudpi': 'Cloud Pi Gen 2',
                'Kubepi': 'Kube Pi',
                'Cpin': 'Cloud Pi Native'
            }
            
            section_title = title_mapping.get(section_title, section_title)
            nav_items.append({section_title: subdir_nav})
    
    return nav_items


def update_mkdocs_nav(mkdocs_path: Path, docs_dir: Path):
    """
    Met à jour la section 'nav' du fichier mkdocs.yml.
    """
    # Lire le fichier mkdocs.yml existant
    with open(mkdocs_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parser le YAML
    mkdocs_config = yaml.safe_load(content)
    
    # Générer la nouvelle navigation
    new_nav = scan_directory(docs_dir, docs_dir)
    
    # Mettre à jour la configuration
    mkdocs_config['nav'] = new_nav
    
    # Sauvegarder avec une mise en forme correcte
    with open(mkdocs_path, 'w', encoding='utf-8') as f:
        # Écrire le YAML avec des paramètres de formatage appropriés
        yaml.dump(mkdocs_config, f, 
                 default_flow_style=False, 
                 allow_unicode=True, 
                 sort_keys=False,
                 width=120,
                 indent=2)
    
    print(f"✅ Navigation mise à jour dans {mkdocs_path}")


def main():
    """
    Fonction principale du script.
    """
    # Détecter automatiquement les chemins
    script_dir = Path(__file__).parent
    
    # Essayer différents emplacements possibles
    possible_configs = [
        script_dir / "public" / "mkdocs.yml",
        script_dir / "mkdocs.yml",
        script_dir / "internal" / "mkdocs.yml"
    ]
    
    mkdocs_path = None
    for config_path in possible_configs:
        if config_path.exists():
            mkdocs_path = config_path
            break
    
    if not mkdocs_path:
        print("❌ Fichier mkdocs.yml non trouvé!")
        print("Emplacements vérifiés:")
        for path in possible_configs:
            print(f"  - {path}")
        return
    
    # Déterminer le répertoire docs
    docs_dir = mkdocs_path.parent / "docs"
    
    if not docs_dir.exists():
        print(f"❌ Répertoire docs non trouvé: {docs_dir}")
        return
    
    print(f"📁 Répertoire docs: {docs_dir}")
    print(f"📄 Fichier mkdocs.yml: {mkdocs_path}")
    
    # Créer une sauvegarde
    backup_path = mkdocs_path.with_suffix('.yml.backup')
    with open(mkdocs_path, 'r', encoding='utf-8') as src, \
         open(backup_path, 'w', encoding='utf-8') as dst:
        dst.write(src.read())
    print(f"💾 Sauvegarde créée: {backup_path}")
    
    # Mettre à jour la navigation
    try:
        update_mkdocs_nav(mkdocs_path, docs_dir)
        print("✅ Navigation mise à jour avec succès!")
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour: {e}")
        # Restaurer la sauvegarde en cas d'erreur
        with open(backup_path, 'r', encoding='utf-8') as src, \
             open(mkdocs_path, 'w', encoding='utf-8') as dst:
            dst.write(src.read())
        print("🔄 Sauvegarde restaurée")


if __name__ == "__main__":
    main() 