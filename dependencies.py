from fastapi import Header, HTTPException
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


async def verify_token(authorization: str = Header(...)):
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")
        if token != os.environ.get("API_KEY"):
            raise HTTPException(status_code=401, detail="Invalid token")
    except (ValueError, KeyError):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
