# Relatório de Resultados: Experimento 1 (Claude)
**Data da Avaliação:** 01 de Junho de 2026
**Módulo Avaliado:** `backend/dataset_ingestion.py` (Ingestão e Limpeza de Dados)
**Foco do Teste:** Cérebro Algorítmico (Labs 1, 2 e 5 do Plano de Projeto V2)

## 1. Ocorrência Prática (Testes Automatizados)
Ao integrar o código gerado pelo Claude diretamente na base de código local, **o sistema falhou na suíte de testes automatizados (`pytest`)**.

**Motivo da Falha:** 
O código do Claude gerou uma mensagem de erro genérica (`"Column 'X' not found"`) quando uma coluna mapeada não existia. A especificação do projeto e os testes unitários (`backend/tests/test_datasets.py`) exigiam estritamente a string `"Missing mapped columns"`. Isso demonstra que a IA não conseguiu inferir o padrão exato de tratamento de exceções esperado pela infraestrutura existente sem um contexto explícito da suíte de testes.

## 2. Notas por Laboratório (Métricas do Plano V2)

### 📊 Laboratório 1: Otimização e Performance Computacional
**Nota: 2 / 5**
* **Justificativa:** O código falhou criticamente na conversão de datas para grandes volumes de dados. Em vez de utilizar a vetorização nativa em C do Pandas (`pd.to_datetime` com `format='mixed'` ou `cache=True`), a IA utilizou um loop iterativo via `.apply()` com uma função Python customizada (`_is_valid_date`), contendo múltiplos blocos `try/except`. Essa abordagem degrada severamente a performance ao processar milhões de linhas.

### 🛡️ Laboratório 2: "Edge Cases" e Testes Unitários
**Nota: 1 / 5**
* **Justificativa:** A função de leitura inicial (`pd.read_csv`) não implementou resiliência contra linhas corrompidas (omissão do parâmetro `on_bad_lines='skip'`). Na presença de um CSV com uma única linha malformada, o código causaria um *crash* total na API (Erro 500), falhando no tratamento básico de "Edge Cases" em ambientes de produção reais.

### 🔒 Laboratório 3: Auditoria de Segurança e LGPD
**Nota: 2 / 5**
* **Justificativa:** A implementação focou apenas em verificar a extensão `.csv` no nome do arquivo, falhando em validar o conteúdo real ou o *MIME type*. Isso abre brechas de segurança para injeção de arquivos maliciosos. Além disso, não houve implementação de limites de tamanho para prevenir exaustão de disco.

### 🖱️ Laboratório 4: Acessibilidade e UX (Interface)
**Nota: N/A**
* **Justificativa:** Este módulo é estritamente backend. (Se avaliado apenas pelo retorno de erros, a nota seria mediana por levantar erros que precisam de tradução no frontend).

### 🤖 Laboratório 5: Resiliência a Alucinações (O Teste Cego)
**Nota: 5 / 5**
* **Justificativa:** A IA obteve excelência neste critério. A lógica de deleção foi rigorosa e cumpriu a regra fundamental de "não inventar números". A combinação de máscaras booleanas para limpar as linhas preservou perfeitamente as colunas não mapeadas, sem alucinar ou preencher dados faltantes com médias irreais.

## 3. Conclusão da Intervenção (Gemini CLI)
Para que o módulo funcionasse corretamente, foi necessária a reescrita (refatoração) do código via Gemini CLI, implementando:
1. `on_bad_lines='skip'` para evitar crashes de parser.
2. `pd.to_datetime(..., format='mixed', cache=True)` para performance massiva.
3. Ajuste fino nas exceções levantadas para alinhamento com a suíte de testes (`pytest`).
Após as correções, **todos os 17 testes passaram com sucesso.**

---

# Relatório de Resultados: Experimento 2 (Claude)
**Data da Avaliação:** 01 de Junho de 2026
**Módulo Avaliado:** `backend/security.py` (Módulo de Segurança e Auditoria)
**Foco do Teste:** Segurança e Auditoria (Lab 3 do Plano de Projeto V2)

## 1. Ocorrência Prática (Testes Automatizados)
Ao integrar o código gerado pelo Claude (o módulo `security.py`) diretamente na base de código local, **o sistema conectou perfeitamente e passou em todos os testes automatizados de autenticação (`pytest`)**. As assinaturas das funções estavam perfeitamente alinhadas com o que a API FastAPI (`main.py`) esperava.

## 2. Notas por Laboratório (Métricas do Plano V2)

### 🔒 Laboratório 3: Auditoria de Segurança e LGPD
**Nota: 5 / 5**
* **Justificativa:** O módulo gerado atendeu plenamente aos requisitos estritos de segurança definidos no gabarito do Experimento 2:
    * **Bcrypt & Salt:** A IA truncou as senhas para respeitar o limite de 72 bytes do bcrypt e utilizou *salts* gerados dinamicamente com 12 rounds de processamento.
    * **JWT Expiration:** A geração de tokens JWT respeitou estritamente a janela de expiração de 30 minutos solicitada.
    * **Auditoria (SQL Injection):** Na resposta textual (fornecida no arquivo `SECURITY_COMPLETE.txt`), a IA respondeu corretamente à pergunta teórica, explicando que o uso do SQLAlchemy ORM protege nativamente contra SQL Injection devido ao uso de *prepared statements*, ilustrando exemplos seguros e inseguros.
    * **Extras:** A IA foi proativa ao incluir validadores de força de senha, validação de formato de e-mail e uma função para injetar cabeçalhos de segurança HTTP (XSS, Clickjacking, etc.).

---

# Relatório de Resultados: Experimento 3 (Claude)
**Data da Avaliação:** 01 de Junho de 2026
**Módulos Avaliados:** `vite.config.ts`, `api.ts`, `Dashboard.tsx` (Frontend React)
**Foco do Teste:** UX e Infraestrutura (Lab 4 do Plano de Projeto V2)

## 1. Ocorrência Prática (Testes Manuais)
A IA gerou a configuração de build (Vite), a camada de serviço da API e o componente de interface em uma única resposta. O código React faz uso de bibliotecas modernas (`recharts`) e gerencia múltiplos estados de tela (Upload, Mapeamento, Dashboard) simulando um "Wizard".

## 2. Notas por Laboratório (Métricas do Plano V2)

### 🖱️ Laboratório 4: Acessibilidade e UX (Interface)
**Nota: 5 / 5**
* **Justificativa:** O código atendeu rigorosamente aos pontos do "Gabarito" definidos para o Experimento 3:
    * **Conectividade / CORS (Infraestrutura):** A IA diagnosticou corretamente a causa do erro de 'Connection Refused' ou 'CORS'. Ela configurou perfeitamente o objeto `proxy` no `vite.config.ts` (`target: 'http://localhost:8001'`), o que permite que o frontend faça chamadas relativas (`/api/...`) contornando as restrições de mesma origem do navegador sem precisar alterar as políticas do backend Python.
    * **Tratamento de Erros (UX):** A IA não deixou a tela ficar "em branco" em caso de falha. Ela construiu blocos de alertas visuais (`{error && <div className="alert alert-error">{error}</div>}`) com classes CSS dedicadas (`.alert-error { background-color: #fee; color: #c33; }`). As requisições na camada de serviço (`api.ts`) capturam `response.status === 401` e redirecionam graciosamente o usuário, além de extrair a mensagem `detail` do backend para exibir na interface.
    * **UX Geral:** Inclusão de estados de "loading", botões desabilitados quando dados obrigatórios faltam (ex: mapeamento incompleto), e restrição nativa de arquivo no input (`accept=".csv"`).

