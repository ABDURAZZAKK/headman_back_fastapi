from models.token import Login, Token
from repositories.userRepo import UserRepository
from core.security import create_access_token, verify_password
from .depends import get_user_repository
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(login: Login, users: UserRepository = Depends(get_user_repository)):
    user = await users.get_by_email(login.email)
    if user is None or not verify_password(login.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    return Token(
        access_token=create_access_token({"sub": user.email}), token_type="Bearer"
    )
