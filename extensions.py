"""
extensions.py
==============
Instâncias compartilhadas, criadas aqui "sem dono" para evitar import
circular. Em app.py, conectamos (init_app) essas extensões à aplicação
Flask de verdade. Esse padrão chama-se "Application Factory".
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
