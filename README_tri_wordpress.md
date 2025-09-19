# Script de Tri du Contenu WordPress

Ce script Python automatise l'organisation du contenu WordPress en utilisant un fichier CSV de configuration.

## 📋 Description

Le script `tri_wordpress.py` lit le fichier `tri.csv` et copie automatiquement les articles depuis le répertoire source (colonne C) vers le répertoire de destination (colonne D).

## 🗂️ Structure des fichiers

```
mkdocs-poc/
├── tri_wordpress.py              # Script principal
├── exemple_utilisation.py        # Script d'exemple
├── tri.csv                      # Fichier de configuration (source des instructions)
├── wordpress-content-to-sort/    # Répertoire contenant le contenu à trier
└── README_tri_wordpress.md       # Cette documentation
```

## 📊 Format du fichier CSV

Le fichier `tri.csv` doit contenir les colonnes suivantes :

| Colonne | Nom | Description |
|---------|-----|-------------|
| A | Titre | Titre de l'article (informatif) |
| B | Chemin actuel | URL actuelle (informatif) |
| C | Répertoire d'export | **Chemin source** relatif depuis `wordpress-content-to-sort/` |
| D | Destination | **Chemin destination** où copier le contenu |

### Exemple de contenu CSV :
```csv
Titre,Chemin actuel,Répertoire d'export,Destination 
Architecture de microservices,https://...,content/architecture-de-microservices,public/docs/concepteur/FAQ
DevOps,https://...,content/devops,public/docs/concepteur/FAQ
```

## 🚀 Utilisation

### 1. Mode simulation (recommandé)

Testez d'abord ce que le script ferait sans modifier aucun fichier :

```bash
python3 tri_wordpress.py --simulation
```

### 2. Exécution normale

Une fois satisfait de la simulation, exécutez réellement :

```bash
python3 tri_wordpress.py
```

### 3. Options avancées

```bash
# Utiliser des chemins personnalisés
python3 tri_wordpress.py --repertoire-base mon-wordpress --fichier-csv mon-tri.csv

# Afficher l'aide
python3 tri_wordpress.py --help
```

### 4. Script d'exemple interactif

Pour une utilisation guidée :

```bash
python3 exemple_utilisation.py
```

## ⚙️ Options disponibles

| Option | Description | Défaut |
|--------|-------------|--------|
| `--repertoire-base`, `-r` | Répertoire de base contenant le contenu | `wordpress-content-to-sort` |
| `--fichier-csv`, `-f` | Fichier CSV avec les instructions | `tri.csv` |
| `--simulation`, `-s` | Mode simulation (aucune modification) | Non |
| `--help`, `-h` | Afficher l'aide | - |

## 📁 Fonctionnement détaillé

1. **Lecture du CSV** : Le script lit `tri.csv` et extrait les informations de tri
2. **Vérifications** : Contrôle l'existence du répertoire de base et du fichier CSV
3. **Traitement** : Pour chaque ligne du CSV :
   - Construit le chemin source : `wordpress-content-to-sort/[Répertoire d'export]`
   - Crée les répertoires de destination si nécessaire
   - Copie le contenu vers : `[Destination]/[nom du répertoire source]`
4. **Résumé** : Affiche les statistiques de réussite/échec

## ✅ Exemple de sortie

```
🚀 Démarrage du script de tri du contenu WordPress
============================================================
📖 Lecture du fichier de tri : tri.csv
✅ 294 opérations de tri trouvées

📁 [1/294] Traitement : Architecture de microservices
   Source : content/architecture-de-microservices
   Destination : public/docs/concepteur/FAQ
   ✅ Copie réussie vers public/docs/concepteur/FAQ/architecture-de-microservices

...

============================================================
📊 RÉSUMÉ DES OPÉRATIONS
✅ Réussites : 290
❌ Échecs : 4
📈 Total traité : 294
```

## 🛡️ Sécurité et bonnes pratiques

### ⚠️ Avant l'exécution

1. **Sauvegarde** : Faites toujours une sauvegarde de vos données
2. **Simulation** : Utilisez `--simulation` pour tester d'abord
3. **Vérification** : Contrôlez que le fichier `tri.csv` est correct
4. **Droits** : Assurez-vous d'avoir les permissions d'écriture

### 🔒 Fonctionnalités de sécurité

- **Validation des chemins** : Vérification de l'existence des sources
- **Création sécurisée** : Les répertoires sont créés de manière récursive
- **Gestion d'erreurs** : Chaque opération est isolée (une erreur n'arrête pas le processus)
- **Mode simulation** : Test sans modification

## 🔧 Résolution de problèmes

### Erreurs communes

| Erreur | Cause | Solution |
|--------|-------|----------|
| `FileNotFoundError: tri.csv` | Fichier CSV manquant | Vérifiez que `tri.csv` existe |
| `Répertoire de base n'existe pas` | Dossier source manquant | Créez `wordpress-content-to-sort/` |
| `Source inexistante` | Chemin dans CSV incorrect | Vérifiez les chemins dans le CSV |
| `Permission denied` | Droits insuffisants | Vérifiez les permissions d'écriture |

### Débogage

1. Utilisez `--simulation` pour identifier les problèmes
2. Vérifiez les chemins dans le fichier CSV
3. Contrôlez les permissions des répertoires
4. Examinez les messages d'erreur détaillés

## 📝 Notes importantes

- **Écrasement** : Si le répertoire de destination existe, il sera écrasé
- **Structure** : Le script préserve la structure des répertoires sources
- **Encodage** : Le CSV doit être en UTF-8
- **Chemins relatifs** : Tous les chemins sont relatifs au répertoire de travail

## 🆘 Support

En cas de problème :

1. Vérifiez cette documentation
2. Utilisez `python3 tri_wordpress.py --help`
3. Testez avec `--simulation`
4. Examinez les messages d'erreur détaillés

---

*Script créé pour automatiser l'organisation du contenu WordPress selon les spécifications du fichier tri.csv*

