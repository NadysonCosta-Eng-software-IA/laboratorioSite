"""
app.py
======
Ponto de entrada da aplicação, usando o padrão "Application Factory":
em vez de criar o objeto Flask direto no nível do módulo, escrevemos
uma FUNÇÃO (create_app) que constrói e devolve a aplicação pronta.

Por que isso é melhor que `app = Flask(__name__)` direto no topo do
arquivo?
1. Evita o import circular mencionado em extensions.py.
2. Permite criar múltiplas instâncias da aplicação com configurações
   diferentes — essencial para TESTES automatizados (Degrau futuro):
   você cria uma app de teste com banco de dados separado, sem afetar
   o banco de desenvolvimento.
"""

from flask import Flask, render_template
from config import Config
from extensions import db, migrate


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Conecta as extensões (criadas "sem dono" em extensions.py)
    # a esta aplicação Flask específica.
    db.init_app(app)
    migrate.init_app(app, db)

    # Registra os Blueprints. Cada um traz seu próprio conjunto de
    # rotas, já com o url_prefix definido dentro do próprio blueprint.
    from blueprints.exames.routes import exames_bp
    from blueprints.pacientes.routes import pacientes_bp

    app.register_blueprint(exames_bp)
    app.register_blueprint(pacientes_bp)

    # Rota da página inicial — um painel simples que vamos enriquecer
    # nos próximos degraus (hoje só mostra links para os dois CRUDs).
    @app.route("/")
    def home():
        return render_template("home.html")

    return app


# Esse bloco só executa quando rodamos "python app.py" diretamente
# (não quando o Flask CLI ou um servidor de produção importa o módulo).
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
