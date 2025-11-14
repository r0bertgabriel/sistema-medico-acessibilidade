"""
Serviço para geração de imagens de eletrocardiograma (ECG)
Gera visualizações sintéticas baseadas nos dados de entrada
"""
import matplotlib
import numpy as np

matplotlib.use('Agg')  # Backend não-interativo para servidor
import hashlib
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt


class ECGImageGenerator:
    """
    Gera imagens de ECG sintéticas baseadas nos parâmetros fornecidos
    """
    
    def __init__(self, output_dir='static/ecg_images'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def _gerar_onda_p(self, tempo, fc, posicao, morfologia='normal'):
        """Gera onda P (contração atrial)"""
        if morfologia == 'aumentada':
            # Onda P aumentada (sobrecarga atrial)
            # Componente atrial direito (mais alta e pontuda)
            duracao1 = 0.06
            amplitude1 = 0.25  # Aumentada em amplitude
            t_p1 = tempo - posicao
            onda_p1 = amplitude1 * np.exp(-((t_p1 / (duracao1/4)) ** 2)) * (np.abs(t_p1) < duracao1)
            
            # Componente atrial esquerdo (prolongado)
            duracao2 = 0.08
            amplitude2 = 0.20
            t_p2 = tempo - (posicao + 0.04)
            onda_p2 = amplitude2 * np.exp(-((t_p2 / (duracao2/4)) ** 2)) * (np.abs(t_p2) < duracao2)
            
            return onda_p1 + onda_p2  # Onda P bifásica e prolongada
        else:
            duracao = 0.08  # 80ms
            amplitude = 0.15
            t_p = tempo - posicao
            return amplitude * np.exp(-((t_p / (duracao/4)) ** 2)) * (np.abs(t_p) < duracao)
    
    def _gerar_complexo_qrs(self, tempo, fc, posicao, amplitude_qrs=1.0, morfologia='normal'):
        """Gera complexo QRS (despolarização ventricular)"""
        if morfologia == 'RSR':  # Bloqueio de ramo direito incompleto
            # Onda R pequena
            r_pos = posicao - 0.01
            r = 0.3 * amplitude_qrs * np.exp(-((tempo - r_pos) / 0.015) ** 2)
            
            # Onda S
            s_pos = posicao + 0.01
            s = -0.4 * amplitude_qrs * np.exp(-((tempo - s_pos) / 0.015) ** 2)
            
            # Onda R' (segunda onda R - padrão RSR')
            r_prime_pos = posicao + 0.03
            r_prime = 0.5 * amplitude_qrs * np.exp(-((tempo - r_prime_pos) / 0.02) ** 2)
            
            return r + s + r_prime
        else:
            # Onda Q (pequena deflexão negativa)
            q_pos = posicao - 0.02
            q = -0.1 * amplitude_qrs * np.exp(-((tempo - q_pos) / 0.01) ** 2)
            
            # Onda R (grande deflexão positiva)
            r_pos = posicao
            r = amplitude_qrs * np.exp(-((tempo - r_pos) / 0.02) ** 2)
            
            # Onda S (deflexão negativa após R)
            s_pos = posicao + 0.02
            s = -0.2 * amplitude_qrs * np.exp(-((tempo - s_pos) / 0.01) ** 2)
            
            return q + r + s
    
    def _gerar_onda_t(self, tempo, fc, posicao):
        """Gera onda T (repolarização ventricular)"""
        duracao = 0.16  # 160ms
        amplitude = 0.3
        t_t = tempo - posicao
        return amplitude * np.exp(-((t_t / (duracao/3)) ** 2)) * (np.abs(t_t) < duracao)
    
    def _adicionar_ruido(self, sinal, nivel=0.02):
        """Adiciona ruído realista ao sinal"""
        ruido = np.random.normal(0, nivel, len(sinal))
        return sinal + ruido
    
    def _adicionar_baseline_wander(self, sinal, tempo, frequencia=0.5):
        """Adiciona oscilação da linha de base (respiração)"""
        baseline = 0.05 * np.sin(2 * np.pi * frequencia * tempo)
        return sinal + baseline
    
    def gerar_ecg_sintetico(self, frequencia_cardiaca, duracao=10, 
                           amplitude_qrs=1.0, tem_arritmia=False, morfologia_qrs='normal',
                           variacao_pp=None, onda_p_morfologia='normal'):
        """
        Gera sinal de ECG sintético
        
        Args:
            frequencia_cardiaca: FC em bpm
            duracao: Duração do traçado em segundos
            amplitude_qrs: Amplitude do complexo QRS (0.5 a 1.5)
            tem_arritmia: Se True, adiciona batimentos irregulares
            morfologia_qrs: 'normal' ou 'RSR' (bloqueio de ramo direito)
            variacao_pp: Variação específica do intervalo P-P (para arritmia sinusal)
            onda_p_morfologia: 'normal' ou 'aumentada' (sobrecarga atrial)
        
        Returns:
            tuple: (tempo, sinal_ecg)
        """
        # Taxa de amostragem (500 Hz é padrão em ECG)
        fs = 500
        tempo = np.linspace(0, duracao, int(duracao * fs))
        sinal = np.zeros_like(tempo)
        
        # Intervalo RR (tempo entre batimentos)
        rr_interval = 60.0 / frequencia_cardiaca
        
        # Posições dos batimentos
        batimento_pos = 0
        contador_batimento = 0
        while batimento_pos < duracao:
            # Adicionar arritmia (variação no intervalo RR)
            if variacao_pp is not None:
                # Arritmia sinusal com variação específica (respiratória)
                # Cria padrão cíclico de aceleração/desaceleração
                variacao = 1.0 + 0.2 * np.sin(2 * np.pi * contador_batimento / 8)
                intervalo = rr_interval * variacao
            elif tem_arritmia and np.random.random() < 0.15:
                variacao = np.random.uniform(0.7, 1.4)
                intervalo = rr_interval * variacao
            else:
                intervalo = rr_interval * np.random.uniform(0.95, 1.05)
            
            # Gerar ondas do batimento
            sinal += self._gerar_onda_p(tempo, frequencia_cardiaca, batimento_pos + 0.08,
                                        morfologia=onda_p_morfologia)
            sinal += self._gerar_complexo_qrs(tempo, frequencia_cardiaca, 
                                              batimento_pos + 0.16, amplitude_qrs,
                                              morfologia=morfologia_qrs)
            sinal += self._gerar_onda_t(tempo, frequencia_cardiaca, batimento_pos + 0.36)
            
            batimento_pos += intervalo
            contador_batimento += 1
        
        # Adicionar efeitos realistas
        sinal = self._adicionar_baseline_wander(sinal, tempo)
        sinal = self._adicionar_ruido(sinal, nivel=0.02)
        
        return tempo, sinal
    
    def plotar_ecg(self, tempo, sinal, dados_paciente, filepath):
        """
        Plota e salva o ECG em arquivo
        
        Args:
            tempo: Array de tempo
            sinal: Array do sinal ECG
            dados_paciente: Dict com informações do paciente
            filepath: Caminho para salvar a imagem
        """
        # Configurar figura
        fig, ax = plt.subplots(figsize=(14, 6), facecolor='#fff8f0')
        ax.set_facecolor('#fff8f0')
        
        # Grid de ECG (quadriculado médico)
        ax.grid(True, which='major', linestyle='-', linewidth=0.8, color='#ff9999', alpha=0.5)
        ax.grid(True, which='minor', linestyle='-', linewidth=0.4, color='#ffcccc', alpha=0.3)
        ax.minorticks_on()
        
        # Plotar sinal
        ax.plot(tempo, sinal, color='#000000', linewidth=1.2)
        
        # Configurações dos eixos
        ax.set_xlabel('Tempo (s)', fontsize=11, fontweight='bold')
        ax.set_ylabel('Amplitude (mV)', fontsize=11, fontweight='bold')
        ax.set_title('ELETROCARDIOGRAMA (ECG)', fontsize=14, fontweight='bold', pad=15)
        
        # Limites
        ax.set_xlim(0, tempo[-1])
        ax.set_ylim(-0.8, 1.5)
        
        # Informações do paciente
        nome = dados_paciente.get('nome_paciente', 'N/A')
        fc = dados_paciente.get('frequencia_cardiaca', 'N/A')
        ritmo = dados_paciente.get('ritmo', 'N/A')
        
        info_texto = (
            f"Paciente: {nome}\n"
            f"FC: {fc} bpm | Ritmo: {ritmo}\n"
            f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        )
        
        ax.text(0.02, 0.98, info_texto, transform=ax.transAxes,
                fontsize=9, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='gray'))
        
        # Calibração (10mm = 1mV, 5mm = 0.2s)
        ax.text(0.98, 0.02, '1 mV | 0.2 s', transform=ax.transAxes,
                fontsize=8, ha='right', va='bottom',
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
        
        plt.tight_layout()
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close(fig)
    
    def gerar_imagem_ecg(self, dados_ecg):
        """
        Gera imagem de ECG a partir dos dados
        
        Args:
            dados_ecg: Dict com dados do ECG
            
        Returns:
            str: Caminho relativo da imagem gerada
        """
        # Extrair parâmetros
        fc = dados_ecg.get('frequencia_cardiaca', 75)
        nome_paciente = dados_ecg.get('nome_paciente', '')
        bloqueio_ramo = dados_ecg.get('bloqueio_ramo', '')
        regularidade = dados_ecg.get('regularidade', 'regular')
        ritmo = dados_ecg.get('ritmo', 'Sinusal')
        
        # Determinar morfologia QRS baseado em bloqueio de ramo
        morfologia_qrs = 'normal'
        if bloqueio_ramo and 'direito' in bloqueio_ramo.lower():
            morfologia_qrs = 'RSR'  # Padrão RSR' para bloqueio de ramo direito
        
        # Determinar morfologia da onda P
        onda_p_morfologia = 'normal'
        onda_p_info = dados_ecg.get('onda_p', {})
        if isinstance(onda_p_info, dict):
            p_morfologia = onda_p_info.get('morfologia', 'normal')
            if 'aumentada' in p_morfologia.lower() or 'sobrecarga' in nome_paciente.lower():
                onda_p_morfologia = 'aumentada'
        
        # Determinar amplitude QRS baseado em achados
        amplitude_qrs = 1.0
        achados = dados_ecg.get('achados', {})
        
        if achados.get('hipertrofia_ventricular_esquerda'):
            amplitude_qrs = 1.4  # QRS mais amplo
        elif achados.get('baixa_voltagem_qrs'):
            amplitude_qrs = 0.5  # QRS de baixa amplitude
        
        # Detectar tipo de arritmia
        tem_arritmia = (
            achados.get('fibrilacao_atrial') or 
            achados.get('extrassistoles') or
            fc < 50 or fc > 100
        )
        
        # Arritmia sinusal específica (variação respiratória)
        variacao_pp = None
        if regularidade == 'irregular' or 'arritmia' in nome_paciente.lower():
            variacao_pp = True  # Ativa variação P-P característica
        
        # Gerar sinal
        tempo, sinal = self.gerar_ecg_sintetico(
            frequencia_cardiaca=fc,
            duracao=10,
            amplitude_qrs=amplitude_qrs,
            tem_arritmia=tem_arritmia,
            morfologia_qrs=morfologia_qrs,
            variacao_pp=variacao_pp,
            onda_p_morfologia=onda_p_morfologia
        )
        
        # Gerar hash único para o arquivo
        dados_str = f"{fc}_{amplitude_qrs}_{tem_arritmia}_{morfologia_qrs}_{datetime.now().timestamp()}"
        hash_nome = hashlib.md5(dados_str.encode()).hexdigest()[:12]
        
        # Nome do arquivo
        filename = f"ecg_{hash_nome}.png"
        filepath = self.output_dir / filename
        
        # Plotar e salvar
        self.plotar_ecg(tempo, sinal, dados_ecg, filepath)
        
        # Retornar caminho relativo
        return f"ecg_images/{filename}"
    
    def limpar_imagens_antigas(self, dias=7):
        """Remove imagens mais antigas que N dias"""
        import time
        limite_tempo = time.time() - (dias * 86400)
        
        for arquivo in self.output_dir.glob('ecg_*.png'):
            if arquivo.stat().st_mtime < limite_tempo:
                arquivo.unlink()
                print(f"🗑️ Imagem antiga removida: {arquivo.name}")


# Instância global
ecg_image_generator = ECGImageGenerator()
