"""
Analisador automático de ECG
"""
from typing import Any, Dict, List, Optional

from .ecg_data import DadosECG


class AnalisadorECG:
    """Classe responsável pela análise e interpretação de dados de ECG
    
    Baseado em diretrizes da American Heart Association (AHA) e padrões
    internacionais de interpretação de ECG.
    """
    
    # Limiares de normalidade baseados em diretrizes da AHA
    LIMIARES = {
        # Frequência cardíaca (bpm)
        "fc_min": 60,
        "fc_max": 100,
        "fc_bradicardia_severa": 40,
        "fc_taquicardia_severa": 150,
        
        # Intervalo PR (segundos)
        "pr_min": 0.12,
        "pr_max": 0.20,
        "pr_bloqueio_1grau": 0.20,
        
        # Complexo QRS (segundos)
        "qrs_min": 0.06,
        "qrs_max": 0.10,
        "qrs_bloqueio_ramo": 0.12,
        
        # Intervalo QT corrigido (segundos)
        "qtc_max_homem": 0.45,
        "qtc_max_mulher": 0.47,
        "qtc_prolongado": 0.50,
        
        # Eixo elétrico (graus)
        "eixo_min_normal": -30,
        "eixo_max_normal": 90,
        "eixo_lad": -30,  # Left Axis Deviation
        "eixo_rad": 90,   # Right Axis Deviation
        
        # Ondas e segmentos
        "st_elevacao": 0.1,  # mm
        "st_depressao": 0.05,  # mm
        "onda_q_patologica": 0.04,  # segundos
    }
    
    def __init__(self):
        self.dados_ecg: Optional[DadosECG] = None
        self.achados: List[str] = []
        self.diagnosticos: List[str] = []
        
    def analisar(self, dados: DadosECG) -> Dict[str, Any]:
        """
        Analisa os dados do ECG e retorna diagnósticos
        """
        self.dados_ecg = dados
        self.achados = []
        self.diagnosticos = []
        
        # Análise sequencial
        self._analisar_ritmo()
        self._analisar_frequencia()
        self._analisar_eixo()
        self._analisar_intervalos()
        self._analisar_ondas_p()
        self._analisar_complexo_qrs()
        self._analisar_segmento_st()
        self._analisar_onda_t()
        self._analisar_bloqueios()
        self._analisar_sobrecargas()
        self._analisar_isquemia()
        
        return {
            "achados": self.achados,
            "diagnosticos": self.diagnosticos,
            "conclusao": self._gerar_conclusao()
        }
    
    def _analisar_ritmo(self):
        """Analisa o ritmo cardíaco"""
        if not self.dados_ecg:
            return
            
        if self.dados_ecg.ritmo == "sinusal":
            if self.dados_ecg.regularidade == "regular":
                self.achados.append("Ritmo sinusal regular")
            else:
                self.achados.append("Ritmo sinusal irregular")
                self.diagnosticos.append("Arritmia sinusal")
        elif self.dados_ecg.ritmo == "fibrilacao_atrial":
            self.achados.append("Fibrilação atrial")
            self.diagnosticos.append("Fibrilação atrial")
        elif self.dados_ecg.ritmo == "flutter_atrial":
            self.achados.append("Flutter atrial")
            self.diagnosticos.append("Flutter atrial")
    
    def _analisar_frequencia(self):
        """Analisa a frequência cardíaca com critérios clínicos expandidos"""
        if not self.dados_ecg:
            return
            
        fc = self.dados_ecg.frequencia_cardiaca
        
        # Bradicardia
        if fc < self.LIMIARES["fc_min"]:
            if fc < self.LIMIARES["fc_bradicardia_severa"]:
                self.achados.append(f"Bradicardia sinusal severa ({fc} bpm)")
                self.diagnosticos.append("Bradicardia sinusal severa - avaliar sintomas e necessidade de marca-passo")
            else:
                self.achados.append(f"Bradicardia sinusal ({fc} bpm)")
                self.diagnosticos.append("Bradicardia sinusal")
        
        # Taquicardia
        elif fc > self.LIMIARES["fc_max"]:
            if fc > self.LIMIARES["fc_taquicardia_severa"]:
                self.achados.append(f"Taquicardia sinusal severa ({fc} bpm)")
                self.diagnosticos.append("Taquicardia sinusal severa - investigar causas secundárias (febre, hipovolemia, etc)")
            else:
                self.achados.append(f"Taquicardia sinusal ({fc} bpm)")
                self.diagnosticos.append("Taquicardia sinusal")
        
        # Normal
        else:
            self.achados.append(f"Frequência cardíaca: {fc} bpm (dentro dos limites normais)")
    
    def _analisar_eixo(self):
        """Analisa o eixo elétrico do QRS"""
        if not self.dados_ecg:
            return
            
        eixo = self.dados_ecg.eixo_qrs
        
        if eixo < -30:
            if eixo < -90:
                self.achados.append(f"Desvio extremo do eixo para a direita ({eixo}°)")
                self.diagnosticos.append("Desvio extremo do eixo para a direita")
            else:
                self.achados.append(f"Desvio do eixo para a esquerda ({eixo}°)")
                self.diagnosticos.append("Desvio do eixo para a esquerda")
        elif eixo > 90:
            if eixo > 120:
                self.achados.append(f"Desvio acentuado do eixo para a direita ({eixo}°)")
            else:
                self.achados.append(f"Desvio do eixo para a direita ({eixo}°)")
            self.diagnosticos.append("Desvio do eixo para a direita")
        else:
            self.achados.append(f"Eixo elétrico normal ({eixo}°)")
    
    def _analisar_intervalos(self):
        """Analisa os intervalos PR, QRS e QT"""
        if not self.dados_ecg or not self.dados_ecg.intervalos:
            return
        
        intervalos = self.dados_ecg.intervalos
        
        # Análise do PR
        if intervalos.pr > self.LIMIARES["pr_max"]:
            self.achados.append(f"Intervalo PR prolongado ({intervalos.pr:.2f} s)")
            self.diagnosticos.append("Bloqueio atrioventricular de 1º grau")
        elif intervalos.pr < self.LIMIARES["pr_min"]:
            self.achados.append(f"Intervalo PR curto ({intervalos.pr:.2f} s)")
            self.diagnosticos.append("Possível pré-excitação ventricular")
        else:
            self.achados.append(f"Intervalo PR normal ({intervalos.pr:.2f} s)")
        
        # Análise do QRS
        if intervalos.qrs > self.LIMIARES["qrs_max"]:
            self.achados.append(f"QRS alargado ({intervalos.qrs:.2f} s)")
            if intervalos.qrs >= 0.12:
                self.achados.append("Sugestivo de bloqueio de ramo completo")
            else:
                self.achados.append("Sugestivo de bloqueio de ramo incompleto")
        else:
            self.achados.append(f"Duração do QRS normal ({intervalos.qrs:.2f} s)")
        
        # Análise do QTc (usar valor mais conservador para ambos os gêneros)
        qtc_max = self.LIMIARES["qtc_max_mulher"]  # 0.47s é o mais conservador
        
        if intervalos.qtc > qtc_max:
            self.achados.append(f"QTc prolongado ({intervalos.qtc:.2f} s)")
            self.diagnosticos.append("Prolongamento do intervalo QT corrigido")
            
            # Verificar se é severamente prolongado
            if intervalos.qtc > self.LIMIARES["qtc_prolongado"]:
                self.diagnosticos.append("⚠️ QTc severamente prolongado - risco de torsades de pointes")
        else:
            self.achados.append(f"QTc normal ({intervalos.qtc:.2f} s)")
    
    def _analisar_ondas_p(self):
        """Analisa as características da onda P"""
        if not self.dados_ecg or not self.dados_ecg.onda_p:
            return
        
        onda_p = self.dados_ecg.onda_p
        
        if not onda_p.presente:
            self.achados.append("Ausência de ondas P visíveis")
            return
        
        if onda_p.positiva_dII and onda_p.positiva_dIII and onda_p.positiva_aVF:
            self.achados.append("Ondas P sinusais (positivas em DII, DIII e aVF)")
        else:
            self.achados.append("Ondas P com morfologia atípica")
        
        if onda_p.morfologia == "aumentada_esquerda":
            self.achados.append("Onda P aumentada à esquerda")
            self.diagnosticos.append("Sobrecarga atrial esquerda")
        elif onda_p.morfologia == "aumentada_direita":
            self.achados.append("Onda P aumentada à direita")
            self.diagnosticos.append("Sobrecarga atrial direita")
    
    def _analisar_complexo_qrs(self):
        """Analisa o complexo QRS"""
        if not self.dados_ecg or not self.dados_ecg.complexo_qrs:
            return
        
        qrs = self.dados_ecg.complexo_qrs
        
        # Morfologia
        if qrs.morfologia == "RSR'":
            self.achados.append("Padrão RSR' em derivações precordiais direitas")
        
        # Progressão de R
        if qrs.progressao_r == "preservada":
            self.achados.append("Progressão da onda R preservada")
        elif qrs.progressao_r == "reduzida":
            self.achados.append("Progressão da onda R reduzida")
            self.diagnosticos.append("Alteração na progressão de R - investigar isquemia anterior")
        
        # Zona de transição
        if qrs.zona_transicao:
            self.achados.append(f"Zona de transição: {qrs.zona_transicao}")
        
        # Ondas Q patológicas
        if qrs.ondas_q_patologicas:
            self.achados.append("Presença de ondas Q patológicas")
            self.diagnosticos.append("Ondas Q patológicas - sugestivo de infarto prévio")
    
    def _analisar_segmento_st(self):
        """Analisa o segmento ST com localização anatômica da isquemia"""
        if not self.dados_ecg or not self.dados_ecg.segmento_st:
            return
        
        st = self.dados_ecg.segmento_st
        
        # Supradesnivelamento - sugestivo de IAMCSST
        if st.supradesnivelamento:
            derivacoes = ", ".join(st.supradesnivelamento)
            self.achados.append(f"Supradesnivelamento do segmento ST em {derivacoes}")
            
            # Localização anatômica
            localizacao = self._determinar_localizacao_isquemia(st.supradesnivelamento)
            if localizacao:
                self.achados.append(f"Localização provável: parede {localizacao}")
                self.diagnosticos.append(f"SUPRADESNIVELAMENTO DE ST EM PAREDE {localizacao.upper()} - SUSPEITA DE IAM COM SUPRA DE ST")
                self.diagnosticos.append("⚠️ EMERGÊNCIA MÉDICA - Acionar protocolo de IAM com urgência")
            else:
                self.diagnosticos.append("Supradesnivelamento de ST - investigar síndrome coronariana aguda")
        
        # Infradesnivelamento - isquemia subendocárdica ou recíproca
        if st.infradesnivelamento:
            derivacoes = ", ".join(st.infradesnivelamento)
            self.achados.append(f"Infradesnivelamento do segmento ST em {derivacoes}")
            
            localizacao = self._determinar_localizacao_isquemia(st.infradesnivelamento)
            if localizacao:
                self.achados.append(f"Sugestivo de isquemia subendocárdica em parede {localizacao}")
                self.diagnosticos.append(f"Infradesnivelamento de ST em parede {localizacao} - investigar angina instável ou IAMSST")
            else:
                self.diagnosticos.append("Infradesnivelamento de ST - correlacionar com quadro clínico")
        
        if not st.supradesnivelamento and not st.infradesnivelamento:
            self.achados.append("Segmento ST isoelétrico - sem alterações agudas")
    
    def _determinar_localizacao_isquemia(self, derivacoes: List[str]) -> str:
        """
        Determina a localização anatômica da isquemia baseado nas derivações
        
        Baseado em mapeamento coronariano padrão:
        - V1-V2: Septo
        - V3-V4: Anterior
        - V5-V6, I, aVL: Lateral
        - II, III, aVF: Inferior
        - V7-V9: Posterior
        """
        derivacoes_set = set(derivacoes)
        
        # Anterior
        if any(d in derivacoes_set for d in ["V1", "V2", "V3", "V4"]):
            if "V1" in derivacoes_set or "V2" in derivacoes_set:
                return "anterosseptal"
            return "anterior"
        
        # Inferior
        if any(d in derivacoes_set for d in ["II", "III", "aVF"]):
            # Verificar se há lateral também
            if any(d in derivacoes_set for d in ["V5", "V6", "I", "aVL"]):
                return "inferolateral"
            return "inferior"
        
        # Lateral
        if any(d in derivacoes_set for d in ["I", "aVL", "V5", "V6"]):
            return "lateral"
        
        # Posterior (V7, V8, V9 ou alterações recíprocas em V1-V2)
        if any(d in derivacoes_set for d in ["V7", "V8", "V9"]):
            return "posterior"
        
        return ""
    
    def _analisar_onda_t(self):
        """Analisa a onda T"""
        if not self.dados_ecg or not self.dados_ecg.onda_t:
            return
        
        onda_t = self.dados_ecg.onda_t
        
        if onda_t.invertida:
            derivacoes = ", ".join(onda_t.invertida)
            self.achados.append(f"Inversão da onda T em {derivacoes}")
            self.diagnosticos.append(f"Alterações da repolarização ventricular (T invertida em {derivacoes})")
        
        if onda_t.apiculada:
            derivacoes = ", ".join(onda_t.apiculada)
            self.achados.append(f"Ondas T apiculadas em {derivacoes}")
            self.diagnosticos.append("Ondas T apiculadas - investigar hipercalemia")
        
        if not onda_t.invertida and not onda_t.apiculada:
            self.achados.append("Ondas T sem alterações patológicas")
    
    def _analisar_bloqueios(self):
        """Analisa bloqueios de condução"""
        if not self.dados_ecg:
            return
            
        if self.dados_ecg.bloqueio_ramo:
            if self.dados_ecg.bloqueio_ramo == "incompleto_direito":
                self.achados.append("Bloqueio incompleto do ramo direito")
                self.diagnosticos.append("Bloqueio incompleto do ramo direito (BIRD)")
            elif self.dados_ecg.bloqueio_ramo == "completo_direito":
                self.achados.append("Bloqueio completo do ramo direito")
                self.diagnosticos.append("Bloqueio completo do ramo direito (BRD)")
            elif self.dados_ecg.bloqueio_ramo == "incompleto_esquerdo":
                self.achados.append("Bloqueio incompleto do ramo esquerdo")
                self.diagnosticos.append("Bloqueio incompleto do ramo esquerdo (BIRE)")
            elif self.dados_ecg.bloqueio_ramo == "completo_esquerdo":
                self.achados.append("Bloqueio completo do ramo esquerdo")
                self.diagnosticos.append("Bloqueio completo do ramo esquerdo (BRE)")
    
    def _analisar_sobrecargas(self):
        """Analisa sobrecargas atriais e ventriculares"""
        if not self.dados_ecg:
            return
            
        if self.dados_ecg.sobrecarga_ventricular:
            if self.dados_ecg.sobrecarga_ventricular == "esquerda":
                self.achados.append("Critérios para sobrecarga ventricular esquerda")
                self.diagnosticos.append("Sobrecarga ventricular esquerda")
            elif self.dados_ecg.sobrecarga_ventricular == "direita":
                self.achados.append("Critérios para sobrecarga ventricular direita")
                self.diagnosticos.append("Sobrecarga ventricular direita")
    
    def _analisar_isquemia(self):
        """Analisa sinais de isquemia ou infarto prévio"""
        if not self.dados_ecg:
            return
        
        # Ondas Q patológicas sugerem infarto prévio
        if self.dados_ecg.complexo_qrs and self.dados_ecg.complexo_qrs.ondas_q_patologicas:
            localizacao = self._determinar_localizacao_isquemia(
                self.dados_ecg.localizacao_isquemia or []
            )
            if localizacao:
                self.achados.append(f"Ondas Q patológicas sugestivas de infarto prévio em parede {localizacao}")
                self.diagnosticos.append(f"Sequela de infarto do miocárdio em parede {localizacao}")
        
        # Isquemia ativa
        if self.dados_ecg.isquemia:
            if self.dados_ecg.localizacao_isquemia:
                locais = ", ".join(self.dados_ecg.localizacao_isquemia)
                self.achados.append(f"Sinais de isquemia miocárdica ativa em região {locais}")
                self.diagnosticos.append(f"Isquemia miocárdica em parede {locais} - requer avaliação cardiológica urgente")
        
        # Infarto agudo
        if self.dados_ecg.infarto:
            self.achados.append("⚠️ SINAIS DE INFARTO AGUDO DO MIOCÁRDIO")
            self.diagnosticos.append("🚨 INFARTO AGUDO DO MIOCÁRDIO - EMERGÊNCIA MÉDICA IMEDIATA")
            self.diagnosticos.append("Recomendações: Acionar código IAM, considerar terapia de reperfusão")
    
    def _gerar_conclusao(self) -> str:
        """Gera a conclusão do laudo"""
        if not self.diagnosticos:
            return "Eletrocardiograma dentro dos padrões de normalidade."
        
        conclusao_parts = ["Eletrocardiograma com:"]
        for i, diag in enumerate(self.diagnosticos, 1):
            conclusao_parts.append(f"{i}. {diag}")
        
        return "\n".join(conclusao_parts)
