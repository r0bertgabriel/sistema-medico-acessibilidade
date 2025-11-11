"""
Inicialização do pacote routes
"""
from .api import api_bp
from .main import main_bp

__all__ = ['main_bp', 'api_bp']
