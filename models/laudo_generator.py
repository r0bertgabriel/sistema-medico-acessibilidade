"""
Gerador de laudos médicos formatados
"""
from datetime import datetime
from typing import Dict, List

from .ecg_analyzer import AnalisadorECG
from .ecg_data import DadosECG


class GeradorLaudo:
    """Classe responsável por gerar laudos médicos formatados"""
    
    def __init__(self):
        self.analisador = AnalisadorECG()
    
    def gerar_laudo_completo(self, dados: DadosECG) -> Dict[str, str]:
        """
        Gera um laudo médico completo em formato texto e para áudio
        
        Returns:
            Dict com 'texto_completo' e 'texto_audio'
        """
        # Realizar análise
        resultado = self.analisador.analisar(dados)
        
        # Gerar laudo formatado
        laudo_texto = self._formatar_laudo_texto(dados, resultado)
        laudo_audio = self._formatar_laudo_audio(dados, resultado)
        
        return {
            "texto_completo": laudo_texto,
            "texto_audio": laudo_audio,
            "achados": resultado["achados"],
            "diagnosticos": resultado["diagnosticos"]
        }
    
    def _formatar_laudo_texto(self, dados: DadosECG, resultado: Dict) -> str:
        """Formata o laudo para visualização em texto"""
        
        linhas = []
        linhas.append("=" * 80)
        linhas.append("INFORME DE ELECTROCARDIOGRAMA")
        linhas.append("=" * 80)
        linhas.append("")
        
        # Dados do paciente
        if dados.paciente_id or dados.nome_paciente or dados.genero or dados.idade:
            linhas.append("IDENTIFICACIÓN DEL PACIENTE")
            linhas.append("-" * 80)
            if dados.nome_paciente:
                linhas.append(f"Nombre: {dados.nome_paciente}")
            if dados.genero:
                linhas.append(f"Género: {dados.genero}")
            if dados.idade:
                linhas.append(f"Edad: {dados.idade} años")
            if dados.paciente_id:
                linhas.append(f"ID: {dados.paciente_id}")
            if dados.data_exame:
                linhas.append(f"Fecha del Examen: {dados.data_exame}")
            else:
                linhas.append(f"Fecha del Examen: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            linhas.append("")
        
        # Dados técnicos
        linhas.append("DATOS TÉCNICOS DEL ECG")
        linhas.append("-" * 80)
        linhas.append(f"Ritmo: {self._formatar_ritmo(dados.ritmo)}")
        linhas.append(f"Frecuencia Cardíaca: {dados.frequencia_cardiaca} lpm")
        linhas.append(f"Regularidad: {dados.regularidade.capitalize()}")
        linhas.append(f"Eje Eléctrico del QRS: {dados.eixo_qrs}°")
        
        if dados.intervalos:
            linhas.append(f"Intervalo PR: {dados.intervalos.pr:.3f} s")
            linhas.append(f"Duración del QRS: {dados.intervalos.qrs:.3f} s")
            linhas.append(f"Intervalo QT: {dados.intervalos.qt:.3f} s")
            linhas.append(f"QTc (corregido): {dados.intervalos.qtc:.3f} s")
        
        linhas.append("")
        
        # Achados
        linhas.append("HALLAZGOS ELECTROCARDIOGRÁFICOS")
        linhas.append("-" * 80)
        if resultado["achados"]:
            for achado in resultado["achados"]:
                linhas.append(f"• {achado}")
        else:
            linhas.append("• Sin alteraciones significativas")
        linhas.append("")
        
        # Diagnósticos
        linhas.append("DIAGNÓSTICOS")
        linhas.append("-" * 80)
        if resultado["diagnosticos"]:
            for i, diag in enumerate(resultado["diagnosticos"], 1):
                linhas.append(f"{i}. {diag}")
        else:
            linhas.append("• ECG dentro de los parámetros de normalidad")
        linhas.append("")
        
        # Conclusão
        linhas.append("CONCLUSIÓN")
        linhas.append("-" * 80)
        linhas.append(resultado["conclusao"])
        linhas.append("")
        
        # Alertas especiais
        if dados.infarto or dados.isquemia:
            linhas.append("")
            linhas.append("!" * 80)
            linhas.append("ATENCIÓN: HALLAZGOS QUE REQUIEREN EVALUACIÓN MÉDICA INMEDIATA")
            linhas.append("!" * 80)
        
        linhas.append("")
        linhas.append("=" * 80)
        linhas.append("Informe generado automáticamente por el Sistema de Accesibilidad Médica")
        linhas.append("Este informe debe ser revisado por un médico cardiólogo")
        linhas.append("=" * 80)
        
        return "\n".join(linhas)
    
    def _formatar_laudo_audio(self, dados: DadosECG, resultado: Dict) -> str:
        """Formata o laudo para narração em áudio usando texto completo (sem caracteres especiais)
        
        Usa o laudo completo mas remove caracteres de formatação especiais
        """
        # Gerar laudo completo formatado
        laudo_completo = self._formatar_laudo_texto(dados, resultado)
        
        # Este texto será limpo pelo AudioCacheService antes de gerar o áudio
        # Aqui apenas retornamos o texto completo
        return laudo_completo
    
    def _formatar_laudo_audio_OLD(self, dados: DadosECG, resultado: Dict) -> str:
        """VERSÃO ANTIGA - Formata o laudo para narração em áudio (conciso e otimizado)"""
        
        partes = []
        
        # Introdução com identificação
        if dados.nome_paciente:
            # Se tiver nome, usar apenas o nome
            partes.append(f"E C G de {dados.nome_paciente}.")
        elif dados.genero and dados.idade:
            # Se não tiver nome mas tiver gênero e idade
            partes.append(f"E C G de paciente {dados.genero.lower()}, {dados.idade} años.")
        else:
            partes.append("Informe de electrocardiograma.")
        
        # Dados principais compactos
        partes.append(f"Ritmo {self._formatar_ritmo(dados.ritmo)}, {dados.regularidade}, {dados.frequencia_cardiaca} latidos por minuto.")
        
        # Intervalos - mencionar valores específicos importantes
        intervalos_info = []
        if dados.intervalos:
            # PR sempre mencionado
            pr_ms = int(dados.intervalos.pr * 1000)
            if dados.intervalos.pr < 0.12:
                intervalos_info.append(f"P R corto, {pr_ms} milisegundos")
            elif dados.intervalos.pr > 0.20:
                intervalos_info.append(f"P R prolongado, {pr_ms} milisegundos")
            else:
                intervalos_info.append(f"P R {pr_ms} milisegundos")
            
            # QRS sempre mencionado
            qrs_ms = int(dados.intervalos.qrs * 1000)
            if dados.intervalos.qrs > 0.12:
                intervalos_info.append(f"Q R S ensanchado, {qrs_ms} milisegundos")
            elif dados.intervalos.qrs > 0.10:
                intervalos_info.append(f"Q R S {qrs_ms} milisegundos, limítrofe")
            else:
                intervalos_info.append(f"Q R S {qrs_ms} milisegundos")
            
            # QTc apenas se alterado
            if dados.intervalos.qtc > 0.44:
                intervalos_info.append(f"Q T c prolongado")
        
        if intervalos_info:
            partes.append(". ".join(intervalos_info) + ".")
        
        # Eixo elétrico sempre mencionado
        eixo = dados.eixo_qrs
        if eixo < -30:
            partes.append(f"Eje desviado a la izquierda, {eixo} grados.")
        elif eixo > 90:
            partes.append(f"Eje desviado a la derecha, {eixo} grados.")
        else:
            partes.append(f"Eje normal, {eixo} grados.")
        
        # Diagnósticos com contexto
        if resultado["diagnosticos"]:
            # Adicionar morfologia se relevante
            if dados.complexo_qrs and dados.complexo_qrs.morfologia != 'normal':
                morfologia = dados.complexo_qrs.morfologia
                if morfologia == "RSR'":
                    partes.append("Morfología Q R S: patrón R S R prima en V1 y V2.")
            
            # Adicionar morfologia de onda P se alterada
            if dados.onda_p and dados.onda_p.morfologia != 'normal':
                if 'aumentada' in dados.onda_p.morfologia.lower():
                    partes.append("Onda P: aumentada, sugiriendo sobrecarga atrial.")
            
            if len(resultado["diagnosticos"]) == 1:
                partes.append(f"Diagnóstico: {resultado['diagnosticos'][0]}.")
            else:
                # Até 3 diagnósticos
                partes.append("Diagnósticos: " + ". ".join(resultado["diagnosticos"][:3]) + ".")
        else:
            partes.append("E C G dentro de los límites normales.")
        
        # Alertas críticos
        if dados.infarto:
            partes.append("¡ATENCIÓN! Infarto agudo. ¡Evaluación médica inmediata!")
        elif dados.isquemia:
            partes.append("Atención: isquemia miocárdica. Evaluación cardiológica urgente.")
        
        return " ".join(partes)
    
    def _formatar_ritmo(self, ritmo: str) -> str:
        """Converte o código do ritmo para descrição legível"""
        ritmos = {
            "sinusal": "sinusal",
            "fibrilacao_atrial": "fibrilación auricular",
            "flutter_atrial": "flutter auricular",
            "taquicardia_supraventricular": "taquicardia supraventricular",
            "taquicardia_ventricular": "taquicardia ventricular",
            "bradicardia": "bradicardia",
        }
        return ritmos.get(ritmo, ritmo)
    
    def gerar_resumo(self, dados: DadosECG) -> str:
        """Gera um resumo curto do ECG"""
        resultado = self.analisador.analisar(dados)
        
        if not resultado["diagnosticos"]:
            return "ECG Normal"
        
        if len(resultado["diagnosticos"]) == 1:
            return resultado["diagnosticos"][0]
        
        return f"{len(resultado['diagnosticos'])} alteraciones encontradas"
