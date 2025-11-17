#!/usr/bin/env python3
"""
Teste de Performance do Cache de Áudio

Demonstra que áudios pré-gerados são reutilizados instantaneamente
sem necessidade de regeneração.
"""
import time

from data.ecg_examples import obter_todos_exemplos
from services.audio_cache_service import AudioCacheService
from services.ecg_service import ECGService


def test_cache_performance():
    """Testa performance do cache (cache HIT vs geração nova)"""
    print("="*70)
    print("🧪 TESTE DE PERFORMANCE DO CACHE DE ÁUDIO")
    print("="*70)
    
    cache_service = AudioCacheService()
    ecg_service = ECGService()
    exemplos = obter_todos_exemplos()
    
    # Pegar primeiro exemplo (normal)
    exemplo_nome = list(exemplos.keys())[0]
    exemplo_dados = exemplos[exemplo_nome]
    
    print(f"\n📊 Testando com: {exemplo_nome}")
    print(f"   Paciente: {exemplo_dados.nome_paciente}")
    
    # Converter para dict e gerar laudo
    dados_dict = exemplo_dados.to_dict()
    resultado = ecg_service.analisar_ecg(dados_dict)
    identificador = f"ecg_{exemplo_nome}"
    
    print("\n" + "-"*70)
    print("🔹 PRIMEIRA CHAMADA (verifica cache)")
    print("-"*70)
    
    inicio = time.time()
    audio_path_1 = cache_service.gerar_ou_obter_audio(
        resultado['laudo_audio_texto'],
        identificador
    )
    tempo_1 = time.time() - inicio
    
    print(f"   Tempo: {tempo_1*1000:.2f}ms")
    print(f"   Arquivo: {audio_path_1}")
    
    print("\n" + "-"*70)
    print("🔹 SEGUNDA CHAMADA (cache HIT - deve ser INSTANTÂNEO)")
    print("-"*70)
    
    inicio = time.time()
    audio_path_2 = cache_service.gerar_ou_obter_audio(
        resultado['laudo_audio_texto'],
        identificador
    )
    tempo_2 = time.time() - inicio
    
    print(f"   Tempo: {tempo_2*1000:.2f}ms")
    print(f"   Arquivo: {audio_path_2}")
    
    print("\n" + "="*70)
    print("📊 RESULTADOS")
    print("="*70)
    
    if tempo_2 < 0.1:  # Menos de 100ms
        print(f"✅ Cache funcionando perfeitamente!")
        print(f"   1ª chamada: {tempo_1*1000:.1f}ms")
        print(f"   2ª chamada: {tempo_2*1000:.1f}ms (cache HIT)")
        print(f"   Melhoria: {(tempo_1/tempo_2):.0f}x mais rápido")
    else:
        print(f"⚠️  Cache pode não estar otimizado")
        print(f"   1ª chamada: {tempo_1*1000:.1f}ms")
        print(f"   2ª chamada: {tempo_2*1000:.1f}ms")
    
    print("\n💡 CONCLUSÃO:")
    print("   Quando você clica em 'Gerar Laudo' na interface,")
    print("   o sistema RECUPERA o áudio em ~1-10ms (cache HIT),")
    print("   sem necessidade de chamar gTTS ou processar novamente.")
    print("="*70)

if __name__ == '__main__':
    test_cache_performance()
