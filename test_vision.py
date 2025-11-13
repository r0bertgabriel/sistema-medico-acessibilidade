#!/usr/bin/env python3
"""
Script de teste para análise de ECG por imagem
"""
import os
import sys
from pathlib import Path

# Adicionar diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent))

from services import VisionService


def testar_analise_imagem(caminho_imagem: str):
    """
    Testa a análise de uma imagem de ECG
    
    Args:
        caminho_imagem: Caminho para a imagem do ECG
    """
    print("=" * 80)
    print("TESTE DE ANÁLISE DE ECG POR IMAGEM")
    print("=" * 80)
    print()
    
    # Verificar se arquivo existe
    if not os.path.exists(caminho_imagem):
        print(f"❌ Erro: Arquivo não encontrado: {caminho_imagem}")
        return
    
    # Verificar se API key está configurada
    if not os.environ.get('OPENAI_API_KEY'):
        print("❌ Erro: OPENAI_API_KEY não configurada")
        print()
        print("Configure a variável de ambiente:")
        print("  export OPENAI_API_KEY='sua-chave-aqui'")
        return
    
    try:
        # Inicializar serviço
        print("🔧 Inicializando Vision Service...")
        vision_service = VisionService()
        print("✅ Serviço inicializado")
        print()
        
        # Analisar imagem
        print(f"📸 Analisando imagem: {caminho_imagem}")
        print("⏳ Aguarde... (isso pode levar alguns segundos)")
        print()
        
        dados_vision = vision_service.analisar_ecg_imagem(caminho_imagem)
        
        print("✅ Análise concluída!")
        print()
        print("=" * 80)
        print("RESULTADOS DA ANÁLISE")
        print("=" * 80)
        print()
        
        # Exibir dados quantitativos
        if 'dados_quantitativos' in dados_vision:
            print("📊 DADOS QUANTITATIVOS")
            print("-" * 40)
            quant = dados_vision['dados_quantitativos']
            print(f"  Frequência Cardíaca: {quant.get('frequencia_cardiaca')} bpm")
            print(f"  Intervalo PR: {quant.get('intervalo_pr')} s")
            print(f"  Duração QRS: {quant.get('duracao_qrs')} s")
            print(f"  Intervalo QT: {quant.get('intervalo_qt')} s")
            print(f"  QTc: {quant.get('qtc')} s")
            print(f"  Eixo QRS: {quant.get('eixo_qrs')}°")
            print()
        
        # Exibir ritmo
        if 'ritmo' in dados_vision:
            print("💓 RITMO")
            print("-" * 40)
            ritmo = dados_vision['ritmo']
            print(f"  Tipo: {ritmo.get('tipo')}")
            print(f"  Regular: {'Sim' if ritmo.get('regular') else 'Não'}")
            print(f"  Descrição: {ritmo.get('descricao')}")
            print()
        
        # Exibir segmento ST
        if 'segmentos' in dados_vision and 'segmento_st' in dados_vision['segmentos']:
            print("📈 SEGMENTO ST")
            print("-" * 40)
            st = dados_vision['segmentos']['segmento_st']
            print(f"  Elevação: {'Sim' if st.get('elevacao') else 'Não'}")
            print(f"  Depressão: {'Sim' if st.get('depressao') else 'Não'}")
            if st.get('derivacoes_afetadas'):
                print(f"  Derivações: {', '.join(st['derivacoes_afetadas'])}")
            print()
        
        # Exibir bloqueios
        if 'bloqueios' in dados_vision:
            print("🚫 BLOQUEIOS")
            print("-" * 40)
            bloq = dados_vision['bloqueios']
            
            if bloq.get('bloqueio_av', {}).get('presente'):
                av = bloq['bloqueio_av']
                print(f"  Bloqueio AV: Grau {av.get('grau')} ({av.get('tipo')})")
            
            if bloq.get('bloqueio_ramo', {}).get('presente'):
                ramo = bloq['bloqueio_ramo']
                completo = "Completo" if ramo.get('completo') else "Incompleto"
                print(f"  Bloqueio de Ramo: {ramo.get('tipo')} ({completo})")
            
            if bloq.get('hemibloqueio', {}).get('presente'):
                hemi = bloq['hemibloqueio']
                print(f"  Hemibloqueio: {hemi.get('tipo')}")
            
            if not any([
                bloq.get('bloqueio_av', {}).get('presente'),
                bloq.get('bloqueio_ramo', {}).get('presente'),
                bloq.get('hemibloqueio', {}).get('presente')
            ]):
                print("  Nenhum bloqueio detectado")
            print()
        
        # Exibir hipertrofias
        if 'hipertrofias' in dados_vision:
            print("💪 HIPERTROFIAS")
            print("-" * 40)
            hiper = dados_vision['hipertrofias']
            hipertrofias_presentes = []
            
            if hiper.get('hipertrofia_ve'):
                hipertrofias_presentes.append("Ventrículo Esquerdo")
            if hiper.get('hipertrofia_vd'):
                hipertrofias_presentes.append("Ventrículo Direito")
            if hiper.get('hipertrofia_ae'):
                hipertrofias_presentes.append("Átrio Esquerdo")
            if hiper.get('hipertrofia_ad'):
                hipertrofias_presentes.append("Átrio Direito")
            
            if hipertrofias_presentes:
                print(f"  Detectadas: {', '.join(hipertrofias_presentes)}")
            else:
                print("  Nenhuma hipertrofia detectada")
            print()
        
        # Exibir isquemia
        if 'isquemia' in dados_vision:
            print("⚠️  ISQUEMIA")
            print("-" * 40)
            isq = dados_vision['isquemia']
            if isq.get('presente'):
                print(f"  Status: PRESENTE")
                if isq.get('localizacao'):
                    print(f"  Localização: {', '.join(isq['localizacao'])}")
                print(f"  Tipo: {isq.get('tipo')}")
                print(f"  Aguda: {'Sim' if isq.get('aguda') else 'Não'}")
            else:
                print("  Não detectada")
            print()
        
        # Exibir conclusão
        if 'conclusao' in dados_vision:
            print("🎯 CONCLUSÃO")
            print("-" * 40)
            conclusao = dados_vision['conclusao']
            print(f"  Gravidade: {conclusao.get('gravidade')}")
            print()
            
            if conclusao.get('principais_achados'):
                print("  Principais Achados:")
                for achado in conclusao['principais_achados']:
                    print(f"    • {achado}")
                print()
            
            if conclusao.get('diagnosticos_suspeitos'):
                print("  Diagnósticos Suspeitos:")
                for diag in conclusao['diagnosticos_suspeitos']:
                    print(f"    • {diag}")
                print()
            
            if conclusao.get('recomendacoes'):
                print("  Recomendações:")
                for rec in conclusao['recomendacoes']:
                    print(f"    • {rec}")
                print()
        
        # Exibir qualidade
        if 'qualidade_ecg' in dados_vision:
            print("🔍 QUALIDADE DO ECG")
            print("-" * 40)
            qual = dados_vision['qualidade_ecg']
            print(f"  Qualidade do Traçado: {qual.get('qualidade_traçado')}")
            print(f"  Artefatos: {'Sim' if qual.get('artefatos') else 'Não'}")
            print(f"  Calibração Adequada: {'Sim' if qual.get('calibracao_adequada') else 'Não'}")
            if qual.get('observacoes'):
                print(f"  Observações: {qual['observacoes']}")
            print()
        
        print("=" * 80)
        print()
        
        # Converter para formato do sistema
        print("🔄 Convertendo para formato do sistema...")
        dados_sistema = vision_service.converter_para_formato_sistema(dados_vision)
        print("✅ Conversão concluída!")
        print()
        
        print("📋 Dados prontos para processamento pelo sistema de laudos")
        print()
        
    except Exception as e:
        print(f"❌ Erro durante análise: {str(e)}")
        import traceback
        traceback.print_exc()


def main():
    """Função principal"""
    if len(sys.argv) < 2:
        print("Uso: python test_vision.py <caminho_para_imagem_ecg>")
        print()
        print("Exemplo:")
        print("  python test_vision.py ecg_example.jpg")
        sys.exit(1)
    
    caminho_imagem = sys.argv[1]
    testar_analise_imagem(caminho_imagem)


if __name__ == '__main__':
    main()
