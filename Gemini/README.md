# WEB-02 BI Dashboard 📊

Uma aplicação Client-Server completa projetada para ingestão, higienização e visualização interativa de dados tabulares (CSV). O sistema permite que os usuários façam upload de conjuntos de dados, mapeiem colunas críticas (Data, Categoria, Valor) e explorem métricas em um painel interativo com filtros de tempo e categorias.

Este projeto também serve como um caso de estudo prático para a avaliação da geração de código e autonomia de IA, apresentando um isolamento rigoroso de regras de negócios e segurança.

## 🚀 Funcionalidades

- **Autenticação Segura:** Sistema completo de Login/Registro utilizando hash de senhas (`bcrypt`) e tokens JWT de curta duração. Proteção nativa contra injeção SQL via SQLAlchemy ORM.
- **Ingestão e Higienização de Dados (CSV):** Validação rigorosa de dados. Linhas corrompidas ou com dados faltantes (nas colunas obrigatórias) são sumariamente descartadas para preservar a integridade matemática, sem "alucinar" ou preencher números falsos.
- **Remoção Global de Espaços:** Limpeza automática de espaços em branco não intencionais (whitespace stripping) em todas as colunas de texto do conjunto de dados.
- **Dashboard Interativo:**
  - **KPIs em Tempo Real:** Soma Total, Média e Contagem de Registros válidos.
  - **Gráficos Dinâmicos:** Gráficos de Linha (Série Temporal) e de Barras (Distribuição de Categorias) estilizados com dark-mode, construídos sobre a biblioteca `recharts`.
- **Filtros Avançados:** Filtre todo o Dashboard definindo um intervalo de datas (`Start Date`, `End Date`) e pesquisando múltiplas categorias específicas simultaneamente.
- **Exportação (Download):** Os usuários podem baixar um relatório final em CSV (`Export Dashboard to CSV`) contendo a versão higienizada dos dados da sua sessão de pesquisa associados às métricas geradas.

## 🛠️ Tecnologias Utilizadas

### Frontend
- **React** (TypeScript)
- **Vite** (Build Tool super-rápida)
- **Recharts** (Visualização de dados/Gráficos)
- **Vanilla CSS** (Estilização responsiva sem dependências pesadas de framework)

### Backend
- **Python / FastAPI**
- **Pandas** (Motor principal para parsing vetorizado e limpeza veloz do CSV)
- **SQLite / SQLAlchemy** (Banco de dados e ORM)
- **Bcrypt & PyJWT** (Segurança e Autenticação)

## 📁 Estrutura do Projeto

```text
TrabalhoTopicosX/
├── backend/                  # API FastAPI (Python)
│   ├── main.py               # Rotas e Endpoints
│   ├── analytics.py          # Lógica de cálculo de KPIs, Filtros e agregação do Pandas
│   ├── dataset_ingestion.py  # Upload de arquivos, validação estrita e limpeza CSV
│   ├── security.py           # Configurações de hashing e emissão de JWT
│   ├── models.py             # Modelos do BD (SQLAlchemy)
│   └── tests/                # Suíte de testes automatizados (pytest)
│
├── frontend/                 # Interface React (TypeScript)
│   ├── vite.config.ts        # Configuração (inclui regras de proxy local)
│   └── src/
│       ├── pages/
│       │   └── Dashboard.tsx # Componente mestre (Wizard de Upload -> Mapping -> Visualização)
│       └── services/
│           └── api.ts        # Ponto central para as chamadas de rede (fetch) e tipagem
│
├── docs/                     # Documentação de Arquitetura (ADRs) e Issues do Projeto
└── execução/                 # Manuais de como rodar a aplicação localmente
```

## 🏁 Como Executar (Ambiente Local)

Temos um arquivo dedicado explicando como subir o ambiente localmente.
👉 **Por favor, consulte [execução/COMO_RODAR.md](./execução/COMO_RODAR.md) para o passo-a-passo detalhado de instalação.**

*Em resumo:*
1. **Backend:** Instale o Python, crie um `venv`, instale os `requirements.txt` e inicie o servidor com `uvicorn main:app --reload --port 8001`.
2. **Frontend:** Instale o Node.js, rode `npm install` dentro da pasta `frontend/` e inicie com `npm run dev`.

## 🧪 Suíte de Testes e Metodologia

Todo o núcleo lógico do sistema (`dataset_ingestion` e `analytics`) e as rotas críticas de autenticação foram construídos sob a metodologia de **Test-Driven Development (TDD)**. 

Para rodar os testes unitários da aplicação, vá até a pasta raiz do `backend/` e execute:
```bash
pytest tests/
```

## 🤖 Relatórios de IA (Gemini & Claude)

Este projeto foi objeto de um estudo comparativo de desenvolvimento assistido por IA.
Os relatórios de avaliação do Gemini CLI sobre os 5 laboratórios metodológicos propostos estão disponíveis na pasta `docs/` deste projeto.
A implementação equivalente gerada pelo Claude está na pasta [`../Claude/`](../Claude/), e a comparação completa entre as duas ferramentas pode ser vista em [`../apresentacao.html`](../apresentacao.html).
