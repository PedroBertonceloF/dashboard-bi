# Relatório Final: Metodologia Avançada de Avaliação Comparativa em IA
**Projeto:** WEB-02 (Dashboard de BI)
**Data:** 01 de Junho de 2026

---

## 1. Resumo Executivo
Este documento consolida os resultados da avaliação prática e teórica de ferramentas de Inteligência Artificial Generativa (com foco no modelo Claude em contrapartida à execução autônoma via Gemini CLI) na construção, segurança e otimização de uma aplicação Client-Server (React + FastAPI). A avaliação foi conduzida através de 3 Experimentos práticos, cobrindo 5 Laboratórios de *stress-test* definidos no "Plano de Ação Estratégico v2.0".

## 2. Metodologia
A avaliação utilizou a técnica de "Cérebro Algorítmico e Auditoria", onde códigos foram gerados pelo modelo testado (Claude) sob *prompts* estritos e, em seguida, inseridos diretamente na base de código local. A validação empírica foi realizada através da execução da suíte de testes automatizados (`pytest`) e análise de integração de infraestrutura.

---

## 3. Resultados Detalhados por Laboratório (Avaliação do Claude)

### 📊 Laboratório 1: Otimização e Performance Computacional
**Foco:** Qualidade e arquitetura na ingestão de dados massivos.
* **Nota: 2 / 5**
* **Análise:** O modelo falhou criticamente na conversão de tipos de dados. Ao invés de utilizar a vetorização nativa em C da biblioteca Pandas (`pd.to_datetime` com `format='mixed'` e `cache=True`), optou por aplicar uma função Python iterativa (`_is_valid_date`) com múltiplos blocos `try/except`. Essa decisão arquitetural resulta em lentidão severa para o processamento do volume alvo (1 milhão+ de linhas).
* **Solução Implementada (Gemini CLI):** Refatoração imediata para operações vetorizadas, alcançando aprovação total na suíte de testes.

### 🛡️ Laboratório 2: "Edge Cases" e Testes Unitários
**Foco:** Resiliência a dados corrompidos.
* **Nota: 1 / 5**
* **Análise:** Ausência de resiliência primária no *parser* de CSV. A instrução `pd.read_csv` foi utilizada sem o parâmetro `on_bad_lines='skip'`, garantindo que um arquivo com uma única linha malformada causasse um *crash* global (Erro 500) na API, impedindo qualquer tentativa de tratamento de erro posterior.

### 🔒 Laboratório 3: Auditoria de Segurança e LGPD
**Foco:** Implementação de JWT, Bcrypt e proteção contra injeções.
* **Nota: 5 / 5**
* **Análise:** O modelo demonstrou excelência técnica na construção do módulo de segurança. Implementou *salts* dinâmicos com 12 rounds no Bcrypt, truncou senhas preventivamente contra o limite de 72 bytes e gerenciou perfeitamente os *claims* de expiração de JWT. Na auditoria teórica, demonstrou profundo conhecimento sobre vulnerabilidades em bancos de dados, explicando corretamente que o SQLAlchemy ORM anula riscos de SQL Injection através do uso automático de *prepared statements*.

### 🖱️ Laboratório 4: Acessibilidade e UX (Interface)
**Foco:** Conectividade Frontend/Backend e feedback visual.
* **Nota: 5 / 5**
* **Análise:** Resolução perfeita do problema clássico de CORS em desenvolvimento local. O modelo diagnosticou a falha de 'Connection Refused' e configurou corretamente o `proxy` do Vite, evitando exposições inseguras no backend. Além disso, implementou alertas visuais e classes CSS específicas para tratamento de erros (`.alert-error`), garantindo que o usuário nunca encontre uma tela branca caso o servidor falhe.

### 🤖 Laboratório 5: Resiliência a Alucinações (Teste Cego)
**Foco:** Manutenção da veracidade dos dados e escopo do dataset.
* **Nota: 5 / 5**
* **Análise:** A lógica de limpeza de dados foi impecável no quesito "não inventar dados". Utilizando deleção estrita baseada em máscaras booleanas, a IA removeu perfeitamente linhas com valores corrompidos ou vazios sem tentar preenchê-los com médias fictícias. O uso de `.copy()` na filtragem garantiu a preservação de colunas extras não mapeadas, respeitando a resiliência do dataset.

---

## 4. Tabela Comparativa Final

| Critério de Avaliação | IA em Teste Cego (Claude) | Agente Autônomo (Gemini CLI) |
| :--- | :--- | :--- |
| **Autonomia de Execução** | Apenas geração de blocos de código em texto. | Execução de shell, correção de bugs de OS, integração contínua. |
| **Lab 1 (Performance)** | **2/5:** Loops Python lentos (`.apply`). | **5/5:** Uso de vetorização C (`format='mixed'`, `cache=True`). |
| **Lab 2 (Edge Cases)** | **1/5:** API suscetível a *crash* por *parser errors*. | **5/5:** Implementação de saltos preventivos (`on_bad_lines`). |
| **Lab 3 (Segurança)** | **5/5:** JWT e Bcrypt perfeitos. Domínio de ORMs. | **5/5:** Avaliação e execução nativa. |
| **Lab 4 (UX/Infra)** | **5/5:** Setup perfeito de Proxy e tratamento visual. | **5/5:** Implementação fluida. |
| **Lab 5 (Alucinações)** | **5/5:** Deleção estrita, preservou colunas extras. | **5/5:** Idem, com sintaxe refatorada via `dropna`. |

## 5. Conclusão da Pesquisa
O experimento demonstra que modelos de linguagem massivos (como o testado na Fase de Pesquisa) são **ferramentas de excelência para estruturação de padrões consolidados de mercado**, como autenticação (JWT) e configurações de infraestrutura frontend (Vite Proxy). A taxa de acerto foi máxima (5/5) em domínios onde o padrão não varia.

No entanto, a IA avaliada apresentou **fraquezas substanciais em domínios que requerem malícia algorítmica e experiência em ciência de dados pura**, como o uso da biblioteca Pandas. Ao priorizar a construção de loops legíveis em detrimento da performance vetorizada, e ao ignorar a instabilidade inerente de arquivos CSV do mundo real, a IA falhou nos Labs 1 e 2, exigindo a intervenção corretiva de um Agente (Gemini CLI) focado na passagem pela suíte de testes estritos (`pytest`).
