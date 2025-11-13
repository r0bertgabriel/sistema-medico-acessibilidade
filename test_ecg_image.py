"""
Teste do gerador de imagens de ECG
"""
from services.ecg_image_generator import ECGImageGenerator

# Criar gerador
generator = ECGImageGenerator()

# Dados de teste
dados_teste = {
    'nome_paciente': 'João da Silva',
    'idade': 45,
    'sexo': 'M',
    'frequencia_cardiaca': 75,
    'achados': {
        'ritmo_sinusal': True,
        'hipertrofia_ventricular_esquerda': False,
        'fibrilacao_atrial': False,
        'extrassistoles': False
    }
}

print("🔬 Testando geração de imagem de ECG...")
print(f"📋 Paciente: {dados_teste['nome_paciente']}")
print(f"❤️  FC: {dados_teste['frequencia_cardiaca']} bpm")

try:
    # Gerar imagem
    caminho_imagem = generator.gerar_imagem_ecg(dados_teste)
    print(f"✅ Imagem gerada com sucesso!")
    print(f"📁 Caminho: static/{caminho_imagem}")
    
    # Verificar se o arquivo existe
    from pathlib import Path
    arquivo = Path('static') / caminho_imagem
    if arquivo.exists():
        tamanho = arquivo.stat().st_size / 1024  # KB
        print(f"📊 Tamanho: {tamanho:.2f} KB")
        print(f"✅ Arquivo criado corretamente!")
    else:
        print(f"❌ ERRO: Arquivo não encontrado em {arquivo}")
        
except Exception as e:
    print(f"❌ ERRO ao gerar imagem: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("Teste concluído!")
print("="*60)
