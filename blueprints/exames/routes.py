"""
routes.py (blueprint de exames)
=================================
CRUD completo do catálogo de exames do laboratório.
Mesma estrutura de 4 operações (Create, Read, Update, Delete) que
você vai repetir em todo blueprint novo — uma vez entendido aqui,
o próximo (Pacientes) vai parecer familiar.
"""

from flask import Blueprint, render_template, redirect, url_for, flash
from extensions import db
from models import Exame
from blueprints.exames.forms import ExameForm

exames_bp = Blueprint("exames", __name__, url_prefix="/exames")


@exames_bp.route("/")
def listar():
    """READ — lista todos os exames cadastrados, em ordem alfabética."""
    todos_exames = Exame.query.order_by(Exame.nome).all()
    return render_template("exames/listar.html", exames=todos_exames)


@exames_bp.route("/novo", methods=["GET", "POST"])
def novo():
    """CREATE — formulário de novo exame."""
    form = ExameForm()

    if form.validate_on_submit():
        novo_exame = Exame(
            nome=form.nome.data,
            codigo_interno=form.codigo_interno.data or None,
            tipo_amostra=form.tipo_amostra.data,
            prazo_entrega_horas=form.prazo_entrega_horas.data,
            instrucoes_preparo=form.instrucoes_preparo.data,
            preco=form.preco.data,
            ativo=form.ativo.data,
        )
        db.session.add(novo_exame)
        db.session.commit()
        flash(f"Exame '{novo_exame.nome}' cadastrado com sucesso!", "success")
        return redirect(url_for("exames.listar"))

    return render_template("exames/form.html", form=form, titulo="Novo Exame")


@exames_bp.route("/<int:exame_id>/editar", methods=["GET", "POST"])
def editar(exame_id):
    """UPDATE — edita um exame existente."""
    exame = db.get_or_404(Exame, exame_id)
    form = ExameForm(obj=exame)

    if form.validate_on_submit():
        form.populate_obj(exame)
        db.session.commit()
        flash(f"Exame '{exame.nome}' atualizado com sucesso!", "success")
        return redirect(url_for("exames.listar"))

    return render_template("exames/form.html", form=form, titulo="Editar Exame")


@exames_bp.route("/<int:exame_id>/excluir", methods=["POST"])
def excluir(exame_id):
    """DELETE — remove um exame. Só aceita POST (nunca um link GET)."""
    exame = db.get_or_404(Exame, exame_id)
    nome = exame.nome
    db.session.delete(exame)
    db.session.commit()
    flash(f"Exame '{nome}' removido.", "info")
    return redirect(url_for("exames.listar"))
