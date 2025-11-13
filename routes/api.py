"""
Rotas da API
"""
from flask import Blueprint, jsonify, request

import config
from data import obter_todos_exemplos
from services import AudioService, ECGService
from services.hemograma_service import HemogramaService

api_bp = Blueprint('api', __name__, url_prefix='/api')

# Instanciar serviços
ecg_service = ECGService()
hemograma_service = HemogramaService()
audio_service = AudioService()
vision_service = None  # Será inicializado sob demanda

# Criar diretório de uploads se não existir
config.UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)


def allowed_file(filename):
    """Verifica se o arquivo tem uma extensão permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS


def get_vision_service():
    """Retorna instância do VisionService (lazy loading)"""
    global vision_service
    if vision_service is None:
        try:
            from services.vision_service import VisionService
            vision_service = VisionService()
        except (ImportError, ValueError):
            # API key não configurada ou módulo openai não instalado
            return None
    return vision_service


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


@api_bp.route('/analisar_imagem', methods=['POST'])
def analisar_ecg_imagem():
    """
    Endpoint para análise de ECG a partir de imagem
    Usa GPT-4o Vision para extrair dados do ECG e gera laudo com áudio
    """
    try:
        # Verificar se o serviço Vision está disponível
        vs = get_vision_service()
        if vs is None:
            return jsonify({
                'success': False,
                'error': 'Serviço de análise por imagem não configurado. '
                        'Configure a variável de ambiente OPENAI_API_KEY.'
            }), 500
        
        # Verificar se há arquivo na requisição
        if 'imagem' not in request.files:
            return jsonify({
                'success': False,
                'error': 'Nenhuma imagem foi enviada'
            }), 400
        
        file = request.files['imagem']
        
        # Verificar se um arquivo foi selecionado
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'Nenhum arquivo selecionado'
            }), 400
        
        # Verificar extensão do arquivo
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': f'Formato de arquivo não permitido. '
                        f'Use: {", ".join(config.ALLOWED_EXTENSIONS)}'
            }), 400
        
        # Salvar arquivo temporariamente
        import os

        from werkzeug.utils import secure_filename
        filename = secure_filename(file.filename or 'upload')
        filepath = config.UPLOAD_FOLDER / filename
        file.save(str(filepath))
        
        try:
            # Analisar imagem com GPT-4o Vision
            dados_vision = vs.analisar_ecg_imagem(str(filepath))
            
            # Converter para formato do sistema
            dados_sistema = vs.converter_para_formato_sistema(dados_vision)
            
            # Analisar com o serviço de ECG
            resultado = ecg_service.analisar_ecg(dados_sistema)
            
            # Adicionar informações da análise Vision ao resultado
            resultado['analise_vision'] = dados_vision
            resultado['conclusao_ia'] = dados_sistema.get('conclusao_ia', {})
            
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
                'diagnosticos': resultado['diagnosticos'],
                'analise_vision': dados_vision,
                'conclusao_ia': dados_sistema.get('conclusao_ia', {}),
                'imagem_processada': filename
            })
            
        finally:
            # Remover arquivo temporário
            if filepath.exists():
                os.unlink(filepath)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao processar imagem: {str(e)}'
        }), 500


# ============================================================================
# ROTAS PARA HEMOGRAMA
# ============================================================================

@api_bp.route('/analisar_hemograma', methods=['POST'])
def analisar_hemograma():
    """
    Endpoint para análise de hemograma completo
    Recebe dados em JSON e retorna laudo completo com áudio
    """
    try:
        dados_json = request.get_json()
        
        # Validar dados
        validacao = hemograma_service.validar_dados(dados_json)
        if not validacao["valido"]:
            return jsonify({
                'success': False,
                'error': 'Dados inválidos',
                'erros': validacao['erros'],
                'avisos': validacao['avisos']
            }), 400
        
        # Analisar hemograma
        resultado = hemograma_service.processar_hemograma(dados_json)
        
        if not resultado.get('sucesso'):
            return jsonify({
                'success': False,
                'error': resultado.get('mensagem', 'Erro ao processar hemograma')
            }), 400
        
        return jsonify({
            'success': True,
            'laudo': resultado['laudo'],
            'audio_url': f'/static/audio/{resultado["audio_filename"]}' if resultado.get('audio_filename') else None,
            'interpretacao': resultado['interpretacao'],
            'alteracoes': resultado['alteracoes'],
            'flags': resultado['flags']
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao processar hemograma: {str(e)}'
        }), 500


@api_bp.route('/hemograma/exemplo/<tipo>')
def obter_exemplo_hemograma(tipo):
    """
    Retorna exemplo de hemograma para testes
    Tipos disponíveis: normal, anemia, leucocitose, plaquetopenia
    """
    try:
        exemplo = hemograma_service.obter_exemplo_hemograma(tipo)
        return jsonify({
            'success': True,
            'exemplo': exemplo
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@api_bp.route('/hemograma/validar', methods=['POST'])
def validar_dados_hemograma():
    """
    Valida dados de hemograma sem processar
    """
    try:
        dados_json = request.get_json()
        validacao = hemograma_service.validar_dados(dados_json)
        
        return jsonify({
            'success': True,
            'validacao': validacao
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
