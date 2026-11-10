import jwt
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI,Request
from app.config import settings


def create_access_token(data):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expire})
    return jwt.encode(to_encode,settings.SECRET_KEY,algorithm = settings.ALGORITHM)

def create_refresh_token(data):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({'exp':expire})
    return jwt.encode(to_encode,settings.SECRET_KEY,algorithm = settings.ALGORITHM)

def decode_token(token):
    return jwt.decode(token,settings.SECRET_KEY,algorithms=settings.ALGORITHM)

def get_current_ip(request:Request):
    print(request.client.host)
    return request.client.host