"""
Aplicação Flask para o Sistema de Laudos de ECG com Acessibilidade
Versão refatorada com arquitetura modular
"""
import os

from flask import Flask, send_from_directory

import config
from routes import api_bp, main_bp


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


# Criar aplicação
app = create_app()


if __name__ == '__main__':
    app.run(
        debug=config.DEBUG,
        host='0.0.0.0',
        port=5000
    )
