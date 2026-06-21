# LabExam — Degrau 1

Sistema de gestão para laboratório de análises clínicas. Esta é a
**primeira etapa** de um projeto maior, construído deliberadamente em
degraus de aprendizado (ver explicação no final).

## O que já existe nesta etapa

- Estrutura de projeto Flask organizada em **Blueprints**
- Template mãe (`base.html`) do qual todas as páginas herdam
- CRUD completo de **Exames** (catálogo do laboratório)
- CRUD completo de **Pacientes**, incluindo validação real de CPF
  (algoritmo de dígito verificador, não só "tem 11 números")
- Banco de dados SQLite via SQLAlchemy

## O que NÃO existe ainda (de propósito)

- Login / autenticação
- Agendamento de coleta (vai depender de Paciente + Exame já existirem)
- Resultados / laudos
- Suporte a múltiplos laboratórios (multi-tenant)
- Site público / chatbot para pacientes

## Como rodar

```bash
# 1. Criar e ativar um ambiente virtual (recomendado)
python3 -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Rodar o servidor de desenvolvimento
python app.py
```

O servidor sobe em `http://127.0.0.1:5000`. O banco de dados SQLite é
criado automaticamente na primeira execução, dentro de `instance/labexam.db`
(essa pasta não vai para o Git — veja `.gitignore`).

## Estrutura de pastas

```
labexam/
├── app.py                    # Application Factory (create_app)
├── config.py                  # Configurações (banco, secret key)
├── extensions.py              # Instâncias compartilhadas (db, migrate)
├── models.py                  # Tabelas: Paciente, Exame
├── requirements.txt
├── blueprints/
│   ├── exames/
│   │   ├── routes.py          # CRUD de exames
│   │   └── forms.py           # Formulário com validação
│   └── pacientes/
│       ├── routes.py          # CRUD de pacientes
│       └── forms.py           # Formulário com validação de CPF
├── templates/
│   ├── base.html              # TEMPLATE MÃE
│   ├── home.html
│   ├── exames/
│   │   ├── listar.html
│   │   └── form.html
│   └── pacientes/
│       ├── listar.html
│       └── form.html
└── static/
    └── css/style.css
```

## Por que "Degrau 1"?

Este projeto nasceu de uma ambição maior: um SaaS completo para
laboratórios (e depois farmácias), com app mobile e módulo de IA para
decisões de negócio. Construir tudo isso de uma vez, sendo o primeiro
projeto Flask sério do desenvolvedor, é a receita certa para travar ou
copiar código sem entender.

Em vez disso, a trilha é:

1. **Degrau 1 (aqui)** — Flask "sério" de verdade: Blueprints, template
   herdado, CRUD completo, validação de formulário. Um laboratório só,
   sem login.
2. **Degrau 2** — Autenticação. O laboratório ganha um "dono" que faz
   login para acessar o painel.
3. **Degrau 3** — Multi-tenant de verdade: múltiplos laboratórios na
   mesma base de dados, com isolamento entre eles.
4. **Degrau 4** — API REST + app mobile em Flutter consumindo essa API.
5. **Fase IA** — só depois de haver dados reais de uso para a IA
   aprender com eles (financeiro, estoque, etc).

Cada degrau é um projeto completo e funcional por si só — não um
tutorial de brinquedo, mas também não a arquitetura final do dia 1.
