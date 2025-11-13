#!/usr/bin/env python3
"""
Teste da API de Hemograma
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from services.hemograma_service import HemogramaService


def teste_api():
    """Testa o serviço de hemograma como se fosse uma chamada da API"""
    print("\n" + "=" * 80)
    print("TESTE: Serviço de Hemograma (simulando API)")
    print("=" * 80 + "\n")
    
    # Dados de exemplo
    dados_json = {
        "paciente": {
            "nome": "Maria Santos",
            "idade": 42,
            "sexo": "F",
            "data_coleta": "12/11/2025"
        },
        "serie_vermelha": {
            "hemacias": 3.5,
            "hemoglobina": 10.0,
            "hematocrito": 32.0,
            "vcm": 75.0,
            "hcm": 25.0,
            "chcm": 32.0,
            "rdw": 16.5
        },
        "serie_branca": {
            "leucocitos": 6500,
            "neutrofilos": 3500,
            "linfocitos": 2200,
            "monocitos": 450,
            "eosinofilos": 180,
            "basofilos": 40
        },
        "plaquetas": {
            "contagem": 280000
        },
        "observacoes": "Paciente refere fadiga e palidez."
    }
    
    print("📋 Validando dados...")
    validacao = HemogramaService.validar_dados(dados_json)
    print(f"   Válido: {validacao['valido']}")
    
    if not validacao['valido']:
        print("   ❌ Erros:")
        for erro in validacao['erros']:
            print(f"      - {erro}")
        return 1
    
    print("   ✅ Dados válidos!")
    print()
    
    print("🔬 Processando hemograma...")
    print("   ⚠️  Nota: Geração de áudio desabilitada para este teste")
    print()
    
    # Processar sem áudio (para teste rápido)
    from models.hemograma_analyzer import AnalisadorHemograma
    from models.hemograma_data import DadosHemograma
    
    dados = DadosHemograma.from_dict(dados_json)
    analisador = AnalisadorHemograma(dados)
    resultado = analisador.analisar()
    
    print("✅ Processamento concluído!")
    print()
    
    print("=" * 80)
    print("RESULTADO DA ANÁLISE:")
    print("=" * 80)
    print(f"Status Geral: {resultado['interpretacao']['status_geral']}")
    print(f"Alterações: {len(resultado['alteracoes'])}")
    print()
    
    if resultado['alteracoes']:
        print("Alterações Detectadas:")
        for alt in resultado['alteracoes']:
            print(f"  🔸 {alt}")
        print()
    
    print("Achados Principais:")
    for achado in resultado['interpretacao']['achados_principais']:
        print(f"  • {achado}")
    print()
    
    if resultado['interpretacao']['sugestoes_diagnosticas']:
        print("Sugestões Diagnósticas:")
        for sugestao in resultado['interpretacao']['sugestoes_diagnosticas']:
            print(f"  💡 {sugestao}")
        print()
    
    # Verificar laudos
    print("=" * 80)
    print("VERIFICAÇÃO DOS LAUDOS:")
    print("=" * 80)
    
    tem_laudo = 'laudo' in resultado and len(resultado['laudo']) > 0
    tem_laudo_audio = 'laudo_audio' in resultado and len(resultado['laudo_audio']) > 0
    
    print(f"✓ Laudo visual gerado: {tem_laudo} ({len(resultado.get('laudo', ''))} caracteres)")
    print(f"✓ Laudo áudio gerado: {tem_laudo_audio} ({len(resultado.get('laudo_audio', ''))} caracteres)")
    
    # Verificar caracteres especiais
    if tem_laudo_audio:
        caracteres_especiais = ['=', '-', '│', '┌', '└', '╔', '╗', '╚', '╝', '║']
        tem_especiais = any(c in resultado['laudo_audio'] for c in caracteres_especiais)
        print(f"✓ Laudo áudio SEM caracteres de formatação: {not tem_especiais}")
        
        if tem_especiais:
            print("   ⚠️  Caracteres encontrados no áudio:")
            for c in caracteres_especiais:
                if c in resultado['laudo_audio']:
                    count = resultado['laudo_audio'].count(c)
                    print(f"      '{c}': {count} vez(es)")
    
    print()
    print("=" * 80)
    print("✅ TESTE CONCLUÍDO COM SUCESSO!")
    print("=" * 80)
    print()
    
    return 0


if __name__ == '__main__':
    try:
        sys.exit(teste_api())
    except Exception as e:
        print(f"\n❌ ERRO: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
