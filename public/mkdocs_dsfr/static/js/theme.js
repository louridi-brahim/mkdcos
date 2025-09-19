/**
 * Fichier principal du thème DSFR
 * Initialise tous les modules
 */

class DSFRTheme {
  constructor() {
    this.modules = {};
    this.init();
  }

  async init() {
    // Initialiser les modules dans l'ordre approprié
    await this.initializeModules();
  }

  async initializeModules() {
    try {
      // Module de recherche
      if (window.SearchModule) {
        this.modules.search = new SearchModule();
      }

      // Module de copie de code
      if (window.CodeCopyModule) {
        this.modules.codeCopy = new CodeCopyModule();
      }

      // Module responsive
      if (window.ResponsiveModule) {
        this.modules.responsive = new ResponsiveModule();
      }

    } catch (error) {
      // Erreur silencieuse pour éviter la pollution de la console
    }
  }

  // Méthode pour réinitialiser les modules si nécessaire
  reinitialize() {
    this.init();
  }

  // Méthode pour accéder aux modules depuis l'extérieur
  getModule(name) {
    return this.modules[name];
  }
}

// Initialisation automatique quand le DOM est prêt
document.addEventListener('DOMContentLoaded', () => {
  window.dsfrTheme = new DSFRTheme();
});

// Export pour utilisation externe
window.DSFRTheme = DSFRTheme;
