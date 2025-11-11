"""
Serviço de análise de ECG
"""
from typing import Any, Dict

from models.ecg_data import (
    ComplexoQRS,
    DadosECG,
    IntervalosECG,
    OndaP,
    OndaT,
    SegmentoST,
)
from models.laudo_generator import GeradorLaudo


class ECGService:
    """Serviço para análise de ECG"""
    
    def __init__(self):
        self.gerador_laudo = GeradorLaudo()
    
    def analisar_ecg(self, dados_json: dict) -> Dict[str, Any]:
        """
        Analisa dados de ECG e gera laudo
        
        Args:
            dados_json: Dicionário com dados do ECG
            
        Returns:
            Dicionário com laudo completo
        """
        dados_ecg = self._construir_dados_ecg(dados_json)
        laudo = self.gerador_laudo.gerar_laudo_completo(dados_ecg)
        
        return {
            'laudo_texto': laudo['texto_completo'],
            'laudo_audio_texto': laudo['texto_audio'],
            'achados': laudo['achados'],
            'diagnosticos': laudo['diagnosticos']
        }
    
    def _construir_dados_ecg(self, dados_json: dict) -> DadosECG:
        """
        Constrói objeto DadosECG a partir de dicionário JSON
        
        Args:
            dados_json: Dicionário com dados do ECG
            
        Returns:
            Objeto DadosECG
        """
        # Construir intervalos
        intervalos_data = dados_json.get('intervalos', {})
        intervalos = IntervalosECG(
            pr=float(intervalos_data.get('pr', 0)),
            qrs=float(intervalos_data.get('qrs', 0)),
            qt=float(intervalos_data.get('qt', 0)),
            qtc=float(intervalos_data.get('qtc', 0))
        )
        
        # Construir onda P
        onda_p_data = dados_json.get('onda_p', {})
        onda_p = OndaP(
            presente=onda_p_data.get('presente', True),
            positiva_dII=onda_p_data.get('positiva_dII', True),
            positiva_dIII=onda_p_data.get('positiva_dIII', True),
            positiva_aVF=onda_p_data.get('positiva_aVF', True),
            morfologia=onda_p_data.get('morfologia', 'normal')
        )
        
        # Construir complexo QRS
        qrs_data = dados_json.get('complexo_qrs', {})
        complexo_qrs = ComplexoQRS(
            morfologia=qrs_data.get('morfologia', 'normal'),
            progressao_r=qrs_data.get('progressao_r', 'preservada'),
            zona_transicao=qrs_data.get('zona_transicao', 'V3-V4'),
            ondas_q_patologicas=qrs_data.get('ondas_q_patologicas', False),
            amplitude_v1_v3=qrs_data.get('amplitude_v1_v3', 'normal'),
            amplitude_v4_v6=qrs_data.get('amplitude_v4_v6', 'normal')
        )
        
        # Construir segmento ST
        st_data = dados_json.get('segmento_st', {})
        segmento_st = SegmentoST(
            supradesnivelamento=st_data.get('supradesnivelamento', []),
            infradesnivelamento=st_data.get('infradesnivelamento', []),
            normal=st_data.get('normal', [])
        )
        
        # Construir onda T
        onda_t_data = dados_json.get('onda_t', {})
        onda_t = OndaT(
            invertida=onda_t_data.get('invertida', []),
            apiculada=onda_t_data.get('apiculada', []),
            normal=onda_t_data.get('normal', [])
        )
        
        # Construir dados completos
        return DadosECG(
            # Identificação
            paciente_id=dados_json.get('paciente_id'),
            nome_paciente=dados_json.get('nome_paciente', ''),
            data_exame=dados_json.get('data_exame'),
            # Ritmo e frequência
            ritmo=dados_json.get('ritmo', 'sinusal'),
            frequencia_cardiaca=int(dados_json.get('frequencia_cardiaca', 0)),
            regularidade=dados_json.get('regularidade', 'regular'),
            # Eixo elétrico
            eixo_qrs=int(dados_json.get('eixo_qrs', 0)),
            # Intervalos e ondas
            intervalos=intervalos,
            onda_p=onda_p,
            complexo_qrs=complexo_qrs,
            segmento_st=segmento_st,
            onda_t=onda_t,
            # Bloqueios e alterações
            bloqueio_ramo=dados_json.get('bloqueio_ramo'),
            bloqueio_av=dados_json.get('bloqueio_av'),
            sobrecarga_atrial=dados_json.get('sobrecarga_atrial'),
            sobrecarga_ventricular=dados_json.get('sobrecarga_ventricular'),
            # Achados especiais
            isquemia=dados_json.get('isquemia', False),
            infarto=dados_json.get('infarto', False),
            localizacao_isquemia=dados_json.get('localizacao_isquemia', [])
        )
