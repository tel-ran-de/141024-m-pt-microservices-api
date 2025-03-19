from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
import schemas
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer

# Секретный ключ для подписи JWT (должен быть надежным и храниться в безопасности)
SECRET_KEY = "your_very_secure_secret_key"
ALGORITHM = "HS256"
oauth2_scheme = HTTPBearer()


def get_token_data(
        token = Depends(oauth2_scheme)
) -> schemas.TokenData:
    """
    Проверяет JWT токен и возвращает данные пользователя.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Декодируем токен
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
