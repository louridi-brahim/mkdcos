# Test de la fonctionnalité de copie de code

Cette page permet de tester la fonctionnalité de copie de code implémentée dans le thème DSFR.

## Bloc de code simple

```bash
echo "Bonjour, monde !"
cd /home/utilisateur
ls -la
```

## Bloc de code Python

```python
def hello_world():
    """Fonction qui affiche un message de salutation."""
    print("Bonjour, monde !")
    return "success"

if __name__ == "__main__":
    result = hello_world()
    print(f"Résultat: {result}")
```

## Bloc de code YAML

```yaml
# Configuration MkDocs
site_name: Documentation Cloud π
site_description: Direction de la Transformation Numérique du ministère de l'Intérieur
theme:
  name: null
  custom_dir: mkdocs_dsfr
  language: fr
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - content.code.copy
```

## Bloc de code JavaScript

```javascript
// Fonction de copie de code
function copyToClipboard(text) {
    if (navigator.clipboard && window.isSecureContext) {
        return navigator.clipboard.writeText(text);
    } else {
        // Fallback pour les navigateurs plus anciens
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
    }
}
```

## Bloc de code avec numéros de ligne

```bash
1  #!/bin/bash
2  # Script de déploiement
3  echo "Début du déploiement..."
4  
5  # Vérification des prérequis
6  if [ ! -f "requirements.txt" ]; then
7      echo "Erreur: requirements.txt non trouvé"
8      exit 1
9  fi
10 
11 echo "Déploiement terminé avec succès"
```

## Code inline

Voici un exemple de code inline : `pip install mkdocs-material` qui peut aussi être copié.

## Blocs de code en liste

1. Première étape - Installation:
   ```bash
   sudo apt-get update
   sudo apt-get install python3-pip
   ```

2. Deuxième étape - Configuration:
   ```yaml
   plugins:
     - search
     - material
   ```

3. Troisième étape - Démarrage:
   ```bash
   mkdocs serve
   ```

## Instructions de test

Pour tester la fonctionnalité :

1. **Bouton de copie visible** : Chaque bloc de code devrait avoir un bouton "Copier" dans le coin supérieur droit
2. **Copie fonctionnelle** : Cliquer sur le bouton devrait copier le contenu dans le presse-papiers
3. **Feedback visuel** : Le bouton devrait changer en "Copié !" avec une icône de coche pendant 2 secondes
4. **Responsive** : Sur mobile, le bouton devrait s'adapter à la taille de l'écran
5. **Accessibilité** : Le bouton devrait être accessible au clavier et avoir les attributs ARIA appropriés

## Test de caractères spéciaux

```json
{
  "nom": "Ministère de l'Intérieur",
  "description": "Documentation Cloud π",
  "caractères_spéciaux": "àéèùçâêîôû",
  "emojis": "🚀 📚 ⚡ 🔧",
  "symboles": "€ $ £ ¥ © ® ™"
}
```
