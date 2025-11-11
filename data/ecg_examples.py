"""
Dados de exemplo para ECG
"""
from models.ecg_data import (
    ComplexoQRS,
    DadosECG,
    IntervalosECG,
    OndaP,
    OndaT,
    SegmentoST,
)


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


def obter_todos_exemplos() -> dict:
    """Retorna dicionário com todos os exemplos"""
    return {
        'normal': criar_exemplo_normal(),
        'arritmia_sinusal': criar_exemplo_arritmia(),
        'bloqueio_ramo': criar_exemplo_bloqueio()
    }
