"""
Aplicação Flask para o Sistema de Laudos de ECG com Acessibilidade
"""
import json
from datetime import datetime

from audio_generator import AudioLaudoGenerator
from flask import Flask, jsonify, render_template, request, send_from_directory
from models.ecg_data import (
    ComplexoQRS,
    DadosECG,
    IntervalosECG,
    OndaP,
    OndaT,
    SegmentoST,
)
from models.laudo_generator import GeradorLaudo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'

# Instanciar geradores
gerador_laudo = GeradorLaudo()
gerador_audio = AudioLaudoGenerator()


@app.route('/')
def index():
    """Página inicial"""
    return render_template('index.html')


@app.route('/analise')
def analise():
    """Página de análise de ECG"""
    return render_template('analise.html')


@app.route('/resultados')
def resultados():
    """Página com fila de resultados de pacientes"""
    return render_template('resultados.html')


@app.route('/teste-acessibilidade')
def teste_acessibilidade():
    """Página de teste para verificar feedback auditivo"""
    return render_template('teste_acessibilidade.html')


@app.route('/api/anunciar', methods=['POST'])
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
        
        # Gerar áudio usando o mesmo sistema dos laudos
        audio_path = gerador_audio.gerar_audio_laudo(texto)
        
        return jsonify({
            'success': True,
            'audio_url': f'/static/{audio_path}'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/analisar', methods=['POST'])
def analisar_ecg():
    """
    Endpoint para análise de ECG
    Recebe dados em JSON e retorna laudo completo
    """
    try:
        dados_json = request.get_json()
        
        # Construir objeto DadosECG a partir do JSON
        dados_ecg = construir_dados_ecg(dados_json)
        
        # Gerar laudo
        laudo = gerador_laudo.gerar_laudo_completo(dados_ecg)
        
        # Gerar áudio do laudo
        audio_path = gerador_audio.gerar_audio_laudo(laudo['texto_audio'])
        
        # Limpar áudios antigos (manter últimos 50)
        gerador_audio.limpar_audios_antigos(50)
        
        return jsonify({
            'success': True,
            'laudo_texto': laudo['texto_completo'],
            'laudo_audio_texto': laudo['texto_audio'],
            'audio_url': f'/static/{audio_path}',
            'achados': laudo['achados'],
            'diagnosticos': laudo['diagnosticos']
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/resultados')
def obter_resultados():
    """
    Retorna resultados de ECG da fila de pacientes
    """
    resultados = {
        'normal': criar_exemplo_normal(),
        'arritmia_sinusal': criar_exemplo_arritmia(),
        'bloqueio_ramo': criar_exemplo_bloqueio()
    }
    
    return jsonify(resultados)


@app.route('/api/resultado/<tipo>', methods=['POST'])
def processar_resultado(tipo):
    """
    Processa um resultado específico e retorna o laudo
    """
    resultados = {
        'normal': criar_exemplo_normal(),
        'arritmia_sinusal': criar_exemplo_arritmia(),
        'bloqueio_ramo': criar_exemplo_bloqueio()
    }
    
    if tipo not in resultados:
        return jsonify({'success': False, 'error': 'Resultado não encontrado'}), 404
    
    dados_ecg = resultados[tipo]
    
    # Gerar laudo
    laudo = gerador_laudo.gerar_laudo_completo(dados_ecg)
    
    # Gerar áudio
    audio_path = gerador_audio.gerar_audio_laudo(laudo['texto_audio'])
    
    return jsonify({
        'success': True,
        'laudo_texto': laudo['texto_completo'],
        'laudo_audio_texto': laudo['texto_audio'],
        'audio_url': f'/static/{audio_path}',
        'achados': laudo['achados'],
        'diagnosticos': laudo['diagnosticos']
    })


def construir_dados_ecg(dados_json: dict) -> DadosECG:
    """Constrói objeto DadosECG a partir de JSON"""
    
    # Intervalos
    intervalos = None
    if 'intervalos' in dados_json:
        i = dados_json['intervalos']
        intervalos = IntervalosECG(
            pr=float(i.get('pr', 0.16)),
            qrs=float(i.get('qrs', 0.08)),
            qt=float(i.get('qt', 0.40)),
            qtc=float(i.get('qtc', 0.42))
        )
    
    # Onda P
    onda_p = None
    if 'onda_p' in dados_json:
        p = dados_json['onda_p']
        onda_p = OndaP(
            presente=p.get('presente', True),
            positiva_dII=p.get('positiva_dII', True),
            positiva_dIII=p.get('positiva_dIII', True),
            positiva_aVF=p.get('positiva_aVF', True),
            morfologia=p.get('morfologia', 'normal')
        )
    
    # Complexo QRS
    complexo_qrs = None
    if 'complexo_qrs' in dados_json:
        q = dados_json['complexo_qrs']
        complexo_qrs = ComplexoQRS(
            morfologia=q.get('morfologia', 'normal'),
            progressao_r=q.get('progressao_r', 'preservada'),
            zona_transicao=q.get('zona_transicao', 'V3-V4'),
            ondas_q_patologicas=q.get('ondas_q_patologicas', False),
            amplitude_v1_v3=q.get('amplitude_v1_v3', 'normal'),
            amplitude_v4_v6=q.get('amplitude_v4_v6', 'normal')
        )
    
    # Segmento ST
    segmento_st = None
    if 'segmento_st' in dados_json:
        st = dados_json['segmento_st']
        segmento_st = SegmentoST(
            supradesnivelamento=st.get('supradesnivelamento', []),
            infradesnivelamento=st.get('infradesnivelamento', []),
            normal=st.get('normal', [])
        )
    
    # Onda T
    onda_t = None
    if 'onda_t' in dados_json:
        t = dados_json['onda_t']
        onda_t = OndaT(
            invertida=t.get('invertida', []),
            apiculada=t.get('apiculada', []),
            normal=t.get('normal', [])
        )
    
    # Criar DadosECG
    dados_ecg = DadosECG(
        paciente_id=dados_json.get('paciente_id'),
        nome_paciente=dados_json.get('nome_paciente'),
        data_exame=dados_json.get('data_exame', datetime.now().strftime('%d/%m/%Y %H:%M')),
        ritmo=dados_json.get('ritmo', 'sinusal'),
        frequencia_cardiaca=int(dados_json.get('frequencia_cardiaca', 70)),
        regularidade=dados_json.get('regularidade', 'regular'),
        eixo_qrs=int(dados_json.get('eixo_qrs', 60)),
        intervalos=intervalos,
        onda_p=onda_p,
        complexo_qrs=complexo_qrs,
        segmento_st=segmento_st,
        onda_t=onda_t,
        bloqueio_ramo=dados_json.get('bloqueio_ramo'),
        bloqueio_av=dados_json.get('bloqueio_av'),
        sobrecarga_atrial=dados_json.get('sobrecarga_atrial'),
        sobrecarga_ventricular=dados_json.get('sobrecarga_ventricular'),
        isquemia=dados_json.get('isquemia', False),
        infarto=dados_json.get('infarto', False),
        localizacao_isquemia=dados_json.get('localizacao_isquemia', [])
    )
    
    return dados_ecg


def criar_exemplo_normal() -> DadosECG:
    """Cria exemplo de ECG normal"""
    return DadosECG(
        nome_paciente="Exemplo - Paciente Normal",
        ritmo="sinusal",
        frequencia_cardiaca=72,
        regularidade="regular",
        eixo_qrs=50,
        intervalos=IntervalosECG(pr=0.16, qrs=0.08, qt=0.38, qtc=0.40),
        onda_p=OndaP(
            presente=True,
            positiva_dII=True,
            positiva_dIII=True,
            positiva_aVF=True,
            morfologia="normal"
        ),
        complexo_qrs=ComplexoQRS(
            morfologia="normal",
            progressao_r="preservada",
            zona_transicao="V3-V4",
            ondas_q_patologicas=False,
            amplitude_v1_v3="normal",
            amplitude_v4_v6="normal"
        ),
        segmento_st=SegmentoST(
            supradesnivelamento=[],
            infradesnivelamento=[],
            normal=["DI", "DII", "DIII", "aVR", "aVL", "aVF", "V1-V6"]
        ),
        onda_t=OndaT(
            invertida=[],
            apiculada=[],
            normal=["DI", "DII", "DIII", "aVL", "aVF", "V1-V6"]
        )
    )


def criar_exemplo_arritmia() -> DadosECG:
    """Cria exemplo de arritmia sinusal"""
    return DadosECG(
        nome_paciente="Exemplo - Arritmia Sinusal",
        ritmo="sinusal",
        frequencia_cardiaca=72,
        regularidade="irregular",
        eixo_qrs=-18,
        intervalos=IntervalosECG(pr=0.16, qrs=0.08, qt=0.40, qtc=0.42),
        onda_p=OndaP(
            presente=True,
            positiva_dII=True,
            positiva_dIII=True,
            positiva_aVF=True,
            morfologia="aumentada_esquerda"
        ),
        complexo_qrs=ComplexoQRS(
            morfologia="normal",
            progressao_r="preservada",
            zona_transicao="V3-V4",
            ondas_q_patologicas=False,
            amplitude_v1_v3="normal",
            amplitude_v4_v6="normal"
        ),
        segmento_st=SegmentoST(
            supradesnivelamento=[],
            infradesnivelamento=[],
            normal=["DI", "DII", "DIII", "aVR", "aVL", "aVF", "V1-V6"]
        ),
        onda_t=OndaT(
            invertida=[],
            apiculada=[],
            normal=["DI", "DII", "DIII", "aVL", "aVF", "V1-V6"]
        )
    )


def criar_exemplo_bloqueio() -> DadosECG:
    """Cria exemplo de bloqueio incompleto de ramo direito"""
    return DadosECG(
        nome_paciente="Exemplo - Bloqueio Incompleto Ramo Direito",
        ritmo="sinusal",
        frequencia_cardiaca=85,
        regularidade="regular",
        eixo_qrs=-18,
        intervalos=IntervalosECG(pr=0.16, qrs=0.09, qt=0.40, qtc=0.42),
        onda_p=OndaP(
            presente=True,
            positiva_dII=True,
            positiva_dIII=True,
            positiva_aVF=True,
            morfologia="normal"
        ),
        complexo_qrs=ComplexoQRS(
            morfologia="RSR'",
            progressao_r="preservada",
            zona_transicao="V3-V4",
            ondas_q_patologicas=False,
            amplitude_v1_v3="aumentada",
            amplitude_v4_v6="normal"
        ),
        segmento_st=SegmentoST(
            supradesnivelamento=[],
            infradesnivelamento=["V2", "V3"],
            normal=["DI", "DII", "DIII", "aVR", "aVL", "aVF", "V4-V6"]
        ),
        onda_t=OndaT(
            invertida=["V1", "V2", "V3"],
            apiculada=[],
            normal=["DI", "DII", "DIII", "aVL", "aVF", "V4-V6"]
        ),
        bloqueio_ramo="incompleto_direito"
    )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
