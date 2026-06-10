"""
Exemplos práticos de como usar o módulo de segurança.
Copie e adapte esses exemplos para seu código.
"""

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import security
import models
from database import get_db

app = FastAPI()

# ============================================================================
# EXEMPLO 1: REGISTRO COM VALIDAÇÃO DE FORÇA DE SENHA
# ============================================================================

class UserCreate(BaseModel):
    email: str
    password: str

@app.post("/api/auth/register")
def register_with_validation(user: UserCreate, db: Session = Depends(get_db)):
    """
    Registro com validação completa de segurança.
    """
    # 1. Validar email
    if not security.validate_email(user.email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    
    # 2. Validar força de senha
    is_valid, message = security.validate_password_strength(user.password)
    if not is_valid:
        raise HTTPException(status_code=400, detail=message)
    
    # 3. Verificar se email já existe
    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 4. Hash de senha
    hashed_password = security.get_password_hash(user.password)
    
    # 5. Criar usuário
    new_user = models.User(
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"id": new_user.id, "email": new_user.email}


# ============================================================================
# EXEMPLO 2: LOGIN COM VERIFICAÇÃO DE SENHA
# ============================================================================

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

@app.post("/api/auth/login", response_model=Token)
def login_with_verification(user: UserLogin, db: Session = Depends(get_db)):
    """
    Login com verificação de senha e geração de JWT.
    """
    # 1. Buscar usuário por email
    db_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()
    
    # 2. Verificar se usuário existe e senha está correta
    if not db_user or not security.verify_password(
        user.password, 
        db_user.hashed_password
    ):
        # Mensagem genérica (não revela se email existe)
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # 3. Criar JWT token
    access_token = security.create_access_token(
        data={
            "sub": str(db_user.id),
            "email": db_user.email
        }
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# ============================================================================
# EXEMPLO 3: PROTEÇÃO DE ENDPOINTS COM JWT
# ============================================================================

def get_current_user(
    token: str = Depends(security.oauth2_scheme),
    db: Session = Depends(get_db)
) -> models.User:
    """
    Dependency para proteger endpoints com JWT.
    """
    # 1. Decodificar token
    payload = security.decode_access_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # 2. Buscar usuário no banco
    user_id = int(payload.sub)
    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user

@app.get("/api/users/me")
def get_current_user_info(current_user: models.User = Depends(get_current_user)):
    """
    Endpoint protegido que retorna informações do usuário atual.
    """
    return {
        "id": current_user.id,
        "email": current_user.email
    }


# ============================================================================
# EXEMPLO 4: REFRESH DE TOKEN
# ============================================================================

@app.post("/api/auth/refresh", response_model=Token)
def refresh_token(
    current_user: models.User = Depends(get_current_user)
):
    """
    Endpoint para renovar token expirado.
    """
    # Criar novo token com mesmos dados
    new_token = security.create_access_token(
        data={
            "sub": str(current_user.id),
            "email": current_user.email
        }
    )
    
    return {
        "access_token": new_token,
        "token_type": "bearer"
    }


# ============================================================================
# EXEMPLO 5: VERIFICAR EXPIRAÇÃO DE TOKEN
# ============================================================================

@app.get("/api/auth/token-info")
def get_token_info(current_user: models.User = Depends(get_current_user)):
    """
    Endpoint para obter informações sobre o token atual.
    """
    # Obter token do header (você precisa passar isso)
    # Este é apenas um exemplo de como usar as funções
    
    return {
        "user_id": current_user.id,
        "email": current_user.email,
        "message": "Token is valid"
    }


# ============================================================================
# EXEMPLO 6: MIDDLEWARE PARA ADICIONAR SECURITY HEADERS
# ============================================================================

@app.middleware("http")
async def add_security_headers(request, call_next):
    """
    Middleware para adicionar security headers em todas as respostas.
    """
    response = await call_next(request)
    
    # Obter headers de segurança
    headers = security.get_security_headers()
    
    # Adicionar headers à resposta
    for key, value in headers.items():
        response.headers[key] = value
    
    return response


# ============================================================================
# EXEMPLO 7: VALIDAÇÃO DE FORÇA DE SENHA CUSTOMIZADA
# ============================================================================

@app.post("/api/auth/validate-password")
def validate_password_endpoint(password: str):
    """
    Endpoint para validar força de senha (útil para frontend).
    """
    is_valid, message = security.validate_password_strength(password)
    
    return {
        "is_valid": is_valid,
        "message": message
    }


# ============================================================================
# EXEMPLO 8: MUDANÇA DE SENHA
# ============================================================================

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

@app.post("/api/auth/change-password")
def change_password(
    request: ChangePasswordRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Endpoint para mudar senha do usuário.
    """
    # 1. Verificar senha antiga
    if not security.verify_password(request.old_password, current_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid current password")
    
    # 2. Validar força da nova senha
    is_valid, message = security.validate_password_strength(request.new_password)
    if not is_valid:
        raise HTTPException(status_code=400, detail=message)
    
    # 3. Verificar que nova senha é diferente da antiga
    if request.old_password == request.new_password:
        raise HTTPException(
            status_code=400,
            detail="New password must be different from old password"
        )
    
    # 4. Hash da nova senha
    new_hashed = security.get_password_hash(request.new_password)
    
    # 5. Atualizar no banco
    current_user.hashed_password = new_hashed
    db.commit()
    
    return {"message": "Password changed successfully"}


# ============================================================================
# EXEMPLO 9: LOGGING DE TENTATIVAS DE LOGIN
# ============================================================================

import logging

logger = logging.getLogger(__name__)

@app.post("/api/auth/login-with-logging", response_model=Token)
def login_with_logging(user: UserLogin, db: Session = Depends(get_db)):
    """
    Login com logging de tentativas.
    """
    # 1. Buscar usuário
    db_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()
    
    # 2. Verificar credenciais
    if not db_user or not security.verify_password(
        user.password,
        db_user.hashed_password
    ):
        # Log de falha
        logger.warning(f"Failed login attempt for email: {user.email}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # 3. Log de sucesso
    logger.info(f"Successful login for user: {user.email}")
    
    # 4. Criar token
    access_token = security.create_access_token(
        data={
            "sub": str(db_user.id),
            "email": db_user.email
        }
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# ============================================================================
# EXEMPLO 10: RATE LIMITING NO LOGIN
# ============================================================================

# Instalar: pip install slowapi

from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/auth/login-with-rate-limit", response_model=Token)
@limiter.limit("5/minute")  # Máximo 5 tentativas por minuto
def login_with_rate_limit(
    request,  # Necessário para rate limiting
    user: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Login com rate limiting (máximo 5 tentativas por minuto).
    """
    db_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()
    
    if not db_user or not security.verify_password(
        user.password,
        db_user.hashed_password
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = security.create_access_token(
        data={
            "sub": str(db_user.id),
            "email": db_user.email
        }
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# ============================================================================
# NOTAS IMPORTANTES
# ============================================================================

"""
1. SEMPRE use HTTPS em produção
   - Tokens JWT são enviados no header Authorization
   - Sem HTTPS, tokens podem ser interceptados

2. NUNCA exponha informações sensíveis em mensagens de erro
   - Use mensagens genéricas como "Invalid credentials"
   - Não diga "Email not found" ou "Password incorrect"

3. SEMPRE valide força de senha no registro
   - Use validate_password_strength()
   - Rejeite senhas fracas

4. SEMPRE use rate limiting no login
   - Protege contra brute force attacks
   - Máximo 5 tentativas por minuto é recomendado

5. SEMPRE faça logging de tentativas de login
   - Ajuda a detectar ataques
   - Importante para auditoria

6. SEMPRE use SQLAlchemy ORM
   - Protege contra SQL Injection
   - Nunca use raw SQL com concatenação de strings

7. SEMPRE adicione security headers
   - Protege contra XSS, clickjacking, etc.
   - Use get_security_headers()

8. SEMPRE use bcrypt para hash de senha
   - Nunca use MD5, SHA1, ou SHA256 simples
   - Bcrypt é lento (proteção contra brute force)

9. SEMPRE use JWT com expiração
   - 30 minutos é um bom padrão
   - Implemente refresh tokens para melhor UX

10. SEMPRE teste segurança
    - Execute pytest tests/test_security.py
    - Todos os 31 testes devem passar
"""
