/**
 * Module de recherche MkDocs
 * Gère la recherche dans la documentation
 */

class SearchModule {
  constructor() {
    this.searchIndex = null;
    this.searchConfig = null;
    this.init();
  }

  async init() {
    console.log('Initialisation du module de recherche...');
    await this.loadSearchIndex();
    this.setupEventListeners();
  }

  // Fonction pour charger l'index de recherche
  async loadSearchIndex() {
    try {
      const response = await fetch('search/search_index.json');
      const data = await response.json();
      this.searchIndex = data.docs;
      this.searchConfig = data.config;
      console.log('Index de recherche chargé:', this.searchIndex.length, 'documents');
    } catch (error) {
      console.error('Erreur lors du chargement de l\'index de recherche:', error);
    }
  }

  // Fonction de recherche simple (recherche dans le titre et le contenu)
  searchDocuments(query) {
    if (!this.searchIndex || !query || query.length < this.searchConfig.min_search_length) {
      return [];
    }
    
    const results = [];
    const queryLower = query.toLowerCase();
    
    for (const doc of this.searchIndex) {
      let score = 0;
      const title = doc.title || '';
      const text = doc.text || '';
      
      // Recherche dans le titre (score plus élevé)
      if (title.toLowerCase().includes(queryLower)) {
        score += 10;
      }
      
      // Recherche dans le contenu
      if (text.toLowerCase().includes(queryLower)) {
        score += 1;
      }
      
      // Recherche exacte (score encore plus élevé)
      if (title.toLowerCase() === queryLower) {
        score += 20;
      }
      
      if (score > 0) {
        results.push({
          ...doc,
          score: score
        });
      }
    }
    
    // Trier par score décroissant
    results.sort((a, b) => b.score - a.score);
    
    return results.slice(0, 10); // Limiter à 10 résultats
  }

  // Fonction pour afficher les résultats
  displaySearchResults(results, query) {
    const resultsContainer = document.getElementById('mkdocs-search-results');
    const contentContainer = document.getElementById('mkdocs-search-results-content');
    const mainContent = document.querySelector('main .fr-col-12.fr-col-md-9 > div:not(#mkdocs-search-results)');
    
    if (results.length === 0) {
      contentContainer.innerHTML = `
        <div class="fr-alert fr-alert--warning">
          <p>Aucun résultat trouvé pour "${query}"</p>
        </div>
      `;
    } else {
      let html = `<div class="fr-alert fr-alert--success"><p>${results.length} résultat(s) trouvé(s) pour "${query}"</p></div>`;
      
      html += '<div class="fr-list">';
      results.forEach(result => {
        const url = result.location ? `${result.location}` : '#';
        const title = result.title || 'Sans titre';
        const excerpt = result.text ? result.text.substring(0, 200) + '...' : '';
        
        html += `
          <div class="fr-list__item">
            <div class="fr-list__title">
              <a href="${url}" class="fr-link">${title}</a>
            </div>
            ${excerpt ? `<div class="fr-list__desc">${excerpt}</div>` : ''}
          </div>
        `;
      });
      html += '</div>';
      
      contentContainer.innerHTML = html;
    }
    
    // Afficher les résultats et masquer le contenu principal
    resultsContainer.style.display = 'block';
    if (mainContent) {
      mainContent.style.display = 'none';
    }
  }

  // Fonction pour masquer les résultats et afficher le contenu principal
  hideSearchResults() {
    const resultsContainer = document.getElementById('mkdocs-search-results');
    const mainContent = document.querySelector('main .fr-col-12.fr-col-md-9 > div:not(#mkdocs-search-results)');
    
    resultsContainer.style.display = 'none';
    if (mainContent) {
      mainContent.style.display = 'block';
    }
  }

  // Fonction de recherche principale
  performSearch(query) {
    if (!query || query.trim() === '') {
      this.hideSearchResults();
      return;
    }
    
    const results = this.searchDocuments(query.trim());
    this.displaySearchResults(results, query.trim());
  }

  setupEventListeners() {
    // Gestionnaire pour le bouton de recherche
    const searchButton = document.getElementById('search-button');
    const searchInput = document.getElementById('search-query');
    
    if (searchButton && searchInput) {
      searchButton.addEventListener('click', () => {
        this.performSearch(searchInput.value);
      });
      
      // Gestionnaire pour la touche Entrée
      searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
          this.performSearch(e.target.value);
        }
      });
      
      // Gestionnaire pour effacer la recherche
      searchInput.addEventListener('input', (e) => {
        if (e.target.value === '') {
          this.hideSearchResults();
        }
      });
    }
    
    console.log('Module de recherche initialisé');
  }
}

// Export pour utilisation
window.SearchModule = SearchModule;
