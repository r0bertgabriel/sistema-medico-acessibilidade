"""
Aplicação Flask para o Sistema de Laudos de ECG com Acessibilidade
Versão refatorada com arquitetura modular
"""
import os
import sys

from flask import Flask, send_from_directory

import config
from routes import api_bp, main_bp


def inicializar_cache_audios():
    """
    Inicializa cache de áudios verificando e gerando laudos necessários
    
    IMPORTANTE: Esta função pré-gera TODOS os áudios de exemplos no startup.
    Quando o usuário clicar em "Gerar Laudo", o sistema apenas REPRODUZ o áudio
    já existente (cache HIT), sem necessidade de regenerar. Isso garante:
    
    - Resposta instantânea (< 100ms)
    - Sem delay de geração
    - Experiência fluida para demonstrações
    - Economia de recursos (não chama gTTS repetidamente)
    """
    try:
        print("\n" + "="*70)
        print("🎤 INICIALIZANDO CACHE DE ÁUDIOS (Pré-geração para Performance)")
        print("="*70)
        
        from data.ecg_examples import obter_todos_exemplos
        from services.audio_cache_service import AudioCacheService
        from services.ecg_service import ECGService
        from services.hemograma_service import HemogramaService
        
        cache_service = AudioCacheService()
        
        # Estatísticas iniciais
        stats = cache_service.estatisticas_cache()
        print(f"📊 Cache atual: {stats['total_arquivos']} arquivos, {stats['tamanho_mb']} MB")
        
        # Pré-gerar ECG
        print("\n🫀 Verificando áudios de ECG...")
        ecg_service = ECGService()
        exemplos = obter_todos_exemplos()
        
        gerados_ecg = 0
        for nome, dados_ecg in exemplos.items():
            try:
                dados_dict = dados_ecg.to_dict()
                resultado = ecg_service.analisar_ecg(dados_dict)
                identificador = f"ecg_{nome}"
                
                cached = cache_service.verificar_cache(resultado['laudo_audio_texto'])
                if not cached:
                    cache_service.pre_gerar_audio(
                        resultado['laudo_audio_texto'],
                        identificador
                    )
                    gerados_ecg += 1
            except Exception as e:
                print(f"   ⚠️ Erro em {nome}: {e}")
        
        if gerados_ecg > 0:
            print(f"   ✅ {gerados_ecg} áudios de ECG gerados")
        else:
            print("   ✅ Todos os áudios de ECG já existem")
        
        # Pré-gerar Hemograma
        print("\n🩸 Verificando áudios de Hemograma...")
        tipos_exemplos = ['normal', 'anemia', 'leucocitose', 'plaquetopenia']
        
        gerados_hemo = 0
        for tipo in tipos_exemplos:
            try:
                exemplo = HemogramaService.obter_exemplo_hemograma(tipo)
                identificador = f"hemograma_{tipo}"
                resultado = HemogramaService.processar_hemograma(exemplo, identificador)
                
                if resultado.get('sucesso') and resultado.get('audio_filename'):
                    # Áudio já foi gerado/verificado pelo service
                    pass
                else:
                    gerados_hemo += 1
            except Exception as e:
                print(f"   ⚠️ Erro em {tipo}: {e}")
        
        print(f"   ✅ Áudios de Hemograma verificados")
        
        # Estatísticas finais
        stats_final = cache_service.estatisticas_cache()
        novos = stats_final['total_arquivos'] - stats['total_arquivos']
        
        print("\n" + "="*70)
        print(f"✅ Cache inicializado: {stats_final['total_arquivos']} áudios ({novos} novos)")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n⚠️ Erro ao inicializar cache de áudios: {e}")
        print("   O sistema continuará funcionando, mas áudios serão gerados sob demanda.\n")


def create_app():
    """Factory function para criar a aplicação Flask"""
    app = Flask(__name__)
    
    # Configurações
    app.config['SECRET_KEY'] = config.SECRET_KEY
    app.config['DEBUG'] = config.DEBUG
    app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH
    app.config['UPLOAD_FOLDER'] = str(config.UPLOAD_FOLDER)
    
    # Registrar blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    
    # Rota para favicon
    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'),
                                  'favicon.ico', mimetype='image/vnd.microsoft.icon')
    
    return app


# Inicializar cache de áudios antes de criar app
if __name__ == '__main__':
    inicializar_cache_audios()

# Criar aplicação
app = create_app()


if __name__ == '__main__':
    app.run(
        debug=config.DEBUG,
        host='0.0.0.0',
        port=5000
    )
