"""
Serviço de processamento de hemogramas
"""
from typing import Any, Dict

from models.hemograma_analyzer import AnalisadorHemograma
from models.hemograma_data import DadosHemograma
from services.audio_service import AudioService


class HemogramaService:
    """Serviço para processar exames de hemograma completo"""
    
    @staticmethod
    def processar_hemograma(dados_dict: Dict[str, Any], identificador: str = None) -> Dict[str, Any]:
        """Processa dados de hemograma e gera análise completa
        
        Args:
            dados_dict: Dicionário com dados do hemograma
            identificador: Identificador opcional para cache de áudio
            
        Returns:
            Dicionário com análise completa e laudo
        """
        try:
            # Criar objeto de dados
            dados = DadosHemograma.from_dict(dados_dict)
            
            # Analisar hemograma
            analisador = AnalisadorHemograma(dados)
            resultado = analisador.analisar()
            
            # Gerar áudio do laudo (usando versão completa com cache)
            audio_service = AudioService()
            audio_path = audio_service.gerar_audio(
                resultado["laudo_audio"],
                identificador=identificador
            )
            resultado["audio_filename"] = audio_path.split('/')[-1] if audio_path else None
            
            resultado["sucesso"] = True
            return resultado
            
        except Exception as e:
            return {
                "sucesso": False,
                "erro": str(e),
                "mensagem": "Erro ao processar hemograma"
            }
    
    @staticmethod
    def validar_dados(dados_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Valida dados de entrada do hemograma
        
        Args:
            dados_dict: Dicionário com dados a validar
            
        Returns:
            Dicionário com resultado da validação
        """
        erros = []
        avisos = []
        
        # Validar dados do paciente
        paciente = dados_dict.get("paciente", {})
        if not paciente.get("nome"):
            erros.append("Nome do paciente é obrigatório")
        
        if not paciente.get("idade") or paciente.get("idade") <= 0:
            erros.append("Idade do paciente é obrigatória e deve ser maior que 0")
        
        sexo = paciente.get("sexo", "").upper()
        if sexo not in ["M", "F"]:
            erros.append("Sexo do paciente deve ser 'M' ou 'F'")
        
        # Validar série vermelha
        serie_vermelha = dados_dict.get("serie_vermelha", {})
        campos_obrigatorios_sv = ["hemacias", "hemoglobina", "hematocrito"]
        
        for campo in campos_obrigatorios_sv:
            valor = serie_vermelha.get(campo)
            if valor is None or valor <= 0:
                erros.append(f"{campo.capitalize()} é obrigatório e deve ser maior que 0")
        
        # Validar série branca
        serie_branca = dados_dict.get("serie_branca", {})
        if not serie_branca.get("leucocitos") or serie_branca.get("leucocitos") <= 0:
            erros.append("Leucócitos é obrigatório e deve ser maior que 0")
        
        # Validar plaquetas
        plaquetas = dados_dict.get("plaquetas", {})
        if not plaquetas.get("contagem") or plaquetas.get("contagem") <= 0:
            erros.append("Contagem de plaquetas é obrigatória e deve ser maior que 0")
        
        # Avisos para parâmetros opcionais mas recomendados
        if not serie_vermelha.get("vcm"):
            avisos.append("VCM não informado - recomendado para análise completa")
        
        if not serie_branca.get("neutrofilos"):
            avisos.append("Contagem de neutrófilos não informada")
        
        return {
            "valido": len(erros) == 0,
            "erros": erros,
            "avisos": avisos
        }
    
    @staticmethod
    def obter_exemplo_hemograma(tipo: str = "normal") -> Dict[str, Any]:
        """Retorna exemplo de hemograma para testes
        
        Args:
            tipo: Tipo de exemplo ('normal', 'anemia', 'leucocitose', etc)
            
        Returns:
            Dicionário com dados de exemplo
        """
        exemplos = {
            "normal": {
                "paciente": {
                    "nome": "Juan Silva",
                    "idade": 35,
                    "sexo": "M",
                    "data_coleta": "12/11/2025"
                },
                "serie_vermelha": {
                    "hemacias": 5.0,
                    "hemoglobina": 15.0,
                    "hematocrito": 45.0,
                    "vcm": 90.0,
                    "hcm": 30.0,
                    "chcm": 34.0,
                    "rdw": 13.0
                },
                "serie_branca": {
                    "leucocitos": 7000,
                    "neutrofilos": 4000,
                    "segmentados": 3800,
                    "bastonetes": 200,
                    "linfocitos": 2000,
                    "monocitos": 500,
                    "eosinofilos": 200,
                    "basofilos": 50
                },
                "plaquetas": {
                    "contagem": 250000
                },
                "observacoes": "Hemograma dentro dos padrões de normalidade."
            },
            "anemia": {
                "paciente": {
                    "nome": "María Santos",
                    "idade": 42,
                    "sexo": "F",
                    "data_coleta": "12/11/2025"
                },
                "serie_vermelha": {
                    "hemacias": 3.5,
                    "hemoglobina": 10.0,
                    "hematocrito": 32.0,
                    "vcm": 75.0,
                    "hcm": 25.0,
                    "chcm": 32.0,
                    "rdw": 16.5
                },
                "serie_branca": {
                    "leucocitos": 6500,
                    "neutrofilos": 3500,
                    "linfocitos": 2200,
                    "monocitos": 450,
                    "eosinofilos": 180,
                    "basofilos": 40
                },
                "plaquetas": {
                    "contagem": 280000
                },
                "observacoes": "Paciente refere fadiga e palidez."
            },
            "leucocitose": {
                "paciente": {
                    "nome": "Pedro Oliveira",
                    "idade": 28,
                    "sexo": "M",
                    "data_coleta": "12/11/2025"
                },
                "serie_vermelha": {
                    "hemacias": 4.8,
                    "hemoglobina": 14.5,
                    "hematocrito": 43.0,
                    "vcm": 88.0,
                    "hcm": 29.0,
                    "chcm": 33.5,
                    "rdw": 12.8
                },
                "serie_branca": {
                    "leucocitos": 15000,
                    "neutrofilos": 11000,
                    "segmentados": 10000,
                    "bastonetes": 1000,
                    "linfocitos": 2500,
                    "monocitos": 800,
                    "eosinofilos": 300,
                    "basofilos": 60
                },
                "plaquetas": {
                    "contagem": 320000
                },
                "observacoes": "Paciente com quadro febril há 2 dias."
            },
            "plaquetopenia": {
                "paciente": {
                    "nome": "Ana Costa",
                    "idade": 55,
                    "sexo": "F",
                    "data_coleta": "12/11/2025"
                },
                "serie_vermelha": {
                    "hemacias": 4.2,
                    "hemoglobina": 13.0,
                    "hematocrito": 39.0,
                    "vcm": 92.0,
                    "hcm": 31.0,
                    "chcm": 34.0,
                    "rdw": 13.2
                },
                "serie_branca": {
                    "leucocitos": 6800,
                    "neutrofilos": 3800,
                    "linfocitos": 2100,
                    "monocitos": 520,
                    "eosinofilos": 210,
                    "basofilos": 45
                },
                "plaquetas": {
                    "contagem": 95000
                },
                "observacoes": "Paciente relata aparecimento de petéquias."
            }
        }
        
        return exemplos.get(tipo, exemplos["normal"])
