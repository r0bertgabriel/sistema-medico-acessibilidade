"""
Rotas da API
"""
from data import obter_todos_exemplos
from flask import Blueprint, jsonify, request
from services import AudioService, ECGService

api_bp = Blueprint('api', __name__, url_prefix='/api')

# Instanciar serviços
ecg_service = ECGService()
audio_service = AudioService()


@api_bp.route('/anunciar', methods=['POST'])
def anunciar_texto():
    """
    Endpoint para gerar e reproduzir áudio de acessibilidade
    Usa o mesmo sistema de voz dos laudos (gTTS)
    """
    try:
        dados = request.get_json()
        texto = dados.get('texto', '')
        
        if not texto:
            return jsonify({'success': False, 'error': 'Texto vazio'}), 400
        
        # Gerar áudio
        audio_path = audio_service.gerar_audio(texto)
        
        return jsonify({
            'success': True,
            'audio_url': f'/static/{audio_path}'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@api_bp.route('/analisar', methods=['POST'])
def analisar_ecg():
    """
    Endpoint para análise de ECG
    Recebe dados em JSON e retorna laudo completo
    """
    try:
        dados_json = request.get_json()
        
        # Analisar ECG
        resultado = ecg_service.analisar_ecg(dados_json)
        
        # Gerar áudio do laudo
        audio_path = audio_service.gerar_audio(resultado['laudo_audio_texto'])
        
        # Limpar áudios antigos
        audio_service.limpar_audios_antigos()
        
        return jsonify({
            'success': True,
            'laudo_texto': resultado['laudo_texto'],
            'laudo_audio_texto': resultado['laudo_audio_texto'],
            'audio_url': f'/static/{audio_path}',
            'achados': resultado['achados'],
            'diagnosticos': resultado['diagnosticos']
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@api_bp.route('/resultados')
def obter_resultados():
    """
    Retorna resultados de ECG da fila de pacientes
    """
    resultados = obter_todos_exemplos()
    return jsonify(resultados)


@api_bp.route('/resultado/<tipo>', methods=['POST'])
def processar_resultado(tipo):
    """
    Processa um resultado específico e retorna o laudo
    """
    resultados = obter_todos_exemplos()
    
    if tipo not in resultados:
        return jsonify({'success': False, 'error': 'Resultado não encontrado'}), 404
    
    dados_ecg = resultados[tipo]
    
    # Converter DadosECG para dict usando método to_dict()
    dados_dict = dados_ecg.to_dict()
    
    # Analisar
    resultado = ecg_service.analisar_ecg(dados_dict)
    
    # Gerar áudio
    audio_path = audio_service.gerar_audio(resultado['laudo_audio_texto'])
    
    # Limpar áudios antigos
    audio_service.limpar_audios_antigos()
    
    return jsonify({
        'success': True,
        'paciente': dados_ecg.nome_paciente,
        'laudo_texto': resultado['laudo_texto'],
        'laudo_audio_texto': resultado['laudo_audio_texto'],
        'audio_url': f'/static/{audio_path}',
        'achados': resultado['achados'],
        'diagnosticos': resultado['diagnosticos']
    })
