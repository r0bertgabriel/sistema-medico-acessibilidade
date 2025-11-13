#!/usr/bin/env python3
"""
Script de teste para o módulo de Hemograma
"""
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from models.hemograma_analyzer import AnalisadorHemograma
from models.hemograma_data import DadosHemograma
from services.hemograma_service import HemogramaService


def testar_hemograma_normal():
    """Testa análise de hemograma normal"""
    print("=" * 80)
    print("TESTE 1: Hemograma Normal")
    print("=" * 80)
    
    dados = DadosHemograma(
        nome_paciente="João Silva (Teste)",
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
    
    print(resultado['laudo'])
    print("\n" + "=" * 80)
    print(f"Status: {resultado['interpretacao']['status_geral']}")
    print("Alterações:", len(resultado['alteracoes']))
    print()


def testar_anemia():
    """Testa detecção de anemia"""
    print("=" * 80)
    print("TESTE 2: Anemia Microcítica")
    print("=" * 80)
    
    dados = DadosHemograma(
        nome_paciente="Maria Santos (Teste)",
        idade=42,
        sexo="F",
        data_coleta="12/11/2025",
        hemacias=3.5,
        hemoglobina=10.0,
        hematocrito=32.0,
        vcm=75.0,
        hcm=25.0,
        chcm=32.0,
        rdw=16.5,
        leucocitos=6500,
        neutrofilos=3500,
        linfocitos=2200,
        monocitos=450,
        eosinofilos=180,
        basofilos=40,
        plaquetas=280000,
        observacoes="Paciente refere fadiga"
    )
    
    analisador = AnalisadorHemograma(dados)
    resultado = analisador.analisar()
    
    print(resultado['laudo'])
    print("\n" + "=" * 80)
    print(f"Status: {resultado['interpretacao']['status_geral']}")
    print(f"Alterações detectadas: {len(resultado['alteracoes'])}")
    print("\nSugestões Diagnósticas:")
    for sugestao in resultado['interpretacao']['sugestoes_diagnosticas']:
        print(f"  - {sugestao}")
    print()


def testar_leucocitose():
    """Testa detecção de leucocitose"""
    print("=" * 80)
    print("TESTE 3: Leucocitose com Neutrofilia")
    print("=" * 80)
    
    dados = DadosHemograma(
        nome_paciente="Pedro Oliveira (Teste)",
        idade=28,
        sexo="M",
        data_coleta="12/11/2025",
        hemacias=4.8,
        hemoglobina=14.5,
        hematocrito=43.0,
        vcm=88.0,
        hcm=29.0,
        chcm=33.5,
        rdw=12.8,
        leucocitos=15000,
        neutrofilos=11000,
        linfocitos=2500,
        monocitos=800,
        eosinofilos=300,
        basofilos=60,
        plaquetas=320000,
        observacoes="Quadro febril"
    )
    
    analisador = AnalisadorHemograma(dados)
    resultado = analisador.analisar()
    
    print("\nInterpretação:")
    print(f"Status: {resultado['interpretacao']['status_geral']}")
    print("\nAchados Principais:")
    for achado in resultado['interpretacao']['achados_principais']:
        print(f"  - {achado}")
    print("\nSugestões Diagnósticas:")
    for sugestao in resultado['interpretacao']['sugestoes_diagnosticas']:
        print(f"  - {sugestao}")
    print()


def testar_servico():
    """Testa o serviço de hemograma"""
    print("=" * 80)
    print("TESTE 4: Serviço de Hemograma (sem áudio)")
    print("=" * 80)
    
    # Testar validação
    dados_invalidos = {
        "paciente": {
            "nome": "",  # Nome vazio
            "idade": 0,  # Idade inválida
            "sexo": "X"  # Sexo inválido
        }
    }
    
    validacao = HemogramaService.validar_dados(dados_invalidos)
    print("\nTeste de Validação (dados inválidos):")
    print(f"Válido: {validacao['valido']}")
    print(f"Erros encontrados: {len(validacao['erros'])}")
    for erro in validacao['erros']:
        print(f"  - {erro}")
    
    # Testar exemplo
    print("\n" + "-" * 80)
    print("Carregando exemplo de hemograma normal...")
    exemplo = HemogramaService.obter_exemplo_hemograma('normal')
    print(f"Exemplo carregado: {exemplo['paciente']['nome']}")
    print(f"Idade: {exemplo['paciente']['idade']} anos")
    print(f"Sexo: {exemplo['paciente']['sexo']}")
    print()


def main():
    """Executa todos os testes"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "TESTES DO MÓDULO DE HEMOGRAMA" + " " * 28 + "║")
    print("╚" + "=" * 78 + "╝")
    print()
    
    try:
        testar_hemograma_normal()
        input("Pressione ENTER para continuar...")
        
        testar_anemia()
        input("Pressione ENTER para continuar...")
        
        testar_leucocitose()
        input("Pressione ENTER para continuar...")
        
        testar_servico()
        
        print("\n" + "=" * 80)
        print("✓ TODOS OS TESTES CONCLUÍDOS COM SUCESSO!")
        print("=" * 80)
        print()
        
    except Exception as e:
        print(f"\n✗ ERRO NOS TESTES: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
