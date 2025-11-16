"""
Serviço de geração de áudio com cache
"""
from typing import Optional

import config
from audio_generator import AudioLaudoGenerator
from services.audio_cache_service import AudioCacheService


class AudioService:
    """Serviço para geração e gerenciamento de áudio com cache inteligente"""
    
    def __init__(self):
        self.gerador_audio = AudioLaudoGenerator()
        self.cache_service = AudioCacheService()
    
    def gerar_audio(self, texto: str, identificador: Optional[str] = None, usar_cache: bool = True) -> str:
        """
        Gera arquivo de áudio a partir de texto (usa cache se disponível)
        
        Args:
            texto: Texto para converter em áudio
            identificador: Identificador opcional para o áudio (facilita debug)
            usar_cache: Se True, verifica cache antes de gerar (padrão: True)
            
        Returns:
            Caminho do arquivo de áudio gerado (relativo: audio/filename.mp3)
        """
        if usar_cache:
            # Usa sistema de cache (verifica se já existe)
            audio_path = self.cache_service.gerar_ou_obter_audio(texto, identificador)
        else:
            # Gera sem cache (sempre novo)
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
