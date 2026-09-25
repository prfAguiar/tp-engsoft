# 🚀 FinLess - Calculadora de Investimentos Premium

> Trabalho Prático da disciplina de Engenharia de Software  
> **Professor:** Marco Tulio Valente

### 👥 Integrantes 

- **Cauã Neto Santos Pires** (Backend)
- **Mateus Matsura Teles Costa** (Fullstack)
- **Pedro Rangel Ferreira de Aguiar** (Backend)
- **Renato Vilela de Melo Pacheco Pinto** (Frontend)

---
## 🎯 Tópico Central: Calculadora de Aplicações Financeiras

### Objetivo do Sistema
**Calculadora para organização e planejamento de investimentos financeiros.**
O sistema tem como objetivo auxiliar pessoas na **organização e no planejamento de seus investimentos financeiros**.  A partir do montante disponível, dos ativos escolhidos e do perfil de investidor, a aplicação sugere uma **divisão adequada dos recursos**.  A calculadora busca facilitar a tomada de decisões, tornando o processo de **investimento mais simples e acessível**, sugerindo além da divisão do montante, a quantidade a ser investida por ativo. Cada usuário terá uma **carteira individual e protegida**, garantindo privacidade e segurança sobre suas informações financeiras.  Futuramente, o sistema poderá incluir recursos como definição de metas, controle de gastos e planejamento para alcançar um patrimônio desejado.

### 🛠️ Tecnologias e Arquitetura 
- **Frontend:** Vue.js (Vite)
- **Backend:** Django REST Framework
- **Database:** PostgreSQL (Local via SQLite)

#### Agentes de IA:
- Google Antigravity, OpenAI Codex.
- *OBS:* ChatBots como Google Gemini, ChatGPT e Claude em casos de limitação dos agentes.

---
## 📖 Histórias de Usuário

- Como usuário, gostaria de poder me cadastrar e salvar meus dados entre sessões.
- Como usuário, gostaria de poder visualizar e/ou alterar meus dados e carteira de investimento.
- Como usuário, gostaria de acessar meus dados e resultados por meio de gráficos informativos.
- Como usuário, gostaria de receber sugestões dos tipos de investimentos.
- Como usuário, gostaria de consultar as características de um investimento para avaliar seus riscos, rentabilidade e prazo.
- Como usuário, gostaria de projetar meus ganhos em um intervalo de tempo.
- Como usuário, gostaria de descobrir meu perfil de investimento.
- Como usuário, gostaria de indicar um montante para sugestão.

---
## ⚙️ Guia de Execução e Testes Locais

Para que a autenticação de contas e persistência de dados funcionem, **ambos os servidores precisam estar rodando simultaneamente** em dois terminais diferentes.

### 1. Configurando o Backend (Terminal 1)
O backend utiliza Python e Django. Na raiz do projeto, configure o ambiente:

**1.1. Criar e Ativar o Ambiente Virtual:**
O ambiente virtual (VENV) isola as bibliotecas do projeto do resto da sua máquina.
```bash
python3 -m venv .venv
source .venv/bin/activate  # No Windows (PowerShell): .\.venv\Scripts\Activate.ps1
```

**1.2. Instalar as Dependências:**
Com o ambiente ativado (você verá `(.venv)` no terminal), instale as bibliotecas necessárias.
```bash
pip install -r backend/requirements.txt
```

**1.3. Migração Obrigatória do Banco de Dados:**
Este comando cria o arquivo `db.sqlite3` e constrói as tabelas de Usuários. Se você pular este passo, o sistema dará erro de "Tabela não encontrada" (500).
```bash
cd backend
python manage.py migrate
```

**1.4. Iniciar o Servidor Django:**
Mantenha este terminal aberto rodando em segundo plano (`http://localhost:8000/`).
```bash
python manage.py runserver
```

### 2. Configurando o Frontend (Terminal 2)
O frontend utiliza Node.js e Vue 3. Abra um **novo terminal** na raiz do projeto:

**2.1. Instalar as Bibliotecas Node:**
Faz o download da pasta `node_modules` contendo o Vue, Vite, Pinia e o Axios.
```bash
cd frontend
npm install
```

**2.2. Iniciar o Servidor de Desenvolvimento Vue.js:**
```bash
npm run dev
```

### 3. Replicabilidade do Teste de Autenticação
1. Acesse **`http://localhost:5173/`** no seu navegador.
2. O **Router Guard** irá barrar o acesso à página principal e redirecionar você para a página segura de Login.
3. Clique em **"Crie uma conta"**. Explore o formulário, experimente errar senhas, ou inserir contas duplicadas para testar o painel visual de tratamento de erros interligado ao banco de dados.
4. Após concluir seu cadastro, faça Login. O token JWT autorizará sua entrada e a **Navbar Premium** no topo exibirá saudações dinâmicas resgatando o seu nome diretamente do perfil salvo.





