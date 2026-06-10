# 🚀 Frontend Setup - React + Dashboard

## ✅ O Que Foi Criado

### Arquivos Principais

1. **`frontend/vite.config.ts`** - Configuração do Vite com proxy
2. **`frontend/.env`** - Variáveis de ambiente
3. **`frontend/src/services/api.ts`** - Serviço de API com tratamento de CORS
4. **`frontend/src/pages/Dashboard.tsx`** - Componente Dashboard completo
5. **`frontend/src/styles/Dashboard.css`** - Estilos do Dashboard

### Documentação

1. **`frontend/CORS_SOLUTION.md`** - Como resolver CORS sem mexer no Python
2. **`frontend/DASHBOARD_GUIDE.md`** - Guia de uso do Dashboard

## 🔧 Solução de CORS

### Problema
React (5173) ↔ API Python (8001) = CORS Error

### Solução
Proxy do Vite redireciona `/api/*` para `http://localhost:8001/api/*`

### Como Funciona
```
React (5173) → Proxy Vite (5173) → API Python (8001)
```

Sem CORS porque tudo vem da mesma porta!

## 📊 Dashboard Completo

### Funcionalidades

✅ **Upload de CSV**
- Selecione arquivo CSV
- Veja prévia dos dados
- Auto-detecta colunas

✅ **Mapeamento de Colunas**
- Selecione Data, Categoria, Valor
- Processa e limpa dados
- Remove linhas inválidas

✅ **KPIs**
- Total Sum (soma de valores)
- Average (média)
- Row Count (número de linhas)

✅ **Gráficos Interativos**
- Time Series (linha)
- By Category (barras)
- Category Distribution (pizza)

✅ **Export**
- Baixe dados processados como CSV

### Tecnologias

- **React 19** - Framework
- **Recharts** - Gráficos
- **TypeScript** - Tipagem
- **Vite** - Build tool
- **CSS3** - Estilos responsivos

## 🚀 Como Executar

### Passo 1: Instalar Dependências

```bash
cd frontend
npm install
```

### Passo 2: Iniciar Backend

```bash
cd backend
uvicorn main:app --reload --port 8001
```

**Saída esperada:**
```
INFO:     Uvicorn running on http://127.0.0.1:8001
```

### Passo 3: Iniciar Frontend

```bash
cd frontend
npm run dev
```

**Saída esperada:**
```
VITE v8.0.12  ready in 123 ms

  ➜  Local:   http://localhost:5173/
```

### Passo 4: Abrir no Browser

Acesse: `http://localhost:5173`

## 📋 Fluxo de Uso

1. **Login** - Faça login com suas credenciais
2. **Upload** - Selecione um arquivo CSV
3. **Mapping** - Mapeie as colunas (Data, Categoria, Valor)
4. **Process** - Clique em "Process Dataset"
5. **Dashboard** - Veja KPIs e gráficos
6. **Export** - Baixe dados processados

## 🔍 Verificação

### Backend Rodando?
```bash
curl http://localhost:8001/docs
```

### Frontend Rodando?
```bash
curl http://localhost:5173
```

### Proxy Funcionando?
Abra DevTools (F12) → Network → Faça login
Você deve ver requisições para `/api/auth/login` (não `http://localhost:8001/...`)

## 📁 Estrutura de Arquivos

```
frontend/
├── .env                          # Variáveis de ambiente
├── vite.config.ts               # Configuração do Vite com proxy
├── package.json                 # Dependências
├── src/
│   ├── services/
│   │   └── api.ts              # Serviço de API
│   ├── pages/
│   │   ├── Login.tsx           # Página de login
│   │   ├── Register.tsx        # Página de registro
│   │   └── Dashboard.tsx       # Dashboard (NOVO)
│   ├── styles/
│   │   └── Dashboard.css       # Estilos do Dashboard (NOVO)
│   ├── App.tsx                 # App principal
│   ├── AuthContext.tsx         # Contexto de autenticação
│   └── main.tsx                # Entry point
├── CORS_SOLUTION.md            # Guia de CORS (NOVO)
└── DASHBOARD_GUIDE.md          # Guia do Dashboard (NOVO)
```

## 🎨 Componentes do Dashboard

### Upload Section
- Input de arquivo CSV
- Prévia dos dados
- Auto-detecção de colunas

### Mapping Section
- Seletores para Date, Category, Value
- Botão de processamento
- Feedback de progresso

### Dashboard Section
- KPI Cards (Total Sum, Average, Row Count)
- Time Series Chart (Recharts LineChart)
- Category Chart (Recharts BarChart)
- Distribution Chart (Recharts PieChart)
- Export Button

## 🔐 Segurança

### Token JWT
- Armazenado em `localStorage`
- Enviado em header `Authorization: Bearer <token>`
- Auto-logout se expirar (401)

### CORS
- Proxy do Vite evita problemas de CORS
- Sem necessidade de configuração no backend

### Validação
- Email validado no backend
- Senha hasheada com bcrypt
- Tokens com expiração de 30 minutos

## 📊 Exemplo de CSV

```csv
Data,Categoria,Valor,Coluna_Extra
2024-01-01,Vendas,100.50,Extra1
2024-01-02,Vendas,200.00,Extra2
2024-01-03,Lucro,300.75,Extra3
2024-01-04,Vendas,150.25,Extra4
2024-01-05,Lucro,250.00,Extra5
```

**Resultado:**
- Total Sum: $1000.50
- Average: $200.10
- Row Count: 5
- Gráficos mostram tendências

## 🐛 Troubleshooting

### Erro: "Cannot GET /api/auth/login"
**Solução:** Reinicie frontend: `npm run dev`

### Erro: "Connection refused"
**Solução:** Inicie backend: `uvicorn main:app --reload --port 8001`

### Erro: "CORS error"
**Solução:** Verifique se está usando `/api` (relativo) em `api.ts`

### Gráficos não aparecem
**Solução:** Verifique se CSV tem dados válidos

## ✅ Checklist

- ✅ Backend rodando em 8001
- ✅ Frontend rodando em 5173
- ✅ Proxy configurado em vite.config.ts
- ✅ API service usando `/api` (relativo)
- ✅ Dashboard component criado
- ✅ Recharts instalado
- ✅ Sem erros de CORS

## 🎉 Pronto!

Tudo está configurado e pronto para usar!

1. Inicie backend: `uvicorn main:app --reload --port 8001`
2. Inicie frontend: `npm run dev`
3. Abra `http://localhost:5173`
4. Faça login
5. Upload de CSV
6. Veja gráficos

Aproveite! 🚀
