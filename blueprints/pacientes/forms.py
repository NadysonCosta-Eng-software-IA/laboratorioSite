"""
forms.py (blueprint de pacientes)
====================================
Novidade aqui: VALIDAÇÃO CUSTOMIZADA de CPF.

WTForms já vem com validadores prontos (DataRequired, Length, etc),
mas CPF tem uma regra de negócio própria — não é só "11 dígitos",
é um algoritmo de dígito verificador. Vamos escrever nossa própria
função de validação e conectá-la ao campo.
"""

import re
from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Optional, Email


def cpf_e_valido(cpf: str) -> bool:
    """
    Implementa o algoritmo oficial de validação de CPF (dígitos
    verificadores). Isso pega erros de digitação reais — não só
    "tem 11 números", mas "esses 11 números formam um CPF
    matematicamente possível".

    Não é uma função de formulário (não recebe form/field) de
    propósito: assim ela pode ser reaproveitada em outros lugares
    do sistema no futuro (ex: numa API), sem depender do WTForms.
    """
    cpf = re.sub(r"[^0-9]", "", cpf)  # remove pontos, traço, espaços

    if len(cpf) != 11:
        return False

    # CPFs com todos os dígitos iguais (111.111.111-11) passam no
    # cálculo matemático mas não são CPFs reais — precisa bloquear à parte.
    if cpf == cpf[0] * 11:
        return False

    def calcular_digito(cpf_parcial: str) -> str:
        soma = sum(
            int(digito) * peso
            for digito, peso in zip(cpf_parcial, range(len(cpf_parcial) + 1, 1, -1))
        )
        resto = (soma * 10) % 11
        return "0" if resto == 10 else str(resto)

    digito1 = calcular_digito(cpf[:9])
    digito2 = calcular_digito(cpf[:9] + digito1)

    return cpf[-2:] == digito1 + digito2


class PacienteForm(FlaskForm):
    nome_completo = StringField(
        "Nome completo",
        validators=[DataRequired(message="O nome é obrigatório."), Length(max=150)],
    )

    cpf = StringField(
        "CPF",
        validators=[DataRequired(message="O CPF é obrigatório.")],
        render_kw={"placeholder": "000.000.000-00"},
    )

    data_nascimento = DateField(
        "Data de nascimento",
        validators=[DataRequired(message="Informe a data de nascimento.")],
        format="%Y-%m-%d",
    )

    sexo = SelectField(
        "Sexo",
        choices=[("M", "Masculino"), ("F", "Feminino"), ("O", "Outro")],
        validators=[DataRequired()],
    )

    telefone = StringField("Telefone", validators=[Optional(), Length(max=20)])

    email = StringField(
        "E-mail",
        validators=[Optional(), Email(message="E-mail inválido."), Length(max=120)],
    )

    submit = SubmitField("Salvar")

    def validate_cpf(self, field):
        """
        Métodos chamados validate_<nome_do_campo> são reconhecidos
        AUTOMATICAMENTE pelo WTForms como validadores extras daquele
        campo — não precisamos registrar isso em lugar nenhum, o
        framework já procura por essa convenção de nome.
        """
        cpf_limpo = re.sub(r"[^0-9]", "", field.data or "")

        if not cpf_e_valido(cpf_limpo):
            raise ValidationError("CPF inválido. Confira os números digitados.")

        # Guardamos o CPF já "limpo" (só dígitos) de volta no campo,
        # para salvar no banco sempre no mesmo formato — independente
        # de o usuário ter digitado com ou sem pontos/traço.
        field.data = cpf_limpo

    def validate_data_nascimento(self, field):
        """Impede datas de nascimento no futuro."""
        if field.data and field.data > date.today():
            raise ValidationError("A data de nascimento não pode ser no futuro.")
