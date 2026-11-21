# FinLess - Backend (Django)

Este diretório contém a API e lógica de negócio do sistema **FinLess**.

## Estrutura Implementada

```text
backend/
├── manage.py                 # Script de gerenciamento do Django
├── .coveragerc               # Configuração de cobertura de testes (C0 + C1 branches)
├── requirements.txt          # Dependências Python (Django, DRF, SimpleJWT, coverage, etc.)
├── core/                     # Configurações centrais (settings c/ SQLite, urls, wsgi)
└── apps/                     # Módulos e aplicações do sistema
    ├── users/                # Autenticação JWT, perfil de usuário e quiz de suitability
    │   └── tests/            # Suíte modularizada (unit/, integration/, factories.py)
    ├── investments/          # Motor de projeção, sugestão, rebalanceamento e YFinance
    │   ├── management/       # Scripts de povoamento (seed_investments)
    │   └── tests/            # Suíte modularizada (unit/, integration/)
    └── wallets/              # Carteira individual, ativos, sinais e integridade de saldo
        └── tests/            # Suíte modularizada (unit/, integration/, factories.py)
```

## Execução de Testes e Cobertura

A partir do diretório `backend/`:

```bash
# Executar toda a suíte com medição de cobertura (comandos C0 + branches C1)
../.venv/bin/coverage run manage.py test --verbosity=2

# Exibir relatório no terminal (com gate mínimo de 80%)
../.venv/bin/coverage report --fail-under=80

# Gerar relatório visual HTML (htmlcov/index.html)
../.venv/bin/coverage html

# Validar independência dos testes (ordem aleatória — princípio FIRST)
../.venv/bin/python manage.py test --shuffle

# Executar apenas uma camada ou app específico
../.venv/bin/python manage.py test apps.users.tests.unit apps.wallets.tests.unit
../.venv/bin/python manage.py test apps.users.tests.integration apps.wallets.tests.integration
```

## Divisão de Responsabilidades Implementadas (Histórias de Usuário)

- **Pedro & Cauã (Backend)**:
  - Catálogo de Ativos com integração `yfinance` para cotações em tempo real (`apps/investments/`).
  - Motor matemático de projeção de rentabilidade composta no tempo (`apps/investments/`).
  - Quiz de perfil de investidor (`apps/users/services.py`) e algoritmo de sugestão/rebalanceamento (`apps/investments/`).
- **Mateus (Fullstack — Persistência e Credenciamento)**:
  - Sistema seguro de autenticação JWT (registro, login, rotação/blacklist de refresh, logout e perfil) em `apps/users/`.
  - Arquitetura e integridade relacional de Carteiras, itens, sinais automáticos e rentabilidade estimada em `apps/wallets/`.
  - Modularização da suíte de testes e infraestrutura de cobertura (`coverage.py`).
