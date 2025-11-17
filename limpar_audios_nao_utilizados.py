#!/usr/bin/env python3
"""
Script para limpar áudios não utilizados do sistema
Remove arquivos MP3 que não correspondem aos exemplos ativos
"""
import json
from pathlib import Path


def limpar_audios_nao_utilizados():
    """Remove áudios que não são usados pelos exemplos atuais"""
    
    audio_dir = Path("static/audio")
    index_file = audio_dir / "audio_cache_index.json"
    
    # Prefixos dos exemplos que DEVEM ser mantidos
    exemplos_validos = {
        # ECG (3 exemplos)
        "ecg_normal",
        "ecg_arritmia_sinusal",
        "ecg_bloqueio_ramo",
        
        # Hemograma (4 exemplos usados no app.py)
        "hemograma_normal",
        "hemograma_anemia",
        "hemograma_leucocitose",
        "hemograma_plaquetopenia",
    }
    
    print("🧹 Limpando áudios não utilizados...")
    print(f"📁 Diretório: {audio_dir.absolute()}")
    print(f"✅ Exemplos válidos: {len(exemplos_validos)}")
    
    # Carregar índice
    with open(index_file, 'r', encoding='utf-8') as f:
        cache_index = json.load(f)
    
    print(f"📊 Cache atual: {len(cache_index)} entradas")
    
    # Identificar arquivos a remover
    removidos = 0
    mantidos = 0
    novo_index = {}
    
    for hash_key, filename in cache_index.items():
        # Extrair prefixo do nome do arquivo (antes do hash)
        # Formato: "ecg_normal_15c79282.mp3" ou "hemograma_anemia_efdb25f2.mp3"
        prefix = "_".join(filename.split("_")[:-1])
        
        # Verificar se é um arquivo válido
        eh_valido = any(prefix.startswith(valido) for valido in exemplos_validos)
        
        if eh_valido:
            novo_index[hash_key] = filename
            mantidos += 1
            print(f"  ✅ Mantido: {filename}")
        else:
            # Remover arquivo MP3
            filepath = audio_dir / filename
            if filepath.exists():
                filepath.unlink()
                print(f"  🗑️  Removido: {filename}")
                removidos += 1
    
    # Remover TODOS os arquivos MP3 órfãos (não no índice)
    print("\n🔍 Procurando arquivos órfãos (não indexados)...")
    arquivos_orfaos = 0
    for mp3_file in audio_dir.glob("*.mp3"):
        if mp3_file.name not in novo_index.values():
            mp3_file.unlink()
            print(f"  🗑️  Órfão removido: {mp3_file.name}")
            arquivos_orfaos += 1
    
    if arquivos_orfaos == 0:
        print("  ✅ Nenhum arquivo órfão encontrado")
    
    # Atualizar índice
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(novo_index, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*70)
    print("✅ Limpeza concluída!")
    print(f"   📊 Arquivos mantidos: {mantidos}")
    print(f"   🗑️  Arquivos removidos (indexados): {removidos}")
    print(f"   🗑️  Arquivos removidos (órfãos): {arquivos_orfaos}")
    print(f"   🗑️  Total removido: {removidos + arquivos_orfaos}")
    print(f"   📝 Índice atualizado: {len(novo_index)} entradas")
    print("="*70)


if __name__ == "__main__":
    limpar_audios_nao_utilizados()
