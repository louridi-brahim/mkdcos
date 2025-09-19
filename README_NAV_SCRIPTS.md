# Scripts de Génération de Navigation MkDocs

Ce projet contient deux scripts Python pour générer automatiquement la section `nav` du fichier `mkdocs.yml` en parcourant l'arborescence du dossier `docs`.

## Scripts Disponibles

### 1. `update_nav.py` - Script Simple

Script basique qui génère automatiquement la navigation complète.

**Utilisation :**
```bash
python update_nav.py
```

**Fonctionnalités :**
- Parcourt récursivement le dossier `docs`
- Extrait les titres depuis les fichiers Markdown (front matter YAML ou titre H1)
- Génère une structure de navigation hiérarchique
- Crée automatiquement une sauvegarde
- Détecte automatiquement l'emplacement du fichier `mkdocs.yml`

### 2. `update_nav_advanced.py` - Script Avancé

Script avec options de personnalisation et configuration avancée.

**Utilisation :**
```bash
# Utilisation basique
python update_nav_advanced.py

# Avec fichier de configuration personnalisé
python update_nav_advanced.py --config nav_config.json

# Mode test (aperçu sans modification)
python update_nav_advanced.py --dry-run

# Spécifier un fichier mkdocs.yml particulier
python update_nav_advanced.py --mkdocs-path /chemin/vers/mkdocs.yml

# Générer un fichier de configuration template
python update_nav_advanced.py --generate-config nav_config.json
```

## Configuration Avancée

Le script avancé accepte un fichier de configuration JSON pour personnaliser le comportement :

### Générer un Template de Configuration

```bash
python update_nav_advanced.py --generate-config nav_config.json
```

### Structure du Fichier de Configuration

```json
{
  "title_mapping": {
    "how-to": "Guides",
    "reference": "Référence",
    "explanation": "Explications",
    "tutorials": "Tutoriels",
    "faq": "FAQ",
    "cloudpi": "Cloud Pi Gen 2",
    "kubepi": "Kube Pi"
  },
  "file_order": [
    "index.md",
    "overview.md",
    "readme.md"
  ],
  "folder_order": [
    "tutorials",
    "how-to",
    "reference",
    "explanation",
    "faq"
  ],
  "exclude_files": [
    ".DS_Store",
    "Thumbs.db"
  ],
  "exclude_folders": [
    ".git",
    ".vscode",
    "__pycache__",
    "node_modules"
  ],
  "custom_titles": {
    "concepteur/overview.md": "Vue d'ensemble - Concepteur",
    "souscripteur/overview.md": "Vue d'ensemble - Souscripteur"
  },
  "preserve_manual_nav": [
    "Section manuelle à préserver"
  ]
}
```

### Options de Configuration

- **`title_mapping`** : Mapping des noms de dossiers vers des titres personnalisés
- **`file_order`** : Ordre de priorité pour les fichiers (les fichiers listés apparaîtront en premier)
- **`folder_order`** : Ordre de priorité pour les dossiers
- **`exclude_files`** : Fichiers à ignorer
- **`exclude_folders`** : Dossiers à ignorer
- **`custom_titles`** : Titres personnalisés pour des fichiers spécifiques
- **`preserve_manual_nav`** : Sections de navigation manuelle à préserver

## Extraction des Titres

Les scripts extraient les titres des fichiers Markdown dans cet ordre de priorité :

1. **Titre personnalisé** (défini dans `custom_titles`)
2. **Front matter YAML** (`title: Mon Titre`)
3. **Premier titre H1** (`# Mon Titre`)
4. **Nom du fichier formaté** (si aucun titre trouvé)

## Fonctionnalités Avancées

### Mode Test
```bash
python update_nav_advanced.py --dry-run
```
Affiche un aperçu de la navigation générée sans modifier le fichier.

### Sauvegarde Automatique
Les scripts créent automatiquement une sauvegarde du fichier `mkdocs.yml` original avec l'extension `.backup`.

### Détection Automatique
Les scripts détectent automatiquement l'emplacement du fichier `mkdocs.yml` dans :
- `public/mkdocs.yml`
- `mkdocs.yml`
- `internal/mkdocs.yml`

## Exemple de Structure Générée

Pour une structure de dossiers comme :
```
docs/
├── index.md
├── demarrage-outillage.md
├── concepteur/
│   ├── overview.md
│   ├── tutorials/
│   │   └── prise-en-main-haxo.md
│   └── how-to/
│       └── deployer-bastion-horizon.md
└── souscripteur/
    ├── overview.md
    └── reference/
        └── offres-iaas.md
```

Le script génèrera :
```yaml
nav:
  - Documentation Technique: index.md
  - Demarrage Outillage: demarrage-outillage.md
  - Concepteur:
      - Vue d'ensemble: concepteur/overview.md
      - Tutoriels:
          - Prise en main du poste HAXO: concepteur/tutorials/prise-en-main-haxo.md
      - Guides:
          - Déployer le bastion d'administration via HORIZON: concepteur/how-to/deployer-bastion-horizon.md
  - Souscripteur:
      - Vue d'ensemble: souscripteur/overview.md
      - Référence:
          - IaaS: souscripteur/reference/offres-iaas.md
```

## Prérequis

```bash
pip install pyyaml
```

## Bonnes Pratiques

1. **Utilisez le mode test** avant d'appliquer les changements sur un projet important
2. **Définissez des titres H1** dans vos fichiers Markdown pour de meilleurs résultats
3. **Utilisez le front matter YAML** pour des titres complexes ou avec caractères spéciaux
4. **Personnalisez la configuration** pour adapter l'ordre et les titres à votre projet
5. **Vérifiez les sauvegardes** automatiques en cas de problème

## Dépannage

### Le script ne trouve pas le fichier mkdocs.yml
Utilisez l'option `--mkdocs-path` pour spécifier le chemin exact :
```bash
python update_nav_advanced.py --mkdocs-path /chemin/vers/mkdocs.yml
```

### Les titres ne sont pas extraits correctement
Vérifiez que vos fichiers Markdown ont :
- Un titre H1 (`# Mon Titre`) en début de fichier
- Ou un front matter YAML avec `title: Mon Titre`

### Ordre des éléments incorrect
Modifiez les sections `file_order` et `folder_order` dans votre fichier de configuration.

## Automatisation

Vous pouvez intégrer ces scripts dans votre workflow de CI/CD ou les exécuter automatiquement lors de modifications des fichiers de documentation.

### Exemple avec un script bash
```bash
#!/bin/bash
# Mettre à jour la navigation après modification des docs
cd /chemin/vers/projet
python update_nav_advanced.py --config nav_config.json
echo "Navigation mise à jour"
``` 