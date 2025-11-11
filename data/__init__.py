"""
Inicialização do pacote data
"""
from .ecg_examples import (
    criar_exemplo_arritmia,
    criar_exemplo_bloqueio,
    criar_exemplo_normal,
    obter_todos_exemplos,
)

__all__ = [
    'criar_exemplo_normal',
    'criar_exemplo_arritmia',
    'criar_exemplo_bloqueio',
    'obter_todos_exemplos',
]
