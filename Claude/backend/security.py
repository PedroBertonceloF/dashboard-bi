"""
Complete security module with JWT tokens and bcrypt password hashing.
Implements best practices for authentication and authorization.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import os
import jwt
import bcrypt
from pydantic import BaseModel, Field

# ============================================================================
# CONFIGURATION
# ============================================================================

# Secret key for JWT signing (should be loaded from environment in production)
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")

# JWT algorithm
ALGORITHM = "HS256"

# Token expiration time (30 minutes)
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Bcrypt rounds for password hashing (12 is good balance between security and speed)
BCRYPT_ROUNDS = 12

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class TokenData(BaseModel):
    """Data contained in JWT token"""
    user_id: int
    email: str
    exp: datetime = Field(description="Token expiration time")
    iat: datetime = Field(description="Token issued at time")


class TokenPayload(BaseModel):
    """Payload structure for JWT token"""
    sub: str  # user_id as string
    email: str
    exp: Optional[int] = None
    iat: Optional[int] = None


# ============================================================================
# PASSWORD HASHING FUNCTIONS
# ============================================================================

def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password (bcrypt hash)
        
    Security notes:
    - Uses 12 rounds of bcrypt (configurable in BCRYPT_ROUNDS)
    - Automatically generates and includes salt
    - Deterministic: same password always produces different hash (due to salt)
    - Bcrypt has a 72-byte limit, so we truncate longer passwords
    """
    if not password or len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")
    
    # Bcrypt has a 72-byte limit, truncate if necessary
    password_bytes = password[:72].encode('utf-8')
    
    # Hash password with bcrypt
    salt = bcrypt.gensalt(rounds=BCRYPT_ROUNDS)
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a bcrypt hash.
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Bcrypt hash to verify against
        
    Returns:
        True if password matches, False otherwise
        
    Security notes:
    - Uses constant-time comparison to prevent timing attacks
    - Returns False for any exception (invalid hash format, etc.)
    """
    try:
        # Bcrypt has a 72-byte limit, truncate if necessary
        password_bytes = plain_password[:72].encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception:
        # Log this in production - could indicate tampering
        return False


# ============================================================================
# JWT TOKEN FUNCTIONS
# ============================================================================

def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Dictionary with token claims (must include 'sub' for user_id)
        expires_delta: Custom expiration time (defaults to 30 minutes)
        
    Returns:
        Encoded JWT token as string
        
    Security notes:
    - Tokens expire after 30 minutes by default
    - Uses HS256 algorithm with SECRET_KEY
    - Includes 'iat' (issued at) and 'exp' (expiration) claims
    - Should be transmitted over HTTPS only
    """
    to_encode = data.copy()
    
    # Set expiration time
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Add standard JWT claims
    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc)
    })
    
    # Encode token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


def decode_access_token(token: str) -> Optional[TokenPayload]:
    """
    Decode and validate a JWT access token.
    
    Args:
        token: JWT token string
        
    Returns:
        TokenPayload if valid, None if invalid or expired
        
    Security notes:
    - Validates signature using SECRET_KEY
    - Checks expiration time
    - Returns None for any validation error (invalid signature, expired, malformed)
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Validate required claims
        user_id: str = payload.get("sub")
        email: str = payload.get("email")
        
        if user_id is None or email is None:
            return None
        
        return TokenPayload(
            sub=user_id,
            email=email,
            exp=payload.get("exp"),
            iat=payload.get("iat")
        )
    except jwt.ExpiredSignatureError:
        # Token has expired
        return None
    except jwt.InvalidTokenError:
        # Invalid token (bad signature, malformed, etc.)
        return None
    except Exception:
        # Catch any other exceptions
        return None


def refresh_access_token(token: str) -> Optional[str]:
    """
    Refresh an access token (create a new one with same claims).
    
    Args:
        token: Current JWT token
        
    Returns:
        New JWT token if current token is valid, None otherwise
        
    Security notes:
    - Only works if current token is still valid (not expired)
    - Creates a completely new token with fresh expiration
    - In production, consider implementing refresh tokens separately
    """
    payload = decode_access_token(token)
    
    if payload is None:
        return None
    
    # Create new token with same claims
    new_token = create_access_token(
        data={
            "sub": payload.sub,
            "email": payload.email
        }
    )
    
    return new_token


# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_email(email: str) -> bool:
    """
    Basic email validation.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if email format is valid
        
    Note:
    - This is basic validation only
    - For production, use email-validator library
    """
    if not email or len(email) > 254:
        return False
    
    # Basic format check
    if "@" not in email or "." not in email.split("@")[-1]:
        return False
    
    # Check for invalid characters
    invalid_chars = ['<', '>', '"', "'", '\\', '/', ' ']
    if any(char in email for char in invalid_chars):
        return False
    
    return True


def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Validate password strength.
    
    Args:
        password: Password to validate
        
    Returns:
        Tuple of (is_valid, message)
        
    Requirements:
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    """
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


# ============================================================================
# SECURITY UTILITIES
# ============================================================================

def get_token_expiration_time(token: str) -> Optional[datetime]:
    """
    Get the expiration time of a token.
    
    Args:
        token: JWT token
        
    Returns:
        Expiration datetime if valid, None otherwise
    """
    payload = decode_access_token(token)
    
    if payload is None or payload.exp is None:
        return None
    
    try:
        return datetime.fromtimestamp(payload.exp, tz=timezone.utc)
    except Exception:
        return None


def is_token_expired(token: str) -> bool:
    """
    Check if a token is expired.
    
    Args:
        token: JWT token
        
    Returns:
        True if token is expired or invalid, False if still valid
    """
    expiration = get_token_expiration_time(token)
    
    if expiration is None:
        return True
    
    return datetime.now(timezone.utc) >= expiration


def get_token_remaining_time(token: str) -> Optional[timedelta]:
    """
    Get remaining time until token expiration.
    
    Args:
        token: JWT token
        
    Returns:
        Remaining time as timedelta, None if token is invalid or expired
    """
    expiration = get_token_expiration_time(token)
    
    if expiration is None:
        return None
    
    remaining = expiration - datetime.now(timezone.utc)
    
    if remaining.total_seconds() <= 0:
        return None
    
    return remaining


# ============================================================================
# SECURITY HEADERS
# ============================================================================

def get_security_headers() -> Dict[str, str]:
    """
    Get recommended security headers for HTTP responses.
    
    Returns:
        Dictionary of security headers
        
    Headers included:
    - X-Content-Type-Options: Prevent MIME type sniffing
    - X-Frame-Options: Prevent clickjacking
    - X-XSS-Protection: Enable XSS protection
    - Strict-Transport-Security: Force HTTPS
    - Content-Security-Policy: Prevent XSS and injection attacks
    """
    return {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'",
    }
