from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate
from app.models.user import User
# We will use a library like passlib or bcrypt for password hashing
from passlib.context import CryptContext

# Set up the password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    @staticmethod
    def hash_password(password: str) -> str:
        """Convert plain text password into a secure, unreadable hash."""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify if a login password matches the stored hash."""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def register_user(db: Session, user_data: UserCreate) -> User:
        """Handle business logic for registering a new user."""
        
        # 1. Check if the email is already registered
        existing_email = UserRepository.get_by_email(db, email=user_data.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already registered"
            )

        # 2. Check if the username is already taken
        existing_username = UserRepository.get_by_username(db, username=user_data.username)
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username is already taken"
            )

        # 3. Hash the raw password securely
        hashed_pwd = UserService.hash_password(user_data.password)

        # 4. Save the user to the database via the Repository
        new_user = UserRepository.create(db, user_data=user_data, hashed_password=hashed_pwd)
        
        return new_user