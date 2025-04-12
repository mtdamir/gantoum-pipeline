from fastapi import Depends, HTTPException 
from fastapi.security import OAuth2PasswordBearer 
from jose import jwt, JWTError 
from config.settings import settings

oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")

def user_guard(token:str = Depends(oauth_scheme)):
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=["HS256"])
        if not payload.get("user_id"):
            raise HTTPException(status_code=401, detail="Unauthorized")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token or expired token")
