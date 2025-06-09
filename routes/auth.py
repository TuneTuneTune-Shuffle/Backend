# This is the routes/auth.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from database import users_collection
from jwt_utils import hash_password, verify_password, create_access_token

router = APIRouter()

class UserIn(BaseModel):
    email: EmailStr
    password: str

@router.post("/signup")
async def signup(user: UserIn):
    if await users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=409, detail="Email already registered")

    hashed = hash_password(user.password)
    await users_collection.insert_one({"email": user.email, "hashed_password": hashed})

    token = create_access_token({"sub": user.email})
    return {"access_token": token, 
            "token_type": "bearer"}

@router.post("/login")
async def login(user: UserIn):
    existing_user = await users_collection.find_one({"email": user.email})
    if not existing_user or not verify_password(user.password, existing_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})
    return {"access_token": token, 
            "token_type": "bearer"}
