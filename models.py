"""
models.py
=========
Tabelas do domínio de um LABORATÓRIO DE ANÁLISES CLÍNICAS.

Diferente de um "Serviço" genérico de salão, aqui cada classe carrega
informação específica do negócio de saúde: tipo de amostra, prazo de
entrega, preparo do paciente, dados clínicos do paciente, etc.

Por enquanto (Degrau 1), Paciente e Exame são tabelas independentes —
ainda não existe Agendamento nem Resultado ligando uma à outra. Isso
fica para o próximo degrau, quando você já estiver confortável com o
CRUD básico de cada uma.
"""

from datetime import datetime, date
from extensions import db


class Paciente(db.Model):
    """
    Representa a pessoa que realiza os exames no laboratório.

    Por que pedir CPF, data de nascimento e sexo logo no início?
    1. CPF como identificador único evita cadastrar a mesma pessoa
       duas vezes por erro de digitação no nome (ex: "Maria Silva"
       vs "Maria da Silva").
    2. Data de nascimento e sexo afetam diretamente os VALORES DE
       REFERÊNCIA de muitos exames (ex: hemograma tem faixas normais
       diferentes para homens, mulheres e crianças). Mesmo que você
       ainda não use isso agora, captar esse dado desde o início evita
       ter que pedir para 1000 pacientes completarem o cadastro depois.
    """

    __tablename__ = "paciente"

    id = db.Column(db.Integer, primary_key=True)

    nome_completo = db.Column(db.String(150), nullable=False)

    # unique=True impede dois pacientes com o mesmo CPF no banco —
    # o próprio banco de dados garante essa regra, não só o formulário.
    # Armazenamos só os 11 dígitos (sem pontos/traço); formatamos na tela.
    cpf = db.Column(db.String(11), unique=True, nullable=False, index=True)

    data_nascimento = db.Column(db.Date, nullable=False)

    # Usamos string curta em vez de Boolean porque sexo biológico,
    # para fins de valores de referência laboratoriais, não é binário
    # simples como "ativo/inativo" — alguns exames têm faixas próprias
    # para "Indeterminado/Outro". Guardamos como texto controlado.
    sexo = db.Column(db.String(1), nullable=False)  # 'M', 'F' ou 'O'

    telefone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), nullable=True)

    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def idade(self):
        """
        Calcula a idade atual a partir da data de nascimento.
        Uma @property permite chamar paciente.idade como se fosse
        um campo comum, mesmo sendo calculado na hora (não fica
        guardado no banco, porque senão ficaria desatualizado a
        cada aniversário).
        """
        hoje = date.today()
        anos = hoje.year - self.data_nascimento.year
        # Ajusta caso o aniversário deste ano ainda não tenha chegado
        fez_aniversario = (hoje.month, hoje.day) >= (
            self.data_nascimento.month,
            self.data_nascimento.day,
        )
        if not fez_aniversario:
            anos -= 1
        return anos

    @property
    def cpf_formatado(self):
        """Transforma '12345678900' em '123.456.789-00' só para exibição."""
        c = self.cpf
        return f"{c[0:3]}.{c[3:6]}.{c[6:9]}-{c[9:11]}"

    def __repr__(self):
        return f"<Paciente {self.id}: {self.nome_completo}>"


class Exame(db.Model):
    """
    Representa um TIPO de exame que o laboratório realiza
    (ex: "Hemograma Completo", "Glicemia em Jejum", "TSH").

    Isso é diferente de um "resultado de exame" — Exame aqui é o
    CATÁLOGO do laboratório (o que ele oferece e por quanto), não
    o exame já realizado em um paciente específico. Essa distinção
    importa: Exame muda raramente; cada coleta/resultado é um
    registro novo, ligado a um paciente e a uma data.
    """

    __tablename__ = "exame"

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(150), nullable=False)

    # Código interno do laboratório (alguns labs usam um código curto
    # tipo "HEMO01" para identificar o exame em etiquetas de amostra).
    codigo_interno = db.Column(db.String(20), unique=True, nullable=True)

    # Tipo de amostra necessária. Usamos opções controladas (não texto
    # livre) para manter consistência — você vai poder filtrar/agrupar
    # exames por tipo de amostra depois.
    TIPOS_AMOSTRA = ["Sangue", "Urina", "Fezes", "Swab", "Saliva", "Outro"]
    tipo_amostra = db.Column(db.String(20), nullable=False, default="Sangue")

    # Em quantas horas o resultado fica pronto, normalmente. Isso é
    # informação que o paciente vai querer ver no site público depois.
    prazo_entrega_horas = db.Column(db.Integer, nullable=False, default=24)

    # Instruções de preparo (ex: "Jejum de 8 horas", "Não urinar 2h
    # antes da coleta"). Campo de texto livre, porque o preparo varia
    # muito de exame para exame e não vale a pena tentar "estruturar"
    # isso em opções fixas.
    instrucoes_preparo = db.Column(db.Text, nullable=True)

    preco = db.Column(db.Numeric(10, 2), nullable=False)

    ativo = db.Column(db.Boolean, default=True, nullable=False)

    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def exige_preparo(self):
        """True se houver alguma instrução de preparo cadastrada."""
        return bool(self.instrucoes_preparo and self.instrucoes_preparo.strip())

    def __repr__(self):
        return f"<Exame {self.id}: {self.nome}>"
