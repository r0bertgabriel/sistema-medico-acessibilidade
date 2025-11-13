"""
Módulo de Text-to-Speech para geração de áudio dos laudos
Adaptado do test-tts.py para integração web com aceleração de áudio
"""
import uuid
from pathlib import Path

import gtts
import pygame

# Importação condicional do pydub para compatibilidade com Python 3.13
try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except (ImportError, ModuleNotFoundError):
    PYDUB_AVAILABLE = False
    print("⚠️  Aviso: pydub não disponível. Aceleração de áudio desabilitada.")
    print("   Para habilitar aceleração, use Python 3.8-3.12 ou instale dependências.")


class AudioLaudoGenerator:
    """Gera arquivos de áudio a partir de laudos de texto com velocidade acelerada"""
    
    def __init__(self, audio_dir: str = "static/audio", speed: float = 1.35):
        """
        Inicializa o gerador de áudio
        
        Args:
            audio_dir: Diretório onde os arquivos de áudio serão salvos
            speed: Velocidade do áudio (1.35 = 1.35x mais rápido para melhor compreensão)
        """
        self.audio_dir = Path(audio_dir)
        self.audio_dir.mkdir(parents=True, exist_ok=True)
        self.lang = "pt-br"
        self.speed = speed
        self.pydub_available = PYDUB_AVAILABLE
    
    def gerar_audio_laudo(self, texto: str, filename: str | None = None, acelerar: bool = True) -> str:
        """
        Gera arquivo de áudio a partir do texto do laudo
        
        Args:
            texto: Texto do laudo para converter em áudio
            filename: Nome do arquivo (opcional, será gerado se não fornecido)
            acelerar: Se True, acelera o áudio para 1.5x (padrão: True)
        
        Returns:
            Caminho relativo do arquivo de áudio gerado
        """
        if not filename:
            filename = f"laudo_{uuid.uuid4().hex[:8]}.mp3"
        
        # Garantir extensão .mp3
        if not filename.endswith('.mp3'):
            filename += '.mp3'
        
        # Caminho para arquivo temporário (sem aceleração)
        temp_filename = f"temp_{filename}"
        temp_filepath = self.audio_dir / temp_filename
        final_filepath = self.audio_dir / filename
        
        # Gerar áudio com gTTS
        tts = gtts.gTTS(texto, lang=self.lang, slow=False)
        tts.save(str(temp_filepath))
        
        # Acelerar o áudio se solicitado e pydub estiver disponível
        if acelerar and self.pydub_available:
            try:
                audio = AudioSegment.from_mp3(str(temp_filepath))
                
                # Acelerar mantendo o pitch (tom) original
                # speedup_factor: quanto maior, mais rápido
                sped_up_audio = audio.speedup(playback_speed=self.speed)
                
                # Salvar áudio acelerado
                sped_up_audio.export(str(final_filepath), format="mp3")
                
                # Remover arquivo temporário
                temp_filepath.unlink()
            except Exception as e:
                print(f"⚠️  Erro ao acelerar áudio: {e}. Usando áudio sem aceleração.")
                if temp_filepath.exists():
                    temp_filepath.rename(final_filepath)
        else:
            # Se não acelerar ou pydub não disponível, apenas renomear
            if acelerar and not self.pydub_available:
                print("ℹ️  Aceleração de áudio não disponível (pydub não instalado)")
            temp_filepath.rename(final_filepath)
        
        # Retornar caminho relativo para uso no HTML
        return f"audio/{filename}"
    
    def reproduzir_audio(self, filepath: str):
        """
        Reproduz um arquivo de áudio (útil para testes)
        
        Args:
            filepath: Caminho completo do arquivo de áudio
        """
        pygame.mixer.init()
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)
    
    def limpar_audios_antigos(self, max_files: int = 50):
        """
        Remove arquivos de áudio mais antigos se houver muitos arquivos
        
        Args:
            max_files: Número máximo de arquivos a manter
        """
        audio_files = sorted(
            self.audio_dir.glob("laudo_*.mp3"),
            key=lambda f: f.stat().st_mtime,
            reverse=True
        )
        
        # Remove arquivos excedentes
        for audio_file in audio_files[max_files:]:
            try:
                audio_file.unlink()
            except Exception as e:
                print(f"Erro ao remover arquivo {audio_file}: {e}")
    
    def remover_audio(self, filename: str):
        """
        Remove um arquivo de áudio específico
        
        Args:
            filename: Nome do arquivo a remover
        """
        filepath = self.audio_dir / filename
        if filepath.exists():
            filepath.unlink()


# Função auxiliar para uso rápido
def gerar_audio_rapido(texto: str, output_dir: str = "static/audio") -> str:
    """
    Função auxiliar para gerar áudio rapidamente
    
    Args:
        texto: Texto para converter
        output_dir: Diretório de saída
    
    Returns:
        Caminho relativo do arquivo gerado
    """
    generator = AudioLaudoGenerator(output_dir)
    return generator.gerar_audio_laudo(texto)
