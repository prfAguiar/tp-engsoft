# Regras de Commit do Projeto

Sempre que realizar commits neste repositório, o agente deve seguir estritamente as regras abaixo:

1. **Conventional Commits**: O padrão Conventional Commits deve ser usado em todas as mensagens de commit (ex: `feat:`, `fix:`, `refactor:`, `docs:`, `style:`, `test:`, `perf:`, `build:`, `chore:`, `revert:`).
2. **Limite de Linhas de Código (LOC)**: Cada commit deve conter no máximo **100 Linhas de Código (LOC)** alteradas.
3. Se houver alterações que superem 100 LOC, elas devem ser divididas lógicamente em múltiplos commits menores, usando `git add -p` ou adicionando arquivos/linhas de forma iterativa, antes de realizar o push para o GitHub.
