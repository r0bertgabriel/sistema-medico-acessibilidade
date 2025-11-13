"""
Módulo models - Sistema de análise de ECG e Hemograma
"""
from .ecg_analyzer import AnalisadorECG
from .ecg_data import DadosECG
from .hemograma_analyzer import AnalisadorHemograma
from .hemograma_data import DadosHemograma
from .laudo_generator import GeradorLaudo

__all__ = [
    'DadosECG',
    'AnalisadorECG',
    'GeradorLaudo',
    'DadosHemograma',
    'AnalisadorHemograma'
]

# Alias para compatibilidade
LaudoGenerator = GeradorLaudo
