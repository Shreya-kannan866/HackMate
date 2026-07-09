from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# 1. REGISTER ENDPOINT
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """Takes username, email, and password -> hashes it -> saves to DB."""
    return UserService.register_user(db=db, user_data=user_in)

# 2. LOGIN ENDPOINT
@router.post("/login", status_code=status.HTTP_200_OK)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Takes username and password -> verifies it -> returns a token."""
    return {"message": "Login logic goes here"}