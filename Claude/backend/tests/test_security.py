"""
Tests for the security module.
Tests password hashing, JWT tokens, and validation functions.
"""

import pytest
from datetime import timedelta
import time
import security


class TestPasswordHashing:
    """Test password hashing and verification"""
    
    def test_hash_password(self):
        """Test that password is hashed correctly"""
        password = "SecurePass123!"
        hashed = security.get_password_hash(password)
        
        # Hash should not be the same as password
        assert hashed != password
        
        # Hash should be a string
        assert isinstance(hashed, str)
        
        # Hash should contain bcrypt prefix
        assert hashed.startswith("$2b$")
    
    def test_verify_correct_password(self):
        """Test that correct password verifies"""
        password = "SecurePass123!"
        hashed = security.get_password_hash(password)
        
        assert security.verify_password(password, hashed) is True
    
    def test_verify_incorrect_password(self):
        """Test that incorrect password fails verification"""
        password = "SecurePass123!"
        wrong_password = "WrongPass123!"
        hashed = security.get_password_hash(password)
        
        assert security.verify_password(wrong_password, hashed) is False
    
    def test_hash_is_unique(self):
        """Test that same password produces different hashes (due to salt)"""
        password = "SecurePass123!"
        hash1 = security.get_password_hash(password)
        hash2 = security.get_password_hash(password)
        
        # Hashes should be different (different salts)
        assert hash1 != hash2
        
        # But both should verify the same password
        assert security.verify_password(password, hash1) is True
        assert security.verify_password(password, hash2) is True
    
    def test_password_too_short(self):
        """Test that short passwords are rejected"""
        with pytest.raises(ValueError):
            security.get_password_hash("short")
    
    def test_verify_invalid_hash(self):
        """Test that invalid hash returns False"""
        assert security.verify_password("password", "invalid_hash") is False


class TestJWTTokens:
    """Test JWT token creation and validation"""
    
    def test_create_token(self):
        """Test that token is created correctly"""
        data = {"sub": "1", "email": "test@example.com"}
        token = security.create_access_token(data)
        
        # Token should be a string
        assert isinstance(token, str)
        
        # Token should have 3 parts (header.payload.signature)
        assert token.count(".") == 2
    
    def test_decode_valid_token(self):
        """Test that valid token is decoded correctly"""
        data = {"sub": "1", "email": "test@example.com"}
        token = security.create_access_token(data)
        
        payload = security.decode_access_token(token)
        
        assert payload is not None
        assert payload.sub == "1"
        assert payload.email == "test@example.com"
    
    def test_decode_invalid_token(self):
        """Test that invalid token returns None"""
        invalid_token = "invalid.token.here"
        payload = security.decode_access_token(invalid_token)
        
        assert payload is None
    
    def test_decode_expired_token(self):
        """Test that expired token returns None"""
        data = {"sub": "1", "email": "test@example.com"}
        # Create token that expires immediately
        token = security.create_access_token(data, expires_delta=timedelta(seconds=-1))
        
        # Wait a bit to ensure expiration
        time.sleep(0.1)
        
        payload = security.decode_access_token(token)
        
        assert payload is None
    
    def test_token_contains_claims(self):
        """Test that token contains required claims"""
        data = {"sub": "1", "email": "test@example.com"}
        token = security.create_access_token(data)
        
        payload = security.decode_access_token(token)
        
        # Should have exp and iat claims
        assert payload.exp is not None
        assert payload.iat is not None
    
    def test_custom_expiration(self):
        """Test that custom expiration is respected"""
        data = {"sub": "1", "email": "test@example.com"}
        expires_delta = timedelta(hours=1)
        token = security.create_access_token(data, expires_delta=expires_delta)
        
        payload = security.decode_access_token(token)
        
        assert payload is not None
        # Token should be valid
        assert security.is_token_expired(token) is False


