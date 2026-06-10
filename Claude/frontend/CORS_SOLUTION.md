# 🔧 Solução de CORS e ConnectionRefused

## Problema

Você está recebendo erros de:
- `ConnectionRefused` - Não consegue conectar na API
- `CORS` - Erro de Cross-Origin Resource Sharing

## Causa

O React roda na porta **5173** e a API roda na porta **8001**. Browsers bloqueiam requisições entre portas diferentes por segurança (CORS).

## Solução (SEM MEXER NO PYTHON)

### 1. Proxy do Vite (Recomendado)

Já foi configurado em `vite.config.ts`:

```typescript
server: {
  port: 5173,
  proxy: {
    '/api': {
      target: 'http://localhost:8001',
      changeOrigin: true,
      rewrite: (path) => path.replace(/^\/api/, '/api'),
    },
  },
}
```

**Como funciona:**
- Requisições para `/api/*` são redirecionadas para `http://localhost:8001/api/*`
- O proxy roda no servidor de desenvolvimento (mesma origem)
- Não há CORS porque tudo vem da mesma porta

### 2. Arquivo .env

Já foi criado em `frontend/.env`:

```
VITE_API_URL=http://localhost:8001/api
```

### 3. Serviço de API

Já foi criado em `frontend/src/services/api.ts`:

```typescript
const API_URL = '/api'; // Uses proxy from vite.config.ts
```

**Importante:** Usa `/api` (relativo) em vez de `http://localhost:8001/api` (absoluto)

## Como Usar

### Passo 1: Instalar Dependências

```bash
cd frontend
npm install
```

### Passo 2: Iniciar o Servidor de Desenvolvimento

```bash
npm run dev
```

**Saída esperada:**
```
  VITE v8.0.12  ready in 123 ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

### Passo 3: Verificar Proxy

Abra o DevTools (F12) → Network → Faça login

**Você deve ver:**
- Requisição para `/api/auth/login`
- Status: 200 (sucesso)
- Sem erros de CORS

## Fluxo de Requisição

```
React (5173)
    ↓
Proxy Vite (5173)
    ↓
API Python (8001)
    ↓
Resposta volta para React
```

## Troubleshooting

### Erro: "Cannot GET /api/auth/login"

**Causa:** Proxy não está funcionando

**Solução:**
1. Verifique se `vite.config.ts` existe
2. Reinicie o servidor: `npm run dev`
3. Limpe cache: `npm run dev -- --force`

### Erro: "Connection refused"

**Causa:** API Python não está rodando

**Solução:**
1. Verifique se backend está rodando: `http://localhost:8001/docs`
2. Se não, inicie: `uvicorn main:app --reload --port 8001`

### Erro: "CORS error"

**Causa:** Proxy não está sendo usado

**Solução:**
1. Verifique se está usando `/api` (relativo) em vez de `http://localhost:8001/api`
2. Verifique `frontend/src/services/api.ts` linha 1:
   ```typescript
   const API_URL = '/api'; // ✅ Correto
   // const API_URL = 'http://localhost:8001/api'; // ❌ Errado
   ```

## Alternativas (Se Proxy Não Funcionar)

### Opção 1: CORS no Backend (Requer Mudança no Python)

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Opção 2: Usar Fetch com Credenciais

```typescript
fetch('/api/auth/login', {
  method: 'POST',
  credentials: 'include', // Incluir cookies
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ email, password }),
})
```

## Verificação Final

1. ✅ Backend rodando em `http://localhost:8001`
2. ✅ Frontend rodando em `http://localhost:5173`
3. ✅ `vite.config.ts` com proxy configurado
4. ✅ `frontend/src/services/api.ts` usando `/api` (relativo)
5. ✅ Sem erros de CORS no DevTools

## Resumo

| Problema | Solução |
|----------|---------|
| ConnectionRefused | Iniciar backend: `uvicorn main:app --reload --port 8001` |
| CORS Error | Usar proxy do Vite (já configurado) |
| Proxy não funciona | Reiniciar: `npm run dev` |
| Requisições lentas | Verificar se backend está respondendo |

## Próximos Passos

1. Iniciar backend: `uvicorn main:app --reload --port 8001`
2. Iniciar frontend: `npm run dev`
3. Abrir `http://localhost:5173`
4. Fazer login
5. Upload de CSV
6. Ver gráficos

Tudo deve funcionar sem erros de CORS! 🎉
