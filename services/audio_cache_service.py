"""
Serviço de Cache de Áudio para reutilização de arquivos gerados
"""
import hashlib
import json
import re
from pathlib import Path
from typing import Optional

from audio_generator import AudioLaudoGenerator


class AudioCacheService:
    """Serviço para gerenciar cache de áudios gerados
    
    - Gera hash MD5 do texto para identificação única
    - Verifica se áudio já existe antes de gerar novo
    - Remove caracteres especiais do texto antes de gerar áudio
    - Mantém índice de cache em JSON para rápida consulta
    """
    
    def __init__(self, audio_dir: str = "static/audio", cache_index_file: str = "audio_cache_index.json"):
        """Inicializa o serviço de cache
        
        Args:
            audio_dir: Diretório onde os áudios são armazenados
            cache_index_file: Arquivo JSON para índice do cache
        """
        self.audio_dir = Path(audio_dir)
        self.audio_dir.mkdir(parents=True, exist_ok=True)
        
        self.cache_index_path = self.audio_dir / cache_index_file
        self.cache_index = self._carregar_indice()
        self.gerador_audio = AudioLaudoGenerator(audio_dir=audio_dir)
    
    def _carregar_indice(self) -> dict:
        """Carrega índice de cache do arquivo JSON"""
        if self.cache_index_path.exists():
            try:
                with open(self.cache_index_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Erro ao carregar índice de cache: {e}")
                return {}
        return {}
    
    def _salvar_indice(self):
        """Salva índice de cache no arquivo JSON"""
        try:
            with open(self.cache_index_path, 'w', encoding='utf-8') as f:
                json.dump(self.cache_index, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ Erro ao salvar índice de cache: {e}")
    
    def _limpar_texto_para_audio(self, texto: str) -> str:
        """Remove caracteres especiais do texto para geração de áudio
        
        Mantém apenas letras, números, espaços e pontuação básica
        
        Args:
            texto: Texto original com formatação
            
        Returns:
            Texto limpo para conversão em áudio
        """
        # Remove linhas de separação (=== ou --- ou ━━━)
        texto = re.sub(r'^[=\-━]{3,}$', '', texto, flags=re.MULTILINE)
        
        # Remove caracteres especiais de formatação mas mantém pontuação
        texto = re.sub(r'[•●○◦▪▫►▸▹‣⦿⦾]', '', texto)  # Remove bullets
        texto = re.sub(r'[│├└┌┐┘┴┬┤┼━]', '', texto)  # Remove box drawing
        texto = re.sub(r'[↑↓→←↔]', '', texto)  # Remove setas
        
        # Remove múltiplos espaços e linhas vazias
        texto = re.sub(r'\n{3,}', '\n\n', texto)  # Max 2 linhas vazias
        texto = re.sub(r' {2,}', ' ', texto)  # Max 1 espaço
        
        # Remove espaços no início/fim de cada linha
        linhas = [linha.strip() for linha in texto.split('\n')]
        texto = '\n'.join(linhas)
        
        return texto.strip()
    
    def _gerar_hash(self, texto: str) -> str:
        """Gera hash MD5 do texto para usar como identificador
        
        Args:
            texto: Texto para gerar hash
            
        Returns:
            Hash MD5 em hexadecimal (32 caracteres)
        """
        texto_limpo = self._limpar_texto_para_audio(texto)
        return hashlib.md5(texto_limpo.encode('utf-8')).hexdigest()
    
    def verificar_cache(self, texto: str) -> Optional[str]:
        """Verifica se existe áudio em cache para o texto
        
        Args:
            texto: Texto do laudo
            
        Returns:
            Caminho relativo do áudio se existir, None caso contrário
        """
        texto_hash = self._gerar_hash(texto)
        
        # Verificar no índice
        if texto_hash in self.cache_index:
            audio_filename = self.cache_index[texto_hash]
            audio_path = self.audio_dir / audio_filename
            
            # Verificar se arquivo realmente existe
            if audio_path.exists():
                print(f"✅ Cache HIT: {audio_filename}")
                return f"audio/{audio_filename}"
            else:
                # Arquivo não existe, remover do índice
                print(f"⚠️ Arquivo de cache não encontrado: {audio_filename}")
                del self.cache_index[texto_hash]
                self._salvar_indice()
        
        print("❌ Cache MISS: gerando novo áudio")
        return None
    
    def gerar_ou_obter_audio(self, texto: str, identificador: Optional[str] = None) -> str:
        """Gera novo áudio ou retorna do cache se já existir
        
        Args:
            texto: Texto completo do laudo
            identificador: Identificador opcional para o áudio (ex: "ecg_normal", "hemograma_anemia")
            
        Returns:
            Caminho relativo do arquivo de áudio
        """
        # Verificar cache primeiro
        cached_audio = self.verificar_cache(texto)
        if cached_audio:
            return cached_audio
        
        # Não está em cache, gerar novo áudio
        texto_hash = self._gerar_hash(texto)
        
        # Nome do arquivo baseado no hash + identificador opcional
        if identificador:
            # Remove caracteres inválidos do identificador
            identificador = re.sub(r'[^\w\-]', '_', identificador)
            filename = f"{identificador}_{texto_hash[:8]}.mp3"
        else:
            filename = f"laudo_{texto_hash[:8]}.mp3"
        
        # Limpar texto para áudio
        texto_limpo = self._limpar_texto_para_audio(texto)
        
        # Gerar áudio
        print(f"🎤 Gerando novo áudio: {filename}")
        audio_path = self.gerador_audio.gerar_audio_laudo(
            texto_limpo, 
            filename=filename,
            acelerar=True
        )
        
        # Adicionar ao índice
        self.cache_index[texto_hash] = filename
        self._salvar_indice()
        
        print(f"✅ Áudio gerado e salvo no cache: {filename}")
        return audio_path
    
    def pre_gerar_audio(self, texto: str, identificador: str) -> str:
        """Pré-gera áudio para um texto específico (usado na inicialização)
        
        Args:
            texto: Texto do laudo
            identificador: Identificador único (ex: "ecg_normal", "hemograma_leucocitose")
            
        Returns:
            Caminho relativo do arquivo de áudio
        """
        return self.gerar_ou_obter_audio(texto, identificador)
    
    def limpar_cache_antigo(self, dias: int = 7):
        """Remove áudios do cache com mais de X dias
        
        Args:
            dias: Número de dias para considerar áudio como antigo
        """
        import time
        
        limite_tempo = time.time() - (dias * 24 * 60 * 60)
        arquivos_removidos = 0
        
        for audio_file in self.audio_dir.glob("*.mp3"):
            if audio_file.stat().st_mtime < limite_tempo:
                try:
                    # Remove do índice se existir
                    for hash_key, filename in list(self.cache_index.items()):
                        if filename == audio_file.name:
                            del self.cache_index[hash_key]
                    
                    # Remove arquivo
                    audio_file.unlink()
                    arquivos_removidos += 1
                    print(f"🗑️ Removido: {audio_file.name}")
                except Exception as e:
                    print(f"⚠️ Erro ao remover {audio_file.name}: {e}")
        
        if arquivos_removidos > 0:
            self._salvar_indice()
            print(f"✅ {arquivos_removidos} arquivos antigos removidos do cache")
    
    def estatisticas_cache(self) -> dict:
        """Retorna estatísticas do cache
        
        Returns:
            Dicionário com estatísticas
        """
        total_arquivos = len(list(self.audio_dir.glob("*.mp3")))
        total_indice = len(self.cache_index)
        
        # Calcular tamanho total
        tamanho_total = sum(f.stat().st_size for f in self.audio_dir.glob("*.mp3"))
        tamanho_mb = tamanho_total / (1024 * 1024)
        
        return {
            "total_arquivos": total_arquivos,
            "total_indice": total_indice,
            "tamanho_mb": round(tamanho_mb, 2),
            "cache_dir": str(self.audio_dir)
        }
