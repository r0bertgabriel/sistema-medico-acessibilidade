"""
Serviço de geração de áudio
"""
from typing import Optional

import config
from audio_generator import AudioLaudoGenerator


class AudioService:
    """Serviço para geração e gerenciamento de áudio"""
    
    def __init__(self):
        self.gerador_audio = AudioLaudoGenerator()
    
    def gerar_audio(self, texto: str) -> str:
        """
        Gera arquivo de áudio a partir de texto
        
        Args:
            texto: Texto para converter em áudio
            
        Returns:
            Caminho do arquivo de áudio gerado
        """
        audio_path = self.gerador_audio.gerar_audio_laudo(texto)
        return audio_path
    
    def limpar_audios_antigos(self, max_files: Optional[int] = None) -> None:
        """
        Remove arquivos de áudio antigos
        
        Args:
            max_files: Número máximo de arquivos a manter
        """
        if max_files is None:
            max_files = config.MAX_AUDIO_FILES
        
        self.gerador_audio.limpar_audios_antigos(max_files)
