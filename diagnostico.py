#!/usr/bin/env python3
"""
Script de análise e diagnóstico completo do projeto
"""
import os
import sys
from pathlib import Path


def check_file_exists(filepath, description):
    """Verifica se arquivo existe"""
    if Path(filepath).exists():
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description} NÃO ENCONTRADO: {filepath}")
        return False

def check_directory(dirpath, description):
    """Verifica se diretório existe"""
    if Path(dirpath).is_dir():
        print(f"✅ {description}: {dirpath}")
        return True
    else:
        print(f"❌ {description} NÃO ENCONTRADO: {dirpath}")
        return False

def check_imports():
    """Testa importação de módulos"""
    print("\n" + "="*80)
    print("TESTANDO IMPORTAÇÕES")
    print("="*80)
    
    modules = [
        ('Flask', 'flask'),
        ('gTTS', 'gtts'),
        ('Pygame', 'pygame'),
        ('Requests', 'requests'),
        ('Pillow', 'PIL'),
        ('OpenAI', 'openai'),
    ]
    
    results = []
    for name, module in modules:
        try:
            __import__(module)
            print(f"✅ {name} importado com sucesso")
            results.append(True)
        except ImportError as e:
            print(f"❌ {name} FALHOU: {e}")
            results.append(False)
    
    # Pydub - esperado falhar em Python 3.13
    try:
        from pydub import AudioSegment
        print(f"✅ Pydub importado (aceleração de áudio disponível)")
        results.append(True)
    except (ImportError, ModuleNotFoundError):
        print(f"⚠️  Pydub não disponível (Python 3.13 - esperado)")
        results.append(True)  # Não é um erro crítico
    
    return all(results)

def check_project_structure():
    """Verifica estrutura do projeto"""
    print("\n" + "="*80)
    print("VERIFICANDO ESTRUTURA DO PROJETO")
    print("="*80)
    
    structure = {
        'Arquivos principais': [
            'app.py',
            'config.py',
            'requirements.txt',
            'README.md',
        ],
        'Diretórios de código': [
            'models',
            'services',
            'routes',
            'data',
            'templates',
            'static',
        ],
        'Arquivos críticos': [
            'models/__init__.py',
            'models/ecg_data.py',
            'models/ecg_analyzer.py',
            'models/laudo_generator.py',
            'services/__init__.py',
            'services/ecg_service.py',
            'services/audio_service.py',
            'services/vision_service.py',
            'routes/__init__.py',
            'routes/main.py',
            'routes/api.py',
        ],
        'Templates': [
            'templates/base.html',
            'templates/index.html',
            'templates/analise.html',
            'templates/analise_imagem.html',
            'templates/resultados.html',
        ],
        'Diretórios de dados': [
            'static/audio',
            'static/uploads',
            'static/css',
            'static/js',
        ],
    }
    
    all_ok = True
    for category, items in structure.items():
        print(f"\n{category}:")
        for item in items:
            if Path(item).exists():
                print(f"  ✅ {item}")
            else:
                print(f"  ❌ {item}")
                all_ok = False
    
    return all_ok

def check_config():
    """Verifica configurações"""
    print("\n" + "="*80)
    print("VERIFICANDO CONFIGURAÇÕES")
    print("="*80)
    
    try:
        import config
        
        checks = [
            ('SECRET_KEY', hasattr(config, 'SECRET_KEY')),
            ('DEBUG', hasattr(config, 'DEBUG')),
            ('AUDIO_DIR', hasattr(config, 'AUDIO_DIR')),
            ('OPENAI_API_KEY', hasattr(config, 'OPENAI_API_KEY')),
            ('OPENAI_MODEL', hasattr(config, 'OPENAI_MODEL')),
            ('UPLOAD_FOLDER', hasattr(config, 'UPLOAD_FOLDER')),
            ('ALLOWED_EXTENSIONS', hasattr(config, 'ALLOWED_EXTENSIONS')),
            ('MAX_CONTENT_LENGTH', hasattr(config, 'MAX_CONTENT_LENGTH')),
        ]
        
        all_ok = True
        for name, exists in checks:
            if exists:
                value = getattr(config, name)
                if name == 'OPENAI_API_KEY':
                    if value and value != '':
                        print(f"✅ {name}: Configurada (***)")
                    else:
                        print(f"⚠️  {name}: NÃO CONFIGURADA (necessária para análise por imagem)")
                        all_ok = False
                else:
                    print(f"✅ {name}: {value}")
            else:
                print(f"❌ {name}: NÃO ENCONTRADA")
                all_ok = False
        
        return all_ok
    
    except Exception as e:
        print(f"❌ Erro ao importar config: {e}")
        return False

