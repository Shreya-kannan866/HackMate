from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db  # Note: adjust to app.database.base or session depending on your exact setup
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """Endpoint for user sign-up."""
    return UserService.register_user(db=db, user_data=user_in)

@router.post("/login", response_model=UserResponse, status_code=status.HTTP_200_OK)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Endpoint for user authentication."""
    user = UserService.authenticate_user(db=db, credentials=credentials)
    return user