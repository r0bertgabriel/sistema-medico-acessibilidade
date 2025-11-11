"""
Rotas principais da aplicação (páginas)
"""
from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Página inicial"""
    return render_template('index.html')


@main_bp.route('/analise')
def analise():
    """Página de análise de ECG"""
    return render_template('analise.html')


@main_bp.route('/resultados')
def resultados():
    """Página com fila de resultados de pacientes"""
    return render_template('resultados.html')


@main_bp.route('/teste-acessibilidade')
def teste_acessibilidade():
    """Página de teste para verificar feedback auditivo"""
    return render_template('teste_acessibilidade.html')
