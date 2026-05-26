# Relatório de Avaliação de Ferramenta de IA: Gemini CLI

## 1. Problema Escolhido e Visão Geral
**Problema:** WEB-02 - Dashboard de BI/Analytics a partir de CSV (KPIs + filtros)
**Ferramenta Avaliada:** Gemini CLI (Agent AI Autônomo)

O objetivo do projeto foi construir uma aplicação capaz de receber arquivos CSV, validar as colunas, limpar os dados (removendo linhas defeituosas), e gerar painéis interativos (KPIs e Gráficos de barras/linhas) sem "inventar" números. Adicionalmente, para cumprir o rigoroso checklist de segurança exigido pela disciplina, o escopo foi expandido para incluir autenticação completa (JWT e senhas com hash).

## 2. Metodologia de Desenvolvimento
Para avaliar o Gemini CLI de forma robusta e evitar a geração de um "código espaguete", adotamos um processo altamente estruturado:

1. **Grill-with-Docs (Entrevista Inicial):** O agente AI não começou a programar imediatamente. Ele utilizou uma skill chamada `grill-with-docs` para entrevistar o usuário, tomar decisões arquiteturais e criar um glossário (`CONTEXT.md`) e registros de decisão arquitetural (ADRs).
2. **Arquitetura Cliente-Servidor:** Decidimos utilizar **React (TypeScript) + Vite** no Frontend e **Python (FastAPI) + SQLite** no Backend. O Python foi escolhido estrategicamente pela facilidade de usar a biblioteca `pandas` para a manipulação de dados pesados exigida na Issue.
3. **PRD e Quebra de Tarefas:** O agente transformou a conversa em um *Product Requirements Document* (PRD) e quebrou o projeto em 7 *Vertical Slices* (Issues), permitindo um desenvolvimento passo a passo.
4. **Test-Driven Development (TDD):** Todo o backend foi construído através da skill de TDD. O agente escrevia testes automatizados (em `pytest`) que falhavam (RED), e em seguida implementava o código mínimo para que passassem (GREEN), garantindo a corretude.

## 3. Diário de Prompts e Iterações

A interação com o Gemini CLI ocorreu em formato de conversa contínua, onde o agente assumia o papel de um Engenheiro de Software Sênior. 

*   **Prompt Inicial:** `"leia o arquivo COMOFAZER que esta nessa PASTA, e use o grill-with-docs"`
    *   *Ação do Agente:* Leu os requisitos e iniciou uma entrevista. Notou um conflito entre o escopo simples do WEB-02 e o checklist de segurança global da disciplina, sugerindo proativamente a criação de um sistema de Login/Registro.
