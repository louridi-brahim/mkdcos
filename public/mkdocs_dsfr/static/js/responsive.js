/**
 * Module de gestion responsive
 * Gère les adaptations pour différentes tailles d'écran selon les standards DSFR
 */

class ResponsiveModule {
  constructor() {
    this.breakpoints = {
      mobile: 576,
      tablet: 768,
      desktop: 992,
      large: 1200
    };
    this.init();
  }

  init() {
    // DSFR FIRST : DSFR gère nativement le responsive
    this.initBreadcrumbResponsive();
    // initSidebarToggle et initSidebarResizer supprimés - DSFR gère cela nativement
  }

  // Méthodes utilitaires pour les breakpoints DSFR
  isMobile() {
    return window.innerWidth < this.breakpoints.tablet;
  }

  isTablet() {
    return window.innerWidth >= this.breakpoints.tablet && window.innerWidth < this.breakpoints.desktop;
  }

  isDesktop() {
    return window.innerWidth >= this.breakpoints.desktop;
  }

  isLargeScreen() {
    return window.innerWidth >= this.breakpoints.large;
  }

  // Gestion responsive simple du fil d'Ariane
  initBreadcrumbResponsive() {
    const breadcrumbButton = document.querySelector('.fr-breadcrumb__button');
    const breadcrumbCollapse = document.querySelector('#breadcrumb-collapse');
    
    if (breadcrumbButton && breadcrumbCollapse) {
      const handleBreadcrumbResponsive = () => {
        if (this.isDesktop()) {
          // Sur desktop/tablet, toujours afficher le fil d'Ariane
          breadcrumbCollapse.classList.remove('fr-collapse');
          breadcrumbButton.style.display = 'none';
        } else {
          // Sur mobile, montrer le bouton et gérer le collapse
          breadcrumbButton.style.display = 'block';
          if (breadcrumbButton.getAttribute('aria-expanded') !== 'true') {
            breadcrumbCollapse.classList.add('fr-collapse');
          }
        }
      };
      
      window.addEventListener('resize', handleBreadcrumbResponsive);
      handleBreadcrumbResponsive(); // Initialisation
    }
  }

}

// Export pour utilisation
window.ResponsiveModule = ResponsiveModule;
