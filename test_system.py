"""
Script de teste para validar os módulos do sistema
"""
from models.ecg_analyzer import AnalisadorECG
from models.ecg_data import DadosECG, IntervalosECG, OndaP
from models.laudo_generator import GeradorLaudo


def testar_ecg_normal():
    """Testa análise de ECG normal"""
    print("=" * 80)
    print("TESTE 1: ECG NORMAL")
    print("=" * 80)
    
    dados = DadosECG(
        nome_paciente="Paciente Teste - Normal",
        ritmo="sinusal",
        frequencia_cardiaca=72,
        regularidade="regular",
        eixo_qrs=50,
        intervalos=IntervalosECG(pr=0.16, qrs=0.08, qt=0.38, qtc=0.40)
    )
    
    gerador = GeradorLaudo()
    resultado = gerador.gerar_laudo_completo(dados)
    
    print("\n📄 LAUDO TEXTO:\n")
    print(resultado['texto_completo'])
    print("\n" + "=" * 80)
    print("🔊 TEXTO PARA ÁUDIO:\n")
    print(resultado['texto_audio'])
    print("\n" + "=" * 80)


def testar_bloqueio_ramo():
    """Testa análise de ECG com bloqueio"""
    print("\n\n" + "=" * 80)
    print("TESTE 2: BLOQUEIO INCOMPLETO DE RAMO DIREITO")
    print("=" * 80)
    
    dados = DadosECG(
        nome_paciente="Paciente Teste - Bloqueio",
        ritmo="sinusal",
        frequencia_cardiaca=85,
        regularidade="regular",
        eixo_qrs=-18,
        intervalos=IntervalosECG(pr=0.16, qrs=0.09, qt=0.40, qtc=0.42),
        bloqueio_ramo="incompleto_direito"
    )
    
    gerador = GeradorLaudo()
    resultado = gerador.gerar_laudo_completo(dados)
    
    print("\n📋 DIAGNÓSTICOS:")
    for i, diag in enumerate(resultado['diagnosticos'], 1):
        print(f"{i}. {diag}")
    
    print("\n🔊 TEXTO PARA ÁUDIO:\n")
    print(resultado['texto_audio'])
    print("\n" + "=" * 80)


def testar_analisador():
    """Testa o analisador isoladamente"""
    print("\n\n" + "=" * 80)
    print("TESTE 3: ANALISADOR DE ECG")
    print("=" * 80)
    
    dados = DadosECG(
        ritmo="sinusal",
        frequencia_cardiaca=105,  # Taquicardia
        regularidade="regular",
        eixo_qrs=-40,  # Desvio esquerda
        intervalos=IntervalosECG(pr=0.22, qrs=0.11, qt=0.45, qtc=0.46)
    )
    
    analisador = AnalisadorECG()
    resultado = analisador.analisar(dados)
    
    print("\n✅ ACHADOS:")
    for achado in resultado['achados']:
        print(f"  • {achado}")
    
    print("\n⚠️ DIAGNÓSTICOS:")
    for diag in resultado['diagnosticos']:
        print(f"  • {diag}")
    
    print("\n📊 CONCLUSÃO:")
    print(resultado['conclusao'])
    print("\n" + "=" * 80)


if __name__ == "__main__":
    print("\n🩺 SISTEMA DE LAUDOS DE ECG - TESTES\n")
    
    try:
        testar_ecg_normal()
        testar_bloqueio_ramo()
        testar_analisador()
        
        print("\n\n✅ TODOS OS TESTES CONCLUÍDOS COM SUCESSO!\n")
        print("💡 Para testar a geração de áudio, execute: python app.py")
        print("   e acesse http://localhost:5000\n")
        
    except Exception as e:
        print(f"\n❌ ERRO NOS TESTES: {e}\n")
        import traceback
        traceback.print_exc()
