from fastapi import APIRouter, HTTPException, Depends
from models.user import User
from schemas.user import UserCreate, UserInDB, Token
from utils.auth import authenticate_user, create_access_token, get_current_user
from tortoise.contrib.fastapi import HTTPNotFoundError
from utils.auth import get_password_hash

router = APIRouter()

@router.post("/register", response_model=UserInDB)
async def register_user(user: UserCreate):
    if await User.filter(username=user.username).exists():
        raise HTTPException(status_code=400, detail="Username already registered")
    
    password_hash = get_password_hash(user.password)  
    new_user = await User.create(username=user.username, password_hash=password_hash)
    return new_user

@router.post("/login", response_model=Token)
async def login_for_access_token(user: UserCreate):
    db_user = await authenticate_user(user.username, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token({"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
