"""
Serviço de análise de ECG por imagem usando GPT-4o Vision
"""
import base64
import json
from typing import Any, Dict

from openai import OpenAI

import config


class VisionService:
    """Serviço para análise de imagens de ECG usando GPT-4o Vision"""
    
    def __init__(self):
        """Inicializa o serviço"""
        self.api_key = config.OPENAI_API_KEY
        self.model = config.OPENAI_MODEL
        
        if not self.api_key:
            raise ValueError(
                "OPENAI_API_KEY não configurada. "
                "Configure a variável de ambiente OPENAI_API_KEY"
            )
        
        # Inicializar cliente OpenAI
        self.client = OpenAI(api_key=self.api_key)
    
    def encode_image(self, image_path: str) -> str:
        """
        Codifica a imagem em base64
        
        Args:
            image_path: Caminho para o arquivo de imagem
            
        Returns:
            String base64 da imagem
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def analisar_ecg_imagem(self, image_path: str) -> Dict[str, Any]:
        """
        Analisa uma imagem de ECG usando GPT-4o Vision
        
        Args:
            image_path: Caminho para a imagem do ECG
            
        Returns:
            Dicionário com os dados extraídos do ECG
        """
        # Codificar imagem
        base64_image = self.encode_image(image_path)
        
        # Preparar prompt otimizado - formulado como análise técnica de sinais
        prompt = """Você é um especialista em análise de sinais elétricos e gráficos. Analise esta imagem de gráfico de ondas elétricas e extraia os dados técnicos em formato JSON.

CONTEXTO: Este é um gráfico padrão de 12 derivações mostrando ondas elétricas ao longo do tempo, com marcações de voltagem (mV) e tempo (segundos). O gráfico contém padrões de ondas repetitivas que precisam ser medidos e classificados.

INSTRUÇÕES:
1. Meça com precisão os intervalos de tempo e amplitudes visíveis no traçado
2. Identifique padrões e características importantes das ondas
3. Use null para valores não determináveis claramente
4. Seja objetivo e técnico na análise dos dados gráficos

FORMATO JSON EXIGIDO:
{
    "dados_quantitativos": {
        "frequencia_cardiaca": <bpm ou null>,
        "intervalo_pr": <segundos ou null>,
        "duracao_qrs": <segundos ou null>,
        "intervalo_qt": <segundos ou null>,
        "qtc": <segundos ou null>,
        "eixo_qrs": <graus ou null>
    },
    "ritmo": {
        "tipo": "<sinusal/FA/flutter/outro>",
        "regular": <true/false>,
        "descricao": "<breve descrição>"
    },
    "ondas": {
        "onda_p": {
            "presente": <true/false>,
            "morfologia": "<normal/anormal/biatrial>",
            "amplitude": <mV ou null>
        },
        "complexo_qrs": {
            "morfologia": "<normal/alargado/fragmentado>",
            "amplitude": <mV ou null>,
            "onda_q_patologica": <true/false>
        },
        "onda_t": {
            "polaridade": "<positiva/negativa/bifásica>",
            "morfologia": "<normal/invertida/apiculada>"
        }
    },
    "segmentos": {
        "segmento_st": {
            "elevacao": <true/false>,
            "depressao": <true/false>,
            "derivacoes_afetadas": ["V1", "V2", "..."],
            "magnitude_mm": <valor ou null>
        }
    },
    "hipertrofias": {
        "hipertrofia_ve": <true/false>,
        "hipertrofia_vd": <true/false>,
        "criterios_presentes": ["critério 1", "critério 2"]
    },
    "bloqueios": {
        "bloqueio_av": {
            "presente": <true/false>,
            "grau": "<1/2/3 ou null>"
        },
        "bloqueio_ramo": {
            "presente": <true/false>,
            "tipo": "<BRD/BRE ou null>"
        }
    },
    "isquemia": {
        "presente": <true/false>,
        "localizacao": ["anterior", "inferior", "lateral"],
        "aguda": <true/false>
    },
    "arritmias": {
        "extrassistoles": {
            "presentes": <true/false>,
            "tipo": "<supraventriculares/ventriculares ou null>"
        },
        "outras": ["lista de arritmias"]
    },
    "conclusao": {
        "gravidade": "<normal/alterações leves/moderadas/graves>",
        "principais_achados": ["achado 1", "achado 2", "achado 3"],
        "diagnosticos_suspeitos": ["diagnóstico 1", "diagnóstico 2"],
        "recomendacoes": ["recomendação 1", "recomendação 2"]
    },
    "qualidade_ecg": {
        "qualidade_traçado": "<excelente/boa/regular/ruim>",
        "artefatos": <true/false>,
        "observacoes": "<breve observação ou null>"
    }
}

