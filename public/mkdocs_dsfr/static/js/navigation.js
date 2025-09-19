/**
 * Module de navigation DSFR
 * Gère le scroll vers l'élément actif
 */

class NavigationModule {
  constructor() {
    this.init();
  }

  init() {
    // Highlight de l'élément actif au chargement
    document.addEventListener('DOMContentLoaded', () => {
      this.highlightActiveNavigation();
    });
  }

  highlightActiveNavigation() {
    // Scroll vers l'élément actif si nécessaire
    const activeLink = document.querySelector('.fr-sidemenu__link--active');
    
    if (activeLink) {
      // Faire défiler vers l'élément actif si nécessaire
      setTimeout(() => {
        activeLink.scrollIntoView({ 
          behavior: 'smooth', 
          block: 'nearest',
          inline: 'nearest'
        });
      }, 100);
    }
  }
}

// Export pour utilisation
window.NavigationModule = NavigationModule;

// Initialisation automatique
new NavigationModule();