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
TTS_LANGUAGE = 'pt'
TTS_TLD = 'com.br'  # Top-level domain para sotaque brasileiro

# Configurações de acessibilidade
KEYBOARD_SHORTCUTS_ENABLED = True
AUDIO_FEEDBACK_ENABLED = True