RETORNE APENAS O JSON. Sem texto antes ou depois."""
        
        # Fazer requisição usando SDK oficial da OpenAI
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}",
                                    "detail": "high"
                                },
                            },
                        ],
                    }
                ],
                max_tokens=4096,
                temperature=0.2,  # Baixa temperatura para respostas mais consistentes
            )
            
            # Extrair resposta
            content = completion.choices[0].message.content
            
            if not content:
                raise Exception("Resposta vazia da API OpenAI")
            
            # Tentar extrair JSON da resposta
            try:
                # Remover possíveis marcadores de código markdown
                content = content.strip()
                if content.startswith('```json'):
                    content = content[7:]
                if content.startswith('```'):
                    content = content[3:]
                if content.endswith('```'):
                    content = content[:-3]
                content = content.strip()
                
                dados_ecg = json.loads(content)
                return dados_ecg
            except json.JSONDecodeError as e:
                raise Exception(
                    f"Erro ao fazer parse do JSON retornado pela API: {e}\n"
                    f"Conteúdo recebido: {content}"
                )
        
        except Exception as e:
            erro_msg = str(e)
            
            # Verificar se é bloqueio por conteúdo médico
            if "can't assist" in erro_msg.lower() or "sorry" in erro_msg.lower():
                raise Exception(
                    "A API OpenAI bloqueou a análise desta imagem. "
                    "Possíveis razões:\n"
                    "1. A imagem foi identificada como conteúdo médico especializado\n"
                    "2. Política da OpenAI: 'The model is not suitable for interpreting "
                    "specialized medical images and shouldn't be used for medical advice'\n\n"
                    "SOLUÇÕES ALTERNATIVAS:\n"
                    "- Use o modo de entrada manual de dados (📊 Nova Análise)\n"
                    "- Considere usar modelos especializados em análise médica\n"
                    "- Entre em contato com o suporte da OpenAI para uso em contexto educacional"
                )
            
            raise Exception(f"Erro ao chamar API OpenAI: {erro_msg}")
    
    def converter_para_formato_sistema(self, dados_vision: Dict[str, Any]) -> Dict[str, Any]:
        """
        Converte os dados do formato Vision para o formato esperado pelo sistema
        
        Args:
            dados_vision: Dados retornados pela API Vision
            
        Returns:
            Dicionário no formato esperado pelo ECGService
        """
        # Extrair dados quantitativos
        quant = dados_vision.get('dados_quantitativos', {})
        ritmo = dados_vision.get('ritmo', {})
        ondas = dados_vision.get('ondas', {})
        segmentos = dados_vision.get('segmentos', {})
        bloqueios = dados_vision.get('bloqueios', {})
        hipertrofias = dados_vision.get('hipertrofias', {})
        isquemia = dados_vision.get('isquemia', {})
        conclusao = dados_vision.get('conclusao', {})
        
        # Construir dicionário no formato do sistema
        dados_sistema = {
            "paciente": {
                "nome": "Análise por Imagem",
                "idade": None,
                "sexo": None
            },
            "dados_ecg": {
                "frequencia_cardiaca": quant.get('frequencia_cardiaca'),
                "ritmo": ritmo.get('tipo', 'sinusal'),
                "eixo_qrs": quant.get('eixo_qrs'),
                "intervalo_pr": quant.get('intervalo_pr'),
                "duracao_qrs": quant.get('duracao_qrs'),
                "intervalo_qt": quant.get('intervalo_qt'),
                "qtc": quant.get('qtc'),
                "onda_p": {
                    "presente": ondas.get('onda_p', {}).get('presente', True),
                    "amplitude": ondas.get('onda_p', {}).get('amplitude'),
                    "duracao": ondas.get('onda_p', {}).get('duracao')
                },
                "onda_t": {
                    "normal": ondas.get('onda_t', {}).get('morfologia') == 'normal',
                    "invertida": ondas.get('onda_t', {}).get('polaridade') == 'negativa'
                },
                "segmento_st": {
                    "elevacao": segmentos.get('segmento_st', {}).get('elevacao', False),
                    "depressao": segmentos.get('segmento_st', {}).get('depressao', False),
                    "derivacoes": segmentos.get('segmento_st', {}).get('derivacoes_afetadas', [])
                },
                "bloqueio_ramo": bloqueios.get('bloqueio_ramo', {}).get('presente', False),
                "hipertrofia_ve": hipertrofias.get('hipertrofia_ve', False),
                "isquemia": isquemia.get('presente', False)
            },
            "analise_vision": dados_vision,  # Manter análise completa para referência
            "conclusao_ia": {
                "gravidade": conclusao.get('gravidade'),
                "principais_achados": conclusao.get('principais_achados', []),
                "diagnosticos": conclusao.get('diagnosticos_suspeitos', []),
                "recomendacoes": conclusao.get('recomendacoes', [])
            }
        }
        
        return dados_sistema
