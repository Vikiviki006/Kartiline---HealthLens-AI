"""
Encryption utility for sensitive PII data like User Identifiers.
"""
import os
from cryptography.fernet import Fernet
from app.utils.logger import logger

# Try to get from env, otherwise use a fallback for dev mode ONLY
_KEY = os.getenv("ENCRYPTION_KEY", Fernet.generate_key().decode())
fernet = Fernet(_KEY.encode())

def encrypt_id(identifier: str) -> str:
    """Encrypts a string identifier."""
    if not identifier:
        return ""
    try:
        return fernet.encrypt(identifier.encode()).decode()
    except Exception as e:
        logger.error(f"Failed to encrypt identifier: {e}")
        return ""

def decrypt_id(encrypted_identifier: str) -> str:
    """Decrypts a string identifier."""
    if not encrypted_identifier:
        return ""
    try:
        return fernet.decrypt(encrypted_identifier.encode()).decode()
    except Exception as e:
        logger.error(f"Failed to decrypt identifier: {e}")
        return ""
