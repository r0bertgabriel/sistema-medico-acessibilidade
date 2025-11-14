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
        linhas.append("LAUDO DE ELETROCARDIOGRAMA")
        linhas.append("=" * 80)
        linhas.append("")
        
        # Dados do paciente
        if dados.paciente_id or dados.nome_paciente:
            linhas.append("IDENTIFICAÇÃO DO PACIENTE")
            linhas.append("-" * 80)
            if dados.nome_paciente:
                linhas.append(f"Nome: {dados.nome_paciente}")
            if dados.paciente_id:
                linhas.append(f"ID: {dados.paciente_id}")
            if dados.data_exame:
                linhas.append(f"Data do Exame: {dados.data_exame}")
            else:
                linhas.append(f"Data do Exame: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            linhas.append("")
        
        # Dados técnicos
        linhas.append("DADOS TÉCNICOS DO ECG")
        linhas.append("-" * 80)
        linhas.append(f"Ritmo: {self._formatar_ritmo(dados.ritmo)}")
        linhas.append(f"Frequência Cardíaca: {dados.frequencia_cardiaca} bpm")
        linhas.append(f"Regularidade: {dados.regularidade.capitalize()}")
        linhas.append(f"Eixo Elétrico do QRS: {dados.eixo_qrs}°")
        
        if dados.intervalos:
            linhas.append(f"Intervalo PR: {dados.intervalos.pr:.3f} s")
            linhas.append(f"Duração do QRS: {dados.intervalos.qrs:.3f} s")
            linhas.append(f"Intervalo QT: {dados.intervalos.qt:.3f} s")
            linhas.append(f"QTc (corrigido): {dados.intervalos.qtc:.3f} s")
        
        linhas.append("")
        
        # Achados
        linhas.append("ACHADOS ELETROCARDIOGRÁFICOS")
        linhas.append("-" * 80)
        if resultado["achados"]:
            for achado in resultado["achados"]:
                linhas.append(f"• {achado}")
        else:
            linhas.append("• Sem alterações significativas")
        linhas.append("")
        
        # Diagnósticos
        linhas.append("DIAGNÓSTICOS")
        linhas.append("-" * 80)
        if resultado["diagnosticos"]:
            for i, diag in enumerate(resultado["diagnosticos"], 1):
                linhas.append(f"{i}. {diag}")
        else:
            linhas.append("• ECG dentro dos padrões de normalidade")
        linhas.append("")
        
        # Conclusão
        linhas.append("CONCLUSÃO")
        linhas.append("-" * 80)
        linhas.append(resultado["conclusao"])
        linhas.append("")
        
        # Alertas especiais
        if dados.infarto or dados.isquemia:
            linhas.append("")
            linhas.append("!" * 80)
            linhas.append("ATENÇÃO: ACHADOS QUE NECESSITAM AVALIAÇÃO MÉDICA IMEDIATA")
            linhas.append("!" * 80)
        
        linhas.append("")
        linhas.append("=" * 80)
        linhas.append("Laudo gerado automaticamente pelo Sistema de Acessibilidade Médica")
        linhas.append("Este laudo deve ser revisado por um médico cardiologista")
        linhas.append("=" * 80)
        
        return "\n".join(linhas)
    
    def _formatar_laudo_audio(self, dados: DadosECG, resultado: Dict) -> str:
        """Formata o laudo para narração em áudio (conciso e otimizado)"""
        
        partes = []
        
        # Introdução com identificação
        if dados.nome_paciente:
            partes.append(f"E C G de {dados.nome_paciente}.")
        else:
            partes.append("Laudo de eletrocardiograma.")
        
        # Dados principais compactos
        partes.append(f"Ritmo {self._formatar_ritmo(dados.ritmo)}, {dados.regularidade}, {dados.frequencia_cardiaca} B P M.")
        
        # Intervalos - mencionar valores específicos importantes
        intervalos_info = []
        if dados.intervalos:
            # PR sempre mencionado
            pr_ms = int(dados.intervalos.pr * 1000)
            if dados.intervalos.pr < 0.12:
                intervalos_info.append(f"P R curto, {pr_ms} milissegundos")
            elif dados.intervalos.pr > 0.20:
                intervalos_info.append(f"P R prolongado, {pr_ms} milissegundos")
            else:
                intervalos_info.append(f"P R {pr_ms} milissegundos")
            
            # QRS sempre mencionado
            qrs_ms = int(dados.intervalos.qrs * 1000)
            if dados.intervalos.qrs > 0.12:
                intervalos_info.append(f"Q R S alargado, {qrs_ms} milissegundos")
            elif dados.intervalos.qrs > 0.10:
                intervalos_info.append(f"Q R S {qrs_ms} milissegundos, limítrofe")
            else:
                intervalos_info.append(f"Q R S {qrs_ms} milissegundos")
            
            # QTc apenas se alterado
            if dados.intervalos.qtc > 0.44:
                intervalos_info.append(f"Q T c prolongado")
        
        if intervalos_info:
            partes.append(". ".join(intervalos_info) + ".")
        
        # Eixo elétrico sempre mencionado
        eixo = dados.eixo_qrs
        if eixo < -30:
            partes.append(f"Eixo desviado à esquerda, {eixo} graus.")
        elif eixo > 90:
            partes.append(f"Eixo desviado à direita, {eixo} graus.")
        else:
            partes.append(f"Eixo normal, {eixo} graus.")
        
        # Diagnósticos com contexto
        if resultado["diagnosticos"]:
            # Adicionar morfologia se relevante
            if dados.complexo_qrs and dados.complexo_qrs.morfologia != 'normal':
                morfologia = dados.complexo_qrs.morfologia
                if morfologia == "RSR'":
                    partes.append("Morfologia Q R S: padrão R S R linha em V1 e V2.")
            
            # Adicionar morfologia de onda P se alterada
            if dados.onda_p and dados.onda_p.morfologia != 'normal':
                if 'aumentada' in dados.onda_p.morfologia.lower():
                    partes.append("Onda P: aumentada, sugerindo sobrecarga atrial.")
            
            if len(resultado["diagnosticos"]) == 1:
                partes.append(f"Diagnóstico: {resultado['diagnosticos'][0]}.")
            else:
                # Até 3 diagnósticos
                partes.append("Diagnósticos: " + ". ".join(resultado["diagnosticos"][:3]) + ".")
        else:
            partes.append("E C G dentro dos limites normais.")
        
        # Alertas críticos
        if dados.infarto:
            partes.append("ATENÇÃO! Infarto agudo. Avaliação médica imediata!")
        elif dados.isquemia:
            partes.append("Atenção: isquemia miocárdica. Avaliação cardiológica urgente.")
        
        return " ".join(partes)
    
    def _formatar_ritmo(self, ritmo: str) -> str:
        """Converte o código do ritmo para descrição legível"""
        ritmos = {
            "sinusal": "sinusal",
            "fibrilacao_atrial": "fibrilação atrial",
            "flutter_atrial": "flutter atrial",
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
        
        return f"{len(resultado['diagnosticos'])} alterações encontradas"
