from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import os
import jwt
import bcrypt
from pydantic import BaseModel, Field

# ============================================================================
# CONFIGURATION
# ============================================================================

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
BCRYPT_ROUNDS = 12

class TokenData(BaseModel):
    user_id: int
    email: str
    exp: datetime = Field(description="Token expiration time")
    iat: datetime = Field(description="Token issued at time")

class TokenPayload(BaseModel):
    sub: str
    email: str
    exp: Optional[int] = None
    iat: Optional[int] = None

def get_password_hash(password: str) -> str:
    if not password or len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")
    
    password_bytes = password[:72].encode('utf-8')
    salt = bcrypt.gensalt(rounds=BCRYPT_ROUNDS)
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        password_bytes = plain_password[:72].encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception:
        return False

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[TokenPayload]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        email: str = payload.get("email")
        if user_id is None or email is None:
            return None
        return TokenPayload(sub=user_id, email=email, exp=payload.get("exp"), iat=payload.get("iat"))
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    except Exception:
        return None

def refresh_access_token(token: str) -> Optional[str]:
    payload = decode_access_token(token)
    if payload is None:
        return None
    new_token = create_access_token(data={"sub": payload.sub, "email": payload.email})
    return new_token

def validate_email(email: str) -> bool:
    if not email or len(email) > 254:
        return False
    if "@" not in email or "." not in email.split("@")[-1]:
        return False
    invalid_chars = ['<', '>', '"', "'", '\\', '/', ' ']
    if any(char in email for char in invalid_chars):
        return False
    return True

def validate_password_strength(password: str) -> tuple[bool, str]:
    if not password:
        return False, "Password is required"
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if len(password) > 128:
        return False, "Password must be less than 128 characters"
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
    
    if not has_upper:
        return False, "Password must contain at least one uppercase letter"
    if not has_lower:
        return False, "Password must contain at least one lowercase letter"
    if not has_digit:
        return False, "Password must contain at least one digit"
    if not has_special:
        return False, "Password must contain at least one special character"
    
    return True, "Password is strong"

def get_token_expiration_time(token: str) -> Optional[datetime]:
    payload = decode_access_token(token)
    if payload is None or payload.exp is None:
        return None
    try:
        return datetime.fromtimestamp(payload.exp, tz=timezone.utc)
    except Exception:
        return None

def is_token_expired(token: str) -> bool:
    expiration = get_token_expiration_time(token)
    if expiration is None:
        return True
    return datetime.now(timezone.utc) >= expiration

def get_token_remaining_time(token: str) -> Optional[timedelta]:
    expiration = get_token_expiration_time(token)
    if expiration is None:
        return None
    remaining = expiration - datetime.now(timezone.utc)
    if remaining.total_seconds() <= 0:
        return None
    return remaining

def get_security_headers() -> Dict[str, str]:
    return {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'",
    }