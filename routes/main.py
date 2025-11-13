"""
Rotas principais da aplicação (páginas)
"""
from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Página inicial"""
    return render_template('index.html')


@main_bp.route('/ecg')
def ecg():
    """Página central do módulo ECG"""
    return render_template('ecg.html')


@main_bp.route('/analise')
def analise():
    """Página de análise de ECG"""
    return render_template('analise.html')


@main_bp.route('/analise-imagem')
def analise_imagem():
    """Página de análise de ECG por imagem"""
    return render_template('analise_imagem.html')


@main_bp.route('/resultados')
def resultados():
    """Página com fila de resultados de pacientes"""
    return render_template('resultados.html')


@main_bp.route('/teste-acessibilidade')
def teste_acessibilidade():
    """Página de teste para verificar feedback auditivo"""
    return render_template('teste_acessibilidade.html')


@main_bp.route('/hemograma')
def hemograma():
    """Página central do módulo Hemograma"""
    return render_template('hemograma_hub.html')


@main_bp.route('/hemograma/analise')
def hemograma_analise():
    """Página de análise de hemograma"""
    return render_template('hemograma.html')


@main_bp.route('/hemograma-resultados')
def hemograma_resultados():
    """Página com resultados de hemogramas"""
    return render_template('hemograma_resultados.html')
