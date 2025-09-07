from datetime import datetime, timezone, timedelta

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from starlette import status

from app.security.models import UserLoginRequest
from jose import jwt, JWTError

from app.settings.settings import Setting

app_setting = Setting()

ROOT_USERNAME =  app_setting.ROOT_USERNAME
ROOT_PASSWORD = app_setting.ROOT_PASSWORD

SECRET_KEY = 'ETHIO89AHKAHAPOPWIRUVBKAAHHvhjkfklddfapoiwfa,fdf.eeeeddfdo09348723232323'
ALGORITHM = 'HS256'



bcrypt_context =  CryptContext(schemes=['bcrypt'], deprecated ='auto')
security = HTTPBearer()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def hash_password():
    return bcrypt_context.hash(app_setting.ROOT_PASSWORD)

def authenticate_password(raw_password:str, username:str):
    if ROOT_USERNAME == username:
        if bcrypt_context.verify(raw_password, ROOT_PASSWORD):
            return True
    return False

def handle_login(login_req: UserLoginRequest):
    if authenticate_password(login_req.raw_password, login_req.username):
        expire = datetime.now(timezone.utc) + timedelta(days=1)
        to_encode = {'sub': login_req.username, 'id': 1, "exp" :expire}  # default id is 1
        encoded_jwt =  jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)

        return encoded_jwt
    else:
        print(f"Wrong credentials")
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid username or password",
            headers= {"WWW-Authenticate": "Bearer"},
        )

def verify_token(auth: HTTPAuthorizationCredentials = Depends(security)):
    token = auth.credentials  # <-- extract token string

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp = payload.get("exp")
        if exp and datetime.now(timezone.utc) > datetime.fromtimestamp(exp, tz=timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )