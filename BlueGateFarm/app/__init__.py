from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 1. Inicializa as extensões
    db.init_app(app)
    
    # IMPORTANTE: Importa e REGISTRA o Blueprint aqui
    from app.api.routes import api as api_blueprint # Importa a variável 'api' do routes.py
    app.register_blueprint(api_blueprint, url_prefix='/api/v1') # Registra com um prefixo

    # Rota de Teste Simples (Root)
    @app.route('/')
    def index():
        return '<h1>Projeto SysAgro: Estrutura base OK!</h1><p>Verifique o status da API em /api/v1/status.</p>'

    return app