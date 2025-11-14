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
    
    def _gerar_onda_p(self, tempo, fc, posicao):
        """Gera onda P (contração atrial)"""
        duracao = 0.08  # 80ms
        amplitude = 0.15
        t_p = tempo - posicao
        return amplitude * np.exp(-((t_p / (duracao/4)) ** 2)) * (np.abs(t_p) < duracao)
    
    def _gerar_complexo_qrs(self, tempo, fc, posicao, amplitude_qrs=1.0):
        """Gera complexo QRS (despolarização ventricular)"""
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
                           amplitude_qrs=1.0, tem_arritmia=False):
        """
        Gera sinal de ECG sintético
        
        Args:
            frequencia_cardiaca: FC em bpm
            duracao: Duração do traçado em segundos
            amplitude_qrs: Amplitude do complexo QRS (0.5 a 1.5)
            tem_arritmia: Se True, adiciona batimentos irregulares
        
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
        while batimento_pos < duracao:
            # Adicionar arritmia (variação no intervalo RR)
            if tem_arritmia and np.random.random() < 0.15:
                variacao = np.random.uniform(0.7, 1.4)
                intervalo = rr_interval * variacao
            else:
                intervalo = rr_interval * np.random.uniform(0.95, 1.05)
            
            # Gerar ondas do batimento
            sinal += self._gerar_onda_p(tempo, frequencia_cardiaca, batimento_pos + 0.08)
            sinal += self._gerar_complexo_qrs(tempo, frequencia_cardiaca, 
                                              batimento_pos + 0.16, amplitude_qrs)
            sinal += self._gerar_onda_t(tempo, frequencia_cardiaca, batimento_pos + 0.36)
            
            batimento_pos += intervalo
        
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
        info_texto = (
            f"Paciente: {dados_paciente.get('nome_paciente', 'N/A')}\n"
            f"FC: {dados_paciente.get('frequencia_cardiaca', 'N/A')} bpm | "
            f"Idade: {dados_paciente.get('idade', 'N/A')} anos | "
            f"Sexo: {dados_paciente.get('sexo', 'N/A')}\n"
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
        
        # Determinar amplitude QRS baseado em achados
        amplitude_qrs = 1.0
        achados = dados_ecg.get('achados', {})
        
        if achados.get('hipertrofia_ventricular_esquerda'):
            amplitude_qrs = 1.4  # QRS mais amplo
        elif achados.get('baixa_voltagem_qrs'):
            amplitude_qrs = 0.5  # QRS de baixa amplitude
        
        # Detectar arritmia
        tem_arritmia = (
            achados.get('fibrilacao_atrial') or 
            achados.get('extrassistoles') or
            fc < 50 or fc > 100
        )
        
        # Gerar sinal
        tempo, sinal = self.gerar_ecg_sintetico(
            frequencia_cardiaca=fc,
            duracao=10,
            amplitude_qrs=amplitude_qrs,
            tem_arritmia=tem_arritmia
        )
        
        # Gerar hash único para o arquivo
        dados_str = f"{fc}_{amplitude_qrs}_{tem_arritmia}_{datetime.now().timestamp()}"
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
