"""
routes.py (blueprint de pacientes)
=====================================
CRUD de pacientes. Mesma estrutura de exames.py, mas com um detalhe
novo: tratar o erro de CPF duplicado também no banco de dados (não só
no formulário), porque dois usuários poderiam, em teoria, tentar
cadastrar o mesmo CPF ao mesmo tempo (uma race condition rara, mas
possível). A constraint unique=True do model garante isso no banco;
aqui só capturamos o erro de forma amigável.
"""

from flask import Blueprint, render_template, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError
from extensions import db
from models import Paciente
from blueprints.pacientes.forms import PacienteForm

pacientes_bp = Blueprint("pacientes", __name__, url_prefix="/pacientes")


@pacientes_bp.route("/")
def listar():
    """READ — lista todos os pacientes, mais recentes primeiro."""
    todos_pacientes = Paciente.query.order_by(Paciente.nome_completo).all()
    return render_template("pacientes/listar.html", pacientes=todos_pacientes)


@pacientes_bp.route("/novo", methods=["GET", "POST"])
def novo():
    """CREATE — cadastro de novo paciente."""
    form = PacienteForm()

    if form.validate_on_submit():
        novo_paciente = Paciente(
            nome_completo=form.nome_completo.data,
            cpf=form.cpf.data,  # já vem "limpo" (só dígitos) pelo validate_cpf
            data_nascimento=form.data_nascimento.data,
            sexo=form.sexo.data,
            telefone=form.telefone.data,
            email=form.email.data,
        )
        db.session.add(novo_paciente)

        try:
            db.session.commit()
            flash(f"Paciente '{novo_paciente.nome_completo}' cadastrado com sucesso!", "success")
            return redirect(url_for("pacientes.listar"))
        except IntegrityError:
            # Acontece se, por alguma corrida de requisições, dois
            # cadastros com o mesmo CPF chegarem quase juntos e o
            # validate_cpf não pegar (porque cada um validou antes
            # do outro existir no banco). Desfazemos a transação e
            # avisamos o usuário com clareza.
            db.session.rollback()
            flash("Já existe um paciente cadastrado com este CPF.", "danger")

    return render_template("pacientes/form.html", form=form, titulo="Novo Paciente")


@pacientes_bp.route("/<int:paciente_id>/editar", methods=["GET", "POST"])
def editar(paciente_id):
    """UPDATE — edita um paciente existente."""
    paciente = db.get_or_404(Paciente, paciente_id)
    form = PacienteForm(obj=paciente)

    if form.validate_on_submit():
        form.populate_obj(paciente)
        try:
            db.session.commit()
            flash(f"Dados de '{paciente.nome_completo}' atualizados.", "success")
            return redirect(url_for("pacientes.listar"))
        except IntegrityError:
            db.session.rollback()
            flash("Já existe outro paciente cadastrado com este CPF.", "danger")

    return render_template("pacientes/form.html", form=form, titulo="Editar Paciente")


@pacientes_bp.route("/<int:paciente_id>/excluir", methods=["POST"])
def excluir(paciente_id):
    """DELETE — remove um paciente. Só aceita POST."""
    paciente = db.get_or_404(Paciente, paciente_id)
    nome = paciente.nome_completo
    db.session.delete(paciente)
    db.session.commit()
    flash(f"Paciente '{nome}' removido.", "info")
    return redirect(url_for("pacientes.listar"))
