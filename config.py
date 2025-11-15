"""
Configurações da aplicação
"""
import os
from pathlib import Path

# Diretório base da aplicação
BASE_DIR = Path(__file__).parent

# Configurações do Flask
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

# Configurações de áudio
AUDIO_DIR = BASE_DIR / 'static' / 'audio'
MAX_AUDIO_FILES = 50  # Número máximo de arquivos de áudio a manter
AUDIO_SPEED = 1.35  # Velocidade de reprodução do áudio

# Configurações de TTS
TTS_LANGUAGE = 'es'
TTS_TLD = 'com'  # Top-level domain para espanhol

# Configurações de acessibilidade
KEYBOARD_SHORTCUTS_ENABLED = True
AUDIO_FEEDBACK_ENABLED = True

# Configurações OpenAI GPT-4o Vision
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
OPENAI_MODEL = 'gpt-4o'  # Modelo com capacidade de visão

# Configurações de upload de imagens
UPLOAD_FOLDER = BASE_DIR / 'static' / 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max
