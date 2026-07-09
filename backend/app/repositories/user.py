from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate  # We will define this schema next!

class UserRepository:
    @staticmethod
    def get_by_id(db: Session, user_id: int) -> User | None:
        """Fetch a single user by their primary ID key."""
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_by_email(db: Session, email: str) -> User | None:
        """Fetch a single user by their email (useful for checking duplicate signups)."""
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_by_username(db: Session, username: str) -> User | None:
        """Fetch a single user by their username (useful for logging in)."""
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def create(db: Session, user_data: UserCreate, hashed_password: str) -> User:
        """Insert a brand new user into the database."""
        db_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,  # Storing the secure hash, never raw text!
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)  # Refreshes db_user to include the newly generated ID
        return db_user