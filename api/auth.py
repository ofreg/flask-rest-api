from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
from jose import jwt, JWTError
from api.models import users
from api.schemas import TokenResponse, TokenRefreshRequest, LoginRequest

SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

auth_router = APIRouter()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@auth_router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    user = users.get(request.username)
    if not user or user["password"] != request.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": request.username})
    refresh_token = create_refresh_token({"sub": request.username})
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)

@auth_router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: TokenRefreshRequest):
    try:
        payload = jwt.decode(request.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        access_token = create_access_token({"sub": username})
        refresh_token = create_refresh_token({"sub": username})
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
