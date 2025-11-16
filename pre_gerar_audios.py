#!/usr/bin/env python3
"""
Script para pré-gerar áudios de todos os exemplos
Executa na inicialização do sistema para cachear áudios
"""
import sys
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from data.ecg_examples import obter_todos_exemplos
from services.audio_cache_service import AudioCacheService
from services.ecg_service import ECGService
from services.hemograma_service import HemogramaService


def pre_gerar_audios_ecg(cache_service: AudioCacheService):
    """Pré-gera áudios de todos os exemplos de ECG"""
    print("\n" + "="*60)
    print("🫀 PRÉ-GERANDO ÁUDIOS DE ECG")
    print("="*60)
    
    ecg_service = ECGService()
    exemplos = obter_todos_exemplos()
    
    total = len(exemplos)
    gerados = 0
    cache_hits = 0
    
    for nome, dados_ecg in exemplos.items():
        print(f"\n📊 Processando: {nome}")
        print(f"   Paciente: {dados_ecg.nome_paciente}")
        
        try:
            # Converter para dict
            dados_dict = dados_ecg.to_dict()
            
            # Analisar ECG
            resultado = ecg_service.analisar_ecg(dados_dict)
            
            # Identificador para cache
            identificador = f"ecg_{nome}"
            
            # Verificar se já está em cache
            cached = cache_service.verificar_cache(resultado['laudo_audio_texto'])
            
            if cached:
                cache_hits += 1
                print(f"   ✅ Já existe em cache: {cached}")
            else:
                # Gerar áudio
                audio_path = cache_service.pre_gerar_audio(
                    resultado['laudo_audio_texto'],
                    identificador
                )
                gerados += 1
                print(f"   🎤 Áudio gerado: {audio_path}")
        
        except Exception as e:
            print(f"   ❌ Erro: {e}")
    
    print("\n📈 Resumo ECG:")
    print(f"   Total: {total}")
    print(f"   Gerados: {gerados}")
    print(f"   Cache hits: {cache_hits}")


def pre_gerar_audios_hemograma(cache_service: AudioCacheService):
    """Pré-gera áudios de todos os exemplos de Hemograma"""
    print("\n" + "="*60)
    print("🩸 PRÉ-GERANDO ÁUDIOS DE HEMOGRAMA")
    print("="*60)
    
    tipos_exemplos = ['normal', 'anemia', 'leucocitose', 'plaquetopenia']
    
    total = len(tipos_exemplos)
    gerados = 0
    cache_hits = 0
    
    for tipo in tipos_exemplos:
        print(f"\n📊 Processando: {tipo}")
        
        try:
            # Obter exemplo
            exemplo = HemogramaService.obter_exemplo_hemograma(tipo)
            print(f"   Paciente: {exemplo['paciente']['nome']}")
            
            # Processar hemograma
            identificador = f"hemograma_{tipo}"
            resultado = HemogramaService.processar_hemograma(exemplo, identificador)
            
            if not resultado.get('sucesso'):
                print(f"   ❌ Erro ao processar: {resultado.get('mensagem')}")
                continue
            
            # Verificar se já estava em cache (verificando logs)
            # O AudioService já faz essa verificação internamente
            
            if resultado.get('audio_filename'):
                print(f"   ✅ Áudio disponível: {resultado['audio_filename']}")
                gerados += 1
            else:
                print("   ⚠️ Nenhum áudio gerado")
        
        except Exception as e:
            print(f"   ❌ Erro: {e}")
    
    print("\n📈 Resumo Hemograma:")
    print(f"   Total: {total}")
    print(f"   Processados: {gerados}")


def main():
    """Função principal"""
    print("="*60)
    print("🎤 GERADOR DE CACHE DE ÁUDIOS")
    print("="*60)
    print("\nEste script pré-gera áudios de todos os exemplos para")
    print("que não precisem ser gerados toda vez que forem acessados.\n")
    
    # Criar serviço de cache
    cache_service = AudioCacheService()
    
    # Mostrar estatísticas iniciais
    stats = cache_service.estatisticas_cache()
    print("📊 Estatísticas Iniciais:")
    print(f"   Arquivos no cache: {stats['total_arquivos']}")
    print(f"   Entradas no índice: {stats['total_indice']}")
    print(f"   Tamanho total: {stats['tamanho_mb']} MB")
    print(f"   Diretório: {stats['cache_dir']}")
    
    # Pré-gerar áudios de ECG
    pre_gerar_audios_ecg(cache_service)
    
    # Pré-gerar áudios de Hemograma
    pre_gerar_audios_hemograma(cache_service)
    
    # Mostrar estatísticas finais
    print("\n" + "="*60)
    stats_final = cache_service.estatisticas_cache()
    print("📊 Estatísticas Finais:")
    print(f"   Arquivos no cache: {stats_final['total_arquivos']}")
    print(f"   Entradas no índice: {stats_final['total_indice']}")
    print(f"   Tamanho total: {stats_final['tamanho_mb']} MB")
    print(f"   Novos áudios: {stats_final['total_arquivos'] - stats['total_arquivos']}")
    
    print("\n✅ Pré-geração de áudios concluída!")
    print("="*60)


if __name__ == "__main__":
    main()
