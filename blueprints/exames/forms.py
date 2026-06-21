"""
forms.py (blueprint de exames)
================================
Formulário de cadastro/edição de Exame.

Novidade em relação ao formulário simples: usamos SelectField para
tipo_amostra, transformando a lista TIPOS_AMOSTRA do model em opções
de um <select> HTML — assim o usuário escolhe de uma lista fixa, em
vez de digitar texto livre que poderia vir com erros de digitação
("Sangue", "sangue", "SANGUE", "Sangu"...).
"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, IntegerField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length, Optional
from models import Exame


class ExameForm(FlaskForm):
    nome = StringField(
        "Nome do exame",
        validators=[DataRequired(message="O nome é obrigatório."), Length(max=150)],
    )

    codigo_interno = StringField(
        "Código interno (opcional)",
        validators=[Optional(), Length(max=20)],
    )

    # choices precisa de uma lista de tuplas (valor_salvo, texto_exibido).
    # Aqui os dois são iguais, mas em outros campos podem diferir
    # (ex: [("M", "Masculino"), ("F", "Feminino")]).
    tipo_amostra = SelectField(
        "Tipo de amostra",
        choices=[(t, t) for t in Exame.TIPOS_AMOSTRA],
        validators=[DataRequired()],
    )

    prazo_entrega_horas = IntegerField(
        "Prazo de entrega (horas)",
        validators=[DataRequired(message="Informe o prazo."), NumberRange(min=1, max=720, message="Entre 1 hora e 30 dias (720h).")],
        default=24,
    )

    instrucoes_preparo = TextAreaField(
        "Instruções de preparo (opcional)",
        validators=[Optional(), Length(max=500)],
    )

    preco = DecimalField(
        "Preço (R$)",
        validators=[DataRequired(message="Informe o preço."), NumberRange(min=0, message="O preço não pode ser negativo.")],
        places=2,
    )

    ativo = BooleanField("Exame ativo (disponível para agendamento)", default=True)

    submit = SubmitField("Salvar")
