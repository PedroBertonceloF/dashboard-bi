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
4. **Test-Driven Development (TDD):** Todo o backend foi construído através da skill de TDD. O agente escrevia testes automatizados (em `pytest`) que falhavam (RED), e em seguida implementava o código mínimo para que passassem (GREEN), garantindo a corretude. Ao final do projeto, 12 testes de integração cobriam todo o fluxo de dados.

## 3. Diário de Prompts e Iterações

A interação com o Gemini CLI ocorreu em formato de conversa contínua, onde o agente assumia o papel de um Engenheiro de Software Sênior. 

*   **Prompt Inicial:** `"leia o arquivo COMOFAZER que esta nessa PASTA, e use o grill-with-docs"`
    *   *Ação do Agente:* Leu os requisitos e iniciou uma entrevista. Notou um conflito entre o escopo simples do WEB-02 e o checklist de segurança global da disciplina, sugerindo proativamente a criação de um sistema de Login/Registro.
*   **Prompt de Implementação:** `"vamos fazer a 2 com tdd"` (Referente à Issue #2 - Upload de CSV).
    *   *Ação do Agente:* Criou o banco de dados `datasets`, a rota de upload e o teste automatizado. 
*   **Prompt de Debug (Performance):** `"acho que escolhi um arquivo grande, esta demorando mt para processar"`
    *   *Ação do Agente:* O agente identificou que o Pandas estava usando a inferência padrão de datas, que é lenta. Otimizou o código alterando para `format='mixed'` e utilizando métodos vetorizados para strings, deixando o processo instantâneo.
*   **Prompt de Debug (Ambiente Windows):** `"ele nao faz login nem faz registro também..."`
    *   *Ação do Agente:* O agente identificou dois problemas de infraestrutura no Windows:
        1. **QuickEdit Mode:** O terminal do Windows pausava o processo do Uvicorn por causa de cliques acidentais na tela. O agente ensinou o usuário a destravar com `ESC`.
        2. **Processo Fantasma:** Uma instância do servidor travou na porta 8000. O agente alterou autonomamente a configuração para a porta `8001`.
*   **Prompt de Melhoria (Higienização):** `"quero fazer com que eu limpe não só os dados que eu escolhi, mas todos os dados limpos da tabela inteira"`
    *   *Ação do Agente:* Utilizou a skill `interview-me` para entender que o usuário queria uma ferramenta de limpeza profissional. Implementou via TDD um sistema que: preserva todas as colunas originais no CSV de saída, remove espaços em branco (`strip`) de todos os textos da tabela e aplica a exclusão rigorosa apenas nas colunas essenciais mapeadas.
*   **Prompt de Ajuste Visual:** `"não quero que a legenda do grafico fique para fora..."`
    *   *Ação do Agente:* Ajustou os paddings de CSS e as margens internas do Recharts para garantir que os eixos e legendas fossem legíveis em qualquer resolução.
*   **Prompt de Documentação Final:** `"crie uma pasta chamada execução e coloque so o que escrever para exectuar o back e o front"`
    *   *Ação do Agente:* Criou a pasta `execução/` e o arquivo `COMO_RODAR.md`, centralizando o manual de instrução do projeto.

## 4. Resultados Alcançados

O sistema entregue possui:
*   **Segurança (100% aderente ao checklist):** Senhas usando `bcrypt`, autenticação JWT, e proteção contra SQL Injection via ORM.
*   **Higienizador de Dados Profissional:** O arquivo exportado (`_cleaned.csv`) é uma versão higienizada do original, com remoção global de espaços em branco e manutenção da estrutura de colunas original.
*   **Dashboard Interativo Completo:** KPIs matematicamente validados e gráficos interativos (Line/Bar) que reagem a filtros de intervalo de datas e multi-seleção de categorias em tempo real.
*   **Histórico Git Organizado:** O projeto foi versionado em commits lógicos que contam a história da construção de cada funcionalidade.

## 5. Análise Crítica do Gemini CLI

### O que funcionou muito bem
*   **Resolução de Problemas (Troubleshooting):** A ferramenta foi capaz de diagnosticar problemas que não estavam no código, mas no sistema operacional (congelamento de terminal e portas ocupadas), demonstrando uma visão sistêmica que vai além da simples escrita de código.
*   **Capacidade de Entrevista (`interview-me`):** Em vez de implementar a primeira coisa que o usuário pedia, o agente usou técnicas de entrevista para extrair a real intenção (como na limpeza global de dados), evitando retrabalho.
*   **Leitura de Screenshots:** O agente conseguiu "olhar" para o terminal do usuário via imagem para detectar que o servidor estava travado no modo de seleção do Windows.

### O que falhou / Riscos
*   **Ambiente e PowerShell:** A instalação de bibliotecas no ambiente virtual (`venv`) falhou algumas vezes devido a permissões de execução do Windows, exigindo que o agente desse comandos explícitos usando o caminho completo do executável do Python.
*   **Migrações Manuais:** Como o projeto usa SQLite, atualizações no modelo de dados exigiram scripts de migração (`ALTER TABLE`) manuais, pois o SQLAlchemy não atualiza esquemas existentes automaticamente.

### Economia de Tempo
Estima-se uma economia de **pelo menos 80% do tempo de desenvolvimento**. O agente resolveu em minutos problemas de limpeza de dados e gráficos que exigiriam horas de pesquisa em documentações. A maior parte do esforço humano foi redirecionada para a validação das regras de negócio e testes de usabilidade.

## 6. Evidências dos Laboratórios (Plano de Projeto V2)
Para cumprir a metodologia experimental do trabalho, realizamos os 5 laboratórios de stress-test descritos no Plano de Projeto V2:

1.  **Lab 1: Otimização e Performance:** Refatoramos a lógica de datas do Pandas (prompt: *"acho que escolhi um arquivo grande, esta demorando mt"*) utilizando `format='mixed'`, resultando em processamento instantâneo.
2.  **Lab 2: Edge Cases e Testes:** Implementamos tratamento de erro para CSVs com colunas ausentes ou extras (prompt: *"Unexpected token 'I'..."*) usando `on_bad_lines='skip'`, garantindo que o sistema não trave com dados sujos.
3.  **Lab 3: Auditoria de Segurança:** Implementamos do zero o sistema de JWT e `bcrypt` no `security.py`, cumprindo 100% do checklist de segurança e LGPD da disciplina.
4.  **Lab 4: Acessibilidade e UX:** Criamos a interface de upload e filtros no `Dashboard.tsx` (prompt: *"vamos para o frontend agora"*) com controles intuitivos e feedback visual imediato.
5.  **Lab 5: Resiliência a Alucinações:** Adotamos a política rigorosa de *"Não inventar números"*. O `analytics.py` foi configurado para retornar `0.0` ou listas vazias em casos de filtros sem dados, em vez de interpolar ou alucinar valores (conforme prompt de stress do usuário).
