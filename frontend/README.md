# FinLess - Frontend (Vue.js)

Este diretório contém a interface de usuário web do sistema **FinLess**.

## Estrutura Implementada

```text
frontend/
├── public/               # Arquivos estáticos públicos (ícones, favicon)
├── src/
│   ├── assets/           # Estilos globais (Glass-morphism, paleta Premium Dark)
│   ├── components/       # Componentes Vue reutilizáveis (Navbar global, Cards)
│   ├── views/            # Telas principais (DashboardView, WalletView, LoginView, etc)
│   ├── router/           # Configuração de rotas de navegação com Router Guards (proteção JWT)
│   ├── services/         # Integração com a API Backend (Axios Interceptors)
│   ├── store/            # Gerenciamento de estado de usuário (Pinia)
│   ├── App.vue           # Componente raiz
│   └── main.js           # Ponto de entrada da aplicação
├── package.json          # Dependências (Vue 3, vue-chartjs, pinia)
└── vite.config.js        # Configuração do Vite/Vue
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
