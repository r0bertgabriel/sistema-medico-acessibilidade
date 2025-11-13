#!/usr/bin/env python3
"""
Teste simples do módulo de Hemograma
"""
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from models.hemograma_analyzer import AnalisadorHemograma
from models.hemograma_data import DadosHemograma


def teste_simples():
    """Teste básico de hemograma normal"""
    print("\n" + "=" * 80)
    print("TESTE SIMPLES: Hemograma Normal")
    print("=" * 80 + "\n")
    
    # Criar dados de teste
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
    
    print("📋 Dados do Paciente:")
    print(f"   Nome: {dados.nome_paciente}")
    print(f"   Idade: {dados.idade} anos")
    print(f"   Sexo: {dados.sexo}")
    print()
    
    # Analisar
    print("🔬 Analisando hemograma...")
    analisador = AnalisadorHemograma(dados)
    resultado = analisador.analisar()
    
    # Verificar resultado
    print("\n✅ Análise concluída!")
    print(f"   Status: {resultado['interpretacao']['status_geral']}")
    print(f"   Alterações detectadas: {len(resultado['alteracoes'])}")
    print()
    
    # Mostrar laudo visual
    print("=" * 80)
    print("LAUDO VISUAL (com formatação):")
    print("=" * 80)
    print(resultado['laudo'][:500])  # Primeiros 500 caracteres
    print("... (continuação omitida)")
    print()
    
    # Mostrar laudo de áudio
    print("=" * 80)
    print("LAUDO PARA ÁUDIO (sem caracteres especiais):")
    print("=" * 80)
    print(resultado['laudo_audio'][:500])  # Primeiros 500 caracteres
    print("... (continuação omitida)")
    print()
    
    # Verificar diferenças
    tem_formatacao_visual = any(c in resultado['laudo'] for c in ['=', '-', '│', '┌', '└'])
    tem_formatacao_audio = any(c in resultado['laudo_audio'] for c in ['=', '-', '│', '┌', '└'])
    
    print("=" * 80)
    print("VERIFICAÇÃO:")
    print("=" * 80)
    print(f"✓ Laudo visual tem formatação: {tem_formatacao_visual}")
    print(f"✓ Laudo áudio SEM formatação: {not tem_formatacao_audio}")
    print()
    
    if not tem_formatacao_audio:
        print("✅ SUCESSO! O laudo de áudio está limpo, sem caracteres especiais!")
    else:
        print("⚠️ ATENÇÃO! O laudo de áudio ainda tem caracteres especiais.")
    
    print()
    return 0


if __name__ == '__main__':
    try:
        sys.exit(teste_simples())
    except Exception as e:
        print(f"\n❌ ERRO: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
