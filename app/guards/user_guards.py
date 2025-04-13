from fastapi import Depends, HTTPException, Security 
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials 
from jose import jwt, JWTError 
from config.settings import settings
from enums.user_enums import Roles

security = HTTPBearer()

def user_guard(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=["HS256"])

        if not payload.get("user_id"):
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        return payload
    
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token or expired token")
        
        

