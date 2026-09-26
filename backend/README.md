# FinLess - Backend (Django)

Este diretório contém a API e lógica de negócio do sistema **FinLess**.

## Estrutura Implementada

```text
backend/
├── manage.py             # Script de gerenciamento do Django
├── core/                 # Configurações centrais (settings c/ Postgres, urls, wsgi)
├── apps/                 # Módulos e aplicações do sistema
│   ├── users/            # API de Autenticação (JWT) e controle de usuários
│   ├── investments/      # Motor de Projeção, Algoritmo de Sugestão e Integração YFinance
│   │   └── management/   # Scripts de povoamento (seed_investments)
│   └── wallets/          # Gerenciamento da carteira individual e ativos
├── requirements.txt      # Dependências Python (Django, psycopg[binary], yfinance)
└── tests/                # Testes automatizados da API
```

## Divisão de Responsabilidades Implementadas (Histórias de Usuário)

- **Pedro & Cauã (Backend)**:
  - Desenvolvimento do Catálogo de Ativos com integração `yfinance` para cotações em tempo real (`apps/investments/`).
  - Motor matemático de projeção de rentabilidade composto no tempo (`apps/investments/`).
  - Algoritmo de Sugestão baseado em alocação de risco (Conservador, Moderado, Agressivo).
  - Povoamento do banco de dados relacional (PostgreSQL) com ativos da B3.
- **Mateus (Fullstack)**:
  - Sistema seguro de autenticação JWT e registro de usuários (`apps/users/`).
  - Arquitetura de Carteiras atreladas aos perfis de risco (`apps/wallets/`).
  - Cálculo dinâmico de rentabilidade média ponderada baseada no extrato do usuário.