class TestPasswordValidation:
    """Test password strength validation"""
    
    def test_valid_strong_password(self):
        """Test that strong password passes validation"""
        password = "SecurePass123!"
        is_valid, message = security.validate_password_strength(password)
        
        assert is_valid is True
    
    def test_password_too_short(self):
        """Test that short password fails"""
        password = "Short1!"
        is_valid, message = security.validate_password_strength(password)
        
        assert is_valid is False
        assert "8 characters" in message
    
    def test_password_no_uppercase(self):
        """Test that password without uppercase fails"""
        password = "securepass123!"
        is_valid, message = security.validate_password_strength(password)
        
        assert is_valid is False
        assert "uppercase" in message
    
    def test_password_no_lowercase(self):
        """Test that password without lowercase fails"""
        password = "SECUREPASS123!"
        is_valid, message = security.validate_password_strength(password)
        
        assert is_valid is False
        assert "lowercase" in message
    
    def test_password_no_digit(self):
        """Test that password without digit fails"""
        password = "SecurePass!"
        is_valid, message = security.validate_password_strength(password)
        
        assert is_valid is False
        assert "digit" in message
    
    def test_password_no_special_char(self):
        """Test that password without special character fails"""
        password = "SecurePass123"
        is_valid, message = security.validate_password_strength(password)
        
        assert is_valid is False
        assert "special character" in message
    
    def test_password_too_long(self):
        """Test that very long password fails"""
        password = "A" * 129 + "a1!"
        is_valid, message = security.validate_password_strength(password)
        
        assert is_valid is False
        assert "128 characters" in message


class TestEmailValidation:
    """Test email validation"""
    
    def test_valid_email(self):
        """Test that valid email passes"""
        assert security.validate_email("user@example.com") is True
    
    def test_email_without_at(self):
        """Test that email without @ fails"""
        assert security.validate_email("userexample.com") is False
    
    def test_email_without_dot(self):
        """Test that email without dot fails"""
        assert security.validate_email("user@example") is False
    
    def test_email_with_spaces(self):
        """Test that email with spaces fails"""
        assert security.validate_email("user @example.com") is False
    
    def test_empty_email(self):
        """Test that empty email fails"""
        assert security.validate_email("") is False
    
    def test_email_too_long(self):
        """Test that very long email fails"""
        long_email = "a" * 250 + "@example.com"
        assert security.validate_email(long_email) is False


class TestTokenUtilities:
    """Test token utility functions"""
    
    def test_is_token_expired_valid(self):
        """Test that valid token is not expired"""
        data = {"sub": "1", "email": "test@example.com"}
        token = security.create_access_token(data)
        
        assert security.is_token_expired(token) is False
    
    def test_is_token_expired_invalid(self):
        """Test that invalid token is considered expired"""
        assert security.is_token_expired("invalid.token") is True
    
    def test_get_token_remaining_time(self):
        """Test that remaining time is calculated correctly"""
        data = {"sub": "1", "email": "test@example.com"}
        token = security.create_access_token(data)
        
        remaining = security.get_token_remaining_time(token)
        
        assert remaining is not None
        # Should be close to 30 minutes
        assert remaining.total_seconds() > 29 * 60
        assert remaining.total_seconds() <= 30 * 60
    
    def test_refresh_token(self):
        """Test that token can be refreshed"""
        data = {"sub": "1", "email": "test@example.com"}
        token = security.create_access_token(data)
        
        # Wait a tiny bit to ensure different iat
        time.sleep(0.01)
        
        new_token = security.refresh_access_token(token)
        
        assert new_token is not None
        # Tokens might be the same if created too quickly, so just verify it's valid
        
        # New token should be valid
        payload = security.decode_access_token(new_token)
        assert payload is not None
        assert payload.sub == "1"


class TestSecurityHeaders:
    """Test security headers"""
    
    def test_security_headers_present(self):
        """Test that all security headers are present"""
        headers = security.get_security_headers()
        
        assert "X-Content-Type-Options" in headers
        assert "X-Frame-Options" in headers
        assert "X-XSS-Protection" in headers
        assert "Strict-Transport-Security" in headers
        assert "Content-Security-Policy" in headers
    
    def test_security_headers_values(self):
        """Test that security headers have correct values"""
        headers = security.get_security_headers()
        
        assert headers["X-Content-Type-Options"] == "nosniff"
        assert headers["X-Frame-Options"] == "DENY"
        assert "1; mode=block" in headers["X-XSS-Protection"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
