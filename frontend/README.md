# FinLess - Frontend (Vue.js)

Este diretório contém a interface de usuário web do sistema **FinLess**.

## Estrutura Implementada

```text
frontend/
├── public/               # Arquivos estáticos públicos (ícones, favicon)
├── e2e/                  # Suíte de testes End-to-End (Playwright)
│   ├── helpers.js
│   ├── auth-guard.spec.js
│   ├── quiz-suggestion.spec.js
│   ├── catalog-modal.spec.js
│   └── wallet-dashboard.spec.js
├── src/
│   ├── assets/           # Estilos globais (Glass-morphism, paleta Premium Dark)
│   ├── components/       # Componentes Vue reutilizáveis (Navbar global, Cards)
│   ├── views/            # Telas principais (DashboardView, WalletView, LoginView, etc)
│   ├── router/           # Configuração de rotas de navegação com Router Guards (proteção JWT)
│   ├── services/         # Integração com a API Backend (Axios Interceptors)
│   ├── store/            # Gerenciamento de estado de usuário (Pinia)
│   ├── App.vue           # Componente raiz
│   └── main.js           # Ponto de entrada da aplicação
├── package.json          # Dependências (Vue 3, vue-chartjs, pinia, @playwright/test)
├── playwright.config.js  # Orquestração dos servidores Backend + Vite para testes E2E
└── vite.config.js        # Configuração do Vite/Vue
```

## Execução dos Testes End-to-End (Playwright)

A partir do diretório `frontend/`:

```bash
# Executar toda a suíte E2E (sobe automaticamente Backend Django :8000 e Vite :5173)
npm run test:e2e

# Executar um fluxo específico
npx playwright test e2e/auth-guard.spec.js
npx playwright test e2e/quiz-suggestion.spec.js
npx playwright test e2e/catalog-modal.spec.js
npx playwright test e2e/wallet-dashboard.spec.js
```

## Divisão de Responsabilidades Implementadas (Histórias de Usuário)

- **Renato (Frontend)**:
  - Criação da identidade visual Premium (Dark Mode, Glass-morphism, tons de ouro).
  - Desenvolvimento das interfaces principais (Dashboard dinâmico e gráficos Chart.js).
  - Estruturação do formulário de Quiz/Perfil e navegação fluida da plataforma.
- **Mateus (Fullstack)**:
  - Telas de Autenticação, Registro seguro e integração de Estado Global (Pinia).
  - Lógica de persistência de sessão JWT via Axios Interceptors no `services/api.js`.
  - Tratamento de Empty States matemáticos e acoplamento estrito entre a Carteira e a Projeção.
