# 📊 Dashboard de BI — Claude vs. Gemini CLI

Estudo comparativo de geração de código assistida por IA, feito para a disciplina de **Tópicos Especiais em Computação (UFMS)**. O mesmo problema (**WEB-02 — dashboard de BI/analytics a partir de CSV**) foi resolvido duas vezes, de forma independente, por duas ferramentas de IA diferentes — mesma especificação, mesmos critérios de avaliação, resultados comparados lado a lado.

<p>
  <img alt="Claude" src="https://img.shields.io/badge/Claude-chat_assistant-CC785C">
  <img alt="Gemini CLI" src="https://img.shields.io/badge/Gemini_CLI-agente_aut%C3%B4nomo-4285F4?logo=googlegemini&logoColor=white">
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-backend-009688?logo=fastapi&logoColor=white">
  <img alt="React" src="https://img.shields.io/badge/React-frontend-61DAFB?logo=react&logoColor=black">
</p>

## 📊 Ver a comparação

👉 Abra [`apresentacao.html`](./apresentacao.html) no navegador — tem o problema, a metodologia, os laboratórios de avaliação, os resultados e o histórico de prompts das duas implementações, com os dois dashboards lado a lado.

## Estrutura

```
Gemini/    implementação gerada com Gemini CLI (agente autônomo de terminal)
Claude/    implementação gerada com Claude (assistente de chat)
```

Cada pasta é um projeto completo e independente — backend (FastAPI) + frontend (React + Vite) — com sua própria documentação (`docs/PRD.md`, `docs/adr/`, `docs/issues/`) e diário de iteração real (`RelatorioNovo.txt`), não só o resultado final.

## O problema (WEB-02)

Ingerir um CSV "sujo", higienizar os dados, mapear colunas (data/categoria/valor) via assistente de 2 passos, e gerar um dashboard com KPIs, série temporal, gráfico por categoria e exportação — com filtros interativos que recalculam tudo dinamicamente.

## Rodando localmente

Cada implementação roda de forma independente:

```bash
cd Gemini   # ou Claude
cat COMOFAZER.txt   # enunciado do trabalho
# backend
cd backend && pip install -r requirements.txt && python main.py
# frontend (outro terminal)
cd frontend && npm install && npm run dev
```

Veja `Gemini/README.md` e `Claude/QUICK_START.md` para detalhes específicos de cada uma.

## Por que isso importa

Não é só "duas cópias do mesmo trabalho" — é uma avaliação metódica de como um agente autônomo de terminal (Gemini CLI) se compara a um assistente de chat (Claude) no mesmo problema real, com os mesmos critérios de correção, qualidade e organização de código. A apresentação documenta prompts, decisões e o "antes/depois" de cada laboratório de avaliação.

## Licença

[MIT](./LICENSE)

## Autor

[Pedro Bertoncelo](https://github.com/PedroBertonceloF) — Ciência da Computação (UFMS)
