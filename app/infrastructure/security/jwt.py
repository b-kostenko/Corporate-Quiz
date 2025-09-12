from datetime import datetime, timedelta, timezone
from typing import Dict

import jwt

from app.core.schemas.user_schemas import TokenType
from app.settings import settings


def create_token(payload: Dict, token_type: TokenType, expire_minutes: int) -> str:
    to_encode = payload.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
    to_encode.update({"exp": expire, "type": token_type})
    return jwt.encode(to_encode, settings.token.SECRET_KEY, algorithm=settings.token.ALGORITHM)

def decode_token(token: str, key: str, options: dict, algorithms: list[str] = None) -> Dict:
    try:
        payload = jwt.decode(jwt=token, key=key, algorithms=algorithms, options=options)
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")


def verify_token(token: str, token_type: TokenType) -> bool:
    try:
        payload = decode_token(token=token, key=settings.token.SECRET_KEY, algorithms=[settings.token.ALGORITHM], options={})
        if payload.get("type") != token_type:
            raise ValueError("Invalid token type")
        return True
    except ValueError as e:
        print(f"Token verification failed: {e}")
        return False
