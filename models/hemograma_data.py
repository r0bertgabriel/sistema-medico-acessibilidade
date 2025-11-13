"""
Estrutura de dados para hemograma completo
"""
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class DadosHemograma:
    """Estrutura para armazenar dados de hemograma completo
    
    Baseado em padrões laboratoriais brasileiros e internacionais
    """
    
    # Dados do paciente
    nome_paciente: str = ""
    idade: int = 0
    sexo: str = "M"  # M ou F
    data_coleta: str = ""
    
    # === SÉRIE VERMELHA (ERITROGRAMA) ===
    hemacias: Optional[float] = None  # milhões/µL ou x10^6/µL
    hemoglobina: Optional[float] = None  # g/dL
    hematocrito: Optional[float] = None  # %
    vcm: Optional[float] = None  # fL (femtolitros)
    hcm: Optional[float] = None  # pg (picogramas)
    chcm: Optional[float] = None  # g/dL
    rdw: Optional[float] = None  # % (variação do tamanho das hemácias)
    
    # === SÉRIE BRANCA (LEUCOGRAMA) ===
    leucocitos: Optional[float] = None  # células/µL ou /mm³
    neutrofilos: Optional[float] = None  # células/µL
    bastonetes: Optional[float] = None  # células/µL (neutrófilos jovens)
    segmentados: Optional[float] = None  # células/µL (neutrófilos maduros)
    linfocitos: Optional[float] = None  # células/µL
    monocitos: Optional[float] = None  # células/µL
    eosinofilos: Optional[float] = None  # células/µL
    basofilos: Optional[float] = None  # células/µL
    
    # === PLAQUETAS ===
    plaquetas: Optional[float] = None  # células/µL ou /mm³
    
    # Observações adicionais
    observacoes: str = ""
    
    # Campos calculados/derivados
    neutrofilos_percentual: Optional[float] = None  # %
    linfocitos_percentual: Optional[float] = None  # %
    monocitos_percentual: Optional[float] = None  # %
    eosinofilos_percentual: Optional[float] = None  # %
    basofilos_percentual: Optional[float] = None  # %
    
    def to_dict(self) -> Dict:
        """Converte os dados para dicionário"""
        return {
            "paciente": {
                "nome": self.nome_paciente,
                "idade": self.idade,
                "sexo": self.sexo,
                "data_coleta": self.data_coleta
            },
            "serie_vermelha": {
                "hemacias": self.hemacias,
                "hemoglobina": self.hemoglobina,
                "hematocrito": self.hematocrito,
                "vcm": self.vcm,
                "hcm": self.hcm,
                "chcm": self.chcm,
                "rdw": self.rdw
            },
            "serie_branca": {
                "leucocitos": self.leucocitos,
                "neutrofilos": self.neutrofilos,
                "bastonetes": self.bastonetes,
                "segmentados": self.segmentados,
                "linfocitos": self.linfocitos,
                "monocitos": self.monocitos,
                "eosinofilos": self.eosinofilos,
                "basofilos": self.basofilos
            },
            "plaquetas": {
                "contagem": self.plaquetas
            },
            "observacoes": self.observacoes
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'DadosHemograma':
        """Cria instância a partir de dicionário"""
        paciente = data.get("paciente", {})
        serie_vermelha = data.get("serie_vermelha", {})
        serie_branca = data.get("serie_branca", {})
        plaquetas = data.get("plaquetas", {})
        
        return cls(
            nome_paciente=paciente.get("nome", ""),
            idade=paciente.get("idade", 0),
            sexo=paciente.get("sexo", "M"),
            data_coleta=paciente.get("data_coleta", ""),
            hemacias=serie_vermelha.get("hemacias"),
            hemoglobina=serie_vermelha.get("hemoglobina"),
            hematocrito=serie_vermelha.get("hematocrito"),
            vcm=serie_vermelha.get("vcm"),
            hcm=serie_vermelha.get("hcm"),
            chcm=serie_vermelha.get("chcm"),
            rdw=serie_vermelha.get("rdw"),
            leucocitos=serie_branca.get("leucocitos"),
            neutrofilos=serie_branca.get("neutrofilos"),
            bastonetes=serie_branca.get("bastonetes"),
            segmentados=serie_branca.get("segmentados"),
            linfocitos=serie_branca.get("linfocitos"),
            monocitos=serie_branca.get("monocitos"),
            eosinofilos=serie_branca.get("eosinofilos"),
            basofilos=serie_branca.get("basofilos"),
            plaquetas=plaquetas.get("contagem"),
            observacoes=data.get("observacoes", "")
        )
