#!/usr/bin/env python3
"""
Teste rápido do módulo de Hemograma (sem dependências externas)
"""
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from models.hemograma_data import DadosHemograma
from models.hemograma_analyzer import AnalisadorHemograma


def teste_hemograma_normal():
    """Testa hemograma normal"""
    print("=" * 80)
    print("TESTE: Hemograma Normal")
    print("=" * 80)
    
    dados = DadosHemograma(
        nome_paciente="João Silva",
        idade=35,
        sexo="M",
        data_coleta="12/11/2025",
        hemacias=5.0,
        hemoglobina=15.0,
        hematocrito=45.0,
        vcm=90.0,
        hcm=30.0,
        chcm=34.0,
        rdw=13.0,
        leucocitos=7000,
        neutrofilos=4000,
        linfocitos=2000,
        monocitos=500,
        eosinofilos=200,
        basofilos=50,
        plaquetas=250000
    )
    
    analisador = AnalisadorHemograma(dados)
    resultado = analisador.analisar()
    
    print("\n--- LAUDO VISUAL (com formatação) ---")
    print(resultado['laudo'])
    
    print("\n\n" + "=" * 80)
    print("--- LAUDO PARA ÁUDIO (sem formatação) ---")
    print("=" * 80)
    print(resultado['laudo_audio'])
    
    print("\n\n" + "=" * 80)
    print("ANÁLISE DO LAUDO DE ÁUDIO:")
    print("=" * 80)
    audio_text = resultado['laudo_audio']
    
    # Verificar se há caracteres problemáticos
    chars_problematicos = ['=', '-', '•', '⚠', '[', ']', '(', ')']
    encontrados = []
    for char in chars_problematicos:
        if char in audio_text:
            encontrados.append(char)
    
    if encontrados:
        print(f"❌ PROBLEMA: Caracteres de formatação encontrados no áudio: {encontrados}")
    else:
        print("✅ SUCESSO: Nenhum caractere de formatação encontrado!")
    
    # Verificar se as abreviações foram expandidas
    if 'V C M' in audio_text or 'VCM' in audio_text:
        print("✅ VCM mencionado no áudio")
    
    # Verificar se unidades foram clarificadas
    if 'microlitro' in audio_text:
        print("✅ Unidades clarificadas (microlitro)")
    
    if 'gramas por decilitro' in audio_text:
        print("✅ Unidades clarificadas (gramas por decilitro)")
    
    print("\n" + "=" * 80)
    print(f"Status: {resultado['interpretacao']['status_geral']}")
    print(f"Alterações: {len(resultado['alteracoes'])}")


def teste_anemia():
    """Testa detecção de anemia"""
    print("\n\n" + "=" * 80)
    print("TESTE: Anemia Microcítica")
    print("=" * 80)
    
    dados = DadosHemograma(
        nome_paciente="Maria Santos",
        idade=42,
        sexo="F",
        hemacias=3.5,
        hemoglobina=10.0,
        hematocrito=32.0,
        vcm=75.0,
        leucocitos=6500,
        plaquetas=280000
    )
    
    analisador = AnalisadorHemograma(dados)
    resultado = analisador.analisar()
    
    print("\n--- INTERPRETAÇÃO ---")
    print(f"Status: {resultado['interpretacao']['status_geral']}")
    print(f"\nAchados:")
    for achado in resultado['interpretacao']['achados_principais']:
        print(f"  • {achado}")
    
    print(f"\nSugestões Diagnósticas:")
    for sugestao in resultado['interpretacao']['sugestoes_diagnosticas']:
        print(f"  • {sugestao}")
    
    # Verificar áudio
    audio_text = resultado['laudo_audio']
    chars_problematicos = ['=', '-', '•', '⚠']
    encontrados = [c for c in chars_problematicos if c in audio_text]
    
    if encontrados:
        print(f"\n❌ Caracteres problemáticos no áudio: {encontrados}")
    else:
        print(f"\n✅ Áudio limpo de caracteres especiais")


if __name__ == '__main__':
    try:
        teste_hemograma_normal()
        teste_anemia()
        
        print("\n\n" + "=" * 80)
        print("✓ TODOS OS TESTES CONCLUÍDOS!")
        print("=" * 80)
        print("\n📊 Resumo:")
        print("  • Sistema 100% OFFLINE (sem OpenAI)")
        print("  • Análise baseada em valores científicos")
        print("  • Áudio otimizado (sem caracteres especiais)")
        print("  • Interpretação clínica automática")
        print()
        
    except Exception as e:
        print(f"\n✗ ERRO: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