*   **Prompt de Implementação:** `"vamos fazer a 2 com tdd"` (Referente à Issue #2 - Upload de CSV).
    *   *Ação do Agente:* Criou o banco de dados `datasets`, a rota de upload e o teste automatizado. 
    *   *Problema:* O agente tentou instalar dependências (`pandas`, `python-multipart`) que acabaram caindo no Python global em vez do ambiente virtual (venv).
*   **Prompt de Debug 1:** Usuário relatou demora no processamento: `"acho que escolhi um arquivo grande, esta demorando mt para processar"`
    *   *Ação do Agente:* O agente identificou que o Pandas estava usando a inferência padrão de datas, que é lenta. Otimizou o código alterando para `format='mixed'` e utilizando métodos vetorizados para strings, deixando o processo instantâneo.
*   **Prompt de Debug 2:** `"ele nao faz login nem faz registro também, confira algo que voce deixou passar ou apagou"`
    *   *Ação do Agente:* O agente fez um diagnóstico remoto e identificou dois problemas raros de infraestrutura no Windows do usuário:
        1. **QuickEdit Mode:** O terminal do Windows estava pausando o processo do Uvicorn porque o usuário clicou na tela (modo de seleção). O agente identificou o quadrado branco na screenshot e ensinou o usuário a apertar `ESC`.
        2. **Processo Fantasma:** Após sucessivos testes, uma instância fantasma do Uvicorn ficou travada na porta 8000. O agente resolveu alterando autonomamente a configuração do proxy do Vite (React) e pedindo para o usuário rodar o servidor na porta `8001`.
*   **Prompt de Correção de Erro (ParserError):** `"Unexpected token 'I', "Internal S"... is not valid JSON"`
    *   *Ação do Agente:* O agente simulou o envio do CSV sujo (`dados_teste_erros.csv`), leu o traceback gerado pelo FastAPI (Erro 500) e descobriu que o arquivo possuía colunas a mais/a menos. O agente corrigiu adicionando `on_bad_lines='skip'` no Pandas e envolvendo a rota num `try/except` para retornar Erro 400 em vez de 500, protegendo a aplicação.

## 4. Resultados Alcançados

O sistema entregue possui:
*   **Segurança (100% aderente ao checklist):** Senhas usando `bcrypt` com hash e salt, autenticação por tokens JWT, e validação contra SQL Injection nativa através do uso do ORM (SQLAlchemy).
*   **Dashboard Interativo:** Upload "two-step" (validação e depois mapeamento de colunas). Uso rigoroso do Pandas para limpeza de dados (Strict Row Deletion) e agregação para KPIs.
*   **Interface Rica:** Gráficos de Tendência Temporal (LineChart) e Categorias (BarChart) desenhados com a biblioteca Recharts, reagindo de forma dinâmica aos dados enviados.

## 5. Análise Crítica do Gemini CLI

### O que funcionou muito bem
*   **Autonomia:** A ferramenta não é apenas um "gerador de código", é um agente. Ela executa comandos no terminal, cria pastas, roda os próprios testes, lê os logs de erro e corrige a si mesma.
*   **Arquitetura:** O uso do TDD forçou a criação de código altamente modular (ex: separação da lógica complexa de Pandas em um "deep module" chamado `dataset_ingestion.py`, separado das rotas da API).
*   **Resolução de Problemas (Troubleshooting):** A capacidade do agente de identificar problemas de ambiente, como portas ocupadas (Port 8000 em uso) e o congelamento do terminal Windows, foi impressionante e economizou horas de depuração que normalmente frustrariam desenvolvedores iniciantes.

### O que falhou / Riscos
*   **Dependências de Ambiente:** O agente teve um pouco de dificuldade no início para garantir que os pacotes `pip` fossem instalados **dentro** do ambiente virtual correto (`venv`), devido a restrições de execução de scripts do PowerShell (`ExecutionPolicy`).
*   **Migrações de Banco de Dados:** Quando o modelo do SQLAlchemy foi atualizado com novas colunas (Issue #3), o SQLite não aplicou a mudança sozinho. O agente causou um crash na aplicação (no table column), mas foi rápido em identificar a falha através dos logs e rodar um script `ALTER TABLE` manual.

### Recomendações de Uso
*   **Uso Iterativo:** Não peça para a IA construir o projeto inteiro de uma vez. O uso da metodologia *Vertical Slices* (Issues individuais) funcionou perfeitamente para manter o contexto pequeno e o código livre de bugs.
*   **Forneça Contexto:** Sempre envie logs, mensagens de erro do navegador ou até mesmo screenshots (como fizemos) quando a aplicação não se comportar como esperado. O Gemini foi capaz de "ler" a interface e os terminais para inferir o estado do sistema com precisão.

### Economia de Tempo
Estima-se uma economia de **pelo menos 70% a 80% do tempo de desenvolvimento**. O que levaria dias (configurar React, FastAPI, Banco de Dados, testes, lógica de agregação do Pandas, segurança JWT e CSS), foi realizado em apenas uma sessão contínua, com a maior parte do tempo humano gasto apenas testando e validando as entregas.
