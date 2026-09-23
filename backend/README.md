# FinLess - Backend (Django)

Este diretório contém a API e lógica de negócio do sistema **FinLess**.

## Estrutura Sugerida

```text
backend/
├── manage.py             # Script de gerenciamento do Django
├── core/                 # Configurações centrais do Django (settings, urls, wsgi)
├── apps/                 # Módulos e aplicações do sistema
│   ├── users/            # Autenticação, perfis e controle de usuários
│   ├── investments/      # Cálculos, projeções, sugestões e perfil de investidor
│   └── wallets/          # Gerenciamento da carteira individual e ativos
├── requirements.txt      # Dependências Python (Django, psycopg2, etc.)
└── tests/                # Testes automatizados da API
```

## Divisão de Responsabilidades (Histórias de Usuário)

- **Pedro & Cauã (Backend)**:
  - Sugestões de investimentos e tipos de ativos (`apps/investments/`)
  - Projeção de rentabilidade e cálculo de ganhos no tempo (`apps/investments/`)
  - Algoritmo de identificação do perfil de investidor e alocação (`apps/investments/`)
- **Mateus (Fullstack)**:
  - Sistema de cadastro, autenticação e sessão de usuários (`apps/users/`)
  - Estrutura e persistência das carteiras dos usuários (`apps/wallets/`)
