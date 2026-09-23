# FinLess - Frontend (Vue.js)

Este diretório contém a interface de usuário web do sistema **FinLess**.

## Estrutura Sugerida

```text
frontend/
├── public/               # Arquivos estáticos públicos (ícones, favicon)
├── src/
│   ├── assets/           # Imagens, estilos globais e ícones
│   ├── components/       # Componentes Vue reutilizáveis (gráficos, cards, inputs)
│   ├── views/            # Telas principais (Dashboard, Carteira, Calculadora, Login)
│   ├── router/           # Configuração de rotas de navegação
│   ├── services/         # Integração com a API Backend (Axios / Fetch)
│   ├── store/            # Gerenciamento de estado (Pinia / Vuex)
│   ├── App.vue           # Componente raiz
│   └── main.js           # Ponto de entrada da aplicação
├── package.json          # Dependências e scripts do Node.js
└── vite.config.js        # Configuração do Vite/Vue
```

## Divisão de Responsabilidades (Histórias de Usuário)

- **Renato (Frontend)**:
  - Navegação e interface intuitiva (`src/views/` e `src/components/`)
  - Gráficos informativos e visualização de resultados e projeções (`src/components/`)
- **Mateus (Fullstack)**:
  - Telas de autenticação/cadastro e persistência de sessão (`src/views/`)
  - Integração das telas com as APIs de carteira e dados de investimentos (`src/services/`)