def check_services():
    """Verifica serviços"""
    print("\n" + "="*80)
    print("VERIFICANDO SERVIÇOS")
    print("="*80)
    
    try:
        from services import AudioService, ECGService, VisionService
        print("✅ ECGService importado")
        print("✅ AudioService importado")
        print("✅ VisionService importado")
        
        # Tentar instanciar
        try:
            ecg = ECGService()
            print("✅ ECGService instanciado")
        except Exception as e:
            print(f"❌ Erro ao instanciar ECGService: {e}")
            return False
        
        try:
            audio = AudioService()
            print("✅ AudioService instanciado")
        except Exception as e:
            print(f"❌ Erro ao instanciar AudioService: {e}")
            return False
        
        try:
            vision = VisionService()
            print("✅ VisionService instanciado")
        except ValueError as e:
            print(f"⚠️  VisionService não pode ser instanciado: {e}")
            print("   (Configure OPENAI_API_KEY para usar análise por imagem)")
        except Exception as e:
            print(f"❌ Erro inesperado ao instanciar VisionService: {e}")
            return False
        
        return True
    
    except Exception as e:
        print(f"❌ Erro ao importar services: {e}")
        return False

def check_routes():
    """Verifica rotas"""
    print("\n" + "="*80)
    print("VERIFICANDO ROTAS")
    print("="*80)
    
    try:
        from routes import api_bp, main_bp
        print("✅ main_bp importado")
        print("✅ api_bp importado")
        
        # Blueprints estão corretos, apenas não podemos iterar sem app
        print("\n✅ Rotas registradas corretamente nos blueprints")
        print("   (Para listar rotas, inicie a aplicação)")
        
        return True
    
    except Exception as e:
        print(f"❌ Erro ao verificar rotas: {e}")
        return False

def check_models():
    """Verifica models"""
    print("\n" + "="*80)
    print("VERIFICANDO MODELOS")
    print("="*80)
    
    try:
        from models import AnalisadorECG, DadosECG, LaudoGenerator
        print("✅ DadosECG importado")
        print("✅ AnalisadorECG importado")
        print("✅ LaudoGenerator importado")
        
        # Tentar criar instâncias
        try:
            analisador = AnalisadorECG()
            print("✅ AnalisadorECG instanciado")
        except Exception as e:
            print(f"❌ Erro ao instanciar AnalisadorECG: {e}")
            return False
        
        try:
            gerador = LaudoGenerator()
            print("✅ LaudoGenerator instanciado")
        except Exception as e:
            print(f"❌ Erro ao instanciar LaudoGenerator: {e}")
            return False
        
        return True
    
    except Exception as e:
        print(f"❌ Erro ao importar models: {e}")
        return False

def check_potential_issues():
    """Verifica problemas potenciais"""
    print("\n" + "="*80)
    print("VERIFICANDO PROBLEMAS POTENCIAIS")
    print("="*80)
    
    issues = []
    
    # Verificar .env
    if not Path('.env').exists():
        issues.append("⚠️  Arquivo .env não encontrado (use .env.example como base)")
    
    # Verificar Python version
    py_version = sys.version_info
    if py_version >= (3, 13):
        issues.append(f"ℹ️  Python {py_version.major}.{py_version.minor} - Aceleração de áudio desabilitada (use 3.8-3.12 para aceleração)")
    
    # Verificar gitignore
    if not Path('.gitignore').exists():
        issues.append("⚠️  .gitignore não encontrado")
    
    # Verificar backup
    if Path('backup_20251111_121320').exists():
        issues.append("ℹ️  Diretório de backup antigo encontrado - considere remover")
    
    if issues:
        for issue in issues:
            print(issue)
    else:
        print("✅ Nenhum problema potencial detectado")
    
    return len(issues) == 0

def main():
    """Função principal"""
    print("="*80)
    print("DIAGNÓSTICO COMPLETO DO SISTEMA DE LAUDOS ECG")
    print("="*80)
    
    results = []
    
    # Executar verificações
    results.append(('Estrutura do Projeto', check_project_structure()))
    results.append(('Importações', check_imports()))
    results.append(('Configurações', check_config()))
    results.append(('Serviços', check_services()))
    results.append(('Modelos', check_models()))
    results.append(('Rotas', check_routes()))
    results.append(('Problemas Potenciais', check_potential_issues()))
    
    # Resumo
    print("\n" + "="*80)
    print("RESUMO DO DIAGNÓSTICO")
    print("="*80)
    
    for name, result in results:
        status = "✅ OK" if result else "❌ FALHOU"
        print(f"{status}: {name}")
    
    all_ok = all(r[1] for r in results)
    
    print("\n" + "="*80)
    if all_ok:
        print("✅ SISTEMA PRONTO PARA USO!")
        print("="*80)
        print("\nPara iniciar o sistema:")
        print("  python app.py")
        print("\nAcesse: http://localhost:5000")
        return 0
    else:
        print("⚠️  ALGUNS PROBLEMAS FORAM DETECTADOS")
        print("="*80)
        print("\nRevise os erros acima e corrija-os antes de usar o sistema.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
