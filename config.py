"""
config.py
=========
Configurações da aplicação. Nenhuma regra de negócio mora aqui —
só "onde" e "como" a aplicação se conecta a recursos externos
(banco de dados, chaves de segurança).
"""

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "chave-temporaria-trocar-depois")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'labexam.db')}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
