"""
Analisador automático de Hemograma Completo
"""
from typing import Any, Dict, Optional, Tuple

from .hemograma_data import DadosHemograma


class AnalisadorHemograma:
    """Classe responsável pela análise e interpretação de dados de Hemograma
    
    Baseado em valores de referência de laboratórios brasileiros (Fleury, Delboni)
    e diretrizes internacionais de hematologia.
    """
    
    # Valores de referência baseados em estudos do Fleury (100.000+ indivíduos)
    # e padrões internacionais
    VALORES_REFERENCIA = {
        "M": {  # Masculino
            "hemacias": {"min": 4.32, "max": 5.67, "unidade": "milhões/µL"},
            "hemoglobina": {"min": 13.3, "max": 16.5, "unidade": "g/dL"},
            "hematocrito": {"min": 39.2, "max": 49.0, "unidade": "%"},
            "vcm": {"min": 80.0, "max": 100.0, "unidade": "fL"},
            "hcm": {"min": 27.0, "max": 32.0, "unidade": "pg"},
            "chcm": {"min": 32.0, "max": 36.0, "unidade": "g/dL"},
            "rdw": {"min": 11.5, "max": 14.5, "unidade": "%"},
            "leucocitos": {"min": 3650, "max": 8120, "unidade": "/µL"},
            "neutrofilos": {"min": 1800, "max": 7000, "unidade": "/µL"},
            "linfocitos": {"min": 1000, "max": 4000, "unidade": "/µL"},
            "monocitos": {"min": 100, "max": 1000, "unidade": "/µL"},
            "eosinofilos": {"min": 40, "max": 500, "unidade": "/µL"},
            "basofilos": {"min": 10, "max": 100, "unidade": "/µL"},
            "plaquetas": {"min": 150000, "max": 450000, "unidade": "/µL"}
        },
        "F": {  # Feminino
            "hemacias": {"min": 3.83, "max": 4.99, "unidade": "milhões/µL"},
            "hemoglobina": {"min": 11.7, "max": 14.9, "unidade": "g/dL"},
            "hematocrito": {"min": 35.1, "max": 44.1, "unidade": "%"},
            "vcm": {"min": 80.0, "max": 100.0, "unidade": "fL"},
            "hcm": {"min": 27.0, "max": 32.0, "unidade": "pg"},
            "chcm": {"min": 32.0, "max": 36.0, "unidade": "g/dL"},
            "rdw": {"min": 11.5, "max": 14.5, "unidade": "%"},
            "leucocitos": {"min": 3470, "max": 8290, "unidade": "/µL"},
            "neutrofilos": {"min": 1800, "max": 7000, "unidade": "/µL"},
            "linfocitos": {"min": 1000, "max": 4000, "unidade": "/µL"},
            "monocitos": {"min": 100, "max": 1000, "unidade": "/µL"},
            "eosinofilos": {"min": 40, "max": 500, "unidade": "/µL"},
            "basofilos": {"min": 10, "max": 100, "unidade": "/µL"},
            "plaquetas": {"min": 150000, "max": 450000, "unidade": "/µL"}
        }
    }
    
    def __init__(self, dados: DadosHemograma):
        """Inicializa o analisador com os dados do hemograma
        
        Args:
            dados: Instância de DadosHemograma com os valores do exame
        """
        self.dados = dados
        self.referencias = self.VALORES_REFERENCIA.get(dados.sexo, self.VALORES_REFERENCIA["M"])
        self.alteracoes = []
        self.flags = {}
        
    def analisar(self) -> Dict[str, Any]:
        """Realiza análise completa do hemograma
        
        Returns:
            Dicionário com análise completa, incluindo interpretação e laudo
        """
        # Análise de cada série
        self._analisar_serie_vermelha()
        self._analisar_serie_branca()
        self._analisar_plaquetas()
        
        # Interpretação integrada
        interpretacao = self._gerar_interpretacao()
        
        # Gerar laudo textual
        laudo = self._gerar_laudo()
        
        # Gerar versão do laudo para áudio (sem formatação)
        laudo_audio = self._gerar_laudo_audio()
        
        return {
            "dados": self.dados.to_dict(),
            "flags": self.flags,
            "alteracoes": self.alteracoes,
            "interpretacao": interpretacao,
            "laudo": laudo,
            "laudo_audio": laudo_audio,
            "referencias": self.referencias
        }
    
    def _verificar_parametro(self, nome: str, valor: Optional[float], 
                            ref: Dict) -> Tuple[str, Optional[str]]:
        """Verifica se um parâmetro está dentro dos valores de referência
        
        Args:
            nome: Nome do parâmetro
            valor: Valor medido
            ref: Dicionário com min, max e unidade de referência
            
        Returns:
            Tupla (flag, mensagem) onde flag é 'N' (normal), 'L' (baixo) ou 'H' (alto)
        """
        if valor is None:
            return "?", None
            
        if valor < ref["min"]:
            msg = f"{nome} BAIXO: {valor} {ref['unidade']} (ref: {ref['min']}-{ref['max']})"
            return "L", msg
        elif valor > ref["max"]:
            msg = f"{nome} ALTO: {valor} {ref['unidade']} (ref: {ref['min']}-{ref['max']})"
            return "H", msg
        else:
            return "N", None
    
    def _analisar_serie_vermelha(self):
        """Analisa série vermelha (eritrograma)"""
        # Hemácias
        flag, msg = self._verificar_parametro("Hemácias", self.dados.hemacias, 
                                              self.referencias["hemacias"])
        self.flags["hemacias"] = flag
        if msg:
            self.alteracoes.append(msg)
        
        # Hemoglobina
        flag, msg = self._verificar_parametro("Hemoglobina", self.dados.hemoglobina,
                                              self.referencias["hemoglobina"])
        self.flags["hemoglobina"] = flag
        if msg:
            self.alteracoes.append(msg)
            
        # Hematócrito
        flag, msg = self._verificar_parametro("Hematócrito", self.dados.hematocrito,
                                              self.referencias["hematocrito"])
        self.flags["hematocrito"] = flag
        if msg:
            self.alteracoes.append(msg)
        
        # VCM (Volume Corpuscular Médio)
        flag, msg = self._verificar_parametro("VCM", self.dados.vcm,
                                              self.referencias["vcm"])
        self.flags["vcm"] = flag
        if msg:
            self.alteracoes.append(msg)
        
        # HCM (Hemoglobina Corpuscular Média)
        flag, msg = self._verificar_parametro("HCM", self.dados.hcm,
                                              self.referencias["hcm"])
        self.flags["hcm"] = flag
        if msg:
            self.alteracoes.append(msg)
        
        # CHCM (Concentração de Hemoglobina Corpuscular Média)
        flag, msg = self._verificar_parametro("CHCM", self.dados.chcm,
                                              self.referencias["chcm"])
        self.flags["chcm"] = flag
        if msg:
            self.alteracoes.append(msg)
        
        # RDW (Variação do tamanho das hemácias)
        flag, msg = self._verificar_parametro("RDW", self.dados.rdw,
                                              self.referencias["rdw"])
        self.flags["rdw"] = flag
        if msg:
            self.alteracoes.append(msg)
    
    def _analisar_serie_branca(self):
        """Analisa série branca (leucograma)"""
        # Leucócitos totais
        flag, msg = self._verificar_parametro("Leucócitos", self.dados.leucocitos,
                                              self.referencias["leucocitos"])
        self.flags["leucocitos"] = flag
        if msg:
            self.alteracoes.append(msg)
        
        # Neutrófilos
        if self.dados.neutrofilos:
            flag, msg = self._verificar_parametro("Neutrófilos", self.dados.neutrofilos,
                                                  self.referencias["neutrofilos"])
            self.flags["neutrofilos"] = flag
            if msg:
                self.alteracoes.append(msg)
        
        # Linfócitos
        if self.dados.linfocitos:
            flag, msg = self._verificar_parametro("Linfócitos", self.dados.linfocitos,
                                                  self.referencias["linfocitos"])
            self.flags["linfocitos"] = flag
            if msg:
                self.alteracoes.append(msg)
        
        # Monócitos
        if self.dados.monocitos:
            flag, msg = self._verificar_parametro("Monócitos", self.dados.monocitos,
                                                  self.referencias["monocitos"])
            self.flags["monocitos"] = flag
            if msg:
                self.alteracoes.append(msg)
        
        # Eosinófilos
        if self.dados.eosinofilos:
            flag, msg = self._verificar_parametro("Eosinófilos", self.dados.eosinofilos,
                                                  self.referencias["eosinofilos"])
            self.flags["eosinofilos"] = flag
            if msg:
                self.alteracoes.append(msg)
        
        # Basófilos
        if self.dados.basofilos:
            flag, msg = self._verificar_parametro("Basófilos", self.dados.basofilos,
                                                  self.referencias["basofilos"])
            self.flags["basofilos"] = flag
            if msg:
                self.alteracoes.append(msg)
    
    def _analisar_plaquetas(self):
        """Analisa contagem de plaquetas"""
        flag, msg = self._verificar_parametro("Plaquetas", self.dados.plaquetas,
                                              self.referencias["plaquetas"])
        self.flags["plaquetas"] = flag
        if msg:
            self.alteracoes.append(msg)
    
    def _gerar_interpretacao(self) -> Dict[str, Any]:
        """Gera interpretação clínica baseada nos achados
        
        Returns:
            Dicionário com interpretação estruturada
        """
        interpretacao = {
            "status_geral": "NORMAL",
            "achados_principais": [],
            "sugestoes_diagnosticas": [],
            "observacoes": []
        }
        
        # Verificar se há alterações
        if self.alteracoes:
            interpretacao["status_geral"] = "ALTERADO"
        
        # Análise de anemia
        if self.flags.get("hemoglobina") == "L":
            interpretacao["achados_principais"].append("Anemia detectada")
            
            # Classificar tipo de anemia baseado no VCM
            if self.dados.vcm and self.dados.vcm < self.referencias["vcm"]["min"]:
                interpretacao["sugestoes_diagnosticas"].append(
                    "Anemia microcítica (VCM bajo). Sugestivo de deficiencia de hierro o talasemia"
                )
            elif self.dados.vcm and self.dados.vcm > self.referencias["vcm"]["max"]:
                interpretacao["sugestoes_diagnosticas"].append(
                    "Anemia macrocítica (VCM alto). Sugestivo de deficiencia de B12 o folato"
                )
            else:
                interpretacao["sugestoes_diagnosticas"].append(
                    "Anemia normocítica. Investigar causas crónicas o hemólisis"
                )
        
        # Análise de policitemia
        if self.flags.get("hemoglobina") == "H" and self.flags.get("hematocrito") == "H":
            interpretacao["achados_principais"].append("Policitemia detectada")
            interpretacao["sugestoes_diagnosticas"].append(
                "Hemoglobina y hematocrito elevados. Investigar policitemia vera o causas secundarias"
            )
        
        # Análise de leucocitose
        if self.flags.get("leucocitos") == "H":
            interpretacao["achados_principais"].append("Leucocitosis")
            
            if self.flags.get("neutrofilos") == "H":
                interpretacao["sugestoes_diagnosticas"].append(
                    "Neutrofilia. Sugestivo de infección bacteriana aguda o proceso inflamatorio"
                )
            if self.flags.get("linfocitos") == "H":
                interpretacao["sugestoes_diagnosticas"].append(
                    "Linfocitosis. Sugestivo de infección viral o proceso linfoproliferativo"
                )
            if self.flags.get("eosinofilos") == "H":
                interpretacao["sugestoes_diagnosticas"].append(
                    "Eosinofilia. Sugestivo de alergia, parasitosis o reacción medicamentosa"
                )
        
        # Análise de leucopenia
        if self.flags.get("leucocitos") == "L":
            interpretacao["achados_principais"].append("Leucopenia")
            interpretacao["sugestoes_diagnosticas"].append(
                "Leucocitos bajos. Investigar causas virales, medicamentosas o inmunosupresión"
            )
        
        # Análise de plaquetopenia
        if self.flags.get("plaquetas") == "L":
            interpretacao["achados_principais"].append("Trombocitopenia")
            if self.dados.plaquetas and self.dados.plaquetas < 50000:
                interpretacao["observacoes"].append(
                    "¡ATENCIÓN! Trombocitopenia severa (menor que 50.000). Riesgo aumentado de sangrado"
                )
            interpretacao["sugestoes_diagnosticas"].append(
                "Plaquetas bajas. Investigar causas (destrucción periférica, producción disminuida, etc)"
            )
        
        # Análise de plaquetose
        if self.flags.get("plaquetas") == "H":
            interpretacao["achados_principais"].append("Trombocitosis")
            interpretacao["sugestoes_diagnosticas"].append(
                "Plaquetas elevadas. Investigar trombocitosis reactiva o esencial"
            )
        
        # RDW elevado
        if self.flags.get("rdw") == "H":
            interpretacao["observacoes"].append(
                "RDW elevado indica anisocitosis (variación en el tamaño de los eritrocitos)"
            )
        
        # Se tudo normal
        if not interpretacao["achados_principais"]:
            interpretacao["achados_principais"].append(
                "Todos los parámetros dentro de los valores de referencia"
            )
        
        return interpretacao
    
    def _gerar_laudo(self) -> str:
        """Gera laudo textual completo
        
        Returns:
            String com laudo formatado
        """
        linhas = []
        
        # Cabeçalho
        linhas.append("=" * 80)
        linhas.append("INFORME DE HEMOGRAMA COMPLETO")
        linhas.append("=" * 80)
        linhas.append("")
        
        # Dados do paciente
        linhas.append(f"Paciente: {self.dados.nome_paciente}")
        linhas.append(f"Edad: {self.dados.idade} años")
        linhas.append(f"Sexo: {'Masculino' if self.dados.sexo == 'M' else 'Femenino'}")
        if self.dados.data_coleta:
            linhas.append(f"Fecha de la recolección: {self.dados.data_coleta}")
        linhas.append("")
        linhas.append("-" * 80)
        
        # Série Vermelha
        linhas.append("ERITROGRAMA (SERIE ROJA)")
        linhas.append("-" * 80)
        
        if self.dados.hemacias:
            ref = self.referencias["hemacias"]
            flag = self.flags.get("hemacias", "?")
            linhas.append(f"Eritrocitos: {self.dados.hemacias} {ref['unidade']} "
                         f"(ref: {ref['min']}-{ref['max']}) [{flag}]")
        
        if self.dados.hemoglobina:
            ref = self.referencias["hemoglobina"]
            flag = self.flags.get("hemoglobina", "?")
            linhas.append(f"Hemoglobina: {self.dados.hemoglobina} {ref['unidade']} "
                         f"(ref: {ref['min']}-{ref['max']}) [{flag}]")
        
        if self.dados.hematocrito:
            ref = self.referencias["hematocrito"]
            flag = self.flags.get("hematocrito", "?")
            linhas.append(f"Hematocrito: {self.dados.hematocrito} {ref['unidade']} "
                         f"(ref: {ref['min']}-{ref['max']}) [{flag}]")
        
        if self.dados.vcm:
            ref = self.referencias["vcm"]
            flag = self.flags.get("vcm", "?")
            linhas.append(f"VCM: {self.dados.vcm} {ref['unidade']} "
                         f"(ref: {ref['min']}-{ref['max']}) [{flag}]")
        
        if self.dados.hcm:
            ref = self.referencias["hcm"]
            flag = self.flags.get("hcm", "?")
            linhas.append(f"HCM: {self.dados.hcm} {ref['unidade']} "
                         f"(ref: {ref['min']}-{ref['max']}) [{flag}]")
        
        if self.dados.chcm:
            ref = self.referencias["chcm"]
            flag = self.flags.get("chcm", "?")
            linhas.append(f"CHCM: {self.dados.chcm} {ref['unidade']} "
                         f"(ref: {ref['min']}-{ref['max']}) [{flag}]")
        
        if self.dados.rdw:
            ref = self.referencias["rdw"]
            flag = self.flags.get("rdw", "?")
            linhas.append(f"RDW: {self.dados.rdw} {ref['unidade']} "
                         f"(ref: {ref['min']}-{ref['max']}) [{flag}]")
        
        linhas.append("")
        
        # Série Branca
        linhas.append("-" * 80)
        linhas.append("LEUCOGRAMA (SERIE BLANCA)")
        linhas.append("-" * 80)
        
        if self.dados.leucocitos:
            ref = self.referencias["leucocitos"]
            flag = self.flags.get("leucocitos", "?")
            linhas.append(f"Leucocitos totales: {self.dados.leucocitos} {ref['unidade']} "
                         f"(ref: {ref['min']}-{ref['max']}) [{flag}]")
        
        if self.dados.neutrofilos:
            ref = self.referencias["neutrofilos"]
            flag = self.flags.get("neutrofilos", "?")
            linhas.append(f"  Neutrófilos: {self.dados.neutrofilos} {ref['unidade']} "
                         f"(ref: {ref['min']}-{ref['max']}) [{flag}]")
            
            if self.dados.bastonetes:
                linhas.append(f"    - Cayados: {self.dados.bastonetes} /µL")
            if self.dados.segmentados:
                linhas.append(f"    - Segmentados: {self.dados.segmentados} /µL")
        
        if self.dados.linfocitos:
            ref = self.referencias["linfocitos"]
            flag = self.flags.get("linfocitos", "?")
            linhas.append(f"  Linfocitos: {self.dados.linfocitos} {ref['unidade']} "
                         f"(ref: {ref['min']}-{ref['max']}) [{flag}]")
        
        if self.dados.monocitos:
            ref = self.referencias["monocitos"]
            flag = self.flags.get("monocitos", "?")
            linhas.append(f"  Monocitos: {self.dados.monocitos} {ref['unidade']} "
                         f"(ref: {ref['min']}-{ref['max']}) [{flag}]")
        
        if self.dados.eosinofilos:
            ref = self.referencias["eosinofilos"]
            flag = self.flags.get("eosinofilos", "?")
            linhas.append(f"  Eosinófilos: {self.dados.eosinofilos} {ref['unidade']} "
                         f"(ref: {ref['min']}-{ref['max']}) [{flag}]")
        
        if self.dados.basofilos:
            ref = self.referencias["basofilos"]
            flag = self.flags.get("basofilos", "?")
            linhas.append(f"  Basófilos: {self.dados.basofilos} {ref['unidade']} "
                         f"(ref: {ref['min']}-{ref['max']}) [{flag}]")
        
        linhas.append("")
        
        # Plaquetas
        linhas.append("-" * 80)
        linhas.append("PLAQUETAS")
        linhas.append("-" * 80)
        
        if self.dados.plaquetas:
            ref = self.referencias["plaquetas"]
            flag = self.flags.get("plaquetas", "?")
            linhas.append(f"Plaquetas: {self.dados.plaquetas} {ref['unidade']} "
                         f"(ref: {ref['min']}-{ref['max']}) [{flag}]")
        
        linhas.append("")
        
        # Interpretação
        interpretacao = self._gerar_interpretacao()
        
        linhas.append("=" * 80)
        linhas.append("INTERPRETACIÓN")
        linhas.append("=" * 80)
        linhas.append("")
        linhas.append(f"Estado General: {interpretacao['status_geral']}")
        linhas.append("")
        
        if interpretacao["achados_principais"]:
            linhas.append("Hallazgos Principales:")
            for achado in interpretacao["achados_principais"]:
                linhas.append(f"  • {achado}")
            linhas.append("")
        
        if interpretacao["sugestoes_diagnosticas"]:
            linhas.append("Sugerencias Diagnósticas:")
            for sugestao in interpretacao["sugestoes_diagnosticas"]:
                linhas.append(f"  • {sugestao}")
            linhas.append("")
        
        if interpretacao["observacoes"]:
            linhas.append("Observaciones:")
            for obs in interpretacao["observacoes"]:
                linhas.append(f"  ⚠ {obs}")
            linhas.append("")
        
        if self.dados.observacoes:
            linhas.append("Observaciones del Examen:")
            linhas.append(self.dados.observacoes)
            linhas.append("")
        
        linhas.append("=" * 80)
        linhas.append("IMPORTANTE: Este informe es generado automáticamente y debe ser")
        linhas.append("evaluado por profesional médico calificado para interpretación")
        linhas.append("clínica completa considerando el contexto del paciente.")
        linhas.append("=" * 80)
        
        return "\n".join(linhas)
    
    def _gerar_laudo_audio(self) -> str:
        """Gera versão do laudo otimizada para áudio (concisa, sem caracteres especiais)
        
        Returns:
            String com laudo formatado para narração em áudio de forma rápida
        """
        linhas = []
        
        # Cabeçalho resumido
        linhas.append(f"Hemograma de {self.dados.nome_paciente}, {self.dados.idade} años.")
        
        # Apenas valores alterados da Série Vermelha
        alterados_vermelho = []
        if self.dados.hemoglobina and self.flags.get("hemoglobina") != "N":
            status = "baja" if self.flags.get("hemoglobina") == "L" else "alta"
            alterados_vermelho.append(f"Hemoglobina {status}: {self.dados.hemoglobina}")
        
        if self.dados.hemacias and self.flags.get("hemacias") != "N":
            status = "bajos" if self.flags.get("hemacias") == "L" else "altos"
            alterados_vermelho.append(f"Eritrocitos {status}: {self.dados.hemacias}")
        
        if self.dados.vcm and self.flags.get("vcm") != "N":
            status = "bajo" if self.flags.get("vcm") == "L" else "alto"
            alterados_vermelho.append(f"VCM {status}: {self.dados.vcm}")
        
        if alterados_vermelho:
            linhas.append("Serie roja: " + ", ".join(alterados_vermelho) + ".")
        else:
            linhas.append("Serie roja: sin alteraciones.")
        
        # Apenas valores alterados da Série Branca
        alterados_branco = []
        if self.dados.leucocitos and self.flags.get("leucocitos") != "N":
            status = "bajos" if self.flags.get("leucocitos") == "L" else "altos"
            alterados_branco.append(f"Leucocitos {status}: {self.dados.leucocitos}")
        
        if self.dados.neutrofilos and self.flags.get("neutrofilos") != "N":
            status = "bajos" if self.flags.get("neutrofilos") == "L" else "altos"
            alterados_branco.append(f"Neutrófilos {status}: {self.dados.neutrofilos}")
        
        if self.dados.linfocitos and self.flags.get("linfocitos") != "N":
            status = "bajos" if self.flags.get("linfocitos") == "L" else "altos"
            alterados_branco.append(f"Linfocitos {status}: {self.dados.linfocitos}")
        
        if alterados_branco:
            linhas.append("Serie blanca: " + ", ".join(alterados_branco) + ".")
        else:
            linhas.append("Serie blanca: sin alteraciones.")
        
        # Plaquetas
        if self.dados.plaquetas:
            flag = self.flags.get("plaquetas", "N")
            if flag != "N":
                status = "bajas" if flag == "L" else "altas"
                linhas.append(f"Plaquetas {status}: {self.dados.plaquetas}.")
            else:
                linhas.append("Plaquetas normales.")
        
        # Interpretação resumida
        interpretacao = self._gerar_interpretacao()
        linhas.append(f"Estado: {interpretacao['status_geral']}.")
        
        if interpretacao["achados_principais"]:
            # Apenas os 3 primeiros achados mais importantes
            achados_resumidos = interpretacao["achados_principais"][:3]
            linhas.append("Principales hallazgos: " + ". ".join(achados_resumidos) + ".")
        
        if interpretacao["sugestoes_diagnosticas"]:
            # Apenas a primeira sugestão
            linhas.append(f"Sugerencia diagnóstica: {interpretacao['sugestoes_diagnosticas'][0]}.")
        
        return " ".join(linhas)
