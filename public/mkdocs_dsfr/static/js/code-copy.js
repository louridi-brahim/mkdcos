/**
 * Module de copie de code
 * Ajoute des boutons de copie aux blocs de code
 */

class CodeCopyModule {
  constructor() {
    this.init();
  }

  init() {
    this.addCopyButtons();
    this.setupMutationObserver();
  }

  // Fonction pour ajouter les boutons de copie aux blocs de code
  addCopyButtons() {
    // Trouver tous les blocs de code
    const codeBlocks = document.querySelectorAll('pre code, .highlight pre, .codehilite pre');
    
    codeBlocks.forEach((codeBlock) => {
      // Vérifier si un bouton de copie existe déjà
      const existingButton = codeBlock.parentElement.querySelector('.copy-code-button');
      if (existingButton) {
        return; // Bouton déjà présent
      }
      
      // Créer le bouton de copie
      const copyButton = this.createCopyButton();
      
      // Ajouter le bouton au conteneur approprié
      this.appendButtonToContainer(codeBlock, copyButton);
    });
  }

  createCopyButton() {
    const copyButton = document.createElement('button');
    copyButton.className = 'copy-code-button';
    copyButton.setAttribute('aria-label', 'Copier le code');
    copyButton.title = 'Copier le code';
    
    // Ajouter l'icône et le texte
    copyButton.innerHTML = `
      <svg class="copy-icon" viewBox="0 0 24 24" aria-hidden="true">
        <path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/>
      </svg>
      Copier
    `;
    
    // Gérer le clic sur le bouton
    copyButton.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      this.handleCopyClick(copyButton);
    });

    return copyButton;
  }

  appendButtonToContainer(codeBlock, copyButton) {
    const container = codeBlock.parentElement;
    if (container.tagName === 'PRE') {
      // Le code est dans un <pre>, ajouter le bouton au parent du <pre>
      const wrapper = container.parentElement;
      if (wrapper && !wrapper.classList.contains('highlight')) {
        // Créer un wrapper si nécessaire
        const highlightWrapper = document.createElement('div');
        highlightWrapper.className = 'highlight';
        container.parentNode.insertBefore(highlightWrapper, container);
        highlightWrapper.appendChild(container);
        highlightWrapper.appendChild(copyButton);
      } else {
        wrapper.appendChild(copyButton);
      }
    } else {
      // Le code est dans un autre conteneur
      container.style.position = 'relative';
      container.appendChild(copyButton);
    }
  }

  handleCopyClick(copyButton) {
    // Récupérer le texte du code
    const codeBlock = copyButton.parentElement.querySelector('code, pre');
    if (!codeBlock) return;

    let codeText = codeBlock.textContent || codeBlock.innerText;
    
    // Nettoyer le texte (enlever les numéros de ligne, etc.)
    codeText = codeText.replace(/^\d+\s+/gm, ''); // Enlever les numéros de ligne
    codeText = codeText.trim();
    
    // Copier dans le presse-papiers
    if (navigator.clipboard && window.isSecureContext) {
      // API moderne
      navigator.clipboard.writeText(codeText).then(() => {
        this.showCopySuccess(copyButton);
      }).catch(() => {
        this.fallbackCopy(codeText, copyButton);
      });
    } else {
      // Fallback pour les navigateurs plus anciens
      this.fallbackCopy(codeText, copyButton);
    }
  }

  // Fonction de fallback pour la copie
  fallbackCopy(text, button) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
      const successful = document.execCommand('copy');
      if (successful) {
        this.showCopySuccess(button);
      } else {
        this.showCopyError(button);
      }
    } catch (err) {
      this.showCopyError(button);
    } finally {
      document.body.removeChild(textArea);
    }
  }

  // Fonction pour afficher le succès de la copie
  showCopySuccess(button) {
    const originalText = button.innerHTML;
    button.classList.add('copied');
    button.innerHTML = `
      <svg class="copy-icon" viewBox="0 0 24 24" aria-hidden="true">
        <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
      </svg>
      Copié !
    `;
    
    setTimeout(() => {
      button.classList.remove('copied');
      button.innerHTML = originalText;
    }, 2000);
  }

  // Fonction pour afficher l'erreur de copie
  showCopyError(button) {
    const originalText = button.innerHTML;
    button.style.background = '#dc3545';
    button.innerHTML = `
      <svg class="copy-icon" viewBox="0 0 24 24" aria-hidden="true">
        <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
      </svg>
      Erreur
    `;
    
    setTimeout(() => {
      button.style.background = '';
      button.innerHTML = originalText;
    }, 2000);
  }

  setupMutationObserver() {
    // Observer les changements dans le DOM pour ajouter les boutons aux nouveaux blocs de code
    if (window.MutationObserver) {
      const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
          if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
            // Vérifier si de nouveaux blocs de code ont été ajoutés
            const hasCodeBlocks = Array.from(mutation.addedNodes).some((node) => {
              return node.nodeType === 1 && (
                node.tagName === 'PRE' ||
                node.querySelector && node.querySelector('pre')
              );
            });
            
            if (hasCodeBlocks) {
              setTimeout(() => this.addCopyButtons(), 100); // Petit délai pour laisser le temps au rendu
            }
          }
        });
      });
      
      observer.observe(document.body, {
        childList: true,
        subtree: true
      });
    }
  }
}

// Export pour utilisation
window.CodeCopyModule = CodeCopyModule;
