"""
Módulo de estruturas de dados para ECG
"""
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class IntervalosECG:
    """Classe para armazenar intervalos do ECG"""
    pr: float  # em segundos
    qrs: float  # em segundos
    qt: float  # em segundos
    qtc: float  # QT corrigido


@dataclass
class OndaP:
    """Características da onda P"""
    presente: bool
    positiva_dII: bool
    positiva_dIII: bool
    positiva_aVF: bool
    morfologia: str  # "normal", "aumentada_esquerda", "aumentada_direita"


@dataclass
class ComplexoQRS:
    """Características do complexo QRS"""
    morfologia: str  # "normal", "RSR'", "QS", etc
    progressao_r: str  # "preservada", "reduzida", "ausente"
    zona_transicao: str  # "V3-V4", "V2-V3", etc
    ondas_q_patologicas: bool
    amplitude_v1_v3: str  # "normal", "aumentada", "reduzida"
    amplitude_v4_v6: str  # "normal", "aumentada", "reduzida"


@dataclass
class SegmentoST:
    """Características do segmento ST"""
    supradesnivelamento: List[str]  # derivações com supra
    infradesnivelamento: List[str]  # derivações com infra
    normal: List[str]  # derivações normais


@dataclass
class OndaT:
    """Características da onda T"""
    invertida: List[str]  # derivações com inversão
    apiculada: List[str]  # derivações com T apiculada
    normal: List[str]  # derivações normais


@dataclass
class DadosECG:
    """Estrutura completa dos dados do ECG"""
    # Identificação do paciente
    paciente_id: Optional[str] = None
    nome_paciente: Optional[str] = None
    genero: Optional[str] = None  # "Masculino", "Femenino"
    idade: Optional[int] = None  # idade em anos
    data_exame: Optional[str] = None
    
    # Ritmo e frequência
    ritmo: str = "sinusal"  # "sinusal", "fibrilacao_atrial", "flutter", etc
    frequencia_cardiaca: int = 70  # bpm
    regularidade: str = "regular"  # "regular", "irregular"
    
    # Eixo elétrico
    eixo_qrs: int = 60  # em graus (-30 a +90 = normal)
    
    # Intervalos
    intervalos: Optional[IntervalosECG] = None
    
    # Ondas e complexos
    onda_p: Optional[OndaP] = None
    complexo_qrs: Optional[ComplexoQRS] = None
    segmento_st: Optional[SegmentoST] = None
    onda_t: Optional[OndaT] = None
    
    # Bloqueios e alterações
    bloqueio_ramo: Optional[str] = None  # "incompleto_direito", "completo_direito", etc
    bloqueio_av: Optional[str] = None  # "primeiro_grau", "segundo_grau", etc
    sobrecarga_atrial: Optional[str] = None  # "esquerda", "direita", "biatrial"
    sobrecarga_ventricular: Optional[str] = None  # "esquerda", "direita", "biventricular"
    
    # Achados especiais
    isquemia: bool = False
    infarto: bool = False
    localizacao_isquemia: Optional[List[str]] = None
    
    def __post_init__(self):
        if self.localizacao_isquemia is None:
            self.localizacao_isquemia = []
    
    def to_dict(self):
        """
        Converte DadosECG para dicionário, útil para API
        """
        result = {
            'nome_paciente': self.nome_paciente,
            'ritmo': self.ritmo,
            'frequencia_cardiaca': self.frequencia_cardiaca,
            'regularidade': self.regularidade,
            'eixo_qrs': self.eixo_qrs,
            'bloqueio_ramo': self.bloqueio_ramo
        }
        
        # Adicionar campos opcionais se existirem
        if self.paciente_id:
            result['paciente_id'] = self.paciente_id
        if self.genero:
            result['genero'] = self.genero
        if self.idade:
            result['idade'] = self.idade
        if self.data_exame:
            result['data_exame'] = self.data_exame
        if self.bloqueio_av:
            result['bloqueio_av'] = self.bloqueio_av
        if self.sobrecarga_atrial:
            result['sobrecarga_atrial'] = self.sobrecarga_atrial
        if self.sobrecarga_ventricular:
            result['sobrecarga_ventricular'] = self.sobrecarga_ventricular
        if self.isquemia:
            result['isquemia'] = self.isquemia
        if self.infarto:
            result['infarto'] = self.infarto
        if self.localizacao_isquemia:
            result['localizacao_isquemia'] = self.localizacao_isquemia
        
        # Converter objetos aninhados
        if self.intervalos:
            result['intervalos'] = {
                'pr': self.intervalos.pr,
                'qrs': self.intervalos.qrs,
                'qt': self.intervalos.qt,
                'qtc': self.intervalos.qtc
            }
        
        if self.onda_p:
            result['onda_p'] = {
                'presente': self.onda_p.presente,
                'positiva_dII': self.onda_p.positiva_dII,
                'positiva_dIII': self.onda_p.positiva_dIII,
                'positiva_aVF': self.onda_p.positiva_aVF,
                'morfologia': self.onda_p.morfologia
            }
        
        if self.complexo_qrs:
            result['complexo_qrs'] = {
                'morfologia': self.complexo_qrs.morfologia,
                'progressao_r': self.complexo_qrs.progressao_r,
                'zona_transicao': self.complexo_qrs.zona_transicao,
                'ondas_q_patologicas': self.complexo_qrs.ondas_q_patologicas,
                'amplitude_v1_v3': self.complexo_qrs.amplitude_v1_v3,
                'amplitude_v4_v6': self.complexo_qrs.amplitude_v4_v6
            }
        
        if self.segmento_st:
            result['segmento_st'] = {
                'supradesnivelamento': self.segmento_st.supradesnivelamento,
                'infradesnivelamento': self.segmento_st.infradesnivelamento,
                'normal': self.segmento_st.normal
            }
        
        if self.onda_t:
            result['onda_t'] = {
                'invertida': self.onda_t.invertida,
                'apiculada': self.onda_t.apiculada,
                'normal': self.onda_t.normal
            }
        
        return result
