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
        
        IMPORTANTE: Com cache ativado, áudios pré-gerados são reutilizados instantaneamente.
        Isso significa que clicar em "Gerar Laudo" apenas reproduz o áudio já existente,
        sem necessidade de regeneração (otimização para demonstração/produção).
        
        Args:
            texto: Texto para converter em áudio
            identificador: Identificador opcional para o áudio (facilita debug)
            usar_cache: Se True, verifica cache antes de gerar (padrão: True)
            
        Returns:
            Caminho do arquivo de áudio gerado (relativo: audio/filename.mp3)
        """
        if usar_cache:
            # Usa sistema de cache (verifica se já existe - INSTANTÂNEO se pré-gerado)
            audio_path = self.cache_service.gerar_ou_obter_audio(texto, identificador)
        else:
            # Gera sem cache (sempre novo - não recomendado em produção)
            audio_path = self.gerador_audio.gerar_audio_laudo(texto)
        
        return audio_path
    
    def limpar_audios_antigos(self, max_files: Optional[int] = None, dias: int = 7) -> None:
        """
        Remove arquivos de áudio antigos (sincronizado com cache)
        
        Args:
            max_files: Número máximo de arquivos a manter (None = usar config)
            dias: Remover arquivos com mais de X dias do cache
        """
        if max_files is None:
            max_files = config.MAX_AUDIO_FILES
        
        # Limpar cache antigo (atualiza índice corretamente)
        self.cache_service.limpar_cache_antigo(dias=dias)
        
        # Depois limpar por quantidade máxima
        self.gerador_audio.limpar_audios_antigos(max_files)
