"""Thème MkDocs conforme au Système de Design de l'État Français (DSFR)"""

from mkdocs.theme import Theme
import os
import logging

logger = logging.getLogger('mkdocs')

class DSFRTheme(Theme):
    """Thème MkDocs conforme au Système de Design de l'État Français (DSFR)"""
    
    def __init__(self):
        super().__init__(
            name='dsfr',
            static_templates={
                '404.html',
                'sitemap.xml',
                'sitemap.xml.template',
            }
        ) 

def on_config(config):
    """Hook pour le chargement de la configuration."""
    logger.info(f"Thème DSFR : {os.path.abspath(__file__)}")
    logger.info(f"Templates : {os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')}")
    return config 