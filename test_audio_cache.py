#!/usr/bin/env python3
"""
Script de teste para verificar o sistema de cache de áudio
"""
import sys
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from services.audio_cache_service import AudioCacheService


def test_cache_basico():
    """Testa funcionalidade básica do cache"""
    print("\n" + "="*60)
    print("🧪 TESTE 1: Funcionalidade Básica do Cache")
    print("="*60)
    
    cache = AudioCacheService()
    
    # Texto de teste
    texto_teste = """
    INFORME DE ELECTROCARDIOGRAMA
    ========================================
    
    Paciente: João Silva
    Edad: 35 años
    
    Ritmo: sinusal
    Frecuencia: 75 lpm
    
    HALLAZGOS:
    • Ritmo sinusal regular
    • Eje eléctrico normal
    • Sin alteraciones significativas
    
    CONCLUSIÓN:
    ECG dentro de los límites normales
    """
    
    print("\n📝 Texto de teste preparado")
    print(f"   Tamanho: {len(texto_teste)} caracteres")
    
    # Primeira geração (deve criar novo áudio)
    print("\n🎤 Tentativa 1: Gerando áudio...")
    audio_path_1 = cache.gerar_ou_obter_audio(texto_teste, "teste_cache_1")
    print(f"   ✅ Áudio gerado: {audio_path_1}")
    
    # Segunda geração (deve usar cache)
    print("\n🎤 Tentativa 2: Gerando mesmo áudio...")
    audio_path_2 = cache.gerar_ou_obter_audio(texto_teste, "teste_cache_2")
    print(f"   ✅ Áudio obtido: {audio_path_2}")
    
    # Verificar se são iguais
    if audio_path_1 == audio_path_2:
        print("\n✅ SUCESSO: Cache funcionando! Mesmo arquivo foi reutilizado.")
    else:
        print("\n⚠️ AVISO: Arquivos diferentes foram gerados")
        print(f"   Path 1: {audio_path_1}")
        print(f"   Path 2: {audio_path_2}")


def test_limpeza_texto():
    """Testa remoção de caracteres especiais"""
    print("\n" + "="*60)
    print("🧪 TESTE 2: Limpeza de Caracteres Especiais")
    print("="*60)
    
    cache = AudioCacheService()
    
    # Texto com muitos caracteres especiais
    texto_original = """
    ============================================
    INFORME DE ECG
    ============================================
    
    ● Hallazgo 1
    ● Hallazgo 2
    ● Hallazgo 3
    
    ↑ Elevado
    ↓ Disminuido
    → Normal
    
    ━━━━━━━━━━━━━━━━━━━━━━
    """
    
    texto_limpo = cache._limpar_texto_para_audio(texto_original)
    
    print("\n📝 Texto Original:")
    print(texto_original[:200] + "...")
    print(f"\n   Tamanho: {len(texto_original)} caracteres")
    
    print("\n🧹 Texto Limpo:")
    print(texto_limpo[:200] + "...")
    print(f"\n   Tamanho: {len(texto_limpo)} caracteres")
    print(f"   Redução: {len(texto_original) - len(texto_limpo)} caracteres")
    
    # Verificar se removeu caracteres especiais
    caracteres_removidos = ['●', '↑', '↓', '→', '━']
    encontrados = [c for c in caracteres_removidos if c in texto_limpo]
    
    if not encontrados:
        print("\n✅ SUCESSO: Todos os caracteres especiais foram removidos")
    else:
        print(f"\n⚠️ AVISO: Ainda existem caracteres especiais: {encontrados}")


def test_hash_consistente():
    """Testa se o hash é consistente para textos iguais"""
    print("\n" + "="*60)
    print("🧪 TESTE 3: Consistência do Hash")
    print("="*60)
    
    cache = AudioCacheService()
    
    texto = "Teste de hash consistente para o sistema de cache"
    
    # Gerar hash múltiplas vezes
    hash1 = cache._gerar_hash(texto)
    hash2 = cache._gerar_hash(texto)
    hash3 = cache._gerar_hash(texto)
    
    print(f"\n📝 Texto: {texto}")
    print(f"\n🔑 Hashes gerados:")
    print(f"   Hash 1: {hash1}")
    print(f"   Hash 2: {hash2}")
    print(f"   Hash 3: {hash3}")
    
    if hash1 == hash2 == hash3:
        print("\n✅ SUCESSO: Hashes são consistentes")
    else:
        print("\n❌ ERRO: Hashes são diferentes!")


def test_cache_multiplos_textos():
    """Testa cache com múltiplos textos diferentes"""
    print("\n" + "="*60)
    print("🧪 TESTE 4: Cache com Múltiplos Textos")
    print("="*60)
    
    cache = AudioCacheService()
    
    textos = {
        "ecg_normal": "ECG normal. Ritmo sinusal. 75 lpm.",
        "ecg_taquicardia": "ECG con taquicardia. Ritmo sinusal. 110 lpm.",
        "hemograma_normal": "Hemograma normal. Todos los parámetros normales.",
        "hemograma_anemia": "Hemograma con anemia. Hemoglobina baja.",
    }
    
    paths = {}
    
    print("\n🎤 Gerando áudios...")
    for identificador, texto in textos.items():
        path = cache.gerar_ou_obter_audio(texto, identificador)
        paths[identificador] = path
        print(f"   {identificador}: {path}")
    
    # Tentar novamente (deve usar cache)
    print("\n🔄 Tentando gerar novamente (deve usar cache)...")
    for identificador, texto in textos.items():
        path = cache.gerar_ou_obter_audio(texto, identificador)
        if path == paths[identificador]:
            print(f"   ✅ {identificador}: Cache HIT")
        else:
            print(f"   ❌ {identificador}: Cache MISS (não deveria acontecer)")


def test_estatisticas():
    """Testa função de estatísticas"""
    print("\n" + "="*60)
    print("🧪 TESTE 5: Estatísticas do Cache")
    print("="*60)
    
    cache = AudioCacheService()
    stats = cache.estatisticas_cache()
    
    print("\n📊 Estatísticas:")
    print(f"   Total de arquivos: {stats['total_arquivos']}")
    print(f"   Total no índice: {stats['total_indice']}")
    print(f"   Tamanho total: {stats['tamanho_mb']} MB")
    print(f"   Diretório: {stats['cache_dir']}")
    
    if stats['total_arquivos'] >= 0 and stats['total_indice'] >= 0:
        print("\n✅ SUCESSO: Estatísticas obtidas com sucesso")
    else:
        print("\n❌ ERRO: Valores inválidos nas estatísticas")


def main():
    """Executa todos os testes"""
    print("="*60)
    print("🧪 TESTES DO SISTEMA DE CACHE DE ÁUDIO")
    print("="*60)
    
    try:
        test_cache_basico()
        test_limpeza_texto()
        test_hash_consistente()
        test_cache_multiplos_textos()
        test_estatisticas()
        
        print("\n" + "="*60)
        print("✅ TODOS OS TESTES CONCLUÍDOS")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ ERRO DURANTE OS TESTES: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
