# ⚡ Quick Start - Dashboard React

## 🚀 Executar em 3 Passos

### Terminal 1: Backend
```bash
cd backend
uvicorn main:app --reload --port 8001
```

### Terminal 2: Frontend
```bash
cd frontend
npm install  # Primeira vez apenas
npm run dev
```

### Terminal 3: Browser
```
http://localhost:5173
```

## ✅ Pronto!

1. Faça login
2. Upload de CSV
3. Mapeie colunas (Data, Categoria, Valor)
4. Veja gráficos e KPIs

## 🔧 Problema de CORS?

**Já foi resolvido!** O proxy do Vite redireciona `/api/*` para `http://localhost:8001/api/*`

Sem necessidade de mexer no Python.

## 📊 O Que Você Tem

✅ Upload de CSV  
✅ Mapeamento de colunas  
✅ Limpeza automática de dados  
✅ KPIs (Total Sum, Average, Row Count)  
✅ Gráficos (Time Series, Categorias, Pizza)  
✅ Export de dados  

## 📁 Arquivos Criados

```
frontend/
├── .env                          # Variáveis de ambiente
├── vite.config.ts               # Proxy configurado
├── src/
│   ├── services/api.ts          # Serviço de API
│   ├── pages/Dashboard.tsx      # Dashboard
│   └── styles/Dashboard.css     # Estilos
├── CORS_SOLUTION.md             # Guia de CORS
└── DASHBOARD_GUIDE.md           # Guia do Dashboard
```

## 🐛 Troubleshooting

| Erro | Solução |
|------|---------|
| Connection refused | Inicie backend: `uvicorn main:app --reload --port 8001` |
| CORS error | Reinicie frontend: `npm run dev` |
| Gráficos não aparecem | Verifique se CSV tem dados válidos |

## 📚 Documentação

- `FRONTEND_SETUP.md` - Setup completo
- `frontend/CORS_SOLUTION.md` - Explicação de CORS
- `frontend/DASHBOARD_GUIDE.md` - Guia de uso

## 🎉 Pronto!

Tudo está configurado. Basta executar os 3 comandos acima e começar a usar!
