#!/usr/bin/env python3
"""
Script de verificação de dependências do sistema
Verifica se todas as dependências necessárias estão instaladas
"""

import importlib.util
import subprocess
import sys


def verificar_python():
    """Verifica a versão do Python"""
    version = sys.version_info
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("  ⚠️  Recomendado Python 3.8 ou superior")
        return False
    return True


def verificar_modulo(nome, nome_pip=None):
    """Verifica se um módulo Python está instalado"""
    if nome_pip is None:
        nome_pip = nome
    
    spec = importlib.util.find_spec(nome)
    if spec is not None:
        print(f"✓ {nome_pip}")
        return True
    else:
        print(f"✗ {nome_pip} - Execute: pip install {nome_pip}")
        return False


def verificar_ffmpeg():
    """Verifica se FFmpeg está instalado"""
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✓ FFmpeg - {version_line}")
            return True
    except FileNotFoundError:
        print("✗ FFmpeg não encontrado")
        print("  ℹ️  OPCIONAL - Sistema funcionará sem FFmpeg")
        print("  ℹ️  Áudios serão gerados em velocidade normal")
        
        if sys.platform == "win32":
            print("\n  Instalação no Windows:")
            print("  1. Via Chocolatey: choco install ffmpeg")
            print("  2. Manual: Veja INSTALACAO_FFMPEG_WINDOWS.md")
            print("  3. Download: https://www.gyan.dev/ffmpeg/builds/")
        else:
            print("\n  Instalação no Linux:")
            print("  - Ubuntu/Debian: sudo apt install ffmpeg")
            print("  - Fedora: sudo dnf install ffmpeg")
            print("  - Arch: sudo pacman -S ffmpeg")
        return False
    except Exception as e:
        print(f"✗ Erro ao verificar FFmpeg: {e}")
        return False


def main():
    """Executa todas as verificações"""
    print("=" * 60)
    print("VERIFICAÇÃO DE DEPENDÊNCIAS - Sistema Médico")
    print("=" * 60)
    print()
    
    # Verificar Python
    print("Python:")
    python_ok = verificar_python()
    print()
    
    # Verificar módulos Python
    print("Módulos Python:")
    modulos = {
        'flask': 'flask',
        'gtts': 'gtts',
        'pygame': 'pygame',
        'pydub': 'pydub',
    }
    
    modulos_ok = []
    for modulo, nome_pip in modulos.items():
        modulos_ok.append(verificar_modulo(modulo, nome_pip))
    print()
    
    # Verificar FFmpeg
    print("Ferramentas Externas:")
    ffmpeg_ok = verificar_ffmpeg()
    print()
    
    # Resumo
    print("=" * 60)
    print("RESUMO")
    print("=" * 60)
    
    todos_modulos_ok = all(modulos_ok)
    
    if python_ok and todos_modulos_ok:
        print("✓ Sistema pronto para uso!")
        if not ffmpeg_ok:
            print("  ℹ️  FFmpeg não instalado - áudios sem aceleração")
    else:
        print("✗ Instale as dependências faltantes:")
        print("  pip install -r requirements.txt")
    
    print()
    
    return 0 if (python_ok and todos_modulos_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
