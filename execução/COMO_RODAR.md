# Instruções de Execução do Projeto

Para rodar o projeto corretamente, abra dois terminais separados e siga os passos abaixo:

---

## 1. Backend (Python / FastAPI)
**Local:** Pasta `backend`

1. Entre na pasta:
   ```cmd
   cd backend
   ```
2. Ative o ambiente virtual:
   ```cmd
   .\venv\Scripts\activate
   ```
3. Inicie o servidor:
   ```cmd
   uvicorn main:app --reload --port 8001
   ```
*O servidor estará rodando em: http://127.0.0.1:8001*

---

## 2. Frontend (React / Vite)
**Local:** Pasta `frontend`

1. Entre na pasta:
   ```cmd
   cd frontend
   ```
2. Inicie o servidor de desenvolvimento:
   ```cmd
   npm run dev
   ```
*A interface estará disponível em: http://localhost:5173*

---

## Observações Importantes:
- **Porta do Backend:** Note que estamos usando a porta **8001** para evitar conflitos com processos antigos do Windows.
- **Modo QuickEdit:** Se o backend parar de responder, clique no terminal e aperte `ESC` para destravar o modo de seleção do Windows.
