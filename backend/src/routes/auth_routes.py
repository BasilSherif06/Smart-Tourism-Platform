from fastapi import APIRouter, Depends, HTTPException, status

from src.core.security import create_access_token
from src.models.user import User
from src.routes.dependencies import get_current_user, get_user_service
from src.schemas.user import Token, UserCreate, UserLogin, UserResponse
from src.services.user_service import (
    EmailAlreadyRegisteredError,
    InvalidCredentialsError,
    UserService,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def signup(
        data: UserCreate,
        service: UserService = Depends(get_user_service),
):
    try:
        return service.signup(data)
    except EmailAlreadyRegisteredError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )


@router.post("/login", response_model=Token)
def login(
        data: UserLogin,
        service: UserService = Depends(get_user_service),
):
    try:
        user = service.authenticate(data)
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return Token(
        access_token=create_access_token(subject=str(user.user_id)),
        token_type="bearer",
    )


@router.get("/me", response_model=UserResponse)
def get_me(user: User = Depends(get_current_user)):
    return user