"""
Aplicação Flask para o Sistema de Laudos de ECG com Acessibilidade
Versão refatorada com arquitetura modular
"""
from flask import Flask
from routes import main_bp, api_bp
import config


def create_app():
    """Factory function para criar a aplicação Flask"""
    app = Flask(__name__)
    
    # Configurações
    app.config['SECRET_KEY'] = config.SECRET_KEY
    app.config['DEBUG'] = config.DEBUG
    
    # Registrar blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    
    return app


# Criar aplicação
app = create_app()


if __name__ == '__main__':
    app.run(
        debug=config.DEBUG,
        host='0.0.0.0',
        port=5000
    )
